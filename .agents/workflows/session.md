---
name: session
description: Điều phối phiên học và ôn tập ngắt quãng
version: 1.1.0
requires_agents:
  - learning-architect
requires_skills:
  - diagnostic-rubric-clinician
artifact_outputs:
  - progress.md
---

# Workflow: /session (Điều Phối Phiên Học Chủ Động & Spaced Retrieval)

Quy trình kích hoạt phiên học, đọc snapshot trạng thái, nạp on-demand skill chẩn đoán, kiểm tra hàng đợi ôn tập ngắt quãng, và tương tác đối thoại Socratic.

---

### [STATE: READ_SNAPSHOT]
- **Mục tiêu:** Nạp đúng vị trí hiện tại và điểm yếu mở của người học mà không gây lãng phí context token.
- **Input Artifacts:** `learning-space/courses/<course>/progress.md`.
- **DoD:**
  - [ ] Agent đã đọc `progress.md` trước khi đưa ra câu nói đầu tiên.
  - [ ] Xác định được module đang học và danh sách các mục trong hàng đợi ôn tập.
- **Evaluation Loop:** Pass -> Chuyển sang `[STATE: SPACED_RETRIEVAL_CHECK]` | Fail -> Yêu cầu người học chọn khóa học.

---

### [STATE: SPACED_RETRIEVAL_CHECK]
- **Mục tiêu:** Củng cố các điểm yếu cũ bằng phương pháp truy hồi ngắt quãng (Spaced Retrieval) 4 chặng:
  Lần sai -> (+1d) Chặng 1 -> (+3d) Chặng 2 -> (+7d) Chặng 3 -> (+14d) Chặng 4 -> MASTERED
- **Thực thi (READ_SKILL):**
  - Nếu `## Hàng đợi Ôn tập` trong `progress.md` có mục đến hạn: Đọc `skills/diagnostic-rubric-clinician/SKILL.md` để chuyển hóa Micro-Trigger thành tối đa 2 câu hỏi kiểm tra nhanh.
  - Người học trả lời đúng -> Thăng cấp chặng tiếp theo (hoặc gán `MASTERED`).
  - Người học trả lời sai -> Đưa về Chặng 1 (+1 ngày).
- **DoD:**
  - [ ] Chỉ hỏi tối đa 2 câu truy hồi, không biến thành bài kiểm tra kéo dài gây mệt mỏi.
- **Evaluation Loop:** Hoàn thành ôn tập -> Chuyển sang `[STATE: ACTIVE_LEARNING_DIALOGUE]`.

---

### [STATE: ACTIVE_LEARNING_DIALOGUE]
- **Mục tiêu:** Hướng dẫn người học qua từng Điểm dừng Socratic trong `lesson.md`.
- **Hành động:**
  - Yêu cầu người học đọc kỹ các đoạn neo `[¶N]` tương ứng trong `source_verbatim.md`.
  - Đặt câu hỏi gợi mở, lắng nghe câu trả lời và phản hồi gợi ý (không đưa ngay đáp án).
  - Nếu module có Web Lab: Nhắc người học mở file `lab.html` trên trình duyệt để kéo thả tham số và bấm nút *"Sao chép kết quả Lab"*.
- **DoD:**
  - [ ] Mỗi phản hồi của Agent đều có tính chất gợi mở hoặc thẩm định luận điểm, không giảng bài độc thoại.
- **Evaluation Loop:** Người học nộp câu trả lời bài tập hoặc dán `[LAB_RECEIPT]` -> Chuyển giao sang `workflows/assess.md`.
- **[ESCALATE_HUMAN]:** Nếu người học bối rối hoặc yêu cầu giải thích lại khái niệm nền tảng, Agent chuyển sang phong cách giải thích đời thường (Feynman).
