---
visual: none
visual_reason: Khái niệm phân định thẻ ngữ nghĩa và cấu trúc form thiên về tư duy phân loại logic và chuẩn trợ năng, giải thích hoàn toàn mạch lạc bằng văn bản và bảng so sánh
---

# BÀI HỌC TỔNG HỢP: HTML5 SEMANTIC & BIỂU MẪU NHẬP LIỆU (FORMS)
*Module M01_html-semantic-forms — Trích xuất trọng tâm Chương 3 [S1]*

## 1. Trực Giác Cốt Lõi (Feynman Intuition)
- **Định nghĩa 1 câu kiểu Feynman:** Thẻ HTML ngữ nghĩa (Semantic HTML) giống như biển chỉ dẫn trên phố — nó không chỉ giúp con người nhìn thấy cái hộp chữ nhật, mà còn giúp cỗ máy tìm kiếm (SEO) và trình đọc màn hình người khiếm thị hiểu chính xác cái hộp đó sinh ra để làm gì.
- **Mục tiêu 80/20:** Xóa bỏ hoàn toàn "bệnh lạm dụng thẻ `<div>`" (Div Soup) và làm chủ thẻ `<form>` cùng các trường `input` thu thập dữ liệu chuẩn đại học.

## 2. Các Luận Điểm Cốt Lõi (Synthesized Principles)
- **Phân tách Khung Xương (Page Layout Anatomy):**
  - `<header>`: Khu vực đầu trang hoặc đầu bài viết (logo, tiêu đề).
  - `<nav>`: Danh sách liên kết điều hướng chính của website.
  - `<main>`: Nội dung độc bản duy nhất của trang (mỗi tài liệu chỉ có duy nhất 1 thẻ `<main>`).
  - `<section>` vs `<article>`: `<article>` là khối nội dung độc lập có thể tái xuất bản ở nơi khác (bài viết, sản phẩm); `<section>` là phân đoạn theo chủ đề nội tại.
  - `<footer>`: Chân trang (bản quyền, liên hệ, chính sách).
- **Cấu trúc Biểu Mẫu Chuẩn Form:**
  - Thẻ bao ngoài: `<form action="/submit" method="POST">`.
  - Cơ chế bắt buộc giữa nhãn và ô nhập: `<label for="user-email">` phải luôn khớp với `<input id="user-email" name="email" type="email" required>`. Nhấn vào text label phải focus ngay vào ô input.
  - Phân loại `input`: `type="text"`, `type="password"`, `type="email"`, `type="number"`, `type="radio"` (cùng `name` để chọn 1), `type="checkbox"`.
  - Khối chọn lựa & văn bản dài: `<select>` kèm `<option>`, `<textarea>`.

## 3. Bẫy Trực Giác & So Sánh Đối Đầu
| Tiêu chí | Tiếp cận Ngây thơ (Div Soup) | Tiếp cận Chuẩn Ngữ Nghĩa (Semantic) |
|---|---|---|
| **Cấu trúc code** | `<div class="menu">`, `<div class="header">` | `<header>`, `<nav>`, `<aside>` |
| **Trợ năng (Accessibility - a11y)** | Trình đọc màn hình mù tịt, coi mọi thứ là khối vô danh | Nhận diện phím tắt chuyển vùng nhảy nhanh đến menu |
| **SEO & Google Bot** | Phải suy đoán nội dung chính, thứ hạng tìm kiếm thấp | Nhận diện ngay lõi bài viết nằm trong `<article>` và `<main>` |
| **Xử lý phím Enter** | Phải viết JavaScript `onkeydown` để submit | Trình duyệt tự submit form khi bấm Enter nếu có `<button type="submit">` |

## 4. Chuỗi Câu Hỏi Socratic 3 Tầng
1. **Tier 1 (Dự đoán tiền đề):** Nếu một biểu mẫu đăng nhập có 2 trường username và password nhưng không bọc trong thẻ `<form>` mà chỉ bọc trong thẻ `<div>`, người dùng bấm phím `Enter` trên bàn phím có gửi được dữ liệu đi không? Tại sao?
2. **Tier 2 (Biên & Đột biến):** Điều gì sẽ xảy ra nếu lập trình viên đặt 3 ô chọn radio giới tính (Nam, Nữ, Khác) nhưng lại đặt thuộc tính `name` của 3 ô đó khác nhau (`name="gender1"`, `name="gender2"`, `name="gender3"`)?
3. **Tier 3 (Chuyển giao xa):** Tại sao trong kiến trúc Microservices và REST API hiện đại, việc phân biệt rạch ròi giữa `method="GET"` (tìm kiếm, lọc) và `method="POST"` (thêm mới, thanh toán) ở cấp độ thẻ `<form>` HTML lại có ý nghĩa sống còn đối với bộ nhớ đệm (HTTP Cache)?

## 5. Tiêu Chí Đánh Giá (Embedded Rubric)
| Tiêu chí | Mức 0 (Chưa hiểu bản chất) | Mức 1 (Đạt yêu cầu) | Mức 2 (Thành thạo kiến trúc) |
|---|---|---|---|
| **Cấu trúc ngữ nghĩa (Semantic)** | Vẫn dùng `<div>` thay thế cho toàn bộ layout chính | Dùng đúng thẻ `<header>`, `<nav>`, `<main>`, `<footer>` | Phân biệt chính xác ranh giới sử dụng giữa `<article>` và `<section>`, giải thích được ảnh hưởng SEO |
| **Kỹ thuật Form Binding** | Bỏ sót thuộc tính `for` trên `<label>` hoặc không gán `id` tương ứng | Ghép nối chuẩn `label[for]` với `input[id]`, dùng đúng `type` | Sử dụng thành thạo các ràng buộc HTML5 (`required`, `pattern`, `min/max`) kèm nhóm `radio` cùng `name` |
| **Hiểu biết luồng HTTP** | Nhầm lẫn giữa phương thức `GET` và `POST` khi gửi dữ liệu | Chỉ ra được `GET` đưa tham số lên URL, `POST` giấu trong Body | Phân tích được lỗ hổng bảo mật khi gửi dữ liệu nhạy cảm qua URL và cơ chế idempotent của HTTP |
