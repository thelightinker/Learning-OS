---
name: ingest
description: Tiếp nhận nguồn và lập lộ trình 80/20
version: 1.0.0
requires_agents:
  - learning-architect
requires_skills: []
artifact_outputs:
  - syllabus.md
  - progress.md
---

# Workflow: /ingest (Tiếp Nhận Tri Thức & Lập Lộ Trình 80/20)

Quy trình tiếp nhận tài liệu nguồn, kiểm tra cấu trúc qua line offset, phân loại phương thức học và khởi tạo không gian khóa học.

---

### [STATE: INTAKE_AND_INSPECT]
- **Mục tiêu:** Quét cấu trúc tài liệu nguồn từ `inputs/` mà không gây tràn context window.
- **Input Artifacts:** Đường dẫn tệp nguồn (ví dụ: `inputs/books/clean-architecture.txt`).
- **Output Artifacts:** Bảng Headings và số dòng xuất ra terminal.
- **Thực thi:**
  ```bash
  python .agents/scripts/extract_segment.py --source "<source-path>" --inspect
  ```
- **DoD:**
  - [ ] Lệnh `--inspect` trả về exit code 0.
  - [ ] Xác định được tổng số dòng và danh sách các phần lớn của tài liệu.
- **Evaluation Loop:** Pass -> Chuyển sang `[STATE: CREATE_SYLLABUS]` | Fail -> Yêu cầu người học kiểm tra lại đường dẫn tệp nguồn.

---

### [STATE: CREATE_SYLLABUS]
- **Mục tiêu:** Tạo bản đồ lộ trình 80/20 và tệp snapshot tiến độ ban đầu.
- **Input Artifacts:** Thông tin mục lục từ bước trước + Mục tiêu của người học.
- **Output Artifacts:**
  - `learning-space/courses/<course-slug>/00_overview/syllabus.md`
  - `learning-space/courses/<course-slug>/progress.md`
- **DoD:**
  - [ ] `syllabus.md` chia nhỏ khóa học thành các module $1.500 - 3.000$ từ kèm mốc dòng `start_line` và `end_line`.
  - [ ] `progress.md` được khởi tạo đúng schema 3 phần và độ dài $\le 40$ dòng.
- **Evaluation Loop:** Pass -> Chuyển sang `[STATE: READY_FOR_LESSON]` | Fail -> Bổ sung cấu trúc module.

---

### [STATE: READY_FOR_LESSON]
- **Mục tiêu:** Báo cáo tóm tắt lộ trình cho người học và sẵn sàng soạn module đầu tiên.
- **Output:** Thông báo ngắn gọn (3-5 dòng) trong chat liệt kê các module cốt lõi và gợi ý lệnh tiếp theo: *"Soạn bài đầu tiên"*.
- **[ESCALATE_HUMAN]:** Nếu tài liệu nguồn là PDF dạng scan không có text layer, dừng lại và yêu cầu người học cung cấp bản text hoặc PDF có text.
