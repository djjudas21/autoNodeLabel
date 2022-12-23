# autonodelabel

Interrogate nodes and add various properties of the system as node labels

By default, only the following hardware labels are provided:

```yaml
apiVersion: v1
kind: Node
metadata:
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/fluentd-ds-ready: "true"
    beta.kubernetes.io/os: linux
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: kube07
    kubernetes.io/os: linux
    microk8s.io/cluster: "true"
```
