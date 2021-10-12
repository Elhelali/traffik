import pymongo
from functools import wraps
from config import mongo_username,mongo_password
def mongo(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        with pymongo.MongoClient(f"mongodb+srv://{mongo_username}:{mongo_password}@trackr.qaowl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") as database:
            return f(database['trackr'],*args,**kwargs)
    return wrap

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        #if request.method == "OPTIONS":
        #    return f
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if request.cookies.get('token'):
            token = request.cookies.get('token') 
      
        # return 401 if token is not passed
        if not token:
            response= make_response( jsonify({'message' : 'Token is missing !!'}), 401)
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response
        try:
            # decoding the payload to fetch the stored details

            decoded_token = jwt.decode(token, SECRET_KEY,
                            algorithms=['HS256'])
            return  f(decoded_token["id"], *args, **kwargs)
        except:
            response= make_response( jsonify({'message' : 'Token is invalid !!'}), 401)
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response
        # returns the current logged in users contex to the routes
        
  
    return decorated