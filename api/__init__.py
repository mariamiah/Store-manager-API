from flask import Flask
from api.views.product_views import product

app = Flask(__name__)
app.register_blueprint(product)
