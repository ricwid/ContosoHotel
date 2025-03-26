from datetime import datetime, timedelta
import json
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from . import app, config


#region -------- BACKEND API ENDPOINTS --------

#endregion -------- BACKEND API ENDPOINTS --------


#region -------- FRONTEND API ENDPOINTS --------

@app.route("/setup")
def setup():
    return render_template("setup.html", config=config.get_layout_configuration())


@app.route("/")
def home():
    # ------- START: CHECK IF THE DATABASE IS SETUP -------
    # ------- END: CHECK IF THE DATABASE IS SETUP -------
    return render_template("home.html", config=config.get_layout_configuration())


@app.route("/list")
def list():
    return render_template("list.html", config=config.get_layout_configuration())

@app.route("/create")
def create():
    return render_template("create.html", config=config.get_layout_configuration(), checkin=datetime.now().strftime('%Y-%m-%d'), checkout=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))

#endregion -------- FRONTEND API ENDPOINTS --------
