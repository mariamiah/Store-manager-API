[![Build Status](https://travis-ci.org/mariamiah/Store-manager-challenge-2.svg?branch=develop)](https://travis-ci.org/mariamiah/Store-manager-challenge-2)
[![Coverage Status](https://coveralls.io/repos/github/mariamiah/Store-manager-challenge-2/badge.svg?branch=develop)](https://coveralls.io/github/mariamiah/Store-manager-challenge-2?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/618edf7cfaa304ef1853/maintainability)](https://codeclimate.com/github/mariamiah/Store-manager-challenge-2/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/95a397aa553941df879ac492bdd1411b)](https://www.codacy.com/app/mariamiah/Store-manager-challenge-2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mariamiah/Store-manager-challenge-2&amp;utm_campaign=Badge_Grade)
# StoreManager-API
Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

## Features 
  - Admin can add a product
  - Admin or store attendant can get all products
  - Admin or store attendant can get a specific product.
  - Store attendant can add a sale order.
  - Admin can get all sale order details.

## API Endpoints
| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| GET | /api/v1/products | Fetches all products|
| GET | api/v1/products/&lt;product_id&gt; | Fetches a single product |
| GET | api/v1/sales | Fetches all sales records |
| GET | api/v1/sales/&lt;sales_id&gt; | Fetches a single sales record |
| POST | api/v1/products | Creates a product |
| POST | api/v1/sales | Creates a sales order |

**Getting started with the app**

**Technologies used to build the application**

  - [Python 3.6](https://docs.python.org/3/)
  - [Flask](http://flask.pocoo.org/)


## Installation

Create a new directory and initialize git in it. Clone this repository by running
```sh
$ git clone https://github.com/mariamiah/Store-manager-challenge-2.git
```
Create a virtual environment. For example, with virtualenv, create a virtual environment named venv using
```sh
$ virtualenv venv
```
Activate the virtual environment
```sh
$ cd venv/scripts/activate
```
Install the dependencies in the requirements.txt file using pip
```sh
$ pip install -r requirements.txt
```

Start the application by running
```sh
$ python run.py
```
Test your setup using [postman](www.getpostman.com) REST-client

**Running tests**

 - Install nosetests 
 - Navigate to project root
 - Use `nosetests tests/` to run the tests
 - To run tests with coverage, use `nosetests --with-coverage --cover-package=app && coverage report`

### Link to Store Manager on Heroku
### [StoreManager](https://storemanager15.herokuapp.com)

