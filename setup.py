from flask import render_template
from app import app

@app.route('/class_setup', methods=['POST', 'GET'])
def setup():
    return render_template('setup.html',
                           classes=[player_class for player_class in classes],
                           nav_title='Welcome.'
                        )

@app.route('/class/<class_name>', methods=['POST', 'GET'])
def return_class(class_name):
    return class_name

