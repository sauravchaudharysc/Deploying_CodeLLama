# TA Buddy

# TA Buddy

## Building the Docker Image to Include All Dependencies

To ensure that all dependencies for the project are included and available, follow these steps:

### 1. Create a `Dockerfile`

Create a file named `Dockerfile` with the following content:

```Dockerfile
FROM nvcr.io/nvidia/pytorch:22.05-py3

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN python -m spacy download en_core_web_sm

RUN mkdir /ai_bodhitree
COPY ./ai_bodhitree /ai_bodhitree
WORKDIR /ai_bodhitree
```
### 2. Build the Docker Image
Run the following command to build the Docker image:

```bash
    docker build . -t tagname:imagename
```

### 3. Running the Docker Image Inside a Container
To run the Docker image inside a container, use the following command:
```
  docker run -it --name ai_bodhitree_container \
  --gpus all \
  --dns 8.8.8.8 \
  -p 10.195.100.5:8003:8000 \
  -v /raid/ganesh/nagakalyani/nagakalyani/autograding/huggingface_codellama/CodeLlama-7b-Instruct-hf:/ai_bodhitree/CodeLlama \
  tagname:imagename /bin/bash
```

**Docker Command Explanation**

- `-it`: Runs the container in interactive mode with a TTY. This allows you to interact with the container via the terminal.

- `--name ai_bodhitree_container`: Assigns a name to the container, making it easier to manage and reference.

- `--gpus all`: Allocates all available GPUs on the host machine to the container, which is useful for GPU-intensive tasks.

- `--dns 8.8.8.8`: Configures the container to use Google's DNS server (8.8.8.8) for name resolution.

- `-p 10.195.100.5:8003:8000`: Maps port 8000 inside the container to port 8003 on the host machine. This allows access to services running inside the container via the specified host port.

- `-v /raid/...:/ai_bodhitree/CodeLlama`: Mounts a directory from the host (/raid/...) to a directory inside the container (/ai_bodhitree/CodeLlama). This facilitates sharing files between the host and the container.

- `tagname:imagename`: Specifies the Docker image to use for creating the container. Replace tagname and imagename with the appropriate image tag and name.

- `/bin/bash`: Launches an interactive Bash shell inside the container, allowing you to run commands interactively.

### 4. Run the Bash File Inside the Container 
Once inside the container, execute the following command to run your script:
```
    bash runall.sh
```
Ensure that runall.sh is in the correct location inside the container and has the appropriate permissions to be executed.