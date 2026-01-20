# Create the secret (update with your actual API key first)
kubectl apply -f k8s-secret.yaml

# Deploy the pod
kubectl apply -f k8s-pod.yaml

# Create the service
kubectl apply -f k8s-service.yaml

# Check pod status
kubectl get pods

# View pod logs
kubectl logs edtech-nlp2sql-pod

# Describe pod for detailed info
kubectl describe pod edtech-nlp2sql-pod

# Port forward to access locally
kubectl port-forward edtech-nlp2sql-pod 8000:8000

# Delete resources
kubectl delete -f k8s-service.yaml
kubectl delete -f k8s-pod.yaml
kubectl delete -f k8s-secret.yaml
