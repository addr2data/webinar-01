Webinar-01
==========

Objectives
----------

- **NO SLIDES** - content is publicly available on GitHub.

	+ This session is available at **https://github.com/addr2data/webinar-01**.

- Provide an opportunity to develop **hands-on-literacy** with AWS services, in three steps:

	+ **Introduce** - AWS services/components/concepts using the AWS console (**webinar**).

	+ **Do** - recreate what was built in the webinar using the awscli (**goingCmdO**).

	+ **Explore** - become familiar with using the AWS APIs directly (**code samples**)

- Introduce as many AWS services as possible over 4-5 webinars.

|

Introduction
------------
During this webinar we will introduce the following AWS services/components/concepts:

- Virtual Private Cloud (VPC)
- Internet Gateways
- Routing Tables and Routes
- Subnets
- VPC Peering
- Security Groups
- Deploying instances via the API
- NAT (Network Address Translation) Gateways
- Elastic IP Addresses
- Application Load Balancers (ALB)
- Network Load Balancers (NLB) 

|

**We are going to cover a lot of ground in this webinar, some details will be glossed over and advanced topics will be skipped altogether.**

	| If you want the nitty-gritty, then join the **AWS Certified Advanced Networking Study Group** (see details below)

|

AWS Certified Advanced Networking Study Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you are looking for the nitty-gritty, then maybe the **AWS Certified Advanced Networking Study Group** is for you.

- Private channel on the **API Users** team in Microsoft Teams.
- Meets every Thu (5:00p -6:00p ET) starting Mar 4, 2021.
- Sessions will be recorded, for those in different regions (i.e. EMEA, APJ).
- Once you join, active participation is required. Either, during the weekly sessions or through the teams channel. 
- If you are interested, reach out to me via email or chat on teams. 

|

Notes for awscli
~~~~~~~~~~~~~~~~

- For parameters where the value is **static**, the specific **value** for this webinar is included.
- For parameters where the value is **dynamic**, and must be discovered, **<parameter>** is included.

|

****

****


Let's build something
---------------------

|

.. image:: ./images/webinar_net-01.png

|

****

****

Virtual Private Cloud (VPC)
---------------------------

The basics
~~~~~~~~~~

- VPCs are the networking layer for EC2.

- They are logically isolated sections of the AWS cloud.

- VPCs have the look and feel of traditional networks

	+ You define the address space (IPv4/IPv6)
	+ You configure subnets
	+ You configure routing tables
	+ You configure network gateways
	+ You apply security

- VPCs are created per AWS Region

::

	What is an AWS Region?

	- A physical location where data centers are clustered.
	- Each AWS Region consists of multiple Availability Zones (AZ)
		- More on AZs when we get to Subnets
	- We will be working in the **us-east-1** Region
		- Located in Northern Virginia
		- Has six (6) AZs

|

- A VPC spans all AZs in a Region.

- When you create an account, a default VPC is created per region. This allows you to launch instances quickly without having to configure a VPC first.

- When you create a VPC, you must define an IPv4 CIDR block (/16 to /28).
	
	+ No matter what IPv4 CIDR block you use, Amazon treats these addresses as private.

- When you create a VPC, you can optionally define an IPv6 CIDR block (/56).
	
	+ This block can be Amazon or customer provided.

	+ Amazon treats these addresses as public.

- Once created, you can't change the initial IPv4 CIDR block, but you can add/remove other CIDR blocks.

- VPCs can operate in dual-stack mode. You instances can communicate using IPv4, IPv6 or both.

- When you create a VPC, you must select a value for **Tenancy**.

	+ **Default:** The tenancy of instances is determined at launch.

	+ **Dedicated:** The tenancy of all instances launched in this VPC is dedicated. 

Quotas
~~~~~~

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - VPC
     - 5 per region
   * - IPv4 CIDR blocks per VPC
     - 5
   * - IPv6 CIDR blocks per VPC
     - 1 ++

*++ Can't be increased*

Costs
~~~~~

- There are no charges directly associated with VPCs

toDoList
~~~~~~~~

- Create a VPC with the following parameters:

	+ Name-tag: **webinar-01**

	+ IPv4 CIDR block: **10.2.0.0/16**

	+ IPv4 CIDR block: **No IPv6 CIDR block**

	+ Tenancy: **Default** 

- Review the details of **webinar-01**

****

*goingCmdO*
~~~~~~~~~~~

