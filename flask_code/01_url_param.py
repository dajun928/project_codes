from flask import Flask, request, abort
from werkzeug.routing import BaseConverter


app = Flask(__name__)


@app.errorhandler(ZeroDivisionError)
def zero_division_error(e):
    print(e)
    return '除数不能为0'


# /users/123
# @app.route('/users/<user_id>')
# @app.route('/users/<string:user_id>')
@app.route('/users/<int:user_id>')
def get_users_data(user_id):
    print(type(user_id))
    return 'get users {}'.format(user_id)


class MobileConverter(BaseConverter):
    regex = r'1[3-9]\d{9}'


app.url_map.converters['mobile'] = MobileConverter


@app.route('/sms_codes/<mobile:mob_num>')
def send_sms_code(mob_num):
    1 / 0
    print(type(mob_num))
    return 'send sms code to {}'.format(mob_num)


# /articles?channel_id=123 -> thread A -> 123  request 上下文
# /articles?channel_id=124 -> thread B -> 124

# /articles
@app.route('/articles')
def get_articles():
    channel_id = request.args.get('channel_id')

    if channel_id is None:
        abort(400)  # 400 Bad Request

    return 'you wanna get articles of channel {}'.format(channel_id)




#
# with open('', 'rb') as f:
#     f.read()


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['pic']
    # with open('./demo.png', 'wb') as new_file:
    #     new_file.write(f.read())
    f.save('./demo.png')
    return 'ok'






