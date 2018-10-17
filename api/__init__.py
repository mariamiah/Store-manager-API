from flask import Flask
from api.views.product_views import product
from api.views.saleRecord_views import sale

app = Flask(__name__)
app.register_blueprint(product)
app.register_blueprint(sale)
