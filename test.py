import requests

BASE = "http://127.0.0.1:5000/"

# Adding the Virtual Machines in the Resource Pool:
response = requests.put(BASE + "virtualmachine/1", {"hostname": "KVM-VM-001", "ip": "1.1.1.1", 'allocstatus': 'Available'})
print(response.json())
response = requests.put(BASE + "virtualmachine/2", {"hostname": "KVM-VM-002", "ip": "2.2.2.2", 'allocstatus': 'Available'})
print(response.json())
response = requests.put(BASE + "virtualmachine/3", {"hostname": "KVM-VM-003", "ip": "3.3.3.3", 'allocstatus': 'Available'})
print(response.json())
response = requests.put(BASE + "virtualmachine/4", {"hostname": "KVM-VM-004", "ip": "4.4.4.4", 'allocstatus': 'Available'})
print(response.json())
response = requests.put(BASE + "virtualmachine/5", {"hostname": "KVM-VM-005", "ip": "5.5.5.5", 'allocstatus': 'Available'})
print(response.json())

# Duplicating the Virtual Machines in the Resource Pool
# Returns message saying {'message': 'VMID already exists'}
response = requests.put(BASE + "virtualmachine/3", {"hostname": "KVM-VM-003", "ip": "3.3.3.3", 'allocstatus': 'Available'})
print(response.json())

# Requesting a resource from the VM Resource pool
# Returns details of the VM allocated from the Resourse Pool
# Example: {'virtmach': 1, 'hostname': 'KVM-VM-001', 'ip': '1.1.1.1', 'allocstatus': 'Available'}
response = requests.get(BASE + "virtualmachine/1")
print(response.json())
response = requests.get(BASE + "virtualmachine/2")
print(response.json())
response = requests.get(BASE + "virtualmachine/3")
print(response.json())
response = requests.get(BASE + "virtualmachine/4")
print(response.json())
response = requests.get(BASE + "virtualmachine/5")
print(response.json())

# Requesting a ALREADY ALLOCATED resource from the VM Resource pool
# Returns message saying: {'message': 'VMs not available for assignment, either all are reserved or down for maintenance'}  
response = requests.get(BASE + "virtualmachine/1")
print(response.json())
response = requests.get(BASE + "virtualmachine/5")
print(response.json())

# OAM task -  Delete VM from the Resource Pool
# Returns list of VM available in the Resourse Pool
response = requests.delete(BASE + "virtualmachine/5")
print(response.json())

# Deleting Non existing machine:
response = requests.delete(BASE + "virtualmachine/50")
print(response.json())
response = requests.delete(BASE + "virtualmachine/100")
print(response.json())

# FREEING TTHE RESOURCES: Returning the VM to the Resource Pool
response = requests.patch(BASE + "virtualmachine/1", {"ip": "1.1.1.1"})
print(response.json())
response = requests.patch(BASE + "virtualmachine/2", {"ip": "2.2.2.2"})
print(response.json())
response = requests.patch(BASE + "virtualmachine/3", {"ip": "3.3.3.3"})
print(response.json())
response = requests.patch(BASE + "virtualmachine/4", {"ip": "4.4.4.4"})
print(response.json())

