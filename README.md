# Practical MLOps for Kubernetes: Managing Machine Learning with GPUs and MicroK8s

Welcome to "Practical MLOps for Kubernetes Engineers". This guide is tailored for Kubernetes engineers looking to deepen their understanding of **machine learning operations** with a focus on Kubernetes and containers.

We'll use MicroK8s on Ubuntu 22.04, primarily on Paperspace (DigitalOcean), giving you real-world experience in managing ML workflows in Kubernetes. The target audience is SMBs (developer and startups).

This is an intermediate-level tutorial (201 level). It assumes you're familiar with containers, Kubernetes, devops, systems/networking, and basic machine learning concepts.

Known Limitations: No cluster auto-scaler. 


## Table of Contents
- [1. Basics of GPU](Chapters/Chapter%201%20-%20GPU%20Basics.md)
- [2. MLOps and Developer Experience](Chapters/Chapter%202%20-%20MLOps%20and%20Developer%20Experience.md)
- [3. GPU + Container](Chapters/Chapter%203%20-%20GPU%20+%20Container.md)
- [4. GPU + Kubernetes](Chapters/Chapter%204%20-%20GPU%20+%20Kubernetes.md)
- [5. Multi-instance GPU](Chapters/Chapter%205%20-%20GPU%20Sharinng.md)
- [6. Ansible Setup](Chapters/Chapter%206%20-%20Ansible%20Setup.md)
- [7.DVC](Chapters/Chapter%207%20-%20DVC.md)
- [8. MLFlow](Chapters/Chapter%208%20-%20MLflow.md)
- [9. Metaflow](Chapters/Chapter%209%20-%20Metaflow.md)
- [10. Kubeflow](Chapters/Chapter%2010%20-%20Kubeflow.md)
- [11. Ray](Chapters/Chapter%2011%20-%20Ray.md)

### 1. Basics of GPU
Learn the fundamentals of GPU technology, with a focus on NVIDIA GPUs. We'll cover hardware checks, driver installation, and dive into GPU compute, memory, and scheduling, including hands-on command-line examples. GPU hardware is installed using recommended ubuntu-drivers utility.

### 2. MLOps
Compare between DevOps and MLOps for Machine learning. While MLOps tooling can be very broad, start with developer view and add the tool only when there is a need. 

### 3. GPU + Container
Set up container environments and deploying GPU-based applications. Docker and Nvidia container toolkit are installed using recommended steps by Docker and Nvidia.

### 4. GPU + Kubernetes
Explore how GPUs integrate with Kubernetes, using MicroK8s and Ansible. This chapter is practical and relevant for Kubernetes in ML applications. We self-host Microk8s on Ubuntu and run it on Paperspace.

### 5. Multi-instance GPU
Learn to optimize Kubernetes for complex scenarios like multi-instance GPUs, enhancing resource utilization and ML workload performance. We use A100 GPU for this.

### 6. Ansible Setup
Set up a multi-node Microk8s cluster w/ shared storage on Paperspace using Ansible with opinionated setting (addons, automatic updated disabled). Ansible is installed using Brew on a client host (mac).

### 7 DVC (Coming soon)

### 8. MLFlow (Coming soon)

### 10. Metaflow (Coming soon)

### 10. Kubeflow (Coming soon)

### 11. Ray (Coming soon)

## Conclusion
We balance theory with practical application, offering hands-on examples and exercises. The content is kept current, aligning with the latest in Kubernetes and ML.
