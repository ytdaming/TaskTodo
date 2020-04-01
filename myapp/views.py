from myapp import app,db
from flask import render_template, flash, redirect, url_for, session,request



@app.route('/')
def index():
    return 'index'
