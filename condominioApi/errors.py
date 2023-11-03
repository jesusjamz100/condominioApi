
# Errores personalizados para la API

class APINotFound(Exception):
    code = 404
    description = 'Not Found'

class APIBadRequest(Exception):
    code = 400
    description = 'Bad Request'