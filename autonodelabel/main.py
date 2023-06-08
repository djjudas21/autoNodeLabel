"""
Collect CPU info and add it as node labels
"""

import re
import os
from cpuinfo import get_cpu_info
from kubernetes import client, config

def map_vendor(vendor):
    """
    Rewrite vendor name
    """
    if vendor == 'GenuineIntel':
        returnval = 'Intel'
    elif vendor == 'AuthenticAMD':
        returnval = 'AMD'
    else:
        returnval = vendor
    return returnval

def clean_cpu_string(brand):
    """
    Rewrite CPU string more neatly.
    
    This:
        Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
    Becomes:
        Intel Core i5-6300U
    """
    # Strip annoying chars
    brand = brand.replace('(R)', '')
    brand = brand.replace('(TM)', '')
    brand = brand.replace('CPU', '')

    # Drop the '@ 2.40GHz' suffix
    brand = brand.split('@')[0]

    # Drop the 'with Radeon Graphics' suffix
    brand = brand.split('with')[0]
    brand = brand.strip()

    return brand

def parse_cpu(vendor, cpu):
    """
    Parse the CPU string to figure out some attributes
    """

    cpulabels = {}
    if vendor == 'Intel':
        # Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
        # Intel(R) Core(TM) i5-6500T CPU @ 2.50GHz
        # Intel(R) Core(TM) i5-4590T CPU @ 2.00GHz
        result = re.search(r"(i\d)-(\d)?\d{3}([A-Z])?", cpu)
        cpulabels['cpuModel'] = result.group(0)
        cpulabels['cpuFamily'] = result.group(1)
        cpulabels['cpuGeneration'] = result.group(2)
        cpulabels['cpuLetter'] = result.group(3)
    elif vendor == 'AMD':
        pass
        # AMD Ryzen 7 5700G with Radeon Graphics
        result = re.search(r"AMD ((\w+ \d) (\d)\d+([A-Z]?))", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
        cpulabels['cpuLetter'] = result.group(4)
    return cpulabels


def drop_nones_inplace(d: dict) -> dict:
    """Recursively drop Nones in dict d in-place and return original dict"""
    dd = drop_nones(d)
    d.clear()
    d.update(dd)
    return d


def drop_nones(d: dict) -> dict:
    """Recursively drop Nones in dict d and return a new dict"""
    dd = {}
    for k, v in d.items():
        if isinstance(v, dict):
            dd[k] = drop_nones(v)
        elif isinstance(v, (list, set, tuple)):
            # note: Nones in lists are not dropped
            # simply add "if vv is not None" at the end if required
            dd[k] = type(v)(drop_nones(vv) if isinstance(vv, dict) else vv
                            for vv in v)
        elif v is not None:
            dd[k] = v
    return dd


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

    # Connect to Kubernetes cluster
    config.load_kube_config()
    api_instance = client.CoreV1Api()

    # Fetch CPU info
    cpuinfo = get_cpu_info()

    # Generate basic labels
    labels = {}
    labels['cpuVendor'] = map_vendor(cpuinfo['vendor_id_raw'])
    labels['cpuString'] = clean_cpu_string(cpuinfo['brand_raw'])

    # Calculate some extra labels
    labels.update(parse_cpu(labels['cpuVendor'], labels['cpuString']))

    # Drop None elements
    labels = (drop_nones_inplace(labels))

    # Generate fully qualified labels
    prefix = 'autolabels.example.com'
    prefixedlabels = {}
    for key, value in labels.items():
        prefixedlabels[f"{prefix}/{key}"] = value
        print(f"{prefix}/{key}: {value}")

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
        api_response = api_instance.patch_node(node, body)

    else:
        print(f"The determined node name {node} was not in the list of Kubernetes node names")

if __name__ == '__main__':
    main()
