# 使用中國 IP 進行批次 URL 狀態測試 Batch URL Status Testing Using China IPs
此代碼主要是透過使用中國代理IP進行批次網址檢測，主要用途可能是針對想確保自己網站是否有被劫持轉跳，或是想確認網址是否開啟正常返回200所使用。 <br>
The code uses Chinese proxy IPs to perform bulk URL tests. It helps detect possible hijacking or unwanted redirects and ensures that each URL responds correctly with HTTP 200. <br>
<br>
<br>
## | 🧰 需要用到的程式：
1. Windows Server (作業系統 Windows 的伺服器)
2. Flask (python呈現前端的架構)
3. python
4. requests (第三方模組，可以讓程式發送 HTTP 請求，程式能像瀏覽器一樣去連線網頁或 API)

## | 💡 代碼特別說明： <br>
1.get_proxy() <br>
  代碼中，是使用"熊貓代理IP ( xiongmaodaili.com ) "，但若不需要中國地區的IP，而是其他地區的IP，此部分也可以更換代理商。

2.熊貓代理IP API <br>
  這部分在 app.py 裡面是無法看到金鑰，金鑰訂單主要號碼，會存放在.env，避免對外曝光。
  
3.ip-api.com <br>
  這是用來查詢代理IP地區位置，為了顯示在前端，確保前端可以知道查詢當下的地區位置。
  ※這邊要特別注意，頻繁抓取，有可能服務氣IP位置也會被該查詢平台給阻擋，進而無法得知代理IP位置。

