import json
import httpx
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from modules import jwt_manager
from modules.crypto import encrypt_api, Encrypt_ID
from modules.utils import format_timestamp
from modules.proto import data_pb2, encode_id_clan_pb2

app = Flask(__name__)

###########FREE-FIRE-VERSION###########
FREEFIRE_VERSION = "ob48"

#############AES KEY/IV###############
_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])


@app.route('/get_clan_info', methods=['GET'])
async def get_clan_info():
    token = jwt_manager.get_token()
    if not token:
        return jsonify({"error": "JWT token is missing or invalid"}), 500

    clan_id = request.args.get('clan_id')
    if not clan_id:
        return jsonify({"error": "Clan ID is required"}), 400

    # Build protobuf payload
    my_data = encode_id_clan_pb2.MyData()
    my_data.field1 = int(clan_id)
    my_data.field2 = 1
    data_bytes = my_data.SerializeToString()

    # AES-CBC encrypt
    cipher = AES.new(_KEY, AES.MODE_CBC, _IV)
    encrypted = cipher.encrypt(pad(data_bytes, AES.block_size))
    encrypted_hex = ' '.join(f"{b:02X}" for b in encrypted)

    headers = {
        "Expect": "100-continue",
        "Authorization": f"Bearer {token}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": FREEFIRE_VERSION,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
        "Host": "clientbp.ggblueshark.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    url = "https://clientbp.ggblueshark.com/GetClanInfoByClanID"
    body = bytes.fromhex(encrypted_hex.replace(" ", ""))

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, data=body)

    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch data: {response.status_code}"}), response.status_code

    if not response.content:
        return jsonify({"error": "Empty response from server"}), 500

    msg = data_pb2.response()
    msg.ParseFromString(response.content)

    return jsonify({
        "id": msg.id,
        "clan_name": msg.special_code,
        "timestamp1": format_timestamp(msg.timestamp1),
        "value_a": msg.value_a,
        "status_code": msg.status_code,
        "sub_type": msg.sub_type,
        "version": msg.version,
        "level": msg.level,
        "flags": msg.flags,
        "welcome_message": msg.welcome_message,
        "region": msg.region,
        "json_metadata": msg.json_metadata,
        "big_numbers": msg.big_numbers,
        "balance": msg.balance,
        "score": msg.score,
        "upgrades": msg.upgrades,
        "achievements": msg.achievements,
        "total_playtime": msg.total_playtime,
        "energy": msg.energy,
        "rank": msg.rank,
        "xp": msg.xp,
        "timestamp2": format_timestamp(msg.timestamp2),
        "error_code": msg.error_code,
        "last_active": format_timestamp(msg.last_active),
        "guild_details": {
            "region": msg.guild_details.region,
            "clan_id": msg.guild_details.clan_id,
            "members_online": msg.guild_details.members_online,
            "total_members": msg.guild_details.total_members,
            "regional": msg.guild_details.regional,
            "reward_time": msg.guild_details.reward_time,
            "expire_time": msg.guild_details.expire_time
        }
    })


if __name__ == '__main__':
    jwt_manager.start_token_updater()
    app.run(host='0.0.0.0', port=5000)
