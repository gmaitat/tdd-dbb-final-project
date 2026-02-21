"""
Test Cases for Product Model
"""
import unittest
from decimal import Decimal
from service.routes import app
from service.models import Product, Category, DataValidationError, db

DATABASE_URI = "sqlite:///:memory:"

PRODUCT_DATA = {
    "name": "Test Product",
    "description": "A test product",
    "price": "10.99",
    "available": True,
    "category": "FOOD"
}


class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(
            name="Test",
            description="A test",
            price=Decimal("9.99"),
            available=True,
            category=Category.FOOD,
        )
        self.assertIsNotNone(product)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Test")
        self.assertEqual(product.price, Decimal("9.99"))
        self.assertEqual(product.available, True)
        self.assertEqual(product.category, Category.FOOD)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(**{**PRODUCT_DATA, "price": Decimal("10.99"), "category": Category.FOOD})
        product.create()
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """It should Read a Product"""
        product = Product(**{**PRODUCT_DATA, "price": Decimal("10.99"), "category": Category.FOOD})
        product.create()
        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = Product(**{**PRODUCT_DATA, "price": Decimal("10.99"), "category": Category.FOOD})
        product.create()
        product.description = "Updated description"
        product.update()
        found = Product.find(product.id)
        self.assertEqual(found.description, "Updated description")

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = Product(**{**PRODUCT_DATA, "price": Decimal("10.99"), "category": Category.FOOD})
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_serialize_a_product(self):
        """It should Serialize a Product"""
        product = Product(**{**PRODUCT_DATA, "price": Decimal("10.99"), "category": Category.FOOD})
        serial_product = product.serialize()
        self.assertEqual(serial_product["name"], product.name)
        self.assertEqual(serial_product["category"], "FOOD")

    def test_deserialize_a_product(self):
        """It should Deserialize a Product"""
        product = Product()
        product.deserialize(PRODUCT_DATA)
        self.assertEqual(product.name, PRODUCT_DATA["name"])
        self.assertEqual(product.category, Category.FOOD)

    def test_deserialize_missing_data(self):
        """It should not Deserialize a Product with missing data"""
        product = Product()
        bad_data = {"name": "test"}
        self.assertRaises(DataValidationError, product.deserialize, bad_data)

    def test_find_by_name(self):
        """It should Find Products by Name"""
        product = Product(**{**PRODUCT_DATA, "price": Decimal("10.99"), "category": Category.FOOD})
        product.create()
        results = Product.find_by_name(product.name)
        self.assertEqual(results.count(), 1)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        product = Product(**{**PRODUCT_DATA, "price": Decimal("10.99"), "category": Category.FOOD})
        product.create()
        results = Product.find_by_category(Category.FOOD)
        self.assertEqual(results.count(), 1)

    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        product = Product(**{**PRODUCT_DATA, "price": Decimal("10.99"), "category": Category.FOOD})
        product.create()
        results = Product.find_by_availability(True)
        self.assertEqual(results.count(), 1)


if __name__ == "__main__":
    unittest.main()
