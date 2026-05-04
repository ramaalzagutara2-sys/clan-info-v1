import httpx
import asyncio
import threading
import time

_JWT_URL = (
    "https://projects-fox-x-get-jwt.vercel.app/get"
    "?uid=3763606630"
    "&password=7FF33285F290DDB97D9A31010DCAA10C2021A03F27C4188A2F6ABA418426527C"
)

_jwt_token: str | None = None


def get_token() -> str | None:
    return _jwt_token


async def _fetch_token():
    global _jwt_token
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(_JWT_URL)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    _jwt_token = data['token']
                    print("JWT Token updated successfully.")
                else:
                    print("JWT fetch failed: status not success.")
            else:
                print(f"JWT fetch failed: HTTP {response.status_code}")
    except httpx.RequestError as e:
        print(f"JWT request error: {e}")


def _updater_loop():
    """Background thread: refresh token every 8 hours."""
    while True:
        time.sleep(8 * 3600)
        asyncio.run(_fetch_token())


def start_token_updater():
    """Fetch token immediately, then start background updater thread."""
    asyncio.run(_fetch_token())
    t = threading.Thread(target=_updater_loop, daemon=True)
    t.start()
