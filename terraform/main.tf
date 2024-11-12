terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
    resource_group_name  = "Cohort30_FarWan_ProjectExercise"
    storage_account_name = "todotfstateacc"
    container_name       = "tfstatestore"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.SUBSCRIPTION_ID
  client_id = var.CLIENT_ID
  client_secret = var.CLIENT_SECRET
  tenant_id = var.TENANT_ID
}

data "azurerm_resource_group" "main" {
  name = var.RESOURCE_GROUP_NAME
}


resource "azurerm_service_plan" "main" {
  name                = "todo_app_appservice_plantf"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "fwtodoapptf"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name   = var.DOCKER_IMAGE_NAME
      docker_registry_url = "https://index.docker.io"

    }
  }

  app_settings = {
    FLASK_APP                           = var.FLASK_APP
    FLASK_DEBUG                         = var.FLASK_DEBUG
    SECRET_KEY                          = var.SECRET_KEY
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = var.WEBSITES_ENABLE_APP_SERVICE_STORAGE
    WEBSITES_PORT                       = var.WEBSITES_PORT
    MONGODB_COLLECTION_NAME             = var.MONGODB_COLLECTION_NAME
    MONGODB_NAME                        = var.MONGODB_NAME
    MONGODB_CONNECTIONSTRING            = azurerm_cosmosdb_account.main.primary_mongodb_connection_string

  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = var.COSMOSDB_ACCOUNT
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"


  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }
  capabilities {
    name = "EnableServerless"
  }

  lifecycle { prevent_destroy = true }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }

}

data "azurerm_cosmosdb_account" "db" {
  name                = var.COSMOSDB_ACCOUNT
  resource_group_name = var.RESOURCE_GROUP_NAME
}

resource "azurerm_cosmosdb_mongo_database" "db" {
  name                = var.MONGODB_NAME
  resource_group_name = data.azurerm_cosmosdb_account.db.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.db.name

}

resource "azurerm_cosmosdb_mongo_collection" "db" {
  name                = var.MONGODB_COLLECTION_NAME
  resource_group_name = data.azurerm_cosmosdb_account.db.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.db.name
  database_name       = azurerm_cosmosdb_mongo_database.db.name


  index {
    keys   = ["_id"]
    unique = true
  }
}



