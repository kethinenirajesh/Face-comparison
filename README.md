# Face-comparison

# prerequisites
1) Docker
2) aws_access_key_id and aws_secret_access_key from AWS
3) Replace "***" with aws_access_key_id and aws_secret_access_key in Face_comparison.py file.

# Build docker image

./build-docker.sh

# Start the service

./start-service

Now your service will be running on: http://localhost:8042/

You can upload the two pic's which you want to compare and submit it.

You will get Similarity score as a output.
