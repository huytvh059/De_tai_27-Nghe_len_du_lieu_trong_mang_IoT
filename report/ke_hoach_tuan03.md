# Kế hoạch Tuần 03 - Đề tài 27

## Mục tiêu Tuần 03

Hoàn thiện minh chứng thực nghiệm cho demo MQTT, thu log/ảnh màn hình và chuẩn bị nội dung báo cáo/slide.

## Kế hoạch chi tiết

| STT | Công việc | Sản phẩm dự kiến | Thời hạn | Ghi chú |
|---|---|---|---|---|
| 1 | Chạy demo `cleartext` | Log cho thấy JSON đọc được trực tiếp | Đầu tuần 03 | Lưu vào `results/logs/cleartext_traffic.log` |
| 2 | Chạy demo `hmac` | Log xác thực hợp lệ và log phát hiện sửa đổi | Giữa tuần 03 | Dùng `--simulate-attack` |
| 3 | Chạy demo `encrypted` | Log ciphertext và giải mã thành công | Giữa tuần 03 | Dùng AES-GCM |
| 4 | Chụp ảnh màn hình demo | Ảnh terminal publisher/subscriber | Giữa tuần 03 | Lưu vào `results/screenshots/` |
| 5 | Hoàn thiện bảng rủi ro | Bảng nghe lén/sửa đổi/giả mạo/replay | Cuối tuần 03 | Đưa vào báo cáo |
| 6 | Chuẩn bị slide | Slide vấn đề, mô hình, kết quả, kết luận | Cuối tuần 03 | Có ít nhất 1 hình tự vẽ |

## Kết quả cần có cuối Tuần 03

- Log chạy đủ 3 chế độ.
- Ảnh màn hình demo.
- README cập nhật minh chứng.
- Bảng rủi ro hoàn thiện.
- Bản nháp slide/báo cáo.

## Rủi ro tiến độ

| Rủi ro | Ảnh hưởng | Cách xử lý |
|---|---|---|
| Broker công cộng không ổn định | Không chạy được demo | Chuyển sang Mosquitto local |
| Thiếu thư viện Python | Lỗi chạy chương trình | Cài `paho-mqtt cryptography` |
| Chưa có ảnh minh chứng | Thiếu bằng chứng nộp | Chụp terminal khi chạy từng kịch bản |
