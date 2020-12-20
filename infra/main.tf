# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.26"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "hello-world-rg"
  location = "eastus2"
}

resource "random_string" "default" {
  length  = 24
  special = false
  lower   = true
  upper   = false
}

resource "azurerm_storage_account" "default" {
  name                     = random_string.default.result
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  allow_blob_public_access = true
}

resource "azurerm_storage_container" "default" {
  name                  = "images"
  storage_account_name  = azurerm_storage_account.default.name
  container_access_type = "container"
}

resource "random_string" "db_password" {
  length           = 32
  special          = true
  override_special = ",._+:@%/-"
}

resource "random_string" "serverdb" {
  length  = 24
  special = false
  lower   = true
  upper   = false
}

resource "azurerm_sql_server" "default" {
  name                         = random_string.serverdb.result
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "lzhu"
  administrator_login_password = random_string.db_password.result
}

resource "azurerm_sql_firewall_rule" "azureaccess" {
  name                = "azureaccess"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_sql_server.default.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

data "http" "mypublicip" {
  url = "http://ifconfig.me"
}

resource "azurerm_sql_firewall_rule" "clientip" {
  name                = "clientip"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_sql_server.default.name
  start_ip_address    = data.http.mypublicip.body
  end_ip_address      = data.http.mypublicip.body
}

resource "azurerm_sql_database" "default" {
  name                = "hello-world-db"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.default.name
  edition             = "Basic"
}
