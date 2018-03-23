
# coding: utf-8

# How to create a ConfigMap and use its data in Pods
# ===========================
# 
# [ConfigMaps](https://kubernetes.io/docs/tasks/configure-pod-container/configmap/) allow you to decouple configuration artifacts from image content to keep containerized applications portable. In this notebook we would learn how to create a ConfigMap and also how to use its data in Pods as seen in https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/

from kubernetes import client
from kubernetes.client.rest import ApiException


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


# ### Create API endpoint instance and API resource instances

api_instance = client.CoreV1Api()
cmap = client.V1ConfigMap()


# ### Create key value pair data for the ConfigMap

cmap.metadata = client.V1ObjectMeta(name="special-config")
cmap.data = {}
cmap.data["special.how"] = "very"
cmap.data["special.type"] = "charm"


# ### Create ConfigMap

api_instance.create_namespaced_config_map(namespace="default", body=cmap)


# ### Initialize test Pod container

container = client.V1Container(name="test-container")
container.image = "gcr.io/google_containers/busybox"
container.command = ["/bin/sh", "-c", "env"]


# ### Create API endpoint instance and API resource instances for test Pod

pod = client.V1Pod()
spec = client.V1PodSpec(containers=[container])
pod.metadata = client.V1ObjectMeta(name="dapi-test-pod")


# ### Define Pod environment variables with data from ConfigMaps

container.env = [client.V1EnvVar(name="SPECIAL_LEVEL_KEY"), client.V1EnvVar(name="SPECIAL_TYPE_KEY")]
container.env[0].value_from = client.V1EnvVarSource()
container.env[0].value_from.config_map_key_ref = client.V1ConfigMapKeySelector(name="special-config", key="special.how")

container.env[1].value_from = client.V1EnvVarSource()
container.env[1].value_from.config_map_key_ref = client.V1ConfigMapKeySelector(name="special-config", key="special.type")

spec.restart_policy = "Never"
spec.containers = [container]
pod.spec = spec


# ### Create Pod

api_instance.create_namespaced_pod(namespace="default", body=pod)


# ### View ConfigMap data from Pod log

log = ""
try: 
    log = api_instance.read_namespaced_pod_log(name="dapi-test-pod", namespace="default")
except ApiException as e:
    if str(e).find("ContainerCreating") != -1:
        print("Creating Pod container.\nRe-run current cell.")
    else:
        print("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)

for line in log.split("\n"):
    if line.startswith("SPECIAL"):
        print(line)


# ### Delete ConfigMap

api_instance.delete_namespaced_config_map(name="special-config", namespace="default", body=cmap)


# ### Delete Pod

api_instance.delete_namespaced_pod(name="dapi-test-pod", namespace="default", body=client.V1DeleteOptions())

