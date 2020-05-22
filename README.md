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






