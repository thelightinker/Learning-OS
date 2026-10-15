 

# BÀI 1: TẠO BẢNG ĐƠN GIẢN & KHÓA CHÍNH (PRIMARY KEY)

## 1. Giải Thích Ngắn Gọn

- **Bảng (Table)**: Nơi chứa dữ liệu gồm các Cột (Column) và Dòng (Row).
- **Cú pháp cốt lõi**:
  ```sql
  CREATE TABLE TênBảng (
      TênCột KiểuDữLiệu RàngBuộc
  );
  ```
- **Khóa chính (`PRIMARY KEY`)**: Cột định danh duy nhất mỗi dòng — **không được trùng**, **không được rỗng** (`NOT NULL`).
- **Kiểu dữ liệu hay dùng trong đề thi**:
  - `CHAR(n)`: Chuỗi cố định $n$ ký tự (mã SV, mã SP, mã NCC).
  - `VARCHAR(n)`: Chuỗi ký tự không dấu (SĐT `VARCHAR(11)`, Email).
  - `NVARCHAR(n)`: Chuỗi tiếng Việt có dấu (Tên người, Địa chỉ).
  - `INT`: Số lượng nguyên.
  - `MONEY`: Tiền tệ.

---

## 2. Ví Dụ Code Thật & Kết Quả Trực Quan

```sql
USE tempdb;
GO

-- Xóa bảng cũ nếu đã tồn tại trước đó để chạy lại không bị lỗi
DROP TABLE IF EXISTS tblDonVi;

-- Tạo bảng Đơn vị tính
CREATE TABLE tblDonVi
(
    MaDV   CHAR(4) NOT NULL PRIMARY KEY,   -- Khóa chính mã 4 ký tự (vd: 'DV01')
    TenDV  NVARCHAR(30) NOT NULL           -- Tên tiếng Việt (vd: N'Hộp', N'Thùng')
);
GO
```

### Kết quả bảng sinh ra trong CSDL:

| MaDV (PK) | TenDV  | Ghi chú trực quan                                                            |
| :-------- | :----- | :----------------------------------------------------------------------------- |
| `DV01`  | Hộp   | Hợp lệ                                                                       |
| `DV02`  | Thùng | Hợp lệ                                                                       |
| `DV01`  | Bao    | ❌ **Lỗi ngay!** Vi phạm khóa chính vì trùng mã `DV01` đã có |

---

## 3. Bài Tập Thực Hành (Sếp code trực tiếp vào các Code Block bên dưới)

### Nhiệm Vụ 1: Tạo bảng Nhà cung cấp (`tblSupplier`)

**Yêu cầu các cột:**

- `SuppID`: Mã nhà cung cấp, `CHAR(6)`, không rỗng, là khóa chính (`PRIMARY KEY`).
- `SuppName`: Tên nhà cung cấp, `NVARCHAR(50)`, không được để trống (`NOT NULL`).
- `SuppAddress`: Địa chỉ, `NVARCHAR(50)`, cho phép để trống (`NULL`).
- `TelNo`: Số điện thoại, `VARCHAR(11)`, cho phép để trống (`NULL`).

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 1 VÀO ĐÂY:
create table TBLSUPLIER
(
  suppid char(6) NOT NULL primary key,
  suppname NVARCHAR(50) not null,
  suppaddress nvarchar(50),
  telno varchar(11)
)
```

---

### Nhiệm Vụ 2: Tạo bảng Sản phẩm (`tblProduct`)

**Yêu cầu các cột:**

- `ProductID`: Mã sản phẩm, `CHAR(7)`, không rỗng, là khóa chính (`PRIMARY KEY`).
- `ProductName`: Tên sản phẩm, `NVARCHAR(50)`, không được để trống (`NOT NULL`).
- `UnitPrice`: Đơn giá bán, kiểu `MONEY`, không được để trống (`NOT NULL`).
- `QtyOnHand`: Số lượng tồn kho, kiểu `INT`, không được để trống (`NOT NULL`).

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 2 VÀO ĐÂY:
create table tblProduct
(
  	productid char(7) not null primary key,
	productname nvarchar(50) not null,
  	Unitprice money Not null,
  	qtyonhand int not null
)
```

---

---

