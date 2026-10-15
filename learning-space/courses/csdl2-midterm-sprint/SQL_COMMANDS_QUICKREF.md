# CẨM NANG LỆNH SQL CẤP TỐC — ÔN THI GIỮA KÌ CSDL II

> Không văn vở, không lý thuyết suông. Chỉ có cú pháp chuẩn và ví dụ thực chiến của 3 bài tập Tuần 5, 6, 7.

---

## PHẦN 1: CÁC LỆNH TẠO BẢNG & KHÓA (TUẦN 5)

### 1. Tạo Database & Chọn làm việc

```sql
CREATE DATABASE TenDatabase;
GO
USE TenDatabase;
GO
```

### 2. Kiểu dữ liệu hay dùng nhất trong đề thi

- `CHAR(n)`: Chuỗi cố định độ dài (Mã SV, Mã ĐH, Mã SP: `CHAR(7)`, `CHAR(6)`).
- `VARCHAR(n)`: Chuỗi thay đổi độ dài, không dấu (Email, SĐT: `VARCHAR(11)`, `VARCHAR(50)`).
- `NVARCHAR(n)`: Chuỗi tiếng Việt có dấu (Họ tên, Địa chỉ: `NVARCHAR(50)`, `NVARCHAR(100)`).
- `INT`: Số nguyên (Số lượng: `QtyOnHand`, `QtyOrdered`).
- `MONEY`: Tiền tệ (Đơn giá, Lương: `UnitPrice`, `Salary`, `Amount`).
- `DATE`: Ngày tháng (Ngày sinh: `DoB`).
- `DATETIME`: Ngày giờ (Ngày đặt, ngày nhập: `OrderDate`, `RepDate`).
- `BIT`: Đúng/Sai (Giới tính: 1 là Nam, 0 là Nữ).

---

### 3. Tạo bảng độc lập (Chỉ có Khóa chính đơn)

*Dùng cho: `tblSupplier`, `tblProduct`, `tblCustomer`, `tblEmployee`*

```sql
CREATE TABLE tblSupplier
(
    SuppID      CHAR(6) NOT NULL PRIMARY KEY,  -- Khóa chính
    SuppName    NVARCHAR(50) NOT NULL,
    SuppAddress NVARCHAR(50) NULL DEFAULT N'Đà Nẵng',
    TelNo       VARCHAR(11) NULL UNIQUE        -- Không trùng
);
```

---

### 4. Tạo bảng có Khóa ngoại 1-N (Bảng con)

*Dùng cho: `tblReceiptNote` (nối Supplier), `tblOrderInvoice` (nối Customer, Employee)*

```sql
CREATE TABLE tblReceiptNote
(
    RepID         CHAR(7) NOT NULL PRIMARY KEY,
    RepDate       DATETIME NULL DEFAULT GETDATE(),
    SuppNo        CHAR(6) NOT NULL,
    -- Cú pháp khóa ngoại:
    FOREIGN KEY (SuppNo) REFERENCES tblSupplier(SuppID)
);
```

---

### 5. Tạo bảng có Khóa chính phức hợp (Composite Key)

*Dùng cho: `tblReceiptNoteDetail`, `tblOrderInvoiceDetail`*

```sql
CREATE TABLE tblReceiptNoteDetail
(
    RepID         CHAR(7) NOT NULL,
    ProductID     CHAR(7) NOT NULL,
    QtyReceipted  INT NOT NULL,
    RepPrice      MONEY NOT NULL,
    -- Khóa chính gồm 2 cột gộp lại:
    PRIMARY KEY (RepID, ProductID),
    -- Khai báo 2 khóa ngoại:
    FOREIGN KEY (RepID) REFERENCES tblReceiptNote(RepID),
    FOREIGN KEY (ProductID) REFERENCES tblProduct(ProductID)
);
```

---

## PHẦN 2: LỆNH ALTER TABLE & TẤT CẢ RÀNG BUỘC (TUẦN 6)

### 1. Thêm cột mới

```sql
ALTER TABLE tblOrderInvoice ADD OrdInvStatus NVARCHAR(50) NULL;
```

### 2. Xóa cột

```sql
ALTER TABLE tblCustomer DROP COLUMN CustAddress;
```

### 3. Sửa kiểu dữ liệu cột

```sql
ALTER TABLE tblEmployee ALTER COLUMN Salary MONEY NOT NULL;
```

---

### 4. Thêm Constraint: CHECK (Kiểm tra điều kiện)

- **Kiểm tra giá trị nằm trong danh sách (`IN`):**

