from flask import Blueprint, render_template,url_for, request, flash, redirect, url_for
# from .models import User
from flask import jsonify
# from werkzeug.security import generate_password_hash, check_password_hash
# from . import db   ##means from __init__.py import db
# from flask_login import login_user, login_required, logout_user, current_user
from .model import mongodb
from bson.objectid import ObjectId
import json
from collections import defaultdict, Counter
from . import mongo
from flask import flash
from flask import session
import datetime

extra = Blueprint('extra', __name__)
@extra.route('/topic', methods=['GET', 'POST'])
def topic():
    word = request.args.get('word')
    words=list(word)
    
    docs = []
    if session.get('selected_loc2',None):
        print("I'm Here")
        selected_locations=(session.get('selected_loc2',None))
        print("iiii",type(selected_locations))
        selected_parties = session.get('selected_parties', None)
        selected_parties = eval(selected_parties)
        selected_locations=eval(selected_locations)
        print(selected_locations)
        for party in selected_parties:
            pipeline = [
                {
                    "$match": {
                        "topics": {"$in": words},
                        "loc": selected_locations
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {"format": "%Y-%m", "date": "$time"}
                        },
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {
                        "_id": 1
                    }
                }
            ]
            if (party=='PMLN'):
                print("12")
                results = list(mongo.db.PMLN_data.aggregate(pipeline))
            elif(party=='PTI'):
                print("45")
                results2 = list(mongo.db.PTI_data.aggregate(pipeline))
        return render_template("topic.html",word=word, results=results,results2=results2)


    else:
        selected_locations=session.get('selected_locations',None)
        print(type(selected_locations))
    selected_parties = session.get('selected_parties', None)
    print(selected_locations)
    print(selected_parties)
    if selected_parties and selected_locations:
        for party in selected_parties:
            if party=='PMLN':
                if isinstance(selected_locations, str):
                    for doc in mongo.db.PMLN_data.find({"loc": selected_locations,"topics": {"$in": [word]}}):
                        docs.append(doc)
                else:
                    for loc in selected_locations:
                        print("For Loop")
                        for doc in mongo.db.PMLN_data.find({"loc": loc,"topics": {"$in": [word]}}):
                            docs.append(doc)
                        #print(doc)
            elif party=='PTI':
                if isinstance(selected_locations, str):
                    for doc in mongo.db.PTI_data.find({"loc": selected_locations,"topics": {"$in": [word]}}):
                        docs.append(doc)
                else:
                    for loc in selected_locations:
                        for doc in mongo.db.PTI_data.find({"loc": loc, "topics": {"$in": [word]}}):
                            docs.append(doc)
                        #print(doc)
    elif selected_parties and not selected_locations:
        for party in selected_parties:
            if party=='PMLN':
                for doc in mongo.db.PMLN_data.find({"topics": {"$in": [word]}}):
                    docs.append(doc)
                    #print(doc)
            elif party=='PTI':
                for doc in mongo.db.PTI_data.find({ "topics": {"$in": [word]}}):
                    docs.append(doc)
                    #print(doc)
    elif not selected_parties and selected_locations:
        for loc in selected_locations:
            for doc in mongo.db.PMLN_data.find({"loc": loc,"topics": {"$in": [word]}}):
                docs.append(doc)
                 #print(doc)
            for doc in mongo.db.PTI_data.find({ "loc": loc,"topics": {"$in": [word]}}):
                docs.append(doc)
                 #print(doc)
    else:
        for doc in mongo.db.PMLN_data.find({"topics": {"$in": [word]}}):
                docs.append(doc)
        for doc in mongo.db.PTI_data.find({ "topics": {"$in": [word]}}):
                docs.append(doc)
    return render_template("signup.html",word=word,docs=docs,selected_locations=selected_locations, selected_parties=selected_parties)
@extra.route('/ranges')
def get_data():
    print ("I'm Here..!")
    return render_template("range.html")

@extra.route('/range', methods=['POST'])
def get_datas():
    start_date = datetime.datetime.strptime(request.form['start_date'], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(request.form['end_date'], "%Y-%m-%d")
    print("Start Date:", start_date)
    print("End Date:", end_date)

    # Query MongoDB using the date range
    results = mongo.db.PTI_data.find({
        'time': {
            '$gte': start_date,
            '$lte': end_date
        }
    })

    # Convert the cursor object to a list of dictionaries
    data = list(results)

    print(data)
    return render_template("ranges.html", data=data)