# BÀI 2: KHÓA NGOẠI (FOREIGN KEY) — LIÊN KẾT BẢNG 1 - N

## 1. Giải Thích Ngắn Gọn

- **Khóa ngoại (`FOREIGN KEY`)**: Cột ở bảng con dùng để "bắt tay" tham chiếu đến Khóa chính của bảng cha.
- **Quy tắc vàng 1:** Cột khóa ngoại ở bảng con bắt buộc phải **cùng kiểu dữ liệu** với khóa chính ở bảng cha (ví dụ cha là `CHAR(6)` thì con cũng phải `CHAR(6)`).
- **Quy tắc vàng 2:** Bảng cha phải được `CREATE` trước thì bảng con mới có cái để `REFERENCES`.
- **Cú pháp ngắn gọn nhất (Inline)**:
  ```sql
  TênCột KiểuDữLiệu FOREIGN KEY REFERENCES BảngCha(CộtKhóaChính)
  ```

---

## 2. Ví Dụ Code Thật & Kết Quả Trực Quan

```sql
USE tempdb;
GO

-- 1. Bảng cha (Đơn vị tính) tạo trước
DROP TABLE IF EXISTS tblHangHoa;
DROP TABLE IF EXISTS tblDonVi;

CREATE TABLE tblDonVi (
    MaDV   CHAR(4) NOT NULL PRIMARY KEY,
    TenDV  NVARCHAR(30) NOT NULL
);

-- 2. Bảng con (Hàng hóa) có khóa ngoại tham chiếu về tblDonVi
CREATE TABLE tblHangHoa (
    MaHang CHAR(5) NOT NULL PRIMARY KEY,
    TenHang NVARCHAR(50) NOT NULL,
    MaDV   CHAR(4) NOT NULL FOREIGN KEY REFERENCES tblDonVi(MaDV)
);
GO
```

### Kết quả trực quan khi chèn dữ liệu:

Giả sử bảng cha `tblDonVi` chỉ có mã `'DV01'` (Hộp) và `'DV02'` (Thùng):

| MaHang (PK) | TenHang      | MaDV (FK) | Trạng thái SQL Server                                                                                |
| :---------- | :----------- | :-------- | :----------------------------------------------------------------------------------------------------- |
| `H001`    | Sữa chua    | `DV01`  | ✅ **Thành công** (vì `DV01` có tồn tại ở bảng cha)                                    |
| `H002`    | Nước ngọt | `DV99`  | ❌ **Lỗi ngay!** (`FOREIGN KEY constraint conflict`: Không tìm thấy `DV99` ở bảng cha) |

---

## 3. Bài Tập Thực Hành (Sếp gõ code vào Code Block bên dưới)

### Nhiệm Vụ 3: Tạo bảng Phiếu Nhập Hàng (`tblReceiptNote`)

Bảng này liên kết với bảng `tblSupplier` (ở Nhiệm vụ 1) qua cột mã nhà cung cấp `SuppNo`.

**Yêu cầu các cột:**

- `RepID`: Mã phiếu nhập, `CHAR(7)`, không rỗng, là khóa chính (`PRIMARY KEY`).
- `RepDate`: Ngày nhập hàng, kiểu `DATETIME`, cho phép `NULL`.
- `RepTotalMoney`: Tổng tiền phiếu nhập, kiểu `MONEY`, cho phép `NULL`.
- `SuppNo`: Mã nhà cung cấp, kiểu `CHAR(6)` không rỗng, là khóa ngoại tham chiếu đến cột `SuppID` của bảng `tblSupplier`.

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 3 VÀO ĐÂY:
CREATE TABLE tblReceiptNote
(
  repid char(7) not null primary key,
  repdate datetime,
  reptotalmoney money,
  suppno char(6) not null foreign key references tblSupplier(SuppID)
)
```

---

---

# BÀI 3: KHÓA CHÍNH PHỨC HỢP (COMPOSITE PRIMARY KEY) & BẢNG CHI TIẾT

## 1. Giải Thích Ngắn Gọn

- **Bảng chi tiết (Cầu nối)**: Dùng khi 1 phiếu nhập/hóa đơn có nhiều sản phẩm, và 1 sản phẩm có mặt ở nhiều phiếu.
- **Khóa chính phức hợp (`COMPOSITE PK`)**: Kết hợp 2 cột (ví dụ `MãPhiếu` + `MãSP`) làm khóa chính, đảm bảo **cặp đôi này không bao giờ bị lặp lại**.
- **Cú pháp bắt buộc**: Khai báo `PRIMARY KEY` ở dòng cuối cùng của bảng:
  ```sql
  PRIMARY KEY (Cột1, Cột2)
  ```

---

## 2. Ví Dụ Code Thật & Kết Quả Trực Quan

```sql
USE tempdb;
GO

