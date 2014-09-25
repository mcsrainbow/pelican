Title: Create an Ansible Module and then use Module Provided Facts
Date: 2014-09-25 16:47
Category: Linux&Unix
Tags: Ansible, Facts
Author: mcsrainbow
Summary: Sometimes the default Ansible Facts are not enough. <p>But we can create an Ansible module and then use module provided 'Facts'.

Sometimes the default Ansible Facts are not enough.

For example, Ansible doesn't provide "ansible_private_ipv4_address" which with private IP address.

With it, we don't need to worry about which IP on which NIC should be used.

But we can create an Ansible module and then use module provided 'Facts'.

**The steps:**

`[root@idc-server2 ~]# ifconfig`

```
eth0      Link encap:Ethernet  HWaddr 1B:2B:3B:4B:5B:6B
          inet addr:172.16.1.2  Bcast:172.16.1.255  Mask:255.255.252.0
...

eth1      Link encap:Ethernet  HWaddr 1A:2A:3A:4A:5A:6A
          inet addr:100.100.100.100  Bcast:100.100.100.255  Mask:255.255.255.240
...

lo        Link encap:Local Loopback 
          inet addr:127.0.0.1  Mask:255.0.0.0
...

```

`[root@idc-server1 ansible]# vim myfacts.yml`

```
---
- hosts: idc-server2
  roles:
  - myfacts
```

`[root@idc-server1 ansible]# mkdir -p roles/myfacts/{tasks,templates}`

```
---
- name: run myfacts module to get customized facts
  myfacts: get_facts=yes

- name: update file with the customized facts
  template: src=myfacts.txt.j2 dest=/tmp/myfacts.txt
```

`[root@idc-server1 ansible]# mkdir -p library/heylinux`

`[root@idc-server1 ansible]# vim library/heylinux/myfacts`

```
ansible_private_ipv4_address : {{ ansible_private_ipv4_address }}

```

`[root@idc-server1 ansible]# vim /usr/share/ansible/heylinux/myfacts`

```
#!/usr/bin/python

import sys
import json
import shlex
import commands
import re

def get_ansible_private_ipv4_address():
    iprex = "(^192\.168)|(^10\.)|(^172\.1[6-9])|(^172\.2[0-9])|(^172\.3[0-1])"
    output = commands.getoutput("""/sbin/ifconfig |grep "Link encap" |awk '{print $1}' |grep -wv 'lo'""")
    nics = output.split('\n')
    for i in nics:
        ipaddr = commands.getoutput("""/sbin/ifconfig %s |grep -w "inet addr" |cut -d: -f2 | awk '{print $1}'""" % (i))
        if re.match(iprex,ipaddr):
            ansible_private_ipv4_address = ipaddr
            return ansible_private_ipv4_address

ansible_facts_dict = {
        "changed" : False,
        "ansible_facts" : {
            }
    }

args_file = sys.argv[1]
args_data = file(args_file).read()

arguments = shlex.split(args_data)
for arg in arguments:
    if "=" in arg:
        (key, value) = arg.split("=")
        if key == "get_facts" and value == "yes":
            ansible_private_ipv4_address = get_ansible_private_ipv4_address()
            ansible_facts_dict['ansible_facts']['ansible_private_ipv4_address'] = ansible_private_ipv4_address

print json.dumps(ansible_facts_dict)
```

`[root@idc-server1 ansible]# ansible-playbook -u root myfacts.yml -i hosts`

```
PLAY [idc1-server2] ***************************************************************

GATHERING FACTS ***************************************************************
ok: [idc1-server2]

TASK: [myfacts | run myfacts module to get customized facts] **************
ok: [idc1-server2]

TASK: [myfacts | update file with the customized facts] *********************
changed: [idc1-server2]

PLAY RECAP ********************************************************************
idc1-server2                   : ok=3    changed=1    unreachable=0    failed=0  
```

`[root@idc-server1 ansible]# ssh idc1-server2 'cat /tmp/myfacts.txt'`

```
ansible_private_ipv4_address : 172.16.1.2
```
