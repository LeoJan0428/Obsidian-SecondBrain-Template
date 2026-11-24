"""Behavioral tests for global pre-commit and commit-msg Git hooks."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

VAULT_ROOT = Path(__file__).resolve().parent.parent
PRE_COMMIT_HOOK = VAULT_ROOT / "00-AgentOS" / "hooks" / "pre-commit"
COMMIT_MSG_HOOK = VAULT_ROOT / "00-AgentOS" / "hooks" / "commit-msg"


def _find_bash() -> str:
    git_bash = Path(r"C:\Program Files\Git\bin\bash.exe")
    if git_bash.exists():
        return str(git_bash)
    found = shutil.which("bash")
    if found:
        return found
    pytest.skip("bash executable not available")
    return ""


def _init_repo(tmp_path: Path, name: str = "repo") -> Path:
    repo = tmp_path / name
    repo.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(
        ["git", "config", "core.hooksPath", PRE_COMMIT_HOOK.parent.as_posix()],
        cwd=repo,
        check=True,
    )
    return repo


def _run_hook(hook: Path, cwd: Path, args: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    bash = _find_bash()
    cmd = [bash, str(hook), *(args or [])]
    env = os.environ.copy()
    return subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True, check=False)


def test_pre_commit_blocks_secrets_env_and_plusplus_escape(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "secrets")

    # 1. .env blocked
    (repo / ".env").write_text("PORT=8080\n", encoding="utf-8")
    subprocess.run(["git", "add", ".env"], cwd=repo, check=True)
    res_env = _run_hook(PRE_COMMIT_HOOK, repo)
    assert res_env.returncode == 1
    subprocess.run(["git", "reset", "-q", "HEAD", "--", ".env"], cwd=repo, check=True)
    (repo / ".env").unlink()

    # 2. Synthetic API key + '+++' content prefix escape + ENCRYPTED PRIVATE KEY
    sk_secret = "sk-" + "1234567890" + "abcdefghij"
    enc_header = "-----BEGIN " + "ENCRYPTED PRIVATE KEY-----"
    (repo / "leak.py").write_text(f"TOKEN = '{sk_secret}'\n", encoding="utf-8")
    subprocess.run(["git", "add", "leak.py"], cwd=repo, check=True)
    assert _run_hook(PRE_COMMIT_HOOK, repo).returncode == 1
    subprocess.run(["git", "reset", "-q", "HEAD", "--", "leak.py"], cwd=repo, check=True)
    (repo / "leak.py").unlink()

    (repo / "plusplus.txt").write_text(f"++{sk_secret}\n", encoding="utf-8")
    subprocess.run(["git", "add", "plusplus.txt"], cwd=repo, check=True)
    assert _run_hook(PRE_COMMIT_HOOK, repo).returncode == 1
    subprocess.run(["git", "reset", "-q", "HEAD", "--", "plusplus.txt"], cwd=repo, check=True)
    (repo / "plusplus.txt").unlink()

    (repo / "enc.txt").write_text(f"{enc_header}\n", encoding="utf-8")
    subprocess.run(["git", "add", "enc.txt"], cwd=repo, check=True)
    assert _run_hook(PRE_COMMIT_HOOK, repo).returncode == 1


def test_pre_commit_allows_example_fixture_and_non_secret_hyphen_word(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "allow")
    (repo / ".env.example").write_text("API_KEY=your_key_here\n", encoding="utf-8")
    fixtures = repo / "tests" / "fixtures"
    fixtures.mkdir(parents=True)
    (fixtures / "credentials.json").write_text('{"client":"dummy"}\n', encoding="utf-8")
    (repo / "deps.txt").write_text("flask-sqlalchemy-extension==1.0.0\n", encoding="utf-8")
    subprocess.run(["git", "add", ".env.example", "tests/fixtures/credentials.json", "deps.txt"], cwd=repo, check=True)

    res = _run_hook(PRE_COMMIT_HOOK, repo)
    assert res.returncode == 0, res.stdout + res.stderr


def test_pre_commit_closes_hooks_dir_bypass_in_other_repos(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "bypass")
    fake_hooks = repo / "00-AgentOS" / "hooks"
    fake_hooks.mkdir(parents=True)
    sk_secret = "sk-" + "1234567890" + "abcdefghij"
    (fake_hooks / "evil.py").write_text(f"KEY = '{sk_secret}'\n", encoding="utf-8")
    subprocess.run(["git", "add", "00-AgentOS/hooks/evil.py"], cwd=repo, check=True)

    res = _run_hook(PRE_COMMIT_HOOK, repo)
    assert res.returncode == 1


def test_pre_commit_chains_repo_local_hook(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "chain_pre")
    (repo / "ok.txt").write_text("clean\n", encoding="utf-8")
    subprocess.run(["git", "add", "ok.txt"], cwd=repo, check=True)

    local_hook = repo / ".git" / "hooks" / "pre-commit"
    marker = repo / "local_pre_ran.txt"
    local_hook.write_bytes(
        f"#!/usr/bin/env bash\ntouch '{marker.as_posix()}'\nexit 0\n".encode()
    )
    local_hook.chmod(0o755)

    res = _run_hook(PRE_COMMIT_HOOK, repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert marker.exists()


def test_commit_msg_accepts_valid_and_git_auto_rejects_bad(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "msg_valid")
    msg_file = tmp_path / "COMMIT_EDITMSG"

    valid_subjects = [
        "feat(scope): add feature\n",
        "ci(vault): verify workflow\n",
        "Merge branch 'main' into feat/x\n",
        'Revert "feat: old change"\n',
        "fixup! feat: old change\n",
    ]
    for subj in valid_subjects:
        msg_file.write_text(subj, encoding="utf-8")
        res = _run_hook(COMMIT_MSG_HOOK, repo, [str(msg_file)])
        assert res.returncode == 0, f"Rejected {subj!r}: {res.stdout}"

    msg_file.write_text("bad commit message without type\n", encoding="utf-8")
    assert _run_hook(COMMIT_MSG_HOOK, repo, [str(msg_file)]).returncode == 1


def test_commit_msg_strips_ai_trailers_preserves_dco_and_chains_local(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "msg_chain")
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text(
        "fix(ui): fix cursor handling\n\n"
        "Cursor position is off on initial render.\n\n"
        "Signed-off-by: Dev <dev@example.com>\n"
        "Co-authored-by: Claude <noreply@anthropic.com>\n"
        "Generated with Claude Code\n",
        encoding="utf-8",
    )

    local_hook = repo / ".git" / "hooks" / "commit-msg"
    marker = repo / "local_msg_ran.txt"
    local_hook.write_bytes(
        f"#!/usr/bin/env bash\ntouch '{marker.as_posix()}'\nexit 0\n".encode()
    )
    local_hook.chmod(0o755)

    res = _run_hook(COMMIT_MSG_HOOK, repo, [str(msg_file)])
    assert res.returncode == 0, res.stdout + res.stderr
    cleaned = msg_file.read_text(encoding="utf-8")
    assert "Cursor position is off on initial render." in cleaned
    assert "Signed-off-by: Dev <dev@example.com>" in cleaned
    assert "Co-authored-by:" not in cleaned
    assert "Generated with Claude Code" not in cleaned
    assert marker.exists()
