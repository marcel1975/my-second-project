from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    Tags,
    aws_ec2 as _ec2,
)
from constructs import Construct


class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_config = self.node.try_get_context('envs')['prod']
 
        self.vpc = _ec2.Vpc(
            self,
            "customVpcId",
            ip_addresses=_ec2.IpAddresses.cidr(prod_config['vpc_configs']['vpc_cidr']),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="public", cidr_mask=24, subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="app", cidr_mask=24, subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                _ec2.SubnetConfiguration(
                    name="db", cidr_mask=24, subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
                )
            ]
        )

        CfnOutput(self,
                       "customVpcOutput",
                       value=self.vpc.vpc_id,
                       export_name="VpcId")