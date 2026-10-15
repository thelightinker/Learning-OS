---
name: tech-decisions
type: reference
created: 2026-10-15
updated: 2026-10-15
description: Các quyết định kiến trúc và công nghệ bản lề
version: 1.0.0
---

# Memory: Technical Decisions

Các quyết định kiến trúc và công nghệ mang tính bản lề.

- **100% Python Standard Library:** Loại bỏ mọi dependency ngoài (không dùng D2, Markmap, FastAPI, SQLite) để đảm bảo kit chạy ngay lập tức trên bất kỳ môi trường nào có Python 3.
- **Normalized SHA-256 Hash:** Chuẩn hóa Unicode NFC và khoảng trắng để đối soát tính toàn vẹn câu chữ thay vì đếm từ.
- **Dual-file persistence:** Khống chế `progress.md` $\le 200$ dòng để bảo toàn context window $\le 4.000$ tokens.