-- Bảng chi tiết phân công: 1 nhân viên làm nhiều dự án
CREATE TABLE tblPhanCong (
    MaNV   CHAR(5) NOT NULL FOREIGN KEY REFERENCES tblNhanVien(MaNV),
    MaDA   CHAR(5) NOT NULL FOREIGN KEY REFERENCES tblDuAn(MaDA),
    SoGio  INT NOT NULL,

    -- Khai báo khóa chính phức hợp gồm cả 2 cột
    PRIMARY KEY (MaNV, MaDA)
);
GO
```

### Kết quả trực quan khi chèn dữ liệu:

| MaNV (FK1) | MaDA (FK2) | SoGio | Trạng thái SQL Server                                                                   |
| :--------- | :--------- | :---- | :---------------------------------------------------------------------------------------- |
| `NV01`   | `DA01`   | 10    | ✅ Hợp lệ                                                                               |
| `NV01`   | `DA02`   | 15    | ✅ Hợp lệ (cùng nhân viên, khác dự án)                                            |
| `NV02`   | `DA01`   | 20    | ✅ Hợp lệ (khác nhân viên, cùng dự án)                                            |
| `NV01`   | `DA01`   | 30    | ❌ **Lỗi ngay!** Vi phạm PK vì cặp (`NV01`, `DA01`) đã được nhập rồi |

---

## 3. Bài Tập Thực Hành (Sếp gõ code vào Code Block bên dưới)

### Nhiệm Vụ 4: Tạo bảng Chi tiết phiếu nhập (`tblReceiptNoteDetail`)

Bảng này làm cầu nối giữa `tblReceiptNote` (Bài 2) và `tblProduct` (Bài 1).

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 4 VÀO ĐÂY:
CREATE TABLE tblReceiptNoteDetail
(
    -- Các cột dữ liệu thông thường
    RepID        CHAR(7) NOT NULL,
    ProductID    CHAR(7) NOT NULL,
    QtyReceipted INT NOT NULL,
    RepPrice     MONEY NOT NULL,

    -- 1. Khóa chính phức hợp (cần có dấu phẩy ngăn cách):
    PRIMARY KEY (RepID, ProductID),

    -- 2. Khóa ngoại RepID (cú pháp: FOREIGN KEY (Cột) REFERENCES Bảng(Cột)):
    FOREIGN KEY (RepID) REFERENCES tblReceiptNote(RepID),

    -- 3. Khóa ngoại ProductID:
    FOREIGN KEY (ProductID) REFERENCES tblProduct(ProductID)
);
```

---

---

# LỚP 2: RÀNG BUỘC TOÀN VẸN VỚI LỆNH ALTER TABLE (TRỌNG TÂM TUẦN 6)

# BÀI 4: RÀNG BUỘC KIỂM TRA (CHECK) & GIÁ TRỊ MẶC ĐỊNH (DEFAULT)

## 1. Giải Thích Ngắn Gọn

- Đề thi Tuần 6 yêu cầu: **Bảng đã có sẵn, dùng lệnh `ALTER TABLE` để gắn thêm luật (ràng buộc)**.
- **Ràng buộc `DEFAULT`**: Tự động điền giá trị nếu bỏ trống:
  ```sql
  ALTER TABLE TênBảng ADD CONSTRAINT TênRàngBuộc DEFAULT GiáTrị FOR TênCột;
  ```
- **Ràng buộc `CHECK`**: Bắt buộc dữ liệu phải thỏa mãn điều kiện (như Lương $\ge 0$, Tuổi $\ge 18$):
  ```sql
  ALTER TABLE TênBảng ADD CONSTRAINT TênRàngBuộc CHECK (BiểuThứcĐiềuKiện);
  ```

