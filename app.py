from flask import Flask,request,render_template
from flask_restful import Resource, Api
import json
import urllib.request
from flask_apscheduler import APScheduler
app = Flask(__name__)
api = Api(app)

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)


@scheduler.task('interval', id='downloadfile', minutes=60)
def download():
    urllib.request.urlretrieve("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json", "file.json")
    


with open('./file.json') as f:
    data = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')



class AllItems(Resource):
    def get(self):
        return data
class Country(Resource):
    def get(self, name):
        for item in data:
            if item['country'] == name:
                return item
        return {'item': None}, 404

api.add_resource(AllItems, '/data/')
api.add_resource(Country, '/data/<string:name>')
scheduler.start()
