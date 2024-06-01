from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_docdb as _docdb,
    aws_ec2 as _ec2,
    aws_iam as _iam
)
from constructs import Construct

class CustomEc2LatestAmiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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

        # Get the latest Windows Server ami
        windows_ami = _ec2.MachineImage.latest_windows(
            version=_ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE
        )

        # Get the latest Amazon linux ami
        # amazon_linux_ami = _ec2.MachineImage.latest_amazon_linux2(
        #     edition=_ec2.AmazonLinuxEdition.STANDARD,
        #     virtualization=_ec2.AmazonLinuxVirt.HVM,
        #     storage=_ec2.AmazonLinuxStorage.EBS
        # )

        amazon_linux_ami = _ec2.MachineImage.latest_amazon_linux2(
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            virtualization=_ec2.AmazonLinuxVirt.HVM,
            storage=_ec2.AmazonLinuxStorage.EBS 
        )

        # Webserver001 instance
        web_server = _ec2.Instance(
            self,
            "webServerId",
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="webServer001",
            # machine_image=_ec2.MachineImage.generic_linux(
            #      {"eu-central-1": "ami-0f673487d7e5f89ca"}
            # ),
            machine_image=amazon_linux_ami,
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

        # Add permissions to the web server instance profile

        web_server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore")
        )
        web_server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess")
        )


        