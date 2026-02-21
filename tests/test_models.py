"""
Test Cases for Product Model
"""
import unittest
import logging
from decimal import Decimal
from service.routes import app
from service.models import Product, Category, DataValidationError, db
from tests.factories import ProductFactory

DATABASE_URI = "sqlite:///:memory:"
logger = logging.getLogger(__name__)


class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        if not app.extensions.get("sqlalchemy"):
            db.init_app(app)
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.close()

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        logger.debug("Testing product: %s", product)
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertEqual(found.price, product.price)
        self.assertEqual(found.available, product.available)
        self.assertEqual(found.category, product.category)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        original_id = product.id
        product.description = "Updated description for testing"
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "Updated description for testing")
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "Updated description for testing")

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        for _ in range(5):
            product = ProductFactory()
            product.create()
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_by_name(self):
        """It should Find Products by Name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        name = products[0].name
        count = len([p for p in products if p.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        available = products[0].available
        count = len([p for p in products if p.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, available)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        category = products[0].category
        count = len([p for p in products if p.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)

    def test_deserialize_missing_data(self):
        """It should raise DataValidationError if data is missing"""
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, {"name": "test"})

    def test_deserialize_bad_available(self):
        """It should raise DataValidationError for bad available type"""
        product = Product()
        bad_data = {
            "name": "Test",
            "description": "Test desc",
            "price": "9.99",
            "available": "yes",
            "category": "FOOD"
        }
        self.assertRaises(DataValidationError, product.deserialize, bad_data)

    def test_update_with_empty_id_raises_error(self):
        """It should raise DataValidationError on update with no ID"""
        product = ProductFactory()
        product.id = None
        self.assertRaises(DataValidationError, product.update)

    def test_repr(self):
        """It should return a string representation"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIn(product.name, repr(product))

    def test_find_by_price_as_string(self):
        """It should find products when price is passed as string"""
        product = ProductFactory()
        product.price = Decimal("19.99")
        product.create()
        found = Product.find_by_price("19.99")
        self.assertEqual(found.count(), 1)

    def test_deserialize_bad_attribute(self):
        """It should raise DataValidationError for bad category"""
        product = Product()
        bad_data = {
            "name": "Test",
            "description": "Test",
            "price": "9.99",
            "available": True,
            "category": "NONEXISTENT_CATEGORY"
        }
        self.assertRaises(DataValidationError, product.deserialize, bad_data)
    
    def test_init_db(self):
        """It should initialize the database"""
        from service.models import init_db
        from flask import Flask
        test_app = Flask(__name__)
        test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        init_db(test_app)  # should not raise

    def test_deserialize_type_error(self):
        """It should raise DataValidationError on TypeError"""
        product = Product()
        self.assertRaises(
            DataValidationError,
            product.deserialize,
            None  # None causa TypeError
        )


if __name__ == "__main__":
    unittest.main()
