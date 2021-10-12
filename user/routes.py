from .models import User
from flask import Blueprint, jsonify, make_response, redirect, request, render_template
from decorators import mongo

user = Blueprint('user', __name__,template_folder='templates')

@user.route('/user/create', methods=['GET','POST'])
@mongo
def create_user(database):
    if User.extension_exists(database,request.form.get("extension")):
        return redirect('/dashboard/users/?error=extension_exists')
    try:
        User.create_user(
            database,
            first_name=request.form.get("name"),
            email=request.form.get("email"),
            password = request.form.get("password")
            )
        return redirect('/')
    except:
        return redirect('/user/create')