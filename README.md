- 👋 Hi, I’m @kmittal8
- 👀 I’m in the process of learning.. 


<!---
kmittal8/kmittal8 is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

# OCI Security Lists Management

This project provides a Streamlit application that helps manage security lists in Oracle Cloud Infrastructure (OCI). The application lists security lists with ingress rules and allows users to update those rules with their current public IP address.

## Features

- List security lists with ingress rule `0.0.0.0/0`.
- Update ingress rules with the current public IP.
- Download security lists as an Excel file.

## Configuration

Before running the application, make sure to set up your OCI configuration. Follow the steps below:

1. **OCI Config File**: Create a configuration file for your OCI account. You can use the following structure:

    ```ini
    [DEFAULT]
    user=ocid1.user.oc1..your_user_ocid
    fingerprint=your_fingerprint
    key_file=/path/to/your/private/key.pem
    tenancy=ocid1.tenancy.oc1..your_tenancy_ocid
    region=us-ashburn-1
    ```

2. **Adjust the Path**: Make sure to adjust the path to your configuration file in the code.

## Requirements

- Python 3.x
- Streamlit
- OCI SDK for Python
- Pandas
- OpenPyXL
- Requests

You can install the required packages using pip: 

```bash 
pip install streamlit oci pandas openpyxl requests
```
## How to Run

1. Clone this repository to your local machine:
```bash 
git clone https://github.com/kmittal8/your-repo-name.git
```
2. Navigate to the project directory:
  ```bash 
cd your-repo-name
```
3. Run the Streamlit application:
```bash 
streamlit run app.py
```
4. Open your browser and go to http://localhost:8501 to view the application.

