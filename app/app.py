from flask import Flask, render_template, request, send_from_directory
from flask import make_response
from translate import translate as translation
from datetime import datetime as dt

app = Flask(__name__)
# Fixing 503 error для хостинга Московского Политеха
application = app


'''
Значение request определяется текущим контекстом запроса,
для каждого потока он свой, можем получить доступ к данным,
которые доступны в запросе.
Обратиться к объекту request можно только контексте запроса
В шаблоне доступен по умолчанию (его не нужно передавать)
'''


@app.route('/')
def index():
    '''Функция-обработчик для главной страницы'''
    return render_template('index.html')


@app.route('/translate', methods=["GET", "POST"])
def translate():
    '''Функция-обработчик для страницы "Переводчик"'''

    if request.method == "POST":
        text = translation(request.form.get('text'),
                           request.form.get('language'))
        return render_template('translate.html', text=text)
    return render_template('translate.html')


@app.errorhandler(404)
def page_not_found(error):
    '''Функция-обработчик для страницы "Страница не найдена"'''
    return render_template('page_not_found.html'), 404
