#! -*- coding: utf8 -*-
import redis
import utils
import config

from flask import Flask, url_for, render_template, Response, json, jsonify, redirect, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, login_required
from forms import LoginForm

DEBUG = True
SECRET_KEY = 'development key'
BOOTSTRAP_JQUERY_VERSION = None

app = Flask(__name__)
app.config.from_object(__name__)

Bootstrap(app)

broker = redis.StrictRedis(**config.REDIS)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = '/login'
login_manager.login_message = u'Debe logearse para acceder'
@login_manager.user_loader
def load_user(userid):
    #TODO implementar carga de usuario
    return None

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #login ok!
        return redirect(request.args.get("next") or url_for('index'))

    return render_template("login.html", form=form)


def enviar_comando(function_name, *args, **kwargs):
    return broker.publish('commands', utils.remote_plc_command(function_name, *args, **kwargs))


def event_stream():
    stream = broker.pubsub()
    stream.subscribe('plc_state')
    for data in stream.listen():
        if data['type'] == 'message':
            yield 'data: %s\n\n' % data['data']

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/graficos')
@login_required
def graficos():
    return render_template('graficos.html')

@app.route('/stream')
@login_required
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/iniciar/<int:programa>')
@login_required
def iniciar_programa(programa):
    if programa in xrange(1, 5):
        enviar_comando('iniciar_programa', programa)
    return "enviado!"

@app.route('/actualizar/<int:programa>', methods='POST')
@login_required
def actualizar_programa(programa):
    return programa


#Debug methods, para poder escribir registro y marcas aleatorias del plc

@app.route('/registro/<int:direccion>/<int:valor>/')
def actualizar_registro(direccion, valor):
    enviar_comando('_escribir_registro', direccion, valor)
    return "enviado!"

@app.route('/marca/<int:direccion>/<int:valor>/')
def actualizar_marca(direccion, valor):
    valor = valor > 0
    enviar_comando('_escribir_marca', direccion, valor)
    return "enviado!"

if __name__ == '__main__':

    app.run(threaded=True, host='0.0.0.0')
