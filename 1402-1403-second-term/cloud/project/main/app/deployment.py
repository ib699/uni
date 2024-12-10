#!/usr/bin/env python

from kubernetes import client, config
from kubernetes.client.models import (
    V1ObjectMeta, V1Secret, V1Service, V1Deployment, V1PodSpec, V1Container, V1EnvVar,
    V1Ingress, V1IngressSpec, V1IngressRule, V1HTTPIngressPath, V1HTTPIngressRuleValue, V1IngressBackend, V1ServiceSpec,
    V1ServicePort, V1DeploymentSpec, V1TypedLocalObjectReference, V1ServiceBackendPort, V1IngressServiceBackend, V1LabelSelector
)
from kubernetes.client import V1CrossVersionObjectReference, V1HorizontalPodAutoscaler, V1HorizontalPodAutoscalerSpec
from kubernetes.client.rest import ApiException
import secrets
import string
import base64
import json

# Configure API key authorization: BearerToken
config_file_path = '/etc/rancher/k3s/k3s.yaml'
try:
    config.load_kube_config(config_file=config_file_path)
except UnicodeDecodeError as e:
    print(f"Error reading kube config file {config_file_path}: {e}")
    raise

# Create API instances
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
networking_v1 = client.NetworkingV1Api()

namespace = "default"

def create_hpa(namespace, app_name, min_replicas, max_replicas, target_cpu_utilization_percentage):
    # Define the target for scaling (the deployment)
    scale_target = V1CrossVersionObjectReference(
        api_version="apps/v1",
        kind="Deployment",
        name=app_name
    )
    
    # Define the HPA spec
    hpa_spec = V1HorizontalPodAutoscalerSpec(
        scale_target_ref=scale_target,
        min_replicas=min_replicas,
        max_replicas=max_replicas,
        target_cpu_utilization_percentage=target_cpu_utilization_percentage
    )
    
    # Define the HPA resource
    hpa = V1HorizontalPodAutoscaler(
        api_version="autoscaling/v1",
        kind="HorizontalPodAutoscaler",
        metadata=V1ObjectMeta(name=app_name),
        spec=hpa_spec
    )
    
    try:
        # Create the HPA in the specified namespace
        autoscaling_v1 = client.AutoscalingV1Api()
        autoscaling_v1.create_namespaced_horizontal_pod_autoscaler(namespace=namespace, body=hpa)
        print(f"HorizontalPodAutoscaler for '{app_name}' created.")
    except ApiException as e:
        print(f"Exception when creating HorizontalPodAutoscaler: {e}")


def create_secret(namespace, secrets):
    for secret_name, secret_value in secrets.items():
        try:
            config.load_kube_config(config_file=config_file_path)
        except UnicodeDecodeError as e:
            print(f"Error reading kube config file {config_file_path}: {e}")
            raise

        v1 = client.CoreV1Api()

        # Base64 encode secret values
        try:
            encoded_data = {secret_name: base64.b64encode(secret_value.encode()).decode('utf-8')}
        except UnicodeEncodeError as e:
            print(f"Error encoding secret value for key {secret_name}: {e}")
            raise

        secret = client.V1Secret(
            api_version="v1",
            kind="Secret",
            metadata=client.V1ObjectMeta(name=secret_name),
            data=encoded_data
        )

        try:
            v1.create_namespaced_secret(namespace=namespace, body=secret)
            print(f"Secret '{secret_name}' created.")
        except ApiException as e:
            print(f"Exception when creating secret: {e}")

def create_service(namespace, name, app_name, port):
    metadata = V1ObjectMeta(name=name, namespace=namespace, labels={"app": app_name})
    spec = V1ServiceSpec(
        selector={"app": app_name},
        ports=[V1ServicePort(port=port, target_port=port)]
    )
    service = V1Service(metadata=metadata, spec=spec)
    v1.create_namespaced_service(namespace=namespace, body=service)

