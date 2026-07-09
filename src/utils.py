import hmac
import hashlib
import json
import base64
import os

# Cố gắng import cryptography để mã hóa AES-GCM chuyên nghiệp.
# Nếu không có, sẽ báo lỗi để người dùng cài đặt (hoặc chúng ta sẽ tự cài đặt trong lab).
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False

# Khóa bí mật mặc định (Trong thực tế cần quản lý an toàn và không hardcode)
DEFAULT_HMAC_KEY = b"SuperSecretHMACKeyForIoTTopic27"
DEFAULT_AES_KEY = b"12345678901234567890123456789012" # 32 bytes = 256 bits

def calculate_hmac(message_str: str, key: bytes = DEFAULT_HMAC_KEY) -> str:
    """
    Tính toán mã băm HMAC-SHA256 để đảm bảo tính toàn vẹn.
    """
    message_bytes = message_str.encode('utf-8')
    hmac_obj = hmac.new(key, message_bytes, hashlib.sha256)
    return hmac_obj.hexdigest()

def verify_hmac(message_str: str, received_hmac: str, key: bytes = DEFAULT_HMAC_KEY) -> bool:
    """
    Xác thực mã băm HMAC-SHA256.
    """
    calculated = calculate_hmac(message_str, key)
    # So sánh an toàn chống tấn công timing attack
    return hmac.compare_digest(calculated, received_hmac)

def encrypt_data(data_dict: dict, key: bytes = DEFAULT_AES_KEY) -> dict:
    """
    Mã hóa dữ liệu JSON bằng AES-GCM-256.
    Trả về dict chứa iv, ciphertext và tag dưới dạng Base64.
    """
    if not HAS_CRYPTOGRAPHY:
        raise RuntimeError("Thư viện 'cryptography' chưa được cài đặt. Vui lòng cài đặt bằng lệnh: pip install cryptography")
    
    plaintext = json.dumps(data_dict).encode('utf-8')
    
    # AESGCM tự động sinh IV và đính kèm tag vào ciphertext ở cuối (16 bytes tag)
    aesgcm = AESGCM(key)
    iv = os.urandom(12) # IV cho GCM là 12 bytes
    ciphertext_with_tag = aesgcm.encrypt(iv, plaintext, None)
    
    # Tách ciphertext và tag (cryptography đóng gói tag ở cuối ciphertext)
    tag_size = 16
    ciphertext = ciphertext_with_tag[:-tag_size]
    tag = ciphertext_with_tag[-tag_size:]
    
    return {
        "iv": base64.b64encode(iv).decode('utf-8'),
        "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
        "tag": base64.b64encode(tag).decode('utf-8')
    }

def decrypt_data(encrypted_dict: dict, key: bytes = DEFAULT_AES_KEY) -> dict:
    """
    Giải mã dữ liệu AES-GCM-256 nhận được.
    Đầu vào là dict chứa iv, ciphertext và tag dưới dạng Base64.
    """
    if not HAS_CRYPTOGRAPHY:
        raise RuntimeError("Thư viện 'cryptography' chưa được cài đặt. Vui lòng cài đặt bằng lệnh: pip install cryptography")
    
    try:
        iv = base64.b64decode(encrypted_dict["iv"])
        ciphertext = base64.b64decode(encrypted_dict["ciphertext"])
        tag = base64.b64decode(encrypted_dict["tag"])
        
        # Ghép lại thành định dạng mà cryptography mong muốn
        ciphertext_with_tag = ciphertext + tag
        
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(iv, ciphertext_with_tag, None)
        return json.loads(plaintext.decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Giải mã thất bại hoặc dữ liệu đã bị sửa đổi trái phép! Chi tiết: {e}")
