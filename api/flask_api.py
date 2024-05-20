from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
import json
import sys
import requests
from time import time
from urllib.parse import urlparse
from flask import Flask, jsonify, request
from flask import Flask, render_template
import mysql.connector
import os
app = Flask(__name__)

def connect_db(host, name, user, password):
    db_connection = mysql.connector.connect(
        host = host,
        user = user,
        database = name,
        passwd = password
    )
    mycursor = db_connection.cursor()
    # mycursor.execute("DROP TABLE IF EXISTS devices")
    # mycursor.execute("CREATE TABLE IF NOT EXISTS devices (devIndex INT , devID VARCHAR(255) , name VARCHAR(255), token VARCHAR(255) )")
    mycursor.execute("CREATE TABLE IF NOT EXISTS vehicles (Id INT AUTO_INCREMENT PRIMARY KEY, vehicleId INT ,all_passengers INT, type_vehicle VARCHAR(200))")
    # mycursor = db_connection.cursor()
    # logging.debug("Database connected:{}".format(db_connection))
    return db_connection

my_db = connect_db("localhost", "smartcity", "root", "")

@app.route('/count', methods = ['POST'])
def add_person() :
    values = request.get_json()
    ID = values.get('ID')
    Direction = values.get('Direction')
    camId = values.get('camId')
    Round = values.get('Round')
    if Direction=="UL"| Direction=="UR":
        sql = "INSERT INTO vehicles (ID, Direction, camId, Round) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        value = (ID, Direction, camId, Round)
        mycursor = my_db.cursor()
        mycursor.execute(sql, value)
        my_db.commit()
    elif Direction=="DL"|Direction=="DR":
        sql = "DELETE FROM `vehicles` WHERE `ID`=%s"
        value = (ID, Direction, camId, Round)
        mycursor = my_db.cursor()
        mycursor.execute(sql, value)
        my_db.commit()
    response = {
        'message' : 'people updated',
        'body' : values
    }
    return jsonify(response), 200 


@app.route('/show', methods = ['GET'])
def show_counter():
    values = request.get_json()

    sql ="SELECT `Direction` FROM `vehicles` WHERE 1"
    mycursor = my_db.cursor()
    mycursor.execute(sql)
    my_db.commit()
    return render_template('Front-end/home.html')
    
if __name__=="__main__": 
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    #app.run(debug='False')