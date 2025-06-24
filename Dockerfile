# Use the official Qdrant image
FROM qdrant/qdrant:latest

# Expose the default Qdrant port
EXPOSE 6333

# Optionally, you can set environment variables here
# ENV QDRANT__SERVICE__HOST=0.0.0.0
# ENV QDRANT__SERVICE__HTTP_PORT=6333

# No additional commands needed; Qdrant starts by default
