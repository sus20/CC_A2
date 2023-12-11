#!/bin/bash

# Expose the Kafdrop service
echo "Starting Kafdrop..."
nohup kubectl port-forward svc/kafdrop-service 9000:9000 -n leaf-image-management-system > /dev/null 2>&1 &

echo "Kafdrop service exposed on http://localhost:9000"
