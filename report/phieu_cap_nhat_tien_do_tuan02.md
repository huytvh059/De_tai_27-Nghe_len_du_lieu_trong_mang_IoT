# Phiếu cập nhật tiến độ đề tài - Tuần 02

## 1. Thông tin chung

| Mục | Nội dung |
|---|---|
| Mã SV | 231A010454 |
| Họ và tên | Thi Võ Hoàng Huy |
| Lớp | INT4410 - Bảo mật trong IoT |
| Tuần báo cáo | Tuần 02 |
| Mã đề tài | 27 |
| Tên đề tài | Nghe lén dữ liệu cảm biến trong mạng IoT |
| Link GitHub/repo | https://github.com/huytvh059/De_tai_27-Nghe_len_du_lieu_trong_mang_IoT |
| Ngày cập nhật | 9/7/2026 |
| Mức tự đánh giá | Đúng tiến độ |
| Email/SĐT liên hệ | 0376793807 |
| Nhóm/cá nhân | Cá nhân |

## 2. Checklist tiến độ Tuần 02

| STT | Nội dung cần hoàn thành | Trạng thái | Ghi chú/minh chứng |
|---|---|---|---|
| 1 | Đã tạo repo GitHub/thư mục làm việc và đặt tên đúng đề tài | Xong | Repo GitHub đã tạo và push |
| 2 | Đã viết đề cương 1-2 trang | Xong | `report/de_cuong_tuan02.md` |
| 3 | Đã thu thập tối thiểu 5 tài liệu tham khảo, có GitHub/tool | Xong | `references/link_nguon.md` |
| 4 | Đã xác định công cụ/phương pháp chính | Xong | `report/phuong_phap_thuc_hien.md` |
| 5 | Đã có kế hoạch Tuần 03 rõ ràng | Xong | `report/ke_hoach_tuan03.md` |

## 3. Nội dung đã thực hiện trong tuần

| STT | Công việc | Kết quả hiện tại | Minh chứng/link/file | Tỷ lệ hoàn thành |
|---|---|---|---|---|
| 1 | Tạo repo GitHub | Repo đúng tên đề tài, đã có cấu trúc thư mục | GitHub repo | 100% |
| 2 | Xây dựng demo MQTT | Có publisher/subscriber và 3 chế độ bảo vệ | `src/` | 80% |
| 3 | Chuẩn bị dữ liệu giả lập | Có CSV và JSON mẫu | `data/` | 100% |
| 4 | Viết đề cương và phương pháp | Có tài liệu Markdown trong `report/` | `report/de_cuong_tuan02.md` | 100% |
| 5 | Tổng hợp tài liệu tham khảo | Có hơn 5 nguồn, gồm GitHub/tool | `references/link_nguon.md` | 100% |

## 4. Minh chứng bắt buộc

- Link repo GitHub: https://github.com/huytvh059/De_tai_27-Nghe_len_du_lieu_trong_mang_IoT
- README: `README.md`
- Đề cương Tuần 02: `report/de_cuong_tuan02.md`
- Phương pháp thực hiện: `report/phuong_phap_thuc_hien.md`
- Kế hoạch Tuần 03: `report/ke_hoach_tuan03.md`
- Tài liệu tham khảo: `references/link_nguon.md`
- Code/config/data/log mẫu: `src/`, `configs/`, `data/`, `results/`

## 5. Khó khăn/rủi ro đang gặp

| Vấn đề | Ảnh hưởng tới tiến độ | Hỗ trợ cần từ GV/bạn học |
|---|---|---|
| Broker MQTT công cộng có thể không ổn định | Có thể ảnh hưởng lúc chạy demo trực tiếp | Cho phép dùng Mosquitto local nếu cần |
| Cần bổ sung ảnh màn hình thực nghiệm | Chưa đủ minh chứng trực quan | Tự thực hiện trong Tuần 03 |

## 6. Kế hoạch Tuần 03

| Công việc Tuần 03 | Sản phẩm dự kiến | Thời hạn | Ghi chú |
|---|---|---|---|
| Chạy demo cleartext | Log JSON rõ | Đầu tuần 03 | Lưu vào `results/logs/` |
| Chạy demo HMAC | Log phát hiện sửa đổi | Giữa tuần 03 | Dùng `--simulate-attack` |
| Chạy demo AES-GCM | Log ciphertext/giải mã | Giữa tuần 03 | Kiểm tra tag |
| Chụp ảnh màn hình | Ảnh minh chứng | Giữa tuần 03 | Lưu `results/screenshots/` |
| Chuẩn bị slide/báo cáo | Bản nháp | Cuối tuần 03 | Theo cấu trúc hướng dẫn |

## 7. Tự đánh giá

| Mục | Đánh giá |
|---|---|
| Tiến độ tự đánh giá | 76-100% |
| Mức độ hiểu đề tài | Khá rõ |
| Cam kết tuần tới | Chạy demo, thu log/ảnh màn hình, hoàn thiện slide và báo cáo |
| Chữ ký/tên sinh viên | Thi Võ Hoàng Huy |
