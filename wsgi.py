"""
WSGI Entry Point for the Product Catalogue Microservice
"""
from service.routes import app
from service.models import Product

# Initialize the database
Product.init_db(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
