from app import app, config
from flask import render_template, redirect, url_for, session

@app.route('/')
def home():
    return "Hello."