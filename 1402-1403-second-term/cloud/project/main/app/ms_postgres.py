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

def create_statefulset():
    labels = {"app": "postgresql"}
    selector = V1LabelSelector(match_labels=labels)

    container = V1Container(
        name="postgresql",
        image="bitnami/postgresql:latest",
        ports=[V1ContainerPort(container_port=5432)],
        env=[
            V1EnvVar(name="POSTGRESQL_REPLICATION_MODE", value="master"),
            V1EnvVar(name="POSTGRESQL_REPLICATION_USER", value="repl_user"),
            V1EnvVar(name="POSTGRESQL_REPLICATION_PASSWORD", value="repl_password"),
            V1EnvVar(name="POSTGRESQL_USERNAME", value="user"),
            V1EnvVar(name="POSTGRESQL_PASSWORD", value="password"),
            V1EnvVar(name="POSTGRESQL_DATABASE", value="my_database"),
        ],
        volume_mounts=[
            V1VolumeMount(
                name="postgresql-data",
                mount_path="/bitnami/postgresql"
            )
        ]
    )

    volume_claim_template = V1PersistentVolumeClaim(
        metadata=V1ObjectMeta(name="postgresql-data"),
        spec=V1PersistentVolumeClaimSpec(
            access_modes=["ReadWriteOnce"],
            resources=V1ResourceRequirements(
                requests={"storage": "1Gi"}
            )
        )
    )

    pod_template = V1PodTemplateSpec(
        metadata=V1ObjectMeta(labels=labels),
        spec=V1PodSpec(containers=[container])
    )

    stateful_set_spec = V1StatefulSetSpec(
        replicas=2,
        selector=selector,
        service_name="postgresql",
        template=pod_template,
        volume_claim_templates=[volume_claim_template]
    )

    stateful_set = V1StatefulSet(
        api_version="apps/v1",
        kind="StatefulSet",
        metadata=V1ObjectMeta(name="postgresql"),
        spec=stateful_set_spec
    )

    return stateful_set

def create_service():
    service = V1Service(
        api_version="v1",
        kind="Service",
        metadata=V1ObjectMeta(name="postgresql"),
        spec=V1ServiceSpec(
            ports=[V1ServicePort(port=5432, target_port=5432)],
            selector={"app": "postgresql"}
        )
    )
    return service


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

def main():
    api_instance = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()

    # Create the Service
    service = create_service()
    core_v1_api.create_namespaced_service(
        namespace="default",
        body=service
    )

    # Create the StatefulSet
    stateful_set = create_statefulset()
    api_instance.create_namespaced_stateful_set(
        namespace="default",
        body=stateful_set
    )

    # Create the table in the master
    # create_table_in_master()

def write_to_master():
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
    cursor.execute("INSERT INTO my_table (app_name, failure_count, success_count, last_failure, last_success) VALUES (%s, %s, %s, %s, %s)",
                   ('app1', 0, 1, None, '2024-07-02 10:00:00'))
    conn.commit()
    cursor.close()
    conn.close()
    
def read_from_slave():
    # Connect to the slave pod
    slave_ip = get_pod_ip("default", "postgresql-0")
    conn = psycopg2.connect(
        dbname="my_database",
        user="user",
        password="password",
        host=slave_ip,
        port=5432
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # main()
    # Example usage:
    create_table_in_master()
    # write_to_master()
    read_from_slave()