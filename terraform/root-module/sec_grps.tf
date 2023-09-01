/*This file contains all security related components like security groups, key pairs, NACL etc
  Note that commonly used route tables are kept in the VPC configuration file itself.
*/

//Creating key pair for use of public instance connection for test purpose
/*resource "aws_key_pair" "sample-pub-key-ec2" {
    key_name = "sample-pub-key-ec2"
    public_key = file("C:/Users/AnandS9/sample-key-ec2.pub")
  
}*/



// Creating security group for public instance to connect through ssh (sample security group)
/*resource "aws_security_group" "allow_ssh_http" {
    description = "Allow ssh & http acces from internet"
    name = "allow_ssh_http"
    vpc_id = aws_vpc.sample-vpc-01.id

    ingress {
        description = "ssh into vpc"
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        description = "http into vpc"
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        description = "all traffic from vpc"
        from_port = 0
        to_port = 0
        protocol = -1
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
      "Name" = "allow-ssh"
      "Creator" = "TF-user"
    }

  
}*/


// Security group for web servers
resource "aws_security_group" "web-svr-sg" {
    description = "Allow traffic from vpc endpoints and load balancer"
    name = "web-svr-sg"
    vpc_id = aws_vpc.sample-vpc-01.id

    /*ingress {
        description = "allow all traffic from vpc endpoints's security group"
        from_port = 0
        to_port = 0
        protocol = -1
        //cidr_blocks = ["0.0.0.0/0"]
        security_groups = [ aws_security_group.endpoint-sg.id ]
    }*/

    ingress {
        description = "allow all from load balancer security group"
        from_port = 0
        to_port = 0
        protocol = -1
        //cidr_blocks = ["0.0.0.0/0"]
        security_groups = [ aws_security_group.load-bal-sg.id ]
    }

    egress {
        description = "all traffic from vpc to outside"
        from_port = 0
        to_port = 0
        protocol = -1
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
      "Name" = "web-svr-sg"
      "Creator" = "TF-user"
    }

  
}

// Security group for VPC endpoints
resource "aws_security_group" "endpoint-sg" {
    description = "Allow traffic from private instances"
    name = "endpoint-sg"
    vpc_id = aws_vpc.sample-vpc-01.id

    ingress {
        description = "allow all traffic from web server security group"
        from_port = 0
        to_port = 0
        protocol = -1
        //cidr_blocks = ["0.0.0.0/0"]
        security_groups = [ aws_security_group.web-svr-sg.id ]
    }

    egress {
        description = "all traffic from vpc to outside"
        from_port = 0
        to_port = 0
        protocol = -1
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
      "Name" = "endpoint-sg"
      "Creator" = "TF-user"
    }

  
}

// Security group for load balancer
resource "aws_security_group" "load-bal-sg" {
    description = "Allow traffic from private instances and internet"
    name = "load-bal-sg"
    vpc_id = aws_vpc.sample-vpc-01.id

    /*ingress {
        description = "allow all traffic from web server security group"
        from_port = 0
        to_port = 0
        protocol = -1
        //cidr_blocks = ["0.0.0.0/0"]
        security_groups = [ aws_security_group.web-svr-sg.id ]
    }*/

    ingress {
        description = "allow http traffic from internet"
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
        //security_groups = [ aws_security_group.web-svr-sg.id ]
    }

    egress {
        description = "all traffic from vpc to outside"
        from_port = 0
        to_port = 0
        protocol = -1
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
      "Name" = "load-bal-sg"
      "Creator" = "TF-user"
    }

  
}











