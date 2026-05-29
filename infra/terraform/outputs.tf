output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "container_app_name" {
  description = "Name of the container app"
  value       = azurerm_container_app.api.name
}

output "container_app_url" {
  description = "Public URL of the container app"
  value       = "https://${azurerm_container_app.api.ingress[0].fqdn}"
}
