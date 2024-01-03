# Chapter 6 - Ansible Setup

It is expected that you are familiar with automation tools like ansible. In general, the set up for the entire k8s cluster with necessary driver, HA, add-ons and GPU support should be done with just 1 command. You will need familiarity with ansible when you need to customize configuration or troubleshoot any issues. 

## How to run

```shell
git clone <this_repo>
cd Ansible
Set up your inventory (ip addresses of your Paperspace VMs) in the inventory file.
In the cloned Ansible/roles/paperspace_rw_storage_class/vars/main.yml file, set up your Paperspace shared drive credentials. Note that you will need to rename/copy main-copyme.yml file.
```

That's all you need for default setup. Now you can install the whole cluster with GPU setup, shared drive and addons using the following.

```shell
ansible-playbook -i inventory microk8s-setup.yml -v
```

Logs will be in stdout and also in ansible.log file. At the end of it, the script will do the following (taken from microk8s-setup.yml):
    - nvidia-host-tools               # Host driver. Does not include fabric manager yet
    - system-setup                    # Basic system readiness and install snap
    - microk8s-node-install           # Install microk8s on each node
    - microk8s-cluster-setup          # Setup the cluster - can be N nodes, starting with 1
    - microk8s-addons                 # Set up basic addons (eg. metric-server and observability)
    - paperspace_rw_storage_class     # Setup Paperspace shared drive (SMB CIS)
    - nvidia-containerd-toolkit       # Add NVIDIA container toolkit for GPU/containerd
    - nvidia-device-plugin            # Add NVIDIA device plugin for GPU/k8s
    - test-a-gpu-container            # Apply a basic manifest. Check that container comes up. Run nvidia-smi inside the container


If something fails, review the task that failed. After that, start running from that task using the following (example task):
ansible-playbook -i inventory microk8s-setup.yml --start-at-task="Create symbolic link for kubectl" 

If you need to customize or add a task, you may like to use a tag for running only specific tasks as the following (example tag):
ansible-playbook -i inventory microk8s-setup.yml --tags add_microk8s_bin_to_path

Paperspace VM's have dynamic public IPs and may change between reboots. Make sure to fix the inventory file

### Safe shutdown
You will need to stop microk8s, and then shut down the machines.

ansible-playbook -i inventory microk8s-shutdown.yml

# Starting up a cluster (post shutdown)
Check IP addrsses when restarting the nodes after poweroff and update the inventory file.
paperspace machines list 2>/dev/null | grep "publicIpAddress" | awk '{print $2}' | tr -d '",'

ansible-playbook -i inventory microk8s-startup.yml

