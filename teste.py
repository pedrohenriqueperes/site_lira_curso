from main import app
from comunidadeimpressionadora import database


with app.app_context():
    database.create_all()

