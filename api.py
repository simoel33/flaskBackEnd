from asyncio import tasks
from calendar import c

import sqlite3
from webbrowser import get
from flask import Flask, jsonify, request
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS,cross_origin


app = Flask(__name__)
api = Api(app)
#activation du CORS
CORS(app)

#la connexion avec la base de donnees
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('patients.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn


# la methode pour afficher tous les patients
def allpatients():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method =="GET":
        cursor = conn.execute("SELECT * FROM patients")
        patients = [
            dict(id=row[0],firstname=row[1],lastname=row[2],cin = row[3],dose1 = row[4] , dose2 = row[5], dose3= row[6] )
            for row in cursor.fetchall()
        ]
        if patients is not None:
            return jsonify(patients),200

# la methode pour Ajouter Un patients
def addPatient(firstname,lastname,cin,dose1,dose2,dose3):
        conn = db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO patients(firstname,lastname,cin,dose1,dose2,dose3) VALUES(?,?,?,?,?,? )"
        cursor.execute(sql,(firstname,lastname,cin,dose1,dose2,dose3))
        conn.commit()
        return {"message":"patients add successfully"},201

# la methode pour afficher un patient avec son CIN
def getPatientByCin(cin):
     conn = db_connection()
     cursor = conn.cursor()
     if request.method =="GET":
        cursor = conn.execute("SELECT * FROM patients WHERE cin = ?",(cin,))
        patients = [
            dict(id=row[0],firstname=row[1],lastname=row[2],cin = row[3],dose1 = row[4] , dose2 = row[5], dose3= row[6] )
            for row in cursor.fetchall()
        ]
     if patients is not None:
        return jsonify(patients),200

#Update Patien
def updatePatient(id,firstname,lastname,cin,dose1,dose2,dose3):
     conn = db_connection()
     cursor = conn.cursor()
     if request.method =="PUT":
        sql = "UPDATE  patients SET firstname=?, lastname=? , cin= ? , dose1=?,dose2=?, dose3=?  WHERE id = ?"
        cursor = conn.execute(sql,(firstname,lastname,cin,dose1,dose2,dose3,id))
        conn.commit()
     return {"message": "updated successfully"},200


    #la class patient qui contients les methodes HTTP et chaque methode il fait appel a une methode en haut
class Patient(Resource):
    # GET HTTP
    def get(self):
        
     return allpatients()
    #POST HTTP
    def post(self):
        data = request.get_json()       
        firstname = data["firstname"]
        lastname = data["lastname"]
        cin = data["cin"]
        dose1 = data["dose1"]
        dose2 = data["dose2"]
        dose3 = data["dose3"]
        return addPatient(firstname,lastname,cin,dose1,dose2,dose3),201
    #PUT HTTP
    def put(self):
        data = request.get_json()       
        firstname = data["firstname"]
        lastname = data["lastname"]
        cin = data["cin"]
        dose1 = data["dose1"]
        dose2 = data["dose2"]
        dose3 = data["dose3"]
        id = data["id"]
        return updatePatient(id,firstname,lastname,cin,dose1,dose2,dose3),200

    



def deletPatientById(cin):
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute("DELETE FROM patients WHERE cin = ?",(cin,))
    conn.commit()
    return {"Pmessage":"patient delted successfully"},204
        




class PatientOperations(Resource):
    def get(self,cin):
        print("id is ------------- "+str(cin))
        return getPatientByCin(cin)

    def delete(self,cin):
        return deletPatientById(cin)




        
    
api.add_resource(Patient,"/patients")
api.add_resource(PatientOperations,'/patients/<string:cin>')
if __name__ == '__main__':
    app.run(debug=True)