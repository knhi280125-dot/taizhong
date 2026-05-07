from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='../templates')

# (1) Danh sách 10 giao lộ hay xảy ra tai nạn tại Đài Trung
# Dữ liệu phục vụ bài tập MIS
ROAD_DATA = [
    "西屯區：環中路與市政路口",
    "北區：中清路與五權路口",
    "北區：太原路與崇德路口",
    "烏日區：高鐵東路與高鐵五路口",
    "神岡區：中山路與大富路口",
    "北屯區：環中東路與太原路口",
    "太平區：市民大道與環中東路口",
    "神岡區：中山路與大洲路口",
    "西區：台灣大道與五權路口",
    "西屯區：台灣大道與黎明路口"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        # (2) Query API thời tiết (Sử dụng API của CWA Taiwan)
        # Em hãy thay 'YOUR_API_KEY' bằng mã API từ https://opendata.cwa.gov.tw/
        api_key = "YOUR_API_KEY" 
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&locationName={city}&elementName=Wx,PoP"
        
        try:
            res = requests.get(url).json()
            if res.get('success') == 'true' and res['records']['location']:
                loc = res['records']['location'][0]
                # Wx: Trạng thái thời tiết, PoP: Xác suất mưa
                wx = loc['weatherElement'][0]['time'][0]['parameter']['parameterName']
                pop = loc['weatherElement'][1]['time'][0]['parameter']['parameterName']
                weather_info = {"city": city, "wx": wx, "pop": pop}
            else:
                weather_info = {"error": "Không tìm thấy dữ liệu. Hãy nhập đúng tên (VD: 臺中市)."}
        except:
            weather_info = {"error": "Lỗi kết nối API hoặc sai API Key."}

    return render_template('index.html', roads=ROAD_DATA, weather=weather_info)

# Cần thiết cho Vercel
app.debug = True
