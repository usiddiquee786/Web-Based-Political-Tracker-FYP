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

auth = Blueprint('auth', __name__)

# def analytic_h(selected_parties):
#     selected_parties=selected_parties
#     total_count = mongo.db.PTI_data.count_documents({})
#     print(total_count)
#     positive_count = mongo.db.PTI_data.count_documents({'sentiment': 'P'})
#     negative_count = mongo.db.PTI_data.count_documents({'sentiment': 'N'})
#     topics = [doc["topics"] for doc in mongo.db.PTI_data.find()]
#     total_count = mongo.db.PMLN_data.count_documents({})
#     print(total_count)
#     positive_count = mongo.db.PMLN_data.count_documents({'sentiment': 'P'})
#     negative_count = mongo.db.PMLN_data.count_documents({'sentiment': 'N'})
#     topics = [doc["topics"] for doc in mongo.db.PMLN_data.find()]
#     positive_percentage = positive_count/total_count * 100
#     negative_percentage = negative_count/total_count * 100
#     words = [word for topic in topics for word in topic]
#     word_freq = Counter(words)
#     sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
#     return render_template("analytics.html",sorted_word_freq=sorted_word_freq,positive_percentage=positive_percentage,negative_percentage=negative_percentage,selected_parties=selected_parties)
selected_locations=[]
selected_parties=[]

