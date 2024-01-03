# Practical MLOps for Kubernetes: Managing Machine Learning with GPUs and MicroK8s

Welcome to "Practical MLOps for Kubernetes Engineers". This guide is tailored for Kubernetes and Devops engineers looking to deepen their understanding of **machine learning operations** with a focus on Kubernetes and containers. 

To put this in perspective, there are 3 different personas.
- Application developers using APIs (eg. Openai api) to build applications. This is not relevant to you.
- Data Scientists building and finetuning models as a product. This is not relevant to you.
- **Engineers looking to build/operate/learn about ML infrastructure and processes. This is for you.**

We'll use MicroK8s on Ubuntu 22.04, primarily on Paperspace (DigitalOcean), giving you real-world experience in managing ML workflows in Kubernetes. The target audience is SMBs, startups, and developers.

This is an intermediate-level tutorial (201 level). It assumes you're familiar with containers, Kubernetes, devops, systems/networking, and basic machine learning concepts.


## Table of Contents
- [1. Basics of GPU](Chapters/Chapter%2001%20-%20GPU%20Basics.md)
- [2. MLOps and Developer Experience](Chapters/Chapter%2002%20-%20MLOps%20and%20Developer%20Experience.md)
- [3. GPU + Container](Chapters/Chapter%2003%20-%20GPU%20+%20Container.md)
- [4. GPU + Kubernetes](Chapters/Chapter%2004%20-%20GPU%20+%20Kubernetes.md)
- [5. Multi-instance GPU](Chapters/Chapter%2005%20-%20GPU%20Sharinng.md)
- [6. Ansible Setup](Chapters/Chapter%2006%20-%20Ansible%20Setup.md)
- [7. DVC - tbd](Chapters/Chapter%2007%20-%20DVC.md)
- [8. MLFlow - tbd](Chapters/Chapter%2008%20-%20MLflow.md)
- [9. Metaflow - tbd](Chapters/Chapter%2009%20-%20Metaflow.md)
- [10. Kubeflow - tbd](Chapters/Chapter%2010%20-%20Kubeflow.md)
- [11. Ray - tbd](Chapters/Chapter%2011%20-%20Ray.md)

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
