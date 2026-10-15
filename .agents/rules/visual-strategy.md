---
name: visual-strategy
trigger: model_decision
description: Quy tắc chiến lược trực quan hóa, cổng quyết định Visual/Lab, bảng màu WCAG AA và rào chắn offline.
version: 1.0.0
priority: P1
---

# Visual Strategy & Pragmatic Labs (Chiến Lược Trực Quan Hóa)

## 1. Nguyên Tắc Text-First & Cổng Lọc Thị Giác
Mặc định bài học chỉ dùng văn bản Markdown thuần túy. Mỗi file `lesson.md` bắt buộc có frontmatter:
```yaml
---
visual: none | mermaid | svg | lab
visual_reason: "Lý do sư phạm bắt buộc phải có visual"
---
```
Nếu `visual` khác `none`, phải chứng minh được: cấu trúc không thể giải thích bằng 3 câu văn, hoặc có quan hệ nhân quả tương tác cần kéo thả tham số.

## 2. Tiêu Chuẩn Các Dạng Trực Quan
- **Mermaid:** Dùng cho flowchart, sequence diagram đơn giản. Nhúng trực tiếp trong Markdown.
- **Inline SVG (`visual.svg`):** Dùng cho ma trận so sánh, kiến trúc phân tầng. Bắt buộc có `viewBox`, responsive, font `system-ui`.
- **Interactive Web Lab (`lab.html`):** Tự chứa trong 1 file duy nhất $\le 400$ dòng.

## 3. Bảng Màu Chuẩn WCAG AA (Độ Tương Phản $\ge 4.5:1$)
Toàn bộ sơ đồ SVG và Web Lab phải dùng bảng màu cố định:
- Nền chính: `#0f172a` (Slate Dark) | Nền phụ: `#1e293b`
- Chữ chính: `#f8fafc` (Light) | Chữ phụ: `#94a3b8`
- Điểm nhấn 1: `#38bdf8` (Cyan/Sky) | Điểm nhấn 2: `#a855f7` (Purple)
- Thành công: `#22c55e` (Green) | Cảnh báo/Lỗi: `#ef4444` (Red)

## 4. Rào Chắn Web Lab Ngoại Tuyến (100% Offline)
- CẤM toàn bộ liên kết ngoài (`http://`, `https://`), CDN (Tailwind, FontAwesome, Google Fonts), CSS `@import`, JS `import/fetch`. Ngoại lệ duy nhất: SVG namespace chuẩn XML.
- Bắt buộc có cơ chế `window.onerror` bắt lỗi runtime hiển thị trực quan.
- Quy trình tương tác 3 bước: Predict (Dự đoán) -> Manipulate (Kéo tham số) -> Explain (Giải thích).
- Cầu nối trạng thái: Nút *"Sao chép kết quả Lab"* xuất block chuẩn `[LAB_RECEIPT]...[/LAB_RECEIPT]` vào Clipboard để nộp vào chat.
