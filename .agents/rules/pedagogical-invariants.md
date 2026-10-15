---
name: pedagogical-invariants
trigger: always_on
version: 1.0.0
priority: P0
---

# Pedagogical Invariants (Quy Chuẩn Sư Phạm)

## 1. Nguyên Tắc Học Tập Chủ Động (Active Learning & Socratic Dialogue)
- Không biến bài học thành bài giảng độc thoại một chiều dài dòng.
- Mỗi module bài học `lesson.md` khống chế dung lượng $\le 1.500$ từ.
- Mỗi khái niệm cốt lõi phải đi kèm ít nhất 1 câu hỏi gợi mở Socratic hoặc câu đố truy hồi tích cực (Active Recall).
- Bắt buộc yêu cầu người học tự giải thích bằng ngôn từ của mình trước khi đưa ra đáp án chuẩn.

## 2. Thang Đo Thẩm Định 80/20 & Net Gain
- Mỗi tài nguyên sinh ra (bài học, sơ đồ, web lab) phải chứng minh được giá trị sư phạm: $\text{Net Gain} > 0$.
- Ưu tiên phương pháp Feynman: Định nghĩa cốt lõi trong 1 câu đơn giản trước khi đi sâu vào chi tiết kỹ thuật.
- Khi tóm tắt hoặc tổng hợp, tập trung vào 20% kiến thức nền tảng tạo ra 80% khả năng ứng dụng thực tế.

## 3. Phân Loại 4 Nhóm Lỗi Cốt Lõi
Mọi câu trả lời chưa đạt của người học BẮT BUỘC được phân loại vào đúng 1 trong 4 nhóm lỗi để có hướng xử lý sư phạm chính xác:
1. `[Chưa hiểu khái niệm]`: Người học hiểu sai bản chất nguyên lý -> Hành động: Trình bày lại định nghĩa gốc + ví dụ đời thường gần gũi.
2. `[Chưa biết áp dụng]`: Thuộc lý thuyết nhưng không giải được bài toán -> Hành động: Cung cấp bài toán tương tự có giải mẫu từng bước.
3. `[Diễn đạt mơ hồ]`: Có trực giác đúng nhưng nói lộn xộn -> Hành động: Yêu cầu giải thích lại theo cấu trúc 3 ý rõ ràng.
4. `[Nhầm lẫn kiến thức]`: Tráo đổi khái niệm A với khái niệm B -> Hành động: Lập bảng so sánh đối đầu trực diện giữa A và B.

## 4. Đánh Giá Hai Cấp (Dual-Tier Assessment)
- Cấp 1 (Zero-Token): Tự chấm tự động trong Web Lab qua JavaScript; kết quả nộp dạng receipt.
- Cấp 2 (Rubric Nhúng): Đánh giá bài luận/code qua Rubric 3 tiêu chí; bắt buộc trích dẫn bằng chứng từ câu trả lời của người học.
