variable "FLASK_APP" {
  type = string
}

variable "FLASK_DEBUG" {
  type = string
}

variable "WEBSITES_ENABLE_APP_SERVICE_STORAGE" {
  type = string
}

variable "SECRET_KEY" {
  type = string
}

variable "WEBSITES_PORT" {
  type = string
}

variable "MONGODB_COLLECTION_NAME" {
  type = string

}

variable "MONGODB_NAME" {
  type = string

}

variable "SUBSCRIPTION_ID" {
  type      = string
  sensitive = true

}

variable "RESOURCE_GROUP_NAME" {
  type      = string
  sensitive = true

}

variable "COSMOSDB_ACCOUNT" {
  type = string

}

variable "DOCKER_IMAGE_NAME" {
  type = string

}

variable "STORAGE_ACCOUNT_NAME" {
  type = string

}

variable "CONTAINER_NAME" {
  type = string

}
