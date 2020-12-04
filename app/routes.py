# -*- coding: utf-8 -*-

from app import app
from flask import render_template
from flask import request, redirect
from flask_login import LoginManager, UserMixin, logout_user, login_required, login_user, current_user
from app import login_manager
from app import conf
from app.vkapi import *
from app.models import User


@app.route('/', methods=['GET', 'POST'])
def index():
    code = request.args.get("code")
    friends = None
    userData = None
    if current_user.is_authenticated:
        access_token = current_user.id
        friends = getFriendsByToken(access_token)
        userData = getUserDataByToken(access_token)
    if code and not current_user.is_authenticated:
        access_token = getAccessKey(code)
        if access_token:
            user = User(access_token)
            login_user(user, remember=True)
            return redirect('/')
    return render_template('index.html', title='Home', friends=friends, userData=userData)


@app.route('/friend/<idUser>', methods=['GET', 'POST'])
def friends(idUser):
    error = None
    friends = getFriendsById(idUser)
    userData = getUserDataById(idUser)
    if not friends:
        error = "У пользователя скрыты друзья."
    return render_template('friends.html', error=error, friends=friends, userData=userData)


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
