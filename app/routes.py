# -*- coding: utf-8 -*-

from app import app
from flask import render_template
import vk

idApp = '7533932'

@app.route('/')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)