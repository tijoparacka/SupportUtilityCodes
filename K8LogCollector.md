# Kubernetes Log Collector

This Python script collects logs from all the pods in a specified namespace or all namespaces in a Kubernetes cluster and compresses them into a single zip file.

## Usage

```bash
python collect_logs.py [NAMESPACE] [OUTPUT_DIRECTORY]


Replace [NAMESPACE] with the desired namespace, or leave it empty to collect logs from all namespaces.
Replace [OUTPUT_DIRECTORY] with the desired output directory for the zipped file.


python collect_logs.py "" "/tmp/logs"
