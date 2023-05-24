import boto3


def publish_message_to_sns(message: str, topic_arn: str):
    sns_client = boto3.client("sns")

    message_id = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )

    return message_id
