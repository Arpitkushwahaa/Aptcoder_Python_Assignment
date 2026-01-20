# Build the Docker image
docker build -t edtech-nlp2sql:latest .

# Run the container
docker run -d \
  --name edtech-api \
  -p 8000:8000 \
  -e GEMINI_API_KEY="your-api-key-here" \
  edtech-nlp2sql:latest

# View logs
docker logs -f edtech-api

# Stop the container
docker stop edtech-api

# Remove the container
docker rm edtech-api
