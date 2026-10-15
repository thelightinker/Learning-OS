---
name: socratic-companion-crafter
description: Kỹ thuật biên soạn Companion Guide sắc sảo chống paraphrase và thiết kế câu hỏi Socratic 3 tầng.
when_to_use: Kích hoạt khi soạn thảo lesson.md trong workflows/generate-lesson.md để chống tóm tắt hộ và xây dựng câu hỏi nhận thức.
allowed-tools: Read, Write, Edit
version: 1.1.0
triggers:
  - generate-lesson
  - draft-companion-guide
---

# Socratic Companion Crafter

Diệt tận gốc bệnh tóm tắt lại văn bản gốc (Paraphrase Trap) và bệnh đặt câu hỏi học vẹt khi viết `lesson.md`.

## 1. Anti-Paraphrase Lens Protocol
- **CẤM:** Viết lại nội dung nguồn kiểu: "Trong đoạn [¶2], tác giả giải thích rằng X là Y."
- **BẮT BUỘC:** Dùng 1 trong 3 lăng kính dẫn đọc (Reading Lenses):
  - **Structural Lens (Cấu trúc):** Chỉ rõ vị trí [¶N] trong mạch lập luận (ví dụ: *"Đọc [¶1]–[¶2] để tìm giả định ngầm tác giả sắp phá bỏ ở [¶3]"*).
  - **Blindspot Lens (Bẫy trực giác):** Cảnh báo điểm người đọc hay lướt qua hoặc hiểu ngược tại [¶N].
  - **Tension Lens (Đối trọng):** Đặt [¶N] cạnh [¶M] hoặc [S1] cạnh [S2] để làm nổi bật xung đột hoặc đánh đổi (trade-off).

## 2. 3-Tier Socratic Checkpoint Architecture
Mọi cụm câu hỏi trong bài học bắt buộc triển khai qua 3 nấc nhận thức lũy tiến:
1. **Tier 1 — Pre-Read Prediction:** Tình huống giả định ép người học đoán kết quả trước khi đọc [¶N].
2. **Tier 2 — Boundary & Mutation Probe:** *"Nếu đảo ngược hoặc xóa bỏ điều kiện X tại [¶N], thành phần nào sụp đổ đầu tiên?"*
3. **Tier 3 — Far Transfer:** Áp dụng nguyên lý vừa học sang một lĩnh vực khác nhưng đồng cấu trúc.

## 3. Orthogonal Rubric Binding
Bộ tiêu chí trong Embedded Rubric phải độc lập trực giao:
- **Tiêu chí 1 (Fidelity):** Mức độ bám sát bằng chứng gốc [¶N]/[S#].
- **Tiêu chí 2 (Causality):** Tính đúng đắn của chuỗi liên kết nhân quả.
- **Tiêu chí 3 (Boundaries):** Khả năng bao quát các trường hợp biên (edge cases).

## 4. Examples
```markdown
# Đoạn nguồn: [¶1]-[¶2] về cơ chế phân giải DNS và TTL Cache
- Tier 1: "Trước khi đọc [¶3], điều gì xảy ra nếu IP server đổi nhưng TTL còn 3600s?"
- Tier 2: "Nếu TTL = 0, điểm nghẽn nào sẽ sập đầu tiên trong hệ thống?"
- Tier 3: "Liên hệ cơ chế TTL này với việc vô hiệu hóa Token phiên đăng nhập (JWT)."
```
