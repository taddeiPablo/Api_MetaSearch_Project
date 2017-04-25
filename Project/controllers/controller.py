###########################################################
## Aqui se declara el controller desde donde se manejaran #
## las routes.											  #
###########################################################

from flask import Blueprint
from flask import request

# aqui recupero el blueprint que escucha los routes
control_api = Blueprint('control_api', __name__)

#route get_categories
@control_api.route("/get_categories", methods=['GET'])
def get_categories():
	try:
		return "funciona"
	except Exception as e:
		raise e

#route search_items (parametros incluidos busqueda avanzada)
@control_api.route("/search/", methods=['GET'])
def search():
	try:
		query = request.args.get('var1', None)
		price = request.args.get('var2', None)
		print(query)
		print(price)
		return "FUNCIONA"
	except Exception as e:
		raise e