Create a VPC

::

    aws ec2 create-vpc ^
    	--cidr-block 10.2.0.0/16 ^
    	--tag-specifications ResourceType=vpc,Tags=[{Key=Name,Value=webinar-01}]

|

The above awscli command will return the configuration of the newly created VPC. The output will include the **vpcId**, which will be required for future operations. Here's one way to return just the **vpcId**, as text, from the awscli.

::

	aws ec2 describe-vpcs ^
		--filters Name=tag:Name,Values=webinar-01 ^
		--query Vpcs[].VpcId --output text

|

****

****

Internet Gateway
-----------------

The basics
~~~~~~~~~~

- A VPC component that allows communication between your VPC and the Internet.

- Internet Gateways are highly-available and scalable.

- Provides a target for Internet routable traffic in your VPC route tables (i.e. default route)

- Supports both IPv4 and IPv6

- Performs Network Address Translation (NAT) for IPv4

- You can have one (1) Internet Gateway per VPC. 


Quotas
~~~~~~

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - Internet Gateways
     - 5 per region ++

*++ Directly associated with the 'VPCs per region' quota.*

Costs
~~~~~

- There are no charges directly associated with Internet Gateways


toDoList
~~~~~~~~

- Create an Internet Gateway named **webinar-01-igw**.
- Attach it to the **webinar-01** VPC

****

*goingCmdO*
~~~~~~~~~~~

Create an Internet Gateway

::

	aws ec2 create-internet-gateway ^
		--tag-specifications ResourceType=internet-gateway,Tags=[{Key=Name,Value=webinar-01-igw}]

|

The above awscli command will return the configuration of the newly created Internet Gateway. The output will include the
**InternetGatewayId**, which will be required for future operations. Here's one way to return just the **InternetGatewayId**,
as text, from the awscli.

::

	aws ec2 describe-internet-gateways ^
		--filters Name=tag:Name,Values=webinar-01-igw ^
		--query InternetGateways[].InternetGatewayId ^
		--output text

|

Attach the Internet Gateway to a VPC.

::

	aws ec2 attach-internet-gateway ^
		--internet-gateway-id <InternetGatewayId> ^
		--vpc-id <vpcId>

|

****

****

Route Tables and Routes
-----------------------

The basics
~~~~~~~~~~

- A VPC component that contains a set of routes that determine where network traffic is directed within your VPC.

- One (1) route table is automatically created when you create a VPC. By default, it's the  **main** route table.

- You can create your own route tables.

- Subnets are associated with route tables, either explicitly or implicitly.

- Any subnet not explicitly associated with a route table, is implicitly associated with the **main** route table.

- A route table defines the routing for any subnet associated with it. 

- You can change which route table is the **main** route table.

- IPv4 and IPv6 is handled separately.

- Each route has a **destination** and a **target**.

	+ The IPv4 default route associated with your *public* subnets, may look like this:

		+ Destination: **0.0.0.0/0**

		+ Target: **igw-xxxxxxxxxxxxxxxxx**

	+ Every route table has an IPv4 local route automatically added to it, for routing IPv4 traffic within a VPC:

		+ Destination: **10.2.0.0/16** (or whatever your VPC IPv4 CIDR block is)

		+ Target: **local**

	+ If you have enabled IPv6, then every route table will also have an IPv6 local route automatically added to it:

		+ Destination: **2600:1f18:a1c:b300::/56** (or whatever your VPC IPv6 CIDR block is)

		+ Target: **local**

- When a route table has multiple routes, the most specific route (longest prefix) that matches the traffic, determines how traffic is routed.

Quotas
~~~~~~

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - Route tables per VPC
     - 200
   * - Routes per route table (non-propagated routes)
     - 50
   * - BGP advertised routes per route table (propagated routes)
     - 100 ++

*++ Propagation is beyond the scope of this webinar.*

Costs
~~~~~

- There are no charges directly associated with Route Tables


toDoList
~~~~~~~~

- Review the **main** route table.

- Add a name-tag **webinar-01-rt-private** to the main route table .

- Create a second route table, using the name-tag **webinar-01-rt-public**.

- Add a **default route** to the **webinar-01-rt-public** route table.

****

*goingCmdO*
~~~~~~~~~~~

Examine the main route table.

::

	aws ec2 describe-route-tables ^
		--filters "Name=vpc-id,Values=<vpc-id>"

|

