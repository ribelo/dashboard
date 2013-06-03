from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField, HiddenField, ValidationError,\
    Required, RecaptchaField

from collections import OrderedDict as odict
from app import app
import json

global_menu_bar = ['dashboard', 'settings']
data = json.load(open('./app/data/dashboard.json'))
dash={'headers': ['#', 'sp1', 'sp2', 'sc1', 'sc2', 'sc3', 'sc4'],
 'rows': [['m5',
   'Thu 30 May 04:40',
   'Wed 29 May 20:25',
   'Thu 30 May 04:40',
   'Thu 30 May 04:40',
   'Thu 30 May 18:30',
   'Wed 29 May 20:25'],
  ['m10',
   'Wed 29 May 20:20',
   'Tue 28 May 10:20',
   'Tue 28 May 20:50',
   'Tue 28 May 17:20',
   'Thu 30 May 15:00',
   'Thu 30 May 15:00'],
  ['m15',
   'Wed 29 May 20:15',
   'Fri 24 May 13:45',
   'Tue 28 May 15:30',
   'Tue 28 May 15:30',
   'Tue 28 May 20:45',
   'Tue 28 May 20:45'],
  ['m30',
   'Mon 27 May 20:30',
   'Sat 25 May 12:30',
   'Fri 24 May 18:30',
   'Tue 28 May 11:00',
   'Tue 28 May 15:30',
   'Mon 29 Apr 13:00'],
  ['m60',
   'Fri 24 May 13:00',
   'Fri 24 May 13:00',
   'Fri 24 May 18:00',
   'Mon 27 May 20:00',
   'Mon 27 May 20:00',
   '---'],
  ['m240',
   'Mon 27 May 20:00',
   'Mon 27 May 20:00',
   'Fri 17 May 16:00',
   'Tue 14 May 20:00',
   'Fri 24 May 12:00',
   '---']]}


@app.route('/dashboard')
@app.route('/')
@app.route('/index')
def dashboard():
    name = 'dashboard'
    dashboard_menus = ['candle', 'wrb', 'zone', 'vsa']
    return render_template('dashboard.html', name=name,
                           global_menu_bar=global_menu_bar,
                           inner_menu=dashboard_menus,
                           dash=dash)


@app.route('/settings')
def settings():
    name = 'settings'
    return render_template('index.html', name=name, global_menu_bar=global_menu_bar)
