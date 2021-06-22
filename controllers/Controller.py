from datetime import datetime, timedelta
import jwt


class Controller:
    def __init__(self):
        pass

    def signup(self,db,request, bcrypt, secret):
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
                if res.acknowledged:
                    time = datetime.utcnow() + timedelta(hours=24)
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
        return {'status': status, "message": message, "token": token}, code


    def login(self, db, request,secret,bcrypt):
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
                        time = datetime.utcnow() + timedelta(hours=24)
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
                        res_data['token'] = token
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
            return {'status': status, "data": res_data, "message": message}, code


    def logout(self):
        return {'status': 'logout passed'}, 200