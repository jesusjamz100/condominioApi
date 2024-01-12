from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path, getenv
from .errorhandlers import registrar_errores
from flask_cors import CORS

load_dotenv()

url = '/condominio/api/v1.0'

# Registrar la aplicacion y setear la configuracion
app = Flask(__name__)
cors = CORS(app, origins=[getenv('FRONTEND_URL')])
app.config.from_object('condominioApi.config.DevelopmentConfig')

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

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