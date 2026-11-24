"""Vault health audit script for SecondBrain Knowledge OS (v3.0)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

DEFAULT_ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_LINK_SCAN_PARTS = {
    ".git",
    ".agents",
    ".claude",
    ".cursor",
    "04-Archive",
    "05-Templates",
    "node_modules",
    ".venv",
}

EXCLUDED_INDEX_PARTS = {
    ".git",
    ".agents",
    ".claude",
    ".cursor",
    "node_modules",
    ".venv",
}

ALLOWED_TEMPLATE_TOKENS = {"title", "date", "time"}

MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
WIKI_LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)
TEMPLATE_TOKEN_RE = re.compile(r"\{\{([^{}]+)\}\}")


def _strip_code(text: str) -> str:
    no_fences = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"`[^`\n]+`", "", no_fences)


def _parse_frontmatter_keys(text: str) -> dict[str, str] | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key_match = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
        if key_match:
            fields[key_match.group(1)] = key_match.group(2).strip().strip('"').strip("'")
    return fields


def check_project_line_limits(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify root AGENTS.md, 00-AgentOS/PROFILE.md (<=50), and active project limits."""
    errors: list[str] = []
    global_limits = (
        (root / "AGENTS.md", 50),
        (root / "00-AgentOS" / "PROFILE.md", 50),
    )
    for target, max_lines in global_limits:
        if target.exists():
            line_count = len(target.read_text(encoding="utf-8").splitlines())
            if line_count > max_lines:
                errors.append(
                    f"{target.relative_to(root).as_posix()} has {line_count} lines (limit <= {max_lines})"
                )

    active_dir = root / "01-Projects" / "_active"
    if not active_dir.exists():
        return errors

    for project_dir in sorted(p for p in active_dir.iterdir() if p.is_dir()):
        limits = (("AGENTS.md", 50), ("CONTEXT.md", 60))
        for filename, max_lines in limits:
            target = project_dir / filename
            if not target.exists():
                errors.append(f"Missing {target.relative_to(root).as_posix()}")
                continue
            line_count = len(target.read_text(encoding="utf-8").splitlines())
            if line_count > max_lines:
                errors.append(
                    f"{target.relative_to(root).as_posix()} has {line_count} lines (limit <= {max_lines})"
                )
    return errors


def check_skills_ssot_sync(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify 00-AgentOS/skills/ matches README.md active skills table and header count."""
    errors: list[str] = []
    skills_dir = root / "00-AgentOS" / "skills"
    readme_path = root / "README.md"

    if not skills_dir.exists():
        return ["Missing 00-AgentOS/skills/ directory"]
    if not readme_path.exists():
        return ["Missing README.md"]

    actual_skills: set[str] = set()
    for skill_folder in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_md = skill_folder / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"Missing SKILL.md in {skill_folder.relative_to(root).as_posix()}")
            continue
        fields = _parse_frontmatter_keys(skill_md.read_text(encoding="utf-8"))
        if not fields or fields.get("name") != skill_folder.name:
            errors.append(
                f"Skill frontmatter name mismatch in {skill_md.relative_to(root).as_posix()}"
            )
        actual_skills.add(skill_folder.name)

    readme_text = readme_path.read_text(encoding="utf-8")
    documented_skills = set(
        re.findall(r"^\|\s*\*\*`([a-z0-9-]+)`\*\*\s*\|", readme_text, re.MULTILINE)
    )

    missing_in_readme = sorted(actual_skills - documented_skills)
    extra_in_readme = sorted(documented_skills - actual_skills)
    if missing_in_readme:
        errors.append(f"Skills missing in README.md table: {missing_in_readme}")
    if extra_in_readme:
        errors.append(f"Extra skills in README.md table not on disk: {extra_in_readme}")

    count_match = re.search(r"\((\d+)\s+Active Skills\)", readme_text)
    if not count_match:
        errors.append("README.md missing '(N Active Skills)' heading count")
    elif int(count_match.group(1)) != len(actual_skills):
        errors.append(
            f"README.md reports {count_match.group(1)} Active Skills, found {len(actual_skills)} on disk"
        )
    return errors


def check_links(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify no broken Markdown links, wikilinks, or local file:///c:/Users/ links in active docs."""
    errors: list[str] = []
    root_resolved = root.resolve()

    by_rel: dict[str, Path] = {}
    by_name: dict[str, list[Path]] = {}
    by_stem: dict[str, list[Path]] = {}

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_INDEX_PARTS for part in rel_parts):
            continue
        rel_posix = path.relative_to(root).as_posix().lower()
        by_rel[rel_posix] = path
        by_name.setdefault(path.name.lower(), []).append(path)
        by_stem.setdefault(path.stem.lower(), []).append(path)

    for md_path in sorted(root.rglob("*.md")):
        rel_parts = md_path.relative_to(root).parts
        if any(part in EXCLUDED_LINK_SCAN_PARTS for part in rel_parts):
            continue
        rel_str = md_path.relative_to(root).as_posix()
        clean = _strip_code(md_path.read_text(encoding="utf-8"))

        if re.search(r"file:///c:/Users/", clean, re.IGNORECASE):
            errors.append(f"Hardcoded local file:///c:/Users/ link in {rel_str}")

        for match in MD_LINK_RE.finditer(clean):
            target = match.group(2).strip()
            if target.startswith(("http://", "https://", "mailto:", "#", "obsidian://")):
                continue
            if target.startswith("file://"):
                errors.append(f"Non-portable file:// link in {rel_str}: ({target})")
                continue
            target_file = unquote(target.split("#")[0].split(" ")[0])
            if not target_file:
                continue
            if not (md_path.parent / target_file).resolve().exists() and not (
                root_resolved / target_file
            ).resolve().exists():
                errors.append(f"Broken Markdown link in {rel_str}: ({target})")

        for match in WIKI_LINK_RE.finditer(clean):
            raw = match.group(1)
            target = raw.split("|")[0].split("#")[0].strip()
            if not target:
                continue
            t_low = target.lower()
            found = (
                (t_low in by_rel)
                or ((t_low + ".md") in by_rel)
                or (t_low in by_name)
                or (t_low in by_stem)
                or any(k.endswith(("/" + t_low, "/" + t_low + ".md")) for k in by_rel)
            )
            if not found:
                errors.append(f"Broken wikilink in {rel_str}: [[{raw}]]")
    return errors


