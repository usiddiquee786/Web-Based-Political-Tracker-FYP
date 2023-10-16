import pymongo


class mongodb():
    client= pymongo.MongoClient("mongodb://localhost:27017/")
    db=client['tweets']
    collection1=db['PTI_data']
    collection2=db['PTI_rply'] 
    collection3=db['PMLN_data']
    collection4=db['PMLN_rply']
    c1column=['user','rply_text', 'ref','lan','sentiment']
    c2column = ['Time', 'Name','User','loc','status', 'Tweet','fav','retweet','ref','lan','sentiment','topics']
