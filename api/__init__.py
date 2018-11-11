from flask import Flask, jsonify, redirect
from api.views.product_views import product
from api.views.user_views import user
from flasgger import Swagger
from api.views.sale_record_views import sale

app = Flask(__name__)
app.register_blueprint(product)
app.register_blueprint(sale)
app.register_blueprint(user)


# Define a swagger template
template = {
    "openapi": "3.0.0",
    "info": {
        "title":
        "Store Manager API",
        "description":
        "Store Manager is a web application that helps store owners manage\
         sales and product inventory records",
        "version":
        "v2"
    }
}

# Instantiate swagger docs
swagger = Swagger(app, template=template)


@app.route('/')
def index():
    return jsonify({"message": "Welcome to store manager application"})


@app.route('/apidocs')
def showdocs():
    return redirect('/apidocs/')
