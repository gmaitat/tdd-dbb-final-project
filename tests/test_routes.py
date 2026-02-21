"""
Test Cases for Product REST API Routes
"""
import unittest
import logging
from urllib.parse import quote_plus
from service.models import Product, Category, db
from tests.factories import ProductFactory

DATABASE_URI = "sqlite:///:memory:"
BASE_URL = "/products"
logger = logging.getLogger(__name__)

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415


def _create_products(client, count):
    """Helper: crea productos via POST"""
    products = []
    for _ in range(count):
        product = ProductFactory()
        resp = client.post(
            BASE_URL,
            json=product.serialize(),
            content_type="application/json",
        )
        assert resp.status_code == HTTP_201_CREATED, resp.data
        products.append(resp.get_json())
    return products


class TestProductRoutes(unittest.TestCase):
    """Test Cases for Product REST API Routes"""

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests"""
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy

        # Crear app fresca solo para tests
        cls.app = Flask(__name__)
        cls.app.config["TESTING"] = True
        cls.app.config["DEBUG"] = False
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Registrar db y modelo
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

        # Registrar rutas
        from service import routes as r
        # Reusar el app de routes pero reconfigurar
        r.app.config["TESTING"] = True
        r.app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        r.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        Product.init_db(r.app)
        cls.client = r.app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.close()

    def setUp(self):
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    # ------------------------------------------------------------------ #
    # Health check
    # ------------------------------------------------------------------ #
    def test_health(self):
        """It should return health status OK"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, HTTP_200_OK)

    # ------------------------------------------------------------------ #
    # Leer un Producto
    # ------------------------------------------------------------------ #
    def test_get_product(self):
        """It should Read a single Product"""
        test_product = _create_products(self.client, 1)[0]
        resp = self.client.get(f"{BASE_URL}/{test_product['id']}")
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product["name"])
        self.assertEqual(data["description"], test_product["description"])
        self.assertEqual(data["price"], test_product["price"])
        self.assertEqual(data["available"], test_product["available"])
        self.assertEqual(data["category"], test_product["category"])

    def test_get_product_not_found(self):
        """It should return 404 when Product is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    # ------------------------------------------------------------------ #
    # Actualizar un Producto
    # ------------------------------------------------------------------ #
    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = _create_products(self.client, 1)[0]
        test_product["description"] = "Updated description"
        resp = self.client.put(
            f"{BASE_URL}/{test_product['id']}",
            json=test_product,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, HTTP_200_OK)
        updated = resp.get_json()
        self.assertEqual(updated["description"], "Updated description")

    def test_update_product_not_found(self):
        """It should return 404 when updating a non-existent Product"""
        product = ProductFactory()
        resp = self.client.put(
            f"{BASE_URL}/0",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    # ------------------------------------------------------------------ #
    # Eliminar un Producto
    # ------------------------------------------------------------------ #
    def test_delete_product(self):
        """It should Delete a Product"""
        products = _create_products(self.client, 5)
        test_product = products[0]
        resp = self.client.delete(f"{BASE_URL}/{test_product['id']}")
        self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)
        resp = self.client.get(f"{BASE_URL}/{test_product['id']}")
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    # ------------------------------------------------------------------ #
    # Listar todos
    # ------------------------------------------------------------------ #
    def test_get_all_products(self):
        """It should List all Products"""
        _create_products(self.client, 5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    # ------------------------------------------------------------------ #
    # Filtrar por Nombre
    # ------------------------------------------------------------------ #
    def test_query_by_name(self):
        """It should List Products filtered by name"""
        products = _create_products(self.client, 5)
        test_name = products[0]["name"]
        count = len([p for p in products if p["name"] == test_name])
        resp = self.client.get(f"{BASE_URL}?name={quote_plus(test_name)}")
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), count)
        for p in data:
            self.assertEqual(p["name"], test_name)

    # ------------------------------------------------------------------ #
    # Filtrar por Categoría
    # ------------------------------------------------------------------ #
    def test_query_by_category(self):
        """It should List Products filtered by category"""
        products = _create_products(self.client, 10)
        test_category = products[0]["category"]
        count = len([p for p in products if p["category"] == test_category])
        resp = self.client.get(f"{BASE_URL}?category={test_category}")
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), count)
        for p in data:
            self.assertEqual(p["category"], test_category)

    # ------------------------------------------------------------------ #
    # Filtrar por Disponibilidad
    # ------------------------------------------------------------------ #
    def test_query_by_availability(self):
        """It should List Products filtered by availability"""
        products = _create_products(self.client, 10)
        test_available = products[0]["available"]
        count = len([p for p in products if p["available"] == test_available])
        resp = self.client.get(f"{BASE_URL}?available={str(test_available).lower()}")
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), count)
        for p in data:
            self.assertEqual(p["available"], test_available)

    # ------------------------------------------------------------------ #
    # Crear Producto
    # ------------------------------------------------------------------ #
    def test_create_product(self):
        """It should Create a new Product"""
        product = ProductFactory()
        resp = self.client.post(
            BASE_URL,
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertIsNotNone(resp.headers.get("Location"))
        data = resp.get_json()
        self.assertEqual(data["name"], product.name)

    def test_create_product_no_content_type(self):
        """It should return 415 if Content-Type is missing"""
        resp = self.client.post(BASE_URL, data="bad data")
        self.assertEqual(resp.status_code, HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """It should return 405 for invalid methods"""
        resp = self.client.delete(BASE_URL)
        self.assertEqual(resp.status_code, HTTP_405_METHOD_NOT_ALLOWED)


if __name__ == "__main__":
    unittest.main()
