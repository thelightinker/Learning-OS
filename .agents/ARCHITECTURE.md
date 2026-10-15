# Learning OS — System Architecture

## 1. System Overview & Core Invariants
Learning OS is an IDE Agent-First pedagogical operating system that compiles heterogeneous raw knowledge sources (books, papers, transcripts) into active learning experiences.

### Key Invariants:
1. **IDE Agent First & Zero-Infrastructure Overhead:** Operates entirely within the IDE Agent environment. The local filesystem is the database. No external databases, servers, or cloud backends.
2. **Mechanical Verbatim Source Slicing:** Extracts source materials using deterministic line offsets via Python Standard Library (`extract_segment.py`), bypassing LLM text generation.
3. **Normalized SHA-256 Verification:** Verifies segment integrity by hashing Unicode NFC and whitespace-collapsed text slices.
4. **Offline Interactive Labs:** Self-contained single-file HTML/JS/SVG simulations with runtime error boundaries and clipboard bridge receipts.
5. **Dual-File Persistent Memory:** Fixed-size snapshot (`progress.md` <= 200 lines) + append-only history (`progress-log.md`).

## 2. Non-Goals & Intentional Scope Boundaries
- **No OCR for scanned image PDFs:** The user must provide plain text, Markdown, or PDFs with readable text layers.
- **No external cloud synchronization:** State is maintained locally on disk and synced via personal Git if desired.
- **No standalone LMS web applications:** Everything runs natively in the user's IDE editor and local browser.
- **No background cron daemons:** Spaced retrieval review triggers on-demand when the learner opens a new session.

## 3. Component Inventory
| Component | Count |
|---|---|
| **Total Agents** | 1 |
| **Total Skills** | 3 |
| **Total Workflows** | 5 |
| **Total Skill Scripts** | 0 |

## 4. Component Topology
- `agent/learning-architect.md`: Master Orchestrator coordinating all 5 workflows.
- `skills/`: 3 on-demand craftsmanship skills (`socratic-companion-crafter`, `interactive-lab-architect`, `diagnostic-rubric-clinician`).
- `workflows/`: 5 workflows (`prep-course`, `ingest`, `generate-lesson`, `session`, `assess`).
- `.agents/rules/`: Pedagogical invariants, verbatim quarantine, and visual strategy rules.
- `.agents/scripts/`: 100% Python stdlib tools (`catalog_inbox.py`, `extract_segment.py`, `verify_system.py`).
- `learning-space/courses/`: User course directories containing syllabus, modules, and progress tracking.
