from flask import Flask, request, jsonify, abort
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/kampus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

@app.route('/')
def hello_world():
    return 'Selamat Datang'

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nim = db.Column(db.CHAR(10), unique=True, nullable=False)
    nama = db.Column(db.CHAR(100), nullable=False)
    alamat = db.Column(db.TEXT)


class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nim', 'nama', 'alamat')


person = PersonSchema()
persons = PersonSchema(many=True)


@app.route('/person', methods=["POST"])
def add_person():
    nim = request.json['nim']
    nama = request.json['nama']
    alamat = request.json['alamat']
    new_person = Person(nim=nim, nama=nama, alamat=alamat)
    db.session.add(new_person)
    db.session.commit()
    return jsonify(person.dump(new_person))


@app.route('/person', methods=["GET"])
def get_person():
    all_persons = Person.query.all()
    result = persons.dump(all_persons)
    return jsonify(result)


@app.route('/person/<int:id>', methods=["PUT"])
def get_peron(id):
    person_data = Person.query.get(id)
    person_data.nim = request.json['nim']
    person_data.nama = request.json['nama']
    person_data.alamat = request.json['alamat']
    db.session.commit()
    return jsonify(person.dump(person_data))


@app.route('/person/<int:id>', methods=["DELETE"])
def person_delete(id):
    person_data = Person.query.get(id)
    db.session.delete(person_data)
    db.session.commit()
    return jsonify(person.dump(person_data))


if __name__ == '__main__':
    app.run(debug=True)



#Dwi Febi Fauzi 18090125