---

## 2. Ví Dụ Code Thật

```sql
USE tempdb;
GO

-- 1. Đặt mặc định Giới tính (GioiTinh) của bảng tblNhanVien là 'F' (Nữ)
ALTER TABLE tblNhanVien 
ADD CONSTRAINT DF_NhanVien_GioiTinh DEFAULT 'F' FOR GioiTinh;

-- 2. Bắt buộc Lương (Luong) của nhân viên phải >= 0
ALTER TABLE tblNhanVien 
ADD CONSTRAINT CK_NhanVien_Luong CHECK (Luong >= 0);
GO
```

### Kết quả trực quan khi chèn dữ liệu:

| Lệnh nhập                    | Dữ liệu thực tế lưu vào bảng        | Trạng thái                                             |
| :----------------------------- | :----------------------------------------- | :------------------------------------------------------- |
| Không nhập cột `GioiTinh` | Cột `GioiTinh` tự nhảy thành `'F'` | ✅ Thành công (nhờ DEFAULT)                           |
| Nhập `Luong = -5000`        | Bị chặn đứng ngay                      | ❌ **Lỗi ngay!** (`CHECK constraint violation`) |

---

## 3. Bài Tập Thực Hành (Sếp gõ code vào Code Block bên dưới)

### Nhiệm Vụ 5: Thêm Ràng Buộc Cho Bảng Khách Hàng (`tblKhachHang`)

1. Thêm ràng buộc `DEFAULT` đặt tên là `DF_KhachHang_DiaChi`: Mặc định địa chỉ là `N'Đà Nẵng'` cho cột `DiaChi`.
2. Thêm ràng buộc `CHECK` đặt tên là `CK_KhachHang_SoDu`: Bắt buộc số dư tài khoản `SoDu >= 0`.

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 5 VÀO ĐÂY:
-- 1. Thêm ràng buộc DEFAULT cho DiaChi:
ALTER TABLE tblKhachHang
ADD CONSTRAINT DF_KhachHang_DiaChi DEFAULT N'Đà Nẵng' FOR DiaChi;

-- 2. Thêm ràng buộc CHECK cho SoDu:
ALTER TABLE tblKhachHang
ADD CONSTRAINT CK_KhachHang_SoDu CHECK (SoDu >= 0);
```

---

---

# BÀI 5: RÀNG BUỘC CHECK NÂNG CAO (HÀM NGÀY & DANH SÁCH GIÁ TRỊ)

## 1. Giải Thích Ngắn Gọn

- **Kiểm tra tuổi $\ge 18$**: Dùng hàm `DATEDIFF(year, CộtNgàySinh, GETDATE()) >= 18` (Tính khoảng cách số năm từ ngày sinh đến ngày hiện tại `GETDATE()`).
- **Giới hạn giá trị trong danh sách**: Dùng từ khóa `IN (GiáTrị1, GiáTrị2, ...)` thay vì viết nhiều lệnh `OR`.
- **Cú pháp**: Luôn bọc điều kiện trong cặp ngoặc tròn: `CHECK (ĐiềuKiện)`.

---

## 2. Ví Dụ Code Thật (Tiếng Việt Viết Tắt)

```sql
USE tempdb;
GO

-- 1. Bắt buộc nhân viên phải đủ 18 tuổi trở lên
ALTER TABLE tblNhanVien 
ADD CONSTRAINT CK_NhanVien_Tuoi 
CHECK (DATEDIFF(year, NgaySinh, GETDATE()) >= 18);

