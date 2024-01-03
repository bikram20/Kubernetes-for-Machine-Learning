# Chapter 4 - GPU + Kubernetes
In chapter 3, we discussed how to run GPU-enabled applications inside a container and tried 2 samples applications. In this chapter, we focus on running GPU-enabled apps in a k8s cluster. To keep focus and yet be able to use things in production, we pick microk8s. 

**Rationale behind choosing Microk8s**
- Goal is to self-host kubernetes with less overhead.
  - Microk8s is well-maintained by Canonical (Ubuntu), installs with 1 command (snap) and can be customized. 
  - It is also HA-ready by default, so as long as you add >= 3 nodes, you get HA by default. 

Our setup is opinionated - there is no cluster autoscaling, and we always use a shared storage (Paperspace managed shared storage) for all nodes. 

In this chapter and next, we will focus on a single node setup. This will allow us to experiment and create a script with necessary commands to get started manually. In chapter 6, we will set up a multi-node HA cluster with e2e automation using ansible.

**Note: If you do not need MIG (multi-instance GPU), you can choose any GPU hardware.** If you need MIG, then it needs to be [A100 or higher (Ampere architecture+)](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/index.html). 

## Set up and Explore Microk8s
Recommend to set up a private network, VM, and a shared drive from the console, so you can focus on k8s. Alternately, you can refer to [CLI/API cheatsheet](Scripts_Artifacts/Paperspace-resources-sheatsheet.md) for commands. 

After you are SSH to the VM, install Microk8s using snap. Also install helm3, and set up kubeconfig on the node. All commands are self-explanatory. Feel free to use apt or direct install for every command except microk8s. For microk8s in particular, let us stick to snap.

```shell
sudo apt update
DEBIAN_FRONTEND=noninteractive sudo apt upgrade -y
sudo apt install snapd

# We use snap to install microk8s, as it is well-maintained and recommended. For everything else, we will follow corresponding tool recommendation
sudo snap install microk8s --classic
sudo ln -s /snap/microk8s/current/kubectl /usr/local/bin/kubectl
# Kubectl is in a different path, hence a softlink was created above
echo "export PATH=$PATH:/snap/microk8s/current/bin" >> ~/.bashrc

mkdir $HOME/.kube
sudo microk8s config > $HOME/.kube/config
sudo usermod -a -G microk8s paperspace
sudo chown -R paperspace ~/.kube
chmod 700 ~/.kube/config 
# You will need to LOGOUT and log back in for kubectl and helm to work.
```

