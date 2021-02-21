import simplejson as json
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError


class Ec2Resource(object):

    def __init__(self):
        self.ec2 = boto3.resource('ec2')


    def create_instances(self, subnets, count):
        return