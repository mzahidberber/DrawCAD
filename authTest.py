
from Service import DrawService
from Service.AuthService import AuthService
import json
from datetime import datetime,timedelta, timezone
from Service.Model import Token

# auth=AuthService()
# a=auth.createUser("zahid3","zahid3@gmail.com","123456Aa")
# b=auth.createToken("zahid3@gmail.com","123456Aa")
# # print(a)
# # print(b.accessTokenExpiration)

# with open('user.json', 'w') as json_file:
#     json.dump(b.to_Dict(), json_file)
# token:Token

# with open('user.json') as f:
#     try:
#         veri=json.load(f)
#         print(veri)
#         token=Token(veri["accessToken"],veri["accessTokenExpiration"],veri["refreshToken"],veri["refreshTokenExpiration"])
        
#     except:
#         print("dosya boşş")

auth=AuthService("zahid@gmail.com","123456Aa")
asd=auth.userAndToken
print(asd.token.accessToken)

aut=AuthService("zahid@gmail.com","123456Aa")
print(aut.userAndToken.to_Dict())
# token1=auth.createToken("zahid@gmail.com","123456Aa")
# draw=DrawService(token1)

# draw.getLayerssss()


        