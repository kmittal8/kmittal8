# Example: Create a Virtual Cloud Network (VCN)
resource "oci_core_vcn" "example_vcn" {
  compartment_id = var.compartment_ocid
  cidr_blocks    = [var.vcn_cidr_block]
  display_name   = "example-vcn-${var.environment}"
  dns_label      = "examplevcn"

  freeform_tags = {
    "Environment" = var.environment
    "ManagedBy"   = "Terraform"
  }
}

# Example: Create an Internet Gateway
resource "oci_core_internet_gateway" "example_ig" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.example_vcn.id
  display_name   = "example-ig-${var.environment}"
  enabled        = true

  freeform_tags = {
    "Environment" = var.environment
    "ManagedBy"   = "Terraform"
  }
}

# Example: Create a Route Table
resource "oci_core_route_table" "example_route_table" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.example_vcn.id
  display_name   = "example-route-table-${var.environment}"

  route_rules {
    network_entity_id = oci_core_internet_gateway.example_ig.id
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
  }

  freeform_tags = {
    "Environment" = var.environment
    "ManagedBy"   = "Terraform"
  }
}

# Example: Create a Subnet
resource "oci_core_subnet" "example_subnet" {
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.example_vcn.id
  cidr_block        = "10.0.1.0/24"
  display_name      = "example-subnet-${var.environment}"
  dns_label         = "examplesubnet"
  route_table_id    = oci_core_route_table.example_route_table.id
  security_list_ids = [oci_core_vcn.example_vcn.default_security_list_id]

  freeform_tags = {
    "Environment" = var.environment
    "ManagedBy"   = "Terraform"
  }
}
