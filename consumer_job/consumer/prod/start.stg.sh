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
apply_kubectl kafdrop-deploy.prod.yaml
apply_kubectl kafdrop-service.prod.yaml
apply_kubectl kafdrop-ingress.prod.yaml

echo "Kafdrop deployment completed successfully."

echo "Deploying Consumer Application"
apply_kubectl consumer-deploy.prod.yaml
apply_kubectl consumer-service.prod.yaml
apply_kubectl consumer-ingress.prod.yaml
apply_kubectl consumer-api-backend-config.prod.yaml


echo "Consumer deployment and service completed successfully."