-- 2. Giới tính chỉ nhận 'F' hoặc 'M'
ALTER TABLE tblNhanVien 
ADD CONSTRAINT CK_NhanVien_GioiTinh 
CHECK (GioiTinh IN ('F', 'M'));
GO
```

### Kết quả trực quan khi chèn dữ liệu:

| Lệnh nhập                 | Dữ liệu kiểm tra                 | Trạng thái                                             |
| :-------------------------- | :---------------------------------- | :------------------------------------------------------- |
| `NgaySinh = '2000-01-01'` | 2026 - 2000 = 26 tuổi ($\ge 18$) | ✅ Thành công                                          |
| `NgaySinh = '2015-05-10'` | 2026 - 2015 = 11 tuổi ($< 18$)   | ❌ **Lỗi ngay!** (`CHECK constraint violation`) |
| `GioiTinh = 'X'`          | Không nằm trong `('F', 'M')`    | ❌ **Lỗi ngay!**                                  |

---

## 3. Bài Tập Thực Hành (Sếp gõ code vào Code Block bên dưới)

### Nhiệm Vụ 6: Thêm Ràng Buộc Kiểm Tra (Tuần 6)

Cho bảng Đơn hàng `tblDonHang` gồm các cột `NgayDat`, `TrangThai`:

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 6 VÀO ĐÂY:
-- 1. Bắt buộc cột TrangThai (viết liền) chỉ nhận 1 trong 3 giá trị:
ALTER TABLE tblDonHang
ADD CONSTRAINT CK_DonHang_TrangThai 
CHECK (TrangThai IN (N'Chờ duyệt', N'Đang giao', N'Đã giao'));

-- 2. So sánh ngày đặt NgayDat phải nhỏ hơn hoặc bằng ngày hiện tại:
ALTER TABLE tblDonHang
ADD CONSTRAINT CK_DonHang_NgayDat
CHECK (NgayDat <= GETDATE());
```

---

---

# BÀI 6: KHÓA NGOẠI PHỤ THUỘC (ON DELETE CASCADE / SET NULL)

## 1. Giải Thích Ngắn Gọn (Câu Hỏi Điểm 8 Tuần 6)

- Khi xóa 1 dòng ở bảng Cha, các dòng liên quan ở bảng Con sẽ xử lý thế nào?
- **`ON DELETE CASCADE`**: Cha bị xóa $\rightarrow$ Các dòng con liên quan **tự động bị xóa sạch theo**.
- **`ON DELETE SET NULL`**: Cha bị xóa $\rightarrow$ Cột khóa ngoại ở bảng con **tự gán thành `NULL`**.
- **`ON DELETE NO ACTION`** *(Mặc định)*: Chặn đứng không cho xóa cha nếu vẫn còn dữ liệu con.
- **Cú pháp thêm khóa ngoại bằng `ALTER TABLE`**:
  ```sql
  ALTER TABLE BảngCon
  ADD CONSTRAINT TênKhóaNgoại
  FOREIGN KEY (CộtBảngCon) REFERENCES BảngCha(CộtBảngCha)
  ON DELETE CASCADE ON UPDATE CASCADE;
  ```

---

## 2. Ví Dụ Code Thật (Tiếng Việt Viết Tắt)

```sql
USE tempdb;
GO

-- Thêm khóa ngoại từ tblDonHang tham chiếu tblKhachHang (Xóa khách thì xóa luôn đơn hàng)
ALTER TABLE tblDonHang
ADD CONSTRAINT FK_DonHang_KhachHang
FOREIGN KEY (MaKH) REFERENCES tblKhachHang(MaKH)
ON DELETE CASCADE
ON UPDATE CASCADE;
GO
```

### Kết quả trực quan khi xóa dữ liệu bảng cha:

| Thao tác trên bảng cha `tblKhachHang`       | Dữ liệu bảng con `tblDonHang`                           | Giải thích                      |
| :----------------------------------------------- | :----------------------------------------------------------- | :-------------------------------- |
| `DELETE FROM tblKhachHang WHERE MaKH = 'KH01'` | Toàn bộ đơn hàng của `'KH01'` tự động biến mất! | ✅ Nhờ có `ON DELETE CASCADE` |

---

## 3. Bài Tập Thực Hành (Sếp gõ code vào Code Block bên dưới)

### Nhiệm Vụ 7: Thêm Khóa Ngoại Cho Bảng Chi Tiết Đơn Hàng (`tblChiTietDonHang`)

