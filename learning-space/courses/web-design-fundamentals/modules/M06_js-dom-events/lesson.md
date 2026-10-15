---
visual: lab
visual_reason: Vòng đời sự kiện DOM (Event Bubbling, Event Delegation) và các thao tác thêm xóa Node trên cây DOM có tính chất nhân quả thời gian thực, bắt buộc người học phải tương tác trên Web Lab để nhìn thấy sự lan truyền sự kiện
---

# BÀI HỌC THỰC NGHIỆM: THAO TÁC DOM & XỬ LÝ SỰ KIỆN TƯƠNG TÁC
*Module thực nghiệm tương tác M06_js-dom-events — Trích xuất trọng tâm Chương 5 [S1]*

## 1. Trực Giác Cốt Lõi (Feynman Intuition)
- **Định nghĩa 1 câu kiểu Feynman:** Cây DOM (Document Object Model) giống như một cái cây gia phả bằng mã nguồn biến trang HTML thành các cành lá mà JavaScript có thể cầm nắm, tỉa tót hoặc gắn thêm lá mới; còn Sự Kiện (Event) giống như tiếng chuông cửa rung lên khi người dùng gõ phím hay bấm chuột.
- **Mục tiêu 80/20:** Làm chủ bộ 3 quyền lực: `document.querySelector()`, `element.addEventListener()`, và `element.classList.toggle()`; giải mã cơ chế lan truyền bọt khí (Event Bubbling) để áp dụng kỹ thuật Ủy nhiệm sự kiện (Event Delegation) đẳng cấp.

## 2. Các Luận Điểm Cốt Lõi (Synthesized Principles)
- **Truy Tìm Phần Tử (Selector APIs):**
  - Quên đi `document.getElementById` hay `getElementsByClassName` rườm rà.
  - Sử dụng thống nhất:
    - `document.querySelector('#submit-btn')`: Lấy phần tử đầu tiên khớp bộ chọn CSS.
    - `document.querySelectorAll('.todo-item')`: Lấy toàn bộ danh sách phần tử dạng `NodeList` (duyệt được bằng `.forEach()`).
- **Thay Đổi Giao Diện An Toàn:**
  - Thay vì can thiệp trực tiếp vào style: `el.style.color = 'red'` (gây bẩn code), hãy thay đổi qua Class:
    - `el.classList.add('active')`
    - `el.classList.remove('active')`
    - `el.classList.toggle('active')`
- **Cơ Chế Bọt Khí (Event Bubbling) & Ủy Nhiệm Sự Kiện (Event Delegation):**
  - Khi bạn bấm vào nút `<button>` bên trong một thẻ `<div>`, sự kiện `click` không chỉ kích hoạt trên nút bấm mà còn nổi bọt (bubble up) lên thẻ `<div>`, thẻ `<body>`, và lên tận đỉnh `window`.
  - *Kỹ thuật 80/20 Event Delegation:* Thay vì gắn 100 sự kiện click cho 100 dòng dữ liệu trong bảng (lãng phí RAM), chỉ cần gắn DUY NHẤT 1 sự kiện `click` lên thẻ cha (`<ul>` hoặc `<table>`), rồi dùng `event.target` để biết chính xác người dùng vừa bấm vào dòng nào!

## 3. Hướng Dẫn Thực Hành Phòng Web Lab
1. Mở tệp [`lab.html`](file:///d:/Downloads/AI%20Agent%20Kits/Agent%20Kits/Learning%20OS/learning-space/courses/web-design-fundamentals/modules/M06_js-dom-events/lab.html) trên trình duyệt.
2. Hoàn thành **Bước 1 (Dự đoán)** về cơ chế lan truyền sự kiện.
3. Thao tác trên cây DOM trực quan: Thêm phần tử mới vào danh sách, bấm vào các nút con và quan sát luồng nổi bọt (Bubbling Wave) đổi màu từ phần tử con lên phần tử cha.
4. Bật/tắt chế độ `event.stopPropagation()` để quan sát hiện tượng chặn nổi bọt.
5. Bấm nút **"Sao chép kết quả Lab Để Nộp Bài"** và dán khối mã `[LAB_RECEIPT]` vào khung chat.

## 4. Chuỗi Câu Hỏi Socratic 3 Tầng
1. **Tier 1 (Dự đoán tiền đề):** Bạn gắn sự kiện click cho thẻ cha `<ul>`. Sau đó dùng JavaScript thêm động một thẻ `<li>` mới vào danh sách. Khi người dùng click vào thẻ `<li>` mới này, hàm xử lý của thẻ cha `<ul>` có bắt được không? Tại sao?
2. **Tier 2 (Biên & Đột biến):** Nếu trong hàm xử lý sự kiện click của nút bấm con, lập trình viên gọi lệnh `event.stopPropagation();`, điều gì sẽ xảy ra với các hàm lắng nghe sự kiện trên thẻ cha? Khi nào thì việc này trở nên nguy hiểm đối với các hệ thống phân tích người dùng (Google Analytics)?
3. **Tier 3 (Chuyển giao xa):** Tại sao việc dùng thuộc tính `innerHTML = ...` để thêm phần tử động từ dữ liệu người dùng nhập vào lại là "tử huyệt" gây ra lỗ hổng bảo mật nghiêm trọng XSS (Cross-Site Scripting), và phương thức `document.createElement()` cùng `textContent` khắc phục điều đó như thế nào?

## 5. Tiêu Chí Đánh Giá (Embedded Rubric)
| Tiêu chí | Mức 0 (Chưa đạt) | Mức 1 (Đạt yêu cầu) | Mức 2 (Thành thạo) |
|---|---|---|---|
| **Thực nghiệm Web Lab** | Chưa mở lab hoặc không cung cấp được `[LAB_RECEIPT]` | Nộp receipt nhưng chưa thử nghiệm chế độ Event Delegation | Thao tác đầy đủ các trường hợp lan truyền sự kiện và giải thích được cơ chế `stopPropagation` |
| **Kỹ thuật Thao tác DOM** | Lạm dụng inline JS `onclick="..."` hoặc gán cứng `el.style` | Sử dụng chuẩn `querySelector` và quản lý giao diện qua `classList` | Thêm xóa Node an toàn bằng `createElement`/`appendChild`, ngăn chặn triệt để lỗ hổng XSS |
| **Tối ưu Sự kiện (Event Architecture)** | Gắn lặp lại listener vào từng phần tử con sinh động | Sử dụng được `event.target` để nhận diện phần tử tương tác | Triển khai xuất sắc mô hình Event Delegation cho danh sách động hàng nghìn phần tử |
