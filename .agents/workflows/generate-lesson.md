---
name: generate-lesson
description: Biên dịch module bài học và phòng lab
version: 1.1.0
requires_agents:
  - learning-architect
requires_skills:
  - socratic-companion-crafter
  - interactive-lab-architect
artifact_outputs:
  - lesson.md
  - source_verbatim.md
---

# Workflow: /generate-lesson (Biên Dịch Module Bài Học)

Quy trình trích xuất nguồn cơ học, thẩm định cổng thị giác, nạp on-demand skill chế tác, tạo tài liệu đồng hành `lesson.md` và phòng lab nếu cần, kết thúc bằng kiểm định tự động.

---

### [STATE: EXTRACT_SOURCE]
- **Mục tiêu:** Cắt phân đoạn nguyên văn từ file gốc mà không qua LLM token.
- **Input Artifacts:** `syllabus.md` (chứa `start_line` và `end_line` của module).
- **Output Artifacts:** `modules/M<NN>_<slug>/source_verbatim.md`.
- **Thực thi:**
  ```bash
  python .agents/scripts/extract_segment.py \
    --source "<source-path>" \
    --start-line <N> \
    --end-line <M> \
    --output "learning-space/courses/<course>/modules/M<NN>/source_verbatim.md"
  ```
- **DoD:**
  - [ ] `source_verbatim.md` tồn tại và có header `verbatim_meta` JSON hợp lệ.
  - [ ] Các đoạn văn bản ngoài code block được đánh số neo `[¶1]`, `[¶2]` đầy đủ.
- **Evaluation Loop:** Pass -> Chuyển `[STATE: VISUAL_GATE]` | Fail -> Hiệu chỉnh mốc dòng.

---

### [STATE: VISUAL_GATE]
- **Mục tiêu:** Quyết định hình thức biểu đạt thị giác theo quy tắc Text-First.
- **Tiêu chí:**
  - Nếu chỉ là phân tích câu chữ/logic đơn tuyến -> Gán `visual: none`.
  - Nếu có luồng hệ thống hoặc cây phân nhánh -> Gán `visual: mermaid` nhúng trong bài.
  - Nếu có hệ động lực nhân quả kéo thả tham số -> Gán `visual: lab` và sinh `lab.html`.
- **DoD:**
  - [ ] Có trường frontmatter `visual:` và `visual_reason:` giải thích cụ thể lý do sư phạm.
- **Evaluation Loop:** Pass -> Chuyển `[STATE: LOAD_CRAFTSMANSHIP_SKILL]` | Fail -> Bổ sung lý do sư phạm.

---

### [STATE: LOAD_CRAFTSMANSHIP_SKILL]
- **Mục tiêu:** Nạp on-demand kỹ thuật chế tác chuyên sâu vào context trước khi viết bài học.
- **Thực thi (READ_SKILL):**
  - Đọc `skills/socratic-companion-crafter/SKILL.md` trước khi viết `lesson.md` (áp dụng Anti-Paraphrase Lenses, Socratic 3 nấc, Orthogonal Rubric).
  - Nếu [STATE: VISUAL_GATE] chọn `visual: lab`: Đọc thêm `skills/interactive-lab-architect/SKILL.md` trước khi sinh `lab.html` (áp dụng cơ chế phi tuyến, Ghost Trace, Rich Telemetry).
- **DoD:**
  - [ ] Đã nạp đúng skill cần thiết theo dạng module và sẵn sàng viết bài.
- **Evaluation Loop:** Pass -> Chuyển `[STATE: COMPOSE_LESSON]`.

---

### [STATE: COMPOSE_LESSON]
- **Mục tiêu:** Soạn `lesson.md` (Companion Guide hoặc Synthesis) và `lab.html` (nếu có).
- **Output Artifacts:**
  - `modules/M<NN>_<slug>/lesson.md`
  - `modules/M<NN>_<slug>/lab.html` (tùy chọn)
- **DoD:**
  - [ ] `lesson.md` tham chiếu chính xác các nhãn neo `[¶N]` có thực trong `source_verbatim.md`.
  - [ ] Có đủ 5 phần chuẩn: Trực giác cốt lõi, Socratic checkpoints, Thuật ngữ, Bài tập tình huống, Embedded Rubric.
  - [ ] Nếu có `lab.html`: 100% offline, có `window.onerror`, có nút copy payload `[LAB_RECEIPT]`.
- **Evaluation Loop:** Pass -> Chuyển `[STATE: VERIFY_MODULE]` | Fail -> Hoàn thiện nội dung.

---

### [STATE: VERIFY_MODULE]
- **Mục tiêu:** Chạy bộ kiểm thử tĩnh tự động trên module vừa tạo.
- **Thực thi:**
  ```bash
  python .agents/scripts/verify_system.py --course "learning-space/courses/<course>"
  ```
- **DoD:**
  - [ ] Lệnh kiểm thử trả về exit code 0 (`PASS: Course is 100% verified and green`).
  - [ ] Không có lỗi `CRITICAL_SOURCE_MUTATION`, `EXTERNAL_URL_DETECTED` hay `HALLUCINATED_ANCHOR`.
- **Evaluation Loop:** Pass -> Hoàn tất module | Fail -> Tự động sửa lỗi theo thông báo linter.
- **[ESCALATE_HUMAN]:** Nếu băm sai lệch do tệp nguồn gốc bị thay đổi ngoài ý muốn, báo người học xác nhận.