def create_deployment(namespace, app_name, replicas, image_address, image_tag, port, resources, envs, secrets):
    env_vars = [V1EnvVar(name=k, value=v) for k, v in envs.items()]
    secret_volumes = []
    secret_volume_mounts = []

    if secrets:
        for secret_name in secrets.keys():
            secret_volumes.append({
                "name": secret_name,
                "secret": {"secretName": secret_name}
            })
            secret_volume_mounts.append({
                "name": secret_name,
                "mountPath": f"/etc/secrets/{secret_name}"
            })

    container = V1Container(
        name=app_name,
        image=f"{image_address}:{image_tag}",
        ports=[client.V1ContainerPort(container_port=port)],
        env=env_vars,
        resources=resources,
        volume_mounts=secret_volume_mounts
    )

    spec = V1PodSpec(containers=[container], volumes=secret_volumes)
    template = client.V1PodTemplateSpec(
        metadata=V1ObjectMeta(labels={"app": app_name, "monitor": "true"}),
        spec=spec
    )

    spec = V1DeploymentSpec(
        replicas=replicas,
        template=template,
        selector=V1LabelSelector(match_labels={"app": app_name, "monitor": "true"})
    )

    deployment = V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=V1ObjectMeta(name=app_name),
        spec=spec
    )

    apps_v1.create_namespaced_deployment(namespace=namespace, body=deployment)

def create_ingress(namespace, app_name, domain_address, service_name, service_port):
    ingress_backend = V1IngressBackend(
        service=V1IngressServiceBackend(
            name=service_name,
            port=V1ServiceBackendPort(number=service_port)
        )
    )

    http_ingress_path = V1HTTPIngressPath(
        path="/",
        path_type="Prefix",
        backend=ingress_backend
    )

    http_ingress_rule_value = V1HTTPIngressRuleValue(
        paths=[http_ingress_path]
    )

    ingress_rule = V1IngressRule(
        host=domain_address,
        http=http_ingress_rule_value
    )

    ingress_spec = V1IngressSpec(rules=[ingress_rule])

    ingress = V1Ingress(
        metadata=V1ObjectMeta(name=app_name, namespace=namespace),
        spec=ingress_spec
    )

    networking_v1.create_namespaced_ingress(namespace=namespace, body=ingress)

def create(data):
    namespace = "default"  # or any other namespace

    if data["secrets"]:
        create_secret(namespace, data["secrets"])

    create_service(namespace, data["app_name"], data["app_name"], data["service_port"])

    create_deployment(namespace, data["app_name"], data["replicas"], data["image_address"], data["image_tag"], data["service_port"], data["resources"], data["envs"], data["secrets"])

    if data["external_access"]:
        create_ingress(namespace, data["app_name"], data["domain_address"], data["app_name"], data["service_port"])
    
    create_hpa(namespace, data["app_name"], data["min_replicas"], data["max_replicas"], data["target_cpu_utilization_percentage"])


def verify_json_keys(data):
    required_keys = ['app_name', 'replicas', 'image_address', 'image_tag', 'domain_address', 'service_port',
                     'resources', 'envs', 'secrets', 'external_access']
    for key in required_keys:
        if key not in data:
            return False, f'Missing required key: {key}'

    return True

def get_deployment_info(deployment_name):
    namespace = "default"  # or any other namespace
    try:
        # Get the deployment
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)

        # Get deployment details
        replicas = deployment.spec.replicas
        ready_replicas = deployment.status.ready_replicas or 0

        deployment_info = {
            "DeploymentName": deployment.metadata.name,
            "Replicas": replicas,
            "ReadyReplicas": ready_replicas,
            "PodStatuses": []
        }

        # Get pods for the deployment
        selector = deployment.spec.selector.match_labels
        label_selector = ",".join([f"{k}={v}" for k, v in selector.items()])
        pods = v1.list_namespaced_pod(namespace, label_selector=label_selector)

        for pod in pods.items:
            pod_info = {
                "Name": pod.metadata.name,
                "Phase": pod.status.phase,
                "HostIP": pod.status.host_ip,
                "PodIP": pod.status.pod_ip,
                "StartTime": pod.status.start_time.strftime("%Y-%m-%d %H:%M:%S") if pod.status.start_time else "N/A"
            }
            deployment_info["PodStatuses"].append(pod_info)

        return json.dumps(deployment_info, indent=2)

    except ApiException as e:
        return json.dumps({"error": str(e)})

def get_all_deployments():
    try:
        # Get all deployments in the specified namespace
        deployments = apps_v1.list_namespaced_deployment("default")
        all_deployment_info = []

        for deployment in deployments.items:
            deployment_info = get_deployment_info(deployment.metadata.name)
            all_deployment_info.append(json.loads(deployment_info))

        return json.dumps(all_deployment_info, indent=2)

    except ApiException as e:
        return {"error": f"Exception when listing deployments: {e}"}

