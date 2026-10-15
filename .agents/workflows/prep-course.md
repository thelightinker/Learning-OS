---
name: prep-course
description: Tiếp nhận tự động từ inbox, phân loại archetype và đề xuất chiến lược khóa học tối giản
version: 1.0.0
requires_agents:
  - learning-architect
requires_skills: []
artifact_outputs:
  - catalog.json
---

# Workflow: /prep-course (Tiếp Nhận Nguồn & Chuẩn Bị Xây Dựng Khóa Học)

Quy trình tự động quét hòm thư duy nhất `inputs/inbox/`, phân loại Archetype tài liệu nguồn, bảo toàn nguyên bản 100% bằng băm SHA-256 và đề xuất chiến lược khóa học trước khi khởi tạo.

---

### [STATE: SCAN_AND_CATALOG]
- **Mục tiêu:** Quét toàn bộ tài liệu trong `inputs/inbox/`, trích xuất siêu dữ liệu và phân loại Archetype mà không sửa đổi file gốc.
- **Thực thi:**
  ```bash
  python .agents/scripts/catalog_inbox.py --inbox "inputs/inbox" --output "inputs/catalog.json"
  ```
- **DoD:**
  - [ ] Lệnh quét trả về exit code 0.
  - [ ] `inputs/catalog.json` được tạo, chứa danh sách tài liệu, mã băm SHA-256, số dòng, mục lục sơ bộ và Archetype đề xuất.
- **Evaluation Loop:** Có tài liệu $\rightarrow$ Chuyển `[STATE: PROPOSE_COURSE_STRATEGY]` | Không có tài liệu $\rightarrow$ Nhắc người học thả file vào `inputs/inbox/`.

---

### [STATE: PROPOSE_COURSE_STRATEGY]
- **Mục tiêu:** Đề xuất chiến lược sư phạm tối ưu và khung module dự kiến dựa trên `catalog.json`.
- **Nội dung Đề Xuất (Hiển thị trong Chat):**
  1. **Khóa học & Slug đề xuất:** (Ví dụ: `clean-architecture`, `system-design`).
  2. **Phương thức học đề xuất (Learning Track):**
     - *Verbatim Line-Slice:* Dành cho sách nguyên bản (học sâu từng đoạn [¶N]).
     - *Paper Deep-Dive:* Dành cho tài liệu nghiên cứu chuyên khảo.
     - *Synthesis & Active Recall:* Dành cho ghi chép, transcript đa nguồn.
  3. **Khung Module dự kiến:** Bảng phân chia các module $1.500 - 3.000$ từ/module kèm dự đoán module nào nên có Web Lab.
- **DoD:**
  - [ ] Đề xuất ngắn gọn, rõ ràng, nêu rõ đòn bẩy 80/20.
  - [ ] Chờ xác nhận từ người học (chỉ cần gõ *"Duyệt"* hoặc chỉnh sửa yêu cầu).
- **Evaluation Loop:** Người học đồng ý $\rightarrow$ Chuyển `[STATE: HANDOFF_TO_INGEST]`.

---

### [STATE: HANDOFF_TO_INGEST]
- **Mục tiêu:** Bàn giao sang quy trình `/ingest` để khởi tạo không gian khóa học thực tế.
- **Thực thi:**
  - Chuyển giao ngữ cảnh sang `workflows/ingest.md`.
  - Khởi tạo `learning-space/courses/<slug>/00_overview/syllabus.md` và `progress.md`.
- **DoD:**
  - [ ] Không gian khóa học được khởi tạo hoàn chỉnh, sẵn sàng soạn bài học đầu tiên.
- **[ESCALATE_HUMAN]:** Nếu tài liệu là PDF dạng scan hoặc chứa mã hóa không đọc được text, dừng lại và yêu cầu người học cung cấp bản text có thể đọc được.
