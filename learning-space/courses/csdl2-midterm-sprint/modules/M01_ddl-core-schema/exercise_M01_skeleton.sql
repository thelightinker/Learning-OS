/* ==============================================================================
   BÀI 1: TẠO BẢNG ĐƠN GIẢN & KHÓA CHÍNH (PRIMARY KEY)
   ============================================================================== */

/* --- 1. GIẢI THÍCH NGẮN GỌN (ĐỌC 20 GIÂY) ---
   - Bảng (Table): Chứa dữ liệu gồm các Cột (Column) và Hàng (Row).
   - Cú pháp tạo bảng: 
        CREATE TABLE TênBảng ( TênCột KiểuDữLiệu RàngBuộc );
   - Khóa chính (PRIMARY KEY): Cột định danh từng dòng, cấm trùng lặp, cấm để trống (NOT NULL).
   - Kiểu chữ hay gặp:
        + CHAR(n): Mã cố định n ký tự (ví dụ mã SV, mã SP: CHAR(7)).
        + VARCHAR(n): Chuỗi không dấu, đổi độ dài (ví dụ: TelNo, Email).
        + NVARCHAR(n): Chuỗi tiếng Việt có dấu (ví dụ: Tên, Địa chỉ).
   - Kiểu số/tiền hay gặp:
        + INT: Số lượng nguyên (1, 2, 100).
        + MONEY: Tiền tệ.
*/

-- ==============================================================================
-- 2. VÍ DỤ CODE THẬT & KẾT QUẢ TRỰC QUAN
-- ==============================================================================
USE tempdb; -- Luyện tập trên tempdb cho sạch máy
GO

-- Xóa bảng cũ nếu đã tồn tại trước đó để chạy lại không bị lỗi
DROP TABLE IF EXISTS tblDonVi;

-- Tạo bảng Đơn vị tính
CREATE TABLE tblDonVi
(
    MaDV   CHAR(4) NOT NULL PRIMARY KEY,   -- Khóa chính: mã 4 ký tự (vd: 'DV01')
    TenDV  NVARCHAR(30) NOT NULL           -- Tên tiếng Việt (vd: N'Hộp', N'Cái')
);
GO

/*
KẾT QUẢ TRỰC QUAN SINH RA KHI INSERT VÀ SELECT BẢNG tblDonVi:
+--------+------------+
| MaDV   | TenDV      |  <-- Cột MaDV là PRIMARY KEY: Không thể có 2 dòng cùng 'DV01'
+--------+------------+
| DV01   | Hộp        |
| DV02   | Thùng      |
+--------+------------+
*/


-- ==============================================================================
-- 3. BÀI TẬP THỰC HÀNH CỦA SẾP (Gõ code vào giữa 2 dòng đánh dấu)
-- ==============================================================================

/* ------------------------------------------------------------------------------
   BÀI TẬP 1: Tạo bảng Nhà cung cấp [tblSupplier]
   Yêu cầu các cột:
   - SuppID:      CHAR(6) NOT NULL, là PRIMARY KEY
   - SuppName:    NVARCHAR(50) NOT NULL
   - SuppAddress: NVARCHAR(50) NULL (cho phép để trống)
   - TelNo:       VARCHAR(11) NULL (cho phép để trống)
   (Gợi ý: Thêm dòng DROP TABLE IF EXISTS tblSupplier; ở đầu)
   ------------------------------------------------------------------------------ */
-- BẮT ĐẦU CODE BÀI 1:



-- KẾT THÚC CODE BÀI 1
GO


/* ------------------------------------------------------------------------------
   BÀI TẬP 2: Tạo bảng Sản phẩm [tblProduct]
   Yêu cầu các cột:
   - ProductID:   CHAR(7) NOT NULL, là PRIMARY KEY
   - ProductName: NVARCHAR(50) NOT NULL
   - UnitPrice:   MONEY NOT NULL
   - QtyOnHand:   INT NOT NULL
   (Gợi ý: Thêm dòng DROP TABLE IF EXISTS tblProduct; ở đầu)
   ------------------------------------------------------------------------------ */
-- BẮT ĐẦU CODE BÀI 2:



-- KẾT THÚC CODE BÀI 2
GO
