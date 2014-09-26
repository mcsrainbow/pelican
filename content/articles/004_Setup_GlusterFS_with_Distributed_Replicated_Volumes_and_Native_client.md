Title: Setup GlusterFS with Distributed Replicated Volumes and Native client
Date: 2014-09-26 15:39
Category: Linux&Unix
Tags: GlusterFS, Distributed
Author: mcsrainbow
Summary: **OS: ** CentOS 6.4 x86_64 Minimal <p>**1. Install packages, on idc1-server{1-4}:** <p>`# wget -P /etc/yum.repos.d http://download.gluster.org/pub/gluster/glusterfs/LATEST/CentOS/glusterfs-epel.repo` <p>`# yum install -y glusterfs glusterfs-server glusterfs-fuse` <p>`# /etc/init.d/glusterd start` <p>...

**OS: ** CentOS 6.4 x86_64 Minimal

#### 1. Install packages, on idc1-server{1-4}:

`# wget -P /etc/yum.repos.d http://download.gluster.org/pub/gluster/glusterfs/LATEST/CentOS/glusterfs-epel.repo`

`# yum install -y glusterfs glusterfs-server glusterfs-fuse`

`# /etc/init.d/glusterd start`

`# chkconfig glusterd on`

#### 2. Configure peers, just on idc1-server1:

`[root@idc1-server1 ~]# gluster peer probe idc1-server2`

```
peer probe: success
```

`[root@idc1-server1 ~]# gluster peer probe idc1-server3`

```
peer probe: success
```

`[root@idc1-server1 ~]# gluster peer probe idc1-server4`

```
peer probe: success
```

**NOTE:**

The following step is very important with the version 3.4.3!

If configured all peers with hostname on one host, must remember to recreate the peer of this host on another host.

Otherwise all other hosts cannot recognize this host by hostname.
10.1.1.35 is the ip address of idc1-server1, detach it then probe with hostname.

Just on idc1-server2:

`[root@idc1-server2 ~]# gluster peer detach 10.1.1.35`

```
peer detach: success
```

`[root@idc1-server2 ~]# gluster peer probe idc1-server1`

```
peer probe: success
```

Just on idc1-server2:

`[root@idc1-server2 ~]# gluster peer status`

```
Number of Peers: 3

Hostname: idc1-server3
Uuid: 01f25251-9ee6-40c7-a322-af53a034aa5a
State: Peer in Cluster (Connected)
  
Hostname: idc1-server4
Uuid: 212295a6-1f38-4a1e-968c-577241318ff1
State: Peer in Cluster (Connected)
  
Hostname: idc1-server1
Port: 24007
Uuid: ed016c4e-7159-433f-88a5-5c3ebd8e36c9
State: Peer in Cluster (Connected)
```

#### 3. Create directories, on idc1-server{1-4}:

`# mkdir -p /usr/local/share/{datavolume1,datavolume2,datavolume3}`

`# chown -R root:root /mnt/{datavolume1,datavolume2,datavolume3}`

`# ls -l /usr/local/share/`

```
total 24
drwxr-xr-x.  2 root root 4096 Sep 23  2011 applications
drwxr-xr-x   2 root root 4096 Apr  1 12:19 datavolume2
drwxr-xr-x.  2 root root 4096 Sep 23  2011 info
drwxr-xr-x. 21 root root 4096 Feb 20  2013 man
drwxr-xr-x   2 root root 4096 Apr  1 12:19 datavolume1
drwxr-xr-x   2 root root 4096 Apr  1 12:19 datavolume3
```

#### 4. Create Distributed Replicated Volumes, just on idc1-server1:

`[root@idc1-server1 ~]# gluster volume create datavolume1 replica 2 transport tcp idc1-server1:/usr/local/share/datavolume1 idc1-server2:/usr/local/share/datavolume1 idc1-server3:/usr/local/share/datavolume1 idc1-server4:/usr/local/share/datavolume1 force`

