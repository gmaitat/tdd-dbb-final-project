"""
Web Steps - Definiciones de pasos para pruebas BDD de la interfaz web
"""
import logging
from behave import when, then  # pylint: disable=no-name-in-module
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger("steps")

BASE_URL = "http://localhost:8080"

# Mapeo de nombres legibles → IDs/atributos HTML
ID_PREFIX = "product_"
FIELD_MAP = {
    "Id": "id",
    "Name": "name",
    "Description": "description",
    "Available": "available",
    "Category": "category",
    "Price": "price",
}
BUTTON_MAP = {
    "Search": "search-btn",
    "Clear": "clear-btn",
    "Create": "create-btn",
    "Update": "update-btn",
    "Retrieve": "retrieve-btn",
    "Delete": "delete-btn",
}


def wait_for_element(context, by, value, timeout=10):
    """Helper: espera hasta que un elemento sea visible"""
    return WebDriverWait(context.driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


##############################################################
# Navegar a la página de inicio
##############################################################
@when('I visit the "Home Page"')
def step_visit_home_page(context):
    """Navega a la página de inicio"""
    context.driver.get(BASE_URL)
    wait_for_element(context, By.ID, "search-btn")


##############################################################
# Establecer texto en un campo
##############################################################
@when('I set the "{field_name}" to "{text_string}"')
def step_set_field(context, field_name, text_string):
    """Establece texto en un campo de entrada"""
    element_id = f"{ID_PREFIX}{FIELD_MAP[field_name]}"
    element = wait_for_element(context, By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


##############################################################
# Seleccionar opción en dropdown
##############################################################
@when('I select "{text_string}" in the "{field_name}" dropdown')
def step_select_dropdown(context, text_string, field_name):
    """Selecciona un valor en un dropdown"""
    element_id = f"{ID_PREFIX}{FIELD_MAP[field_name]}"
    element = wait_for_element(context, By.ID, element_id)
    Select(element).select_by_visible_text(text_string)


##############################################################
# Presionar botón
##############################################################
@when('I press the "{button}" button')
def step_press_button(context, button):
    """Presiona un botón"""
    button_id = BUTTON_MAP[button]
    element = wait_for_element(context, By.ID, button_id)
    element.click()


##############################################################
# Copiar campo (guardar en context.clipboard)
##############################################################
@when('I copy the "{field_name}" field')
def step_copy_field(context, field_name):
    """Copia el valor de un campo al portapapeles del contexto"""
    element_id = f"{ID_PREFIX}{FIELD_MAP[field_name]}"
    element = wait_for_element(context, By.ID, element_id)
    context.clipboard = element.get_attribute("value")
    logger.info("Copied '%s' from field '%s'", context.clipboard, field_name)


##############################################################
# Pegar campo (desde context.clipboard)
##############################################################
@when('I paste the "{field_name}" field')
def step_paste_field(context, field_name):
    """Pega el valor del portapapeles en un campo"""
    element_id = f"{ID_PREFIX}{FIELD_MAP[field_name]}"
    element = wait_for_element(context, By.ID, element_id)
    element.clear()
    element.send_keys(context.clipboard)


##############################################################
# Verificar mensaje de estado
##############################################################
@then('I should see the message "{message}"')
def step_should_see_message(context, message):
    """Verifica que el mensaje de estado contiene el texto esperado"""
    status_element = wait_for_element(context, By.ID, "flash_message")
    assert message in status_element.text, (
        f"Expected message '{message}' but got '{status_element.text}'"
    )


##############################################################
# Verificar valor en campo de texto
##############################################################
@then('I should see "{text_string}" in the "{field_name}" field')
def step_should_see_in_field(context, text_string, field_name):
    """Verifica que un campo de texto contiene el valor esperado"""
    element_id = f"{ID_PREFIX}{FIELD_MAP[field_name]}"
    element = wait_for_element(context, By.ID, element_id)
    actual = element.get_attribute("value")
    assert text_string in actual, (
        f"Expected '{text_string}' in field '{field_name}' but found '{actual}'"
    )


##############################################################
# Verificar valor seleccionado en dropdown
##############################################################
@then('I should see "{text_string}" in the "{field_name}" dropdown')
def step_should_see_in_dropdown(context, text_string, field_name):
    """Verifica que un dropdown tiene el valor esperado seleccionado"""
    element_id = f"{ID_PREFIX}{FIELD_MAP[field_name]}"
    element = wait_for_element(context, By.ID, element_id)
    selected = Select(element).first_selected_option.text
    assert text_string in selected, (
        f"Expected '{text_string}' in dropdown '{field_name}' but found '{selected}'"
    )


##############################################################
# Verificar texto presente en la tabla de resultados
##############################################################
@then('I should see "{text_string}" in the results')
def step_should_see_in_results(context, text_string):
    """Verifica que el texto aparece en la tabla de resultados"""
    results = wait_for_element(context, By.ID, "search_results")
    assert text_string in results.text, (
        f"Expected '{text_string}' in results but it was not found.\nResults: {results.text}"
    )


##############################################################
# Verificar texto AUSENTE en la tabla de resultados
##############################################################
@then('I should not see "{text_string}" in the results')
def step_should_not_see_in_results(context, text_string):
    """Verifica que el texto NO aparece en la tabla de resultados"""
    results = wait_for_element(context, By.ID, "search_results")
    assert text_string not in results.text, (
        f"Expected '{text_string}' NOT to be in results but it was found.\nResults: {results.text}"
    )