Thêm khóa ngoại cho cột `MaDH` của bảng `tblChiTietDonHang` tham chiếu đến cột `MaDH` của bảng `tblDonHang` với hiệu ứng `ON DELETE CASCADE` và `ON UPDATE CASCADE`.

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 7 VÀO ĐÂY:
-- (Đã dọn sẵn khung, sếp chỉ cần điền 2 dòng cuối):
ALTER TABLE tblChiTietDonHang
ADD CONSTRAINT FK_ChiTietDonHang_DonHang
FOREIGN KEY (MaDH) REFERENCES tblDonHang(MaDH)
ON DELETE CASCADE
ON UPDATE CASCADE;
```

---

---

# LỚP 3: THAO TÁC DỮ LIỆU DML & NHẬP RECORD (TRỌNG TÂM TUẦN 7)

# BÀI 7: LỆNH SET DATEFORMAT & CHÈN DỮ LIỆU ĐA DÒNG (INSERT INTO)

## 1. Giải Thích Ngắn Gọn (Kỹ Năng Sống Còn Tuần 7)

- **`SET DATEFORMAT dmy;`**: Lệnh bắt buộc phải chạy trước khi nhập ngày tháng ở Việt Nam để máy hiểu ngày nhập là `Ngày/Tháng/Năm` (thay vì mặc định của Mỹ là `Tháng/Ngày/Năm`). Không có lệnh này khi nhập ngày `25/12/2026` sẽ bị lỗi tràn ngày `Out of range`!
- **Thứ tự chèn bảng (Quy tắc không bị lỗi FK)**:
  1. Chèn bảng Cha trước: `tblKhachHang`, `tblNhanVien`, `tblSanPham`.
  2. Chèn bảng Con: `tblDonHang` (vì cần `MaKH` và `MaNV` có sẵn).
  3. Chèn bảng Chi Tiết cuối cùng: `tblChiTietDonHang` (vì cần `MaDH` và `MaSP` có sẵn).
- **Cú pháp chèn nhiều dòng (Multi-row INSERT)**:
  ```sql
  INSERT INTO TênBảng (Cột1, Cột2, ...)
  VALUES 
      (Dòng1_GiaTri1, Dòng1_GiaTri2, ...),
      (Dòng2_GiaTri1, Dòng2_GiaTri2, ...);
  ```

---

## 2. Ví Dụ Code Thật (Tiếng Việt Viết Tắt)

```sql
USE tempdb;
GO

-- 1. Bật định dạng Ngày-Tháng-Năm
SET DATEFORMAT dmy;
GO

-- 2. Chèn 2 khách hàng mẫu vào tblKhachHang
INSERT INTO tblKhachHang (MaKH, TenKH, DiaChi, SoDu)
VALUES 
    ('KH01', N'Nguyễn Văn An', N'Đà Nẵng', 1500000),
    ('KH02', N'Trần Thị Bình', N'Quảng Nam', 500000);
GO
```

### Kết quả bảng sinh ra trong CSDL:

| MaKH     | TenKH            | DiaChi     | SoDu       |
| :------- | :--------------- | :--------- | :--------- |
| `KH01` | Nguyễn Văn An  | Đà Nẵng | 1500000.00 |
| `KH02` | Trần Thị Bình | Quảng Nam | 500000.00  |

---

## 3. Bài Tập Thực Hành (Sếp gõ code vào Code Block bên dưới)

### Nhiệm Vụ 8: Nhập 3 Sản Phẩm Vào Bảng `tblSanPham`

Bảng `tblSanPham` gồm 4 cột: `MaSP`, `TenSP`, `DonGia`, `SoLuong`.

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 8 VÀO ĐÂY:
INSERT INTO tblSanPham (MaSP, TenSP, DonGia, SoLuong)
VALUES 
    ('SP01', N'Bàn phím cơ', 850000, 20),
    ('SP02', N'Chuột không dây', 350000, 50),
    ('SP03', N'Tai nghe Gaming', 600000, 15);
GO
```

---

---

# BÀI 8: CHÈN BẢNG CON (CÓ KHÓA NGOẠI) & BÀI TOÁN ĐỘ PHỦ (TUẦN 7)

## 1. Giải Thích Ngắn Gọn (Trọng Tâm Bài Tuần 7)

