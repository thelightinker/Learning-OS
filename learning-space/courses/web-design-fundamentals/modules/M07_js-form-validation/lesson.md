---
visual: none
visual_reason: Khái niệm biểu thức chính quy (RegExp pattern matching) và xử lý sự kiện submit Form Validation thiên về logic đối sánh chuỗi văn bản và quản lý trạng thái lỗi người dùng, giải thích tối ưu qua bảng khuôn mẫu Regex và mã nguồn thực chiến
---

# BÀI HỌC TỔNG HỢP: FORM VALIDATION THỰC CHIẾN VỚI REGEXP & XỬ LÝ LỖI
*Module M07_js-form-validation — Trích xuất trọng tâm Chương 5 [S1]*

## 1. Trực Giác Cốt Lõi (Feynman Intuition)
- **Định nghĩa 1 câu kiểu Feynman:** Biểu thức chính quy (Regular Expression) giống như một cái khuôn đúc bánh — dữ liệu người dùng nhập vào là bột, nếu vừa khít với khuôn (đúng dạng email, số điện thoại) thì cho qua, còn nếu méo mó thì chặn ngay tại cửa lò trước khi gửi về máy chủ.
- **Mục tiêu 80/20:** Làm chủ kỹ thuật chặn gửi form mặc định bằng `event.preventDefault()`, sử dụng `RegExp.test()` để kiểm tra tính hợp lệ của dữ liệu, và hiển thị thông báo lỗi thân thiện chuẩn đồ án tốt nghiệp.

## 2. Các Luận Điểm Cốt Lõi (Synthesized Principles)
- **Chốt Chặn Đầu Tiên: Vô Hiệu Hóa Hành Vi Mặc Định:**
  ```javascript
  const form = document.querySelector('#register-form');
  form.addEventListener('submit', function(e) {
    e.preventDefault(); // CỰC KỲ QUAN TRỌNG: Ngăn trang web tải lại gây mất dữ liệu!
    // Tiến hành kiểm tra dữ liệu...
  });
  ```
- **Khuôn Mẫu Biểu Thức Chính Quy (RegExp 80/20):**
  - Cú pháp khởi tạo literal: `/^pattern$/` (`^` bắt đầu chuỗi, `$` kết thúc chuỗi).
  - Phương thức kiểm tra: `regex.test(inputString)` $\rightarrow$ trả về `true` hoặc `false`.
  - Bảng khuôn mẫu hay dùng nhất trong bài thi:
    - *Email chuẩn:* `/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/`
    - *Số điện thoại Việt Nam:* `/^(0[3|5|7|8|9])+([0-9]{8})$/` (10 chữ số, bắt đầu bằng 03, 05, 07, 08, 09).
    - *Mật khẩu mạnh:* `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/` (Ít nhất 8 ký tự, gồm chữ hoa, chữ thường và số).
- **Quy Trình Xử Lý Lỗi Thân Thiện UX:**
  - Không bao giờ dùng hàm `alert()` để báo lỗi (thô thiển, chặn tương tác trình duyệt).
  - Bổ sung thẻ `<span class="error-msg">` ngay dưới mỗi ô input.
  - Khi có lỗi: gán class `input-error` (viền đỏ) và chèn thông điệp lỗi vào thẻ `span`.
  - Khi người dùng bắt đầu gõ sửa: lắng nghe sự kiện `'input'` để xóa lỗi ngay lập tức.

## 3. Bẫy Trực Giác & So Sánh Đối Đầu
| Tình huống | Validation Ngây Thơ (HTML5 only) | Validation Toàn Diện (JavaScript + RegExp) |
|---|---|---|
| **Khả năng tùy biến thông báo lỗi** | Dùng tooltip mặc định của trình duyệt, thô cứng và phụ thuộc ngôn ngữ máy tính | Tự do định dạng CSS, hiển thị icon và thông báo tiếng Việt mượt mà |
| **Logic phụ thuộc nhiều trường** | Không thể so sánh xem "Mật khẩu" và "Nhập lại mật khẩu" có khớp nhau không | Dễ dàng so khớp logic `passInput.value === confirmInput.value` |
| **Kiểm tra thời gian thực (Real-time)** | Chỉ kích hoạt khi người dùng bấm nút Submit | Kích hoạt ngay khi người dùng rời chuột (`blur`) hoặc đang gõ (`input`) |
| **Tầm quan trọng đối với Backend** | Người dùng có thể tắt JavaScript hoặc dùng Postman để bypass | **Nguyên tắc bất biến:** Client-side validation chỉ để tăng trải nghiệm UX; Backend BẮT BUỘC phải validate lại lần 2! |

## 4. Chuỗi Câu Hỏi Socratic 3 Tầng
1. **Tier 1 (Dự đoán tiền đề):** Nếu trong hàm lắng nghe sự kiện `submit` của biểu mẫu bạn quên gọi lệnh `event.preventDefault()`, điều gì sẽ xảy ra khi người dùng bấm nút Đăng ký dù dữ liệu nhập vào toàn bộ là sai?
2. **Tier 2 (Biên & Đột biến):** Biểu thức chính quy kiểm tra email `/^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$/` có nhược điểm gì? Địa chỉ email `nguyen.van.a+test@gmail.com` có vượt qua được biểu thức này không? Cần sửa ký tự nào trong regex?
3. **Tier 3 (Chuyển giao xa):** Tại sao có câu nói: *"Đừng bao giờ tin tưởng bất kỳ dữ liệu nào đến từ Client"*, và nếu JavaScript trên trình duyệt đã kiểm tra RegExp cực kỳ chặt chẽ rồi thì vì sao Server vẫn phải viết mã kiểm tra lại từ đầu?

## 5. Tiêu Chí Đánh Giá (Embedded Rubric)
| Tiêu chí | Mức 0 (Chưa đạt) | Mức 1 (Đạt yêu cầu) | Mức 2 (Thành thạo) |
|---|---|---|---|
| **Làm chủ Luồng Submit Form** | Quên `preventDefault()` khiến form tự refresh trang mất dấu vết lỗi | Chặn submit đúng cách, lấy được giá trị `.trim()` từ các ô input | Cấu trúc luồng validation phân tách module rõ ràng, trả về trạng thái boolean mạch lạc |
| **Kỹ năng sử dụng RegExp** | Không hiểu cú pháp regex, copy bừa các chuỗi pattern trên mạng | Viết và đọc hiểu các ký tự biên `^`, `$`, `+`, `*`, `[a-z]` cơ bản | Tự thiết kế regex kiểm tra định dạng phức tạp (mã sinh viên, mật khẩu có ký tự đặc biệt) |
| **Thiết kế Trải nghiệm Lỗi (UX)** | Lạm dụng `alert()` giật cục làm phiền người dùng | Hiển thị lỗi đỏ dưới chân input và ẩn lỗi khi người dùng gõ lại | Tạo hiệu ứng shake rung nhẹ khi submit lỗi và focus tự động vào trường lỗi đầu tiên |
