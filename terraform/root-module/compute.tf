/*This file contains the configuration of the web servers running on ec2 instnaces*/


/*// Creating public instance in public subnet to test functionality properply initially for test purpose
  // As a Sample code below
resource "aws_instance" "web-svr-1" {

    //subnet_id = aws_subnet.private-sub-1
    subnet_id = aws_subnet.public-sub-1.id
    instance_type = "t2.micro"
    //associate_public_ip_address = false
    associate_public_ip_address = true
    ami = "ami-0f62d9254ca98e1aa"
    key_name = aws_key_pair.sample-pub-key-ec2.key_name
    vpc_security_group_ids = [aws_security_group.allow_ssh_http.id]
    user_data_replace_on_change = true
    ebs_block_device {
        delete_on_termination = true
        volume_size = 1
        volume_type = "gp3"
        device_name = "/dev/sdb"
        
      
    }    
    // user data can be given in two formats provided below:
    // 1.
    //user_data = <<EOF
    //#!/bin/bash
    //sudo su -    

    //EOF

    // 2.
    user_data = file("./init-ws.sh")

    

    
  
}*/

// Creating user data template file using datasource
//data "template_file" "user_data" {
//    template = "${file("init-ws.sh")}"  
//}




// Creating our web server instances now
// Note: we are using AMIs with preinstanlled SSM agents
// Below is the first instance web-svr-1 in public-subnet-1 in ap-southeast-1a
resource "aws_instance" "web-svr-1" {

    subnet_id = aws_subnet.private-sub-1.id
    //subnet_id = aws_subnet.public-sub-1.id
    instance_type = "t2.micro"  
    associate_public_ip_address = false 
    //associate_public_ip_address = true
    ami = "ami-094bbd9e922dc515d"
    //key_name = aws_key_pair.sample-pub-key-ec2.key_name
    vpc_security_group_ids = [aws_security_group.web-svr-sg.id]
    user_data_replace_on_change = true
    iam_instance_profile = aws_iam_instance_profile.SSM-managed-instances.name
    ebs_block_device {
        delete_on_termination = true
        volume_size = 1
        volume_type = "gp3"
        device_name = "/dev/sdb"
        
      
    }    
    // user data can be given in two formats provided below:
    // 1.
    user_data = <<EOF
    #!/bin/bash
    sudo su -
    yum update -y

    # Below steps are implemented to mount the separate disk that we bought
    # Making file system on the disk by formatting it into fs type ext4
    mkfs -t ext4 /dev/sdb 
    # Remember that the device name value is hardcoded since it is available in the config 

    # Now we have a single partition on our disk with filesystem type as ext4
    # Next step is to mount the disk on to a filesystem and make the fstab entry for automount operation
    mkdir /web_svr_mnt
    # Mount point made above
    mount /dev/sdb /web_svr_mnt
    # Disk has now been mounted

    # Below we are retreiving the information to be appended into /etc/fstab file
    init=""   # declaring initial variable
    init=$(blkid /dev/sdb | awk '{ print $2 }') # pulling the 2nd field from blkid command output 
    medium=$${init:6}  # trimming first 6 characters
    final=$${medium::-1}  # trimming last 1 character

    # Making the fstab entry
    echo "UUID=$final    /web_svr_mnt     ext4    defaults,noatime  0   2" >> /etc/fstab

    # Now mount operation will automatically happen on reboot

    # Next step is to install and configure web server on the instance
    yum -y install httpd
    systemctl start httpd
    systemctl enable httpd

    # Creating softlink from apache root folder to our folder in the separate filesystem on EBS volume
    mkdir /web_svr_mnt/web_svr_root
    ln -s /var/www/html /web_svr_mnt/web_svr_root/

    cd /web_svr_mnt/web_svr_root/html
    touch index.html
    ip="" # getting instance metadata (ip address here)
    ip=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
    echo -e "<!DOCTYPE html>\n<html>\n<head>\n<title>\n</title>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>\nbody {background-color:#ffffff;background-repeat:no-repeat;background-position:top left;background-attachment:fixed;}\nh1{font-family:Arial, sans-serif;color:#000000;background-color:#ffffff;}\np {font-family:Georgia, serif;font-size:14px;font-style:normal;font-weight:normal;color:#000000;background-color:#ffffff;}\n</style>\n</head>\n<body>\n<h1>Hello VF-Cloud World from $ip </h1>\n<p></p>\n</body>\n</html>\n" > index.html

    # Now installing aws-ssm-agent for using session manager
    yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
    systemctl enable amazon-ssm-agent


    EOF

    // 2.
    //user_data = file("./init-ws.sh")
    // 3.
    //user_data = "${data.template_file.user_data.rendered}"
    depends_on = [
      aws_eip.nat-eip-1, 
      aws_eip.nat-eip-2, 
      aws_nat_gateway.nat-pub-sub-1,
      aws_nat_gateway.nat-pub-sub-2,
      aws_subnet.private-sub-1,
      aws_subnet.private-sub-2,
      aws_route_table.prv-rt-1,
      aws_route_table.prv-rt-2,
      aws_route_table_association.rt-a-prv-sub-1,
      aws_route_table_association.rt-a-prv-sub-2

    ]

    

    
  
}