The above awscli command will return the configuration of the automatically created Route Table. The output will include the
**RouteTableId**, which will be required for future operations. Here's one way to return just the **RouteTableId**,
as text, from the awscli.

::

	aws ec2 describe-route-tables ^
		--filters "Name=vpc-id,Values=<vpc-id>" ^
		--query RouteTables[].RouteTableId ^
		--output text

|

Add a name-tag **webinar-01-rt-private** to the **main** route table .

::

	aws ec2 create-tags ^
		--resources <route-table-id> ^
		--tags Key=Name,Value=webinar-01-rt-private

|

Create a second route table, using the name-tag **webinar-01-rt-public**

::

	aws ec2 create-route-table ^
		--vpc-id <vpc-id> ^
		--tag-specifications ResourceType=route-table,Tags=[{Key=Name,Value=webinar-01-rt-public}]

|

Add a default route to the **webinar-01-rt-public** route table.

::

	aws ec2 create-route ^
		--destination-cidr-block 0.0.0.0/0 ^
		--gateway-id <igw-id> ^
		--route-table-id <rtb-id>

|

****

****

Subnets
-------

The basics
~~~~~~~~~~

- When you create a Subnet in a VPC:

	+ You must specify an AZ within the associated Region.

	+ You must specify a IPv4 CIDR block within the IPv4 CIDR block of the VPC.

	+ If the VPC has an IPv6 CIDR block defined, then you can optionally define an IPv6 CIDR block for the Subnet

::

	What is an AWS Availability Zone (AZ)?

	- An AZ consists of one or more data centers
	- These data centers have redundant power, networking and connectivity.
	- AZs are physically separated by many kilometers. 
	- Customers who operate applications across AZs are able to achieve higher levels of availability.
	- The two (2) AZs that we will use during this webinar are us-east-1a and us-east-1b

|

- Each Subnet has five (5) addresses reserved from its IPv4 CIDR block.

	+ For example, our Subnets will use IPv4 CIDR blocks with a prefix length of **/23**, which results in **512** possible IPv4 addresses, but only **507** IPv4 addresses available for Instances.

	+ The reserved addresses are as follows:

		+ base + 0: Network address

		+ base + 1: Reserved by AWS (VPC router)

		+ base + 2: Reserved by AWS (VPC base + 2 is DNS server, but base + 2 is also reserved in each subnet)

		+ base + 3: Reserved by AWS (future use)

		+ last: Broadcast address

- If traffic for a particular Subnet is routed to an Internet Gateway (based on the Route Table association), then it is considered to be a *public* subnet.

- For an Instance on a *public* subnet to communicate over the Internet with IPv4, it must have a *Public IPv4 address* or an *Elastic IP address*.

	+ More on *Public IPv4 addresses* and *Elastic IP addresses* later  

- Subnets have a setting called **Auto-assign IPv4**, which can be enabled/disabled. If this setting is enabled for a subnet:

	+ Instances launched in that Subnet will be assigned a *Public IPv4 address*, unless overridden during Instance launch. 

- For an Instance on a *public* subnet to communicate over the Internet with IPv6, it must have an IPv6 address.

- If traffic for a particular Subnet is not routed to an Internet Gateway (based on the Route Table association), then it is considered to be a *private* subnet.

Quotas
~~~~~~

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - Subnets per VPC
     - 200

Costs
~~~~~

- There are no charges directly associated with Subnets

toDoList
~~~~~~~~

- Create four (4) subnets using the following parameters:

.. list-table::
   :widths: 25, 25, 25
   :header-rows: 0

   * - **Name-tag**
     - **Availability Zone**
     - **IPv4 CIDR**
   * - `webinar-01-sub-private-01`
     - `us-east-1a`
     - `10.2.0.0/23`
   * - `webinar-01-sub-private-02`
     - `us-east-1b`
     - `10.2.2.0/23`
   * - `webinar-01-sub-public-01`
     - `us-east-1a`
     - `10.2.128.0/23`
   * - `webinar-01-sub-public-02`
     - `us-east-1b`
     - `10.2.130.0/23`

|

- Review the four (4) subnets that we just created.

- Associate **webinar-01-sub-public-01** and **webinar-01-sub-public-02** with **webinar-01-rt-public**

- Review the association in **webinar-01-rt-public**

****

*goingCmdO*
~~~~~~~~~~~

Create four (4) subnets

