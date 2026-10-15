---
name: interactive-lab-architect
description: Thiết kế mô phỏng HTML5/Canvas tự chứa có điểm gãy phi tuyến, đối sánh Ghost-Trace và xuất Telemetry [LAB_RECEIPT].
when_to_use: Kích hoạt khi thiết kế lab.html trong workflows/generate-lesson.md khi Visual Gate xác định visual là lab.
allowed-tools: Read, Write, Edit
version: 1.1.0
triggers:
  - build-interactive-lab
  - visual-gate-lab
---

# Interactive Lab Architect

Chống bệnh "Lab đồ chơi tuyến tính" (kéo thanh trượt $A$ thì $B$ tăng đều). Biến `lab.html` thành phòng thí nghiệm tư duy có chiều sâu khám phá.

## 1. Non-Linear / Trade-off Simulation Engine
- **CẤM:** Mô phỏng đơn tuyến bậc nhất ($y = a \cdot x$).
- **BẮT BUỘC:** Cài đặt ít nhất 1 trong 3 cơ chế tạo Aha Moment:
  - **Competing Forces (Đánh đổi):** Cải thiện biến $A$ làm suy giảm biến $B$ (tốc độ vs chính xác, bảo mật vs độ trễ).
  - **Inflection / Tipping Point (Ngưỡng gãy):** Trạng thái ổn định cho đến khi tham số vượt ngưỡng tới hạn $T_{crit}$ làm hệ thống đổi pha hoặc sập.
  - **Regime Switch (Chuyển chế độ):** Công tắc chuyển đổi cấu trúc vận hành để đối sánh trực quan 2 mô hình.

## 2. Visual Comparison & Ghost-Trace Pattern
- **Ghost Trace:** Khi người học chạy thử nghiệm mới, lưu lại quỹ đạo lần chạy trước với độ mờ (`opacity: 0.25`, nét đứt) để lộ rõ độ lệch nhân quả.
- **Cognitive Flow Gate:** Khóa nút chuyển sang pha Explain cho đến khi người học chọn xong Predict và thực hiện tối thiểu 2 lần thay đổi tham số ở pha Manipulate.

## 3. Rich Telemetry trong [LAB_RECEIPT]
Nút *"Sao chép kết quả Lab"* bắt buộc thu thập và đóng gói dữ liệu vào block `[LAB_RECEIPT]...[/LAB_RECEIPT]`:
- `prediction_choice`: Lựa chọn giả thuyết ban đầu của người học.
- `explored_bounds`: Mảng các tham số đã thử và cờ `tipping_point_reached: true/false`.
- `learner_explanation`: Lời tự giải thích cơ chế của người học.

## 4. Examples
```json
[LAB_RECEIPT]
{
  "prediction_choice": "latency_drops",
  "explored_bounds": [{"concurrency": 50, "p99": 12}, {"concurrency": 500, "p99": 840}],
  "tipping_point_reached": true,
  "learner_explanation": "Vượt quá connection pool làm hàng đợi tràn phi tuyến."
}
[/LAB_RECEIPT]
```
