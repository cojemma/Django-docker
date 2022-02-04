import jwt
import datetime

class Jwt:
    def __init__(self, token=None):
        self.key = 'Srros12@@058Aa'
        self.token = token
    def encode(self, dic):
        payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)}
        for key in dic.keys():
            payload[key] = dic[key]
        print(payload)
        self.token = jwt.encode(payload, self.key)
        return self
    def decode(self):
        decode_jwt = None
        try:
            decode_jwt = jwt.decode(self.token, self.key, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            print('out of time')
        except jwt.InvalidTokenError:
            print('Invalid Token')
        return decode_jwt

jj = Jwt().encode({'username':'aaa'})
print(jj.token)
a = jj.decode()
print(a)