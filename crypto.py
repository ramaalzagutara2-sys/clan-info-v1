from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# AES Keys
_API_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
_API_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

_dec = [
    '80','81','82','83','84','85','86','87','88','89','8a','8b','8c','8d','8e','8f',
    '90','91','92','93','94','95','96','97','98','99','9a','9b','9c','9d','9e','9f',
    'a0','a1','a2','a3','a4','a5','a6','a7','a8','a9','aa','ab','ac','ad','ae','af',
    'b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','ba','bb','bc','bd','be','bf',
    'c0','c1','c2','c3','c4','c5','c6','c7','c8','c9','ca','cb','cc','cd','ce','cf',
    'd0','d1','d2','d3','d4','d5','d6','d7','d8','d9','da','db','dc','dd','de','df',
    'e0','e1','e2','e3','e4','e5','e6','e7','e8','e9','ea','eb','ec','ed','ee','ef',
    'f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','fa','fb','fc','fd','fe','ff'
]
_xxx = [
    '1','01','02','03','04','05','06','07','08','09','0a','0b','0c','0d','0e','0f',
    '10','11','12','13','14','15','16','17','18','19','1a','1b','1c','1d','1e','1f',
    '20','21','22','23','24','25','26','27','28','29','2a','2b','2c','2d','2e','2f',
    '30','31','32','33','34','35','36','37','38','39','3a','3b','3c','3d','3e','3f',
    '40','41','42','43','44','45','46','47','48','49','4a','4b','4c','4d','4e','4f',
    '50','51','52','53','54','55','56','57','58','59','5a','5b','5c','5d','5e','5f',
    '60','61','62','63','64','65','66','67','68','69','6a','6b','6c','6d','6e','6f',
    '70','71','72','73','74','75','76','77','78','79','7a','7b','7c','7d','7e','7f'
]


def encrypt_api(plain_text: str) -> str:
    """Encrypt hex string using API AES-CBC key."""
    data = bytes.fromhex(plain_text)
    cipher = AES.new(_API_KEY, AES.MODE_CBC, _API_IV)
    return cipher.encrypt(pad(data, AES.block_size)).hex()


def decrypt_api(cipher_text: str) -> str:
    """Decrypt hex string using API AES-CBC key."""
    cipher = AES.new(_API_KEY, AES.MODE_CBC, _API_IV)
    return unpad(cipher.decrypt(bytes.fromhex(cipher_text)), AES.block_size).hex()


def Encrypt_ID(x: int) -> str:
    """Encode integer UID to protobuf-style varint hex."""
    x = int(x) / 128
    if x > 128:
        x /= 128
        if x > 128:
            x /= 128
            if x > 128:
                x /= 128
                strx = int(x)
                y = (x - strx) * 128
                z = (y - int(y)) * 128
                n = (z - int(z)) * 128
                m = (n - int(n)) * 128
                return _dec[int(m)] + _dec[int(n)] + _dec[int(z)] + _dec[int(y)] + _xxx[strx]
            else:
                strx = int(x)
                y = (x - strx) * 128
                z = (y - int(y)) * 128
                n = (z - int(z)) * 128
                return _dec[int(n)] + _dec[int(z)] + _dec[int(y)] + _xxx[strx]
        else:
            strx = int(x)
            y = (x - strx) * 128
            z = (y - int(y)) * 128
            return _dec[int(z)] + _dec[int(y)] + _xxx[strx]
    else:
        strx = int(x)
        if strx == 0:
            y = (x - strx) * 128
            return _xxx[int(y)]
        else:
            y = (x - strx) * 128
            return _dec[int(y)] + _xxx[strx]


def Encrypt_id_emote(uid: int) -> str:
    """Encode UID using protobuf varint encoding."""
    result = []
    while uid > 0:
        byte = uid & 0x7F
        uid >>= 7
        if uid > 0:
            byte |= 0x80
        result.append(byte)
    return bytes(result).hex()


def Decrypt_id_emote(uidd: str) -> int:
    """Decode protobuf varint encoded UID."""
    bytes_value = bytes.fromhex(uidd)
    r, shift = 0, 0
    for byte in bytes_value:
        r |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            break
        shift += 7
    return r
