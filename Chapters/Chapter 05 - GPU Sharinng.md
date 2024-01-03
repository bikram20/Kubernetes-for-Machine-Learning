# Chapter 5 - GPU Sharing
In this chapter, we delve into the concept of GPU Sharing, a crucial aspect of maximizing the efficiency and cost-effectiveness of NVIDIA GPUs. Unlike CPUs, which are adept at multitasking across various processes, GPUs are traditionally allocated to a single process at a time. This default allocation can lead to underutilization of the GPU's robust capabilities. By enabling GPU sharing, similar to how CPUs are shared among processes and containers, we can significantly enhance GPU utilization and reduce overall costs.

There are 2 types of sharing that NVIDIA GPUs support.
- Time-slicing
- MIG or multi-instances groups

Both are configured by customizing the device plugin. We will configure time-slicing in this chapter, as it works in software and so is supported on almost every data center GPU. For configuring MIG, follow the 

## MIG vs. Time-slicing
NVIDIA GPUs support two primary methods of sharing:

- **Time-slicing**: Also known as MPS/multi-process service. Implemented in CUDA. This method allows multiple processes to share the GPU by allocating time slots to each process. It works similarly to how traditional CPUs manage multiple processes, ensuring that each process gets a fair amount of time to access the GPU. This is supported on most GPUs. 
- **MIG (Multi-Instance GPU)**: [MIG enables](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/index.html#introduction) a single GPU to be partitioned into multiple isolated instances. Each instance can be allocated to a separate process, providing a more granular level of control over GPU resources. MIG is true hardware-level isolation - almost like having N independent GPUs out of a single GPU. It is supported on only A100 (Ampere) and H100 (Grace Hopper). To configure MIG, follow similar process (helm upgrade) as outlined below for time-slicing, and use the right options for MIG. [Reference](https://github.com/NVIDIA/k8s-device-plugin?tab=readme-ov-file#configuration-option-details)

## Can MIG and time-slicing be combined?
Yes. 
[Reference](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/index.html#cuda-mps)

While MIG and time-slicing are distinct GPU sharing methods, they can indeed be combined to offer even more granular control over GPU resource allocation. Time-slicing allows you to further subdivide each MIG instance. Multiple processes or containers can share a single MIG instance, taking turns using its resources based on a configured time allocation scheme.


## Configure time-slicing
Let us try to run multiple pods with GPU resource requirements.

```shell
kubectl get po
kubectl appy -f vector-add.yaml
kubectl appy -f vector-add2.yaml
kubectl appy -f vector-add3.yaml
```

**You will see that 2nd and 3rd pod are in the pending state**. In kubectl describe, you will see that there are no other GPUs avilable. At the same time, pod1 is not really doing much. So if we could share the GPU between multiple pods, that would be a better utilization of resources.

We will do it by re-configuring the device plugin. [Reference](https://github.com/NVIDIA/k8s-device-plugin#shared-access-to-gpus-with-cuda-time-slicing)

```shell
helm upgrade -i nvdp nvdp/nvidia-device-plugin \
  --namespace nvidia-device-plugin \
  --create-namespace \
  --version 0.14.3  \
  --set-file config.map.config=timesharing-configmap.yaml

kubectl describe node
```

It shows 8 GPUs (due to time-slicing configuration) instead of 1.
Capacity:
  cpu:                8
  ephemeral-storage:  101275324Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             46224044Ki
  nvidia.com/gpu:     8
  pods:               110


And all 3 pods should be running.
paperspace@psxgrv5u6:~$ kubectl get po
NAME                  READY   STATUS    RESTARTS   AGE
gpu-operator-test     1/1     Running   0          68m
gpu-operator-test-3   1/1     Running   0          25m
gpu-operator-test-2   1/1     Running   0          65m


## Enable GPU Feature Discovery (GFD)
This module helps discover the GPU capabilities and maintain appropriate node labels. Can be installed along with Device plugin chat with an option "--set gfd.enabled=true". 

[Reference](https://github.com/NVIDIA/k8s-device-plugin#deploying-with-gpu-feature-discovery-for-automatic-node-labels)


```shell
# GFD is configured
helm get values nvdp -n nvidia-device-plugin
helm get all nvdp -n nvidia-device-plugin
helm get manifest nvdp -n nvidia-device-plugin  | grep -A 30 -i gfd

# Add GFD
helm upgrade -i nvdp nvdp/nvidia-device-plugin \
  --namespace nvidia-device-plugin \
  --create-namespace \
  --version 0.14.3  \
  --set-file config.map.config=timesharing-configmap.yaml \
  --set gfd.enabled=true

# Check the labels on the node
kubectl get no -o json | jq '.items[].metadata.labels' | grep nvidia.com
```

In the next chapter, we can automated everything done so far end-to-end using ansible.