import re, io, json
from flask import Flask, request
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)



def check_date(date):
	pattern = re.compile('[0-9]{2}-[0-9]{4}')
	if pattern.match(date) == None:
		return False
	else:
		return True

def check_web_page(page):
	pattern = re.compile('^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$')
	if pattern.match(page) == None:
		return False
	else:
		return True

def save_heroes(heroes):
	with open('superheros.json', mode='wt') as file:
		json.dump(heroes, file)
	
def get_heroes():
	try:
		with open('superheros.json') as file:
			heroes = json.load(file)
		return heroes
	except IOError:
		return []

class Bohaterowie(restful.Resource):		
	def get(self):
		return get_heroes()

	def post(self):
		if not request.json:
			return {'error':'nie json'}
			
		if len(request.json['name'])>20:
			return{'name':'invalid name format'}, 400
			
		if len(request.json['real_name'])>50:
			return{'real_name':'invalid real_name format'}, 400
			
		if not check_date(request.json['appearance_date']):
			return{'appearance_date':'invalid appearance_date format'}, 400
		
		if not check_web_page(request.json['web_page']):
			return{'web_page':'invalid web_page format'}, 400		
			
		dane = get_heroes()
		for i in range(len(dane)):
			if dane[i]['name'] == request.json['name']:
				return {'error':'ale my juz to mamy..'}, 400
			
		bohater = {
					"name":request.json['name'],
					"real_name":request.json['real_name'],
					"appearance_date":request.json['appearance_date'],
					"web_page":request.json['web_page']
				   }
				   
		dane.append(bohater)
		save_heroes(dane)
		return{'status':'created'}, 201

class Bohater(restful.Resource):
	def get(self, id):
		dane = get_heroes()
		for i in dane:
			if i['name'] == id:
				return i
		return{'error':'not found'}, 404
		
		
	def delete(self, id):
		dane = get_heroes()
		for i in range(len(dane)):
			if dane[i]['name'] == id:
				del dane[i]
				save_heroes(dane)
				return{'status':'no content'}, 204
		return{'error':'not found'},404
		
	def put(self, id):
		dane = get_heroes()
		for i in dane:
			if i['name'] == id:
				if not request.json:
					return {'error':'nie json'}
			
				if len(request.json['name'])>20:
					return{'name':'invalid name format'}, 400
					
				if len(request.json['real_name'])>50:
					return{'real_name':'invalid real_name format'}, 400
					
				if not check_date(request.json['appearance_date']):
					return{'appearance_date':'invalid appearance_date format'}, 400
				
				if not check_web_page(request.json['web_page']):
					return{'web_page':'invalid web_page format'}, 400	
				
				i['name'] = request.json['name']
				i['real_name'] = request.json['real_name']
				i['appearance_date'] = request.json['appearance_date']
				i['web_page'] = request.json['web_page']
				save_heroes(dane)
				return{'status':'ok'},200
		
		return{'error':'not found'}, 404
		
		
		
api.add_resource(Bohaterowie, '/bohater/')
api.add_resource(Bohater, '/bohater/<string:id>/')

if __name__ == '__main__':
    app.run(debug=True)