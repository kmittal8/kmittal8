import os
import platform
import oci
import streamlit as st
import pandas as pd
from io import BytesIO
import requests  # Import requests to fetch current public IP

# Load OCI Config
config = oci.config.from_file(
    os.path.join("C:\\code\\oci_kmittal_tenancy\\config_kmittal.txt" if platform.system() == "Windows" else "/home/user/mypycode/oci_api/config.txt")
)

# Function to list security lists with ingress rule 0.0.0.0/0. This will display all regions.
def list_security_lists():
    identity_client = oci.identity.IdentityClient(config)
    regions = identity_client.list_region_subscriptions(config['tenancy']).data
    data = []

    for region in regions:
        config['region'] = region.region_name
        core_client = oci.core.VirtualNetworkClient(config)
        
        for compartment in identity_client.list_compartments(compartment_id=config['tenancy'], lifecycle_state="ACTIVE").data:
            security_lists = core_client.list_security_lists(compartment_id=compartment.id).data
            
            for sl in security_lists:
                # Check for ingress rules with source 0.0.0.0/0
                if any(rule.source == '0.0.0.0/0' for rule in sl.ingress_security_rules):
                    defined_tags = sl.defined_tags if sl.defined_tags else {}
                    
                    # Extract relevant ingress rule information
                    ingress_rules_summary = [
                        f"Source: {rule.source}, Protocol: {rule.protocol}" 
                        for rule in sl.ingress_security_rules
                    ]
                    
                    data.append({
                        "Region": region.region_name,
                        "Compartment": compartment.name,
                        "Security List Name": sl.display_name,
                        "OCID": sl.id,
                        "Defined Tags": defined_tags,  # Include defined tags
                        "Ingress Rules": "; ".join(ingress_rules_summary)  # Join summaries into a string
                    })
    return data

# Function to update ingress rules with the current public IP.
def update_ingress_rules(security_list_id, region_name, current_public_ip):
    config['region'] = region_name  # Update the region in the config
    core_client = oci.core.VirtualNetworkClient(config)
    security_list = core_client.get_security_list(security_list_id).data
    
    # Identify existing ingress rules
    updated_rules = []
    public_ip_exists = False
    zero_rule_exists = False

    # Check for existing public IP and 0.0.0.0/0
    for rule in security_list.ingress_security_rules:
        if rule.source == f"{current_public_ip}/32":
            public_ip_exists = True  # Mark that the public IP already exists
        elif rule.source == '0.0.0.0/0':
            zero_rule_exists = True  # Mark that 0.0.0.0/0 exists and will be replaced
            continue  # Skip adding the original 0.0.0.0/0 rule
        
        # Add other rules as is
        updated_rules.append(rule)

    # Remove the existing public IP if it exists
    if public_ip_exists:
        updated_rules = [rule for rule in updated_rules if rule.source != f"{current_public_ip}/32"]

    # If 0.0.0.0/0 was found, replace it with the current public IP
    if zero_rule_exists:
        updated_rules.append(
            oci.core.models.IngressSecurityRule(
                description='Updated access from public IP',
                source=f"{current_public_ip}/32",
                source_type='CIDR_BLOCK',
                is_stateless=False,
                protocol='all'  # All protocols
            )
        )
    else:
        # If the current public IP does not already exist, add it
        updated_rules.append(
            oci.core.models.IngressSecurityRule(
                description='Updated access from public IP',
                source=f"{current_public_ip}/32",
                source_type='CIDR_BLOCK',
                is_stateless=False,
                protocol='all'  # All protocols
            )
        )

    # Update the security list with the new ingress rules
    core_client.update_security_list(
        security_list_id, 
        oci.core.models.UpdateSecurityListDetails(ingress_security_rules=updated_rules)
    )

# Fetch Current Public IP
current_public_ip = requests.get('https://api.ipify.org').text

# Streamlit App
st.title("OCI Security Lists Management")

# Fetch and display the security lists
security_lists = list_security_lists()
if security_lists:
    df = pd.DataFrame(security_lists)
    st.dataframe(df)

    # Create an in-memory Excel file
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Security Lists')
    excel_buffer.seek(0)

    # Download button for the Excel file
    st.download_button(
        label="Download Excel",
        data=excel_buffer,
        file_name="security_lists.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Update ingress rules with current public IP button
    if st.button("Update Ingress Rules with Public IP"):
        progress_bar = st.progress(0)  # Initialize progress bar
        total_security_lists = len(security_lists)

        for index, sl in enumerate(security_lists):
            update_ingress_rules(sl["OCID"], sl["Region"], current_public_ip)
            progress_bar.progress((index + 1) / total_security_lists)  # Update progress

        st.success("Ingress rules have been updated with the current public IP.")
else:
    st.write("No security lists found with ingress rule 0.0.0.0/0.")
