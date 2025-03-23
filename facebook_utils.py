import re
import requests

def load_cookie_from_file(path="facebook_cookie.txt") -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Cookie file not found.")
        return ""

def get_user_id(username: str) -> int | None:
    cookie = load_cookie_from_file()
    if not cookie:
        return None

    url = f"https://www.facebook.com/{username}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "cookie": cookie
    }

    response = requests.get(url, headers=headers)
    content = response.text

    pattern = fr'"userVanity":"{re.escape(username)}","userID":"(\d+)"'
    match = re.search(pattern, content)
    if match:
        return int(match.group(1))
    return None
