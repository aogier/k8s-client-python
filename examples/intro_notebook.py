
# coding: utf-8

# Managing kubernetes objects using common resource operations with the python client
# -----------------------------------------------------------------------------------------------
# 
# Some of these operations include;
# 
# - **`create_xxxx`** : create a resource object. Ex **`create_namespaced_pod`** and **`create_namespaced_deployment`**, for creation of pods and deployments respectively. This performs operations similar to **`kubectl create`**.
# 
# 
# - **`read_xxxx`** : read the specified resource object. Ex **`read_namespaced_pod`** and **`read_namespaced_deployment`**, to read pods and deployments respectively. This performs operations similar to **`kubectl describe`**.
# 
# 
# - **`list_xxxx`** : retrieve all resource objects of a specific type. Ex **`list_namespaced_pod`** and **`list_namespaced_deployment`**, to list pods and deployments respectively. This performs operations similar to **`kubectl get`**.
# 
# 
# - **`patch_xxxx`** : apply a change to a specific field. Ex **`patch_namespaced_pod`** and **`patch_namespaced_deployment`**, to update pods and deployments respectively. This performs operations similar to **`kubectl patch`**, **`kubectl label`**, **`kubectl annotate`** etc.
# 
# 
# - **`replace_xxxx`** : replacing a resource object will update the resource by replacing the existing spec with the provided one. Ex **`replace_namespaced_pod`** and **`replace_namespaced_deployment`**, to update pods and deployments respectively, by creating new replacements of the entire object. This performs operations similar to **`kubectl rolling-update`**, **`kubectl apply`** and **`kubectl replace`**.
# 
# 
# - **`delete_xxxx`** : delete a resource. This performs operations similar to **`kubectl delete`**.
# 
# 
# For Futher information see the Documentation for API Endpoints section in https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md

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


# ### Fill required object fields (apiVersion, kind, metadata and spec).

name = "my-busybox"

template = client.V1PodTemplateSpec()
template.metadata =  client.V1ObjectMeta(name="busybox")
template.metadata.labels = {"app":"busybox"}

container = client.V1Container(name = name, image = "busybox:1.26.1", args = ["sleep", "3600"])

template.spec = client.V1PodSpec(containers = [container])
spec = client.ExtensionsV1beta1DeploymentSpec(template=template)


# ### Create API endpoint instance as well as API resource instances (body and specification).

api_instance = client.ExtensionsV1beta1Api()
dep = client.ExtensionsV1beta1Deployment(metadata = client.V1ObjectMeta(name=name), spec=spec)


# ### Create Deployment using create_xxxx command for Deployments.

api_instance.create_namespaced_deployment(namespace="default",body=dep)


# ### Use list_xxxx command for Pod, to list Pods.

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
pods = v1.list_pod_for_all_namespaces(watch=False)
for i in pods.items:
    print("%s\t%s\t%s" %
          (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


# ### Use list_xxxx command for Deployment, to list Deployments.

deps = api_instance.list_namespaced_deployment(namespace="default")
for item in deps.items:
    print("%s  %s" % (item.metadata.namespace, item.metadata.name))


# ### Use read_xxxx command for Deployment, to display the detailed state of the created Deployment resource.

api_instance.read_namespaced_deployment(namespace="default",name=name)


# ### Use patch_xxxx command for Deployment, to make specific update to the Deployment.

dep.metadata.labels = {"key": "value"}
api_instance.patch_namespaced_deployment(name=name, namespace="default", body=dep)


# ### Use replace_xxxx command for Deployment, to update Deployment with a completely new version of the object.

dep.spec.template.spec.containers[0].image = "busybox:1.26.2"
api_instance.replace_namespaced_deployment(name=name, namespace="default", body=dep)


# ### Use delete_xxxx command for Deployment, to delete created Deployment.

api_instance.delete_namespaced_deployment(name=name, namespace="default", body=client.V1DeleteOptions(propagation_policy="Foreground", grace_period_seconds=5))

