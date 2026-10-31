from flask import Flask
import requests, threading, time, os
app = Flask(__name__)
TOKEN = "9187395283:AAHR_Veh2co_wkmOidYBHqv8GitDF4tnJUk"
API = f"https://api.telegram.org/bot{TOKEN}"
LIKE_API = "https://api-likee.vercel.app/like"
offset = 0
def send_likes(chat_id, uid):
    try:
        requests.post(f"{API}/sendMessage", data={"chat_id": chat_id, "text": f"ببعت ل {uid}..."}, timeout=10)
        r = requests.get(f"{LIKE_API}?uid={uid}&server_name=ME", timeout=60)
        j = r.json()
        msg = f"زودت! قبل:{j.get('LikesBefore')} بعد:{j.get('LikesAfter')} +{j.get('LikesGivenByAPI')}"
        requests.post(f"{API}/sendMessage", data={"chat_id": chat_id, "text": msg}, timeout=10)
    except Exception as e:
        requests.post(f"{API}/sendMessage", data={"chat_id": chat_id, "text": str(e)}, timeout=10)
def loop():
    global offset
    while True:
        try:
            res = requests.get(f"{API}/getUpdates?offset={offset}&timeout=20", timeout=25).json()
            for u in res.get("result", []):
                offset = u["update_id"]+1
                txt = u.get("message",{}).get("text","").strip()
                cid = u.get("message",{}).get("chat",{}).get("id")
                if not cid: continue
                if txt == "/start":
                    requests.post(f"{API}/sendMessage", data={"chat_id": cid, "text": "بوتك جاهز ابعت ID"}, timeout=10)
                elif txt.isdigit():
                    threading.Thread(target=send_likes, args=(cid, txt)).start()
        except: time.sleep(3)
@app.route('/')
def home(): return "Running"
threading.Thread(target=loop, daemon=True).start()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
