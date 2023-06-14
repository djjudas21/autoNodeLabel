"""
Collect CPU info and add it as node labels
"""

import os
import argparse
import time
from cpumodel.cpumodel import get_cpu_model
from kubernetes import client, config

def list_nodes(api_instance):
    """
    Retrieve a list of all nodes in the cluster as a simple array
    """
    node_list = api_instance.list_node()
    temp_list=[]

    json_data=client.ApiClient().sanitize_for_serialization(node_list)
    if len(json_data["items"]) != 0:
        for node in json_data["items"]:
            temp_list.append(node["metadata"]["name"])

    return temp_list

def main():
    """
    Collect CPU info and add it as node labels
    """

    # Read in args
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dry-run',
                        help="don't actually label anything", action='store_true')
    parser.add_argument('-v', '--verbose',
                        help="enable verbose output", action='store_true')
    parser.add_argument('-s', '--sleep',
                        help="sleep forever after labelling", action='store_true')
    parser.add_argument('-p', '--prefix',
                        help="prefix for node labels", default='autonodelabel.io', type=str)
    args = parser.parse_args()

    # Connect to Kubernetes cluster
    config.load_kube_config()
    api_instance = client.CoreV1Api()

    # Get generic CPU attributes from cpumodel
    labels = get_cpu_model()

    # Generate fully qualified labels
    prefixedlabels = {}
    for key, value in labels.items():
        prefixedlabels[f"{args.prefix}/{key}"] = value
        if args.verbose is True:
            print(f"{args.prefix}/{key}: {value}")

    # Deduce hostname from env var
    node = os.getenv('NODE_NAME') or 'localhost'

    # Get list of nodes from Kubernetes API
    nodes = list_nodes(api_instance)

    if node in nodes:
        print("Labelling node")

        # Generate API object
        body = {
            "metadata": {
                "labels": prefixedlabels
            }
        }

        # Label node
        if args.dry_run is not True:
            api_response = api_instance.patch_node(node, body)

        # Sleep forever to allow running as a DaemonSet since there is currently
        # no provision in Kubernetes for jobs that run on every node
        if args.sleep:
            while True:
                time.sleep(3600)

    else:
        print(f"The determined node name {node} was not in the list of Kubernetes node names")

if __name__ == '__main__':
    main()
