from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_)
from aws_cdk import aws_cloudwatch as cloudwatch

class OrderApiStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 Bucket
        orders_bucket = s3.Bucket(self, 'OrderBucket888')

        # Create a Lambda function to fetch orders from S3
        orders_lambda = lambda_.Function(self, 'OrdersLambda',
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler='lambda.lambda_handler',
            code=lambda_.Code.from_asset('lambda'), 
            environment={
                "BUCKET_NAME": orders_bucket.bucket_name
            }
        )

        # Create an API Gateway
        api = apigateway.RestApi(self, "OrdersApi")

        # Create an API resource and method to retrieve orders
        orders_resource = api.root.add_resource("orders")
        get_orders_integration = apigateway.LambdaIntegration(orders_lambda)
        orders_resource.add_method("GET", get_orders_integration)

        # CloudWatch alarm for empty order responses
        empty_orders_metric = orders_lambda.metric(
            metric_name="EmptyOrders",
            statistic="Sum")

        alarm = cloudwatch.Alarm(self, "EmptyOrdersAlarm",
            metric=empty_orders_metric,
            threshold=5,
            evaluation_periods=1,
            datapoints_to_alarm=1)