#!/usr/bin/env python3
"""
verify_system.py — Comprehensive System Linter & Verification Tool
100% Python Standard Library. Zero-External Dependencies.
Part of Learning OS Agent Kit.
"""

import sys
import os
import argparse
import json
import re
import hashlib
import difflib
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

# Regex for external URLs: requires domain structure with a dot to avoid catching JS comments (//todo, //======)
URL_PATTERN = re.compile(r'(?:https?:)?//[a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,}[^\s"\'<>)+]*')

# Whitelist standard SVG XML namespaces
URL_WHITELIST = {
    "http://www.w3.org/2000/svg",
    "https://www.w3.org/2000/svg",
    "http://www.w3.org/1999/xlink",
    "https://www.w3.org/1999/xlink",
    "http://www.w3.org/TR/SVG11",
    "https://www.w3.org/TR/SVG11",
}

# HTML5 Void elements that do not require closing tags
HTML5_VOID_ELEMENTS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
}


class HTMLTagBalancer(HTMLParser):
    """Checks tag open/close balance for HTML5 files."""
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t not in HTML5_VOID_ELEMENTS:
            self.stack.append((t, self.getpos()))

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in HTML5_VOID_ELEMENTS:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{t}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.stack[-1]
        if last_tag == t:
            self.stack.pop()
        else:
            self.errors.append(
                f"Mismatched tag: expected </{last_tag}> (opened line {pos[0]}), got </{t}> at line {self.getpos()[0]}"
            )

    def close(self):
        super().close()
        for tag, pos in self.stack:
            self.errors.append(f"Unclosed tag <{tag}> opened at line {pos[0]}")


def normalize_text(text: str) -> str:
    """Normalizes text for robust semantic comparison (Unicode NFC + collapsed spaces)."""
    # Strip verbatim_meta comments
    text = re.sub(r'<!--\s*verbatim_meta:.*?-->', '', text, flags=re.DOTALL)
    # Strip paragraph anchors [¶N]
    text = re.sub(r'\[¶\d+\]\s*', '', text)
    # Unicode NFC normalization
    text = unicodedata.normalize('NFC', text)
    # Collapse whitespaces
    return ' '.join(text.split())


def check_verbatim_integrity(verbatim_path: Path) -> list:
    """Check 1: Compares SHA-256 hash of normalized verbatim against slice of original source."""
    errors = []
    content = verbatim_path.read_text(encoding="utf-8", errors="replace")
    
    match = re.search(r'<!--\s*verbatim_meta:\s*(\{.*?\})\s*-->', content)
    if not match:
        errors.append(f"MISSING_METADATA: No valid verbatim_meta JSON found in {verbatim_path}")
        return errors

    try:
        meta = json.loads(match.group(1))
    except Exception as e:
        errors.append(f"INVALID_METADATA: Failed to parse verbatim_meta JSON: {e}")
        return errors

    source_path = Path(meta.get("source", ""))
    if not source_path.is_absolute():
        # Try relative to verbatim path, course path, or root
        candidates = [
            verbatim_path.parent / source_path,
            verbatim_path.parents[3] / source_path,
            Path.cwd() / source_path
        ]
        resolved = None
        for c in candidates:
            if c.exists():
                resolved = c
                break
        if resolved:
            source_path = resolved

    if not source_path.exists():
        errors.append(f"SOURCE_NOT_FOUND: Source file does not exist: {meta.get('source')}")
        return errors

    start_line = meta.get("start_line", 1)
    end_line = meta.get("end_line", 1)

    source_lines = source_path.read_text(encoding="utf-8", errors="replace").splitlines()
    actual_end = min(end_line, len(source_lines))
    source_slice = "\n".join(source_lines[start_line - 1 : actual_end])

    norm_source = normalize_text(source_slice)
    norm_verbatim = normalize_text(content)

    hash_source = hashlib.sha256(norm_source.encode("utf-8")).hexdigest()
    hash_verbatim = hashlib.sha256(norm_verbatim.encode("utf-8")).hexdigest()

    if hash_source != hash_verbatim:
        diff = list(difflib.unified_diff(
            norm_source.split(), norm_verbatim.split(),
            fromfile="source_slice", tofile="source_verbatim",
            n=3
        ))
        diff_sample = " ".join(diff[:10])
        errors.append(
            f"CRITICAL_SOURCE_MUTATION in {verbatim_path.name}: "
            f"Hash mismatch ({hash_source[:8]} != {hash_verbatim[:8]}). First diff: {diff_sample}"
        )

    return errors