def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_postgres_secret(namespace, secret_name):
    try:
        # Generate random values for username, password, and database name
        username = generate_random_string(8)
        password = generate_random_string(12)
        dbname = generate_random_string(10)

        # Encode data for Kubernetes secret
        encoded_data = {
            'username': base64.b64encode(username.encode()).decode('utf-8'),
            'password': base64.b64encode(password.encode()).decode('utf-8'),
            'dbname': base64.b64encode(dbname.encode()).decode('utf-8')
        }
    except Exception as e:
        return f"Error generating secret values for {secret_name}: {e}"

    secret = client.V1Secret(
        api_version="v1",
        kind="Secret",
        metadata=client.V1ObjectMeta(name=secret_name),
        data=encoded_data
    )

    try:
        v1.create_namespaced_secret(namespace=namespace, body=secret)
        return username, password, dbname
    except ApiException as e:
        return f"Exception when creating secret: {e}"

def create_configmap(namespace, configmap_name, data):
    configmap = client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        metadata=client.V1ObjectMeta(name=configmap_name),
        data=data
    )

    try:
        v1.create_namespaced_config_map(namespace=namespace, body=configmap)
        return f"ConfigMap '{configmap_name}' created."
    except ApiException as e:
        return f"Exception when creating configmap: {e}"

def create_postgresql_deployment(namespace, app_name, replicas, image, secret_name, resources, external):
    env_vars = {}

    # Create a Secret for PostgreSQL credentials
    secrets = {secret_name: f"{secret_name}-value"}
    env_vars['POSTGRES_USER'], env_vars['POSTGRES_PASSWORD'], env_vars['POSTGRES_DB'] = create_postgres_secret(namespace, secret_name)

    env_vars_list = [client.V1EnvVar(name=k, value=v) for k, v in env_vars.items()]

    # Define PostgreSQL deployment spec
    container = client.V1Container(
        name=app_name,
        image=image,
        env=env_vars_list,
        ports=[client.V1ContainerPort(container_port=5432)],
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": app_name}),
        spec=client.V1PodSpec(containers=[container])
    )

    spec = client.V1DeploymentSpec(
        replicas=replicas,
        selector=client.V1LabelSelector(match_labels={"app": app_name}),
        template=template
    )

    if external:
        container.ports.append(client.V1ContainerPort(container_port=5432, name="postgresql", protocol="TCP"))
        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=f"{app_name}-service"),
            spec=client.V1ServiceSpec(
                selector={"app": app_name},
                ports=[client.V1ServicePort(port=5432, target_port=5432)]
            )
        )

        try:
            v1.create_namespaced_service(namespace=namespace, body=service)
        except ApiException as e:
            return f"Exception when creating service: {e}"

    if resources:
        container.resources = client.V1ResourceRequirements(
            requests={"cpu": resources['cpu'], "memory": resources['memory']}
        )

    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=app_name),
        spec=spec
    )

    try:
        apps_v1.create_namespaced_deployment(namespace=namespace, body=deployment)
        return f"Deployment '{app_name}' created."
    except ApiException as e:
        return f"Exception when creating deployment: {e}"

def update_pod_monitor_label(namespace, pod_name, monitor_value):
    try:
        # Retrieve the current pod
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        if not pod.metadata.labels:
            pod.metadata.labels = {}
        
        # Update the monitor label
        pod.metadata.labels['monitor'] = monitor_value

        # Patch the pod with the updated labels
        v1.patch_namespaced_pod(name=pod_name, namespace=namespace, body=pod)
        print(f"Pod '{pod_name}' monitor label updated to '{monitor_value}'.")
    except ApiException as e:
        print(f"Exception when updating pod: {e}")

sample = {
    "app_name": "example-app",
    "replicas": 3,
    "image_address": "nginx",
    "image_tag": "latest",
    "domain_address": "local.example.com",
    "service_port": 80,
    "resources": {
        "limits": {"cpu": "500m", "memory": "512Mi"},
        "requests": {"cpu": "250m", "memory": "256Mi"}
    },
    "envs": {
        "ENVVAR1": "value1",
        "ENVVAR2": "value2"
    },
    "secrets": {
        "secret1": "valsecret1"
    },
    "external_access": True,
    "min_replicas": 2,
    "max_replicas": 10,
    "target_cpu_utilization_percentage": 50
}

# create(sample)

# get_all_deployments()

# deployment_name = "example-app"  # replace with your deployment name
# deployment_info_json = get_deployment_info(deployment_name)
# print(deployment_info_json)

# pod_name = "example-app-pod"  # replace with your pod name
# update_pod_monitor_label(namespace="default", pod_name=pod_name, monitor_value="false")

