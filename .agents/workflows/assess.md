---
name: assess
description: Chấm điểm rubric, tiếp nhận lab receipt và cập nhật tiến độ
version: 1.1.0
requires_agents:
  - learning-architect
requires_skills:
  - diagnostic-rubric-clinician
artifact_outputs:
  - progress.md
  - progress-log.md
---

# Workflow: /assess (Chấm Điểm Thích Ứng & Quản Trị Bộ Nhớ Bền Vững)

Quy trình đánh giá câu trả lời của người học hoặc kết quả thực nghiệm Web Lab, nạp on-demand skill chẩn đoán, gán 1 trong 4 mã lỗi nhận thức, cập nhật `progress.md`, ghi log bằng CLI và tự động cắt tỉa (compaction).

---

### [STATE: RECEIVE_SUBMISSION]
- **Mục tiêu:** Tiếp nhận câu trả lời bài tập hoặc chuỗi payload `[LAB_RECEIPT]`.
- **Thực thi (READ_SKILL):**
  - Đọc `skills/diagnostic-rubric-clinician/SKILL.md` vào context.
  - Nếu đầu vào chứa block `[LAB_RECEIPT]`: Đối chiếu thêm trường `explored_bounds` và `tipping_point_reached` trước khi chấm rubric.
- **Phân loại đầu vào:**
  - Nếu là payload `[LAB_RECEIPT]...[/LAB_RECEIPT]`: Chuyển sang Cấp 1 Zero-Token (kiểm tra `prediction_correct` và `mastery_score` tự động).
  - Nếu là câu trả lời bài luận / code: Chuyển sang Cấp 2 (chấm theo Embedded Rubric của `lesson.md`).
- **DoD:**
  - [ ] Nhận diện chính xác hình thức nộp bài trong 1 turn duy nhất.
- **Evaluation Loop:** Chuyển sang `[STATE: EVALUATE_AND_DIAGNOSE]`.

---

### [STATE: EVALUATE_AND_DIAGNOSE]
- **Mục tiêu:** Chấm điểm theo rubric 3 tiêu chí và gắn đúng 1 trong 4 nhãn lỗi chuẩn nếu chưa đạt:
  1. `[E1_ANCHOR_MISS]`: Bỏ sót hoặc đọc sai dữ kiện có thật tại đoạn [¶N] / [S#].
  2. `[E2_CAUSAL_GAP]`: Nhớ đúng từ khóa nhưng nối sai chiều nhân quả hoặc cơ chế vận hành.
  3. `[E3_BOUNDARY_BLIND]`: Công thức đúng ở điều kiện thường nhưng sập ở biên (hoặc `tipping_point_reached: false`).
  4. `[E4_TRANSFER_FAIL]`: Hiểu lý thuyết trong bài nhưng không áp dụng được sang bối cảnh mới.
- **Remediation Protocol:**
  - CẤM đưa đáp án mẫu ngay lần đầu nếu chưa đạt chuẩn qua bài.
  - BẮT BUỘC phản hồi bằng 1 Phản ví dụ (Counter-example) làm lộ mâu thuẫn trong lập luận của người học.
- **DoD:**
  - [ ] Mọi nhận xét đều trích dẫn bằng chứng cụ thể từ câu trả lời của người học.
  - [ ] Điểm số phân định rõ Mức 0, Mức 1 hoặc Mức 2 cho từng tiêu chí.
- **Evaluation Loop:** Chuyển sang `[STATE: PERSIST_AND_COMPACT]`.

---

### [STATE: PERSIST_AND_COMPACT]
- **Mục tiêu:** Cập nhật trạng thái vào `progress.md` và ghi nhật ký lịch sử mà không làm tràn context window.
- **Thực thi:**
  1. Ghi nhật ký vào `progress-log.md` qua lệnh CLI:
      ```bash
      python .agents/scripts/verify_system.py \
        --append-log "learning-space/courses/<course>/progress-log.md" \
        --entry "[YYYY-MM-DD] Module M<NN>: <PASSED/FAILED> (Chi tiết kết quả)"
      ```
  2. Cập nhật `progress.md`:
     - Nếu đạt: Đổi trạng thái module sang `COMPLETED`, chuyển sang module tiếp theo.
     - Nếu chưa đạt: Thêm khái niệm lỗi vào `## Hàng đợi Ôn tập (Spaced Retrieval)` ở Chặng 1 (+1 ngày).
  3. Kiểm tra số dòng của `progress.md`:
     - Nếu $> 150$ dòng: Chuyển các mục đã `MASTERED` sang `progress-log.md` để giữ tệp $\le 100$ dòng.
- **DoD:**
  - [ ] `progress.md` được cập nhật và duy trì $\le 150$ dòng.
  - [ ] Lệnh `--append-log` chạy thành công với exit code 0.
- **Evaluation Loop:** Hoàn tất đánh giá -> Chúc mừng người học và chuyển tiếp module tiếp theo.
- **[ESCALATE_HUMAN]:** Nếu người học liên tục thất bại 3 lần trên cùng một khái niệm, đề xuất tạm dừng và gợi ý tài liệu đọc thêm để củng cố.
