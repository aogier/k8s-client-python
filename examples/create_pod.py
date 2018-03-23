
# coding: utf-8

# How to start a Pod
# ==================
# 
# In this notebook, we show you how to create a single container Pod.
# 
# Start by importing the Kubernetes module
# -----------------------------------------

from kubernetes import client


# 
# Client configuration is simplified so you can run examples either inside or outside a k8s scheduled pod. For normal use you will have to choose
# 
# ```python
# from kubernetes import config
# 
# # Choose one:
# 
# # from inside a cluster:
# config.load_incluster_config()
# 
# # from outside a cluster:
# config.load_kube_config()
# 
# ```
# 
# If you are using a proxy, you can use the _client Configuration_ to setup the host that the client should use. Otherwise read the kubeconfig file.

from example_utils.config import load as example_config

example_config()


# Pods are a stable resource in the V1 API group. Instantiate a client for that API group endpoint.

v1=client.CoreV1Api()


# In this example, we only start one container in the Pod. The container is an instance of the _V1Container_ class. 

container=client.V1Container(name="busybox")
container.image="busybox"
container.args=["sleep", "3600"]


pod=client.V1Pod()
spec=client.V1PodSpec(containers=[container])
pod.metadata=client.V1ObjectMeta(name="busybox")


# The specification of the Pod is made of a single container in its list.

pod.spec = spec


# Get existing list of Pods, before the creation of the new Pod.

ret = v1.list_namespaced_pod(namespace="default")
for i in ret.items:
    print("%s  %s  %s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


# You are now ready to create the Pod.

v1.create_namespaced_pod(namespace="default",body=pod)


# Get list of Pods, after the creation of the new Pod. Note the newly created pod with name "busybox"

ret = v1.list_namespaced_pod(namespace="default")
for i in ret.items:
    print("%s  %s  %s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


# Delete the Pod
# --------------
# 
# You refer to the Pod by name, you need to add its namespace and pass some _delete_ options.

v1.delete_namespaced_pod(name="busybox", namespace="default", body=client.V1DeleteOptions())

