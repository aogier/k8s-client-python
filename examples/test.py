
# coding: utf-8

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


v1=client.CoreV1Api()


for ns in v1.list_namespace().items:
    print(ns.metadata.name)

