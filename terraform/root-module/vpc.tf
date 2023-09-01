/* This file contains the configuration of the custom VPC in our project*/

// Creating VPC using private ip ranges
resource "aws_vpc" "sample-vpc-01" {
    cidr_block = "192.168.0.0/24"  // Using a private ip range of home networks since it is a small network
    enable_dns_hostnames = true
    tags = {
      "Name" = "sample-vpc-01"
      "Creator" = "TF-user"
    }
  
}

// Creatin internet gateway for our vpc
resource "aws_internet_gateway" "sample-igw-1" {
    vpc_id = aws_vpc.sample-vpc-01.id
    tags = {
      "Name" = "sample-igw-1"
      "Creator" = "TF-user"
    }
  
}

// Creating subnets
// First public subnet in ap-southeast-1a availability zone
resource "aws_subnet" "public-sub-1" {
    vpc_id = aws_vpc.sample-vpc-01.id
    cidr_block = "192.168.0.0/27"
    availability_zone = "ap-southeast-1a"
    tags = {
      "Name" = "public-sub-1"
      "Creator" = "TF-user"
    }
  
}

// First private subnet in ap-southeast-1a availability zone
resource "aws_subnet" "private-sub-1" {
    vpc_id = aws_vpc.sample-vpc-01.id
    cidr_block = "192.168.0.32/27"
    availability_zone = "ap-southeast-1a"
    tags = {
      "Name" = "private-sub-1"
      "Creator" = "TF-user"
    }
  
}

// Second public subnet in ap-southeast-1b availability zone
resource "aws_subnet" "public-sub-2" {
    vpc_id = aws_vpc.sample-vpc-01.id
    cidr_block = "192.168.0.64/27"
    availability_zone = "ap-southeast-1b"
    tags = {
      "Name" = "public-sub-2"
      "Creator" = "TF-user"
    }
  
}


// Second private subnet in ap-southeast-1b availability zone
resource "aws_subnet" "private-sub-2" {
    vpc_id = aws_vpc.sample-vpc-01.id
    cidr_block = "192.168.0.96/27"
    availability_zone = "ap-southeast-1b"
    tags = {
      "Name" = "private-sub-2"
      "Creator" = "TF-user"
    }
  
}

//Creating elastic ip for NAT gateway1 in 1st AZ which is ap-southeast-1a
resource "aws_eip" "nat-eip-1" {
    vpc = true
    depends_on = [
      aws_internet_gateway.sample-igw-1
    ]
    tags = {
      "Name" = "nat-eip-1"
      "Creator" = "TF-user"
    }
  
}

//Creating elastic ip for NAT gateway2 in 2nd AZ which is ap-southeast-1b
resource "aws_eip" "nat-eip-2" {
    vpc = true
    depends_on = [
      aws_internet_gateway.sample-igw-1
    ]
    tags = {
      "Name" = "nat-eip-2"
      "Creator" = "TF-user"
    }
  
}

/*// Creating NAT gateway in private subnet 1.  
resource "aws_nat_gateway" "nat-prv-sub-1" {
    subnet_id = aws_subnet.private-sub-1.id
    connectivity_type = "public"
    allocation_id = aws_eip.nat-eip-1.id
    tags = {
      "Name" = "nat-prv-sub-1"
      "Creator" = "TFuser"
    }
  
}*/

/* Note NAT gateways should not be sitting in the Private subnet because of security reasons.
   Gateways should be sitting outside the private subnet so that if hacker find the ip if NAT gateways they
   wont be able to figure out the private subnet devices.*/


// Creating NAT gateway in public subnet 1.
resource "aws_nat_gateway" "nat-pub-sub-1" {
    subnet_id = aws_subnet.public-sub-1.id
    connectivity_type = "public"
    allocation_id = aws_eip.nat-eip-1.id
    tags = {
      "Name" = "nat-pub-sub-1"
      "Creator" = "TFuser"
    }
  
}

// Creating NAT gateway in public subnet 2.
resource "aws_nat_gateway" "nat-pub-sub-2" {
    subnet_id = aws_subnet.public-sub-2.id
    connectivity_type = "public"
    allocation_id = aws_eip.nat-eip-2.id
    tags = {
      "Name" = "nat-pub-sub-2"
      "Creator" = "TFuser"
    }
  
}

//Creating custom route tables for private subnet 1 in 1st AZ ap-southeast-1a
resource "aws_route_table" "prv-rt-1" {
    vpc_id = aws_vpc.sample-vpc-01.id

    route {
      cidr_block = "0.0.0.0/0"
      nat_gateway_id = aws_nat_gateway.nat-pub-sub-1.id
    } 

    tags = {
      "Name" = "prv-rt-1"
      "Creator" = "TF-user"
    }

  
}

