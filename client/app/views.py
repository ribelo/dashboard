#-*- coding: utf-8-*-
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField, HiddenField, ValidationError,\
    Required, RecaptchaField

from collections import OrderedDict as odict
from app import app
import json

global_menu_bar = ['dashboard', 'settings']
data = json.load(open('./app/data/dashboard.json'))
dash = {'hheaders': ['m5', 'm10', 'm15', 'm30', 'm60', 'm240'],
 'rows': [[{'output': 'Mon 03 Jun 19:40', 'type': 'bear'},
   {'output': 'Mon 03 Jun 19:40', 'type': 'bear'},
   {'output': 'Sun 02 Jun 19:30', 'type': 'bear'}],
  [{'output': 'Mon 03 Jun 19:00', 'type': 'bull'},
   {'output': 'Mon 03 Jun 19:00', 'type': 'bull'},
   {'output': 'Sun 02 Jun 20:00', 'type': 'bear'}],
  [{'output': 'Mon 03 Jun 19:00', 'type': 'bull'},
   {'output': 'Mon 03 Jun 17:45', 'type': 'bull'},
   {'output': 'Fri 17 May 16:00', 'type': 'bull'}],
  [{'output': 'Mon 03 Jun 19:00', 'type': 'bull'},
   {'output': 'Mon 03 Jun 09:00', 'type': 'bear'},
   {'output': 'Fri 10 May 17:30', 'type': 'bull'}],
  [{'output': 'Mon 03 Jun 17:00', 'type': 'bull'},
   {'output': 'Thu 30 May 21:00', 'type': 'bear'},
   {'output': '---', 'type': None}],
  [{'output': 'Sun 02 Jun 08:00', 'type': 'bear'},
   {'output': 'Sun 02 Jun 08:00', 'type': 'bear'},
   {'output': '---', 'type': None}]],
 'vheaders': ['#', 'wrb', 'wrb_hg', 'fvb']}


@app.route('/dashboard')
@app.route('/')
@app.route('/index')
def dashboard():
    name = 'dashboard'
    dashboard_menus = ['candle', 'wrb', 'zone', 'vsa']
    return render_template('dashboard.html', name=name,
                           global_menu_bar=global_menu_bar,
                           inner_menu=dashboard_menus,
                           jdata=dash)


@app.route('/settings')
def settings():
    name = 'settings'
    return render_template('index.html', name=name,
                           global_menu_bar=global_menu_bar)





def jsonify(dfs, columns, names=None, date_format='%a %d %b %H:%M'):
    if not names:
        names = ['#']
        names.extend(columns)
    else:
        names.insert(0, '#')

    result = {'vheaders': names, 'hheaders': [], 'rows': []}

    for df in sorted(dfs, key=lambda x: x.index.freq):
        freq = df.index.freq.delta.total_seconds()/60
        result['hheaders'].append('m{}'.format(int(freq)))
        row = []
        for column in columns:
            data = {'output': '---', 'type': None}
            time_ = None
            try:
                time_ = df.index[df[column] != 0][-1]
            except IndexError:
                pass
            try:
                data['output'] = time_.strftime(date_format)
                data['type'] = 'bull' if df[column][time_] > 0 else 'bear'
            except (AttributeError, KeyError):
                pass
            row.append(data)
        result['rows'].append(row)
    return result


def json_to_html(jdata):
    return render_template('table.html', jdata=jdata)
