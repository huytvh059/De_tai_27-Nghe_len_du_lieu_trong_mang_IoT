import json
import argparse
import os
import sys
import csv
from datetime import datetime

# Đảm bảo in ký tự Unicode (tiếng Việt) không bị lỗi trên Windows Console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import paho.mqtt.client as mqtt

# Import các hàm bảo mật từ thư viện utils cục bộ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import verify_hmac, decrypt_data

def get_mqtt_client(username=None, password=None):
    try:
        from paho.mqtt.enums import CallbackAPIVersion
        client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    except ImportError:
        client = mqtt.Client()
        
    if username and password:
        client.username_pw_set(username, password)
    return client

def write_to_output_csv(data_dict, file_path):
    """
    Ghi dữ liệu cảm biến nhận được vào file CSV kết quả
    """
    file_exists = os.path.exists(file_path)
    # Lấy các trường dữ liệu tiêu chuẩn
    fieldnames = ["received_at", "timestamp", "device_id", "temperature", "humidity", "status", "integrity_verified"]
    
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        row = {
            "received_at": datetime.now().isoformat(),
            "timestamp": data_dict.get("timestamp", "N/A"),
            "device_id": data_dict.get("device_id", "N/A"),
            "temperature": data_dict.get("temperature", 0.0),
            "humidity": data_dict.get("humidity", 0.0),
            "status": data_dict.get("status", "N/A"),
            "integrity_verified": data_dict.get("integrity_verified", "N/A")
        }
        writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="MQTT Subscriber - Lắng nghe dữ liệu cảm biến IoT")
    parser.add_argument("--broker", default="test.mosquitto.org", help="Địa chỉ MQTT Broker (mặc định: test.mosquitto.org)")
    parser.add_argument("--port", type=int, default=1883, help="Cổng kết nối Broker (mặc định: 1883)")
    parser.add_argument("--mode", choices=["cleartext", "hmac", "encrypted"], default="cleartext", 
                        help="Chế độ bảo mật mong đợi của payload (cleartext / hmac / encrypted)")
    parser.add_argument("--topic", default="iot/sensor/data", help="MQTT Topic để đăng ký nhận tin")
    parser.add_argument("--username", default=None, help="Tên đăng nhập (nếu broker yêu cầu)")
    parser.add_argument("--password", default=None, help="Mật khẩu (nếu broker yêu cầu)")
    parser.add_argument("--simulate-attack", action="store_true", 
                        help="Giả lập cuộc tấn công sửa đổi gói tin trên đường truyền (để kiểm chứng tính toàn vẹn)")
    
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base_dir, "results", "logs")
    output_csv = os.path.join(base_dir, "results", "output.csv")
    
    os.makedirs(log_dir, exist_ok=True)
    
    # Xác định đường dẫn ghi log giao thức tương ứng
    if args.mode == "cleartext":
        log_file_path = os.path.join(log_dir, "cleartext_traffic.log")
    else:
        log_file_path = os.path.join(log_dir, "secure_traffic.log")
        
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"[+] Kết nối thành công! Đang subscribe tới topic: {args.topic}")
            client.subscribe(args.topic)
        else:
            print(f"[-] Kết nối thất bại, mã trả về: {rc}")
            
    def on_message(client, userdata, msg):
        raw_payload = msg.payload.decode('utf-8')
        received_time = datetime.now().isoformat()
        
        # Ghi nhận log giao thức thô (như kẻ nghe lén chụp được)
        with open(log_file_path, "a", encoding="utf-8") as lf:
            lf.write(f"[{received_time}] RAW PAYLOAD: {raw_payload}\n")
            
        print("\n" + "="*50)
        print(f"[*] Nhận bản tin mới lúc: {received_time}")
        print(f"[*] Raw payload chụp được từ đường truyền MQTT:\n{raw_payload}")
        print("="*50)
        
        # Biến để kiểm chứng tính toàn vẹn
        integrity_verified = "N/A"
        data_to_save = {}
        
        try:
            if args.mode == "cleartext":
                # Ở chế độ cleartext, bất kỳ ai nghe lén cũng đọc được dữ liệu trực tiếp
                data_to_save = json.loads(raw_payload)
                integrity_verified = "FALSE (Không có cơ chế bảo vệ tính toàn vẹn)"
                
                print("[!] CẢNH BÁO: Dữ liệu đang được truyền dưới dạng RÕ (Cleartext)!")
                print(f"[+] Thiết bị ID: {data_to_save.get('device_id')}")
                print(f"[+] Nhiệt độ: {data_to_save.get('temperature')}°C | Độ ẩm: {data_to_save.get('humidity')}%")
                
            elif args.mode == "hmac":
                payload_json = json.loads(raw_payload)
                data_block = payload_json.get("data", {})
                received_hmac = payload_json.get("hmac", "")
                
                # Biến đổi dữ liệu dạng chuỗi để xác thực
                data_str = json.dumps(data_block)
                
                # Giả lập cuộc tấn công sửa đổi gói tin nếu cờ --simulate-attack được bật
                if args.simulate_attack:
                    print("[!] Tấn công giả lập: Đang sửa đổi giá trị nhiệt độ trong gói tin...")
                    data_block["temperature"] = 99.9  # Sửa đổi giá trị
                    data_str = json.dumps(data_block)
                
                # Xác thực tính toàn vẹn
                if verify_hmac(data_str, received_hmac):
                    integrity_verified = "TRUE (Hợp lệ)"
                    print("[+] XÁC THỰC HMAC THÀNH CÔNG: Dữ liệu toàn vẹn và đúng nguồn gốc!")
                    data_to_save = data_block
                else:
                    integrity_verified = "FAILED (Bị sửa đổi!)"
                    print("[-] XÁC THỰC HMAC THẤT BẠI: Phát hiện dữ liệu đã bị sửa đổi trái phép trên đường truyền!")
                    data_to_save = data_block # Vẫn lưu nhưng đánh dấu bị lỗi toàn vẹn
                    
                print(f"[+] Thiết bị ID: {data_to_save.get('device_id')}")
                print(f"[+] Nhiệt độ: {data_to_save.get('temperature')}°C | Độ ẩm: {data_to_save.get('humidity')}%")
                
            elif args.mode == "encrypted":
                payload_json = json.loads(raw_payload)
                
                # Giả lập cuộc tấn công sửa đổi gói tin mã hóa
                if args.simulate_attack:
                    print("[!] Tấn công giả lập: Đang phá hoại chuỗi ciphertext mã hóa...")
                    payload_json["ciphertext"] = payload_json["ciphertext"][:-5] + "AAAAA"
                
                # Giải mã dữ liệu
                decrypted_data = decrypt_data(payload_json)
                integrity_verified = "TRUE (Hợp lệ và được bảo mật)"
                print("[+] GIẢI MÃ THÀNH CÔNG: Dữ liệu được bảo vệ an toàn (Confidentiality & Integrity)!")
                data_to_save = decrypted_data
                
                print(f"[+] Thiết bị ID: {data_to_save.get('device_id')}")
                print(f"[+] Nhiệt độ: {data_to_save.get('temperature')}°C | Độ ẩm: {data_to_save.get('humidity')}%")
                
        except Exception as e:
            if args.mode == "encrypted":
                integrity_verified = "FAILED (Không thể giải mã/Bị phá hoại)"
                print(f"[-] LỖI GIẢI MÃ: Kẻ tấn công đã sửa đổi gói tin hoặc khóa không đúng! Chi tiết: {e}")
            else:
                print(f"[-] Lỗi phân tích gói tin: {e}")
                
        # Lưu kết quả phân tích vào output.csv
        if data_to_save:
            data_to_save["integrity_verified"] = integrity_verified
            write_to_output_csv(data_to_save, output_csv)
            print(f"[*] Đã ghi nhận kết quả vào file: {output_csv}")

    # Cấu hình MQTT Client
    client = get_mqtt_client(args.username, args.password)
    
    # Đăng ký các hàm callback
    try:
        # Hỗ trợ cấu hình Paho MQTT v2 callbacks
        client.on_connect = on_connect
        client.on_message = on_message
    except Exception:
        # Fallback
        client.on_connect = on_connect
        client.on_message = on_message
        
    print(f"[*] Đang kết nối tới MQTT Broker {args.broker}:{args.port}...")
    try:
        client.connect(args.broker, args.port, 60)
    except Exception as e:
        print(f"[-] Kết nối thất bại: {e}")
        sys.exit(1)
        
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[*] Dừng subscriber.")
    finally:
        client.disconnect()
        print("[*] Đã ngắt kết nối.")

if __name__ == "__main__":
    main()
