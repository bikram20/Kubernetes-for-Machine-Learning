# Commands for setting up and configuring Microk8s

Cheat sheet for reference and useful when we setup automation.

## Setting up Resources in Paperspace

**Note** Recommend to create the cloud resources in Paperspace using a console if using first time. Much more convenient, allows you to see the cost etc, and you can stay focused on k8s/gpu. 


### Account 

If using Paperspace, set up your local CLI by setting up CLI with api.
https://docs.paperspace.com/core/api-reference/

```shell
node -v
npm install -g paperspace-node
paperspace -v
paperspace login  # Use email as login and api key as password
```

### Private Network
[CLI/API help](https://docs.paperspace.com/core/api-reference/networks)

**You have to do this one time from the console**, there's no API to create a private network.

```shell
paperspace networks list
```

Note the network ID where (either NY2 or AMS1) we will create the VM.

### VM
[CLI/API help](https://docs.paperspace.com/core/api-reference/machines)

Note the OS template id and networks list.
```shell
paperspace  templates list --label "Ubuntu 22.04 Server"
paperspace networks list
```

Note the exact machine type (hardware) from the console. 

**Keep in mind that there is a cost to using these VMs, so make sure to power-off the machine when you are not using.** If running first time, it is reasonable to use a CPU-only (eg. C6 - 0.16/hr) to get k8s running and setting up automation. You do not need a A100 ($3.09/hr), unless you specifically want MIG (multitenant GPU) feature.

```shell
#paperspace machines create  --region "East Coast (NY2)" --machine-type "C6" --size 100 --billingType "hourly" --machineName "bgubuntu-1" --templateId "t0nspur5" --networkId "nlflafvc" --dynamicPublicIp true

paperspace machines create  --region "East Coast (NY2)" --machine-type "A4000" --size 100 --billingType "hourly" --machineName "bgubuntu-1" --templateId "t0nspur5" --networkId "nlflafvc" --dynamicPublicIp true

#paperspace machines create  --region "East Coast (NY2)" --machine-type "A100" --size 100 --billingType "hourly" --machineName "bgubuntu-1" --templateId "t0nspur5" --networkId "nlflafvc" --dynamicPublicIp true

paperspace machines list
```

Connect using ssh.

### Shared Drive
We will use the shared storage from inside k8s, so no need to mount on the host. Assuming you have created already from the console (make sure it is in the same region where your infra will be running).

$PSKEY env variable has the paperspace api key. Personal information is masked.

```shell
# You will need to create a shared drive from the console
# jq . is for formatting the json output
curl -s --request POST  --header "Authorization: Bearer $PSKEY" --header 'content-type: application/json' --url https://api.paperspace.com/graphql  --data '{"query":"query SharedDrives($first: Int) {sharedDrives(first: $first) {nodes{id name mountPoint size username password region{name}}}}","variables":{"first":20}}' | jq .
```
