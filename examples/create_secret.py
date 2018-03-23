
# coding: utf-8

# How to create and use a Secret
# ================
# 
# A [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) is an object that contains a small amount of sensitive data such as a password, a token, or a key. In this notebook, we would learn how to create a Secret and how to use Secrets as files from a Pod as seen  in https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets

from kubernetes import client
from kubernetes.stream import stream

import time


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
client.configuration.assert_hostname = False


# ### Create API endpoint instance and API resource instances

api_instance = client.CoreV1Api()
sec  = client.V1Secret()


# ### Fill required Secret fields

sec.metadata = client.V1ObjectMeta(name="mysecret")
sec.type = "Opaque"
sec.data = {"username": "bXl1c2VybmFtZQ==", "password": "bXlwYXNzd29yZA=="}


# ### Create Secret

api_instance.create_namespaced_secret(namespace="default", body=sec)


# ### Add volumeMount which would be used to hold secret

volume_mounts = [client.V1VolumeMount(name = "foo", mount_path = "/srv/secret")]


# ### Create test Pod API resource instances

pod = client.V1Pod()
container = client.V1Container(name = "mypod", volume_mounts = volume_mounts, args = ["sleep", "3600"])
container.image = "busybox"
spec = client.V1PodSpec(containers=[container])
pod.metadata = client.V1ObjectMeta(name="mypod")


# ### Create volume required by secret

spec.volumes = [client.V1Volume(name="foo")]
spec.volumes[0].secret = client.V1SecretVolumeSource(secret_name="mysecret")


pod.spec = spec


# ### Create the Pod

api_instance.create_namespaced_pod(namespace="default",body=pod)


# ### View secret being used within the pod

#Wait until pod is running before executing this section.
while True:
    resp = api_instance.read_namespaced_pod(name="mypod",
                                   namespace='default')
    if resp.status.phase != 'Pending':
        break
    time.sleep(1)

user = stream(api_instance.connect_get_namespaced_pod_exec, name="mypod", namespace="default",
              command=[ "/bin/sh", "-c", "cat /srv/secret/username" ],
              stderr=True, stdin=False, stdout=True, tty=False)
print(user)
passwd = stream(api_instance.connect_get_namespaced_pod_exec, name="mypod", namespace="default",
                command=[ "/bin/sh", "-c", "cat /srv/secret/password" ],
                stderr=True, stdin=False, stdout=True, tty=False)
print(passwd)


# ### Delete Pod

api_instance.delete_namespaced_pod(name="mypod", namespace="default", body=client.V1DeleteOptions())


# ### Delete Secret

api_instance.delete_namespaced_secret(name="mysecret", namespace="default", body=sec)