4.狀態碼分類  <br>
  | 狀態 | 狀態碼 | 最終目的地 | 代理IP位置 |
  |--------|--------|--------|--------|
  | ✅ 正常 | 200 | https://a.com | 使用代理 |
  | 🔀 轉跳 | 301/302 | https://b.com | 使用代理 |
  | 🚫 403 | 403 | - | 使用代理 |
  | ⚠️ 異常 | 403 | -| 使用代理 |
  | 🔌 連線中斷 | - | - | - |
  | ⌛ 請求超時 | - | - | - |
  | ❌ 其他錯誤 | - | - | - |

  ※出現連線中斷時，可以重新再發送新的IP重查詢一次，有時候是IP的問題。 <br>
 <br>
  5.Port ( app.run ) <br>
    端口設置，記得讓伺服器防火牆端口開放，不然也會無法正常開啟網頁。 <br>
 <br>
  6.域名指向 <br>
  正常你在設置的時候是 xxx.xxx.xxx.xxx:port 但如果要套上域名，因為網頁伺服器通常開放端口是80，你要額外把域名設置對應端口。 <br>
 <br>
  ## | 🪟 windows 環境設置：<br>
  1.前往( https://www.python.org/downloads/ ) 下載最新版本的python <br>
   <br>
  2.安裝時，記得勾選「 ✅ Add Python to PATH 」 <br>
  <br>
  3.安裝好，打開你本機的 PowerShell(cmd)，輸入以下指令，檢查是否有成功安裝。(如果顯示版本號，例如：Python 3.12.3，代表成功。) <br>
```powershell
python --version
```
  <br>
  4.建立你的專案資料夾 Flask ( 假設你的專案資料夾放置：C:\flask_project ) <br>
  <br>
  5.在 PowerShell(cmd) 輸入： <br>

```
C:\flask_project
```
```
cd C:\flask_project
```
 <br>
  6.建立虛擬環境，在 PowerShell(cmd) 輸入： ※以下都要在 cd C:\flask_project 下執行命令 <br>

```powershell
py -m venv .venv
```
 <br>
  7.啟用虛擬環境，在 PowerShell(cmd) 輸入： ※以下都要在 cd C:\flask_project 下執行命令 <br>

```powershell
.\.venv\Scripts\Activate.ps1
```
※若執行時出現錯誤，則可執行這行一次即可解決。

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
  ※如果看到 ```(.venv)``` 表示成功 <br>
 <br>
  8.升級 pip，在 PowerShell(cmd) 輸入： ※以下都要在 cd C:\flask_project 下執行命令 <br>
  
```powershell
python -m pip install --upgrade pip
```
 <br>
  9.安裝 Flask 與常用套件，在 PowerShell(cmd) 輸入： ※以下都要在 cd C:\flask_project 下執行命令 <br>
  
```powershell
pip install -r requirements.txt
```
 <br>
  10.啟動 Flask，在 PowerShell(cmd) 輸入： ※以下都要在 cd C:\flask_project 下執行命令 <br>
  
```powershell
python app.py
```
  ※或是點選目錄裡面的 run.bet ，那個是我寫好的啟動模式，像個開關點開讓他跑就好。 <br>
 <br>
  11.瀏覽器輸入：xxx.xxx.xxx.xxx:5000 (你的server IP位置) <br>
    ※如果你綁定域名，也可以改成 example.com:5000 (記得端口要去DNS更改一下) <br>


---


# 🌍 Flask URL Status Checker (China IP Support)

A Flask-based web application that performs **batch URL checks using Chinese proxy IPs**.  
This project helps you determine whether your website is accessible from China, detect hijacks or redirects, and verify if URLs return the correct status code (e.g. `200 OK`).

## 🧰 Required Programs
1. **Windows Server** – Windows-based server operating system  
2. **Flask** – Python web framework for rendering the frontend  
3. **Python** – the core programming language  
4. **Requests** – third-party library that allows your program to send HTTP requests (like a browser accessing web pages or APIs)

## 💡 Code Explanation

### 1️⃣ `get_proxy()`
Uses the **Xiongmao Proxy IP** service ([xiongmaodaili.com](https://xiongmaodaili.com)) to obtain Chinese proxy IPs.  
If you prefer other regions, you can replace it with a different proxy provider.

### 2️⃣ Xiongmao Proxy API Key
The proxy API key is **not shown in `app.py`** — it’s securely stored in a `.env` file to avoid exposing credentials publicly.

### 3️⃣ `ip-api.com`
This external API checks the **geographical location** of each proxy IP.  
It’s used for displaying region information on the frontend.  
⚠️ Frequent queries may cause your IP to be temporarily blocked by `ip-api.com`.

### 4️⃣ HTTP Status Code Classification
| Status | Code | Final Destination | Proxy IP Location |
|--------|------|------------------|-------------------|
| ✅ Normal | 200 | https://a.com | Using proxy |
| 🔀 Redirect | 301 / 302 | https://b.com | Using proxy |
| 🚫 Forbidden | 403 | – | Using proxy |
| ⚠️ Error | 403 | – | Using proxy |
| 🔌 Connection Error | – | – | – |
| ⌛ Timeout | – | – | – |
| ❌ Other Errors | – | – | – |

💡 If a connection error occurs, retry with a new proxy IP — sometimes the issue is with the proxy itself.

### 5️⃣ Port Configuration (`app.run`)
When setting the Flask port (e.g., `5000`), make sure your **Windows firewall allows inbound traffic** on that port, otherwise the website won’t load.

### 6️⃣ Domain Binding
By default, you access your app via `xxx.xxx.xxx.xxx:port`.  
If you use a **domain name**, note that most web servers open port **80**,  
so you must configure your domain to map to the same port (e.g., `5000`).

## 🪟 Windows Environment Setup

### 1️⃣ Install Python
Download the latest version from:  
👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

During installation, **check the box**:
```
✅ Add Python to PATH
```

### 2️⃣ Verify Installation
Open **PowerShell** (or CMD) and run:
```powershell
python --version
```
If you see a version (e.g., `Python 3.12.3`), installation succeeded.

### 3️⃣ Create Your Project Folder
Example:
```
C:\flask_project
```

### 4️⃣ Navigate to Your Folder
```powershell
cd C:\flask_project
```

### 5️⃣ Create a Virtual Environment
```powershell
py -m venv .venv
```

### 6️⃣ Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```
If you see `(.venv)` in your terminal, activation was successful.  
If you get a PowerShell error, run this once:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 7️⃣ Upgrade pip
```powershell
python -m pip install --upgrade pip
```

### 8️⃣ Install Flask and Dependencies
If you have a `requirements.txt` file:
```powershell
pip install -r requirements.txt
```
Otherwise, manually install:
```powershell
pip install flask requests python-dotenv waitress
```

### 9️⃣ Start Flask
```powershell
python app.py
```
Alternatively, double-click the `run.bat` file (if included).  
It works like a one-click startup switch.

### 🔗 10️⃣ Open in Browser
Visit:
```
http://xxx.xxx.xxx.xxx:5000
```
(Replace `xxx.xxx.xxx.xxx` with your server IP.)

If you’ve set up a domain, you can use:
```
http://example.com:5000
```
Make sure your DNS record points to your server IP and that port `5000` is open.

## ⚙️ Notes

- If using port `5000`, ensure it’s open in the **Windows firewall**:
```powershell
New-NetFirewallRule -DisplayName "Flask 5000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000
```

- For production environments, consider using **Waitress** or **IIS reverse proxy** to handle incoming requests on standard ports (80/443).

### ✨ Example Startup Code (`app.py`)
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Flask Server Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Make sure port 5000 is open on your server
```

## 🧩 Summary

| Step | Command | Description |
|------|----------|-------------|
| 1 | `cd C:\flask_project` | Go to project folder |
| 2 | `py -m venv .venv` | Create virtual environment |
| 3 | `.\.venv\Scripts\Activate.ps1` | Activate environment |
| 4 | `pip install -r requirements.txt` | Install dependencies |
| 5 | `python app.py` | Run Flask server |

### 💬 Example Access
```
http://yourIP:5000
```
or  
```
http://yourdomain.com:5000
```
<br>
Author: Ebay Kuo<br>
License: MIT<br>
Last Updated: 2025<br>



