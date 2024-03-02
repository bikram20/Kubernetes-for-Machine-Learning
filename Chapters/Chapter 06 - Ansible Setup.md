# Chapter 6 - Ansible Setup

It is expected that you are familiar with automation tools like ansible. In general, the set up for the entire k8s cluster with necessary driver, HA, add-ons and GPU support should be done with just 1 command. You will need familiarity with ansible when you need to customize configuration or troubleshoot any issues. 

## How to run

```shell
git clone <this_repo>
cd Ansible
```

There are 4 different playbooks:
- Use **paperspace-vm-manage.yml** for setting up your VMs. It is declarative (can run multiple times) and automatically populates the inventory file. Note that a create/delete for a VM takes some time to take effect, so you will need to rerun paperspace-vm-manage.yml playbook for the inventory file to be correctly populated.
- **microk8s-setup.yml** is the main playbook. It sets up microk8s cluster with GPU drivers, necessary addons and shared drive. <b>Future: Bypass most of the steps by creating and using custom image pre-installed with drivers and microk8s. This can save most of the setup time.</b>
- microk8s-shutdown.yml is the playbook to shutdown the cluster and poweroff the machines. Helpful if you are not using the cluster and plan to shutdown to save cost.
- microk8s-startup.yml starts the microk8s cluster. Note, it does NOT poweron the machines. You need to do that manually for now.


### Setting up your VMs in Paperspace

**You must set up your paperspace API key before you run the playbook.**
- In the cloned Ansible/roles/paperspace-vm-manager/defaults/main.yml file, set up the Paperspace API key and VM defaults. [Reference](https://docs.paperspace.com/core/api-reference/machines#create)

You may want to create multiple counts of machines of different categories - for example: 2 machines for C4 cpu-only VMs, 3 machines for A4000 gpu VMs etc. You should first configure your desired spec in the playbook paperspace-vm-manage.yml. An example below.

```shell
---
- name: Deploy VMs to Paperspace
  hosts: localhost
  gather_facts: no
  roles:
    - role: paperspace-vm-manager
      vars:
        machine_name: "bg_C4"
        machine_type: "C4"
        machine_counts: 2
    - role: paperspace-vm-manager
      vars:
        machine_name: "bg_P4000"
        machine_type: "A4000"
        machine_counts: 1

```

The playbook is designed to be declarative, meaning you may change the machine_counts and rerun anytime. Even without changing anything, it will simply update the inventory file. Note that you should not change the VM names manually in the console, as the script relies on the names of the VMs to identify the machines.

To set up your VMs per your spec, run the playbook.

```shell
ansible-playbook paperspace-vm-manage.yml -v
```

Note that the inventory file will not be fully populated at this time. That's because it takes a while for the systems to boot and get ip addresses. So re-rerun the playbook again after 30-60 seconds. It is idempotent, so no issues even if you run many times. Inventory file should be populated after 30-60 seconds.

Now your VMs are ready and you can set up the microk8s cluster.


### Setting up the Microk8s Cluster

**You must configure the following before you run the playbook.**
- In the cloned Ansible/roles/paperspace_rw_storage_class/vars/main.yml file, set up your Paperspace shared drive credentials. Note that you will need to rename/copy main-copyme.yml file to main.yml.
In the cloned Scripts_Artifacts/smb_storageclass.yml file, set up your Paperspace shared drive network path.

That's all you need for default setup. Now you can install the whole cluster with GPU setup, shared drive and addons using the following.

```shell
# It is designed to be idempotent, so should not impact even if you run multiple times
ansible-playbook -i inventory microk8s-setup.yml -v
```

Logs will be in stdout and also in ansible.log file. At the end of it, the script will do the following (taken from microk8s-setup.yml):
```block
    - nvidia-host-tools               # Host driver. Does not include fabric manager yet
    - system-setup                    # Basic system readiness and install snap
    - microk8s-node-install           # Install microk8s on each node
    - microk8s-cluster-setup          # Setup the cluster - can be N nodes, starting with 1
    - microk8s-addons                 # Set up basic addons (eg. metric-server and observability)
    - paperspace_rw_storage_class     # Setup Paperspace shared drive (SMB CIS)
    - nvidia-containerd-toolkit       # Add NVIDIA container toolkit for GPU/containerd
    - nvidia-device-plugin            # Add NVIDIA device plugin for GPU/k8s
    - test-a-gpu-container            # Apply a basic manifest. Check that container comes up. Run nvidia-smi inside the container
```

If something fails, review the task that failed. After that, start running from that task using the following (example task):
```shell
ansible-playbook -i inventory microk8s-setup.yml --start-at-task="Create symbolic link for kubectl" 
```

If you need to customize or add a task, you may like to use a tag for running only specific tasks as the following (example tag):
```shell
ansible-playbook -i inventory microk8s-setup.yml --tags add_microk8s_bin_to_path
```

### Safe shutdown
You will need to stop microk8s, and then shut down the machines.
```shell
ansible-playbook -i inventory microk8s-shutdown.yml
```

### Starting up a cluster (post shutdown)
Paperspace VM's have dynamic public IPs and may change between reboots. Make sure to fix the inventory file. You may just re-run this after you power-on the VMs manually.

```shell
ansible-playbook paperspace-vm-manage.yml -v
```


```shell
ansible-playbook -i inventory microk8s-startup.yml
```
