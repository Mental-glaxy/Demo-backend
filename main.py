from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_cors import CORS
from flask_jwt  import JWT, jwt_required,current_identity
import controllers.Config as config
import controllers.Controller as ctrl
import jwt
controller = ctrl.Controller()
conf = config.Config()
app = Flask(__name__)
app.config["MONGO_URI"] = conf.data('mongo_url')
mongo = MongoClient('localhost', 27017)
db = mongo['online-platform']
bcrypt = Bcrypt(app)
secret = conf.data('secret')
CORS(app, resources={r"/*": {"origins": "*"}})


def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                jwt.decode(str(token), secret, algorithms="HS256")
            except:
                return {"status": "fail", "message": "unauthorized"}, 401
            return f(*args, **kwargs)
        else:
            return {"status": "fail", "message": "unauthorized"}, 401
    return decorated



@app.route("/")
def index():
    return "Backend is working!"

@app.route("/login", methods=["POST"])
def login():
    return controller.login(db,request,secret,bcrypt)


@app.route("/register",  methods=["POST"])
def register():
    return controller.signup(db,request,bcrypt,secret)


@app.route("/logout",  methods=["POST"])
def logout():
    return controller.logout()


@app.route("/stats",  methods=["GET"])
@tokenReq
def get_stats():
    return controller.stats(db)


@app.route("/save-stats",  methods=["Post"])
@tokenReq
def save_stats():
    return controller.save_stats(request, db)


@app.route("/account",  methods=["GET"])
@tokenReq
def get_info():
    return "Инфо об аккаунте"

app.run(host="0.0.0.0", port=5000,debug=True)

