# Practical MLOps for Kubernetes: Managing Machine Learning with GPUs and MicroK8s

Welcome to "Practical MLOps for Kubernetes Engineers/Operators". This guide is tailored for Kubernetes and Devops engineers looking to deepen their understanding of **machine learning operations** with a focus on Kubernetes and containers. 

To put this in perspective, there are 3 different personas.
- Application developers using APIs (eg. Openai api) to build applications. This is not relevant to you.
- Data Scientists building and finetuning models as a product. This is not relevant to you.
- **Engineers looking to build/operate/learn about ML infrastructure and processes. This is for you.**

We'll use MicroK8s on Ubuntu 22.04, primarily on Paperspace (DigitalOcean), giving you real-world experience in managing ML workflows in Kubernetes. Here's why MicroK8s:
- Thin footprint and low operational overhead
- Highly available and production-ready
- Natively supported on Ubuntu
- Start with just 1 node. Have access to the entire ML/AI ecosystem of tools built around Kubernetes and prepare your infrastructure for the future.

This is an intermediate-level tutorial (201 level). It assumes you're familiar with containers, Kubernetes, devops, systems/networking, and basic machine learning concepts. 

If you are familiar with all the concepts, then ansible scripts (chapter 6 and 12) is all you need to set up the infrastusture.


## Table of Contents
- [1. Basics of GPU](Chapters/Chapter%2001%20-%20GPU%20Basics.md)
- [2. MLOps and Developer Experience](Chapters/Chapter%2002%20-%20MLOps%20and%20Developer%20Experience.md)
- [3. GPU + Container](Chapters/Chapter%2003%20-%20GPU%20+%20Container.md)
- [4. GPU + Kubernetes](Chapters/Chapter%2004%20-%20GPU%20+%20Kubernetes.md)
- [5. Multi-instance GPU](Chapters/Chapter%2005%20-%20GPU%20Sharinng.md)
- [6. Ansible Setup](Chapters/Chapter%2006%20-%20Ansible%20Setup.md)
- [7. Running and FInetuning LLM on Kubernetes](Chapters/Chapter%2007%20-%20Running%20and%20finetuning%20LLMs%20on%20Kubernetes.md)

### 1. Basics of GPU
Learn the fundamentals of GPU technology, with a focus on NVIDIA GPUs. We'll cover hardware checks, driver installation, and dive into GPU compute, memory, and scheduling, including hands-on command-line examples. 

### 2. MLOps
Compare between DevOps and MLOps for Machine learning. While MLOps tooling can be very broad, start with developer view and add the tool only when there is a need. 

### 3. GPU + Container
Set up container environments and deploying GPU-based applications. 

### 4. GPU + Kubernetes
Explore how GPUs integrate with Kubernetes, using MicroK8s and Ansible. This chapter is practical and relevant for Kubernetes in ML applications. We self-host Microk8s on Ubuntu and run it on Paperspace.

### 5. Multi-instance GPU
Learn to optimize Kubernetes for complex scenarios like multi-instance GPUs, enhancing resource utilization and ML workload performance. 

### 6. Ansible Setup
Set up a GPU-ready, multi-node Microk8s cluster w/ shared storage on Paperspace using Ansible with opinionated setting (addons, automatic updated disabled). 

### 7. Running a finetuning LLMs on Kubernetes
Finetune and Run a Mistral 7B model on Kubernetes.  
