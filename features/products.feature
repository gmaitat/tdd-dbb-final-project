Feature: Product Catalog Administration
  As a Product Manager
  I need to be able to Create, Read, Update and Delete Products
  So that I can manage the products in the catalog

  Background:
    Given the following products
      | name    | description          | price | available | category   |
      | Hat     | A red fedora         | 59.95 | True      | CLOTHS     |
      | Shoes   | Blue shoes           | 125.00| True      | CLOTHS     |
      | Big Mac | 1/4 lb burger        | 5.99  | True      | FOOD       |
      | Sheets  | King size bed sheets | 87.00 | True      | HOUSEWARES |

  ##############################################################
  # Crear un Producto (ya dado como ejemplo)
  ##############################################################
  Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hammer"
    And I set the "Description" to "A steel hammer"
    And I select "True" in the "Available" dropdown
    And I select "TOOLS" in the "Category" dropdown
    And I set the "Price" to "34.95"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hammer" in the "Name" field
    And I should see "A steel hammer" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "TOOLS" in the "Category" dropdown
    And I should see "34.95" in the "Price" field

  ##############################################################
  # Leer un Producto
  ##############################################################
  Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "CLOTHS" in the "Category" dropdown
    And I should see "59.95" in the "Price" field

  ##############################################################
  # Actualizar un Producto
  ##############################################################
  Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    When I set the "Description" to "A blue hat"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "A blue hat" in the "Description" field

  ##############################################################
  # Eliminar un Producto
  ##############################################################
  Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    When I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"

  ##############################################################
  # Listar todos los Productos
  ##############################################################
  Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should not see "Hammer" in the results

  ##############################################################
  # Buscar Productos por Categoría
  ##############################################################
  Scenario: Search Products by Category
    When I visit the "Home Page"
    And I select "CLOTHS" in the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should not see "Big Mac" in the results
    And I should not see "Sheets" in the results

  ##############################################################
  # Buscar Productos por Disponibilidad
  ##############################################################
  Scenario: Search Products by Availability
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

  ##############################################################
  # Buscar Productos por Nombre
  ##############################################################
  Scenario: Search Products by Name
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Big Mac" in the results
    And I should not see "Sheets" in the results
