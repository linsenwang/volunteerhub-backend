# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# 假设这里的数据将保存在内存中，实际应用中可以存储在数据库中
form_data = []

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()  # 获取 JSON 数据
    form_data.append(data)  # 将数据保存到内存
    data['timestamp'] = time.time()
    print(data)
    with open('data.txt', 'a') as f:
        f.write(str(data) + '\n')
    return jsonify({"message": "Form submitted successfully", "data": data}), 200

@app.route('/api/card-data')
def get_card_data():
    print("Fetching card data...")  # 调试信息
    jobs = [
        {
            "title": "图书馆邮递员",
            "details": {
                "number_of_positions": 2,
                "working_hours": "周二和周五，上午8:25 - 11:25（每周至少有1个半天的工作时间）。",
                "location": "思明校区图书馆至翔安校区德旺图书馆。",
            },
            "url": "https://www.wjx.cn/vm/hN6BwE0.aspx#"
        },
        {
            "title": "古籍特藏与修复部",
            "details": {
                "number_of_positions": 2,
                "working_hours": "周一至周五，上午8:30 - 11:30，下午2:30 - 5:30（每周至少有2-3个半天的工作时间）。",
                "location": "思明校区图书馆古籍特藏与修复部。",
            },
            "url": "https://www.wjx.cn/vm/Q4YWhyN.aspx#"
        },
        {
            "title": "编目部",
            "details": {
                "number_of_positions": 1,
                "working_hours": "周一至周五，上午8:30 - 11:30，下午2:30 - 5:30（每周至少有2-3个半天的工作时间）。",
                "location": "思明校区图书馆编目部。",
            },
            "url": "https://www.wjx.cn/vm/Otb8PUQ.aspx#"
        },
        {
            "title": "研究资料部",
            "details": {
                "number_of_positions": 1,
                "working_hours": "周一至周五，上午8:30 - 11:30，下午3:00 - 6:00（每周至少有2-3个半天的工作时间）。",
                "location": "思明校区图书馆研究资料部。",
            },
            "url": "https://www.wjx.cn/vm/QfhRaGW.aspx#"
        },
        {
            "title": "德旺图书馆前台组助理",
            "details": {
                "number_of_positions": 2,
                "working_hours": "周一至周五 8:00-12:00丨14:30-18:00丨18:00-22:00；周六至周日 9:00-12:00丨14:30-18:00丨18:00-22:00（每周至少有2个半天的工作时间，其中工作日至少1个半天）。",
                "location": "翔安校区德旺图书馆。",
            },
        }
    ]

    return jsonify(jobs)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)



        # {
        #     "title": "编目部",
        #     "details": {
        #         "number_of_positions": 1,
        #         "working_hours": "周一至周五，上午8:30 - 11:30，下午2:30 - 5:30（每周至少有2-3个半天的工作时间）。",
        #         "location": "思明校区图书馆编目部。",
        #     },
        #     "url": "https://www.wjx.cn/vm/Otb8PUQ.aspx#"
        # },
        # {
        #     "title": "研究资料部",
        #     "details": {
        #         "number_of_positions": 1,
        #         "working_hours": "周一至周五，上午8:30 - 11:30，下午3:00 - 6:00（每周至少有2-3个半天的工作时间）。",
        #         "location": "思明校区图书馆研究资料部。",
        #     },
        #     "url": "https://www.wjx.cn/vm/QfhRaGW.aspx#"
        # },
        # {
        #     "title": "德旺图书馆前台组助理",
        #     "details": {
        #         "number_of_positions": 2,
        #         "working_hours": "周一至周五 8:00-12:00丨14:30-18:00丨18:00-22:00；周六至周日 9:00-12:00丨14:30-18:00丨18:00-22:00（每周至少有2个半天的工作时间，其中工作日至少1个半天）。",
        #         "location": "翔安校区德旺图书馆。",
        #     },
        #     "url": "https://www.wjx.cn/vm/QV0llnW.aspx"
        # },
        # {
        #     "title": "德旺图书馆活动组助理",
        #     "details": {
        #         "number_of_positions": 2,
        #         "working_hours": [
        #             {"position": "数学与智力玩具空间助理", "working_hours": "周三下午16:30-18:30，且每周至少另有1个半天的工作时间；"},
        #             {"position": "摄影助理", "working_hours": "周一至周日 9:00-12:00丨14:30-17:30丨18:00-22:00，不定时工作，一周至少有2个半天的工作时间。"}
        #         ],
        #         "location": "翔安校区德旺图书馆。",
        #     },
        #     "url": "https://www.wjx.cn/vm/QV0llnW.aspx"
        # },
        # {
        #     "title": "储存图书馆助理",
        #     "details": {
        #         "number_of_positions": 2,
        #         "working_hours": "周一至周五上午9:30-11:30、下午14:00-16:00（每周至少有3个半天的工作时间）。",
        #         "location": "翔安校区德旺图书馆储存图书馆。",
        #     },
        #     "url": "https://www.wjx.cn/vm/QV0llnW.aspx"
        # }