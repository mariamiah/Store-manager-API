from flask import Flask, jsonify, redirect
from api.views.product_views import product
from api.views.category_views import category
from api.views.user_views import user
from flasgger import Swagger
from api.views.sale_record_views import sale

app = Flask(__name__)
app.register_blueprint(product)
app.register_blueprint(sale)
app.register_blueprint(user)
app.register_blueprint(category)


# Define a swagger template
template = {
    "swagger": "2.0",
    "info": {
        "title":
        "Store Manager API",
        "description":
        "Store Manager is a web application that helps store owners manage\
         sales and product inventory records",
        "version":
        "1.0.0"
    },
    "schemes": ["http", "https"]
}

# Instantiate swagger docs
swagger = Swagger(app, template=template)


@app.route('/')
def index():
    return jsonify({"message": "Welcome to store manager application"})


@app.route('/apidocs')
def showdocs():
    return redirect('/apidocs/')
