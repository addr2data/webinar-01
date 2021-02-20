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
~~~~~
In the awscli commands provided below

- For parameters where the value is **static**, the specific **value** for this webinar is included.
- For parameters where the value is **dynamic**, and must be discovered, **<parameter>** is included.

|

****

****

Let's build this
----------------

|

.. image:: ./images/webinar_net-01.png

|

****

****

Amazon Virtual Private Cloud (VPC)
----------------------------------
VPCs are logically isolated sections of the AWS cloud.

- VPCs have the look and feel of traditional networks

	+ You can define the IPv4/IPv6 address space
	+ You can create subnets
	+ YOu can configure routing tables 

*Note: there are no charges associated with VPCs*

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

|

****

****

Internet Gateway
-----------------
A VPC component that allows communication between your VPC and the Internet. It is highly-available and scalable.

- Provides a target for Internet routable traffic in your VPC route tables (i.e. default route)
- Performs Network Address Translation (NAT) for IPv4
- Supports both IPv4 and IPv6

*Note: there are no charges associated with Internet Gateways*

toDoList
~~~~~~~~

- Create an Internet Gateway named **webinar-01-igw**.
- Attach it to our VPC

****

*goingCmdO*
~~~~~~~~~~~

awscli::

	aws ec2 create-internet-gateway --tag-specifications ResourceType=internet-gateway,Tags=[{Key=Name,Value=webinar-01-igw}]

|

The above awscli command will return the configuration of the newly created Internet Gateway. The output will include the
**InternetGatewayId**, which will be required for future operations. Here's one way to return just the **InternetGatewayId**,
as text, from the awscli.

awscli::
	
	$ aws ec2 describe-internet-gateways --filters Name=tag:Name,Values=webinar-01-igw --query InternetGateways[].InternetGatewayId --output text

|

awscli::

	aws ec2 attach-internet-gateway --internet-gateway-id <igw-id> --vpc-id <vpc-id>

|

****

****

Route Tables and Routes
-----------------------
A VPC component that contains a set of routes. These routes determine where network traffic is directed within your VPC.

- A route table that automatically comes with your VPC. It is called the **main** route table.
- You can create your own **custom** route tables.
- Subnets are associated with route tables, either explicitly or implicitly.
- Any subnet not explicitly associated with a **custom** route table, is implicitly associated with the **main** route table 

*Note: there are no charges associated with route tables or routes*

toDoList
~~~~~~~~

- Review the **main** route table.
- Name main route table **webinar-01-rt-private**.
- Create a **custom** route table named **webinar-01-rt-public** .
- Add a **default route** to the **webinar-01-rt-public** route table.

****

*goingCmdO*
~~~~~~~~~~~

First, let's examine the main route table.

awscli::

	aws ec2 describe-route-tables --filters "Name=vpc-id,Values=<vpc-id>"

|

The above awscli command will return the configuration of the automatically created Route Table. The output will include the
**RouteTableId**, which will be required for future operations. Here's one way to return just the **RouteTableId**,
as text, from the awscli.


awscli::

	aws ec2 describe-route-tables --filters "Name=vpc-id,Values=<vpc-id>" --query RouteTables[].RouteTableId --output text

|

Next, we are going name the main route table **webinar-01-rt-private**.

awscli::

	aws ec2 create-tags --resources <route-table-id> --tags Key=Name,Value=webinar-01-rt-private

|

Next, we are going create a custom route table named **webinar-01-rt-public**

awscli::

	aws ec2 create-route-table --vpc-id <vpc-id> --tag-specifications ResourceType=route-table,Tags=[{Key=Name,Value=webinar-01-rt-public}]

|

Finally, we are going to add a default route to the **webinar-01-rt-public** route table.

awscli::

	aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --gateway-id <igw-id> --route-table-id <rtb-id>

|

****

****

Subnets
-------
Subnets are

*Note: there are no charges associated with subnets*

toDoList
~~~~~~~~

- Create a subnet in availability zone **us-east-1a** named **webinar-01-sub-private-01**, using cidr **10.2.128.0/23**
- Create a subnet in availability zone **us-east-1a** named **webinar-01-sub-public-01**, using cidr **10.2.0.0/23**
- Create a subnet in availability zone **us-east-1b** named **webinar-01-sub-private-02**, using cidr **10.2.130.0/23**
- Create a subnet in availability zone **us-east-1b** named **webinar-01-sub-public-02**, using cidr **10.2.2.0/23**
- Review the subnets just created.
- Review the association in the **public** route table

****

*goingCmdO*
~~~~~~~~~~~

First, let's create some subnets