//Creating custom route tables for private subnet 2 in 2nd AZ ap-southeast-1b
resource "aws_route_table" "prv-rt-2" {
    vpc_id = aws_vpc.sample-vpc-01.id

    route {
      cidr_block = "0.0.0.0/0"
      nat_gateway_id = aws_nat_gateway.nat-pub-sub-2.id
    } 

    tags = {
      "Name" = "prv-rt-2"
      "Creator" = "TF-user"
    }

  
}

// Associating the above route table to the private subnet 1
resource "aws_route_table_association" "rt-a-prv-sub-1" {
    subnet_id = aws_subnet.private-sub-1.id
    route_table_id = aws_route_table.prv-rt-1.id

}

// Associating the above route table to the private subnet 2
resource "aws_route_table_association" "rt-a-prv-sub-2" {
    subnet_id = aws_subnet.private-sub-2.id
    route_table_id = aws_route_table.prv-rt-2.id
  
}

//creating the public route table for the public subnets

resource "aws_route_table" "pub-rt-1" {
    vpc_id = aws_vpc.sample-vpc-01.id

    route {
      cidr_block = "0.0.0.0/0"
      gateway_id = aws_internet_gateway.sample-igw-1.id
    } 

    tags = {
      "Name" = "pub-rt-1"
      "Creator" = "TF-user"
    }
  
}

//associating public route table to public subnets
resource "aws_route_table_association" "rt-a-pub-sub-1" {
    subnet_id = aws_subnet.public-sub-1.id
    route_table_id = aws_route_table.pub-rt-1.id
  
}

resource "aws_route_table_association" "rt-a-pub-sub-2" {
    subnet_id = aws_subnet.public-sub-2.id
    route_table_id = aws_route_table.pub-rt-1.id
  
}






// Creating vpc endpoints for privately accessing aws services(aws systems manager in this project)

resource "aws_vpc_endpoint" "ec2-endpoint" {
  
  vpc_id = aws_vpc.sample-vpc-01.id
  vpc_endpoint_type = "Interface"
  service_name = "com.amazonaws.ap-southeast-1.ec2"
  subnet_ids = [ aws_subnet.private-sub-1.id, aws_subnet.private-sub-2.id ]
  security_group_ids = [ aws_security_group.endpoint-sg.id ]
  private_dns_enabled = true
  ip_address_type = "ipv4"
  
  
}

resource "aws_vpc_endpoint" "ec2-msg-endpoint" {
  
  vpc_id = aws_vpc.sample-vpc-01.id
  vpc_endpoint_type = "Interface"
  service_name = "com.amazonaws.ap-southeast-1.ec2messages"
  subnet_ids = [ aws_subnet.private-sub-1.id, aws_subnet.private-sub-2.id ]
  security_group_ids = [ aws_security_group.endpoint-sg.id ]
  private_dns_enabled = true
  ip_address_type = "ipv4"
  
  
}

resource "aws_vpc_endpoint" "ssm-endpoint" {
  
  vpc_id = aws_vpc.sample-vpc-01.id
  vpc_endpoint_type = "Interface"
  service_name = "com.amazonaws.ap-southeast-1.ssm"
  subnet_ids = [ aws_subnet.private-sub-1.id, aws_subnet.private-sub-2.id ]
  security_group_ids = [ aws_security_group.endpoint-sg.id ]
  private_dns_enabled = true
  ip_address_type = "ipv4"
  
  
}

resource "aws_vpc_endpoint" "ssm-msg-endpoint" {

  vpc_id = aws_vpc.sample-vpc-01.id
  vpc_endpoint_type = "Interface"
  service_name = "com.amazonaws.ap-southeast-1.ssmmessages"
  subnet_ids = [ aws_subnet.private-sub-1.id, aws_subnet.private-sub-2.id ]
  security_group_ids = [ aws_security_group.endpoint-sg.id ]
  private_dns_enabled = true
  ip_address_type = "ipv4"
  
  
}

// Gateway endpoint 
resource "aws_vpc_endpoint" "s3-gtw-endpoint" {

  vpc_id = aws_vpc.sample-vpc-01.id
  vpc_endpoint_type = "Gateway"
  service_name = "com.amazonaws.ap-southeast-1.s3"
  //subnet_ids = [ aws_subnet.private-sub-1.id, aws_subnet.private-sub-2.id ]
  //security_group_ids = [ aws_security_group.endpoint-sg.id ]
  //private_dns_enabled = true
  //ip_address_type = "ipv4"
  route_table_ids = [aws_route_table.prv-rt-1.id]
  
  
}











