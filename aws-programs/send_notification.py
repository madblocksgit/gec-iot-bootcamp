import boto3

AWS_KEY=''
AWS_SECRET=''

sns=boto3.client("sns",
	region_name="us-east-1",
	aws_access_key_id=AWS_KEY,
	aws_secret_access_key=AWS_SECRET)


'''sns.publish(TopicArn="arn:aws:sns:us-east-1:496667932506:geciot",
	Message="Humidity Crossed",
	Subject="IoT Notification")'''

sns.publish(PhoneNumber="+917893015625",
	Message="Humidity Crossed")