awscli::

	aws ec2 create-subnet --cidr-block 10.2.128.0/23 --vpc-id <vpcId> --availability-zone us-east-1a --tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-sub-private-01}]

	aws ec2 create-subnet --cidr-block 10.2.0.0/23 --vpc-id <vpcId> --availability-zone us-east-1a --tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-sub-public-01}]

	aws ec2 create-subnet --cidr-block 10.2.130.0/23 --vpc-id <vpcId> --availability-zone us-east-1a --tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-sub-private-02}]

	aws ec2 create-subnet --cidr-block 10.2.2.0/23 --vpc-id <vpcId> --availability-zone us-east-1a --tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-sub-public-02}]

|

Next, let's review the subnet configuration.

awscli::

	aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc-id>"

|

Next, let's show the **Name** and **SubnetId** of the subnets we created in a table.

awscli::

	aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpcId>" --query "Subnets[*].{name: Tags[?Key=='Name'] | [0].Value, Id: SubnetId}" --output table --color off

	-----------------------------------------------------------
	|                     DescribeSubnets                     |
	+---------------------------+-----------------------------+
	|            Id             |            name             |
	+---------------------------+-----------------------------+
	|  subnet-06d45e8022909b538 |  webinar-01-sub-private-01  |
	|  subnet-0a89f3ebc7a958154 |  webinar-01-sub-public-02   |
	|  subnet-057041e32aad58f18 |  webinar-01-sub-private-02  |
	|  subnet-085968550caaec8d7 |  webinar-01-sub-public-01   |
	+---------------------------+-----------------------------+

|

Next, let's associate the two *public* subnets with the *public* route table 

awscli::

	aws ec2 associate-route-table --route-table-id <RouteTableId>--subnet-id <SubnetId>

|

Finally, let's review the associations in the *public* route table.

awscli::

	aws ec2 describe-route-tables --filters "Name=vpc-id,Values=vpc-0728135c72ee58885"

|

****

****

VPC Peering
-----------
VPC peering allows you to create a network connection (VPC peering connection) between two VPCs and route IPv4/IPv6 traffic between them.

- VPC peering connection can be created within the AWS account or between AWS accounts.
- VPCs can be in the same or different regions.

toDoList
~~~~~~~~

- Create a VPC peering connection between **webinar-01** (requester) and **addr2data** VPCs (acceptor).
- Accept the VPC peering connection
- Add a route to the **private** routing table in the **webinar-01** VPC.
- Add a route to the **public** routing table in the **webinar-01** VPC.
- Add a route to the **public** routing table in the **addr2data** VPC.

****

*goingCmdO*
~~~~~~~~~~~

First, let's create a VPC peering connection between **webinar-01** (requester) and **addr2data** (acceptor)

::

	aws ec2 create-vpc-peering-connection --peer-vpc-id <vpcId> --vpc-id <vpcId> --tag-specifications ResourceType=vpc-peering-connection,Tags=[{Key=Name,Value=webinar-01-peerlink}]

|

Then, let's accept the VPC peering connection

::

	aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id <VpcPeeringConnectionId>

|

Then, let's add a route to the **private** route table in the **webinar-01** VPC

::

	aws ec2 create-route --destination-cidr-block 10.0.0.0/16 --gateway-id <VpcPeeringConnectionId> --route-table-id <RouteTableId>

|

Then, let's add a route to the **public** route table in the **webinar-01** VPC

::

	aws ec2 create-route --destination-cidr-block 10.0.0.0/16 --gateway-id <VpcPeeringConnectionId> --route-table-id <RouteTableId>

|

Then, let's add a route to the **public** route table in the **addr2data-01** VPC.

::

	aws ec2 create-route --destination-cidr-block 10.2.0.0/16 --gateway-id <VpcPeeringConnectionId> --route-table-id <RouteTableId>

|

****

****

Security Groups
---------------
We will 


toDoList
~~~~~~~~

- Create a security group named **web-servers**
- Discuss **outbound** vs. **inbound** rules
- Add the following rules to the **web-servers** security group:

	+ *type* = **SSH**, *protocol* = **TCP**, *port* = **22**, *source* = **10.0.0.0/16**, *description* = **SSH from addr2data VPC**
	+ *type* = **Custom**, *protocol* = **TCP**, *port* = **5000**, *source* = **10.0.0.0/16**, *description* = **HTTP from addr2data VPC**

****

*goingCmdO*
~~~~~~~~~~~

First, let's deploy two instances

::





Testing local connectivity
--------------------------
We will 


toDoList
~~~~~~~~

- Deploy an instance named **web-public**, using the **base_webserver** AMI, selecting **webinar-01-sub-public-01** for the subnet.

****

*goingCmdO*
~~~~~~~~~~~

First, let's deploy two instances

::