@auth.route('/analytics', methods=['GET', 'POST'])
def analytics():

    if request.method == 'POST':
        if session.get('selected_locations',None) or session.get('selected_parties'):
           session.clear()
        selected_locations = request.form.getlist('locations')
        selected_parties = request.form.getlist('parties')
        print("Im here", selected_locations)
        session['selected_locations'] = selected_locations
        session['selected_parties'] = selected_parties
        if not (selected_parties and selected_locations):
            print("I'm Here Party testing 1")
            # print(party)
            total_count = mongo.db.PMLN_data.count_documents({}) + mongo.db.PTI_data.count_documents({})
            positive_count = mongo.db.PMLN_data.count_documents({'sentiment': 'P'}) + mongo.db.PTI_data.count_documents({'sentiment': 'P'})
            negative_count = mongo.db.PMLN_data.count_documents({'sentiment': 'N'}) + mongo.db.PTI_data.count_documents({'sentiment': 'N'})
            topics = mongo.db.PMLN_data.distinct('topics') + mongo.db.PTI_data.distinct('topics')
            if selected_parties:
                party_counts = {'PMLN': mongo.db.PMLN_data, 'PTI': mongo.db.PTI_data}
                print("I'm Here Party testing 2")
                # print(party)
                total_count = sum(party_counts[party].count_documents({}) for party in selected_parties)
                positive_count = sum(party_counts[party].count_documents({'sentiment': 'P'}) for party in selected_parties)
                negative_count = sum(party_counts[party].count_documents({'sentiment': 'N'}) for party in selected_parties)
                topics = [doc["topics"] for party in selected_parties for doc in party_counts[party].find({})]
            elif selected_locations:
                party_counts = {'PMLN': mongo.db.PMLN_data, 'PTI': mongo.db.PTI_data}
                for party in party_counts:
                    print("I'm Here Party testing 3")
                    # print(party)
                    total_count += sum(party_counts[party].count_documents({'loc': loc}) for loc in selected_locations)
                    positive_count += sum(party_counts[party].count_documents({'loc': loc, 'sentiment': 'P'}) for loc in selected_locations)
                    negative_count += sum(party_counts[party].count_documents({'loc': loc, 'sentiment': 'N'}) for loc in selected_locations)
                    topics += [doc["topics"] for loc in selected_locations for doc in party_counts[party].find({'loc': loc})]
        else:
            
            party_counts = {'PMLN': mongo.db.PMLN_data, 'PTI': mongo.db.PTI_data}
            print("I'm Here Party testing 4")
            # print(party)
            total_count = sum(party_counts[party].count_documents({'loc': loc}) for party in selected_parties for loc in selected_locations)
            positive_count = sum(party_counts[party].count_documents({'loc': loc, 'sentiment': 'P'}) for party in selected_parties for loc in selected_locations)
            negative_count = sum(party_counts[party].count_documents({'loc': loc, 'sentiment': 'N'}) for party in selected_parties for loc in selected_locations)
            topics = [doc["topics"] for party in selected_parties for loc in selected_locations for doc in party_counts[party].find({'loc': loc})]
        if total_count==0:
            str2="Data Not Found"
            return render_template("record.html", selected_locations=selected_locations, selected_parties=selected_parties ,str2=str2)
        
        positive_percentage = positive_count/total_count * 100
        negative_percentage = negative_count/total_count * 100
        words = [word for topic in topics for word in topic]
        word_freq = Counter(words)
        sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
        return render_template("analytics.html",selected_locations=selected_locations, selected_parties=selected_parties,sorted_word_freq=sorted_word_freq,positive_percentage=positive_percentage,negative_percentage=negative_percentage)
    else:
        print("ahmad")
        selected_locations = request.args.get('loc')
        parties = request.args.get('parties')
        session['selected_loc2'] = selected_locations
        session['selected_parties'] = parties
        if selected_locations is not None and parties is not None:
            selected_locations=eval(selected_locations)
            selected_parties = eval(parties)
            print(selected_locations, selected_parties,"Done")
            total_count=0
            positive_count=0
            negative_count=0
            topics=[]
            for party in selected_parties:
                if (party == 'PMLN'):
                    total_count += mongo.db.PMLN_data.count_documents({'loc':selected_locations})
                    print(total_count)
                    positive_count += mongo.db.PMLN_data.count_documents({'loc':selected_locations,'sentiment': 'P'})
                    negative_count += mongo.db.PMLN_data.count_documents({'loc':selected_locations,'sentiment': 'N'})
                    topics.extend([doc["topics"] for doc in mongo.db.PMLN_data.find({'loc':selected_locations})])
                elif (party == 'PTI'):
                    total_count += mongo.db.PTI_data.count_documents({'loc':selected_locations})
                    print(total_count)
                    positive_count += mongo.db.PTI_data.count_documents({'loc':selected_locations,'sentiment': 'P'})
                    negative_count += mongo.db.PTI_data.count_documents({'loc':selected_locations,'sentiment': 'N'})
                    topics.extend([doc["topics"] for doc in mongo.db.PTI_data.find({'loc':selected_locations})])
            if total_count==0:
                str2="Data Not Found"
                return render_template("record.html", selected_locations=selected_locations, selected_parties=selected_parties,str2=str2)
            positive_percentage = positive_count/total_count * 100
            negative_percentage = negative_count/total_count * 100
            words = [word for topic in topics for word in topic]
            word_freq = Counter(words)
            sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
            # print (sorted_word_freq)
            return render_template("analytics.html",selected_locations=selected_locations, selected_parties=selected_parties,sorted_word_freq=sorted_word_freq,positive_percentage=positive_percentage,negative_percentage=negative_percentage)
        else:
            total_count=0
            positive_count=0
            negative_count=0
            topics=[]
            total_count = mongo.db.PTI_data.count_documents({})
            positive_count = mongo.db.PTI_data.count_documents({'sentiment': 'P'})
            negative_count = mongo.db.PTI_data.count_documents({'sentiment': 'N'})
            topics = [doc["topics"] for doc in mongo.db.PTI_data.find()]
            positive_percentage = positive_count/total_count * 100
            negative_percentage = negative_count/total_count * 100
            words = [word for topic in topics for word in topic]
            word_freq = Counter(words)
            sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
            return render_template("analytics.html", sorted_word_freq=sorted_word_freq,positive_percentage=positive_percentage,negative_percentage=negative_percentage)
        


# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


