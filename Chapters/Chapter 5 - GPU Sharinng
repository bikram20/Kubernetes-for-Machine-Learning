# Chapter 5 - GPU Sharing
Unlike CPU, GPU's are allocated to a single process at one time by default. It is no-brainer that if the GPU resource can be shared among processes/containers just like CPU, then the utilization will improve along with reduced cost.

There are 2 types of sharing that NVIDIA GPUs support.
- Time-slicing
- MIG

Both are configured by customizing the device plugin. We will review time-slicing in this chapter.

## MIG vs. Time-slicing


## Can MIG and time-slicing be combined?


## Configure time-slicing
Let us try to run multiple pods with GPU resource requirements.

kubectl get po
kubectl appy -f vector-add.yaml
kubectl appy -f vector-add2.yaml
kubectl appy -f vector-add3.yaml

You will see that 2nd and 3rd pod are in the pending state. In kubectl describe, you will see that there are no other GPUs avilable. At the same time, pod1 is not really doing much. So if we could share the GPU between multiple pods, that would be a better utilization of resources.

We will do it by re-configuring the device plugin. Referece: https://github.com/NVIDIA/k8s-device-plugin#shared-access-to-gpus-with-cuda-time-slicing

helm upgrade -i nvdp nvdp/nvidia-device-plugin \
  --namespace nvidia-device-plugin \
  --create-namespace \
  --version 0.14.3  \
  --set-file config.map.config=timesharing-configmap.yaml



kubectl describe node

shows 8 containers (due to time-slicing configuration) running.
Capacity:
  cpu:                8
  ephemeral-storage:  101275324Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             46224044Ki
  nvidia.com/gpu:     8
  pods:               110


And all 3 pods are running.
paperspace@psxgrv5u6:~$ kubectl get po
NAME                  READY   STATUS    RESTARTS   AGE
gpu-operator-test     1/1     Running   0          68m
gpu-operator-test-3   1/1     Running   0          25m
gpu-operator-test-2   1/1     Running   0          65m


## Enable GPU Feature Discovery (GFD)
This module helps discover the GPU capabilities and maintain appropriate node labels. Can be installed along with Device plugin chat with an option "--set gfd.enabled=true". 

Reference: https://github.com/NVIDIA/k8s-device-plugin#deploying-with-gpu-feature-discovery-for-automatic-node-labels




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
