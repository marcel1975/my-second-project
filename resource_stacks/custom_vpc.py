from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    Tags,
    aws_ec2 as _ec2,
    aws_s3 as _s3
)
from constructs import Construct

class CustomVpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_config = self.node.try_get_context('envs')['prod']

        custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            #cidr=prod_config['vpc_configs']['vpc_cidr'],
            ip_addresses=_ec2.IpAddresses.cidr(prod_config['vpc_configs']['vpc_cidr']),
            max_azs=3,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicSubnet",
                    subnet_type=_ec2.SubnetType.PUBLIC,
                    cidr_mask=prod_config['vpc_configs']['cidr_mask']
                ),
                _ec2.SubnetConfiguration(
                    name="privateSubnet",
                    subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=prod_config['vpc_configs']['cidr_mask']
                ),
                _ec2.SubnetConfiguration(
                    name="dbSubnet",
                    subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=prod_config['vpc_configs']['cidr_mask']
                )
            ]
        )

        Tags.of(custom_vpc).add("Owner", "MarcinWalkowski")

        CfnOutput(self,
                  "customVpcOutput",
                  value=custom_vpc.vpc_id,
                  export_name="customVpcId"
                  )

        bkt = _s3.Bucket(
            self,
            "myBucketId"
        )

        Tags.of(bkt).add("Owner", "MarcinWalkowski")

        # Importing an existing bucket 
        bkt1 = _s3.Bucket.from_bucket_name(
            self,
            "myImportedBucket",
            "myawsbucket-20240421"
        )

        CfnOutput(
            self,
            "myImportedBucketOutput",
            value=bkt1.bucket_name
        )

        # Importing an default VPC !!!!!!
        vpc_default = _ec2.Vpc.from_lookup(
            self,
            "myImportedVpc",
            vpc_id="vpc-39784f52"
        )

        CfnOutput(
            self,
            "myImportedVpcOutput",
            value=vpc_default.vpc_id
        )

        # Creating VPC Peering Connection
        vpc_peering = _ec2.CfnVPCPeeringConnection(
            self,
            "myVpcPeering",
            vpc_id=vpc_default.vpc_id,
            peer_vpc_id=custom_vpc.vpc_id
        )


