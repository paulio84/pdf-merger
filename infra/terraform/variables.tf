variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "environment" {
  description = "Deployment environment name (test or prod)"
  type        = string

  validation {
    condition     = contains(["test", "prod"], var.environment)
    error_message = "Environment must be 'test' or 'prod'."
  }
}

variable "location" {
  description = "Azure region to deploy resources into"
  type        = string
  default     = "uksouth"
}

variable "image_tag" {
  description = "Container image tag to deploy"
  type        = string
  default     = "latest"
}

variable "min_replicas" {
  description = "Minimum number of container replicas"
  type        = number
  default     = 0
}

variable "max_replicas" {
  description = "Maximum number of container replicas"
  type        = number
  default     = 1
}

variable "cors_allowed_origins" {
  description = "List of allowed CORS origins"
  type        = list(string)
}

variable "rate_limit" {
  description = "Rate limit string e.g. 100/minute"
  type        = string
  default     = "10/minute"
}