- **Quy tắc khóa ngoại khi INSERT**: Cột `MaKH` và `MaNV` ở bảng `tblDonHang` **bắt buộc phải lấy từ các mã đã có sẵn ở bảng cha** (`'KH01'`, `'KH02'`). Nếu nhập bừa `'KH99'` $\rightarrow$ Bị chặn đứng ngay!
- **Kỹ thuật đạt độ phủ đề bài yêu cầu**:
  - *Đề bài:* "Tồn tại ít nhất 1 khách mua nhiều hơn 1 đơn hàng" $\rightarrow$ Cho khách `'KH01'` mua cả đơn `'DH01'` và đơn `'DH02'`.
  - *Đề bài:* "Tồn tại ít nhất 1 nhân viên thụ lý nhiều hơn 1 đơn hàng" $\rightarrow$ Cho nhân viên `'NV01'` duyệt cả 2 đơn đó.

---

## 2. Ví Dụ Code Thật (Tiếng Việt Viết Tắt)

```sql
USE tempdb;
GO

SET DATEFORMAT dmy;
GO

-- Chèn 2 đơn hàng: Khách KH01 mua cả 2 đơn, Nhân viên NV01 duyệt cả 2 đơn
INSERT INTO tblDonHang (MaDH, NgayDat, TrangThai, MaKH, MaNV)
VALUES 
    ('DH01', '15/10/2026', N'Chờ duyệt', 'KH01', 'NV01'),
    ('DH02', '16/10/2026', N'Đang giao', 'KH01', 'NV01');
GO
```

### Kết quả trực quan đối chiếu ràng buộc:

| MaDH     | NgayDat    | TrangThai   | MaKH (FK) | MaNV (FK) | Trạng thái                                                         |
| :------- | :--------- | :---------- | :-------- | :-------- | :------------------------------------------------------------------- |
| `DH01` | 15/10/2026 | Chờ duyệt | `KH01`  | `NV01`  | ✅ Hợp lệ (KH01, NV01 có thật)                                   |
| `DH02` | 16/10/2026 | Đang giao  | `KH01`  | `NV01`  | ✅ Đạt độ phủ (KH01 mua 2 đơn)                                |
| `DH03` | 17/10/2026 | Chờ duyệt | `KH99`  | `NV01`  | ❌ **Lỗi ngay!** (Vì `KH99` không có trong tblKhachHang) |

---

## 3. Bài Tập Thực Hành (Sếp gõ code vào Code Block bên dưới)

### Nhiệm Vụ 9: Chèn 2 Dòng Cho Bảng Chi Tiết Đơn Hàng (`tblChiTietDonHang`)

Bảng `tblChiTietDonHang` gồm 4 cột: `MaDH`, `MaSP`, `SoLuong`, `DonGia`.

- *Yêu cầu độ phủ của đề bài:* "Tồn tại ít nhất một đơn hàng có nhiều hơn 1 loại sản phẩm".
- *Cách làm:* Cho đơn hàng `'DH01'` mua cả 2 sản phẩm `'SP01'` và `'SP02'`.

```sql
-- SẾP VIẾT CODE NHIỆM VỤ 9 VÀO ĐÂY:
INSERT INTO tblChiTietDonHang (MaDH, MaSP, SoLuong, DonGia)
VALUES 
    -- Dòng 1: Đơn DH01 mua sản phẩm SP01, số lượng 2:
    ('DH01', 'SP01', 2, 850000),

    -- Dòng 2: Đơn DH01 (nhớ có số 0) mua sản phẩm SP02, số lượng 1:
    ('DH01', 'SP02', 1, 350000);
GO
```

---
---

# 🎯 BẢNG TỔNG KẾT VŨ KHÍ PHÒNG THI GIỮA KÌ (CHUẨN 100% TUẦN 5 - 6 - 7)

> **Thông điệp:** Em cắt bỏ ngay phần JOIN! Giữa kì năm 2 chỉ chốt hạ ở **Tuần 5 + 6 + 7**. Sếp chỉ cần nắm chắc 3 mảnh ghép dưới đây là tự tin giật điểm 8 - 10!

---

