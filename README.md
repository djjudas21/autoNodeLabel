# autonodelabel

Interrogate Kubernetes nodes and add various properties of the hardware as node labels, to help with scheduling in mixed hardware clusters.

By default, only the following hardware labels are provided on MicroK8s:

```yaml
apiVersion: v1
kind: Node
metadata:
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/os: linux
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: kube07
    kubernetes.io/os: linux
    microk8s.io/cluster: "true"
```

The only CPU-specific information about the node we can access is the architecture. The number of CPU cores and
amount of memory can only be used implicitly by setting `resources` on pods.

This project queries the CPU, generates some labels, and adds them to nodes, that can be used in nodeSelectors.

## Examples

Example labels generated on some CPUs I have access to

### Raspberry Pi 4 Model B

```yaml
autonodelabel.io/cpuVendor: ARM
autonodelabel.io/cpuString: Cortex-A72
```

### Intel Core i5-6300U

```yaml
autonodelabel.io/cpuVendor: Intel
autonodelabel.io/cpuString: "Intel-Core i5-6300U"
autonodelabel.io/cpuModel: "Core-i5-6300U"
autonodelabel.io/cpuFamily: "Core-i5"
autonodelabel.io/cpuGeneration: "6"
autonodelabel.io/cpuLetter: U
```

### AMD Ryzen 7 5700G

```yaml
autonodelabel.io/cpuVendor: AMD
autonodelabel.io/cpuString: "AMD-Ryzen-7-5700G"
autonodelabel.io/cpuModel: "Ryzen-7-5700G"
autonodelabel.io/cpuFamily: "Ryzen-7"
autonodelabel.io/cpuGeneration: "5"
autonodelabel.io/cpuLetter: G
```

## Node selectors

Once your nodes are labelled, you can target workloads at specific pods by using
[nodeSelectors](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/).

For example, if you have a cluster made from two types of nodes, some with a Core i3 CPU and some
with a Core i5, you could use the following nodeSelector to ensure your pod only runs on the more
powerful nodes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test
spec:
  nodeSelector:
    autonodelabel.io/cpuFamily: "Core-i5"
```

## Docker image

There is a Docker image published as [djjudas21/autonodelabel](https://hub.docker.com/r/djjudas21/autonodelabel).
This image is built with `-v` for verbose output and `-s` for sleep forever, so it can be used as Kubernetes DaemonSet.
