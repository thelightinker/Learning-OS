---
name: verbatim-quarantine
trigger: model_decision
description: Quy tắc bảo toàn nguồn tuyệt đối, kiểm soát băm SHA-256 và cách ly tệp nguyên văn source_verbatim.md.
version: 1.0.0
priority: P0
---

# Verbatim Quarantine Invariant (Bảo Toàn Nguồn Tuyệt Đối)

## 1. Bản Chất Rủi Ro & Điều Răn Bất Biến
Khi học sách hoặc tài liệu nguyên bản, người học cần hấp thụ chính xác tư tưởng và ngôn từ của tác giả. Mọi hành vi tự ý tóm tắt, viết lại, hoặc diễn giải tráo đổi câu chữ trong văn bản gốc đều bị coi là lỗi nghiêm trọng (`CRITICAL_SOURCE_MUTATION`).

## 2. Giao Thức Cách Ly Vật Lý Hai Tệp
- `source_verbatim.md`: 100% văn bản nguyên bản của tác giả. CẤM chỉnh sửa, cấm tóm tắt, cấm thêm lời bình.
- `lesson.md`: Tài liệu hướng dẫn đồng hành (Companion Guide) của Agent. Toàn bộ câu hỏi Socratic, giải thích từ ngữ và bài tập thực hành nằm tại đây.
- Neo tham chiếu: Mọi câu hỏi trong `lesson.md` tham chiếu về nguồn qua nhãn đoạn văn `[¶1]`, `[¶2]` (ví dụ: *"Đọc đoạn [¶4] và chỉ ra..."*).

## 3. Trích Xuất Cơ Học Qua Line Offset
- Tuyệt đối CẤM dùng LLM để gõ lại nội dung nguồn vào `source_verbatim.md`.
- BẮT BUỘC dùng script hệ thống `extract_segment.py` để cắt cơ học:
  1. Dùng `extract_segment.py --source <file> --inspect` để tra cứu số dòng Headings ($< 200$ tokens).
  2. Dùng `extract_segment.py --source <file> --start-line <N> --end-line <M> --output <dest>` để cắt chính xác đoạn văn bản.
- Header bắt buộc của `source_verbatim.md`:
  `<!-- verbatim_meta: {"source": "inputs/...", "start_line": N, "end_line": M} -->`

## 4. Bảo Vệ Khối Mã (Code Block Guard)
- Khi script chèn nhãn neo `[¶N]`, nếu gặp khối mã Markdown (bắt đầu bằng ` ``` `) hoặc bảng dữ liệu, script giữ nguyên vẹn 100% và KHÔNG chèn `[¶N]` vào giữa các dòng trống bên trong khối mã.

## 5. Thẩm Định Băm Chuỗi Chuẩn Hóa
- `verify_system.py` đọc `verbatim_meta`, cắt đúng dòng `start_line:end_line` từ file gốc và băm SHA-256 sau khi chuẩn hóa Unicode NFC và khoảng trắng.
- Nếu sai khác dù chỉ 1 ký tự, hệ thống chặn phát hành module bài học ngay lập tức.
