from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    Tags,
    aws_ec2 as _ec2
)
from constructs import Construct

class CustomEc2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #default_vpc = _ec2.Vpc.from_lookup(self, "importedVPC", vpc_id="vpc-39784f52")
        # Creation of custom VPC
        vpc = _ec2.Vpc(
            self,
            "customVpcId",
            #cidr="10.0.0.0/24",
            ip_addresses=_ec2.IpAddresses.cidr(self.node.try_get_context('envs')['prod']['vpc_configs']['vpc_cidr']),
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="public", subnet_type=_ec2.SubnetType.PUBLIC
                )
            ]
        )


        # Read bootstrap script
        with open("bootstrap_scripts/install_httpd.sh", mode="r") as file:
            user_data = file.read()

        # Webserver001 instance
        web_server = _ec2.Instance(
            self,
            "webServerId",
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="webServer001",
            machine_image=_ec2.MachineImage.generic_linux(
                {"eu-central-1": "ami-0f673487d7e5f89ca"}
            ),
            vpc=vpc,
            vpc_subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PUBLIC),
            user_data=_ec2.UserData.custom(user_data)
        )

        # output of IP address

        output1 = CfnOutput(
            self,
            "webServerOutput",
            description="Public IP Address of the Web Server",
            value=f"http://{web_server.instance_public_ip}"
        )

        # allow incomming traffic to WebServer001

        web_server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
            description="Allow inbound HTTP traffic on port 80"
        )