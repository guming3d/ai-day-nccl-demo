import os
import argparse
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import (IdentityConfiguration, AmlCompute, AmlComputeSshSettings, ComputeInstance)
from azure.ai.ml.constants import ManagedServiceIdentityType

# Set up argument parser
parser = argparse.ArgumentParser(description="Create Azure ML compute resources.")
parser.add_argument("--compute", action="store_true", help="Create a compute instance instead of a compute cluster.")
parser.add_argument("--cluster", action="store_true", default=True, help="Create a compute cluster (default action).")
args = parser.parse_args()

# Retrieve details from environment variables
subscription_id = os.getenv('SUBSCRIPTION_ID')
resource_group = os.getenv('RESOURCE_GROUP')
work_space = os.getenv('WORKSPACE_NAME')
cluster_name = os.getenv('CLUSTER_NAME')

# get a handle to the workspace
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, work_space)

# Create an identity configuration for a system-assigned managed identity
identity_config = IdentityConfiguration(type=ManagedServiceIdentityType.SYSTEM_ASSIGNED)

# Common SSH settings for both compute cluster and compute instance
cluster_ssh = AmlComputeSshSettings(
    admin_username="azureuser",
    ssh_key_value="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDes4CR/XbYZElNaSO5F/BdoR/KvbEyyzKrMzDGDE2nJftgxObnP0dedVsLm49jLu93v2XUXtYQq1TXC3fH+PpEAnFqJ1OK6na5NRYbjKqxAVtf7VM7FqvASZxkf/u8aI1S5Dz1Uyqj/DPYtjXWyNMHGqiAuCUaTgHjf7W7kwfwEVFXQL5YYVyM6Vkre0Ytzilhoyg0vJec5mrcSzEd5KukP6XwZg/81CD4EDOVH1iEPeWF9JFCzcMmQo9cAZJmUMJVNXIBRQVgwNpnNG5eSgXUr+FopzEykyiznOUThSDQDfYYFsmna/7Vz7OSMXpGrqV6vOUE9TXPIPNPaIBa0XDaRD2TcjrhWuOP1vjPd9sL0z2lth67SmQUVV2rGcN53kqQXF1o5fMjmZdcLyiqHtDxv0T9piRpU+0wUOGODNlTj3NU8suFKKEzH9FH5AMldCquCoLIHzel5yg7G7NGUtHAxNg1ux9iPa4MW2oKMQQ0KvcugVoQWJPMYMm9EfFumd0= minggu@minggu-laptop",
    )

# compute_size="Standard_ND96asr_v4" #"Standard_ND96amsr_A100_v4"
compute_size="Standard_NC24ads_A100_v4" #"Standard_ND96amsr_A100_v4"

if args.compute:
    # Code to create a compute instance
    compute_instance = ComputeInstance(
        name=cluster_name,
        type="ComputeInstance",
        size=compute_size,
        ssh_public_access_enabled=True,
        ssh_settings=cluster_ssh,
        identity=identity_config)
    
    operation = ml_client.begin_create_or_update(compute_instance)
    result = operation.result()
    print(f"Compute instance '{cluster_name}' has been created/updated.")
    print(f"Compute instance information: {result}")

elif args.cluster:
    # Existing code to create a compute cluster
    cluster_basic = AmlCompute(
        name=cluster_name,
        type="amlcompute",
        size=compute_size,
        ssh_public_access_enabled=True,
        ssh_settings=cluster_ssh,
        min_instances=0,
        max_instances=2,
        idle_time_before_scale_down=900,
        identity=identity_config)

    operation = ml_client.begin_create_or_update(cluster_basic)
    result = operation.result()
    print(f"Cluster '{cluster_name}' has been created/updated.")
    print(f"Cluster information: {result}")
