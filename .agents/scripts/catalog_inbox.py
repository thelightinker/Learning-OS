#!/usr/bin/env python3
"""
catalog_inbox.py — Universal Source Intake & Document Archetype Classifier
100% Python Standard Library. Zero External Dependencies.
Part of Learning OS Agent Kit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def compute_sha256(path: Path) -> str:
    """Computes SHA-256 hash of file contents in binary mode."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def detect_headings(text: str) -> List[Dict[str, Any]]:
    """Extracts major section headings and their line numbers."""
    headings = []
    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        s = line.strip()
        # Markdown headings
        if s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            title = s.lstrip("#").strip()
            if title:
                headings.append({"line": idx, "level": level, "title": title})
        # Text chapter/section headings
        elif re.match(r'^(?:Chương|Phần|Chapter|Section|Part)\s+[0-9IVXLCDM]+[:.]?\s*(.*)$', s, re.IGNORECASE):
            headings.append({"line": idx, "level": 1, "title": s})
    return headings


def classify_archetype(ext: str, line_count: int, headings: List[Dict[str, Any]], sample_text: str) -> Dict[str, str]:
    """Classifies document archetype and suggests pedagogical strategy."""
    sample_lower = sample_text.lower()
    
    # Check paper signals
    paper_signals = ["abstract", "introduction", "methodology", "references", "conclusion", "tóm tắt"]
    has_paper_signals = sum(1 for sig in paper_signals if sig in sample_lower) >= 2

    if line_count > 2500 and len(headings) >= 3:
        return {
            "archetype": "book",
            "recommended_track": "Verbatim Line-Slice Track",
            "rationale": "Tài liệu dài có cấu trúc chương mục rõ ràng. Nên học sâu từng chương nguyên bản kèm Socratic checkpoints."
        }
    elif has_paper_signals or (500 <= line_count <= 2500 and len(headings) >= 2):
        return {
            "archetype": "paper",
            "recommended_track": "Paper Deep-Dive Track",
            "rationale": "Tài liệu nghiên cứu/chuyên khảo cô đọng. Nên đào sâu mô hình nhân quả và các trường hợp biên."
        }
    else:
        return {
            "archetype": "transcript_notes",
            "recommended_track": "Synthesis & Active Recall Track",
            "rationale": "Ghi chép hoặc tài liệu ngắn/văn nói. Nên tổng hợp 80/20, hệ thống hóa và tạo câu đố truy hồi tích cực."
        }


def scan_directory(target_dir: Path) -> List[Dict[str, Any]]:
    """Scans all documents in directory recursively."""
    results = []
    supported_extensions = {".txt", ".md", ".pdf", ".html", ".markdown"}
    
    for item in sorted(target_dir.rglob("*")):
        if item.is_file() and item.suffix.lower() in supported_extensions and not item.name.startswith("."):
            if item.name.lower() in {"readme.md", "catalog.json"}:
                continue
            
            try:
                raw_bytes = item.read_bytes()
                sha256 = hashlib.sha256(raw_bytes).hexdigest()
                text = raw_bytes.decode("utf-8", errors="replace")
                lines = text.splitlines()
                line_count = len(lines)
                sample_text = text[:4000]
                headings = detect_headings(text)
                classification = classify_archetype(item.suffix.lower(), line_count, headings, sample_text)
                
                results.append({
                    "filename": item.name,
                    "rel_path": item.as_posix(),
                    "size_bytes": len(raw_bytes),
                    "line_count": line_count,
                    "sha256": sha256,
                    "archetype": classification["archetype"],
                    "recommended_track": classification["recommended_track"],
                    "rationale": classification["rationale"],
                    "headings_count": len(headings),
                    "outline_preview": headings[:8]
                })
            except Exception as exc:
                results.append({
                    "filename": item.name,
                    "rel_path": item.as_posix(),
                    "error": str(exc)
                })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="catalog_inbox.py — Universal Intake & Archetype Classifier")
    parser.add_argument("--inbox", type=str, default="inputs/inbox", help="Path to inbox drop zone")
    parser.add_argument("--fallback-scan", type=str, default="inputs", help="Fallback directory if inbox is empty")
    parser.add_argument("--output", type=str, default="inputs/catalog.json", help="Path to output catalog.json")
    parser.add_argument("--json", action="store_true", help="Print catalog as JSON to stdout")

    args = parser.parse_args()
    inbox_path = Path(args.inbox).resolve()
    
    if not inbox_path.exists():
        inbox_path.mkdir(parents=True, exist_ok=True)

    items = scan_directory(inbox_path)
    
    # Fallback to scanning inputs/ if inbox has no candidate documents
    if not items and args.fallback_scan:
        fallback_path = Path(args.fallback_scan).resolve()
        if fallback_path.exists() and fallback_path != inbox_path:
            items = scan_directory(fallback_path)

    catalog = {
        "schema_version": "1.0.0",
        "inbox_path": inbox_path.as_posix(),
        "total_documents": len(items),
        "documents": items
    }

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    if args.json:
        print(json.dumps(catalog, indent=2, ensure_ascii=False))
    else:
        print(f"\n============================================================")
        print(f"      LEARNING OS — UNIVERSAL SOURCE INTAKE CATALOG         ")
        print(f"============================================================")
        print(f"Drop Zone Target : {inbox_path}")
        print(f"Catalog SSOT     : {output_path}")
        print(f"Documents Found  : {len(items)}\n")
        
        for idx, doc in enumerate(items, start=1):
            if "error" in doc:
                print(f"[{idx}] {doc['filename']} -> ERROR: {doc['error']}")
            else:
                print(f"[{idx}] {doc['filename']} ({doc['line_count']} lines | {doc['size_bytes']} bytes)")
                print(f"    - Archetype  : {doc['archetype'].upper()} ({doc['recommended_track']})")
                print(f"    - Rationale  : {doc['rationale']}")
                if doc['headings_count'] > 0:
                    print(f"    - Headings   : {doc['headings_count']} sections detected (e.g. '{doc['outline_preview'][0]['title']}')")
                print()
        print("============================================================\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
