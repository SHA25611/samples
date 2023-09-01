/*This file contains all the IAM related configurations*/

// Creating assume role policy that allows entities to assume a certain role
data "aws_iam_policy_document" "instance_assume_role_policy" {
    statement {
      actions = ["sts:AssumeRole"]
      principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
      }

    }
  
}


// Creating IAM policy for management of all resources using aws systems manager
resource "aws_iam_policy" "AmazonSSMManagedInstanceCore" {
    name = "AmazonSSMManagedInstanceCore"
    policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeAssociation",
                "ssm:GetDeployablePatchSnapshotForInstance",
                "ssm:GetDocument",
                "ssm:DescribeDocument",
                "ssm:GetManifest",
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:ListAssociations",
                "ssm:ListInstanceAssociations",
                "ssm:PutInventory",
                "ssm:PutComplianceItems",
                "ssm:PutConfigurePackageResult",
                "ssm:UpdateAssociationStatus",
                "ssm:UpdateInstanceAssociationStatus",
                "ssm:UpdateInstanceInformation"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2messages:AcknowledgeMessage",
                "ec2messages:DeleteMessage",
                "ec2messages:FailMessage",
                "ec2messages:GetEndpoint",
                "ec2messages:GetMessages",
                "ec2messages:SendReply"
            ],
            "Resource": "*"
        }
    ]
})
  
}

// Creating the IAM role have ssm related policies
resource "aws_iam_role" "ssm-for-ec2" {
    description = "Will be assumed by our web server instnaces"
    force_detach_policies = true
    name = "ssm-for-ec2"
    assume_role_policy = data.aws_iam_policy_document.instance_assume_role_policy.json
    managed_policy_arns = [aws_iam_policy.AmazonSSMManagedInstanceCore.arn]


  
}


// Creating an instance profile containing the subjected role.
// Note : only instance profile can be attached with ec2 instances, 
// i.e. role must be contained within a profile
resource "aws_iam_instance_profile" "SSM-managed-instances" {
    name = "SSM-managed-instances"
    role = aws_iam_role.ssm-for-ec2.name
  
}