```sql
-- Trạng thái đơn hàng
ALTER TABLE tblOrderInvoice 
ADD CONSTRAINT CK_OrdInvStatus 
CHECK (OrdInvStatus IN (N'Chờ duyệt', N'Đã duyệt – Đang đóng gói', N'Đang giao', N'Đã giao'));

-- Giới tính
ALTER TABLE tblEmployee 
ADD CONSTRAINT CK_Gender 
CHECK (Gender IN ('F', 'M'));
```

- **Kiểm tra số lớn hơn hoặc bằng 0:**

```sql
ALTER TABLE tblProduct 
ADD CONSTRAINT CK_UnitPrice 
CHECK (UnitPrice >= 0);
```

- **Kiểm tra độ tuổi đủ 18 (`DATEDIFF`):**

```sql
ALTER TABLE tblEmployee 
ADD CONSTRAINT CK_DoB_18 
CHECK (DATEDIFF(year, DoB, GETDATE()) >= 18);
```

- **Kiểm tra thứ tự thời gian:**

```sql
ALTER TABLE tblOrderInvoice 
ADD CONSTRAINT CK_Order_Dates 
CHECK (OrderDate < GETDATE() AND InvDate > OrderDate AND DelDate > InvDate);
```

- **Kiểm tra định dạng Email (LIKE):**

```sql
ALTER TABLE tblCustomer 
ADD CONSTRAINT CK_Email_Format 
CHECK (
    (Email LIKE '[a-zA-Z]%@gmail.com') OR 
    (Email LIKE '[a-zA-Z]%@yahoo.com') OR 
    (Email LIKE '[a-zA-Z]%@ute.udn.vn')
);
```

- **Kiểm tra số điện thoại (10 hoặc 11 chữ số):**

```sql
ALTER TABLE tblCustomer 
ADD CONSTRAINT CK_TelNo 
CHECK (
    TelNo LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' OR 
    TelNo LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
);
```

---

### 5. Thêm Constraint: DEFAULT (Giá trị mặc định)

```sql
-- Cú pháp: DEFAULT <GiaTri> FOR <TenCot>
ALTER TABLE tblEmployee 
ADD CONSTRAINT DF_Gender DEFAULT 'F' FOR Gender;

ALTER TABLE tblCustomer 
ADD CONSTRAINT DF_CustAddress DEFAULT N'Đà Nẵng' FOR Address;
```

---

### 6. Thêm Constraint: UNIQUE (Duy nhất không trùng)

```sql
ALTER TABLE tblCustomer 
ADD CONSTRAINT UQ_Customer_Email UNIQUE (Email);

ALTER TABLE tblCustomer 
ADD CONSTRAINT UQ_Customer_TelNo UNIQUE (TelNo);
```

---

### 7. Thêm Khóa ngoại kèm xóa tự động (`ON DELETE CASCADE`)

```sql
ALTER TABLE tblOrderInvoiceDetail
ADD CONSTRAINT FK_OID_Order 
FOREIGN KEY (OrderID) REFERENCES tblOrderInvoice(OrderID)
ON DELETE CASCADE
ON UPDATE CASCADE;
```

---

## PHẦN 3: LỆNH NHẬP LIỆU DML (TUẦN 7)

### 1. Lệnh chỉnh định dạng ngày (Bắt buộc chạy trước khi Insert)

```sql
SET DATEFORMAT dmy; -- Ngày trước, Tháng sau, Năm cuối (Ví dụ: '25/12/2026')
```

### 2. Chèn 1 dòng

```sql
INSERT INTO tblProduct (ProductID, ProductName, UnitPrice, QtyOnHand, RecorderLevel)
VALUES ('SP001', N'Chuột không dây', 250000, 50, 10);
```

### 3. Chèn nhiều dòng cùng lúc (Nhanh, không lặp lại từ khóa)

```sql
INSERT INTO tblSupplier (SuppID, SuppName, SuppAddress, TelNo, ContactPerson)
VALUES 
    ('NCC01', N'Công ty Phong Vũ', N'Đà Nẵng', '0905111222', N'Nguyễn Văn A'),
    ('NCC02', N'FPT Shop', N'TP Hồ Chí Minh', '0905333444', N'Trần Thị B');
```

---

## NGUYÊN TẮC THỨ TỰ SỐNG CÒN KHI LÀM BÀI

1. **Khi TẠO BẢNG:** Tạo bảng không có khóa ngoại trước -> Bảng có khóa ngoại sau cùng.
2. **Khi NHẬP LIỆU:** Nhập bảng cha trước -> Nhập bảng con sau.
3. **Khi XÓA (DROP):** Xóa bảng con trước -> Xóa bảng cha sau.
