from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/online-platform"
mongo = PyMongo(app)
db = mongo.db


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

