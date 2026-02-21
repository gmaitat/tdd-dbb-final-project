"""
Product Store Service

Paths:
------
GET /products - Returns a list all of the Products
GET /products/{id} - Returns the Product with a given id number
POST /products - creates a new Product record in the database
PUT /products/{id} - updates a Product record in the database
DELETE /products/{id} - deletes a Product record in the database
"""

import logging
from flask import Flask, jsonify, request, url_for, abort
from service.models import Product, Category, DataValidationError, db

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


############################################################
# Health check endpoint
############################################################
@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "OK"}), 200


############################################################
# LIST ALL PRODUCTS
############################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns all of the Products"""
    logger.info("Request for product list")
    products = []

    category = request.args.get("category")
    name = request.args.get("name")
    available = request.args.get("available")

    if category:
        category_value = getattr(Category, category.upper(), None)
        if category_value is None:
            abort(400, description=f"Invalid category: {category}")
        products = Product.find_by_category(category_value)
    elif name:
        products = Product.find_by_name(name)
    elif available is not None:
        available_bool = available.lower() in ["true", "1", "yes"]
        products = Product.find_by_availability(available_bool)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    logger.info("Returning %d products", len(results))
    return jsonify(results), 200


############################################################
# READ A PRODUCT
############################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Retrieves a single Product"""
    logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(404, description=f"Product with id '{product_id}' was not found.")
    return jsonify(product.serialize()), 200


############################################################
# CREATE A NEW PRODUCT
############################################################
@app.route("/products", methods=["POST"])
def create_product():
    """Creates a Product"""
    logger.info("Request to Create a Product...")
    check_content_type("application/json")

    product = Product()
    data = request.get_json()
    logger.debug("Processing: %s", data)
    product.deserialize(data)
    product.create()
    logger.info("Product with new id [%s] saved!", product.id)

    location_url = url_for("get_product", product_id=product.id, _external=True)
    return (
        jsonify(product.serialize()),
        201,
        {"Location": location_url},
    )


############################################################
# UPDATE AN EXISTING PRODUCT
############################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Updates a Product"""
    logger.info("Request to Update a product with id [%s]", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(404, description=f"Product with id '{product_id}' was not found.")

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), 200


############################################################
# DELETE A PRODUCT
############################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Deletes a Product"""
    logger.info("Request to Delete a product with id [%s]", product_id)

    product = Product.find(product_id)
    if product:
        product.delete()

    return "", 204


############################################################
# Utility functions
############################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        logger.error("No Content-Type specified.")
        abort(415, description=f"Content-Type must be {content_type}")
    if request.headers["Content-Type"] == content_type:
        return
    logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, description=f"Content-Type must be {content_type}")


############################################################
# Error Handlers
############################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles Value Errors from bad data"""
    return bad_request(error)


@app.errorhandler(400)
def bad_request(error):
    """Handles bad requests with 400_BAD_REQUEST"""
    message = str(error)
    logger.warning(message)
    return (
        jsonify(
            status=400, error="Bad Request", message=message
        ),
        400,
    )


@app.errorhandler(404)
def not_found(error):
    """Handles resources not found with 404_NOT_FOUND"""
    message = str(error)
    logger.warning(message)
    return (
        jsonify(status=404, error="Not Found", message=message),
        404,
    )


@app.errorhandler(415)
def mediatype_not_supported(error):
    """Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE"""
    message = str(error)
    logger.warning(message)
    return (
        jsonify(
            status=415, error="Unsupported media type", message=message
        ),
        415,
    )


@app.errorhandler(500)
def internal_server_error(error):
    """Handles unexpected server error with 500_SERVER_ERROR"""
    message = str(error)
    logger.error(message)
    return (
        jsonify(status=500, error="Internal Server Error", message=message),
        500,
    )
