# Terraform Oracle Cloud Infrastructure (OCI) Provider Sample

This repository contains sample Terraform scripts to connect to and provision resources in Oracle Cloud Infrastructure (OCI).

## Prerequisites

1. **Terraform**: Install Terraform (>= 1.0)
   ```bash
   # Download from https://www.terraform.io/downloads
   ```

2. **OCI Account**: Active Oracle Cloud Infrastructure account

3. **OCI CLI** (Optional but recommended):
   ```bash
   # Install OCI CLI
   bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
   ```

4. **API Key**: Generate an API key pair for OCI authentication

## Setting Up OCI Authentication

### Step 1: Generate API Key Pair

```bash
# Create .oci directory
mkdir -p ~/.oci

# Generate private key
openssl genrsa -out ~/.oci/oci_api_key.pem 2048

# Generate public key
openssl rsa -pubout -in ~/.oci/oci_api_key.pem -out ~/.oci/oci_api_key_public.pem

# Set proper permissions
chmod 600 ~/.oci/oci_api_key.pem
```

### Step 2: Add Public Key to OCI Console

1. Log in to OCI Console
2. Navigate to: User Settings → API Keys
3. Click "Add API Key"
4. Upload or paste the content of `~/.oci/oci_api_key_public.pem`
5. Copy the fingerprint displayed

### Step 3: Gather Required OCIDs

You'll need the following OCIDs from the OCI Console:

- **Tenancy OCID**: Profile → Tenancy → OCID
- **User OCID**: Profile → User Settings → OCID
- **Compartment OCID**: Identity → Compartments → Select compartment → OCID
- **Region**: Your preferred region (e.g., `us-ashburn-1`, `us-phoenix-1`)

## Configuration

### 1. Copy the example tfvars file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

### 2. Edit `terraform.tfvars` with your values:

```hcl
tenancy_ocid     = "ocid1.tenancy.oc1..aaaaaaaa..."
user_ocid        = "ocid1.user.oc1..aaaaaaaa..."
fingerprint      = "aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99"
private_key_path = "~/.oci/oci_api_key.pem"
region           = "us-ashburn-1"
compartment_ocid = "ocid1.compartment.oc1..aaaaaaaa..."
```

**Important**: Never commit `terraform.tfvars` to version control!

## Files in this Repository

- **provider.tf**: OCI provider configuration with multiple authentication methods
- **variables.tf**: Variable definitions
- **terraform.tfvars.example**: Example variable values (copy to terraform.tfvars)
- **main.tf**: Sample resources (VCN, subnet, internet gateway, route table)
- **outputs.tf**: Output values after deployment
- **.gitignore**: Prevents committing sensitive files

## Usage

### Initialize Terraform:

```bash
terraform init
```

### Validate Configuration:

```bash
terraform validate
```

### Plan Deployment:

```bash
terraform plan
```

### Apply Configuration:

```bash
terraform apply
```

### Destroy Resources:

```bash
terraform destroy
```

## Authentication Methods

This sample supports multiple authentication methods:

### 1. API Key (Default - Recommended for local development)
```hcl
provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}
```

### 2. Instance Principal (For resources running in OCI)
```hcl
provider "oci" {
  auth   = "InstancePrincipal"
  region = var.region
}
```

### 3. Resource Principal (For OCI Functions)
```hcl
provider "oci" {
  auth   = "ResourcePrincipal"
  region = var.region
}
```

### 4. Security Token (Using OCI CLI session)
```hcl
provider "oci" {
  auth                = "SecurityToken"
  config_file_profile = "DEFAULT"
  region              = var.region
}
```

## Example Resources

This sample creates:

- **VCN (Virtual Cloud Network)**: A private network in OCI
- **Internet Gateway**: Allows internet connectivity
- **Route Table**: Routes traffic to the internet gateway
- **Subnet**: A subnet within the VCN

## Available OCI Regions

Common OCI regions:
- `us-ashburn-1` (US East - Ashburn)
- `us-phoenix-1` (US West - Phoenix)
- `uk-london-1` (UK South - London)
- `eu-frankfurt-1` (Germany Central - Frankfurt)
- `ap-tokyo-1` (Japan East - Tokyo)
- `ap-mumbai-1` (India West - Mumbai)

[Full list of regions](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm)

## Troubleshooting

### "401 Unauthorized" Error
- Verify your API key fingerprint matches in OCI Console
- Check that the private key path is correct
- Ensure the user has proper permissions

### "404 Not Found" Error
- Verify all OCIDs are correct
- Ensure you have access to the specified compartment
- Check that resources exist in the specified region

### Permission Errors
- Verify your user has the required IAM policies
- Check compartment-level permissions

## Security Best Practices

1. Never commit `terraform.tfvars` or `.pem` files
2. Use least-privilege IAM policies
3. Rotate API keys regularly
4. Use Instance/Resource Principal authentication for production workloads
5. Store sensitive values in environment variables or secure vaults

## Additional Resources

- [OCI Terraform Provider Documentation](https://registry.terraform.io/providers/oracle/oci/latest/docs)
- [OCI Documentation](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [Terraform OCI Examples](https://github.com/oracle/terraform-provider-oci/tree/master/examples)

## License

This is sample code for educational purposes.