@auth.route('/testing', methods=['GET', 'POST'])
def testing():
    loc=[]
    docs = []
    word = request.args.get('word')
    # selected_parties = request.args.getlist('selected_parties')
    # selected_locations = request.args.getlist('selected_locations')
    if session.get('selected_loc2',None):
        print("I'm Here")
        selected_locations=(session.get('selected_loc2',None))
        print("iiii",type(selected_locations))
        selected_parties = session.get('selected_parties', None)
        selected_parties = eval(selected_parties)
        selected_locations=eval(selected_locations)
        print(selected_locations)
        print("HI",selected_parties)
        for party in selected_parties:
            if (party=='PMLN'):
                print("12")
                for doc in mongo.db.PMLN_data.find({"loc": selected_locations,"topics": {"$in": [word]}}):
                        docs.append(doc)
            elif(party=='PTI'):
                print("45")
                for doc in mongo.db.PTI_data.find({"loc": selected_locations,"topics": {"$in": [word]}}):
                        docs.append(doc)
        return render_template("signup.html",word=word,docs=docs,selected_locations=selected_locations, selected_parties=selected_parties)


    else:
        selected_locations=session.get('selected_locations',None)
        print(type(selected_locations))
    selected_parties = session.get('selected_parties', None)
    print(selected_locations)
    print(selected_parties)
    if selected_parties and selected_locations:
        for party in selected_parties:
            if party=='PMLN':
                print ("PMLN")
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
                print ("PMLN22")
                for doc in mongo.db.PMLN_data.find({"topics": {"$in": [word]}}):
                    docs.append(doc)
                    #print(doc)
            elif party=='PTI':
                for doc in mongo.db.PTI_data.find({ "topics": {"$in": [word]}}):
                    docs.append(doc)
                    #print(doc)
    elif not selected_parties and selected_locations:
        for loc in selected_locations:
            print ("PMLN3")
            for doc in mongo.db.PMLN_data.find({"loc": loc,"topics": {"$in": [word]}}):
                docs.append(doc)
                 #print(doc)
            for doc in mongo.db.PTI_data.find({ "loc": loc,"topics": {"$in": [word]}}):
                docs.append(doc)
                 #print(doc)
    else:
        print ("PMLN44")
        for doc in mongo.db.PMLN_data.find({"topics": {"$in": [word]}}):
                docs.append(doc)
        for doc in mongo.db.PTI_data.find({ "topics": {"$in": [word]}}):
                docs.append(doc)
    return render_template("signup.html",word=word,docs=docs,selected_locations=selected_locations, selected_parties=selected_parties)


@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    print("Umar")
    user = request.args.get('user')
    data=mongo.db.PTI_data.find_one({'User':user})
    if data:
        total_count = mongo.db.PTI_data.count_documents({'User':user})
        print(total_count)
        positive_count = mongo.db.PTI_data.count_documents({'User':user,'sentiment': 'P'})
        negative_count = mongo.db.PTI_data.count_documents({'User':user,'sentiment': 'N'})
        topics = [doc["topics"] for doc in mongo.db.PTI_data.find({'User':user})]
        positive_percentage = positive_count/total_count * 100
        negative_percentage = negative_count/total_count * 100
        words = [word for topic in topics for word in topic]
        word_freq = Counter(words)
        sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
        return render_template("profile.html",sorted_word_freq=sorted_word_freq,positive_percentage=positive_percentage,negative_percentage=negative_percentage,data=data)
    data=mongo.db.PMLN_data.find_one({'User':user})
    if data:
        total_count = mongo.db.PMLN_data.count_documents({'User':user})
        print(total_count)
        positive_count = mongo.db.PMLN_data.count_documents({'User':user,'sentiment': 'P'})
        negative_count = mongo.db.PMLN_data.count_documents({'User':user,'sentiment': 'N'})
        topics = [doc["topics"] for doc in mongo.db.PMLN_data.find({'User':user})]
        positive_percentage = positive_count/total_count * 100
        negative_percentage = negative_count/total_count * 100
        words = [word for topic in topics for word in topic]
        word_freq = Counter(words)
        sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
        return render_template("profile.html",sorted_word_freq=sorted_word_freq,positive_percentage=positive_percentage,negative_percentage=negative_percentage,data=data)
    
    
@auth.route('/partiesdata', methods=['GET', 'POST'])
def parties():
    print("Umar")
    selected_parties = request.args.getlist('selected_parties')
    selected_locations = request.args.getlist('selected_locations')
    id=request.args.get('id')
    data=mongo.db.PMLN_data.find_one({'_id': ObjectId(id)})
    if data:
        data2=mongo.db.PMLN_rply.find({'ref':data['ref']})
        Name=data['Name']
        return render_template("tweet.html" ,data=data,data2=data2, Name=Name)
    # data=mongo.db.PTI_data.find_one({'_id': ObjectId(id)})
    data = mongo.db.PTI_data.find_one({'_id': ObjectId(id)})
    if data:
        data2=mongo.db.PTI_rply.find({'ref':data['ref']})
        Name=data['Name']
        return render_template("tweet.html" ,data=data,data2=data2, Name=Name)
    
    # Name=data['Name']
    
    return render_template("tweet.html" ,data=data,data2=data2, Name=Name)
@auth.route('/profiletweets', methods=['GET', 'POST'])
def profiletweets():
    print("Umar")
    word=request.args.get('word')
    user=request.args.get('user')
    data=mongo.db.PMLN_data.find_one({'User': user})
    docs = []
    if data:
        for doc in mongo.db.PMLN_data.find({"User":user,"topics": {"$in": [word]}}):
            docs.append(doc)
            # print(doc)
        return render_template("signup.html",word=word,docs=docs)
    data=mongo.db.PTI_data.find_one({'User': user})
    if data:
        for doc in mongo.db.PTI_data.find({"User":user,"topics": {"$in": [word]}}):
            docs.append(doc)
            # print(doc)
        return render_template("signup.html",word=word,docs=docs)
