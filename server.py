from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def get_instagram_user_id(username):
    try:
        url = f"https://www.instagram.com/{username}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            match = re.search(r'"profilePage_([0-9]+)"', response.text)
            if match:
                return match.group(1)
        return None
    except Exception as e:
        return None

@app.route("/get-id", methods=["GET"])
def get_id():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user_id = get_instagram_user_id(username)
    if user_id:
        return jsonify({"user_id": user_id})
    else:
        return jsonify({"error": "User ID not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