```
volume create: datavolume1: success: please start the volume to access data
```

`[root@idc1-server1 ~]# gluster volume create datavolume2 replica 2 transport tcp idc1-server1:/usr/local/share/datavolume2 idc1-server2:/usr/local/share/datavolume2 idc1-server3:/usr/local/share/datavolume2 idc1-server4:/usr/local/share/datavolume2 force`

```
volume create: datavolume2: success: please start the volume to access data
```

`[root@idc1-server1 ~]# gluster volume create datavolume3 replica 2 transport tcp idc1-server1:/usr/local/share/datavolume3 idc1-server2:/usr/local/share/datavolume3 idc1-server3:/usr/local/share/datavolume3 idc1-server4:/usr/local/share/datavolume3 force`

```
volume create: datavolume3: success: please start the volume to access data
```

`[root@idc1-server1 ~]# gluster volume start datavolume1`

```
volume start: datavolume1: success
```

`[root@idc1-server1 ~]# gluster volume start datavolume2`

```
volume start: datavolume2: success
```

`[root@idc1-server1 ~]# gluster volume start datavolume3`

```
volume start: datavolume3: success
```

`[root@idc1-server1 ~]# gluster volume info`

```
Volume Name: datavolume1
Type: Distributed-Replicate
Volume ID: aea76c2a-b754-4037-9634-c2062e2955c3
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: idc1-server1:/usr/local/share/datavolume1
Brick2: idc1-server2:/usr/local/share/datavolume1
Brick3: idc1-server3:/usr/local/share/datavolume1
Brick4: idc1-server4:/usr/local/share/datavolume1
 
Volume Name: datavolume2
Type: Distributed-Replicate
Volume ID: 1ed65c6e-ee23-475a-82c7-2967e2fc2569
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: idc1-server1:/usr/local/share/datavolume2
Brick2: idc1-server2:/usr/local/share/datavolume2
Brick3: idc1-server3:/usr/local/share/datavolume2
Brick4: idc1-server4:/usr/local/share/datavolume2
 
Volume Name: datavolume3
Type: Distributed-Replicate
Volume ID: b63bb4ea-bd37-4dd6-9a4c-230e6d236afa
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: idc1-server1:/usr/local/share/datavolume3
Brick2: idc1-server2:/usr/local/share/datavolume3
Brick3: idc1-server3:/usr/local/share/datavolume3
Brick4: idc1-server4:/usr/local/share/datavolume3
```

#### 5. Configure the Network ACL, just on idc1-server1:

`[root@idc1-server1 ~]# gluster volume set datavolume1 auth.allow 10.1.1.*,10.1.2.*`

#### 6. Tests on idc1-client15, install the version '-3.4.0.57rhs-1.el6_5' which supports option: 'backup-volfile-servers'

`[root@idc1-client15 ~]# yum install -y glusterfs-3.4.0.57rhs-1.el6_5 glusterfs-libs-3.4.0.57rhs-1.el6_5 glusterfs-fuse-3.4.0.57rhs-1.el6_5`

`[root@idc1-client15 ~]# mkdir -p /mnt/{datavolume1,datavolume2,datavolume3}`

`[root@idc1-client15 ~]# chown -R root:root /mnt/{datavolume1,datavolume2,datavolume3}`

`[root@idc1-client15 ~]# mount -t glusterfs -o backup-volfile-servers=idc1-server2:idc1-server3:idc1-server4,ro idc1-server1:datavolume1 /mnt/datavolume1/`

`[root@idc1-client15 ~]# mount -t glusterfs -o backup-volfile-servers=idc1-server2:idc1-server3:idc1-server4,ro idc1-server1:datavolume2 /mnt/datavolume2/`

`[root@idc1-client15 ~]# mount -t glusterfs -o backup-volfile-servers=idc1-server2:idc1-server3:idc1-server4,ro idc1-server1:datavolume3 /mnt/datavolume3/`

`[root@idc1-client15 ~]# df -h`