### MẢNH GHÉP 1: TẠO BẢNG DDL CƠ BẢN (BÀI TẬP TUẦN 5)
```sql
-- 1. Bảng Cha (Độc lập): Tạo trước, Khóa chính đơn
CREATE TABLE tblKhachHang (
    MaKH    CHAR(6) NOT NULL PRIMARY KEY,
    TenKH   NVARCHAR(50) NOT NULL,
    SoDu    MONEY NULL
);

-- 2. Bảng Con (1 - N): Tạo sau, có Khóa ngoại tham chiếu cha
CREATE TABLE tblDonHang (
    MaDH    CHAR(7) NOT NULL PRIMARY KEY,
    NgayDat DATETIME NULL,
    MaKH    CHAR(6) NOT NULL FOREIGN KEY REFERENCES tblKhachHang(MaKH)
);

-- 3. Bảng Chi Tiết (Cầu nối N - N): Khóa chính phức hợp 2 cột
CREATE TABLE tblChiTietDonHang (
    MaDH    CHAR(7) NOT NULL,
    MaSP    CHAR(7) NOT NULL,
    SoLuong INT NOT NULL,
    PRIMARY KEY (MaDH, MaSP), -- Khóa chính 2 cột
    FOREIGN KEY (MaDH) REFERENCES tblDonHang(MaDH),
    FOREIGN KEY (MaSP) REFERENCES tblSanPham(MaSP)
);
```

---

### MẢNH GHÉP 2: RÀNG BUỘC VỚI LỆNH `ALTER TABLE` (BÀI TẬP TUẦN 6)
```sql
-- 1. Ràng buộc DEFAULT (Điền giá trị mặc định):
ALTER TABLE tblKhachHang 
ADD CONSTRAINT DF_KhachHang_DiaChi DEFAULT N'Đà Nẵng' FOR DiaChi;

-- 2. Ràng buộc CHECK điều kiện số (Lớn hơn hoặc bằng 0):
ALTER TABLE tblKhachHang 
ADD CONSTRAINT CK_KhachHang_SoDu CHECK (SoDu >= 0);

-- 3. Ràng buộc CHECK tuổi đủ 18:
ALTER TABLE tblNhanVien 
ADD CONSTRAINT CK_NhanVien_Tuoi CHECK (DATEDIFF(year, NgaySinh, GETDATE()) >= 18);

-- 4. Ràng buộc CHECK trạng thái thuộc danh sách IN:
ALTER TABLE tblDonHang 
ADD CONSTRAINT CK_DonHang_TrangThai CHECK (TrangThai IN (N'Chờ duyệt', N'Đang giao', N'Đã giao'));

-- 5. Ràng buộc CHECK ngày đặt <= ngày hiện tại:
ALTER TABLE tblDonHang 
ADD CONSTRAINT CK_DonHang_NgayDat CHECK (NgayDat <= GETDATE());

-- 6. Khóa ngoại có xóa dây chuyền (ON DELETE CASCADE):
ALTER TABLE tblChiTietDonHang
ADD CONSTRAINT FK_ChiTietDonHang_DonHang
FOREIGN KEY (MaDH) REFERENCES tblDonHang(MaDH)
ON DELETE CASCADE ON UPDATE CASCADE;
```

---

### MẢNH GHÉP 3: NHẬP LIỆU DML & ĐỘ PHỦ (BÀI TẬP TUẦN 7)
```sql
-- 1. Lệnh sống còn trước khi nhập ngày:
SET DATEFORMAT dmy;
GO

-- 2. Chèn đa dòng: Chuỗi có nháy đơn, tiếng Việt có N'...'
INSERT INTO tblSanPham (MaSP, TenSP, DonGia, SoLuong)
VALUES 
    ('SP01', N'Bàn phím cơ', 850000, 20),
    ('SP02', N'Chuột không dây', 350000, 50);

-- 3. Chèn bảng con đạt độ phủ (1 khách mua 2 đơn, 1 đơn mua 2 sản phẩm):
INSERT INTO tblDonHang (MaDH, NgayDat, TrangThai, MaKH, MaNV)
VALUES 
    ('DH01', '15/10/2026', N'Chờ duyệt', 'KH01', 'NV01'),
    ('DH02', '16/10/2026', N'Đang giao', 'KH01', 'NV01'); -- Cùng khách KH01

INSERT INTO tblChiTietDonHang (MaDH, MaSP, SoLuong, DonGia)
VALUES 
    ('DH01', 'SP01', 2, 850000),
    ('DH01', 'SP02', 1, 350000); -- Cùng đơn DH01 mua 2 SP
```


