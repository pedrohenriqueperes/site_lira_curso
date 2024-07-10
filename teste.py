from comunidadeimpressionadora import app, database

with app.app_context():
    # Dropar todas as tabelas
    database.drop_all()

    # Criar todas as tabelas novamente
    database.create_all()


