# Redis cluster setup

## Modules Used:
1. redis
1. rediscluster
1. redis-trib

## Python virtual environment setup:
```bash
mkdir <dir-name>
cd <dir-name>

virtualenv --python=/usr/local/python/python-2.7/std/bin/python --system-site-packages --inherit=/usr/local/python/python-2.7/std <name_of_the_virtualenv>
```
### To activate virtual environment:
```bash
source <name_of_the_virtualenv>/bin/activate
```

## Installing modules
```
pip install redis

pip install redis-trib

easy_install rediscluster
 ```

---

## Cluster Creation on Local System

### Attributes passed:
1. Port
1. Configuration file
```
cluster-enabled yes
cluster-config-file cluster-node-1.conf
cluster-node-timeout 5000
appendonly yes
appendfilename node-1.aof
```
3. Root

##### Open python terminal:
```
ipython
```
### To Start a Cluster:
```python
from deshaw.db.redis_server import ClusterLocal

master_nodes = [{'port': 7001, 'config': 'path/to/config_file', 'root': 'path/to/root'},{'port': 7002, 'config': 'path/to/config_file', 'root': 'path/to/root'},{'port': 7003, 'config': 'path/to/config_file', 'root': 'path/to/root'}]

cluster = ClusterLocal(startup_nodes = master_nodes)

# Create cluste of 3 master nodes
cluster.run()

# Add a slave 127.0.0.1:7004 to node 127.0.0.1:7001
cluster.add_replica(master_port = 7001, slave_node = {'port': 7004, 'config': 'path/to/config_file', 'root': 'path/to/root'})

# Add a new master node 
cluster.add_node(new_node = {'port': 7005, 'config': 'path/to/config_file', 'root': 'path/to/root'})

# Remove the node 127.0.0.1:7002 from the cluster
# Hash slots will be distributed among other nodes
cluster.del_node(del_node_port = 7002)

#  kill 127.0.0.1:7001. Its slave will become new master
cluster.kill(kill_node_port = 7001)

# Transfer hash slots from one node to the other
cluster.migrate(source_node_port = 7004, dest_node_port = 7005, slot_begin = 30, slot_end = 200 )

# Rescue the cluster with failed slots
cluster.rescue(alive_node_port = 7003, rescue_node = {'port': 7006, 'config': 'path/to/config_file', 'root': 'path/to/root'})

# Shutdown the cluster with a single node
cluster.shutdown(last_port = 7004) 
```
### To Connect to a running Cluster:

```python
from deshaw.db.redis_handle import RedisHandle

# port that is in the cluster
cluster = RedisHandle([{'host':'127.0.0.1', 'port': 7001}])  

client = cluster.client()

client.set('foo', 'bar')

print(client.get('foo'))
```

---
---

## Running Cluster on a grid:

```python
from deshaw.db.redis_server import ClusterService

master_nodes = [{'port': 7001, 'config': 'path/to/config_file', 'root': 'path/to/root'},{'port': 7002, 'config': 'path/to/config_file', 'root': 'path/to/root'},{'port': 7003, 'config': 'path/to/config_file', 'root': 'path/to/root'}]

cluster = ClusterService(svcname = 'u/USER/redis-cluster', startup_nodes = master_nodes)

# Submit cluster on a grid
cluster.submit_to_grid()

# Add a slave node HOST:7005 to the node HOST:7001
cluster.add_replica(master_port = 7001, slave_node = {'port': 7005, 'config': 'path/to/config_file', 'root': 'path/to/root'})
```

## To Connect to a running Cluster:

```python
from deshaw.db.redis_handle import RedisHandle

cluster = RedisHandle(arg = 'u/USER/redis-cluster', iscluster = True)

client = cluster.client()

print(client.cluster_slots())

client.set('foo', 'bar')

print(client.get('foo'))
```


---
---

# Redis sentinel setup

### Some of Sentinel capabilities are:

* **Monitoring**.  Sentinel constantly checks if your master and replica instances are working as expected.
* **Automatic failover**. If a master is not working as expected, Sentinel can start a failover process where a replica is promoted to master, the other additional replicas are reconfigured to use the new master, and the applications using the Redis server are informed about the new address to use when connecting.

## Configuring Sentinel

Minimal sentinel configuration file looks like:

```
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 60000
sentinel failover-timeout mymaster 180000
sentinel parallel-syncs mymaster 1

sentinel monitor resque 192.168.1.3 6380 4
sentinel down-after-milliseconds resque 10000
sentinel failover-timeout resque 180000
sentinel parallel-syncs resque 5
```
The example configuration above basically monitors two sets of Redis instances, each composed of a master and an undefined number of replicas. One set of instances is called **mymaster**, and the other **resque**.

The meaning of the arguments of **sentinel monitor** statements is the following:

```
sentinel monitor <master-group-name> <ip> <port> <quorum>
```
* The **quorum** is the number of Sentinels that need to agree about the fact the master is not reachable, in order to really mark the master as failing, and eventually start a failover procedure if possible.
* However **the quorum is only used to detect the failure**. In order to actually perform a failover, one of the Sentinels need to be elected leader for the failover and be authorized to proceed. This only happens with the vote of the **majority of the Sentinel processes**.

> For more information please visit [Redis Sentinel Documentation](https://redis.io/topics/sentinel)

---
## Configuring Slave

To start a node as a slave node it's configuration file must contain:
```
slaveof <master_node_ip> <master_node_port>
```
---

## Running Sentinel on local system

```python
from deshaw.db.redis_server import SentinelLocal
sentinels = [
            {'port': 5000,'config': 'path/to/sentinel_config_file','root': 'path/to/root'}
            {'port': 5000,'config': 'path/to/sentinel_config_file','root': 'path/to/root'}
            {'port': 5000,'config': 'path/to/sentinel_config_file','root': 'path/to/root'}
            ]

master_nodes = [
                {'port': 6379, 'config': 'path/to/config_file', 'root': 'path/to/root',
                'slave': [
                {'port': 6380, 'config': 'path/to/config_file', 'root': 'path/to/root'},
                {'port': 6381, 'config': 'path/to/config_file', 'root': 'path/to/root'}
                ]},
                {'port': 6382, 'config': 'path/to/config_file', 'root': 'path/to/root'}
               ]

sentinel = SentinelLocal(sentinels = sentinels, master_nodes = master_nodes)

sentinel.run()
```
## To connect to a monitored master of a running Sentinel

Sentinel provides the address of the master for some **master group name** which can be used to get the master for that **master group name**.

```python
from deshaw.db.redis_handle import RedisHandle

sentinel_node = {'host': '127.0.0.1', 'port': 5000, 'master_group_name': 'mymaster'}

sentinel = RedisHandle(arg = sentinel_node, isSentinel = True)

client = sentinel.client()

client.set("foo","bar")

client.get("foo")
```




