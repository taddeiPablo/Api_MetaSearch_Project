########################################################	
##	Punto de ingreso a la app						  ##
########################################################

from flask import Flask
# forma de llamar a un modulo mas bien algo especifico del modulo (control_api)
from controllers.controller import control_api

app = Flask(__name__)

# aqui se registra el controller creado
app.register_blueprint(control_api)

if __name__ == '__main__':
	app.run()