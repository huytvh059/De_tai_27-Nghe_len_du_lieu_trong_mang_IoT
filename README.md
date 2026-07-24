# Nghe lén dữ liệu cảm biến trong mạng IoT (Đề tài 27)

Bài tiểu luận cuối kỳ môn **Bảo mật IoT (INT4410)**. Dự án là một demo MQTT thu nhỏ
minh họa: dữ liệu cảm biến gửi dạng **thô (cleartext)** thì ai bắt gói cũng đọc được,
và ba cách bảo vệ dữ liệu — gửi thô, ký **HMAC-SHA256**, mã hóa **AES-256-GCM** — cùng
cơ chế **xác thực + phân quyền (ACL)** ở tầng broker.

- **Publisher** đóng vai cảm biến, đọc số liệu giả lập từ `data/dataset_gia_lap.csv` và gửi payload JSON.
- **Subscriber** đóng vai server giám sát, nhận payload, kiểm tra toàn vẹn/giải mã và ghi log.
- Hai bên nói chuyện qua một **MQTT broker** (broker công khai để thử nhanh, hoặc Mosquitto cục bộ có xác thực/ACL).

## Cấu trúc thư mục

```
.
├── README.md              # Tài liệu này
├── requirements.txt       # Thư viện Python cần cài
├── src/                   # Mã nguồn
│   ├── publisher.py       # Cảm biến giả lập: đọc CSV, gửi payload theo 3 chế độ
│   ├── subscriber.py      # Server nhận: kiểm tra HMAC / giải mã AES, ghi log + output.csv
│   └── utils.py           # Hàm HMAC-SHA256, AES-256-GCM và canonical_json (chuẩn hóa JSON để ký)
├── configs/               # Cấu hình broker Mosquitto cục bộ
│   ├── mosquitto.conf     # Bật xác thực + ACL, log
│   ├── aclfile            # Phân quyền topic (publisher_user: ghi, subscriber_user: đọc)
│   └── passwd             # Mẫu file mật khẩu (tạo bằng mosquitto_passwd)
├── data/                  # Dữ liệu đầu vào
│   ├── dataset_gia_lap.csv# Dữ liệu cảm biến DHT22 giả lập (nhiệt độ, độ ẩm)
│   └── payload_mau.json   # Bản tin mẫu trước/sau khi bảo vệ
├── results/               # Kết quả thực nghiệm (minh chứng)
│   ├── logs/              # Log lưu lượng (cleartext_traffic.log, secure_traffic.log)
│   ├── output.csv         # Dữ liệu subscriber nhận được + trạng thái toàn vẹn
│   └── screenshots/       # Ảnh chụp màn hình các kịch bản
├── report/                # Báo cáo, đề cương, kế hoạch
├── slides/                # Slide trình bày
└── references/            # Nguồn tham khảo (link_nguon.md)
```

## Yêu cầu & cài đặt

Cần **Python 3** và hai thư viện:

```bash
pip install -r requirements.txt
```

(hoặc cài trực tiếp: `pip install paho-mqtt cryptography`)

## Cách chạy / sử dụng

Mở **hai cửa sổ terminal**: một chạy subscriber (bên nhận), một chạy publisher (bên gửi).
`--mode` ở hai bên **phải giống nhau**. Nên chạy **subscriber trước**, rồi mới chạy publisher.

### A. Chạy nhanh trên broker công khai (không cần cài broker)

Mặc định dùng `test.mosquitto.org` nên không cần dựng broker riêng.

Cửa sổ 1 — subscriber (chọn `cleartext`, `hmac` hoặc `encrypted`):

```bash
python src/subscriber.py --mode cleartext
```

Cửa sổ 2 — publisher (mode phải trùng subscriber):

```bash
python src/publisher.py --mode cleartext --interval 1.5
```

Ba chế độ khác nhau ở chỗ:

| Mode | Ý nghĩa |
|------|---------|
| `cleartext` | Gửi JSON thô — kẻ nghe lén đọc được toàn bộ. |
| `hmac` | Đính kèm HMAC-SHA256 — vẫn đọc được nhưng sửa là bị phát hiện. |
| `encrypted` | Mã hóa AES-256-GCM — trên đường truyền chỉ còn chuỗi vô nghĩa. |

Muốn kiểm chứng cơ chế phát hiện sửa đổi, chạy subscriber với `--simulate-attack`
(nó sửa gói tin sau khi nhận; HMAC/AES sẽ báo dữ liệu đã bị đổi):

```bash
python src/subscriber.py --mode hmac --simulate-attack
```

### B. Chạy với broker cục bộ có xác thực + phân quyền (ACL)

Dùng để minh họa chống **giả mạo danh tính** (sai mật khẩu bị từ chối) và **vượt quyền**
(tài khoản chỉ có quyền đọc không được ghi). Cần cài **Eclipse Mosquitto**.

1. Sinh tài khoản thật (chạy trong thư mục dự án):

   ```bash
   mosquitto_passwd -c configs/passwd publisher_user
   mosquitto_passwd    configs/passwd subscriber_user
   ```

2. Chạy broker cục bộ (xem log trực tiếp):

   ```bash
   mosquitto -c configs/mosquitto.conf -v
   ```

3. Trỏ client về broker cục bộ kèm tài khoản:

   ```bash
   # publisher_user có quyền GHI
   python src/publisher.py --broker 127.0.0.1 --username publisher_user --password <mat_khau>
   # subscriber_user có quyền ĐỌC
   python src/subscriber.py --broker 127.0.0.1 --username subscriber_user --password <mat_khau>
   ```

> **Mô hình 2 máy (tùy chọn):** đặt broker trên một máy/VM riêng — sửa `listener 1883 0.0.0.0`
> trong `configs/mosquitto.conf`, rồi ở máy client dùng `--broker <IP_broker>`.

### Tham số dòng lệnh

| Tham số | publisher | subscriber | Mặc định | Mô tả |
|---------|:---:|:---:|----------|-------|
| `--mode` | ✓ | ✓ | `cleartext` | `cleartext` / `hmac` / `encrypted` |
| `--broker` | ✓ | ✓ | `test.mosquitto.org` | Địa chỉ broker |
| `--port` | ✓ | ✓ | `1883` | Cổng broker |
| `--topic` | ✓ | ✓ | `iot/sensor/data` | Topic MQTT |
| `--username` / `--password` | ✓ | ✓ | (rỗng) | Đăng nhập broker (nếu có ACL) |
| `--interval` | ✓ | | `2.0` | Giây giữa các gói (publisher) |
| `--simulate-attack` | | ✓ | tắt | Giả lập sửa gói để kiểm chứng toàn vẹn |

## Kết quả & minh chứng

Log lưu lượng và dữ liệu subscriber nhận được được lưu trong `results/`
(`logs/`, `output.csv`), kèm ảnh chụp màn hình các kịch bản trong `results/screenshots/`.

## Nguồn tham khảo

Eclipse Mosquitto, Eclipse Paho MQTT (Python), RFC 2104 (HMAC),
NIST SP 800-38D (AES-GCM). Chi tiết trong `references/link_nguon.md`.
