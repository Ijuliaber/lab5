# py_ver == "3.6.9"
import flask


app = flask.Flask(__name__)


# root_ssh_pwd = "k33pc41mU$$Ri$c0min9"
# main_server_ip = "8.8.8.8"


@app.route('/introduction')
def introduction():
    return """
            <html>
                <title>Знакомство</title>
                <body>
                    <form action="/set_name">
                        Представьтесь, пожалуйста: <input name="name" type="text" />
                        <input name="submit" type="submit">
                    </form>
                </body>
            </html>
"""


@app.route('/')
def index_page():
    if flask.request.cookies.get('name'):
        return """
            <html>
                <title>Приветствие</title>
                <script>
window.getCookie = function(name) {
  var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) return match[2];
}
document.write('<h1>Привет, ' + getCookie('name') + '!</h1>')
                </script>
                <body>

                </body>
            </html>
"""
    else:
        return """
            <html>
                <title>Приветствие</title>
                <script></script>
                <body>
                    <a href="/introduction">Как вас зовут?</a>
                </body>
            </html>
"""


@app.route('/set_name')
def cookie_setter():
    response = flask.make_response(flask.redirect('/'))
    response.set_cookie('name', flask.request.args.get('name'))
    return response


import cPickle, base64, hashlib


@app.route('/secret')
def get_msg():
    if flask.request.method == 'POST':
        if flask.request.data:
            msg = cPickle.loads(base64.b64decode(flask.request.data))
            if msg.hash == hashlib.sha256(msg.text.encode('utf8')).hexdigest():
                with open('messages', 'a') as msg_log:
                    msg_log.write(msg.text)


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Security-Policy'] = "default-src 'self'"
    return response


if __name__ == '__main__':
    app.run()
