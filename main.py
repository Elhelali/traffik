from flask import Flask,jsonify,request,render_template,make_response
from decorators import mongo
import requests,string,random
import json
from user.routes import user
from datetime import datetime
import time
import pytz

#random.uniform(0.001,-0.001) add this to longitude an dlatitude

app = Flask(__name__)
app.register_blueprint(user)

@app.route('/')
def intro():
    return render_template("map.html")

@app.route('/data/traffic.json/<fr0m>/<to>/<country>/')
@app.route('/data/traffic.json/<fr0m>/<to>/<country>/<region>')
@mongo
def traffic_json(db,duration=-300,fr0m=0,to=time.time(),country="",region=""):

    fr0m = fr0m[:-3]+"."+fr0m[-3:]
    to = to[:-3]+"."+to[-3:]
    fr0m =datetime.fromtimestamp(float(fr0m)).astimezone(pytz.utc)
    to = datetime.fromtimestamp(float(to)).astimezone(pytz.utc)
    print(fr0m)
    print(to)
    d = db['traffic'].find({"requests": {"$elemMatch": {"timestamp": {"$gt": fr0m, "$lt":to} }}}, {'requests.$': 1})
    print(list(d))
    if region == "":
        if country == "all":
            data =list(db['traffic'].find({
                "lat": {"$gt": -300},
                "requests": {"$elemMatch": {"timestamp": {"$gt": fr0m, "$lt":to} }}
                },{"_id":0}))
        else:
            data =list(db['traffic'].find({
                "countryCode":country,
                "requests": {"$elemMatch": {"timestamp": {"$gt": fr0m, "$lt":to} }}

                },{"_id":0}))
        
    else:
        data =list(db['traffic'].find({
                    "countryCode":"US",
                    "region":region,
                    "requests": {"$elemMatch": {"timestamp": {"$gt": fr0m, "$lt":to} }}

        },{"_id":0}))
    for item in data:
        i=""
        for request in item["requests"]:
            i = i + request["page"] + " \n <br> "
        item["icon"]= "triangle-",
        item["label"]=  len(item["requests"]) 
        item["tooltip"]=item["query"], i   
    response = make_response(
        json.dumps(data, indent=4, sort_keys=True, default=str),
        200
    )
    return response
app.run(host='localhost', port=8080, debug=True)
