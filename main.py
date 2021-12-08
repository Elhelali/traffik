from flask import Flask,jsonify,request,render_template,make_response
from decorators import mongo
import requests,string,random
import json
from user.routes import user

#random.uniform(0.001,-0.001) add this to longitude an dlatitude

app = Flask(__name__)
app.register_blueprint(user)

@app.route('/index')
def intro():
    return render_template("map.html")

    
@app.route('/data/traffic.json')
@mongo
def traffic_json(db):
    data =list(db['traffic'].find({"lat": {"$gt": -300}},{"_id":0}))
    for item in data:
        item["icon"]= "triangle-",
        item["label"]=  len(item["requests"]) 
        item["tooltip"]=item["query"], item["requests"]
        
    print(data)
    response = make_response(
        json.dumps(data, indent=4, sort_keys=True, default=str),
        200
    )
    return response
app.run(host='localhost', port=8080, debug=True)