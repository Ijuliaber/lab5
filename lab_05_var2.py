# py_ver == "3.6.9"
import flask
import nmap





app = flask.Flask(__name__)


# root_ssh_pwd = "k33pc41mU$$Ri$c0min9"
# main_server_ip = "8.8.8.8"


import json
import time


@app.route('/feedback_form')
def introduction():
    feedback = ''
    with open('feedback.json', 'r') as feedback_file:
        feedback_dict = json.loads(feedback_file.read())
        for key, value in feedback_dict.items():
            feedback += "<p><i>Анононим, %s</i>: %s</p>" % (key, value)

    return """<html>
                <title>Обратная связь</title>
                <body>
                %s
                    <form action="/save_feedback" method="post">
                        Поделитесь своим мнением: <input name="feedback" type="text" />
                        <input name="submit" type="submit" value="Отправить">
                    </form>
                </body>
            </html>
""" % feedback


@app.route('/save_feedback', methods=["GET", "POST"])
def index_page():
    feedback = flask.request.form.get('feedback')
    d = {"<": "&#x3C;", ">": "&#x3E;", '"': "&#x22;"}


    url_word = []
    for word in feedback:
        if word in d:
            url_word.append(d[word])
        else:
            url_word.append(word)
    new_feedback = ''.join(url_word)



    feedback_dict = {}
    with open('feedback.json', 'r') as feedback_file:
        feedback_dict.update(json.loads(feedback_file.read()))
    feedback_dict[time.time()] = new_feedback
    with open('feedback.json', 'w') as feedback_file:
        feedback_file.write(json.dumps(feedback_dict))
    return flask.redirect('/feedback_form')


@app.route('/send_host')
def set_target():
    return """
            <html>
                <title>Target selection</title>
                <body>
                    <form action="/scan">
                        Enter target IP: <input name="ip" type="text" />
                        <input name="submit" type="submit">
                    </form>
                </body>
            </html>
"""

def ip_val(ip: str):
    try:
        ip = ip.split(".")
        if len(ip) != 4:
            raise ValueError
        for i in ip:
            i = int(i)
            if i < 0 or i > 255:
                raise ValueError
        return ".".join(ip)
    except (TypeError, ValueError):
        return ""


import os


@app.route('/scan')
def scanner():
    ip = flask.request.args.get('ip')
    ip = ip_val(ip)
    if not ip:
        return "Wrong address"
    result = os.popen('nmap ' + ip).read()
    return "%s" % result


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Security-Policy'] = "default-src 'self'"
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


if __name__ == '__main__':
    app.run()