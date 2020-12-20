output "storage_acc_name" {
  value = azurerm_storage_account.default.name
}

output "sql_user_name" {
  value = azurerm_sql_server.default.administrator_login
}

output "sql_server" {
  value = azurerm_sql_server.default.fully_qualified_domain_name
}

output "sql_password" {
  value = azurerm_sql_server.default.administrator_login_password
}

output "sql_database" {
  value = azurerm_sql_database.default.name
}

output "blob_account" {
  value = azurerm_storage_account.default.name
}

output "blob_storage_key" {
  value = azurerm_storage_account.default.primary_access_key
}

output "blob_container" {
  value = azurerm_storage_container.default.name
}
