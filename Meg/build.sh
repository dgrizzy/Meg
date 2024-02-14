IMAGE_NAME="meg"

# Get the current datetime in the format YYYYMMDDHHMMSS
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Create the Docker tag with the image name and timestamp
TAG="${IMAGE_NAME}:${TIMESTAMP}"

# Directory containing the Dockerfile
DOCKERFILE_DIRECTORY="."

# Build the Docker image
docker build -t "${TAG}" "${DOCKERFILE_DIRECTORY}"

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Docker image ${TAG} built successfully."
else
    echo "Failed to build Docker image."
fi