# Tài liệu tham khảo & nguồn liên kết - Đề tài 27

Danh sách nguồn dùng cho đề tài **Nghe lén dữ liệu cảm biến trong mạng IoT**. Các nguồn gồm công cụ GitHub bắt buộc/đề xuất và tài liệu kỹ thuật để giải thích MQTT, HMAC, AES-GCM, TLS.

| STT | Nguồn | Loại | Link | Vai trò trong đề tài |
|---|---|---|---|---|
| 1 | Eclipse Mosquitto | GitHub/tool | https://github.com/eclipse-mosquitto/mosquitto | MQTT Broker dùng để dựng lab và cấu hình xác thực/ACL |
| 2 | Eclipse Paho Python Client | GitHub/tool | https://github.com/eclipse-paho/paho.mqtt.python | Thư viện Python để viết publisher/subscriber MQTT |
| 3 | Mbed TLS | GitHub/tool | https://github.com/Mbed-TLS/mbedtls | Nguồn tham khảo về TLS/mật mã cho thiết bị nhúng IoT |
| 4 | OWASP IoT Security Verification Standard | GitHub/tài liệu | https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS | Checklist kiểm tra bảo mật IoT ở mức truyền tải và dữ liệu |
| 5 | RFC 2104 - HMAC | Chuẩn kỹ thuật | https://datatracker.ietf.org/doc/html/rfc2104 | Cơ sở lý thuyết cho HMAC-SHA256 chống sửa đổi payload |
| 6 | NIST SP 800-38D - AES-GCM | Chuẩn kỹ thuật | https://csrc.nist.gov/publications/detail/sp/800-38d/final | Cơ sở lý thuyết cho AES-GCM bảo vệ bí mật và toàn vẹn |
| 7 | MQTT Version 5.0 Specification | Chuẩn giao thức | https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html | Mô tả nguyên lý publish/subscribe, topic, broker, client |

## Ghi chú sử dụng

- Nguồn 1-3 là nguồn GitHub/tool đúng theo hướng dẫn đề tài.
- Nguồn 4 hỗ trợ phần checklist và đánh giá bảo mật IoT.
- Nguồn 5-7 hỗ trợ phần cơ sở lý thuyết, thuật toán và giao thức.
