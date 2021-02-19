Webinar-01
==========

VPC
---
Using the AWS Console, create a VPC named **webinar-01** with a CIDR of **10.2.0.0/16**. 

awscli (windows)::

    $ aws ec2 create-vpc --cidr-block 10.2.0.0/16 ^
    --tag-specifications ResourceType=vpc,Tags=[{Key=Name,Value=webinar-01}]

****


Route Table
-----------
aws ec2 create-tags --resources <route-table-id> --tags Key=Name,Value=webinar-01-private

aws ec2 create-route-table --vpc-id <vpc-id> --tag-specifications ResourceType=route-table,Tags=[{Key=Name,Value=webinar-01-public}]
 

IGW
---
aws ec2 create-internet-gateway --tag-specifications ResourceType=internet-gateway,Tags=[{Key=Name,Value=webinar-01-igw}]

aws ec2 attach-internet-gateway --internet-gateway-id <igw-id> --vpc-id <vpc-id>


Add Route
---------
aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --gateway-id <igw-id> --route-table-id <rtb-id>


Create Subnets
--------------
aws ec2 create-subnet --cidr-block 10.2.130.0/23 --vpc-id <vpc-id> --availability-zone us-east-1b --tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-private02}]


Associate Subnets with Route Table
----------------------------------
aws ec2 associate-route-table --route-table-id <value>--subnet-id <value>


Create a Peering Link
---------------------
aws ec2 create-vpc-peering-connection --peer-vpc-id <value> --vpc-id <value> --tag-specifications ResourceType=vpc-peering-connection,Tags=[{Key=Name,Value=webinar-01-peerlink}]

aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id <value>


Add routes for peering link
---------------------------
aws ec2 create-route --destination-cidr-block 10.0.0.0/16 --gateway-id <value> --route-table-id <value>

aws ec2 create-route --destination-cidr-block 10.0.0.0/16 --gateway-id <value> --route-table-id <value>

aws ec2 create-route --destination-cidr-block 10.2.0.0/16 --gateway-id <value> --route-table-id <value>







aws ec2 describe-vpcs --filters Name=tag:Name,Values=webinar-01