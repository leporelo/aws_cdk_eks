#!/usr/bin/env python3

from aws_cdk import core

from eks.eks_stack import EksStack

my_service_details = {
    "namespace": "eksdemo",
    "labels": {
        "app": "eks-demo-nginx",
        "fargate": "enabled"
    },
    "service_name": "eks-demo-nginx",
    "replicas": 2,
    "image": "nginx:latest",
    "port": 80
}

app = core.App()
EksStack(app, "eks", my_service_details=my_service_details)

app.synth()
