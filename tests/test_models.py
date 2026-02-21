"""
Test Cases for Product Model
"""
import unittest
import logging
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
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        db.session.close()

    def setUp(self):
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    # ------------------------------------------------------------------ #
    # Caso de Prueba: Leer un Producto
    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    # Caso de Prueba: Actualizar un Producto
    # ------------------------------------------------------------------ #
    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        logger.debug("Testing product: %s", product)
        product.id = None
        product.create()
        logger.debug("Product created: %s", product)
        original_id = product.id
        product.description = "Updated description for testing"
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "Updated description for testing")
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "Updated description for testing")

    # ------------------------------------------------------------------ #
    # Caso de Prueba: Eliminar un Producto
    # ------------------------------------------------------------------ #
    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    # ------------------------------------------------------------------ #
    # Caso de Prueba: Listar Todos los Productos
    # ------------------------------------------------------------------ #
    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        for _ in range(5):
            product = ProductFactory()
            product.create()
        products = Product.all()
        self.assertEqual(len(products), 5)

    # ------------------------------------------------------------------ #
    # Caso de Prueba: Buscar por Nombre
    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    # Caso de Prueba: Buscar por Disponibilidad
    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    # Caso de Prueba: Buscar por Categoría
    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    # Tests adicionales de robustez
    # ------------------------------------------------------------------ #
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


if __name__ == "__main__":
    unittest.main()