::

	aws ec2 create-subnet ^
		--cidr-block 10.2.0.0/23 ^
		--vpc-id <vpcId> ^
		--availability-zone us-east-1a ^
		--tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-sub-private-01}]

	aws ec2 create-subnet ^
		--cidr-block 10.2.2.0/23 ^
		--vpc-id <vpcId> ^
		--availability-zone us-east-1b ^
		--tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-sub-private-02}]

	aws ec2 create-subnet ^
		--cidr-block 10.2.128.0/23 ^
		--vpc-id <vpcId> ^
		--availability-zone us-east-1a ^
		--tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-sub-public-01}]

	aws ec2 create-subnet ^
		--cidr-block 10.2.130.0/23 ^
		--vpc-id <vpcId> ^
		--availability-zone us-east-1b ^
		--tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=webinar-01-sub-public-02}]

|

Review the the four (4) subnets created above.

::

	aws ec2 describe-subnets ^
		--filters "Name=vpc-id,Values=<vpc-id>"

|

Show the **Name** and **SubnetId** of the four (4) Subnets in a table.

::

	aws ec2 describe-subnets ^
		--filters "Name=vpc-id,Values=<vpcId>" ^
		--query "Subnets[*].{name: Tags[?Key=='Name'] | [0].Value, Id: SubnetId}" --output table --color off

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

Associate **webinar-01-sub-public-01** and **webinar-01-sub-public-02** with **webinar-01-rt-public**

::

	aws ec2 associate-route-table ^
		--route-table-id <RouteTableId> ^
		--subnet-id <SubnetId>

|

Review the associations in **webinar-01-rt-public**.

::

	aws ec2 describe-route-tables ^
		--filters "Name=vpc-id,Values=vpc-0728135c72ee58885"

|

****

****

VPC peering
-----------

The basics
~~~~~~~~~~

- VPC peering allows you to create a network connection (VPC peering connection) between two VPCs.

- Traffic can be routed between VPCs, using private IPv4 address or IPv6 addresses.

- A VPC peering connection can be created between:

	+ Two VPCs in the same AWS account

	+ Two VPCs in different AWS accounts

	+ Two VPCs in different Regions (aka inter-region VPC peering connection).


Quotas
~~~~~~

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - Active VPC peering connections per VPC
     - 50
   * - Outstanding VPC peering connection requests
     - 25
   * - Expiry time for an unaccepted VPC peering connection request
     - 168 hours (1 week)


Costs
~~~~~

- There are no charges directly associated with VPC peering.


toDoList
~~~~~~~~

- Create a VPC peering connection named **webinar-01-pcx** between **webinar-01** (requester) and **addr2data** VPCs (acceptor).

- Accept the VPC peering connection

- Add the following route to **webinar-01-rt-public**

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Destination**
     - **Target**
   * - `10.0.0.0/16`
     - `<VpcPeeringConnectionId>`

- Add the following route to **webinar-01-rt-private**

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Destination**
     - **Target**
   * - `10.0.0.0/16`
     - `<VpcPeeringConnectionId>`

- Add the following route to **addr2data-rt-public**

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Destination**
     - **Target**
   * - `10.2.0.0/16`
     - `<VpcPeeringConnectionId>`

****

*goingCmdO*
~~~~~~~~~~~

Create a VPC peering connection between **webinar-01** (requester) and **addr2data** (acceptor)

::

	aws ec2 create-vpc-peering-connection ^
		--peer-vpc-id <vpcId> ^
		--vpc-id <vpcId> ^
		--tag-specifications ResourceType=vpc-peering-connection,Tags=[{Key=Name,Value=webinar-01-peerlink}]

|

Accept the VPC peering connection

::

	aws ec2 accept-vpc-peering-connection ^
		--vpc-peering-connection-id <VpcPeeringConnectionId>

|

Add the following route to **webinar-01-rt-public**

::

	aws ec2 create-route ^
		--destination-cidr-block 10.0.0.0/16 ^
		--gateway-id <VpcPeeringConnectionId> ^
		--route-table-id <RouteTableId>

|

Add the following route to **webinar-01-rt-private**

::

	aws ec2 create-route ^
		--destination-cidr-block 10.0.0.0/16 ^
		--gateway-id <VpcPeeringConnectionId> ^
		--route-table-id <RouteTableId>

|

Add the following route to **addr2data-rt-public**

