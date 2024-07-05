from kubernetes import client, config
from kubernetes.client import V1PersistentVolumeClaim, V1PersistentVolumeClaimSpec, V1ResourceRequirements, V1PersistentVolumeClaimVolumeSource
from kubernetes.client import V1Deployment, V1DeploymentSpec, V1PodTemplateSpec, V1PodSpec, V1Container, V1VolumeMount, V1Volume, V1ObjectMeta, V1LabelSelector

# Configure API key authorization: BearerToken
config_file_path = '/etc/rancher/k3s/k3s.yaml'
try:
    config.load_kube_config(config_file=config_file_path)
except UnicodeDecodeError as e:
    print(f"Error reading kube config file {config_file_path}: {e}")
    raise



def create_configmap(namespace, configmap_name, data):
    configmap = client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        metadata=client.V1ObjectMeta(name=configmap_name),
        data=data
    )

    v1 = client.CoreV1Api()
    try:
        v1.create_namespaced_config_map(namespace=namespace, body=configmap)
        return f"ConfigMap '{configmap_name}' created."
    except ApiException as e:
        if e.status == 409:  # Conflict, meaning the ConfigMap already exists
            v1.replace_namespaced_config_map(name=configmap_name, namespace=namespace, body=configmap)
            return f"ConfigMap '{configmap_name}' replaced."
        return f"Exception when creating configmap: {e}"




if __name__ == "__main__":
    namespace = "default"
    configmap_name = "monitor-config"
    data = {"sleep_time": "10"}
    print(create_configmap(namespace, configmap_name, data))