Now we should configure snap to [prevent automatic updates](https://snapcraft.io/docs/managing-updates) to microk8s. That way, we can update using `snap refresh microk8s` manually.

```shell
snap list
sudo snap refresh --hold microk8s # Do not allow snap to update microk8s
# verify
snap list
```

## Explore Microk8s
Start by reviewing the processes.

```shell
sudo ps -aux | egrep -i "microk8s|containerd"
sudo ps -aux | grep -i "containerd"
sudo ps -aux | grep -i "microk8s" | grep -v "containerd"
```

Start with containerd processes.
- Main process: /snap/microk8s/6089/bin/containerd --config /var/snap/microk8s/6089/args/containerd.toml --root /var/snap/microk8s/common/var/lib/containerd --state /var/snap/microk8s/common/run/containerd --address /var/snap/microk8s/common/run/containerd.sock
- Containerd shim that runs each container/pod: /snap/microk8s/6089/bin/containerd-shim-runc-v2 -namespace k8s.io -id [CONTAINER_ID] -address /var/snap/microk8s/common/run/containerd.sock
- Containerd commands (similar to Docker cli)
```shell
sudo microk8s ctr containers --help
sudo microk8s ctr containers ls
sudo microk8s ctr containers info [CONTAINER_ID]
# Match it with the pods
microk8s kubectl get pods --all-namespaces

# Logs
sudo journalctl -u snap.microk8s.daemon-containerd
sudo microk8s ctr logs [CONTAINER_ID]
```

Other Microk8s processs.
- /snap/microk8s/6089/kubelite --scheduler-args-file=...: Microk8s bundles a number of [kubernetes control plane services into a single kubelite daemon/process](https://microk8s.io/docs/configuring-services). 
- /snap/microk8s/6089/bin/k8s-dqlite --storage-dir=...: Dqlite (distributed SQLite) is a lightweight, distributed relational database. In MicroK8s, dqlite is used as the storage backend for the Kubernetes cluster data.
- /bin/bash /snap/microk8s/6089/apiservice-kicker: This script is part of MicroK8s' internal mechanisms. It monitors the API server and ensures it's functioning correctly. 
- /bin/bash /snap/microk8s/6089/run-cluster-agent-with-args: The cluster agent facilitates various cluster operations and communications. It starts the /snap/microk8s/6089/bin/cluster-agent process.

For all Microk8s services:
- Configurations are in /var/snap/microk8s/<current>/args/<service>
- Logs in /var/snap/microk8s/common/var/log, or use `journalctl -u snap.microk8s.daemon-kubelite`


Other commands to remember.

```shell
# For reference when needed
microk8s status
microk8s stop; microk8s start
#
snap services microk8s
snap info microk8s
sudo journalctl -u snap.microk8s.daemon-containerd
snap restart microk8s.daemon-containerd
```

### Access from remote internet using kubectl
Update the CSR file to include the external ip address of the VM.
vi /var/snap/microk8s/current/certs/csr.conf.template

Microk8s will automatically pick up the change and restart API server after regenerating certs. Then you can use "microk8s config" and copy it to a remote system.

If you run into issues, the other option (not recommended) for development work is to bypass TLS verification in ~/.kube/config, in the cluster section, right below the server name/ip.

```
- cluster:
    server: https://<ip>:<port>
    insecure-skip-tls-verify: true
  name: microk8s-cluster

```

In summary, Microk8s is pretty simple and well-designed software for experiment and production.

## Install addons
Note that a few basic software (eg. dns) were not installed by default. Microk8s uses addons to enable the additional software. Addons are wrappers on top of helm, and convenient as long as you review the versions.

### Customizing addons
[Reference](https://microk8s.io/docs/how-to-manage-addons)

The shell scripts for core addons are here:
https://github.com/canonical/microk8s-core-addons/tree/main/addons

They are available in /snap/microk8s/current/addons/core. You can  modify the script and run "microk8s enable <addon>". However, it is better to fork the repo, modify the scripts, and then:

```shell
microk8s addons repo add <repo_name> <repo_url>
microk8s enable <addon_name>
```

Note that microk8s gives priority to custom (user owned forked), then community, and then least priority to core repo in the event of a name conflict.

### Install basic addons

#### dns
DNS is already enabled by default, so we will skip it. Verify using `microk8s status`.

#### hostpath-storage
Primarily for testing purposes.

```shell
microk8s enable hostpath-storage
```

#### Metrics-server
Review the scripts.

```shell
cd /snap/microk8s/current/addons/core/addons/metrics-server
cat enable
cat metrics-server.yaml | grep image
```

The image version is 0.6.3. On reviewing the [metrics-server releases](https://github.com/kubernetes-sigs/metrics-server/releases), the latest version is 0.6.4 with almost no change from 0.6.3. So we can simply use this addon. 

```shell
microk8s enable metrics-server
```

#### Observability
Review the script.
```shell
ls -l /snap/microk8s/current/addons/core/addons/observability
cat /snap/microk8s/current/addons/core/addons/observability/enable
```

This script installs helm charts for kube-prometheus-stack, loki, and tempo (for trace). We will install only first 2. Summary of the script.

- Arguments
--kube-prometheus-stack-values: Specifies custom values for the Prometheus stack configuration.
--kube-prometheus-stack-version: Sets a specific version for the Prometheus stack.
--loki-stack-values: Provides custom values for the Loki configuration.
--loki-stack-version: Sets a specific version for the Loki stack.
--tempo-values: For configuring Tempo with custom values.
--tempo-version: Sets a specific version for Tempo.
--without-tempo: If present, it indicates that Tempo should not be installed.
- You need to run it everytime new nodes are added to the cluster.
- It configures kube-controller and kube-scheduler endpoints to be scraped by prometheus. It is necessary as those components are running as processes (not pods).


So the good part is that this script allows us to do necessary customization same as helm. And we can run it as many time without impacting anything (it uses helm upgrade --install).

kube-prometheus-stack 45.5.0 was released in Mar 2023. Most recent version is 55.5.1. 
Loki chart 2.9.9 was some time in 2022. Most recent version is 2.9.11 - we will use this as there is a [fix for a CVE with critical severity](https://github.com/grafana/helm-charts/commits/main/charts/loki-stack/Chart.yaml).

```shell
microk8s enable observability --kube-prometheus-stack-version=55.5.1 --loki-stack-version=2.9.11 --without-tempo
```

Note that the default storage used by observability is hostpath.


## Set up shared drive
Before proceeding to setup Nvidia tools, let us install the CSI for shared drive access.

**Note, your username/password are the credentials for the shared drive.**

```shell
helm repo add csi-driver-smb https://raw.githubusercontent.com/kubernetes-csi/csi-driver-smb/master/charts

helm upgrade csi-driver-smb csi-driver-smb/csi-driver-smb \
  --namespace kube-system \
  --version v1.13.0 \
  --set linux.kubelet="/var/snap/microk8s/common/var/lib/kubelet" \
  --install

# Create the Secret. Make sure to use your SMB shared drive (Paperspace) credentials
kubectl create secret generic smbcreds \
  --namespace default \
  --from-literal=username=$smb_username \
  --from-literal=password=$smb_password

# A copy of smb-storageclass.yml is under Script directory in the current repo
cp ./Scripts_Artifacts/smb-storageclass.yml /tmp/smb-storageclass.yml
kubectl get storageclass smb
# NOTE - you need to update the path to your shared drive!
kubectl apply -f /tmp/smb-storageclass.yml
```

To test an example:
```shell
kubectl apply -f Scripts_Artifacts/smb-test.yaml
kubectl exec smb-test-pod -- cat /mnt/data/testfile
kubectl exec smb-test-pod -- cat /mnt/data/testfile2
kubectl exec smb-test-pod-2 -- cat /mnt/data/testfile
kubectl delete -f Scripts_Artifacts/smb-test.yaml
# If pods do not become active and PVC is still not bound, then check the SMB controller pod log. 
# Most likely culprit is either you did not specify credentials or the path in the storageclass is incorrect.
```

## Set up GPU

For GPU, we need tools at different layers.
- Host driver (chapter 1)
- Nvidia container toolkit (chapter 3)
- Nvidia device plugin - required for kubernetes scheduler to be aware of GPU and schedule jobs
- DGCM (Nvidia data center gpu manager) based monitoring - required for prometheus/grafana monitoring


The best option is to use Nvidia GPU k8s operator (https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html), and have everything installed in k8s. Unfortunately it did not work with any options (direct install via Nvidia guidelines or even microk8s enable gpu). If you want to try out operator path, feel free to do so. It may be just that it did not work for A4000 GPUs, but will work for other GPUs.

Given that we are already familiar with driver and container toolkit installation on the host, we just need to install device plugin and DGCM. This will allow us to isolate if anything goes wrong and troubleshoot faster. In any case, these can be easily automated via ansible helm. This is a good condensed reading relevant to GPU installation.

https://microk8s.io/docs/addon-gpu


### Install using Operator (for future)
This section is for reference only and may be used in future. For now, we will install the components using helm chart (following section).

Review the script.
```shell
ls -l /snap/microk8s/current/addons/core/addons/gpu
cat enable
```

Configurable options: --driver, --version (default v22.9.1), --toolkit-version, --value (for helm)

Let us use 23.9.1 (https://github.com/NVIDIA/gpu-operator/releases)


Refer to [nvidia operator doc](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) for all options
microk8s enable --version=v23.9.1 --set driver.enabled=false --set toolkit.enabled=false



### Install host driver

```shell
ubuntu-drivers list --gpgpu --recommended
sudo ubuntu-drivers install
apt search nvidia-utils-535
sudo apt install nvidia-utils-535-server
# We do not need CUDA as it will be part of containers
microk8s stop
reboot 
# Verify nvidia-smi post reboot
```

### Install nvidia-container-toolkit on the host

curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update
sudo apt-get install nvidia-container-runtime


cat /var/snap/microk8s/current/args/containerd-template.toml

Note that it does not contain any reference to nvidia container runtime. We need to update this file. Add the following to /var/snap/microk8s/current/args/containerd-template.toml under the right section. Refer to the [pre-requisites for nvidia device plugin](https://github.com/NVIDIA/k8s-device-plugin#prerequisites).

```quote
version = 2
[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    [plugins."io.containerd.grpc.v1.cri".containerd]
      default_runtime_name = "nvidia"

      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.nvidia]
          privileged_without_host_devices = false
          runtime_engine = ""
          runtime_root = ""
          runtime_type = "io.containerd.runc.v2"
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.nvidia.options]
            BinaryName = "nvidia-container-runtime"
```

sudo snap restart microk8s
OR
snap restart microk8s.daemon-containerd

Note: Because Microk8s containerd is on a different path, you  have to configure the containerd to set up nvidia. [This issue](https://github.com/canonical/microk8s/issues/3959) is good to review if you run into issues.


### Install Device Plugin on k8s

https://github.com/NVIDIA/k8s-device-plugin?tab=readme-ov-file#deployment-via-helm


helm repo add nvdp https://nvidia.github.io/k8s-device-plugin
helm repo update
helm search repo nvdp --devel
helm upgrade -i nvdp nvdp/nvidia-device-plugin \
  --namespace nvidia-device-plugin \
  --create-namespace \
  --version 0.14.3



# Test

$ cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  restartPolicy: Never
  containers:
    - name: cuda-container
      image: nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda10.2
      resources:
        limits:
          nvidia.com/gpu: 1 # requesting 1 GPU
  tolerations:
  - key: nvidia.com/gpu
    operator: Exists
    effect: NoSchedule
EOF


kubectl logs gpu-pod

