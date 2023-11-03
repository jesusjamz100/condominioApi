from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from .errorhandlers import registrar_errores

# Registrar la aplicacion y setear la configuracion
app = Flask(__name__)
app.config.from_object('condominioApi.config.DevelopmentConfig')

# Registrar el manejo de errores
registrar_errores(app)

# Instancia del ORM y sistema de migraciones
db = SQLAlchemy()
migrate = Migrate()

# Inicializacion de la base de datos
db.init_app(app)
migrate.init_app(app, db)

# Blueprints (endpoints)
from condominioApi.endpoints import *

url = '/condominio/api/v1.0'

app.register_blueprint(propietarios, url_prefix=f'{url}/propietarios')
app.register_blueprint(ingresos, url_prefix=f'{url}/ingresos')
app.register_blueprint(cuentas, url_prefix=f'{url}/cuentas')
app.register_blueprint(torres, url_prefix=f'{url}/torres')
app.register_blueprint(apartamentos, url_prefix=f'{url}/apartamentos')
app.register_blueprint(pisos, url_prefix=f'{url}/pisos')
app.register_blueprint(recibos, url_prefix=f'{url}/recibos')
app.register_blueprint(egresos, url_prefix=f'{url}/egresos')
app.register_blueprint(facturas, url_prefix=f'{url}/facturas')

# En caso de no existir, crea la base de datos
if not path.exists('instance/condominio.db'):
    with app.app_context():
        db.create_all()
        print('creada base de datos')