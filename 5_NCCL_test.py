import os
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, command, MpiDistribution

from azure.ai.ml.entities import (
    SshJobService,
    VsCodeJobService,
    JupyterLabJobService,
)

# Retrieve details from environment variables
subscription_id = os.getenv("SUBSCRIPTION_ID")
resource_group = os.getenv("RESOURCE_GROUP")
work_space = os.getenv("WORKSPACE_NAME")
cluster_name = os.getenv("CLUSTER_NAME")

# get a handle to the workspace
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, work_space
)

job = command(
    code="./src",  # local path where the code is stored
    command="bash NCCL.sh",
    environment="NCCL-Benchmark-Env-New:1.0",
    # command="bash gpu_perf.sh",
    # environment="nccltests_azureml:openmpi4.1.0-cuda11.1-cudnn8-ubuntu18.04",
    compute=cluster_name,
    instance_count=2,
    distribution=MpiDistribution(
        process_count_per_instance=1,
    ),
    services={
        "My_jupyterlab": JupyterLabJobService(),
        "My_vscode": VsCodeJobService(),
        "My_ssh": SshJobService(
            nodes="all",  # For distributed jobs, use the `nodes` property to pick which node you want to enable interactive services on. If `nodes` are not selected, by default, interactive applications are only enabled on the head node. Values are "all", or compute node index (for ex. "0", "1" etc.)
            ssh_public_keys="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDes4CR/XbYZElNaSO5F/BdoR/KvbEyyzKrMzDGDE2nJftgxObnP0dedVsLm49jLu93v2XUXtYQq1TXC3fH+PpEAnFqJ1OK6na5NRYbjKqxAVtf7VM7FqvASZxkf/u8aI1S5Dz1Uyqj/DPYtjXWyNMHGqiAuCUaTgHjf7W7kwfwEVFXQL5YYVyM6Vkre0Ytzilhoyg0vJec5mrcSzEd5KukP6XwZg/81CD4EDOVH1iEPeWF9JFCzcMmQo9cAZJmUMJVNXIBRQVgwNpnNG5eSgXUr+FopzEykyiznOUThSDQDfYYFsmna/7Vz7OSMXpGrqV6vOUE9TXPIPNPaIBa0XDaRD2TcjrhWuOP1vjPd9sL0z2lth67SmQUVV2rGcN53kqQXF1o5fMjmZdcLyiqHtDxv0T9piRpU+0wUOGODNlTj3NU8suFKKEzH9FH5AMldCquCoLIHzel5yg7G7NGUtHAxNg1ux9iPa4MW2oKMQQ0KvcugVoQWJPMYMm9EfFumd0= minggu@minggu-laptop",
        ),
    },
)

returned_job = ml_client.jobs.create_or_update(job)
ml_client.jobs.stream(returned_job.name)