```
Filesystem            Size  Used Avail Use% Mounted on
/dev/mapper/vg_t-lv_root
                       59G  7.7G   48G  14% /
tmpfs                 3.9G     0  3.9G   0% /dev/shm
/dev/xvda1            485M   33M  428M   8% /boot
idc1-server3:datavolume1     98G  8.6G   85G  10% /mnt/datavolume1
idc1-server3:datavolume2     98G  8.6G   85G  10% /mnt/datavolume2
idc1-server3:datavolume3     98G  8.6G   85G  10% /mnt/datavolume3
```

**Tests:**

Write on idc1-client15 mount point /mnt/datavolume1:

`[root@idc1-client15 ~]# umount /mnt/datavolume1`

`[root@idc1-client15 ~]# mount -t glusterfs idc1-server3:datavolume1 /mnt/datavolume1/`

`[root@idc1-client15 ~]# echo "This is idc1-client15" > /mnt/datavolume1/hello.txt`

`[root@idc1-client15 ~]# mkdir /mnt/testdir`

`[root@idc1-server1 ~]# ls /usr/local/share/datavolume1/`

```
hello.txt testdir
```

Saw hello.txt and testdir

Write on idc1-server1 volumes dir /usr/local/share/datavolume1:

`[root@idc1-server1 ~]# echo "This is idc1-server1" > /usr/local/share/datavolume1/hello.2.txt`

`[root@idc1-server1 ~]# mkdir /usr/local/share/datavolume1/test2`

`[root@idc1-client15 ~]# ls /mnt/datavolume1`

`[root@idc1-client15 datavolume1]# ls -l /mnt/datavolume1`

```
hello.txt testdir
```

Didn't see hello.2.txt and test2

Write on idc1-server1 mount point /mnt/datavolume1:

`[root@idc1-server1 ~]# mount -t glusterfs idc1-server1:datavolume1 /mnt/datavolume1/`

`[root@idc1-server1 ~]# echo "This is idc1-server1" > /mnt/datavolume1/hello.3.txt`

`[root@idc1-server1 ~]# mkdir /mnt/datavolume1/test3`

`[root@idc1-client15 datavolume1]# ls /mnt/datavolume1`

```
hello.2.txt  hello.3.txt hello.txt  test2  test3  testdir
```

Saw hello.3.txt and test3, and the hello.2.txt and test2 also.

So I guess if we just write or delete file outside the mount point, it doesn't notify other nodes, so the changes didn't take effect.
We should mount it on all servers which we want to write or delete files.

**Other Notes:**

Delete:

`# gluster volume stop datavolume1`


`# gluster volume delete datavolume1`

Move:

`# gluster peer detach idc1-server4`

ACL:

`# gluster volume set datavolume1 auth.allow 10.1.1.*,10.1.2.*`

Add:

`# gluster peer probe idc1-server5`

`# gluster peer probe idc1-server6`

`# gluster volume add-brick datavolume1 idc1-server5:/usr/local/share/datavolume1 idc1-server6:/usr/local/share/datavolume1`

Shrink and migration:

`# gluster volume remove-brick datavolume1 idc1-server1:/usr/local/share/datavolume1 idc1-server5:/usr/local/share/datavolume1 start`

`# gluster volume remove-brick datavolume1 idc1-server1:/usr/local/share/datavolume1 idc1-server5:/usr/local/share/datavolume1 status`

`# gluster volume remove-brick datavolume1 idc1-server1:/usr/local/share/datavolume1 idc1-server5:/usr/local/share/datavolume1 commit`

Rebalance:

`# gluster volume rebalance datavolume1 start`

`# gluster volume rebalance datavolume1 status`

`# gluster volume rebalance datavolume1 stop`

If idc1-server1 dead:

`# gluster volume replace-brick datavolume1 idc1-server1:/usr/local/share/datavolume1 idc1-server5:/usr/local/share/datavolume1 commit -force`

`# gluster volume heal datavolume1 full`
