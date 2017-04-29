import requests ## libreria para hacer el request a los navegadores
from bs4 import BeautifulSoup ## libreria utilizada para parsear el html 
from flask import Flask, jsonify ## librerias de flask a utilizar
import os ## libreria para el manejo de files.
import sqlite3 ## 


app = Flask(__name__)

DATABASE = '../test/db/Testing.db' # path hacia la base de datos

###############################################
## seccion de route con scrapy beautifulsoup ##
## 'div', {"class" : "results"}
###############################################
@app.route("/")
def hello():
    return "Hello World!"
@app.route("/about")
def about():
	return "<h1>ESTO ES LA PAGINA DE ABOUT</h1>"
@app.route("/json")
def json():
	list = [
		{'id': '1', 'val': '200'},
		{'id': '2', 'val': '300'}
	]
	return jsonify(results=list)
@app.route("/google")
def search():
	url = 'https://www.google.com.ar/search?q=comprar+peugeot+504' # url del navegador
	req = requests.get(url) # obtengo la respuesta
	html = req.text # aqui tomo la respuesta en formato de texto plano
	soup = BeautifulSoup(html, 'html.parser') # aqui parseo a html para poder realizar el scrapy
	list = [] # armo un array
	# aqui se buscan los elementos requeridos apartir de pasarle unos selectores 
	# ejemplo : 'div' {"class" : "g"}
	for link in soup.findAll('div', { "class" : "g" }):
		# aqui se obtiene el tag a de la siguiente manera : link.a.get(href)
		list.append({'url': search_items(link.a.get('href'))})
	return jsonify(results=list)
@app.route("/yahoo")
def search_y():
	url = 'https://espanol.search.yahoo.com/search?p=comprar+peugeot+504'
	req = requests.get(url)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	list = []
	for link in soup.findAll('div', {"class" : "dd"}):
		list.append({'url' : link.a.get('href')})
	return jsonify(results=list)
@app.route("/bing")
def search_b():
	url = 'http://www.bing.com/search?q=comprar+peugeot+504'
	req = requests.get(url)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	list = []
	for link in soup.findAll('div', {"class" : "sb_add"}):
		list.append({'url' : link.a.get('href')})
	return jsonify(results=list)
@app.route("/duck")
def duck():
	url = 'https://duckduckgo.com/html/?q=comprar+autos'
	req = requests.get(url)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	list = []
	for link in soup.findAll('a'):
		print(link.get('href'))
	return jsonify(results=list)

@app.route("/mercado")
def mercado_l():
	url = 'http://autos.mercadolibre.com.ar/peugeot/504/'
	req = requests.get(url)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	list = []
	for link in soup.findAll('div', { "class" : "section" }):
		print(link.ol)
	return jsonify(results=[])
############################################
## seccion manejo de base de datos sqlite ##
############################################

# aqui se estable la conexion a la base de datos.
def get_db():
	db = getattr(Flask, '_database', None)
	if db is None:
		db = sqlite3.connect(DATABASE) # aqui se pasa el path hacia la data
	return db
@app.teardown_appcontext
def close_connection(exception):
	db = getattr(Flask, '_database', None)
	if db is not None:
		db.close()

# aqui se crean nuevos routes
@app.route("/categorias")
def cat():
	query = 'select * from categories'
	args=()
	one=False
	list = []
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	for cat in rv:
		category = {'category': cat[1], 'key': cat[2]}
		list.append(category)
	return jsonify(results=list)
@app.route("/navegadores")
def nav():
	query = 'select * from navigators'
	args=()
	one=False
	list = []
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	for nav in rv:
		navegators = {'navegator': nav[1], 'selectors': nav[2]}
		list.append(navegators)
	return jsonify(results=list)
@app.route("/pages")
def pages():
	try:
		query = 'select * from pages'
		args=() # parametros para la query
		one = False
		list = []
		con = get_db() # aqui se devuelve la conexion#sqlite3.connect(DATABASE)
		rv = None
		# aqui se maneja la conexion a la base de datos
		with con:
			cur = con.cursor() # obtengo el cursor de la base de datos
			cur.execute(query, args) # aqui lanzo la query hacia la base datos
			rv = cur.fetchall()  # aqui se recuperan los datos
		if con:
			cur.close() # se cierre la conexion
		for pag in rv:
			page = {'selectors': pag[1], 'subselectors': pag[2]}
			list.append(page)
	except Exception as e:
		# aqui capturo una posible excepcion
		print(e)
		con.close() # cerramos la conexion a la base datos
	else:
		pass
	finally:
		con.close() # cerramos la conexion a la base de datos
	return jsonify(results=list)

###############################################
## aqui se realiza la busqueda de los items  | &sa= ##
###############################################

# busquedas
def search_items(url):
	try:
		url_str = url.split("=")
		newUrl = url_str[1].replace("&sa","")
		return newUrl
	except Exception as e:
		raise
	else:
		pass
	finally:
		pass

if __name__ == "__main__":
    app.run()