Webinar-01
==========

Introduction
------------
When getting started with AWS (and when get started with a new service), I found that the following approach worked well for me. Hopefully, it will work well for you.

- Deploy using the console
- Deploy using awscli
- Deploy from a scripting language (e.g. Python)

During this webinar we will be primarily using the AWS console, but I have also provided equivalent awscli commands for each operation.


Notes
-----
In the awscli commands provided below

- For parameters where the value is **static**, the specific **value** for this webinar is included.
- For parameters where the value is **dynamic**, and must be discovered, **<parameter>** is included.

****

What we are building
--------------------

.. image:: ./images/webinar_net-01.png

***

Amazon Virtual Private Cloud (VPC)
----------------------------------
VPCs are logically isolated sections of the AWS cloud.

- VPCs have the look and feel of traditional networks

	+ You can define the IPv4/IPv6 address space
	+ You can create subnets
	+ YOu can configure routing tables 

toDoList
~~~~~~~~

- Create a VPC named **webinar-01** with a CIDR of **10.2.0.0/16**. 

****

*goingCmdO*
~~~~~~~~~~~

awscli::

    $ aws ec2 create-vpc --cidr-block 10.2.0.0/16 --tag-specifications ResourceType=vpc,Tags=[{Key=Name,Value=webinar-01}]

|

The above awscli command will return the configuration of the newly created VPC. The output will include the **vpcId**, which will be required for future operations. Here's one way to return just the **vpcId**, as text, from the awscli.

awscli::
	
	$ aws ec2 describe-vpcs --filters Name=tag:Name,Values=webinar-01 --query Vpcs[].VpcId --output text

****

****

Internet Gateway
-----------------
Create an Internet Gateway

awscli::

	aws ec2 create-internet-gateway --tag-specifications ResourceType=internet-gateway,Tags=[{Key=Name,Value=webinar-01-igw}]

Attach the Internet Gateway to the VPC

awscli (windows)::

	aws ec2 attach-internet-gateway --internet-gateway-id <igw-id> --vpc-id <vpc-id>

****

Route Tables
------------
Add a name (webinar-01-private) to the main route table

awscli (windows)::

	aws ec2 create-tags --resources <route-table-id> ^
	--tags Key=Name,Value=webinar-01-private

Create a second route table named (webinar-01-public) 

awscli (windows)::

	aws ec2 create-route-table --vpc-id <vpc-id> ^
	--tag-specifications ResourceType=route-table,Tags=[{Key=Name,Value=webinar-01-public}]

****



Routes
------
Addes routes

awscli (windows)::

	aws ec2 create-route --destination-cidr-block 0.0.0.0/0 ^
	--gateway-id <igw-id> --route-table-id <rtb-id>

****

Subnets
-------

Create subnets

awscli (windows)::

	aws ec2 create-subnet --cidr-block 10.2.130.0/23 ^
	--vpc-id <vpc-id> --availability-zone us-east-1b ^
	--tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-private02}]

****

Associate Subnets with Route Table
----------------------------------

awscli (windows)::

	aws ec2 associate-route-table --route-table-id <value>--subnet-id <value>

****

VPC peering link
----------------
Create a VPC peering link

awscli (windows)::

	aws ec2 create-vpc-peering-connection --peer-vpc-id <value> --vpc-id <value> ^
	--tag-specifications ResourceType=vpc-peering-connection,Tags=[{Key=Name,Value=webinar-01-peerlink}]

Accept the peering link

awscli (windows)::

	aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id <value>

Add routes to the peer-link

awscli (windows)::

	aws ec2 create-route --destination-cidr-block 10.0.0.0/16 ^
	--gateway-id <value> --route-table-id <value>

awscli (windows)::

	aws ec2 create-route --destination-cidr-block 10.0.0.0/16 ^
	--gateway-id <value> --route-table-id <value>

awscli (windows)::

	aws ec2 create-route --destination-cidr-block 10.2.0.0/16 ^
	--gateway-id <value> --route-table-id <value>







