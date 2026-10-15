#!/usr/bin/env python3
"""
extract_segment.py — Mechanical Verbatim Source Slicing Tool
100% Python Standard Library. Zero-LLM Token Cost.
Part of Learning OS Agent Kit.
"""

import sys
import os
import argparse
import json
import re
from pathlib import Path


def inspect_source(source_path: Path):
    """
    Scans source file and outputs table of headings, line numbers, and approximate word counts.
    Takes minimal token budget (< 200 tokens).
    """
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    lines = source_path.read_text(encoding="utf-8", errors="replace").splitlines()
    total_lines = len(lines)
    
    print(f"\nSource File: {source_path.name} (Total Lines: {total_lines})")
    print(f"{'Line':<8} | {'Level':<6} | {'Approx Words':<12} | Heading")
    print("-" * 65)

    headings_found = 0
    heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$")
    
    last_line = 1
    for idx, line in enumerate(lines, 1):
        m = heading_pattern.match(line.strip())
        if m:
            headings_found += 1
            hashes, title = m.groups()
            level = len(hashes)
            # Estimate words between last heading and this one
            words_chunk = sum(len(lines[i].split()) for i in range(last_line - 1, idx - 1))
            print(f"{idx:<8} | H{level:<5} | {words_chunk:<12} | {title[:40]}")
            last_line = idx

    if headings_found == 0:
        # Plain text without markdown headings: output chunk breakdown every 200 lines
        print("Notice: No markdown headings found. Chunk breakdown (200-line intervals):")
        for start in range(1, total_lines + 1, 200):
            end = min(start + 199, total_lines)
            words = sum(len(lines[i].split()) for i in range(start - 1, end))
            sample = lines[start - 1].strip()[:30] if lines[start - 1].strip() else "..."
            print(f"{start:<8} | Chunk  | {words:<12} | Lines {start}-{end} ({sample})")

    print("-" * 65)
    print(f"Total Lines: {total_lines} | Headings Found: {headings_found}\n")


def extract_slice(source_path: Path, start_line: int, end_line: int, output_path: Path, anchor_prefix: str = "¶"):
    """
    Cuts exactly lines start_line to end_line from source file, preserves code blocks,
    inserts [¶N] paragraph anchors outside code blocks, and writes verbatim_meta JSON header.
    """
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    raw_lines = source_path.read_text(encoding="utf-8", errors="replace").splitlines()
    total_lines = len(raw_lines)

    if start_line < 1 or end_line < start_line or start_line > total_lines:
        print(f"Error: Invalid line range [{start_line}, {end_line}] for file with {total_lines} lines.", file=sys.stderr)
        sys.exit(1)

    actual_end = min(end_line, total_lines)
    selected_lines = raw_lines[start_line - 1 : actual_end]

    # Process lines, tracking code blocks
    in_code_block = False
    paragraph_index = 0
    at_paragraph_start = True
    output_lines = []

    for line in selected_lines:
        trimmed = line.strip()
        
        # Check for code block boundary
        if trimmed.startswith("```"):
            in_code_block = not in_code_block
            output_lines.append(line)
            at_paragraph_start = False
            continue

        if in_code_block:
            output_lines.append(line)
            at_paragraph_start = False
            continue

        # Outside code block
        if not trimmed:
            # Empty line signifies paragraph break
            output_lines.append(line)
            at_paragraph_start = True
        elif trimmed.startswith("#"):
            # A markdown heading is always its own anchored element
            paragraph_index += 1
            output_lines.append(f"[{anchor_prefix}{paragraph_index}] {line}")
            at_paragraph_start = True
        else:
            if at_paragraph_start:
                paragraph_index += 1
                output_lines.append(f"[{anchor_prefix}{paragraph_index}] {line}")
                at_paragraph_start = False
            else:
                output_lines.append(line)

    # Prepare verbatim_meta JSON
    # Try to make source path relative to learning-os if possible, else use name
    source_ref = source_path.as_posix()
    meta = {
        "source": source_ref,
        "start_line": start_line,
        "end_line": actual_end,
        "total_paragraphs": paragraph_index
    }
    meta_json = json.dumps(meta, ensure_ascii=False)
    header = f"<!-- verbatim_meta: {meta_json} -->\n\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_content = header + "\n".join(output_lines) + "\n"
    output_path.write_text(final_content, encoding="utf-8")
    print(f"Success: Extracted {len(selected_lines)} lines ({paragraph_index} paragraphs) to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="extract_segment.py — Mechanical Verbatim Source Slicing Tool for Learning OS"
    )
    parser.add_argument("--source", type=str, required=True, help="Path to input source file")
    parser.add_argument("--inspect", action="store_true", help="Inspect source headings and line ranges without extracting")
    parser.add_argument("--toc", action="store_true", help="Alias for --inspect")
    parser.add_argument("--start-line", type=int, help="Start line number (1-indexed)")
    parser.add_argument("--end-line", type=int, help="End line number (1-indexed, inclusive)")
    parser.add_argument("--output", type=str, help="Destination path for source_verbatim.md")
    parser.add_argument("--anchor-prefix", type=str, default="¶", help="Prefix for paragraph anchors (default: ¶)")

    args = parser.parse_args()
    source_path = Path(args.source).resolve()

    if args.inspect or args.toc:
        inspect_source(source_path)
        return

    if args.start_line is None or args.end_line is None or not args.output:
        print("Error: --start-line, --end-line, and --output are required when not using --inspect.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    output_path = Path(args.output).resolve()
    extract_slice(source_path, args.start_line, args.end_line, output_path, args.anchor_prefix)


if __name__ == "__main__":
    main()
