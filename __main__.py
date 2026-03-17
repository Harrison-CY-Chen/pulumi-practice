import pulumi
import pulumi_aws as aws

pulumi_practice_lambda = aws.lambda_.Function("pulumi-practice-lambda",
    architectures=["arm64"],
    code=pulumi.AssetArchive({"index.py": pulumi.FileAsset("./index.py")}),
    ephemeral_storage={
        "size": 512,
    },
    handler="index.handler",
    logging_config={
        "log_format": "Text",
        "log_group": "/aws/lambda/pulumi-practice-lambda",
    },
    name="pulumi-practice-lambda",
    package_type="Zip",
    region="ap-northeast-1",
    role="arn:aws:iam::073903779593:role/service-role/pulumi-practice-lambda-role-5orqruan",
    runtime=aws.lambda_.Runtime.PYTHON3D10,
    tracing_config={
        "mode": "PassThrough",
    },
    opts = pulumi.ResourceOptions(protect=False))
