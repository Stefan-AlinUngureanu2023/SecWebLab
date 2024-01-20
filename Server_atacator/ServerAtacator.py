from flask import Flask, request
from flask_cors import CORS, cross_origin

#app = Flask(__name__)
#
#@app.route("/api/date")
#def hello_world():
#    return "<p>Hello, World!</p>"

# initialization
#app = Flask(__name__)
#app.config['CORS_HEADERS'] = 'Content-Type'

#cors = CORS(app, resources={r"/foo": {"origins": "*"}})

#@app.route('/foo', methods=['POST'])
#@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
#def foo():
#    return request.cookies.get("cookie")

#if __name__ == '__main__':
#   app.run()


app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/foo", methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def helloWorld():
  return "Hello, cross-origin-world!"