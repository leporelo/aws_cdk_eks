from aws_cdk import (
    core, 
    aws_eks as eks, 
    aws_ec2 as ec2 )

class EksServices(core.Construct):

    def __init__(self, scope: core.Construct, id: str, eks_cluster, service, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.eks_cluster = eks_cluster
        self.service = service

        def my_demo_service(self, service):
            labels = service['labels']

            deployment = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": service['service_name'],
                    "namespace": service['namespace']
                },
                "spec": {
                    "replicas": service['replicas'],
                    "selector": {"matchLabels": labels},
                    "template": {
                        "metadata": {"labels": labels},
                        "spec": {
                            "containers": [{
                                "name": service['service_name'],
                                "image": service['image'],
                                "ports": [{"containerPort": service['port'], "protocol": "TCP"}]
                            }],
                        }
                    }
                }
            }

            service = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": service['service_name'], 
                    "namespace": service['namespace']
                    },
                "spec": {
                    "type": "LoadBalancer",
                    "ports": [{"port": 80, "targetPort": service['port']}],
                    "selector": service['labels']
                }
            }

            namespace = {
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": {
                    "name": "eksdemo",
                    "labels": {
                        "name": "eksdemo"
                    }
                }
            }

            return deployment, service, namespace

        deployment_manifest, service_manifest, namespace_manifest = my_demo_service(self, self.service)

        eks.KubernetesManifest(self, "MySampleService-", cluster=self.eks_cluster, manifest=[namespace_manifest, deployment_manifest, service_manifest])