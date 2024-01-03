# Use an official NVIDIA CUDA base image
FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y python3-pip  && rm -rf /var/lib/apt/lists/*
RUN pip install torch torchvision torchaudio transformers[torch] datasets scikit-learn
#RUN pip install --no-cache-dir torch torchvision torchaudio transformers[torch] datasets scikit-learn

# Run the script when the container launches
CMD ["python3", "mat_mul.py"]