::

	aws ec2 create-route ^
		--destination-cidr-block 10.2.0.0/16 ^
		--gateway-id <VpcPeeringConnectionId> ^
		--route-table-id <RouteTableId>

|

****

****

Let's review where we are at
----------------------------

|

.. image:: ./images/webinar_net-02.png

|

Security Groups
---------------

The basics
~~~~~~~~~~

- Security Groups act as a virtual firewall for your EC2 instances.

	+ Inbound rules control the incoming traffic to your instance.

	+ Outbound rules control the outgoing traffic from your instance.

- When you launch an instance in a VPC, you specify one or more security groups from that VPC.

	+ If you don't, then the default security group.

- You can modify the rules in a Security Group at any time.

- New and modified rules are automatically applied to all instances that are associated with the security group.

Quotas
~~~~~~

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - VPC security groups per Region
     - 2500
   * - Inbound rules per security group
     - 60 (1,2,4)
   * - Outbound rules per security group
     - 60 (1,2,4)
   * - Security groups per network interface
     - 5 (1,3,4)

- *(1) This quota is enforced separately for IPv4 and IPv6*

- *(2) Referencing another security counts as one rule*

- *(3) The maximum is 16*

- *(4) The quota for security groups per network interface multiplied by the quota for rules per security group cannot exceed 1000*

Costs
~~~~~

- There are no charges directly associated with Security Groups

|

****

****

Instances
~~~~~~~~~

The basics
~~~~~~~~~~

- Reasonable coverage of EC2 Instances would require an entire webinar.

- Let it suffice to say that Instances are virtual machines.

Quotas
~~~~~~

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - Network interfaces per instance
     - Varies per Instance Type (1,2)
   * - Network interfaces per Region
     - 5000
   * - Outbound rules per security group
     - 60 (1, 2, 4)
   * - Security groups per network interface
     - 5 (1, 3, 4)

- *(1) For Instance Type t2.micro the limit is 2*

- *(2) For Instance Type t2.medium the limit is 3*


Getting started with the EC2 API
--------------------------------

The basics
~~~~~~~~~~
Now we are going to deploy some Instances and test connectivity. To do that we are going to use a Python script that communicates with EC API, using **boto3**.

Let's take a look at what arguments that Python script takes

.. image:: ./images/webserver_cmd-01.png

|

We are going to run the following command, but before we do let's examine that **cfg-private.yml** file.

::

	python webservers.py create cfg-private.yml


.. image:: ./images/cfg-private.png

|

Here is a summary of what that script using the *create* argument will do.

- It will create a security group named **webinar-01-sg-web-private**

- It will add an ingress rule to **webinar-01-sg-web-private** that allows **SSH** traffic from **10.0.0.0/16** and **10.2.0.0/16** 

- It will launch a single instance, using the following parameters:

	+ AMI: **base_webserver** (previously saved image - on boot, a simple web server starts on port 5000)
	
	+ Network: **webinar-01**
	
	+ Subnet: **webinar-01-sub-private-01**
	
	+ Security Groups: **webinar-01-sg-web-private**
	
	+ Tags: *Key* = **Name**, *Value* = **web-private**

toDoList
~~~~~~~~

- Let's go ahead and run it.

::

	python webservers.py create cfg-private.yml


- From **jumpHost**, run the following command to connect to **web-private** via SSH.

::

	python webserver.py connect private.json


- From **jumpHost**, run the following command to browse to http://**web-private**:5000.

::

	python webserver.py connect private.json --browser


- Add a rule to allow TCP 5000 from **10.0.0.0/16** and **10.2.0.0/16** to security group **webinar-01-sg-web-private**

|

- From **jumpHost**, run the following command to browse to **http://<web-private>:5000**.


::

	python webserver.py connect private.json --browser

- From **web-private**, run the following command.

::

	ping www.google.com


*goingCmdO*
~~~~~~~~~~~

Create a security group.  

::

	aws ec2 create-security-group ^
		--group-name webinar-01-sg-web-private ^
		--description "Allow SHH from anywhere" --vpc-id <vpc-id>

	aws ec2 authorize-security-group-ingress ^
		--group-id <GroupId> ^
		--protocol tcp ^
		--port 22 ^
		--cidr 0.0.0.0/0

|

Launch a single instance.

::

	aws ec2 run-instances ^
		--image-id ami-0090f21784e1f13dd ^
		--instance-type t2.micro ^
		--key-name web-private ^
		--subnet-id <SubnetId> ^
		--security-group-ids <GroupId> ^
		--tag-specifications ResourceType=instance,Tags=[{Key=Name,Value=web-public}]

