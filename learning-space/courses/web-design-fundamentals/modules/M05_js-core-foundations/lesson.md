---
visual: none
visual_reason: Khái niệm biến, cơ chế hoisting, Scope chuỗi phạm vi và phân biệt tham trị/tham chiếu trong JavaScript thiên về mô hình tư duy ô nhớ Stack/Heap, giải thích tối ưu bằng bảng so sánh trực diện và ví dụ mã nguồn
---

# BÀI HỌC TỔNG HỢP: JAVASCRIPT NỀN TẢNG — BIẾN, SCOPE, MẢNG & ĐỐI TƯỢNG
*Module M05_js-core-foundations — Trích xuất trọng tâm Chương 5 [S1]*

## 1. Trực Giác Cốt Lõi (Feynman Intuition)
- **Định nghĩa 1 câu kiểu Feynman:** Biến nguyên thủy (Number, String, Boolean) giống như một tờ tiền thật bạn cầm trên tay (sao chép là in ra tờ mới), còn Biến đối tượng (Object, Array) giống như chiếc chìa khóa nhà (sao chép chiếc chìa khóa thì cả hai người cùng mở chung một ngôi nhà).
- **Mục tiêu 80/20:** Xóa sổ thói quen dùng `var`; làm chủ `const` & `let` cùng phạm vi khối (Block Scope); nắm vững 3 hàm xử lý mảng thần thánh (`map`, `filter`, `forEach`) và cú pháp hàm mũi tên (`arrow function`).

## 2. Các Luận Điểm Cốt Lõi (Synthesized Principles)
- **Quy Tắc Khai Báo Biến Hiện Đại:**
  - `const`: Ưu tiên số 1 (dùng cho 90% biến). Biến không thể gán lại bằng dấu `=`, ngăn ngừa bug vô tình ghi đè.
  - `let`: Dùng cho biến cần thay đổi giá trị (biến đếm trong vòng lặp, trạng thái thay đổi).
  - `var`: **CẤM DÙNG** trong code mới vì có hiện tượng Hoisting kỳ quặc và phạm vi hàm (Function Scope) dễ gây rò rỉ dữ liệu.
- **Phân Biệt Tham Trị (Primitive) vs Tham Chiếu (Reference):**
  - *Primitive (Number, String, Boolean, null, undefined):* Lưu trực tiếp giá trị vào bộ nhớ Stack. Gán `a = b` là tạo bản sao độc lập hoàn toàn.
  - *Reference (Object, Array, Function):* Lưu địa chỉ ô nhớ trỏ tới vùng nhớ Heap. Khi `user2 = user1`, thay đổi thuộc tính trên `user2` sẽ làm thay đổi luôn cả `user1`!
- **Hàm Mũi Tên (Arrow Function) & Xử Lý Mảng Bất Biến (Immutable Array Methods):**
  - Cú pháp gọn gàng: `const square = x => x * x;`
  - `map()`: Biến đổi từng phần tử thành một mảng mới cùng độ dài (ví dụ: chuyển danh sách điểm số thành danh sách HTML).
  - `filter()`: Lọc ra các phần tử thỏa mãn điều kiện (ví dụ: lọc sinh viên có điểm $\ge 5$).
  - `forEach()`: Duyệt qua từng phần tử để thực hiện tác vụ phụ (Side Effect như render DOM).

## 3. Bẫy Trực Giác & So Sánh Đối Đầu
| Tình huống code | Khai báo `var` (Lỗi thời) | Khai báo `let` / `const` (Chuẩn ES6) |
|---|---|---|
| **Truy cập trước khi khai báo** | Trả về `undefined` (do Hoisting kéo lên đầu) | Ném lỗi `ReferenceError` (Temporal Dead Zone an toàn) |
| **Phạm vi trong khối lệnh `if/for`** | Rò rỉ ra ngoài hàm/toàn cục | Bị giam chặt trong cặp ngoặc nhọn `{ ... }` (Block Scope) |
| **Khai báo lại cùng tên biến** | Trình duyệt âm thầm chấp nhận, dễ đè mất biến cũ | Trình duyệt báo lỗi ngay lập tức `SyntaxError` |
| **Sửa đổi mảng khai báo bằng `const`** | N/A | **Hoàn toàn được phép** `arr.push(4)` vì địa chỉ ô nhớ không đổi; chỉ cấm `arr = [4]`! |

## 4. Chuỗi Câu Hỏi Socratic 3 Tầng
1. **Tier 1 (Dự đoán tiền đề):** Đoán kết quả in ra màn hình Console của đoạn code sau:
   ```javascript
   const fruits = ["Táo", "Cam"];
   fruits.push("Chuối");
   console.log(fruits.length);
   ```
   Code trên có bị lỗi vì gán vào biến `const` không? Tại sao?
2. **Tier 2 (Biên & Đột biến):** Cho đoạn mã sau:
   ```javascript
   let objA = { score: 10 };
   let objB = objA;
   objB.score = 20;
   console.log(objA.score);
   ```
   Giá trị của `objA.score` là 10 hay 20? Điều gì xảy ra dưới tầng ô nhớ RAM của máy tính?
3. **Tier 3 (Chuyển giao xa):** Tại sao trong lập trình giao diện hiện đại (React, Vue, hoặc quản lý State trong Web App), người ta luôn dùng `map()` hoặc `filter()` để tạo mảng mới thay vì sửa trực tiếp vào mảng cũ bằng `push()` hay `splice()`?

## 5. Tiêu Chí Đánh Giá (Embedded Rubric)
| Tiêu chí | Mức 0 (Chưa hiểu bản chất) | Mức 1 (Đạt yêu cầu) | Mức 2 (Thành thạo) |
|---|---|---|---|
| **Làm chủ Biến & Scope** | Vẫn quen tay dùng `var` hoặc không phân biệt được `const` với `let` | Sử dụng đúng `const` cho hằng và `let` cho biến lặp | Giải thích cặn kẽ cơ chế Block Scope và Temporal Dead Zone |
| **Tư duy Ô nhớ (Reference vs Value)** | Bối rối khi sửa object phụ làm thay đổi object gốc | Hiểu cơ chế tham chiếu của Object và biết dùng toán tử Spread `{ ...obj }` | Phân biệt được Shallow Copy (sao chép nông) và Deep Copy (sao chép sâu) |
| **Kỹ năng xử lý Mảng hàm** | Chỉ biết dùng vòng lặp `for (let i = 0...)` truyền thống | Dùng thành thạo `forEach`, `map`, `filter` kèm Arrow Function | Kết hợp chuỗi method (Chaining: `.filter().map()`) tạo luồng xử lý dữ liệu thanh lịch |
