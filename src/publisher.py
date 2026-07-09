import time
import json
import csv
import argparse
import os
import sys

# Đảm bảo in ký tự Unicode (tiếng Việt) không bị lỗi trên Windows Console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import paho.mqtt.client as mqtt

# Import các hàm mã hóa từ thư viện utils cục bộ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import calculate_hmac, encrypt_data

def get_mqtt_client(username=None, password=None):
    """
    Khởi tạo MQTT client hỗ trợ cả phiên bản Paho v1.x và v2.x
    """
    try:
        from paho.mqtt.enums import CallbackAPIVersion
        client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    except ImportError:
        client = mqtt.Client()
        
    if username and password:
        client.username_pw_set(username, password)
    return client

def main():
    parser = argparse.ArgumentParser(description="MQTT Publisher - Mô phỏng thiết bị cảm biến IoT")
    parser.add_argument("--broker", default="test.mosquitto.org", help="Địa chỉ MQTT Broker (mặc định: test.mosquitto.org)")
    parser.add_argument("--port", type=int, default=1883, help="Cổng kết nối Broker (mặc định: 1883)")
    parser.add_argument("--mode", choices=["cleartext", "hmac", "encrypted"], default="cleartext", 
                        help="Chế độ bảo mật gửi payload (cleartext / hmac / encrypted)")
    parser.add_argument("--topic", default="iot/sensor/data", help="MQTT Topic để gửi dữ liệu")
    parser.add_argument("--username", default=None, help="Tên đăng nhập (nếu broker yêu cầu)")
    parser.add_argument("--password", default=None, help="Mật khẩu (nếu broker yêu cầu)")
    parser.add_argument("--interval", type=float, default=2.0, help="Khoảng thời gian gửi giữa các gói tin (giây)")
    
    args = parser.parse_args()
    
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dataset_gia_lap.csv")
    if not os.path.exists(csv_file_path):
        print(f"[-] Không tìm thấy file dữ liệu giả lập tại: {csv_file_path}")
        sys.exit(1)
        
    # Kết nối tới Broker
    client = get_mqtt_client(args.username, args.password)
    
    print(f"[*] Đang kết nối tới MQTT Broker {args.broker}:{args.port}...")
    try:
        client.connect(args.broker, args.port, 60)
    except Exception as e:
        print(f"[-] Kết nối thất bại: {e}")
        sys.exit(1)
        
    client.loop_start()
    
    print(f"[+] Đã kết nối thành công! Đang gửi dữ liệu ở chế độ [{args.mode.upper()}]...")
    
    try:
        with open(csv_file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                # Tạo payload từ dòng dữ liệu cảm biến
                sensor_data = {
                    "timestamp": row["timestamp"],
                    "device_id": row["device_id"],
                    "temperature": float(row["temperature"]),
                    "humidity": float(row["humidity"]),
                    "status": row["status"]
                }
                
                raw_json = json.dumps(sensor_data)
                
                # Xử lý theo từng chế độ bảo mật
                if args.mode == "cleartext":
                    # Gửi trực tiếp dữ liệu dạng rõ
                    payload_to_send = raw_json
                elif args.mode == "hmac":
                    # Tính toán mã băm HMAC cho dữ liệu cảm biến và đính kèm vào payload
                    signature = calculate_hmac(raw_json)
                    payload_to_send = json.dumps({
                        "data": sensor_data,
                        "hmac": signature
                    })
                elif args.mode == "encrypted":
                    # Mã hóa toàn bộ dữ liệu cảm biến bằng AES-256-GCM
                    encrypted_dict = encrypt_data(sensor_data)
                    payload_to_send = json.dumps(encrypted_dict)
                
                # Gửi bản tin MQTT
                print(f"\n[Gửi gói tin #{idx+1}] Topic: {args.topic}")
                print(f"Payload gửi đi:\n{payload_to_send}")
                
                client.publish(args.topic, payload_to_send, qos=1)
                time.sleep(args.interval)
                
    except KeyboardInterrupt:
        print("\n[*] Dừng gửi dữ liệu theo yêu cầu người dùng.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[*] Đã ngắt kết nối.")

if __name__ == "__main__":
    main()
