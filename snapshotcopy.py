import boto3  
import re  
import datetime

#Please mention your region name
#below line code is call cross region
ec = boto3.client('ec2',region_name='us-east-2')  
iam = boto3.client('iam')

#begins lambda function
def lambda_handler(event, context):  
    account_ids = list()
    try:         
        iam.get_user()
    except Exception as e:
        # use the exception message to get the account ID the function executes under
        account_ids.append(re.search(r'(arn:aws:sts::)([0-9]+)', str(e)).groups()[1])

    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag:DRcopy', 'Values': ['Required']}
        #{'Name': 'tag-value', 'Values': [delete_on]},
    ]
    snapshot_response = ec.describe_snapshots(Filters=filters)
    
    region_name = 'us-east-2'
    copy_region = 'us-east-1'
    source_region = region_name
    
    #addl_ec = boto3.client('ec2', region_name=copy_region)
    
    addl_ec = boto3.client('ec2', region_name='us-east-1')
    print("Found the following snapshots:")
    
    
    for snap in snapshot_response['Snapshots']:
        print (snap['SnapshotId'])            
        addl_snap = addl_ec.copy_snapshot(
            SourceRegion='us-east-2',
            SourceSnapshotId=(snap['SnapshotId']),
            #SourceSnapshotId='snap-0b049c43a8b496485',
            Description='test2',
            DestinationRegion='us-east-1')
       
           
        
    print()