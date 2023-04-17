import os
import subprocess
import sys
import zipfile

def get_all_namespaces():
    namespaces = []
    result = subprocess.run(["kubectl", "get", "namespaces", "-o", "jsonpath='{.items[*].metadata.name}'"], capture_output=True, text=True)
    if result.returncode == 0:
        namespaces = result.stdout.strip("'").split(" ")
    else:
        print("Error: Unable to get namespaces.")
    return namespaces

def get_all_pods(namespace):
    pods = []
    result = subprocess.run(["kubectl", "get", "pods", "-n", namespace, "-o", "jsonpath='{.items[*].metadata.name}'"], capture_output=True, text=True)
    if result.returncode == 0:
        pods = result.stdout.strip("'").split(" ")
    else:
        print(f"Error: Unable to get pods in namespace {namespace}.")
    return pods

def save_pod_logs(namespace, pod):
    log_file = f"{namespace}-{pod}.log"
    result = subprocess.run(["kubectl", "logs", "-n", namespace, pod], capture_output=True, text=True)
    if result.returncode == 0:
        with open(log_file, "w") as file:
            file.write(result.stdout)
        print(f"Saved logs for pod {pod} in namespace {namespace} to {log_file}.")
        return log_file
    else:
        print(f"Error: Unable to get logs for pod {pod} in namespace {namespace}.")
        return None

def compress_logs(log_files, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for log_file in log_files:
            zipf.write(log_file)
            os.remove(log_file)
    print(f"Compressed logs saved to {zip_path}.")

def main():
    target_namespace = None
    output_directory = None
    log_files = []

    if len(sys.argv) > 1:
        target_namespace = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_directory = sys.argv[2]
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

    if target_namespace:
        pods = get_all_pods(target_namespace)
        for pod in pods:
            log_file = save_pod_logs(target_namespace, pod)
            if log_file:
                log_files.append(log_file)
    else:
        namespaces = get_all_namespaces()
        for namespace in namespaces:
            pods = get_all_pods(namespace)
            for pod in pods:
                log_file = save_pod_logs(namespace, pod)
                if log_file:
                    log_files.append(log_file)

    if log_files:
        zip_name = "collected_logs.zip"
        zip_path = os.path.join(output_directory, zip_name) if output_directory else zip_name
        compress_logs(log_files, zip_path)

if __name__ == "__main__":
    main()
