from flask import Flask,request,jsonify,json,send_file
from pymongo import MongoClient
from flask_cors import CORS
import pandas as pd
from threading import Thread
client = MongoClient('localhost', 27017)

db = client.AttendanceSystem