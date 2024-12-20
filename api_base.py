from flask import Flask,request,jsonify,json,send_file
from capture_image_from_camera import *
from pymongo import MongoClient
from train_data import *
from flask_cors import CORS
import pandas as pd
# from threading import Thread
from main import *
from bson.json_util import dumps
from bson import json_util
from twilio.rest import Client
from flask_mail import Mail, Message
# from flask_socketio import SocketIO
# from authentication import *
from functools import wraps
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
# socketio = SocketIO(app)
# socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app)
#@@@@@@@@@@@@@@@@@@@@@@LOGIN@@@@@@@@@@@@@@@@@@@@@

# Secret key for encoding and decoding JWTs
app.config['SECRET_KEY'] = 'your_secret_key'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'msg': 'Token is missing'}), 401

        try:
            data = jwt.decode(token.split(" ")[1], app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'msg': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'msg': 'Invalid token'}), 401

        # Attach user information to the request for later use in the route
        request.user = data['email']

        return f(*args, **kwargs)

    return decorated_function

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         email = request.json.get('email')
#         password = request.json.get('password')
#         user = db.login.find_one({'email': email,'password':password})
#         print(user,'userisfdderd')
#         if user:
#             # if user and check_password_hash(user['password'], password):
#             return jsonify({
#                 'msg': 'Login successful'
#             })
#         else:
#             return jsonify({
#                 'msg': 'Invalid email or password'
#             })   
#     else:
#         return jsonify({
#             'msg':'method not allowed'
#         })
    

