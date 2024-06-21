# Build the Docker image
docker build -t my-docker-image:latest .

# Tag the image for ECR (replace <account-id> and <region> with your details)
docker tag my-docker-image:latest <account-id>.dkr.ecr.<region>.amazonaws.com/my-docker-image:latest

# Push the image to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/my-docker-image:latest
