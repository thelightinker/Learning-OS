---
visual: lab
visual_reason: Bố cục Flexbox và Grid có tính chất phân bổ không gian và hành vi co giãn (flex-grow, flex-shrink, wrap) phi tuyến tính, bắt buộc người học phải thao tác trực tiếp trên Web Lab để cảm nhận trực quan
---

# BÀI HỌC THỰC NGHIỆM: BỐ CỤC HIỆN ĐẠI FLEXBOX & CSS GRID
*Module thực nghiệm tương tác M03_css-flexbox-grid — Trích xuất trọng tâm Chương 4 [S1]*

## 1. Trực Giác Cốt Lõi (Feynman Intuition)
- **Định nghĩa 1 câu kiểu Feynman:** Flexbox giống như xếp hành lý vào cốp xe theo một hàng dọc hoặc ngang (1 chiều - One Dimensional), còn CSS Grid giống như sắp xếp bàn cờ vua với cả hàng ngang và cột dọc cùng lúc (2 chiều - Two Dimensional).
- **Mục tiêu 80/20:** Xóa sổ vĩnh viễn việc dùng `float` và `clear` cổ lỗ sĩ; làm chủ 3 trục căn chỉnh kinh điển: `justify-content` (trục chính - main axis), `align-items` (trục phụ - cross axis), và thuộc tính `gap`.

## 2. Các Luận Điểm Cốt Lõi (Synthesized Principles)
- **Hệ Thống Trục của Flexbox:**
  - `flex-direction: row` (mặc định): Trục chính nằm ngang (trái sang phải), trục phụ thẳng đứng (trên xuống dưới).
  - `justify-content`: Điều phối khoảng trống trên trục chính (`flex-start`, `center`, `flex-end`, `space-between`, `space-around`, `space-evenly`).
  - `align-items`: Căn chỉnh các phần tử trên trục phụ (`stretch`, `center`, `flex-start`, `flex-end`).
  - Kỹ thuật "Centering Thần Thánh" (Căn giữa hoàn hảo cả ngang lẫn dọc):
    ```css
    .parent {
      display: flex;
      justify-content: center;
      align-items: center;
    }
    ```
- **Sức Mạnh của CSS Grid:**
  - Định nghĩa lưới 2 chiều: `grid-template-columns: repeat(3, 1fr)` (chia đều 3 cột bằng nhau) kèm `gap: 20px`.
  - Phép màu Responsive tự động co giãn không cần media query:
    ```css
    .responsive-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
    }
    ```

## 3. Hướng Dẫn Thực Hành Phòng Web Lab
1. Mở tệp [`lab.html`](file:///d:/Downloads/AI%20Agent%20Kits/Agent%20Kits/Learning%20OS/learning-space/courses/web-design-fundamentals/modules/M03_css-flexbox-grid/lab.html) bằng bất kỳ trình duyệt nào.
2. Hoàn thành **Bước 1 (Dự đoán)** để mở khóa bộ công cụ điều phối không gian.
3. Chuyển đổi qua lại giữa 2 chế độ **Flexbox** và **Grid**, tinh chỉnh `justify-content`, `align-items`, và `gap`.
4. Quan sát điểm gãy (tipping point) khi thu nhỏ màn hình hoặc bật `flex-wrap: wrap`.
5. Bấm nút **"Sao chép kết quả Lab Để Nộp Bài"** và dán khối mã `[LAB_RECEIPT]` vào khung chat.

## 4. Chuỗi Câu Hỏi Socratic 3 Tầng
1. **Tier 1 (Dự đoán tiền đề):** Nếu một container có `display: flex; flex-direction: column;`, thuộc tính `justify-content: center;` sẽ căn giữa các phần tử theo chiều ngang hay chiều dọc?
2. **Tier 2 (Biên & Đột biến):** Khi có 5 khối con nằm trong một Flex container chiều rộng 500px, mỗi khối có `width: 150px` nhưng `flex-wrap: nowrap`. Chuyện gì sẽ xảy ra với kích thước thực tế của 5 khối đó? Thuộc tính nào quyết định tỷ lệ co lại của chúng?
3. **Tier 3 (Chuyển giao xa):** Khi xây dựng giao diện thanh điều hướng Navbar (Logo bên trái, Menu ở giữa, Avatar người dùng bên phải), bạn sẽ chọn Flexbox hay Grid? Hãy đề xuất giải pháp tối giản nhất chỉ bằng 1 dòng CSS trên phần tử con.

## 5. Tiêu Chí Đánh Giá (Embedded Rubric)
| Tiêu chí | Mức 0 (Chưa đạt) | Mức 1 (Đạt yêu cầu) | Mức 2 (Thành thạo) |
|---|---|---|---|
| **Thực nghiệm Web Lab** | Chưa mở lab hoặc không cung cấp được `[LAB_RECEIPT]` | Nộp receipt hợp lệ nhưng chỉ thử nghiệm 1 chế độ bố cục | Thực hiện tối thiểu 3 lần thay đổi tham số, khám phá hành vi của `flex-wrap` và `grid minmax` |
| **Phân biệt Flexbox & Grid** | Nhầm lẫn trục chính main-axis khi đổi sang `flex-direction: column` | Căn chỉnh chính xác các trục trong Flexbox và chia cột trong Grid | Chỉ ra đúng bài toán nên dùng Flexbox (1D UI bar) và bài toán nên dùng Grid (2D Dashboard) |
| **Tư duy Responsive tự động** | Dùng float/absolute cứng nhắc khiến giao diện vỡ trên di động | Dùng Flexbox có `flex-wrap: wrap` để xuống dòng tự nhiên | Thành thạo công thức `repeat(auto-fit, minmax(...))` tạo layout đáp ứng không cần Media Query |
