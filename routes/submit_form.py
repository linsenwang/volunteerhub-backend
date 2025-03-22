from flask import Flask, request, jsonify
import time

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()  # 获取 JSON 数据
    data['timestamp'] = time.time()
    print(data)
    with open('data.txt', 'a') as f:
        f.write(str(data) + '\n')
    return jsonify({"message": "Form submitted successfully", "data": data}), 200