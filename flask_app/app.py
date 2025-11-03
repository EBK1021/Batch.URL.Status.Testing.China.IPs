from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_proxy():
    secret = os.getenv("PANDA_API_SECRET")
    order_no = os.getenv("PANDA_ORDER_NO")

    if not secret or not order_no:
        return None, "未設定代理金鑰"

    api_url = (
        f"http://www.xiongmaodaili.com/xiongmao-web/api/glip?"      #這裡使用的是熊貓代理xiongmaodaili.com
        f"secret={secret}&orderNo={order_no}&count=1&isTxt=1&proxyType=1&returnAccount=1"       #API避免金鑰外洩，隱藏主要訂單號碼。
    )

    try:
        res = requests.get(api_url, timeout=5)
        proxy_ip = res.text.strip()

        if ":" in proxy_ip:
            ip_only = proxy_ip.split(":")[0]

            # 查詢 IP 位置（使用 ip-api.com）
            try:
                ipinfo = requests.get(f"http://ip-api.com/json/{ip_only}", timeout=3).json()
                location = f"{ipinfo.get('country', '')}, {ipinfo.get('regionName', '')}, {ipinfo.get('city', '')}"
            except:
                location = "無法取得位置"

            proxies = {
                "http": f"http://{proxy_ip}",
                "https": f"http://{proxy_ip}"
            }

            return proxies, f"（{location}）"

    except:
        return None, "代理請求失敗"

    return None, "無法取得代理"

def check_url_status(url, follow_redirects=True):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com"
    }

    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        session.mount("https://", requests.adapters.HTTPAdapter(max_retries=1))

        proxies, proxy_location = get_proxy()

        response = session.get(url, timeout=5, allow_redirects=follow_redirects, proxies=proxies)

        status = response.status_code
        final_url = response.url

        if status == 200:
            return f"✅ 正常 (狀態碼: {status})，最終網址: {final_url}，🌐 使用代理：{proxy_location}"
        elif status in [301, 302]:
            redirect_url = response.headers.get("Location", "未知")
            return f"🔀 轉跳 (狀態碼: {status})，轉跳至: {redirect_url}，🌐 使用代理：{proxy_location}"
        elif status == 403:
            return f"🚫 403 禁止存取，可能需要特定 IP 或額外驗證，🌐 使用代理：{proxy_location}"
        else:
            return f"⚠️ 異常 (狀態碼: {status})，🌐 使用代理：{proxy_location}"

    except requests.exceptions.ConnectionError as e:
        return f"🔌 連線中斷（※可單獨重新檢測該網址）：{str(e)}"
    except requests.exceptions.Timeout:
        return "⌛ 請求超時，伺服器無回應"
    except requests.exceptions.RequestException as e:
        return f"❌ 其他錯誤：{str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
   
   #這裡主要可以放置默認的查詢網址，網址需帶上http or https，以及最後不可以有斜線"/"
    urls = [
        "https://A.com",
        "https://www.B.com"
    ]

    if request.method == "POST":
        urls = request.form.get("urls").split("\n")
        urls = [url.strip() for url in urls if url.strip()]
        follow_redirects = request.form.get("follow_redirects") == "on"
        result = {url: check_url_status(url, follow_redirects) for url in urls}

    return render_template("index.html", result=result, urls="\n".join(urls))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) #記得要在Server開放指定端口
