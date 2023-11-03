from flask import jsonify
from .errors import *

# Crea el manejo de errores para el retorno de una respuesta serializada
def registrar_errores(app):

    @app.errorhandler(APINotFound)
    def handle_excpetion(err):
        response = {"error": err.description, "message": ""}

        if len(err.args) > 0:
            response["message"] = err.args[0]
        
        app.logger.error(f"{err.description}: {response['message']}")

        return jsonify(response), err.code
    
    @app.errorhandler(APIBadRequest)
    def handle_excpetion(err):
        response = {"error": err.description, "message": ""}

        if len(err.args) > 0:
            response["message"] = err.args[0]
        
        app.logger.error(f"{err.description}: {response['message']}")

        return jsonify(response), err.code