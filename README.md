# GPU and Accelerated Computing for Kubernetes Engineers

Welcome to "GPU and Accelerated Computing for Kubernetes Engineers." This guide is tailored for Kubernetes engineers looking to deepen their understanding of machine learning with a focus on Kubernetes and containers. We'll use MicroK8s on Ubuntu 22.04, primarily on Paperspace (DigitalOcean), giving you real-world experience in managing ML workflows in Kubernetes.

This is an intermediate-level tutorial (201 level). It assumes you're familiar with containers, Kubernetes, automation, systems/networking, and basic machine learning concepts.

## Table of Contents
- [1. Basics of GPU](#1-basics-of-gpu)
- [2. GPU Application Stack](#2-gpu-application-stack)
- [3. GPU + Container](#3-gpu--container)
- [4. GPU + Kubernetes](#4-gpu--kubernetes)
- [5. Multi-instance GPU](#5-multi-instance-gpu)
- [6. Ansible Setup](#6-ansible-setup)
- [7. Kubeflow](#7-kubeflow)
- [8. Ray (Future Content)](#8-ray-future)

### 1. Basics of GPU
Learn the fundamentals of GPU technology, with a focus on NVIDIA GPUs. We'll cover hardware checks, driver installation, and dive into GPU compute, memory, and scheduling, including hands-on command-line examples.

### 2. GPU Application Stack
Get to know the GPU application ecosystem. This includes drivers, application libraries, and MLops tools like Kubeflow. We'll also discuss containerization for reproducibility.

### 3. GPU + Container
Set up container environments and deploying GPU-based applications.

### 4. GPU + Kubernetes
Explore how GPUs integrate with Kubernetes, using MicroK8s and Ansible. This chapter is practical and relevant for Kubernetes in ML applications.

### 5. Multi-instance GPU
Learn to optimize Kubernetes for complex scenarios like multi-instance GPUs, enhancing resource utilization and ML workload performance.

### 6. Ansible Setup
Set up a multi-node Microk8s cluster w/ shared storage on Paperspace using Ansible with some opinionated setting (addons, automatic updated disabled)

### 7. Kubeflow
Dive into Kubeflow within Kubernetes. We'll look at examples like hyperparameter tuning and working with Large Language Models, aligning with current ML trends.

### 8. Ray (Future)
Future content will focus on Ray for distributed ML, addressing scalability in data-heavy environments.

## Conclusion
We balance theory with practical application, offering hands-on examples and exercises. The content is kept current, aligning with the latest in Kubernetes and ML.