def check_anchors(lesson_path: Path, verbatim_path: Path) -> list:
    """Check 2: Ensures lesson citations [¶N] are valid and exist in source_verbatim."""
    errors = []
    if not verbatim_path.exists():
        return errors

    v_content = verbatim_path.read_text(encoding="utf-8", errors="replace")
    available_anchors = {int(x) for x in re.findall(r'\[¶(\d+)\]', v_content)}

    l_content = lesson_path.read_text(encoding="utf-8", errors="replace")
    cited_anchors = {int(x) for x in re.findall(r'\[¶(\d+)\]', l_content)}

    if not cited_anchors:
        errors.append(f"MISSING_ANCHORS: {lesson_path.name} in verbatim mode does not cite any paragraph anchors [¶N].")
    else:
        hallucinated = cited_anchors - available_anchors
        if hallucinated:
            errors.append(
                f"HALLUCINATED_ANCHOR: {lesson_path.name} cites non-existent anchor(s) {sorted(hallucinated)}. "
                f"Available anchors: 1..{max(available_anchors) if available_anchors else 0}."
            )

    return errors


def check_html_lab(lab_path: Path) -> list:
    """Check 3 & 4: Validates HTML tag balance and enforces strict offline URL boundaries."""
    errors = []
    content = lab_path.read_text(encoding="utf-8", errors="replace")

    # 1. URL Security Check
    matches = URL_PATTERN.findall(content)
    for url in matches:
        clean_url = url.split("?")[0].split("#")[0].rstrip("/'\"")
        if clean_url not in URL_WHITELIST:
            errors.append(f"EXTERNAL_URL_DETECTED: {lab_path.name} contains unauthorized online link: {url}")

    # 2. Tag Balance Check
    parser = HTMLTagBalancer()
    try:
        parser.feed(content)
        parser.close()
        for err in parser.errors:
            errors.append(f"HTML_PARSE_ERROR in {lab_path.name}: {err}")
    except Exception as e:
        errors.append(f"HTML_SYNTAX_ERROR in {lab_path.name}: {e}")

    return errors


def check_markdown_frontmatter(lesson_path: Path) -> list:
    """Check 5: Enforces visual and visual_reason frontmatter metadata."""
    errors = []
    content = lesson_path.read_text(encoding="utf-8", errors="replace")

    if not content.startswith("---"):
        errors.append(f"MISSING_FRONTMATTER: {lesson_path.name} must start with YAML frontmatter '---'")
        return errors

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append(f"MISSING_FRONTMATTER: {lesson_path.name} frontmatter block is not closed with '---'")
        return errors

    fm_text = parts[1]
    
    # Check visual: none | mermaid | svg | lab
    visual_match = re.search(r'visual:\s*(none|mermaid|svg|lab)', fm_text)
    if not visual_match:
        errors.append(f"MISSING_FRONTMATTER: {lesson_path.name} missing 'visual: [none|mermaid|svg|lab]'")

    # Check visual_reason: ...
    reason_match = re.search(r'visual_reason:\s*(.+)', fm_text)
    if not reason_match or not reason_match.group(1).strip():
        errors.append(f"MISSING_FRONTMATTER: {lesson_path.name} missing 'visual_reason: <explanation>'")

    return errors


def check_progress_file(progress_path: Path) -> list:
    """Check 6: Monitors progress.md line limits (warning at 150, error at 200)."""
    errors = []
    if not progress_path.exists():
        errors.append(f"PROGRESS_MISSING: {progress_path} does not exist.")
        return errors

    lines = len(progress_path.read_text(encoding="utf-8", errors="replace").splitlines())
    if lines > 200:
        errors.append(
            f"CONTEXT_LIMIT_BREACH: {progress_path.name} has {lines} lines, exceeding 200 line hard limit! "
            "Execute compaction immediately."
        )
    elif lines > 150:
        print(f"WARNING: {progress_path.name} has {lines} lines (> 150). Compaction recommended.", file=sys.stderr)

    return errors


