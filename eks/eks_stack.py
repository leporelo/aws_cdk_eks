from aws_cdk import (
    core, 
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam
    )
from .eks_services import EksServices


class EksStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, 
        my_service_details={}, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.my_service_details = my_service_details

        masters_role = iam.Role(
            self, "clusterAdmin",
            role_name="demo_EKS_cluster_role",
            assumed_by=iam.AccountRootPrincipal()
        )

        k8s_cluster = eks.Cluster(
            self, "defaultCluster", 
            cluster_name="DemoEKS",
            version=eks.KubernetesVersion.V1_19,
            default_capacity=1,
            default_capacity_type=eks.DefaultCapacityType.EC2,
            default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL),
            masters_role=masters_role
            )
        k8s_cluster.add_fargate_profile(
            "FargateEnabled", selectors=[
                eks.Selector(
                    namespace="eksdemo", 
                    labels={"fargate":"enabled"})
            ]
        )

        my_service = EksServices(self, "myService", eks_cluster=k8s_cluster, service=self.my_service_details)