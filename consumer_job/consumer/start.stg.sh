#!/bin/bash

apply_kubectl() {
    file=$1
    kubectl apply -f "$file" -n leaf-image-management-system
    if [ $? -ne 0 ]; then
        echo "Error applying $file."
        exit 1
    fi
}

# Deploy Kafdrop
echo "Deploying Kafdrop"
apply_kubectl kafdrop-deploy.stg.yaml
apply_kubectl kafdrop-service.stg.yaml

echo "Kafdrop deployment completed successfully."