app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        user = db.login.find_one({'email': email, 'password': password})

        if user:
            # Generate JWT token
            token = jwt.encode({
                'email': email,
                'exp': datetime.utcnow() + timedelta(days=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'msg': 'Login successful',
                'token': token 
            })
        else:
            return jsonify({
                'msg': 'Invalid email or password'
            })
    else:
        return jsonify({
            'msg': 'Method not allowed'
        })
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
# cors = CORS(app, resources={r"/socket.io/*": {"origins": "http://localhost:3000/traindata"}})
# socketio = SocketIO(app, cors_allowed_origins="*")

client = MongoClient('localhost', 27017)
 
db = client.AttendanceSystem

#@@@ this api for capture data
@app.route('/capturing_data',methods=['POST','GET'])
def capturing():
    if request.method == 'POST':
        inp_fileName_id = request.form.get('validationCustom02')
        folderName = request.form.get('validationCustom01')
        print(folderName,'folderName')
        print(inp_fileName_id,'inp_fileName_id')
        capture_data(inp_fileName_id, folderName)
        print(folderName,'folderName')
        return jsonify({
            'msg':'foldername and filename successfull submitted'
        })
    
# is_camera_running = False

# New route to get camera release status
@app.route('/camera_release', methods=['POST','GET'])

def camera_release():
    global is_camera_running

    if request.method == 'POST':
        try:
            if not is_camera_running:
                main_code()  # Run the face recognition code only if the camera is not already running
                is_camera_running = True
        
                return jsonify({'message': 'Camera started successfully'})
            else:
                return jsonify({'message': 'Camera is already running'})
        except Exception as e:
            is_camera_running = False  # Set to False in case of an error
            return jsonify({'error': f'Error during face recognition: {str(e)}'}), 500







#@@@ this api for train data
@app.route('/train_data', methods=['POST', 'GET'])

def train():
    if request.method == 'POST':
        try:
            result_message = train_data()
            if result_message:
                return jsonify({"message": result_message})
            response_data = {'message': result_message}
            if response_data:
                return jsonify(response_data), 200
        
        except Exception as e:
            response_data = {'message': f"Error during training: {str(e)}"}
            return jsonify(response_data), 500

# socketio = SocketIO(app)

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')


# @app.route('/train_data', methods=['GET'])
# def train_data():
#     if request.method =='GET':
#         try:
#             training_data_folder = os.path.join(os.getcwd(), 'datafolder')

#             known_faces, known_labels = train_face_recognition(training_data_folder)

#             if known_faces and known_labels:
#                 with open("trained_data.pkl", "wb") as f:
#                     pickle.dump((known_faces, known_labels), f)
#                 print('Training successful')
#                 return jsonify({'message': 'Training successful.'}), 200
#             else:
#                 print('No training data available.')
#                 return jsonify({'error': 'No training data available.'}), 404

#         except Exception as e:
#             return jsonify({'error': f"Error during training: {str(e)}"}), 500
#     else:
#         print('methods not allowed')
#         return jsonify({
#             'msg':'methods not allowed'
#         })

#@get data api ##############
json_file_path = os.path.join(os.getcwd(),'employee_data.json')
# print(json_file_path,'json_file_path')
@app.route('/jsonData', methods=['GET', 'POST'])

def handle_json_data():
    if request.method == 'GET':
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                print(data)
                # df = pd.DataFrame(data)
                # print(df,'dfffff')  # Use pd.read_json(data) if data is in JSON format
                # return jsonify(df.to_dict(orient='records'))
                # data=pd.read_table(data)
                return jsonify(data)
        except FileNotFoundError:
            return jsonify({'error': 'File not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
#@@@ this api use for add detail of empoyee    
@app.route('/addEmployeeData', methods=['POST'])
def add_employee_data():
    if request.method=='POST':
        filename=request.json.get('filename')
        emp_name=request.json.get('emp_name')
        emp_id=request.json.get('emp_id')
        print(filename , emp_name , emp_id , 'hihhihihihh')
        if filename is not None:
            new_data = {
                filename + '_\\d+': {
                    'emp_name': emp_name,
                    'emp_id': emp_id
                }
            }

            try:
                with open(json_file_path, 'r') as file:
                    existing_data = json.load(file)
                existing_data.append(new_data)
                with open(json_file_path, 'w') as file:
                    json.dump(existing_data, file, indent=2)

                return jsonify({'message': 'New data added successfully'}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Invalid filename'}), 400

# @app.route('/update_jsonData', methods=['GET', 'POST'])
# def update_jsonData():
#     if request.method == 'POST':
#         try:
#             new_data = request.json
#             with open(json_file_path, 'w') as file:
#                 json.dump(new_data, file, indent=2)
#             return jsonify({'message': 'JSON file updated successfully'})
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# def start_recognition(camera_port, known_faces, known_labels, employee_data, attendance_file):
#     # The rest of the function remains unchanged
#     recognize_faces(camera_port, known_faces, known_labels, employee_data, attendance_file)

# API route for starting face recognition
@app.route('/start_recognition', methods=['POST'])

def start_recognition_api():
    main_code()
    return jsonify({'message': 'Face recognition started successfully'})

#@@ this api for download excel
@app.route('/download_excel', methods=['GET'])

def download_excel():
    try:
        excel_file_path = os.path.join(os.getcwd(), 'attendance.xlsx')

        if os.path.exists(excel_file_path):
            return send_file(excel_file_path, as_attachment=True)

        else:
            return "File not found", 404
    except Exception as e:
        return str(e), 500
    
@app.route('/employee_data', methods=['GET'])

def get_employee_data():
    try:
       agrr= [
                    {
                        '$project': {
                            '_id': 0, 
                            'name': 1, 
                            'Employee_ID': 1, 
                            'status': 1, 
                            'date': 1, 
                            'time': 1
                        }
                    }
                ]
       agdata=db.employee_data.aggregate(agrr)
       print(agdata,'agdata')
       if agdata:

            employee_data_list = list(agdata)

            df = pd.DataFrame(employee_data_list)

            print(df)
            return jsonify({'data': df.to_dict(orient='records')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    
# newapi forbrowser support camera 
import base64
from io import BytesIO
from PIL import Image
try:
    with open("trained_data.pkl", "rb") as f:
        known_faces, known_labels = pickle.load(f)
    print(f"Loaded {len(known_faces)} known faces.")
except FileNotFoundError:
    known_faces, known_labels = [], []
    print("No known faces loaded. Please train the model first.")


def process_image(image_data):
    try:
        # Decode the base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_bytes))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Perform face recognition
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        recognized_faces = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_labels[first_match_index]

            recognized_faces.append({'name': name, 'location': [top, right, bottom, left]})

        return recognized_faces

    except Exception as e:
        print(f"Error in process_image: {e}")
        raise


@app.route('/process-frame', methods=['POST'])
def process_frame():
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'message': 'No image data provided'}), 400

        # Debug log
        print("Image received for processing")

        # Process the image
        recognized_faces = process_image(data['image'])
        print(recognized_faces,'recognized_facesrecognized_facesrecognized_faces')
        # Return the result
        return jsonify({'recognized_faces': recognized_faces})

    except Exception as e:
        print(f"Error processing frame: {e}")
        return jsonify({'error': str(e)}), 500


    

if __name__==('__main__'):
    app.run(debug=True,port=8090)

