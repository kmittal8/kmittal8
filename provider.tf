terraform {
  required_version = ">= 1.0"

  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 5.0.0"
    }
  }
}

# OCI Provider Configuration
provider "oci" {
  # Authentication via API Key
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region

  # Alternative: Authentication via Instance Principal (for resources running in OCI)
  # auth = "InstancePrincipal"

  # Alternative: Authentication via Resource Principal (for OCI Functions)
  # auth = "ResourcePrincipal"

  # Alternative: Authentication via Security Token
  # auth                = "SecurityToken"
  # config_file_profile = "DEFAULT"
}
