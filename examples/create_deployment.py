
# coding: utf-8

# How to create a Deployment
# ==========================
# 
# In this notebook, we show you how to create a Deployment with 3 ReplicaSets. These ReplicaSets are owned by the Deployment and are managed by the Deployment controller. We would also learn how to carry out RollingUpdate and RollBack to new and older versions of the deployment.

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

from example_utils.config import load as example_config

example_config()


extension = client.ExtensionsV1beta1Api()


# ### Create Deployment object

deployment = client.ExtensionsV1beta1Deployment()


# ### Fill required Deployment fields (apiVersion, kind, and metadata)

deployment.api_version = "extensions/v1beta1"
deployment.kind = "Deployment"
deployment.metadata = client.V1ObjectMeta(name="nginx-deployment")


# ### Pod template container description

container = client.V1Container(name="nginx")
container.image = "nginx:1.7.9"
container.ports = [client.V1ContainerPort(container_port=80)]


# ### Create Pod template

template = client.V1PodTemplateSpec()
template.metadata = client.V1ObjectMeta(labels={"app": "nginx"})
template.spec = client.V1PodSpec(containers=[container])


# ### A Deployment also needs a .spec section

spec = client.ExtensionsV1beta1DeploymentSpec(template=template)
spec.replicas = 3


deployment.spec = spec


# ### Create Deployment

extension.create_namespaced_deployment(namespace="default", body=deployment)


# ### Update container image 

deployment.spec.template.spec.containers[0].image = "nginx:1.9.1"


# ### Apply update (RollingUpdate)

extension.replace_namespaced_deployment(name="nginx-deployment", namespace="default", body=deployment)


# ### Create DeploymentRollback object
# This object is used to rollback to a previous version of the deployment.

rollback_to = client.ExtensionsV1beta1RollbackConfig()
rollback_to.revision = 0
rollback = client.ExtensionsV1beta1DeploymentRollback(name = "nginx-deployment", rollback_to=rollback_to)
rollback.api_version = "extensions/v1beta1"
rollback.kind = "DeploymentRollback"


# ### Execute RollBack

extension.create_namespaced_deployment_rollback(name="nginx-deployment", namespace="default", body=rollback)


# ### Delete Deployment

extension.delete_namespaced_deployment(name="nginx-deployment", namespace="default", body=client.V1DeleteOptions(propagation_policy="Foreground", grace_period_seconds=5))

