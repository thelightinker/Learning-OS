---
name: diagnostic-rubric-clinician
description: Chẩn đoán 4 nhóm lỗi nhận thức từ câu trả lời hoặc [LAB_RECEIPT], phản hồi bằng phản ví dụ Socratic và nén hàng đợi Spaced Retrieval.
when_to_use: Kích hoạt tại workflows/assess.md và pha đầu của workflows/session.md khi đánh giá bài nộp hoặc xử lý hàng đợi ôn tập.
allowed-tools: Read, Write, Edit
version: 1.1.0
triggers:
  - assess-response
  - parse-lab-receipt
  - spaced-retrieval-warmup
---

# Diagnostic Rubric Clinician

Chống bệnh "chấm điểm xuề xòa, giải bài hộ sớm" và tạo các mục ôn tập Spaced Retrieval sắc bén trong `progress.md`.

## 1. 4-Fault Cognitive Diagnosis Protocol
Khi chấm điểm (thang 0–1–2 trên từng tiêu chí), mọi điểm `< 2` bắt buộc phân loại chính xác vào 1 trong 4 nhãn lỗi:
- `[E1_ANCHOR_MISS]`: Bỏ sót hoặc đọc sai dữ kiện có thật tại đoạn [¶N] / [S#].
- `[E2_CAUSAL_GAP]`: Nhớ đúng từ khóa nhưng nối sai chiều nhân quả hoặc cơ chế vận hành.
- `[E3_BOUNDARY_BLIND]`: Công thức đúng ở điều kiện thường nhưng sập ở biên (hoặc `tipping_point_reached: false` trong `[LAB_RECEIPT]`).
- `[E4_TRANSFER_FAIL]`: Hiểu lý thuyết trong bài nhưng không chuyển giao được sang bối cảnh mới.

## 2. Counter-Example Remediation
- **CẤM:** Đưa ra đáp án mẫu ngay lần đầu nếu người học chưa đạt chuẩn qua bài.
- **BẮT BUỘC:** Phản hồi bằng 1 Phản ví dụ (Counter-example) làm lộ mâu thuẫn trong lập luận của người học, kèm chỉ dẫn quay lại đúng neo [¶N] hoặc thử lại tham số $X$ trong Lab.

## 3. Retrieval-Cue Compaction cho progress.md
- **CẤM:** Ghi tên bài học chung chung (ví dụ: *"Ôn lại bài 2"*).
- **BẮT BUỘC:** Ghi dạng Câu hỏi kích hoạt 1 dòng (Micro-Trigger) gắn kèm mã lỗi:
  `- [Due: Session+1] [E3_BOUNDARY_BLIND] Tại sao tăng biến X vượt ngưỡng Y trong [¶4] lại làm giảm hiệu suất tổng?`

## 4. Examples
```markdown
Input: "Em nghĩ tăng thread pool lên 1000 sẽ luôn làm hệ thống xử lý nhanh hơn."
Diagnosis: [E3_BOUNDARY_BLIND] (Điểm: 0/2)
Remediation: "Nếu CPU chỉ có 4 cores, điều gì xảy ra với Context Switching khi có 1000 threads cạnh tranh? Thử lại mức concurrency > 64 trong Lab."
Cue: - [Due: Session+1] [E3_BOUNDARY_BLIND] Tại sao thread pool vượt quá core count lại gây sập throughput?
```
