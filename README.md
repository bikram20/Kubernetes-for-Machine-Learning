# Setting up Machine Learning Infrastructure on Kubernetes

This tutorial is tailored for Kubernetes and Devops engineers looking to deepen their understanding of **machine learning operations** with a focus on Kubernetes and containers. 

To put this in perspective, there are 3 different personas.
- Application developers using APIs (eg. Openai api) to build applications. This is not relevant to you.
- Data Scientists building and finetuning models as a product. This is not relevant to you.
- **Engineers looking to build/operate/learn about ML infrastructure and processes. This is for you.**

We'll use MicroK8s on Ubuntu 22.04, running on [Paperspace cloud](https://www.paperspace.com) by [DigitalOcean](https://www.digitalocean.com), giving you real-world experience in managing ML workflows in Kubernetes.

Why MicroK8s?
- Thin footprint and low operational overhead to run on a single VM. Hence useful for learning.
- Highly available and production-ready

## Table of Contents
- [1. Basics of GPU](Chapters/Chapter%2001%20-%20GPU%20Basics.md)
- [2. MLOps and Developer Experience](Chapters/Chapter%2002%20-%20MLOps%20and%20Developer%20Experience.md)
- [3. GPU + Container](Chapters/Chapter%2003%20-%20GPU%20+%20Container.md)
- [4. GPU + Kubernetes](Chapters/Chapter%2004%20-%20GPU%20+%20Kubernetes.md)
- [5. Multi-instance GPU](Chapters/Chapter%2005%20-%20GPU%20Sharinng.md)
- [6. Ansible Setup](Chapters/Chapter%2006%20-%20Ansible%20Setup.md)

### 1. Basics of GPU
Learn the fundamentals of GPU technology, with a focus on NVIDIA GPUs. We'll cover hardware checks, driver installation, and dive into GPU compute, memory, and scheduling, including hands-on command-line examples. 

### 2. MLOps
Compare between DevOps and MLOps for Machine learning. While MLOps tooling can be very broad, start with developer view and add the tool only when there is a need. 

### 3. GPU + Container
Set up container environments and deploying GPU-based applications. 

### 4. GPU + Kubernetes
Explore how GPUs integrate with Kubernetes, using Microk8s. We self-host Microk8s/Ubuntu on [Paperspace](https://www.paperspace.com).

### 5. Multi-instance GPU
Optimize Kubernetes for complex scenarios like multi-instance GPUs, enhancing resource utilization and ML workload performance. 

### 6. Ansible Setup
Set up a GPU-ready, multi-node Microk8s cluster with shared storage on Paperspace using Ansible with opinionated settings.
