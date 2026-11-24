"""Automated vault health verification suite (positive + negative tests)."""

import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
if str(VAULT_ROOT) not in sys.path:
    sys.path.insert(0, str(VAULT_ROOT))

from scripts.audit_vault import (
    check_canvas_links,
    check_dashboard_webclipper_contract,
    check_evergreen_frontmatter,
    check_hooks_lf_endings,
    check_links,
    check_orphan_resources,
    check_project_line_limits,
    check_skills_ssot_sync,
    check_template_placeholders,
)


def test_active_project_line_limits() -> None:
    assert check_project_line_limits(VAULT_ROOT) == []


def test_skills_ssot_and_readme_sync() -> None:
    assert check_skills_ssot_sync(VAULT_ROOT) == []


def test_no_broken_links_in_active_vault() -> None:
    assert check_links(VAULT_ROOT) == []


def test_canvas_links_in_active_vault() -> None:
    assert check_canvas_links(VAULT_ROOT) == []


def test_template_placeholders_in_active_vault() -> None:
    assert check_template_placeholders(VAULT_ROOT) == []


def test_orphan_resources_in_active_vault() -> None:
    assert check_orphan_resources(VAULT_ROOT) == []


def test_dashboard_webclipper_frontmatter_contract() -> None:
    assert check_dashboard_webclipper_contract(VAULT_ROOT) == []


def test_evergreen_notes_frontmatter_schema() -> None:
    assert check_evergreen_frontmatter(VAULT_ROOT) == []


def test_git_hooks_use_pure_lf() -> None:
    assert check_hooks_lf_endings(VAULT_ROOT) == []


def test_negative_project_line_limits_catches_overflow(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text("\n".join(["line"] * 51), encoding="utf-8")
    agentos_dir = tmp_path / "00-AgentOS"
    agentos_dir.mkdir(parents=True)
    (agentos_dir / "PROFILE.md").write_text("\n".join(["line"] * 51), encoding="utf-8")
    proj = tmp_path / "01-Projects" / "_active" / "Demo"
    proj.mkdir(parents=True)
    (proj / "AGENTS.md").write_text("\n".join(["line"] * 51), encoding="utf-8")
    (proj / "CONTEXT.md").write_text("\n".join(["line"] * 61), encoding="utf-8")
    errors = check_project_line_limits(tmp_path)
    assert len(errors) == 4


def test_negative_canvas_links_catches_missing_file(tmp_path: Path) -> None:
    (tmp_path / "board.canvas").write_text(
        '{"nodes":[{"id":"1","type":"file","file":"missing/CONTEXT.md"}],"edges":[]}',
        encoding="utf-8",
    )
    errors = check_canvas_links(tmp_path)
    assert len(errors) == 1
    assert "missing/CONTEXT.md" in errors[0]


def test_negative_template_placeholders_catches_unsupported_and_exempts_webclipper(
    tmp_path: Path,
) -> None:
    tpl_dir = tmp_path / "05-Templates"
    tpl_dir.mkdir(parents=True)
    (tpl_dir / "Bad_Template.md").write_text(
        "# {{Knowledge Title}}\nDate: {{date:YYYY-MM-DD}}\nValid: {{title}} {{date}} {{time}}\n",
        encoding="utf-8",
    )
    (tpl_dir / "WebClipper_Template.md").write_text(
        "---\nsource: {{url}}\ncaptured_at: {{date:YYYY-MM-DD HH:mm:ss}}\n---\n{{content}}\n",
        encoding="utf-8",
    )
    errors = check_template_placeholders(tmp_path)
    assert len(errors) == 2
    assert any("Knowledge Title" in err for err in errors)
    assert any("date:YYYY-MM-DD" in err for err in errors)


def test_negative_orphan_resources_catches_unreferenced_asset(tmp_path: Path) -> None:
    attach = tmp_path / "03-Resources" / "attachments"
    attach.mkdir(parents=True)
    (attach / ".gitkeep").write_text("", encoding="utf-8")
    (attach / "used.png").write_bytes(b"png")
    (attach / "orphan.png").write_bytes(b"png")
    (tmp_path / "note.md").write_text("![[used.png]]\n", encoding="utf-8")
    errors = check_orphan_resources(tmp_path)
    assert len(errors) == 1
    assert "orphan.png" in errors[0]


def test_negative_skills_ssot_catches_readme_drift(tmp_path: Path) -> None:
    skill = tmp_path / "00-AgentOS" / "skills" / "demo-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: demo-skill\n---\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "## Skills (2 Active Skills)\n| **`other-skill`** | desc |\n",
        encoding="utf-8",
    )
    errors = check_skills_ssot_sync(tmp_path)
    assert len(errors) >= 3


def test_negative_links_catches_broken_md_wiki_and_file_uri(tmp_path: Path) -> None:
    doc = tmp_path / "note.md"
    doc.write_text(
        "[missing](./nope.md)\n[[GhostNote]]\n[local](file:///c:/Users/someone/a.md)\n",
        encoding="utf-8",
    )
    errors = check_links(tmp_path)
    assert len(errors) >= 3


def test_negative_dashboard_contract_catches_field_mismatch(tmp_path: Path) -> None:
    (tmp_path / "DASHBOARD.md").write_text(
        '```dataview\nTABLE\n  source_url as "Source"\nFROM "_inbox"\n```\n',
        encoding="utf-8",
    )
    tpl_dir = tmp_path / "05-Templates"
    tpl_dir.mkdir(parents=True)
    (tpl_dir / "WebClipper_Template.md").write_text(
        "---\nsource: https://example.com\n---\n",
        encoding="utf-8",
    )
    errors = check_dashboard_webclipper_contract(tmp_path)
    assert len(errors) == 1
    assert "source_url" in errors[0]


def test_negative_evergreen_frontmatter_catches_missing_keys(tmp_path: Path) -> None:
    area = tmp_path / "02-Areas" / "AI"
    area.mkdir(parents=True)
    (area / "bad_note.md").write_text("---\ntitle: Incomplete\n---\n", encoding="utf-8")
    errors = check_evergreen_frontmatter(tmp_path)
    assert len(errors) == 1


def test_negative_hooks_lf_catches_crlf(tmp_path: Path) -> None:
    hooks = tmp_path / "00-AgentOS" / "hooks"
    hooks.mkdir(parents=True)
    (hooks / "pre-commit").write_bytes(b"#!/usr/bin/env bash\r\nexit 0\r\n")
    (hooks / "commit-msg").write_bytes(b"#!/usr/bin/env bash\nexit 0\n")
    errors = check_hooks_lf_endings(tmp_path)
    assert len(errors) == 1
    assert "pre-commit" in errors[0]