def check_canvas_links(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify all file nodes in active .canvas files resolve to existing vault paths."""
    errors: list[str] = []
    for canvas_path in sorted(root.rglob("*.canvas")):
        rel_parts = canvas_path.relative_to(root).parts
        if any(part in EXCLUDED_LINK_SCAN_PARTS for part in rel_parts):
            continue
        rel_str = canvas_path.relative_to(root).as_posix()
        try:
            payload = json.loads(canvas_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel_str}: {exc}")
            continue
        for node in payload.get("nodes", []):
            if node.get("type") != "file":
                continue
            target_rel = node.get("file")
            if not target_rel or not (root / target_rel).exists():
                errors.append(f"Broken canvas file reference in {rel_str}: {target_rel!r}")
    return errors


def check_template_placeholders(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify Obsidian Core Templates use only {{title}}, {{date}}, or {{time}} placeholders."""
    errors: list[str] = []
    templates_dir = root / "05-Templates"
    if not templates_dir.exists():
        return errors

    for tpl_path in sorted(templates_dir.glob("*.md")):
        if tpl_path.name == "WebClipper_Template.md":
            continue
        rel_str = tpl_path.relative_to(root).as_posix()
        clean = _strip_code(tpl_path.read_text(encoding="utf-8"))
        for match in TEMPLATE_TOKEN_RE.finditer(clean):
            token = match.group(1).strip()
            if token not in ALLOWED_TEMPLATE_TOKENS:
                errors.append(
                    f"Unsupported core template placeholder '{{{{{token}}}}}' in {rel_str}"
                )
    return errors


def check_orphan_resources(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify every asset under 03-Resources/{attachments,snippets}/ is referenced in the vault."""
    errors: list[str] = []
    resources_dir = root / "03-Resources"
    if not resources_dir.exists():
        return errors

    doc_texts: dict[Path, str] = {}
    for ext in ("*.md", "*.canvas"):
        for doc_path in root.rglob(ext):
            rel_parts = doc_path.relative_to(root).parts
            if any(part in EXCLUDED_INDEX_PARTS or part == ".obsidian" for part in rel_parts):
                continue
            doc_texts[doc_path] = doc_path.read_text(encoding="utf-8", errors="ignore")

    for bucket in ("attachments", "snippets"):
        bucket_dir = resources_dir / bucket
        if not bucket_dir.exists():
            continue
        for asset in sorted(p for p in bucket_dir.rglob("*") if p.is_file()):
            if asset.name.startswith(".") or asset.name.upper() == "README.MD":
                continue
            if not any(asset.name in text for src_path, text in doc_texts.items() if src_path != asset):
                errors.append(f"Unreferenced resource asset: {asset.relative_to(root).as_posix()}")
    return errors


def check_dashboard_webclipper_contract(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify DASHBOARD.md _inbox Dataview query fields match WebClipper_Template.md frontmatter."""
    errors: list[str] = []
    dashboard_path = root / "DASHBOARD.md"
    template_path = root / "05-Templates" / "WebClipper_Template.md"

    if not dashboard_path.exists() or not template_path.exists():
        return ["Missing DASHBOARD.md or 05-Templates/WebClipper_Template.md"]

    dash_text = dashboard_path.read_text(encoding="utf-8")
    inbox_block: str | None = None
    for block in re.findall(r"```dataview\s*\n(.*?)\n```", dash_text, re.DOTALL):
        if 'FROM "_inbox"' in block:
            inbox_block = block
            break
    if not inbox_block:
        return ["Missing Dataview _inbox TABLE block in DASHBOARD.md"]

    fields_match = re.search(r"TABLE\s+(.*?)\s+FROM\s+\"_inbox\"", inbox_block, re.DOTALL)
    if not fields_match:
        return ["Missing TABLE fields in DASHBOARD.md _inbox Dataview block"]

    template_fields = _parse_frontmatter_keys(template_path.read_text(encoding="utf-8")) or {}
    for line in fields_match.group(1).splitlines():
        field = line.strip().rstrip(",").split(" as ")[0].strip()
        if not field or field.startswith("file."):
            continue
        if field not in template_fields:
            errors.append(
                f"DASHBOARD.md queries '{field}' from _inbox, missing in WebClipper_Template.md"
            )
    return errors


def check_evergreen_frontmatter(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify top-level evergreen notes (02-Areas/<Domain>/*.md) have standard YAML frontmatter.

    Nested coursework and competition subfolders (e.g. 02-Areas/Coursework/.../*.md) are exempted.
    """
    errors: list[str] = []
    areas_dir = root / "02-Areas"
    required_keys = {"title", "type", "domain", "tags", "last_updated"}

    if not areas_dir.exists():
        return errors

    for md_path in sorted(areas_dir.glob("*/*.md")):
        if md_path.name.upper() == "README.MD":
            continue
        rel_str = md_path.relative_to(root).as_posix()
        fields = _parse_frontmatter_keys(md_path.read_text(encoding="utf-8"))
        if not fields:
            errors.append(f"Missing YAML frontmatter in {rel_str}")
            continue
        missing = sorted(required_keys - set(fields.keys()))
        if missing:
            errors.append(f"Frontmatter missing keys {missing} in {rel_str}")
    return errors


def check_hooks_lf_endings(root: Path = DEFAULT_ROOT) -> list[str]:
    """Verify 00-AgentOS/hooks scripts exist and use pure LF line endings."""
    errors: list[str] = []
    for hook_name in ("pre-commit", "commit-msg"):
        hook_path = root / "00-AgentOS" / "hooks" / hook_name
        if not hook_path.exists():
            errors.append(f"Missing hook: {hook_path.relative_to(root).as_posix()}")
            continue
        if b"\r\n" in hook_path.read_bytes():
            errors.append(f"Hook contains CRLF line endings: {hook_path.relative_to(root).as_posix()}")
    return errors


CHECKS = (
    check_project_line_limits,
    check_skills_ssot_sync,
    check_links,
    check_canvas_links,
    check_template_placeholders,
    check_orphan_resources,
    check_dashboard_webclipper_contract,
    check_evergreen_frontmatter,
    check_hooks_lf_endings,
)


def run_all_checks(root: Path = DEFAULT_ROOT) -> list[str]:
    """Run all vault health checks and return combined error messages."""
    errors: list[str] = []
    for check_fn in CHECKS:
        errors.extend(check_fn(root))
    return errors


def main() -> int:
    errors = run_all_checks(DEFAULT_ROOT)
    if errors:
        print(f"Vault audit FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"Vault audit PASSED (0 errors across all {len(CHECKS)} governance checks).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
