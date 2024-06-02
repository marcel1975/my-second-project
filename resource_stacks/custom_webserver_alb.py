from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_iam as _iam,
    aws_autoscaling as _autoscaling,
    aws_ec2 as _ec2,
    aws_iam as _iam,
    aws_elasticloadbalancingv2 as _elbv2
)
from constructs import Construct

class CustomWebserverAlbStack(Stack):
    
        def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
            super().__init__(scope, construct_id, **kwargs)
    
            # Read bootstrap script:
            try:
                with open("bootstrap_scripts/install_httpd.sh", mode="r") as file:
                    user_data = file.read()
            except OSError:
                print("Unable to read user data script")
            
            linux_ami = _ec2.MachineImage.latest_amazon_linux2(
                edition=_ec2.AmazonLinuxEdition.STANDARD,
                virtualization=_ec2.AmazonLinuxVirt.HVM,
                storage=_ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                
            )

            alb = _elbv2.ApplicationLoadBalancer(
                self,
                "myAlbId",
                vpc=vpc,
                internet_facing=True,
                load_balancer_name="WebServerALB"
            )

            # Allow ALB to recive traffic from any IP address on port 80
            alb.connections.allow_from_any_ipv4(
                _ec2.Port.tcp(80),
                description="Allow inbound HTTP traffic on port 80"
            )

            # Add Listener to ALB
            listener = alb.add_listener(
                "ListenerId",
                port=80,
                open=True
            )

            # Adding websrver iam role
            web_server_role = _iam.Role(
                self,
                "webServerRoleId",
                assumed_by=_iam.ServicePrincipal("ec2.amazonaws.com"),
                managed_policies=[
                    _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                    _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
                ]
            )

            # Creating AutoScaling Group with ec2 instances
            webserver_asg = _autoscaling.AutoScalingGroup(
                self,
                "webServerAsgId",
                vpc=vpc,
                vpc_subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED),
                instance_type=_ec2.InstanceType.of(
                    _ec2.InstanceClass.BURSTABLE2,
                    _ec2.InstanceSize.MICRO
                ),
                machine_image=linux_ami,
                min_capacity=2,
                max_capacity=3,
                role=web_server_role,
                user_data=_ec2.UserData.custom(user_data)
            )

            # Allow ASG Security Group to access ALB
            webserver_asg.connections.allow_from(alb,
                                                 _ec2.Port.tcp(80),
                description="Allow Webserver to access ALB on port 80"
            )

            # Adding ASG instances to ALB target group
            listener.add_targets(
                "webServerTargetId",
                port=80,
                targets=[webserver_asg]
            )

            # Output of ALB DNS name
            output_alb_1 = CfnOutput(
                self,
                "myAlbOutput",
                description="DNS Name of the ALB",
                value=f"http://{alb.load_balancer_dns_name}"
            )
                 
