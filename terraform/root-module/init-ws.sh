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
