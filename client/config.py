import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'.encode()
BOOTSTRAP_USE_MINIFIED = True
BOOTSTRAP_USE_CDN = True
BOOTSTRAP_FONTAWESOME = True

DASHBOARD = {'candle': {'columns': ['dir', 'wrb', 'wrb_hg'],
                        'names': ['candle', 'wrb', 'wrb hg']},
             'zones': {'columns': ['swing_point1', 'swing_point2', 'strong_continuation1',
                                   'strong_continuation2', 'strong_continuation3',
                                   'strong_continuation4', 'zones'],
                       'names': ['sp1', 'sp2', 'sc1', 'sc2', 'sc3', 'sc4', 'any']},
             'vsa': {'columns': ['supply_demand', 'effort'],
                     'names': ['sd', 'effort']},
             'wrb analysis': {'columns': ['dcm', 'fvb'],
                              'names': ['dcm', 'fvb']}}
