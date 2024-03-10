from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    if animal:
        response_body = f'''
        <ul>ID: {animal.id}</ul>
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
        <ul>Zookeeper: {animal.zookeeper.name if animal.zookeeper else 'N/A'}</ul>
        <ul>Enclosure: {animal.enclosure.environment if animal.enclosure else 'N/A'}</ul>
        '''
        response = make_response(response_body, 200)
    else:
        response = make_response('<h1>Animal not found</h1>', 404)

    return response


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    if zookeeper:
        response_body = f'''
        <ul>ID: {zookeeper.id}
        <ul>Name: {zookeeper.name}</ul>
        <ul>Birthday: {zookeeper.birthday}</ul>
        '''
        if zookeeper.animals:
            response_body += '<ul>Animals:</ul>'
            for animal in zookeeper.animals:
                response_body += f'<ul>Animal: {animal.name}, Type: {animal.species}</ul>'
        else:
            response_body += '<ul>No animals associated with this zookeeper</ul>'

        response = make_response(response_body, 200)
    else:
        response = make_response('<h1>Zookeeper not found</h1>', 404)

    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    
    if enclosure:
        response_body = f'''
        <ul>ID: {enclosure.id}</ul>
        <ul>Environment: {enclosure.environment if enclosure.environment else 'N/A'}</ul>
        <ul>Open to Visitors: {enclosure.open_to_visitors if enclosure.open_to_visitors else 'N/A'}</ul>
        '''
        if enclosure.animals:
            response_body += '<ul>Animals:</ul>'
            for animal in enclosure.animals:
                response_body += f'<ul>Animal: {animal.name}</ul>'
        else:
            response_body += '<ul>No animals associated with this enclosure</ul>'
        
        response = make_response(response_body, 200)
    else:
        response = make_response('<h1>Enclosure not found</h1>', 404)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
