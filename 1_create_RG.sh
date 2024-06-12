#!/bin/bash

export ACR_RG=minggu-VM
export ACR_NAME=NCCLA100MINGGU
export LOCATION=canadacentral

export RG="MINGGU-AML$(date +%m%d)"
export location=canadacentral #francecentral
export ws_name="MINGGU-WS$(date +%m%d)"
export acr_id=`az acr show --name $ACR_NAME --resource-group $ACR_RG --query id --output tsv`

az group create --name $RG --location $location
az ml workspace create --name $ws_name --resource-group $RG --location $location --container-registry $acr_id

