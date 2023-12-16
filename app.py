from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import date
import json
import requests
import pandas as pd
import os
import shutil
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from openpyxl import Workbook
from collections import OrderedDict
from pathlib import Path


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.age}"

@app.route('/')
def index():
    persons = Person.query.order_by(Person.id).all()
    return render_template('persons.html', persons=persons)

@app.route('/dashboard')
def dashboard():
    # Add logic to generate data for the dashboard
    data = {'key': 'value'}
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    # Create all database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