def check_templates(templates_dir: Path) -> bool:
    """Validates scaffolds in .agents/templates/."""
    print(f"\n[Verifying Templates in {templates_dir}]")
    all_errors = []

    for lab in templates_dir.glob("*.html"):
        errs = check_html_lab(lab)
        all_errors.extend(errs)

    for md in templates_dir.glob("*.md"):
        if md.name.startswith("lesson-"):
            errs = check_markdown_frontmatter(md)
            all_errors.extend(errs)
        elif md.name == "progress.md":
            errs = check_progress_file(md)
            all_errors.extend(errs)

    if all_errors:
        print(f"FAIL: {len(all_errors)} error(s) found in templates:", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return False
    
    print("PASS: All templates conform to strict linter standards.")
    return True


def check_course(course_dir: Path) -> bool:
    """Validates an entire course directory (full 6-layer suite)."""
    print(f"\n[Verifying Course: {course_dir.name}]")
    all_errors = []

    # Check progress.md
    progress_file = course_dir / "progress.md"
    all_errors.extend(check_progress_file(progress_file))

    # Check modules
    modules_dir = course_dir / "modules"
    if modules_dir.exists():
        for mod in sorted(modules_dir.iterdir()):
            if not mod.is_dir():
                continue
            
            lesson = mod / "lesson.md"
            verbatim = mod / "source_verbatim.md"
            lab = mod / "lab.html"

            if verbatim.exists():
                all_errors.extend(check_verbatim_integrity(verbatim))

            if lesson.exists():
                all_errors.extend(check_markdown_frontmatter(lesson))
                if verbatim.exists():
                    all_errors.extend(check_anchors(lesson, verbatim))

            if lab.exists():
                all_errors.extend(check_html_lab(lab))

    if all_errors:
        print(f"FAIL: {len(all_errors)} error(s) in course '{course_dir.name}':", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return False

    print(f"PASS: Course '{course_dir.name}' is 100% verified and green.")
    return True


def append_log_entry(log_path: Path, entry: str):
    """Appends an entry to progress-log.md without reading the entire log into memory."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry.strip() + "\n")
    print(f"Success: Appended entry to {log_path.name}")


def check_clean_workspace(kit_root: Path) -> bool:
    """Verifies no loose junk/scratch files exist at workspace root."""
    print(f"\n[Verifying Workspace Hygiene in {kit_root}]")
    allowed_root_files = {"agents.md", "readme.md", ".gitignore"}
    allowed_root_dirs = {".agents", "inputs", "learning-space", ".tmp", "scratch"}
    
    stray_items = []
    for item in kit_root.iterdir():
        name_lower = item.name.lower()
        if item.is_file():
            if name_lower not in allowed_root_files:
                stray_items.append(f"Stray file at workspace root: {item.name}")
        elif item.is_dir():
            if name_lower not in allowed_root_dirs and not name_lower.startswith(".git"):
                stray_items.append(f"Stray directory at workspace root: {item.name}")

    if stray_items:
        for stray in stray_items:
            print(f"  [-] ERROR: {stray}")
        return False

    print("  [+] PASS: Workspace root is 100% clean and free of litter.")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="verify_system.py — Comprehensive Linter & Verification Tool for Learning OS"
    )
    parser.add_argument("--course", type=str, help="Path to specific course directory")
    parser.add_argument("--all", action="store_true", help="Scan all courses in learning-space/courses")
    parser.add_argument("--check-templates", action="store_true", help="Verify templates in .agents/templates")
    parser.add_argument("--check-hygiene", action="store_true", help="Verify workspace is free of stray files")
    parser.add_argument("--append-log", type=str, help="Target progress-log.md file path to append to")
    parser.add_argument("--entry", type=str, help="Log message text to append")
    parser.add_argument("--root", type=str, default=".", help="Root path of the Learning OS kit")

    args = parser.parse_args()

    # Append log mode
    if args.append_log:
        if not args.entry:
            print("Error: --entry is required when using --append-log", file=sys.stderr)
            sys.exit(1)
        append_log_entry(Path(args.append_log).resolve(), args.entry)
        sys.exit(0)

    # Check templates mode
    if args.check_templates:
        kit_root = Path(args.root).resolve()
        templates_dir = kit_root / ".agents" / "templates"
        if not templates_dir.exists():
            templates_dir = Path("d:/Downloads/AI Agent Kits/Agent Kits/Learning OS/.agents/templates")
        success = check_templates(templates_dir)
        sys.exit(0 if success else 1)

    # Check hygiene mode
    if args.check_hygiene:
        kit_root = Path(args.root).resolve()
        success = check_clean_workspace(kit_root)
        sys.exit(0 if success else 1)

    # Check specific course
    if args.course:
        course_dir = Path(args.course).resolve()
        if not course_dir.exists():
            print(f"Error: Course path not found: {course_dir}", file=sys.stderr)
            sys.exit(1)
        success = check_course(course_dir)
        sys.exit(0 if success else 1)

    # Check all courses
    if args.all:
        kit_root = Path(args.root).resolve()
        if not check_clean_workspace(kit_root):
            sys.exit(1)

        courses_dir = kit_root / "learning-space" / "courses"
        if not courses_dir.exists():
            courses_dir = Path("d:/Downloads/AI Agent Kits/Agent Kits/Learning OS/learning-space/courses")
        if not courses_dir.exists():
            print(f"Error: Courses directory not found: {courses_dir}", file=sys.stderr)
            sys.exit(1)
        
        all_passed = True
        courses = [c for c in courses_dir.iterdir() if c.is_dir()]
        if not courses:
            print(f"Notice: No courses found in {courses_dir}")
            sys.exit(0)

        for c in courses:
            if not check_course(c):
                all_passed = False

        sys.exit(0 if all_passed else 1)

    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()

