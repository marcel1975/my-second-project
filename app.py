#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from resource_stacks.custom_vpc import CustomVpcStack
from resource_stacks.custom_ec2 import CustomEc2Stack
from resource_stacks.custom_ec2_with_profile import CustomEc2WithProfileStack
from resource_stacks.custom_ec2_with_latest_ami import CustomEc2LatestAmiStack
from resource_stacks.custom_ec2_with_ebs_piops import CustomEc2PiopsStack
from resource_stacks.custom_webserver_alb import CustomWebserverAlbStack
from resource_stacks.custom_vpc import CustomVpcStack
from resource_stacks.vpc_stack import VpcStack
from resource_stacks.custom_parameters_ssm_secret import CustomParametersSsmSecretStack

from aws_cdk import Environment
from aws_cdk import Tags

app = cdk.App()

# Custom VPC stack
# vpc_stack = VpcStack(app, "custom-vpc-stack",
#                env=Environment(account=app.node.get_context('envs')['prod']['account'],
#                                region=app.node.get_context('envs')['prod']['region']
#                               )
#               )

# Custom Ec2 stack
# CustomEc2Stack(app, "custom-ec2-stack",
#                env=Environment(account=app.node.get_context('envs')['prod']['account'],
#                                region=app.node.get_context('envs')['prod']['region']
#                               )
#               )

# Custom Ec2 stack with profile

# CustomEc2WithProfileStack(app, "custom-ec2-stack-with-profile",
#                           env=Environment(account=app.node.get_context('envs')['prod']['account'],
#                                           region=app.node.get_context('envs')['prod']['region']
#                                          )
#                          )


# CustomEc2LatestAmiStack(app, "custom-ec2-stack-with-latest-ami",
#                           env=Environment(account=app.node.get_context('envs')['prod']['account'],
#                                           region=app.node.get_context('envs')['prod']['region']
#                                           #region="eu-north-1"
#                                          )
#                          )

# env= Environment(account="003639982821", region="eu-central-1"


# CustomWebserverAlbStack(app, "custom-webserver-alb-stack", vpc = vpc_stack.vpc,
#                          env=Environment(account=app.node.get_context('envs')['prod']['account'],
#                                          region=app.node.get_context('envs')['prod']['region']
#                                         )
#                         )

# Tags.of(app).add("email", app.node.try_get_context('envs')['prod']['email'])

CustomParametersSsmSecretStack(app, "custom-parameters-ssm-secret-stack",
                               env=Environment(account=app.node.get_context('envs')['prod']['account'],
                                               region=app.node.get_context('envs')['prod']['region']
                                              )
)
app.synth()