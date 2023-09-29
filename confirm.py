import json
import subprocess
print("Before proceeding further please make sure AWS CLI is configured in your system")
input()

# Print the AMI name and AMI ID to the console.


def All_redhat():
    output_image = subprocess.getoutput(
        "aws ec2 describe-images --filters Name=name,Values=RHEL-*")
    # Parse the JSON output.
    json_data = json.loads(output_image)

    # Extract the AMI name and AMI ID for each AMI.
    for ami in json_data['Images']:
        ami_name = ami['Name']
        ami_id = ami['ImageId']
        ami_name = (f'AMI name: {ami_name}')
        ami_id = (f'AMI ID: {ami_id}')
        print(ami_id)
        print(ami_name)
    return ami_name, ami_id