@auth.route('/education', methods=['GET', 'POST'])
def education():
    docs = []
    count1=0
    count2=0
    count3=0
    count4=0
    pipeline = [
        {
            "$match": {
                "topics": {"$in": ["Education", "Learning", "School", "Teacher", "Student", "Classroom", "Curriculum", "Exam", "Test", "Degree", "Diploma", "College", "University", "Literacy", "Numeracy", "STEM", "Arts", "Humanities", "Vocational","education", "learning", "school", "teacher", "student", "classroom", "curriculum", "exam", "test", "degree", "diploma", "college", "university", "literacy", "numeracy", "stem", "arts", "humanities", "vocational"]}
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
    pipeline2 = [
        {
            "$match": {
                "topics": {
                    "$in": ["Education", "Learning", "School", "Teacher", "Student", "Classroom", "Curriculum", "Exam", "Test", "Degree", "Diploma", "College", "University", "Literacy", "Numeracy", "STEM", "Arts", "Humanities", "Vocational", "education", "learning", "school", "teacher", "student", "classroom", "curriculum", "exam", "test", "degree", "diploma", "college", "university", "literacy", "numeracy", "stem", "arts", "humanities", "vocational"]
                },
                "status": "v"
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
    results = list(mongo.db.PTI_data.aggregate(pipeline))
    results2=list(mongo.db.PMLN_data.aggregate(pipeline))
    resultsv = list(mongo.db.PTI_data.aggregate(pipeline2))
    resultsv2=list(mongo.db.PMLN_data.aggregate(pipeline2))
    print (results)
    for doc in mongo.db.PTI_data.find({"topics": {"$in": ["Education", "Learning", "School", "Teacher", "Student", "Classroom", "Curriculum", "Exam", "Test", "Degree", "Diploma", "College", "University", "Literacy", "Numeracy", "STEM", "Arts", "Humanities", "Vocational","education", "learning", "school", "teacher", "student", "classroom", "curriculum", "exam", "test", "degree", "diploma", "college", "university", "literacy", "numeracy", "stem", "arts", "humanities", "vocational"]}}):
        docs.append(doc)
        count1=count1+1
    for doc in mongo.db.PTI_data.find({"status": "v","topics": {"$in": ["Education", "Learning", "School", "Teacher", "Student", "Classroom", "Curriculum", "Exam", "Test", "Degree", "Diploma", "College", "University", "Literacy", "Numeracy", "STEM", "Arts", "Humanities", "Vocational","education", "learning", "school", "teacher", "student", "classroom", "curriculum", "exam", "test", "degree", "diploma", "college", "university", "literacy", "numeracy", "stem", "arts", "humanities", "vocational"]}}):
        docs.append(doc)
        count3=count3+1
    for doc in mongo.db.PMLN_data.find({"topics": {"$in": ["Education", "Learning", "School", "Teacher", "Student", "Classroom", "Curriculum", "Exam", "Test", "Degree", "Diploma", "College", "University", "Literacy", "Numeracy", "STEM", "Arts", "Humanities", "Vocational","education", "learning", "school", "teacher", "student", "classroom", "curriculum", "exam", "test", "degree", "diploma", "college", "university", "literacy", "numeracy", "stem", "arts", "humanities", "vocational"]}}):
        docs.append(doc)
        count2=count2+1
    for doc in mongo.db.PMLN_data.find({"status": "v","topics": {"$in": ["Education", "Learning", "School", "Teacher", "Student", "Classroom", "Curriculum", "Exam", "Test", "Degree", "Diploma", "College", "University", "Literacy", "Numeracy", "STEM", "Arts", "Humanities", "Vocational","education", "learning", "school", "teacher", "student", "classroom", "curriculum", "exam", "test", "degree", "diploma", "college", "university", "literacy", "numeracy", "stem", "arts", "humanities", "vocational"]}}):
        docs.append(doc)
        count4=count4+1
    return render_template("education.html",results=results,results2=results2,count1=count1,count2=count2,resultsv=resultsv,resultsv2=resultsv2,count3=count3,count4=count4)
@auth.route('/economics', methods=['GET', 'POST'])
def economics():
    
    list1=["Economic", "economic", "Economy", "economy", "GDP", "gdp", "Inflation", "inflation", "Deflation", "deflation", "Recession", "recession", "Recovery", "recovery", "Growth", "growth", "Trade", "trade", "Investment", "investment", "Stock", "stock", "Market", "market", "Consumer", "consumer", "Producer", "producer", "Price", "price", "Wage", "wage", "Salary", "salary", "Tax", "tax", "Budget", "budget", "Debt", "debt", "Wealth", "wealth", "Poverty", "poverty"]
    docs = []
    count1=0
    count2=0
    count3=0
    count4=0
    pipeline = [
        {
            "$match": {
                "topics": {"$in": list1}
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
    pipeline2 = [
        {
            "$match": {
                "topics": {
                    "$in": list1
                },
                "status": "v"
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
    results = list(mongo.db.PTI_data.aggregate(pipeline))
    results2=list(mongo.db.PMLN_data.aggregate(pipeline))
    resultsv = list(mongo.db.PTI_data.aggregate(pipeline2))
    resultsv2=list(mongo.db.PMLN_data.aggregate(pipeline2))
    print (results)
    for doc in mongo.db.PTI_data.find({"topics": {"$in": list1}}):
        docs.append(doc)
        count1=count1+1
    for doc in mongo.db.PTI_data.find({"status": "v","topics": {"$in": list1}}):
        docs.append(doc)
        count3=count3+1
    for doc in mongo.db.PMLN_data.find({"topics": {"$in": list1}}):
        docs.append(doc)
        count2=count2+1
    for doc in mongo.db.PMLN_data.find({"status": "v","topics": {"$in": list1}}):
        docs.append(doc)
        count4=count4+1
    return render_template("economics.html",results=results,results2=results2,count1=count1,count2=count2,resultsv=resultsv,resultsv2=resultsv2,count3=count3,count4=count4)
@auth.route('/health', methods=['GET', 'POST'])
def health():
    list1=["Health", "health", "Healthcare", "healthcare", "Medicine", "medicine", "Doctor", "doctor", "Nurse", "nurse", "Hospital", "hospital", "Clinic", "clinic", "Patient", "patient", "Illness", "illness", "Disease", "disease", "Infection", "infection", "Vaccination", "vaccination", "Immunization", "immunization", "Epidemic", "epidemic", "Pandemic", "pandemic", "Mental health", "mental health", "Physical health", "physical health", "Wellness", "wellness", "Fitness", "fitness", "Nutrition", "nutrition", "Diet", "diet", "Exercise", "exercise", "Addiction", "addiction", "Therapy", "therapy", "Treatment", "treatment", "Recovery", "recovery"]
    docs = []
    count1=0
    count2=0
    count3=0
    count4=0
    pipeline = [
        {
            "$match": {
                "topics": {
                    "$in": list1
                }
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
    pipeline2 = [
        {
            "$match": {
                "topics": {
                    "$in": list1
                },
                "status": "v"
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
    results = list(mongo.db.PTI_data.aggregate(pipeline))
    results2=list(mongo.db.PMLN_data.aggregate(pipeline))
    resultsv = list(mongo.db.PTI_data.aggregate(pipeline2))
    resultsv2=list(mongo.db.PMLN_data.aggregate(pipeline2))
    print (results)
    for doc in mongo.db.PTI_data.find({"topics": {"$in": list1}}):
        docs.append(doc)
        count1=count1+1
    for doc in mongo.db.PTI_data.find({"status": "v","topics": {"$in": list1}}):
        docs.append(doc)
        count3=count3+1
    for doc in mongo.db.PMLN_data.find({"topics": {"$in": list1}}):
        docs.append(doc)
        count2=count2+1
    for doc in mongo.db.PMLN_data.find({"status": "v","topics": {"$in": list1}}):
        docs.append(doc)
        count4=count4+1
    return render_template("health.html",results=results,results2=results2,count1=count1,count2=count2,resultsv=resultsv,resultsv2=resultsv2,count3=count3,count4=count4)
@auth.route('/poverty', methods=['GET', 'POST'])
def poverty():
    list1=["Poverty","poverty","hunger","Hunger","Homelessness","homelessness","Deprivation","deprivation","struggling","Struggling"]
    docs = []
    count1=0
    count2=0
    count3=0
    count4=0
    pipeline = [
        {
            "$match": {
                "topics": {
                    "$in": list1
                }
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
    pipeline2 = [
        {
            "$match": {
                "topics": {
                    "$in": list1
                },
                "status": "v"
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
    results = list(mongo.db.PTI_data.aggregate(pipeline))
    results2=list(mongo.db.PMLN_data.aggregate(pipeline))
    resultsv = list(mongo.db.PTI_data.aggregate(pipeline2))
    resultsv2=list(mongo.db.PMLN_data.aggregate(pipeline2))
    print (results)
    for doc in mongo.db.PTI_data.find({"topics": {"$in": list1}}):
        docs.append(doc)
        count1=count1+1
    for doc in mongo.db.PTI_data.find({"status": "v","topics": {"$in": list1}}):
        docs.append(doc)
        count3=count3+1
    for doc in mongo.db.PMLN_data.find({"topics": {"$in": list1}}):
        docs.append(doc)
        count2=count2+1
    for doc in mongo.db.PMLN_data.find({"status": "v","topics": {"$in": list1}}):
        docs.append(doc)
        count4=count4+1
    return render_template("poverty.html",results=results,results2=results2,count1=count1,count2=count2,resultsv=resultsv,resultsv2=resultsv2,count3=count3,count4=count4)
@auth.route('/parties', methods=['GET', 'POST'])
def partiess():
    print("umar")
    # selected_parties = json.loads(request.args.get('parties'))
    # print(selected_parties)
    n_ptimemberBAL=mongo.db.Pti_member.count_documents({"loc":"BAL"})
    n_pmlnmemberBAL=mongo.db.Pmln_member.count_documents({"loc":"BAL"})
    pti_tweetBAL=mongo.db.PTI_data.count_documents({"loc":"BAL"})
    pmln_tweetBAL=mongo.db.PMLN_data.count_documents({"loc":"BAL"})
    ##########
    n_ptimemberISL=mongo.db.Pti_member.count_documents({"loc":"ISL"})
    n_pmlnmemberISL=mongo.db.Pmln_member.count_documents({"loc":"ISL"})
    pti_tweetISL=mongo.db.PTI_data.count_documents({"loc":"ISL"})
    pmln_tweetISL=mongo.db.PMLN_data.count_documents({"loc":"ISL"})
    #######
    n_ptimemberSI=mongo.db.Pti_member.count_documents({"loc":"SI"})
    n_pmlnmemberSI=mongo.db.Pmln_member.count_documents({"loc":"SI"})
    pti_tweetSI=mongo.db.PTI_data.count_documents({"loc":"SI"})
    pmln_tweetSI=mongo.db.PMLN_data.count_documents({"loc":"SI"})
    ######
    n_ptimemberPJ=mongo.db.Pti_member.count_documents({"loc":"PJ"})
    n_pmlnmemberPJ=mongo.db.Pmln_member.count_documents({"loc":"PJ"})
    pti_tweetPJ=mongo.db.PTI_data.count_documents({"loc":"PJ"})
    pmln_tweetPJ=mongo.db.PMLN_data.count_documents({"loc":"PJ"})
    #####
    n_ptimemberKP=mongo.db.Pti_member.count_documents({"loc":"KP"})
    n_pmlnmemberKP=mongo.db.Pmln_member.count_documents({"loc":"KP"})
    pti_tweetKP=mongo.db.PTI_data.count_documents({"loc":"KP"})
    pmln_tweetKP=mongo.db.PMLN_data.count_documents({"loc":"KP"})
    response_data = {
        "n_ptimemberBAL": n_ptimemberBAL,
        "n_pmlnmemberBAL": n_pmlnmemberBAL,
        "pti_tweetBAL": pti_tweetBAL,
        "pmln_tweetBAL": pmln_tweetBAL,
        "n_ptimemberISL": n_ptimemberISL,
        "n_pmlnmemberISL": n_pmlnmemberISL,
        "pti_tweetISL": pti_tweetISL,
        "pmln_tweetISL": pmln_tweetISL,
        "n_ptimemberSI": n_ptimemberSI,
        "n_pmlnmemberSI": n_pmlnmemberSI,
        "pti_tweetSI": pti_tweetSI,
        "pmln_tweetSI": pmln_tweetSI,
        "n_ptimemberPJ": n_ptimemberPJ,
        "n_pmlnmemberPJ": n_pmlnmemberPJ,
        "pti_tweetPJ": pti_tweetPJ,
        "pmln_tweetPJ": pmln_tweetPJ,
        "n_ptimemberKP": n_ptimemberKP,
        "n_pmlnmemberKP": n_pmlnmemberKP,
        "pti_tweetKP": pti_tweetKP,
        "pmln_tweetKP": pmln_tweetKP,
    }
    return jsonify(response_data)


