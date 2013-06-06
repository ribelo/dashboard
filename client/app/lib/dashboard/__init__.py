#-*- coding: utf-8-*-
import jinja2
import jinja_env


def jsonify(dfs, columns=None, header=None):
    result = {'headers': ['#'], 'rows': []}
    if headers:
        result['headers'].extend(headers)
    else:
        result['headers'].extend(columns)
    for df in sorted(dfs, key=lambda x: x.index.freq):
        freq = df.index.freq.delta.total_seconds()/60
        row = []
        row.append('m{}'.format(int(freq)))
        for column in columns:
            time_ = None
            try:
                time_ = df.index[df[column] != 0][-1]
            except IndexError:
                pass
            if time:
                dir_ =  df.dir[
        result['rows'].append(row)
    return result


def json_to_html(jdata):
    template = jinja_env.get_template('table.html')
    return template.render(jdata=jdata)
