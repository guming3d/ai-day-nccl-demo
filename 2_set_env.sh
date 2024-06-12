#!/bin/bash

# Set environment variables for Python script
# export RESOURCE_GROUP="MINGGU-AML$(date +%m%d)"
export RESOURCE_GROUP="MINGGU-AML0605"
# export WORKSPACE_NAME="MINGGU-WS$(date +%m%d)"
export WORKSPACE_NAME="MINGGU-WS0605"
export SUBSCRIPTION_ID=$(az account show --query id -o tsv)
export CLUSTER_NAME="NCv4"
