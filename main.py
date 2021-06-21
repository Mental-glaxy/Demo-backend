from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from functools import wraps
import jwt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/online-platform"
mongo = PyMongo(app)
db = mongo.db
bcrypt = Bcrypt(app)
secret = "ABOBA"


def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                jwt.decode(token, secret)
            except:
                return jsonify({"status": "fail", "message": "unauthorized"}), 401
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "fail", "message": "unauthorized"}), 401
    return decorated


@app.route("/")
def index():
    return "Backend is working!"


@app.route("/login", methods=["POST"])
def login():
    return "Login is working!"


@app.route("/register",  methods=["POST"])
def register():
    return "Register is working!"


@app.route("/logout",  methods=["POST"])
def logout():
    return "Logout is working!"


@app.route("/stats",  methods=["GET"])
@tokenReq
def get_stats():
    return "Статистика"


@app.route("/save-stats",  methods=["Post"])
@tokenReq
def get_stats():
    return "Статистика сохранена!"


@app.route("/account",  methods=["GET"])
@tokenReq
def get_info():
    return "Инфо об аккаунте"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

