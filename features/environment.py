"""
Environment setup for Behave BDD tests
Configura y destruye el navegador Selenium para cada escenario
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    """Configura el driver de Selenium antes de todos los tests"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(5)
    context.base_url = os.environ.get("BASE_URL", "http://localhost:8080")
    context.clipboard = ""


def after_all(context):
    """Cierra el navegador después de todos los tests"""
    context.driver.quit()


def before_scenario(context, scenario):
    """Acciones antes de cada escenario"""
    context.clipboard = ""


def after_scenario(context, scenario):
    """Acciones después de cada escenario (limpiar si falla)"""
    if scenario.status == "failed":
        scenario_name = scenario.name.replace(" ", "_")
        context.driver.save_screenshot(f"screenshots/{scenario_name}.png")
