# autonodelabel

Interrogate nodes and add various properties of the system as node labels

By default, only the following hardware labels are provided:

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

This project queries the CPU and generates some labels that can be used in nodeSelectors.

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
autonodelabel.io/cpuString: Intel Core i5-6300U
autonodelabel.io/cpuModel: i5-6300U
autonodelabel.io/cpuFamily: i5
autonodelabel.io/cpuGeneration: 6
autonodelabel.io/cpuLetter: U
```

### AMD Ryzen 7 5700G

```yaml
autonodelabel.io/cpuVendor: AMD
autonodelabel.io/cpuString: AMD Ryzen 7 5700G
autonodelabel.io/cpuModel: Ryzen 7 5700G
autonodelabel.io/cpuFamily: Ryzen 7
autonodelabel.io/cpuGeneration: 5
autonodelabel.io/cpuLetter: G
```
