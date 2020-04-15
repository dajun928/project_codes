from flask import Flask, render_template, make_response, request, session


app = Flask(__name__)


class DefaultConfig(object):
    SECRET_KEY = 'fih9fh9eh9gh2'


app.config.from_object(DefaultConfig)


@app.route('/')
def home():
    mint = 123
    mstr = 'itcast'

    data = dict(
        my_int=123,
        my_str='itcast'
    )

    # data = {
    #     'my_int': 123,
    #     'my_str': 'itcast'
    # }
    # return render_template('index.html', my_str=mstr, my_int=mint)
    return render_template('index.html', **data)
    # return render_template('index.html', my_str='itcast', my_int=123)


@app.route('/demo4')
def demo4():
    # return '状态码为 666', 666
    return '状态码为 666', 666, {'Itcast': 'Python'}

    # resp = make_response()
    #
    # return resp


@app.route('/cookie')
def set_cookie():
    resp = make_response('set cookie ok')
    resp.set_cookie('username', 'itcast')
    return resp


@app.route('/get_cookie')
def get_cookie():
    resp = request.cookies.get('username')
    return resp


@app.route('/delete_cookie')
def delete_cookie():
    response = make_response('hello world')
    response.delete_cookie('username')
    return response


@app.route('/set_session')
def set_session():
    session['username'] = 'itcast'
    return 'set session ok'


@app.route('/get_session')
def get_session():
    username = session.get('username')
    return 'get session username {}'.format(username)



