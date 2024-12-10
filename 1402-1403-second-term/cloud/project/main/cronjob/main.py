import time
from kubernetes import client, config
from kubernetes.client.models import (
    V1ObjectMeta, V1Service, V1PodSpec, V1Container, V1EnvVar, V1ServiceSpec,
    V1ServicePort, V1LabelSelector, V1ContainerPort, V1PersistentVolumeClaim, 
    V1PersistentVolumeClaimSpec, V1ResourceRequirements, V1VolumeMount, 
    V1PodTemplateSpec, V1StatefulSetSpec, V1StatefulSet
)
from kubernetes.client.rest import ApiException
import psycopg2
from psycopg2 import sql
import os

# Configure API key authorization: BearerToken
config_file_path = '/etc/rancher/k3s/k3s.yaml'
try:
    config.load_kube_config(config_file=config_file_path)
except UnicodeDecodeError as e:
    print(f"Error reading kube config file {config_file_path}: {e}")
    raise

def get_pod_ip(namespace, pod_name):
    core_v1_api = client.CoreV1Api()
    pod = core_v1_api.read_namespaced_pod(name=pod_name, namespace=namespace)
    return pod.status.pod_ip

def create_table_in_master():
    master_ip = get_pod_ip("default", "postgresql-0")
    conn = psycopg2.connect(
        dbname="my_database",
        user="user",
        password="password",
        host=master_ip,
        port=5432
    )
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS my_table (
        id SERIAL PRIMARY KEY,
        pod_name VARCHAR(100),
        app_name VARCHAR(100),
        failure_count INTEGER,
        success_count INTEGER,
        last_failure VARCHAR(30),
        last_success VARCHAR(30),
        created_at VARCHAR(30)
    );
    CREATE UNIQUE INDEX IF NOT EXISTS idx_my_table_pod_name ON my_table(pod_name);
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

def write_to_master(pod_name, app_name, failure_count, success_count, last_failure, last_success, created_at):
    # Connect to the master pod
    master_ip = get_pod_ip("default", "postgresql-0")
    conn = psycopg2.connect(
        dbname="my_database",
        user="user",
        password="password",
        host=master_ip,
        port=5432
    )
    cursor = conn.cursor()
    upsert_query = """
    INSERT INTO my_table (pod_name, app_name, failure_count, success_count, last_failure, last_success, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (pod_name)
    DO UPDATE SET
        app_name = EXCLUDED.app_name,
        failure_count = EXCLUDED.failure_count,
        success_count = EXCLUDED.success_count,
        last_failure = EXCLUDED.last_failure,
        last_success = EXCLUDED.last_success,
        created_at = EXCLUDED.created_at;
    """
    cursor.execute(upsert_query, (pod_name, app_name, failure_count, success_count, last_failure, last_success, created_at))
    conn.commit()
    cursor.close()
    conn.close()

def get_sleep_time_from_configmap(namespace, configmap_name):
    core_v1_api = client.CoreV1Api()
    try:
        config_map = core_v1_api.read_namespaced_config_map(name=configmap_name, namespace=namespace)
        return int(config_map.data.get("sleep_time", "5"))
    except ApiException as e:
        print(f"Exception when reading ConfigMap: {e}")
        return 5  # Default sleep time

def monitor_pods():
    namespace = "default"
    configmap_name = "monitor-config"
    core_v1_api = client.CoreV1Api()
    
    while True:
        sleep_time = get_sleep_time_from_configmap(namespace, configmap_name)
        
        try:
            pods = core_v1_api.list_namespaced_pod(namespace=namespace, label_selector="monitor=true")
            for pod in pods.items:
                pod_name = pod.metadata.name
                pod_status = pod.status.phase
                
                # Ensure the metadata and status are not None
                labels = pod.metadata.labels if pod.metadata.labels else {}
                annotations = pod.metadata.annotations if pod.metadata.annotations else {}
                container_statuses = pod.status.container_statuses if pod.status.container_statuses else []
                
                app_name = labels.get("app", "N/A")
                created_at = pod.metadata.creation_timestamp

                # Initialize failure_count, success_count, last_failure, and last_success
                failure_count = 0
                success_count = 0
                last_failure = "N/A"
                last_success = "N/A"

                # Determine failure count, last failure, and last success from container statuses
                for container_status in container_statuses:
                    if container_status.restart_count:
                        failure_count += container_status.restart_count
                    if container_status.state.terminated:
                        if container_status.state.terminated.reason == "Completed":
                            last_success = container_status.state.terminated.finished_at
                            success_count += 1
                        elif container_status.state.terminated.reason in ["Error", "Failed"]:
                            last_failure = container_status.state.terminated.finished_at
                            failure_count += 1
                    elif container_status.state.running:
                        last_success = created_at.strftime("%Y-%m-%d %H:%M:%S")  # Use created_at time
                        success_count += 1
                    elif container_status.state.waiting and container_status.state.waiting.reason in ["CrashLoopBackOff", "ErrImagePull", "ImagePullBackOff", "CreateContainerConfigError"]:
                        last_failure = "Currently Failing"
                        failure_count += 1

                # Print the collected data
                print(f"Pod Name: {pod_name}")
                print(f"Status: {pod_status}")
                print(f"App Name: {app_name}")
                print(f"Failure Count: {failure_count}")
                print(f"Success Count: {success_count}")
                print(f"Last Failure: {last_failure}")
                print(f"Last Success: {last_success}")
                print(f"Created At: {created_at}")
                print("----------")
                write_to_master(pod_name, app_name, failure_count, success_count, last_failure, last_success, created_at)

        except Exception as e:
            print(f"Error monitoring pods: {e}")
        
        time.sleep(sleep_time)

if __name__ == "__main__":
    # create_table_in_master()
    os.system("sudo apt install pip; pip install psycopg2 kubernetes --break-system-packages")
    monitor_pods()
