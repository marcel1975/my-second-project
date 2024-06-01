from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    aws_s3 as _s3,
    aws_kms as _kms
    # aws_sqs as sqs,
)
from constructs import Construct

class MyArtifactBucketStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, is_prod=False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(self.node.try_get_context('prod')['kms_arn'])

        mykey = _kms.Key.from_key_arn(self,
                                      "myKeyId",
                                      self.node.try_get_context('prod')['kms_arn']
        )

        if is_prod:
            artifactBucket = _s3.Bucket(
                self,
                "myProdArtifactBucketId",
                versioned=True,
                encryption_key=mykey,
                encryption=_s3.BucketEncryption.KMS,
                removal_policy=RemovalPolicy.RETAIN
            )
        else:
            artifactBucket = _s3.Bucket(
                self,
                "myDevArtifactBucketId",
                removal_policy=RemovalPolicy.DESTROY
            )
