import requests
from faker import Faker
from flask import Flask, render_template, request


app = Flask(__name__)
fake = Faker()


@app.route('/requirements', methods=['get'])
def requirements():
    with open('requirements.txt', mode='r', encoding='utf-16') as file:
        context = {'requirements': file.readlines()}
    return render_template('requirements.html', **context)


@app.route('/generate_users', methods=['get', 'post'])
def user_generator():
    users_list = []

    if request.method == 'POST':
        if request.form['users_count']:
            users_count = int(request.form['users_count'])
        else:
            users_count = 100
        for _ in range(users_count):
            users_list.append(f'{fake.first_name()} {fake.unique.ascii_email()}')
        context = {'users_list': users_list}

    return render_template('generate_users.html', **context)


@app.route('/space', methods=['get'])
def space():
    response = requests.get('http://api.open-notify.org/astros.json')
    response.raise_for_status()

    context = {}
    try:
        context['number'] = response.json()["number"]
    except KeyError:
        context['number'] = 0
        context['space'] = []

    if 'space' not in context:
        context['space'] = response.json()["people"]

    return render_template('space.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
