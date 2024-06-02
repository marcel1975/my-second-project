from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    Tags,
    aws_ssm as _ssm,
    aws_secretsmanager as _secretsmanager
)
from constructs import Construct

import json

class CustomParametersSsmSecretStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # creation of AWS secrets and AWS parameeters
        parameter1 = _ssm.StringParameter(
            self,
            "parameter1",
            description="Load Testing configuration",
            parameter_name="NoOfConcurrentUsers",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD
        )

        parameter2 = _ssm.StringParameter(
            self,
            "parameter2",
            description="Load Testing configuration",
            parameter_name="/locust/configs/NoOfConcurrentUsers",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD
        )
        
        parameter3 = _ssm.StringParameter(
            self,
            "parameter3",
            description="Load Testing configuration",
            parameter_name="/locust/configs/DurationInSec",
            string_value="300",
            tier=_ssm.ParameterTier.STANDARD
        )

        secret1 = _secretsmanager.Secret(
            self,
            "secret1",
            description="Customer DB password",
            secret_name="customerDBpassword"
        )

        templatet_secret = _secretsmanager.Secret(
            self,
            "templateSecret",
            description="Templeted secret for user data",
            generate_secret_string=_secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "marcel"}),
                generate_string_key="password",
            )
        )
                                                  
                                                  

        output1 = CfnOutput(
            self,
            "output1",
            description="NoofConcurrentUsers",
            value=f"{parameter1.string_value}"
        )
 
        output2 = CfnOutput(
            self,
            "secrert1output",
            description="secret1",
            value=f"{secret1.secret_value}"
        )
