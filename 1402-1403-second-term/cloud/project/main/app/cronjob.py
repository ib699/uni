import subprocess
from kubernetes import client, config
from kubernetes.client.rest import ApiException

config_file_path = '/root/cloud/cronjob/k3s.yaml'
try:
    config.load_kube_config(config_file=config_file_path)
except UnicodeDecodeError as e:
    print(f"Error reading kube config file {config_file_path}: {e}")
    raise

# Function to create Persistent Volume (PV) and Persistent Volume Claim (PVC)
def create_pv_pvc(namespace, pv_name, pvc_name, storage_size, host_path):
    # PV definition
    pv = {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {
            "name": pv_name
        },
        "spec": {
            "capacity": {
                "storage": storage_size
            },
            "accessModes": [
                "ReadWriteMany"
            ],
            "hostPath": {
                "path": host_path
            }
        }
    }

    # PVC definition
    pvc = {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {
            "name": pvc_name
        },
        "spec": {
            "accessModes": [
                "ReadWriteMany"
            ],
            "resources": {
                "requests": {
                    "storage": storage_size
                }
            }
        }
    }

    # Create PV and PVC
    try:
        v1 = client.CoreV1Api()
        pv_response = v1.create_persistent_volume(body=pv)
        pvc_response = v1.create_namespaced_persistent_volume_claim(namespace=namespace, body=pvc)
        print(f"Created PV '{pv_name}' and PVC '{pvc_name}' successfully.")
    except ApiException as e:
        print(f"Exception when creating PV or PVC: {e}")

# Function to create Pod
def create_pod(namespace, pod_name, python_script_path, pvc_name):
    # Pod definition
    pod = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": pod_name
        },
        "spec": {
            "containers": [{
                "name": "python-container",
                "image": "python:3.9",
                "command": ["python3", python_script_path],
                "volumeMounts": [{
                    "name": "python-storage",
                    "mountPath": "/mnt/data"
                }]
            }],
            "volumes": [{
                "name": "python-storage",
                "persistentVolumeClaim": {
                    "claimName": pvc_name
                }
            }]
        }
    }

    # Create Pod
    try:
        v1 = client.CoreV1Api()
        pod_response = v1.create_namespaced_pod(namespace=namespace, body=pod)
        print(f"Created Pod '{pod_name}' successfully.")
    except ApiException as e:
        print(f"Exception when creating Pod: {e}")

# Main function
def main():
    # Define namespace and paths
    namespace = "default"
    pv_name = "python-pv"
    pvc_name = "python-pvc"
    storage_size = "1Gi"
    host_path = "/mnt/data"
    pod_name = "python-pod"
    python_script_path = "/root/cloud/cronjob/main.py"

    # Change directory to where the script and requirements are located
    try:
        subprocess.check_call(["cd", "/root/cloud/cronjob"])
    except subprocess.CalledProcessError as e:
        print(f"Error changing directory: {e}")
        return

    # Install dependencies from requirements.txt
    try:
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return

    # Create PV and PVC
    create_pv_pvc(namespace, pv_name, pvc_name, storage_size, host_path)

    # Create Pod
    create_pod(namespace, pod_name, python_script_path, pvc_name)

if __name__ == "__main__":
    main()
