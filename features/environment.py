"""
Environment setup for Behave BDD tests
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def before_all(context):
    """Configura el driver de Selenium antes de todos los tests"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")

    # Intentar con chromedriver del sistema
    try:
        service = Service("/usr/bin/chromedriver")
        context.driver = webdriver.Chrome(service=service, options=options)
    except Exception:
        try:
            context.driver = webdriver.Chrome(options=options)
        except Exception:
            # Fallback: Firefox si está disponible
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            ff_options = FirefoxOptions()
            ff_options.add_argument("--headless")
            context.driver = webdriver.Firefox(options=ff_options)

    context.driver.implicitly_wait(5)
    context.base_url = os.environ.get("BASE_URL", "http://localhost:8080")
    context.clipboard = ""


def after_all(context):
    """Cierra el navegador después de todos los tests"""
    if hasattr(context, "driver"):
        context.driver.quit()


def before_scenario(context, scenario):
    context.clipboard = ""


def after_scenario(context, scenario):
    if scenario.status == "failed" and hasattr(context, "driver"):
        os.makedirs("screenshots", exist_ok=True)
        scenario_name = scenario.name.replace(" ", "_")
        context.driver.save_screenshot(f"screenshots/{scenario_name}.png")
