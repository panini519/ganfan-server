from flask import Flask, request, jsonify
from flask_cors import CORS
import csv, os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data.csv'

@app.route('/submit', methods=['POST'])
def submit():
    if request.is_json:
        data = request.get_json()
        name = data.get('princessName', '')
        with_me = data.get('withMe', '')
        food = data.get('food', '')
        locations = data.get('location', [])
        if isinstance(locations, str):
            locations = [locations]
    else:
        data = request.form
        name = data.get('princessName', '')
        with_me = data.get('withMe', '')
        food = data.get('food', '')
        locations = request.form.getlist('location')

    row = [name, with_me, food, ';'.join(locations)]
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, mode='a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['公主的名字', '是否一起吃', '吃什么', '吃哪里'])
        writer.writerow(row)

    return jsonify({"message": "你真棒！干饭成功 ✅"}), 200

@app.route('/', methods=['GET'])
def index():
    return '✅ 干饭后端在线，正在监听 POST /submit 🍚'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

@app.route('/view', methods=['GET'])
def view_data():
    if not os.path.isfile(DATA_FILE):
        return "<h2>暂无干饭数据～</h2>"

    with open(DATA_FILE, encoding='utf-8') as f:
        rows = list(csv.reader(f))

    if not rows:
        return "<h2>暂无干饭数据～</h2>"

    headers = rows[0]
    data_rows = rows[1:]

    table = "<table border='1' cellpadding='6' style='border-collapse: collapse;'>"
    table += "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead><tbody>"
    for row in data_rows:
        table += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    table += "</tbody></table>"

    return f"<h2>🍚 干饭数据展示</h2>{table}"
