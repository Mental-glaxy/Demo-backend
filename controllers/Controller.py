from datetime import datetime, timedelta
import jwt


class Controller:
    def __init__(self):
        pass

    def signup(self, db, request, bcrypt, secret):
        message = ""
        token = ""
        code = 500
        status = "fail"
        try:
            data = request.get_json()
            check = db['users'].find({"email": data['email']})
            if check.count() >= 1:
                message = "Пользователь с таким email уже существует!"
                code = 401
                status = "fail"
            else:
                # hashing the password so it's not stored in the db as it was
                data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                data['created'] = datetime.now()
                # this is bad practice since the data is not being checked before insert
                res = db["users"].insert_one(data)
                print(res)
                if res.acknowledged:
                    time = datetime.utcnow() + timedelta(days=365)
                    token = jwt.encode({
                        "user": {
                            "login": f"{data['login']}",
                            "email": f"{data['email']}",
                        },
                        "exp": time
                    }, secret)
                    status = "successful"
                    message = "user created successfully"
                    code = 201
        except Exception as ex:
            message = f"{ex}"
            status = "fail"
            code = 500
        return ({'status': status, "message": message, "token": token.decode('utf-8')}, code)

    def login(self, db, request, secret, bcrypt):
        message = ""
        res_data = {}
        code = 500
        status = "fail"
        try:
            data = request.get_json()
            user = db['users'].find_one({"login": f'{data["login"]}'})
            if user:
                user['_id'] = str(user['_id'])
                if user and bcrypt.check_password_hash(user['password'], data['password']):
                    time = datetime.utcnow() + timedelta(days=365)
                    token = jwt.encode({
                        "user": {
                            "login": f"{user['login']}",
                            "id": f"{user['_id']}",
                        },
                        "exp": time
                    }, secret)
                    del user['password']
                    message = f"user authenticated"
                    code = 200
                    status = "successful"
                    res_data['token'] = token.decode('utf-8')
                    res_data['user'] = user
                else:
                    message = "wrong password"
                    code = 401
                    status = "fail"
            else:
                message = "invalid login details"
                code = 401
                status = "fail"
        except Exception as ex:
            message = f"{ex}"
            code = 500
            status = "fail"
        return ({'status': status, "data": res_data, "message": message}, code)



    def logout(self):
        return {'status': 'logout passed'}, 200

    # Another functional

    def account(self, request,db):
        pass

    def stats(self, db):
        res = []
        code = 500
        status = "fail"
        message = ""
        try:
            for r in db['games'].find().sort("_id", -1):
                r['_id'] = str(r['_id'])
                res.append(r)
            if res:
                message = "games result loaded!"
                status = 'successful'
                code = 200
            else:
                message = "games result no available"
                status = 'successful'
                code = 200
        except Exception as ee:
            res = {"error": str(ee)}
        return {"status": status, 'data': res, "message": message}, code


    def save_stats(self, request, db):
        res = []
        code = 500
        status = "fail"
        message = ""
        try:
            res = db['games'].insert_one(request.get_json())
            if res.acknowledged:
                message = "Результат игры сохранен!"
                status = 'successful'
                code = 201
                res = {"_id": f"{res.inserted_id}"}
            else:
                message = "insert error"
                res = 'fail'
                code = 500
        except Exception as ee:
            res = {"error": str(ee)}
        return {"status": status, 'data': res, "message": message}, code