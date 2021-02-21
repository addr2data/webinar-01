import simplejson as json
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from .errors import AwsHelperError


class Ec2Client(object):

    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.vpc_id = None

    def find_vpc(self, vpc_name):
        try:
            response = self.ec2.describe_vpcs()
            for vpc in response['Vpcs']:
                for tag in vpc['Tags']:
                    if vpc_name == tag['Value']:
                        self.vpc_id = vpc['VpcId']
            if not self.vpc_id:
                raise AwsHelperError("vpc not found")
        except ClientError as err:
            raise AwsHelperError(err)

    def find_subnet_ids(self, subnet_names):
        self.subnet_ids = []
        try:
            response = self.ec2.describe_subnets(
                Filters=[{'Name': 'vpc-id', 'Values': [self.vpc_id]}])
            for subnet in response['Subnets']:
                for tag in subnet['Tags']:
                    if tag['Value'] in subnet_names:
                        self.subnet_ids.append(subnet['SubnetId'])
            if not self.subnet_ids:
                raise AwsHelperError("no subnet ids found")
        except ClientError as err:
            raise AwsHelperError(err)

    def create_webserver_sg(self, sg_cfg):
        try:
            response = self.ec2.create_security_group(
                Description=sg_cfg['description'],
                GroupName=sg_cfg['name'],
                VpcId=self.vpc_id,
                TagSpecifications=sg_cfg['tags']
            )
            self.sg_id = response['GroupId']
        except ClientError as err:
            raise AwsHelperError(err)

        try:
            response = self.ec2.authorize_security_group_ingress(
                GroupId=self.sg_id,
                IpPermissions=sg_cfg['rules'])
        except ClientError as err:
            raise AwsHelperError(err)

    def run_instances(self, webserver_cfg):
        instances = []
        for subnet in self.subnet_ids:
            try:
                response = self.ec2.run_instances(
                    ImageId=webserver_cfg['ami'],
                    InstanceType=webserver_cfg['type'],
                    KeyName=webserver_cfg['keypair'],
                    MaxCount=webserver_cfg['count'],
                    MinCount=webserver_cfg['count'],
                    SecurityGroupIds=[self.sg_id],
                    SubnetId=subnet,
                    TagSpecifications=webserver_cfg['tags']
                )
                for instance in response['Instances']:
                    instances.append(instance['InstanceId'])
            except ClientError as err:
                raise AwsHelperError(err)
        return {'sgId': self.sg_id, 'instances': instances}

    # print(json.dumps(vpc, indent=4, sort_keys=False))

    def term_instances(self, instances):
        try:
            response = self.ec2.terminate_instances(InstanceIds=instances)
        except ClientError as err:
            raise AwsHelperError(err)

    def delete_security_group(self, sg):
        try:
            response = self.ec2.delete_security_group(GroupId=sg)
        except ClientError as err:
            raise AwsHelperError(err)
