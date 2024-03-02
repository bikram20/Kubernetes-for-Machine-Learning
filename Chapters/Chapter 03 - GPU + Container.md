# Chapter 3 - GPU + Container
The first 2 chapters were more of big picture. This chapter will focus on using containers (we will use Docker) and running a GPU workload inside a container.

*NOTE*: If you have a total disk size 50GB, you will likely run into storage issues, as Docker images are ~10GB. It is better to increase the disk size.

## Install and Review Docker
Use the same Ubuntu VM you created. We will install docker using [recommended installation](https://docs.docker.com/engine/install/ubuntu/). 

```shell
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
```

Now let us review the config and processes.

```shell
paperspace@ps3nfhuzbif3:~$ sudo docker info
paperspace@ps3nfhuzbif3:~$ sudo docker system info
paperspace@ps3nfhuzbif3:~$ vi /etc/docker/daemon.json
paperspace@ps3nfhuzbif3:~$ sudo ps aux | grep -i docker
paperspace@ps3nfhuzbif3:~$ sudo find / -name containerd
paperspace@ps3nfhuzbif3:~$ sudo find / -name runc
paperspace@ps3nfhuzbif3:~$ 
```

Note that Docker installed both containerd and runc. This following diagram should make it clear. 

![Docker Big Picture](https://www.docker.com/wp-content/uploads/2022/12/docker-engine-1-11-runc-1.png.webp)


1. **Docker as a High-Level Interface**: Docker provides a user-friendly interface for working with containers. It offers command-line tools and APIs for building, running, and managing containers. Docker is more than just a wrapper; it's a comprehensive platform that simplifies container management.
2. **Containerd as a Container Runtime**: `containerd` is indeed the daemon responsible for managing the entire container lifecycle. It handles tasks like image transfer and storage, container execution, supervision, and low-level storage and network interfaces. Docker uses `containerd` under the hood for these operations.
3. **Runc for Running Containers**: `runc` is a CLI tool for spawning and running containers according to the OCI (Open Container Initiative) specification. `containerd` uses `runc` to create and run containers. `runc` operates at a lower level and is typically not visible as a long-running process, which is why it doesn't appear in `ps aux` output like `dockerd` or `containerd`.
4. **GPU Awareness**: By default, Docker and `containerd` are not aware of specialized hardware like NVIDIA GPUs. This means they cannot natively leverage GPU resources in containers.
5. **Role of the NVIDIA Container Toolkit**: To enable GPU support in containers, the NVIDIA Container Toolkit is required. It extends the capabilities of Docker and `containerd` to make them aware of and able to use NVIDIA GPUs. It does this by adding a custom runtime and hooks that set up the necessary environment inside containers to access and utilize GPU resources.
6. **NVIDIA Container Runtime**: Part of the NVIDIA Container Toolkit, the NVIDIA Container Runtime, is configured as an additional runtime in Docker. This runtime includes the necessary components to integrate GPU support with containers, allowing Docker to run containers that can leverage NVIDIA GPU resources effectively.

In summary, Docker provides the high-level toolset for container management, `containerd` and `runc` handle the lower-level operations, and the NVIDIA Container Toolkit enables Docker and `containerd` to use NVIDIA GPUs in containers.


## Install and Review NVIDIA container toolkit

[Reference](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.14.3/install-guide.html)

First, review the architecture of how NVIDIA toolkit plays with containerd.

![NVIDA Toolkit Big Picture](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.14.3/_images/runtime-architecture.png)

- **Making runc GPU Aware:** The NVIDIA Container Toolkit, specifically through the NVIDIA Container Runtime, does make runc GPU-aware. It does this not by modifying runc directly, but by adding a runtime hook. This hook is a key component in enabling the container to access NVIDIA GPU resources.
- **Runtime Hook:** The NVIDIA Container Runtime integrates a prestart hook into the container lifecycle. This hook sets up the necessary environment (like GPU drivers and libraries) inside the container, enabling it to access and utilize the GPU.
Configuring containerd/Docker: The NVIDIA Container Toolkit modifies the configuration of containerd or Docker to use the NVIDIA - **Container Runtime as an additional runtime.** In the case of Docker, this is typically done by editing the daemon.json file to specify the NVIDIA runtime. For containerd, it involves configuring the containerd service to use the NVIDIA runtime.
- **Invocation of runc:** When a container requiring GPU access is launched, containerd/Docker invokes the NVIDIA Container Runtime, which then uses the runtime hook to prepare the GPU environment before runc starts the container. This process is seamless to the user, who simply needs to specify the need for GPU access (typically through a command-line parameter like --gpus all in Docker).

```shell
paperspace@ps3nfhuzbif3:~$ curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
paperspace@ps3nfhuzbif3:~$ sudo apt-get update
paperspace@ps3nfhuzbif3:~$ sudo apt-get install -y nvidia-container-toolkit
paperspace@ps3nfhuzbif3:/etc/docker$ sudo nvidia-ctk runtime configure --runtime=docker
INFO[0000] Loading config from /etc/docker/daemon.json  
INFO[0000] Wrote updated config to /etc/docker/daemon.json 
INFO[0000] It is recommended that docker daemon be restarted. 
paperspace@ps3nfhuzbif3:/etc/docker$ sudo systemctl restart docker
paperspace@ps3nfhuzbif3:/etc/docker$ cat /etc/docker/daemon.json  
{
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    }
}paperspace@ps3nfhuzbif3:/etc/docker$ 
```

Note that we had to explicitly configure nvidia-container-runtime for Docker.

```shell
paperspace@ps3nfhuzbif3:/etc/docker$ sudo docker info  | grep -i runtime
 Runtimes: io.containerd.runc.v2 nvidia runc
 Default Runtime: runc
paperspace@ps3nfhuzbif3:/etc/docker$ 
```

Now let us run a sample workload container.

```shell
paperspace@ps3nfhuzbif3:/etc/docker$ sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
a48641193673: Pull complete 
Digest: sha256:6042500cf4b44023ea1894effe7890666b0c5c7871ed83a97c36c76ae560bb9b
Status: Downloaded newer image for ubuntu:latest
Fri Dec 29 19:14:51 2023       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA RTX A4000               Off | 00000000:00:05.0 Off |                  Off |
| 41%   33C    P8              12W / 140W |      2MiB / 16376MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
paperspace@ps3nfhuzbif3:/etc/docker$ 
```

Note that nvidia-smi command worked because --gpus all option. It mounted the necessary binaries into the container.

```shell
sudo docker run -it --rm --runtime=nvidia --gpus all ubuntu /bin/bash
mount | grep -i nvidia
which nvidia-smi
```

Now we can build a docker image with the matrix multiplication script (from chapter 1), and run it as a container.

```shell
paperspace@ps3nfhuzbif3:~/Scripts$ ls -l
total 8
-rw-rw-r-- 1 paperspace paperspace  483 Dec 29 19:34 Dockerfile
-rwxrwxr-x 1 paperspace paperspace 2607 Dec 29 19:30 mat_mul.py
paperspace@ps3nfhuzbif3:~/Scripts$ cat Dockerfile
paperspace@ps3nfhuzbif3:~/Scripts$ cat mat_mul.py
paperspace@ps3nfhuzbif3:~/Scripts$ sudo docker build -t pytorch-cuda .
paperspace@ps3nfhuzbif3:~/Scripts$ sudo docker images
paperspace@ps3nfhuzbif3:~/Scripts$ sudo docker run --rm --gpus all pytorch-cuda
A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.

Matrices dimension: 10000, Time taken on CPU: 3.213898181915283 seconds
Matrices dimension: 25000, Time taken on CUDA cores: 4.067363500595093 seconds
Matrices dimension: 25000, Time taken on Tensor Cores (FP16): 0.6378970146179199 seconds
paperspace@ps3nfhuzbif3:~/Scripts$
paperspace@ps3nfhuzbif3:~/Scripts$ sudo docker run -it --rm --gpus all pytorch-cuda bash
```

So everything works well. Now let us try the spam_classification sample script. We have a LLM (eg BERT) and finetune it on a spam dataset. Then we run bunch of prediction using a prediction script. This aligns with ML workflow, where you continue to train or finetune a model based on new set of data. 

As you continue to iterate on the scripts on your host machine, you may just mount the host folder in one terminal and run the scripts from inside container (another terminal). Another reason is that you need to save the trained model elsewhere, otherwise it will be deleted when container run is complete.

```shell
paperspace@ps3nfhuzbif3:~/Scripts$ sudo docker run -it --rm --gpus all -v $(pwd):/mnt  pytorch-cuda:v3 bash
root@4fca2ef6a1f5:/mnt# python3 spam_classify.py 
```

When the training run is going on, you can check GPU usage from host terminal.

```shell
paperspace@ps3nfhuzbif3:~/Scripts$ nvidia-smi 
Fri Dec 29 21:07:22 2023       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA RTX A4000               Off | 00000000:00:05.0 Off |                  Off |
| 75%   92C    P2             136W / 140W |   3371MiB / 16376MiB |     96%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A     23808      C   python3                                    3364MiB |
+---------------------------------------------------------------------------------------+
paperspace@ps3nfhuzbif3:~/Scripts$ 
```

When is training is completed, the model is saved to current folder on the host device. 

```shell
paperspace@ps3nfhuzbif3:~/Scripts$ ls -l 
total 24
drwxr-xr-x 2 root       root       4096 Dec 29 20:46 bert_spam_classifier
-rw-rw-r-- 1 paperspace paperspace  806 Dec 29 20:44 Dockerfile
-rwxrwxr-x 1 paperspace paperspace 2607 Dec 29 19:30 mat_mul.py
drwxr-xr-x 3 root       root       4096 Dec 29 20:45 results
-rw-rw-r-- 1 paperspace paperspace 2619 Dec 29 21:07 spam_classify.py
-rw-rw-r-- 1 paperspace paperspace 1033 Dec 29 21:16 spam_predit.py
paperspace@ps3nfhuzbif3:~/Scripts$ ls -l bert_spam_classifier/  # Saved model
total 427704
-rw-r--r-- 1 root root       727 Dec 29 21:08 config.json
-rw-r--r-- 1 root root 437958648 Dec 29 21:08 model.safetensors
paperspace@ps3nfhuzbif3:~/Scripts$ 
```

Now we can run the spam_predict.py script (under Scripts_Artifacts folder). Make sure review the path of the model in the script.


```shell
root@4fca2ef6a1f5:/mnt# python3 spam_predit.py 
cuda
No input text provided.
root@4fca2ef6a1f5:/mnt# python3 spam_predit.py  "Hey how are you?"  # 'ham' means not-spam
cuda
Prediction for 'Hey how are you?': ham
root@4fca2ef6a1f5:/mnt# python3 spam_predit.py  "Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera for Free! Call The Mobile Update Co FREE on 08002986030"
cuda
Prediction for 'Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera for Free! Call The Mobile Update Co FREE on 08002986030': spam
root@4fca2ef6a1f5:/mnt# 
```


At this point, you can deactivate your VM if you no longer need it. 