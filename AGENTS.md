# Learning OS — Agent Operational Contract

Khế ước vận hành tối thượng cho IDE Agent khi làm việc trong workspace Learning OS.

## 1. Quy tắc Đọc Trước Khi Nói (Read-Before-Speak)
Mở đầu phiên học mới hoặc khi người học tiếp tục, Agent BẮT BUỘC đọc snapshot `progress.md` của khóa học hiện hành trước khi sinh phản hồi đầu tiên. Tuyệt đối không chào hỏi chung chung khi chưa nắm vị trí hiện tại và hàng đợi ôn tập.

## 2. Bảng Ánh Xạ Ý Định Tự Nhiên (Intent Routing)
- "Chuẩn bị khóa học" / "Quét inbox" / Thả tài liệu vào `inputs/inbox/` -> Gọi quy trình `/prep-course`
- "Học tài liệu này" / Cung cấp nguồn mới -> Gọi quy trình `/ingest`
- "Soạn bài tiếp theo" / "Tạo module mới" -> Gọi quy trình `/generate-lesson`
- "Tiếp tục học" / "Vào bài học" -> Gọi quy trình `/session`
- "Chấm bài" / Paste `[LAB_RECEIPT]` -> Gọi quy trình `/assess`
- "Học tiếp sau gián đoạn" -> Gọi quy trình `/resume`

## 3. Quản Trị Ngữ Cảnh & Nạp Theo Nhu Cầu (Just-In-Time Rules & Skills)
Chỉ nạp các quy tắc trong `.agents/rules/` khi cần thiết:
- Khi soạn bài hoặc chấm điểm -> Nạp `pedagogical-invariants.md`
- Khi xử lý tài liệu nguồn nguyên bản -> Nạp `verbatim-quarantine.md`
- Khi cân nhắc thêm sơ đồ hoặc Web Lab -> Nạp `visual-strategy.md`

### On-Demand Skills Routing (Cấm nạp sẵn toàn bộ khi khởi động)
- Khi viết `lesson.md`: Nạp `skills/socratic-companion-crafter/SKILL.md` (chống paraphrase, câu hỏi Socratic).
- Khi tạo `lab.html`: Nạp `skills/interactive-lab-architect/SKILL.md` (mô phỏng phi tuyến, telemetry).
- Khi chấm bài / ôn tập: Nạp `skills/diagnostic-rubric-clinician/SKILL.md` (4 mã lỗi, counter-example).

## 4. Danh Sách Điều Cấm Tuyệt Đối (Strict Negative Boundaries)
- CẤM chỉnh sửa bất kỳ tệp nào trong thư mục `inputs/` (Read-Only tuyệt đối).
- CẤM "xả rác" ra thư mục gốc (`root`) hoặc `.agents/`: Tuyệt đối KHÔNG tạo file nháp, test script tạm thời (`test_*.py`, `temp_*`, `scratch.*`, `tmp_*`, `*.tmp`) tại root hoặc trong `.agents/`.
- CẤM lưu dữ liệu trung gian sai nơi: Mọi file nháp, scratchpad hoặc script thử nghiệm cơ động BẮT BUỘC nhốt trong `.tmp/` hoặc thư mục `scratch/` của IDE Agent và phải tự dọn dẹp sau khi hoàn thành tác vụ.
- CẤM tạo file bài học ngoài cây cấu trúc: Mọi bài học, sơ đồ, Web Lab phải nằm đúng trong `learning-space/courses/<course-slug>/modules/M<NN>_<slug>/`.
- CẤM dùng LLM gõ lại văn bản gốc vào `source_verbatim.md`; bắt buộc dùng `extract_segment.py`.
- CẤM nạp toàn bộ tệp `progress-log.md` vào context; chỉ append qua `verify_system.py --append-log`.
- CẤM chèn liên kết ngoài (`http://`, `https://`) hoặc CDN vào `lab.html`.
- CẤM sinh visual hoặc lab khi chưa vượt qua cổng thị giác và chưa có lý do sư phạm trong frontmatter.
