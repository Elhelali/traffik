from flask import Flask,jsonify
from decorators import mongo
import requests
from user.routes import user

app = Flask(__name__)
app.register_blueprint(user)

@app.route('/test')
@mongo
def intro(db):
    x =list(db['trackr'].find({},{'_id':0}))
    print (x)
    return jsonify(x)
    
@app.route('/create_group')
@mongo
def create_group(db):
    x =list(db['trackr'].insert({}))
    print (x)
    return jsonify(x)

app.run(host='localhost', port=8080, debug=True)