|

Add a rule to the security group to allow TCP port 5000 from **10.0.0.0/16**.

::

	aws ec2 authorize-security-group-ingress ^
		--group-id <GroupId> ^
		--protocol tcp ^
		--port 5000 ^
		--cidr 10.0.0.0/16

|

Add a rule to the security group to allow TCP port 5000 from **10.2.0.0/16**.

::

	aws ec2 authorize-security-group-ingress ^
		--group-id <GroupId> ^
		--protocol tcp ^
		--port 5000 ^
		--cidr 10.2.0.0/16

|

****

****

Elastic IPs
-----------
To be added.

toDoList
~~~~~~~~


|

****

****

Nat Gateway
-----------


toDoList
~~~~~~~~

- Deploy NAT Gateway named **webinar-01-nat**
- Add a default route to the **webinar-01-rt-private** route table, using the NAT gateway as the target. 

*goingCmdO*
~~~~~~~~~~~

::

	aws ec2 allocate-address ^
		--domain vpc

::

	aws ec2 create-nat-gateway ^
		--allocation-id <AllocationId> ^
		--subnet-id <SubnetId>

|

Add a default route to the **webinar-01-rt-private** route table, using the NAT gateway as the taget.

::

	aws ec2 create-route ^
		--destination-cidr-block 0.0.0.0/0 ^
		--nat-gateway-id <NatGatewayId> ^
		--route-table-id <RouteTableId>

|

****

****

Load Balancers
--------------
To be added.

toDoList
~~~~~~~~

- Create an Application Load-balancer with the following settings

	+ Basic Configuration

		+ name: **webinar-01-lb-app**

		+ IP address type: ipv4

	+ Listeners

		+ Load Balancer Protocol: **HTTP**

		+ Load Balancer Port: **5000**

	+ Availability Zones

		+ VPC: **webinar-01**

		+ Availability Zones

			us-east-1a: **webinar-01-sub-public-01**

			us-east-1b: **webinar-01-sub-public-02**

	+ Configure Security Groups

		+ Assign a security group: **Create a new security group**

		+ Security group name: **webinar-01-sg-lb-app**

		+ Description : **Security group for application load Balancer**

		+ Rule

			Type: **Custom TCP Rule**

			Protocol: **TCP**

			Port Range: **5000**

			Source: **Custom 0.0.0.0/0**

	+ Configure Routing

		+ Target group

			Target group: **New target group**

			Name: **webinar-01-tg-app**

			Target type: **Instance**

			Protocol: **HTTP**

			Port: **5000**

			Protocol version: **HTTP1**

		+ Health checks

			Protocol: **HTTP**

			Path: **/**

	+ Register Targets

		+ Instances

			Select **all**

			Click **Add to registered**

|

- Create an Network Load-balancer with the following settings

	+ Basic Configuration

		+ name: **webinar-01-lb-net**

		+ IP address type: ipv4

	+ Listeners

		+ Load Balancer Protocol: **HTTP**

		+ Load Balancer Port: **5000**

	+ Availability Zones

		+ VPC: **webinar-01**

		+ Availability Zones

			us-east-1a: **webinar-01-sub-public-01**

			us-east-1b: **webinar-01-sub-public-02**

	+ Configure Routing

		+ Target group

			Target group: **New target group**

			Name: **webinar-01-tg-net**

			Target type: **Instance**

			Protocol: **TCP**

			Port: **5000**

		+ Health checks

			Protocol: **TCP**

	+ Register Targets

		+ Instances

			Select **all**

			Click **Add to registered**


*goingCmdO*
~~~~~~~~~~~

::
	aws elbv2 create-load-balancer ^
		--name webinar-01-lb-app ^
		--scheme internet-facing ^
		--type application ^
		--ip-address-type ipv4 ^
		--subnets <SubnetId> <SubnetId> ^
		--security-groups <SecurityGroupId>





|

****

****

Network Load Balancer
---------------------

- Create Network Load-balancer
- Create Target Group for Network Load-balancer
- Register Targets
- Describe Target Group health
- Create Listener for each Network Load-balancer
- Describe Target Group health
- Verify Network Load-balancer
- Test connectivity

toDoList
~~~~~~~~

- Deploy NAT Gateway

*goingCmdO*
~~~~~~~~~~~