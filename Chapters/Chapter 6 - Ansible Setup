Chapter 6 - Ansible Setup



Check IP addrsses when restarting the nodes after poweroff:
paperspace machines list 2>/dev/null | grep "publicIpAddress" | awk '{print $2}' | tr -d '",'

ansible-playbook -i inventory microk8s-setup.yml
ansible-playbook -i inventory microk8s-setup.yml --start-at-task="Create symbolic link for kubectl" 
ansible-playbook -i inventory microk8s-setup.yml --tags add_microk8s_bin_to_path

ansible-playbook -i inventory microk8s-shutdown.yml
ansible-playbook -i inventory microk8s-startup.yml


# Must for using NVIDIA ansible role
ansible-galaxy install nvidia.nvidia_driver

## Driver update
Most important. There are 2 options. We recommend the Ubuntu APT based installation.

### Ubuntu recommended

ansible-playbook -v -i inventory nvidia-drivers-via-ubuntu.yml 


### NVIDIA ansible role

ansible-playbook -v -i inventory nvidia-drivers-via-nvidia.yml 

https://blog.deploif.ai/posts/install_nvidia_drivers

We recommend that you must get the driver installed first. If that fails, then everything else will fail. Hence we separate out the driver install into a separate playbook.

Mandatory to configure the branch/version of the driver. As of Dec 2023, 535 branch seems to be well supported with an LTS timeline up to 2026.


# Install the rest of the system

ansible-playbook -i inventory microk8s-setup.yml -v

