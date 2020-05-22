Just some sample files

# SIP-Redis-2020
Sachin Saharan Redis clustering Internship project 2020


Guide to setup a redis cluster and to access it as a client.
===================================================================================================================

-------------------------------------------------------------------------------------------------------------------
Modules used to create Redis Cluster:

1) redis-trib
2) rediscluster

Now to install these modules in our system, we need to create a python virtual environment so that we can use pip
for installation. For that use the following commands:

-> mkdir 'dir-name'
  
-> cd 'dir-name'
  
-> virtualenv --python=/usr/local/python/python-2.7/std/bin/python  --system-site-packages  --inherit=/usr/local/python/python-2.7/std <name_of_the_virtualenv>

---To activate the virtual environment use:

->source <name_of_the_virtualenv>/bin/activate

---Now to install these moduels use:

-> pip install redis

-> pip install redis-trib

-> easy_install rediscluster

----------------------------------------------------------------------------------------------------------------

Redis Cluster Setup:-

1.) Creating a cluster on a local system.

- To create a cluster on a local system we need to provide two neccessary elements for each node:
a) port (at which node should run)
b) configuration file ( Which should contain all the cluster related configurations)

-- An example for a configuration file is( like redis.conf):

cluster-enabled yes

cluster-config-file cluster-node-1.conf

cluster-node-timeout 5000

appendonly yes

appendfilename node-1.aof

-- We can also provide a root directory for each node, where all its file will be stored (like .conf and .aof files), but
it is optional.


-----Now to create a redis cluster(and to perform other operations on cluster), open a python terminal(by using ipython command and being in your virtualenv) and then run the following commands:

-> ipython

>>> from redis_server import ClusterLocal

>>> master_nodes = [{'port': 7001, 'config': 'path/to/config_file', 'root': 'path/to/root'},{'port': 7002, 'config': 'path/to/config_file', 'root': 'path/to/root'},{'port': 7003, 'config': 'path/to/config_file', 'root': 'path/to/root'}]

>>> cluster = ClusterLocal(startup_nodes = master_nodes)

>>> cluster.run()     
/////   Create the cluster of three master nodes

>>> cluster.add_replica(master_port = 7001, slave_node = {'port': 7004, 'config': 'path/to/config_file'})
//// Add a replica node running at port 7004 on a master node running at port 7001

>>> cluster.add_node(new_node = {'port': 7005, 'config': 'path/to/config_file'})
//// Add a new master node into the cluster (Without any hash slots)

>>> cluster.del_node(del_node_port = 7002)
//// Delete a node running on port 7002. All the slots(and key-values inside the slots) in node 7002 will be distributed among other master nodes. Remember that a node can only be deleted if it doesn't have any slave nodes.

>>> cluster.kill(kill_node_port = 7001)
/// kill the node 127.0.0.1:7001. So now it's slave will be elected as a new master

>>> cluster.migrate(source_node_port = 7004, dest_node_port = 7005, slot_begin = 30, slot_end = 200 )
///  Transfer the slots from source node(7004) to destination node(7005). The range of slots transferred are from 
 slot_begin to slot_end. Please notice that initially, all the slots must belongs to the source node.

>>> cluster.rescue(alive_node_port = 7003, rescue_node = {'port': 7006, 'config': 'path/to/config_file'})
///  127.0.0.1:7003 is one of the nodes that is still alive in the cluster
and 127.0.0.1:7006 is the node that would take care of all failed slots

>>> cluster.shutdown(last_port = 7004)
/// To shutdown the cluster when there is just a single node left in the cluster


---- To access the cluster as a client use following commands:

-> ipython

>>> from redis_handle import RedisHandle

>>> clust = RedisHandle([{'host':'127.0.0.1', 'port': 7001}])
//// port that is provided has to be in the cluster

>>> client = clust.client()

>>> client.set('foo', 'bar')

>>> print(client.get('foo'))


-------------------------------------------------------------------------------------------------------------------------------


