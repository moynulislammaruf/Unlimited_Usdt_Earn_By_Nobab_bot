from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

user_points = {}

@app.route('/api/claim', methods=['POST'])
def claim():
    data = request.json
    user = str(data.get("user_id", "guest"))
    user_points[user] = user_points.get(user, 0) + 5
    return jsonify(success=True, message=f"🎉 You now have {user_points[user]} points!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