// Below is the second instance web-svr-2 in public-subnet-1 in ap-southeast-1b
resource "aws_instance" "web-svr-2" {

    subnet_id = aws_subnet.private-sub-2.id
    //subnet_id = aws_subnet.public-sub-2.id
    instance_type = "t2.micro"
    associate_public_ip_address = false 
    //associate_public_ip_address = true
    ami = "ami-094bbd9e922dc515d"
    //key_name = aws_key_pair.sample-pub-key-ec2.key_name
    vpc_security_group_ids = [aws_security_group.web-svr-sg.id]
    user_data_replace_on_change = true
    iam_instance_profile = aws_iam_instance_profile.SSM-managed-instances.name
    ebs_block_device {
        delete_on_termination = true
        volume_size = 1
        volume_type = "gp3"
        device_name = "/dev/sdb"
        
      
    }    
    // user data can be given in two formats provided below:
    // 1.
    user_data = <<EOF
    #!/bin/bash
    sudo su -
    yum update -y

    # Below steps are implemented to mount the separate disk that we bought
    # Making file system on the disk by formatting it into fs type ext4
    mkfs -t ext4 /dev/sdb 
    # Remember that the device name value is hardcoded since it is available in the config 

    # Now we have a single partition on our disk with filesystem type as ext4
    # Next step is to mount the disk on to a filesystem and make the fstab entry for automount operation
    mkdir /web_svr_mnt
    # Mount point made above
    mount /dev/sdb /web_svr_mnt
    # Disk has now been mounted

    # Below we are retreiving the information to be appended into /etc/fstab file
    init=""   # declaring initial variable
    init=$(blkid /dev/sdb | awk '{ print $2 }') # pulling the 2nd field from blkid command output 
    medium=$${init:6}  # trimming first 6 characters
    final=$${medium::-1}  # trimming last 1 character

    # Making the fstab entry
    echo "UUID=$final    /web_svr_mnt     ext4    defaults,noatime  0   2" >> /etc/fstab

    # Now mount operation will automatically happen on reboot

    # Next step is to install and configure web server on the instance
    yum -y install httpd
    systemctl start httpd
    systemctl enable httpd

    # Creating softlink from apache root folder to our folder in the separate filesystem on EBS volume
    mkdir /web_svr_mnt/web_svr_root
    ln -s /var/www/html /web_svr_mnt/web_svr_root/

    cd /web_svr_mnt/web_svr_root/html
    touch index.html
    ip="" # getting instance metadata (ip address here)
    ip=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
    echo -e "<!DOCTYPE html>\n<html>\n<head>\n<title>\n</title>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>\nbody {background-color:#ffffff;background-repeat:no-repeat;background-position:top left;background-attachment:fixed;}\nh1{font-family:Arial, sans-serif;color:#000000;background-color:#ffffff;}\np {font-family:Georgia, serif;font-size:14px;font-style:normal;font-weight:normal;color:#000000;background-color:#ffffff;}\n</style>\n</head>\n<body>\n<h1>Hello VF-Cloud World from $ip </h1>\n<p></p>\n</body>\n</html>\n" > index.html

    # Now installing aws-ssm-agent for using session manager
    yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
    systemctl enable amazon-ssm-agent    

    EOF

    // 2.
    //user_data = file("./init-ws.sh")
    // 3. 
    //user_data = "${data.template_file.user_data.rendered}"
    depends_on = [
      aws_eip.nat-eip-1, 
      aws_eip.nat-eip-2, 
      aws_nat_gateway.nat-pub-sub-1,
      aws_nat_gateway.nat-pub-sub-2,
      aws_subnet.private-sub-1,
      aws_subnet.private-sub-2,
      aws_route_table.prv-rt-1,
      aws_route_table.prv-rt-2,
      aws_route_table_association.rt-a-prv-sub-1,
      aws_route_table_association.rt-a-prv-sub-2

    ]

    

    
  
}

/* The below code is for doing the load balancer configuration*/
// Creating ec2-target group for load balancer
resource "aws_lb_target_group" "web-svr-cls" {
    name = "web-svr-cls"
    target_type = "instance"
    port = 80
    protocol = "HTTP"
    vpc_id = aws_vpc.sample-vpc-01.id
    health_check {
      healthy_threshold = 2      
    }
  
}

// Attaching instances to the above target group using another resource
resource "aws_lb_target_group_attachment" "web-svr-cls-inst1" {
    target_group_arn = aws_lb_target_group.web-svr-cls.arn
    target_id = aws_instance.web-svr-1.id
    
  
}

// only one instance can be attched at a time using this resource
resource "aws_lb_target_group_attachment" "web-svr-cls-inst2" {
    target_group_arn = aws_lb_target_group.web-svr-cls.arn
    target_id = aws_instance.web-svr-2.id
    
  
}


// Creating listener for load balancer
resource "aws_lb_listener" "sample-lsnr-01" {
    load_balancer_arn = aws_lb.sample-lb-01.arn
    port = 80
    protocol = "HTTP"
    default_action {
      type = "forward"
      target_group_arn = aws_lb_target_group.web-svr-cls.arn
    }
  
}


// Creating application load balancer(internet facing)
resource "aws_lb" "sample-lb-01" {
    name = "sample-lb-01"
    load_balancer_type = "application"
    internal = false // this makes it internet facing
    ip_address_type = "ipv4"
    subnets = [ aws_subnet.public-sub-1.id, aws_subnet.public-sub-2.id ] // these should always be public for internet facing lb
    security_groups = [ aws_security_group.load-bal-sg.id ]

  
}



















