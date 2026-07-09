# Phương pháp thực hiện - Đề tài 27

## 1. Nguyên tắc thực hiện

Đề tài được triển khai trong môi trường lab an toàn, chỉ dùng dữ liệu giả lập. Mục tiêu là hiểu rủi ro bảo mật và biện pháp phòng chống, không thực hiện nghe lén hoặc tấn công hệ thống thật.

## 2. Mô hình lab

```text
Publisher giả lập cảm biến -> MQTT Broker -> Subscriber kiểm tra dữ liệu
```

Publisher tạo payload cảm biến. MQTT Broker trung chuyển bản tin. Subscriber nhận payload, ghi log và kiểm tra cơ chế bảo vệ.

## 3. Kịch bản thực nghiệm

| Kịch bản | Payload gửi đi | Kẻ nghe lén thấy gì | Mục tiêu kiểm chứng |
|---|---|---|---|
| Cleartext | JSON thô | Đọc được toàn bộ dữ liệu | Chứng minh rủi ro lộ dữ liệu |
| HMAC-SHA256 | `{data, hmac}` | Đọc được dữ liệu nhưng không sửa được âm thầm | Kiểm tra toàn vẹn |
| AES-256-GCM | `{iv, ciphertext, tag}` | Chỉ thấy bản mã | Bảo vệ bí mật và toàn vẹn |

## 4. Checklist thực hiện

- [x] Tạo repo GitHub đúng tên đề tài.
- [x] Viết publisher/subscriber MQTT bằng Paho.
- [x] Tạo dữ liệu cảm biến giả lập.
- [x] Tạo chế độ cleartext.
- [x] Tạo chế độ HMAC-SHA256.
- [x] Tạo chế độ AES-256-GCM.
- [x] Tạo cấu hình Mosquitto, ACL, passwd mẫu.
- [x] Tạo bảng rủi ro và sơ đồ Mermaid trong README.
- [ ] Tuần 03: chạy demo thực tế, chụp ảnh màn hình và bổ sung log.

## 5. Bảng điều kiện khai thác và phòng chống

| Mối đe dọa | Điều kiện khai thác | Ảnh hưởng | Phòng chống |
|---|---|---|---|
| Nghe lén | Payload MQTT không mã hóa, kẻ tấn công cùng mạng | Lộ dữ liệu cảm biến | TLS hoặc AES-GCM payload |
| Sửa đổi | Không có kiểm tra toàn vẹn | Dữ liệu sai lệch | HMAC-SHA256 hoặc AES-GCM tag |
| Giả mạo | Broker cho publish tự do, không ACL | Thiết bị giả gửi dữ liệu | Username/password, ACL, topic riêng |
| Replay | Không có timestamp/nonce | Gửi lại dữ liệu cũ | Timestamp, nonce, kiểm tra thời gian |

## 6. Minh chứng hiện có

- Mã nguồn: `src/publisher.py`, `src/subscriber.py`, `src/utils.py`.
- Dataset: `data/dataset_gia_lap.csv`.
- Payload mẫu: `data/payload_mau.json`.
- Log mẫu: `results/logs/`.
- Sơ đồ và bảng rủi ro: `README.md`.
