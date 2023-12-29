# Practical MLOps for Kubernetes: Managing Machine Learning with GPUs and MicroK8s

Welcome to "Practical MLOps for Kubernetes Engineers". This guide is tailored for Kubernetes engineers looking to deepen their understanding of **machine learning operations** with a focus on Kubernetes and containers.

We'll use MicroK8s on Ubuntu 22.04, primarily on Paperspace (DigitalOcean), giving you real-world experience in managing ML workflows in Kubernetes. The target audience is SMBs (developer and startups).

This is an intermediate-level tutorial (201 level). It assumes you're familiar with containers, Kubernetes, automation, systems/networking, and basic machine learning concepts.


## Table of Contents
- ![1. Basics of GPU](Chapters/Chapter%201%20-%20GPU%20Basics.md)
- ![2. MLOps and Developer Experience](Chapters/Chapter%202%20-%20MLOps%20and%20Developer%20Experience.md)
- [3. GPU + Container](#3-gpu--container)
- [4. GPU + Kubernetes](#4-gpu--kubernetes)
- [5. Multi-instance GPU](#5-multi-instance-gpu)
- [6. Ansible Setup](#6-ansible-setup)
- [7.DVC]
- [8. MLFlow]
- [9. Kubeflow](#7-kubeflow)
- [10. Ray (Future Content)](#8-ray-future)

### 1. Basics of GPU
Learn the fundamentals of GPU technology, with a focus on NVIDIA GPUs. We'll cover hardware checks, driver installation, and dive into GPU compute, memory, and scheduling, including hands-on command-line examples.

### 2. MLOps
Compare between DevOps and MLOps for Machine learning. While MLOps tooling can be very broad, start with developer view and add the tool only when there is a need.

### 3. GPU + Container
Set up container environments and deploying GPU-based applications.

### 4. GPU + Kubernetes
Explore how GPUs integrate with Kubernetes, using MicroK8s and Ansible. This chapter is practical and relevant for Kubernetes in ML applications.

### 5. Multi-instance GPU
Learn to optimize Kubernetes for complex scenarios like multi-instance GPUs, enhancing resource utilization and ML workload performance.

### 6. Ansible Setup
Set up a multi-node Microk8s cluster w/ shared storage on Paperspace using Ansible with opinionated setting (addons, automatic updated disabled)

### 7 DVC (Coming soon)
Create a reproducible ML workflow with DVC. Hands-on.

### 7. MLFlow (Coming soon)
Add MLFlow to the previous setup.

### 8. Kubeflow (Coming soon)
Dive into Kubeflow within Kubernetes. We'll look at examples like hyperparameter tuning and working with Large Language Models, aligning with current ML trends.

### 9. Ray (Coming soon)
Future content will focus on Ray for distributed ML, addressing scalability in data-heavy environments.

## Conclusion
We balance theory with practical application, offering hands-on examples and exercises. The content is kept current, aligning with the latest in Kubernetes and ML.
