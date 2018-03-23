
# coding: utf-8

# How to create a Service
# =============
# 
# In this notebook, we show you how to create a [Service](https://kubernetes.io/docs/concepts/services-networking/service/). 
# A service is a key Kubernetes API resource. It defines a networking abstraction to route traffic to a particular set of Pods using a label selection.

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


# ### Create API endpoint instance

api_instance = client.CoreV1Api()


# ### Create API resource instances

service = client.V1Service()


# ### Fill required Service fields (apiVersion, kind, and metadata)

service.api_version = "v1"
service.kind = "Service"
service.metadata = client.V1ObjectMeta(name="my-service")


# ### Provide Service .spec description
# Set Service object named **my-service** to target TCP port **9376** on any Pod with the **'app'='MyApp'** label. The label selection allows Kubernetes to determine which Pod should receive traffic when the service is used.

spec = client.V1ServiceSpec()
spec.selector = {"app": "MyApp"}
spec.ports = [client.V1ServicePort(protocol="TCP", port=80, target_port=9376)]
service.spec = spec


# ### Create Service

api_instance.create_namespaced_service(namespace="default", body=service)


# ### Delete Service

delete_options = client.models.v1_delete_options.V1DeleteOptions()
api_instance.delete_namespaced_service(name="my-service",
                                       namespace="default",
                                       body=delete_options)

