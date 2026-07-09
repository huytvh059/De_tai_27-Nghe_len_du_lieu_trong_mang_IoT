# Đề cương Tuần 02 - Đề tài 27

## 1. Thông tin đề tài

- **Sinh viên:** Thi Võ Hoàng Huy
- **Mã sinh viên:** 231A010454
- **Học phần:** Bảo mật trong IoT
- **Mã đề tài:** 27
- **Tên đề tài:** Nghe lén dữ liệu cảm biến trong mạng IoT
- **Repo GitHub:** https://github.com/huytvh059/De_tai_27-Nghe_len_du_lieu_trong_mang_IoT

## 2. Lý do chọn đề tài

Trong hệ thống IoT, thiết bị cảm biến thường gửi dữ liệu định kỳ về gateway hoặc server qua MQTT. Nếu payload được truyền dạng rõ, người cùng mạng có thể nghe lén để đọc thông tin như `device_id`, nhiệt độ, độ ẩm, vị trí hoặc trạng thái thiết bị.

Đề tài này minh họa rủi ro khi dữ liệu cảm biến truyền không được bảo vệ, sau đó đề xuất HMAC để phát hiện sửa đổi và AES-GCM để bảo vệ bí mật/toàn vẹn.

## 3. Mục tiêu

- Minh họa dữ liệu cảm biến MQTT truyền dạng rõ có thể bị đọc trực tiếp.
- Xây dựng demo publisher/subscriber bằng Python Paho MQTT.
- So sánh 3 chế độ: `cleartext`, `hmac`, `encrypted`.
- Phân tích nghe lén, sửa đổi dữ liệu, giả mạo thiết bị và replay.
- Đề xuất TLS, xác thực broker, ACL, HMAC hoặc mã hóa payload.

## 4. Phạm vi thực hiện

- Môi trường lab an toàn, dùng dữ liệu giả lập, không tấn công hệ thống thật.
- Giao thức chính: MQTT.
- Broker thử nghiệm: `test.mosquitto.org` hoặc Mosquitto cục bộ.
- Dữ liệu: nhiệt độ, độ ẩm, trạng thái thiết bị mẫu.

## 5. Công cụ và kỹ thuật

| Thành phần | Vai trò |
|---|---|
| Eclipse Mosquitto | MQTT Broker thử nghiệm/cục bộ |
| Eclipse Paho Python | Tạo publisher và subscriber MQTT |
| HMAC-SHA256 | Kiểm tra toàn vẹn và nguồn gốc payload |
| AES-256-GCM | Mã hóa payload, xác thực tag chống sửa đổi |
| Mermaid | Vẽ sơ đồ luồng bảo vệ dữ liệu |
| CSV/JSON | Lưu dữ liệu giả lập và payload mẫu |

## 6. Mô hình hệ thống

```text
Thiết bị cảm biến giả lập -> MQTT Broker -> Server/Subscriber kiểm tra dữ liệu
```

Ba chế độ so sánh:

1. **Cleartext:** payload JSON đọc được trực tiếp.
2. **HMAC:** payload vẫn đọc được nhưng sửa đổi sẽ bị phát hiện.
3. **Encrypted:** payload được mã hóa, kẻ nghe lén chỉ thấy ciphertext.

## 7. Sản phẩm dự kiến

- Repo GitHub đúng cấu trúc yêu cầu.
- Mã nguồn MQTT demo: `publisher.py`, `subscriber.py`, `utils.py`.
- Dataset và payload mẫu.
- Log minh chứng cleartext và payload được bảo vệ.
- Bảng rủi ro nghe lén/sửa đổi/giả mạo/replay.
- Sơ đồ Mermaid luồng bảo vệ dữ liệu.
- Tài liệu tham khảo tối thiểu 5 nguồn.
