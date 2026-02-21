"""
Load Steps for BDD - Cargar datos de fondo para escenarios BDD
"""
import requests
from behave import given  # pylint: disable=no-name-in-module

# URL base del servicio
BASE_URL = "http://localhost:8080"
PRODUCTS_URL = f"{BASE_URL}/products"


@given("the following products")
def step_load_products_from_table(context):
    """Elimina todos los productos existentes y carga los de la tabla background"""
    # 1. Eliminar todos los productos existentes
    resp = requests.get(PRODUCTS_URL, timeout=10)
    assert resp.status_code == 200, f"Failed to get products: {resp.status_code}"
    for product in resp.json():
        resp = requests.delete(
            f"{PRODUCTS_URL}/{product['id']}", timeout=10
        )
        assert resp.status_code == 204, f"Failed to delete product: {resp.status_code}"

    # 2. Cargar los productos desde context.table
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "available": row["available"].lower() in ["true", "yes", "1"],
            "category": row["category"].upper(),
        }
        resp = requests.post(PRODUCTS_URL, json=payload, timeout=10)
        assert resp.status_code == 201, (
            f"Failed to create product '{row['name']}': {resp.status_code} - {resp.text}"
        )
