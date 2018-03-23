
# coding: utf-8

# How to watch changes to an object
# ==================
# 
# In this notebook, we learn how kubernetes API resource Watch endpoint is used to observe resource changes. It can be used to get information about changes to any kubernetes object.

from kubernetes import client, watch


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


# ### Create API instance

api_instance = client.CoreV1Api()


# ### Run a Watch on the Pods endpoint. 
# Watch would be executed and produce output about changes to any Pod. After running the cell below, You can test this by running the Pod notebook [create_pod.ipynb](create_pod.ipynb) and observing the additional output here. You can stop the cell from running by restarting the kernel.

w = watch.Watch()
for event in w.stream(api_instance.list_pod_for_all_namespaces, timeout_seconds=15):
    print("Event: %s %s %s" % (event['type'],event['object'].kind, event['object'].metadata.name))

