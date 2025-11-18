# Output values

output "vcn_id" {
  description = "The OCID of the VCN"
  value       = oci_core_vcn.example_vcn.id
}

output "vcn_name" {
  description = "The display name of the VCN"
  value       = oci_core_vcn.example_vcn.display_name
}

output "subnet_id" {
  description = "The OCID of the subnet"
  value       = oci_core_subnet.example_subnet.id
}

output "internet_gateway_id" {
  description = "The OCID of the Internet Gateway"
  value       = oci_core_internet_gateway.example_ig.id
}

output "region" {
  description = "The OCI region"
  value       = var.region
}
