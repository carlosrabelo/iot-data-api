from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser

app = Flask(__name__)
db = SQLAlchemy(app)

config = ConfigParser()
config.read('config.ini')

database = {
    'user': config.get('DATABASE', 'user'),
    'password': config.get('DATABASE', 'password'),
    'host': config.get('DATABASE', 'host'),
    'port': config.get('DATABASE', 'port'),
    'database': config.get('DATABASE', 'database')
}

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database['user']}:{database['password']}@{database['host']}:{database['port']}/{database['database']}"

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field1 = db.Column(db.Float)
    field2 = db.Column(db.Float)

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

@app.route('/update', methods=['POST'])
def update_data():
    field1 = float(request.form.get('field1'))
    field2 = float(request.form.get('field2'))

    data = SensorData(field1=field1, field2=field2)
    db.session.add(data)
    db.session.commit()

    return "Data added successfully"

@app.route('/data', methods=['GET'])
def get_data():
    all_data = SensorData.query.all()

    data_list = []
    for data in all_data:
        data_list.append({
            'field1': data.field1,
            'field2': data.field2
        })

    return jsonify(data_list)

if __name__ == '__main__':
    db.create_all()
    app.run()
