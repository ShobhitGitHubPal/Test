# from twilio.rest import Client
# from flask_mail import Mail, Message
# # from flask_socketio import SocketIO
# # from authentication import *
# from functools import wraps
# from flask_cors import CORS
# ########@@@@@@@@@@@@@@@@@@
# CORS(app)

# app.config['ACCOUNT_SID'] = 'AC5f88040e6854cb8c340f77e38e03970d',
# app.config['ACCESS_KEY'] = 'f539a994081b7ca5e327827c48bf1b15',
# app.config['TWILIO_PHONE_NUMBER'] = "+12565888672"

# message_service = Client(
#     'AC5f88040e6854cb8c340f77e38e03970d', 'f539a994081b7ca5e327827c48bf1b15')
# #@@@@@@@
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'shobhit.pal@fourbrick.com'
# app.config['MAIL_PASSWORD'] = 'qdve zeva rvuc iecp'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# mail = Mail(app)
# ######################## tokenization #######################################################################
# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):

#         token = None
#         if "Authorization" in request.headers:
#             token = request.headers["Authorization"].split(" ")[-1]
#             # print(token,"dasgfhgfsahgdfsahgd")

#         if not token:
#             return jsonify({"message": " valid token is missing", 'status': 400})

#         try:
#             data = jwt.decode(
#                 token,
#                 algorithms="HS512",
#                 key="GameDev",
#             )
#             # print("dsifhsdkuhfkusdhfkuhsd", data)

#             aggr = [
#                 {
#                     '$match': {
#                         '_id': ObjectId(data['userId'])
#                     }
#                 }, {
#                     '$addFields': {
#                         '_id': {
#                             '$toString': '$_id'
#                         }
#                     }
#                 }
#             ]

#             current_user = list(signup_data.aggregate(aggr))

#             database_data = len(current_user)

#             if database_data == 0:
#                 return jsonify({"message": "no data", 'status': 400})

#         except Exception as e:
#             return jsonify({"message": "Token is invalid", 'status': 400})
#         return f(current_user[0], *args, **kwargs)

#     return decorator
# ############################# stop tokenization ##########################################
# @app.route("/signup", methods=['POST'])
# def signup():
#     if request.method == "POST":
#         email = request.form.get("email")
#         # username = request.form.get('username')
#         # password = request.form.get("password")
#         # verify_password = request.form.get("verify_password")
#         # receive_update_email = request.form.get("receive_update_email")
#         # if password == verify_password:
#         email_exist = signup_data.find_one({"email": email})
#         # phone_exist = signup_data.find_one({"mobile":mobile})

#         if email_exist:
#             return jsonify({"message": "Email is already exist", 'status': 400})
#         # if phone_exist:
#         #     return jsonify({"message":"Phone no. is already exist",'status':400})
#         otp = random.randint(1000, 9999)
#         try:
#             msg = Message("OTP for Registration",
#                           sender='shohit.pal@fourbrick.com', recipients=[email])
#             msg.body = f"Your OTP for registration is: {otp}"
#             mail.send(msg)
#             print(otp, 'otp')
#             custom_id = ObjectId()

#             # Insert data with the same _id
#             data = {
#                 "_id": custom_id,
#                 "email": email,
#                 "OTP": otp,
#                 "verified": False,
#             }
#             signup_data.insert_one(data)
#             return jsonify({'message': 'otp send successfully', 'status': 200})

#         except Exception as e:
#             print(e)
#             return jsonify({"message": "Error sending OTP.", 'status': 400}), 500

# ####################### verify otp #########################################################################################


# @app.route("/verify", methods=['POST'])
# def verify():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         print(email, 'email')
#         input_otp = request.form.get('input_otp')
#         print(input_otp, 'input_otp')
#         user_data = signup_data.find_one({"email": email})
#         print(user_data, 'user_data')
#         stored_otp = user_data.get("OTP") if user_data else None
#         print(stored_otp)

#         if email and stored_otp:
#             if stored_otp is not None and input_otp == str(stored_otp):
#                 # Use the same _id for the verify operation
#                 custom_id = user_data.get("_id")
#                 print(custom_id, 'custom_id')
#                 # Update the document with the same _id
#                 data = {
#                     "username": request.form.get('username'),
#                     "email": email,
#                     'input_otp': input_otp,
#                     "password": request.form.get("password"),
#                     "verify_password": request.form.get("verify_password"),
#                     "receive_update_email": request.form.get("receive_update_email") == 'on',
#                     "verified": True,
#                 }
#                 print(data, 'dddd')
#                 print(signup_data.update_one(
#                     {"_id": custom_id}, {"$set": data}), 'kkjjj')

#                 return jsonify({"message": "OTP verification successful.", 'status': 200})
#             else:
#                 return jsonify({"message": "Invalid OTP.", 'status': 400})
#         else:
#             return jsonify({
#                 'message': 'Email or OTP is invalid', 'status': 400
#             })
#     else:
#         return jsonify({
#             'message': 'Invalid request', 'status': 400
#         })


# ###############################################################################################################################
#     #################### login ################################################################################################################
# @app.route("/login", methods=['POST'])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")

#         user_data = signup_data.find_one(
#             {"email": email, 'password': password})
#         print(user_data)
#         if user_data:
#             if user_data['verified']:

#                 if str(user_data['password']) == str(password):
#                     user_data['_id'] = str(user_data['_id'])
#                     del user_data['password']
#                     access_token = jwt.encode(
#                         {
#                             "userDetails": user_data, "userId": user_data["_id"]
#                         },
#                         key="GameDev",
#                         algorithm="HS512",
#                     )
#                     response = make_response(
#                         jsonify({"token": access_token, "user": user_data})
#                     )
#                     response.set_cookie(
#                         "token",
#                         access_token,
#                         # secure=True,
#                         httponly=True,
#                         samesite=None,

#                     )
#                     data = jwt.decode(
#                         access_token,
#                         algorithms="HS512",
#                         key="GameDev",
#                     )
#                     return jsonify({"message": "Login successful.", "token": access_token, "token_Data": data, 'status': 200})

#             else:
#                 return jsonify({"message": "User Not Verified.", 'status': 400})
#         else:
#             return jsonify({"message": "Email or Password wrong...", 'status': 400})

#     else:
#         return jsonify({"message": "Email not found. Please register first.", 'status': 400})


# ################## location ##########################################################