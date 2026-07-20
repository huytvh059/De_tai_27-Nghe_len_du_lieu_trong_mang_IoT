# Nghe lén dữ liệu cảm biến trong mạng IoT

Đề tài 27 - Bảo mật IoT (INT4410). Demo cho thấy dữ liệu cảm biến gửi qua MQTT
dạng thô thì ai bắt gói cũng đọc được, và ba cách xử lý: gửi thô, ký HMAC, và
mã hóa AES-256-GCM.

Publisher đóng vai cảm biến (đọc số liệu giả lập từ `data/dataset_gia_lap.csv`),
Subscriber đóng vai server nhận và kiểm tra dữ liệu. Cả hai nói chuyện qua một
MQTT broker.

## Cài đặt

Cần Python 3 và hai thư viện:

```bash
pip install paho-mqtt cryptography
```

## Chạy thử

Mở hai cửa sổ terminal. Mặc định dùng broker công khai `test.mosquitto.org`
nên không phải cài broker riêng.

Cửa sổ 1 - subscriber (chọn `cleartext`, `hmac` hoặc `encrypted`):

```bash
python src/subscriber.py --mode cleartext
```

Cửa sổ 2 - publisher (mode phải trùng với subscriber):

```bash
python src/publisher.py --mode cleartext --interval 1.5
```

Muốn xem cơ chế toàn vẹn hoạt động thế nào, chạy subscriber với `--simulate-attack`:
nó sẽ sửa gói tin sau khi nhận, HMAC/AES sẽ báo dữ liệu đã bị đổi.

```bash
python src/subscriber.py --mode hmac --simulate-attack
```

Ba mode khác nhau ở chỗ:

- `cleartext` - gửi JSON thô, đọc trộm được toàn bộ.
- `hmac` - đính kèm HMAC-SHA256, vẫn đọc được nhưng sửa là bị phát hiện.
- `encrypted` - mã hóa AES-256-GCM, trên đường truyền chỉ còn chuỗi vô nghĩa.

Log và dữ liệu subscriber nhận được lưu trong `results/`.

## Broker cục bộ (tùy chọn)

Thư mục `configs/` có sẵn `mosquitto.conf`, `aclfile` và `passwd` mẫu để chạy
Mosquitto trên máy, dùng cho phần thử xác thực và phân quyền topic (ACL). Tạo mật
khẩu rồi trỏ publisher/subscriber về `127.0.0.1`:

```bash
mosquitto_passwd -c configs/passwd publisher_user
mosquitto -c configs/mosquitto.conf -v
python src/publisher.py --broker 127.0.0.1 --username publisher_user --password <pass>
```

## Thư mục

- `src/` - publisher, subscriber và các hàm HMAC/AES trong `utils.py`
- `configs/` - cấu hình Mosquitto
- `data/` - dữ liệu cảm biến giả lập
- `results/` - log, screenshot, output
- `report/`, `slides/` - báo cáo và slide
- `references/` - nguồn tham khảo

## Nguồn

Eclipse Mosquitto, Eclipse Paho MQTT (Python), RFC 2104 (HMAC),
NIST SP 800-38D (AES-GCM). Chi tiết trong `references/link_nguon.md`.
