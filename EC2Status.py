import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # TODO implement
    print(event)
    app=event['app']
    region=event['region']
    st = get_resources_from_dynamodb(app,region)
    return {
        'statusCode': 200,
        'body': st
    }
    
def get_resources_from_dynamodb(app,region):
    try:
        print("enter ec2")
        # Get all items from the table (can be adjusted to fetch specific data)
        session = boto3.session.Session()
        dynamodb = session.resource('dynamodb', region_name='ap-south-2')
        table = dynamodb.Table('EC2_Inventory')
        ec2response=[]
        filter_str = (Attr('AppName').eq(app) & Attr('Region').eq(region))
        response = table.scan(
                #ExpressionAttributeValues=attributes_str,
                FilterExpression=filter_str

        )
        # dr_instancetype = DynValue = ''
        for i in response['Items']:
            print(i['InstanceId'])
            mumregion='ap-south-1'
            muminstancetype = check_instance_exists(i['InstanceId'],mumregion)
            drsclient = boto3.client('drs',region_name='ap-south-2')
            drsresponse = drsclient.describe_source_servers(
            filters={
               'hardwareId': i['InstanceId'],
            },
            maxResults=123,
            )
            #print(drsresponse)
            
            if drsresponse['items']:
                for d in drsresponse['items']:
                    print(d['sourceServerID'])
                    print(d['recoveryInstanceId'])
                    if d['recoveryInstanceId']:
                        hydregion='ap-south-2'
                        hydinstance_id = d['recoveryInstanceId']
                        hydinstancetype = check_instance_exists(d['recoveryInstanceId'],hydregion)
                        print(type(hydinstancetype))
                        if not hydinstancetype:
                            hydinstance_id = ""
                            hydinstancetype = ""
                    else:
                        hydinstance_id = ""
                        hydinstancetype = ""
                    region2='ap-south-2'
                    filter1_str = (Attr('AppName').eq(app) & Attr('Region').eq(region2) & Attr('EDR.SourceID').contains(d['sourceServerID']))
                    print(filter1_str)
                    response1 = table.scan(
                            #ExpressionAttributeValues=attributes_str,
                            FilterExpression=filter1_str
            
                    )
                    print(response1)
                    if response1['Items']:
                        for i in response1['Items']:
                            print("Enter loop for sourceid")
                            # print(i)
                            dr_instancetype = i['InstanceDetails']['InstanceType']
                            
                            DynValue = "True"
                            print(dr_instancetype,DynValue)
                    
                    else:
                        dr_instancetype = ""
                        DynValue = "False"
                    print(dr_instancetype,DynValue)
                    print(i['InstanceId'],i['InstanceDetails']['InstanceType'],d['sourceServerID'],hydinstance_id,hydinstancetype)
                    tjson={'AppName':app,'InstanceId':i['InstanceId'],'InstanceType':i['InstanceDetails']['InstanceType'],'SourceId':d['sourceServerID'],'SourceType':dr_instancetype,'HydInstanceId':hydinstance_id,'HydInstanceType':hydinstancetype,"DynamoDB":DynValue}
                    print(tjson)

                    ec2response.append(tjson)
            else:
                tjson={'AppName':app,'InstanceId':i['InstanceId'],'InstanceType':i['InstanceDetails']['InstanceType'],'SourceId':"Check if ec2 ispresent",'SourceType':dr_instancetype,'HydInstanceId':hydinstance_id,'HydInstanceType':hydinstancetype,"DynamoDB":DynValue}
                print(tjson)

                ec2response.append(tjson)
#        print("response",response)
#        return response.get('Items', [])
        return ec2response
    except Exception as e:
        print(e)
        return []

def check_instance_exists(instance_id,region):
    # Create EC2 client

    ec2 = boto3.client('ec2',region_name=region)
    try:
        # Describe instances using the instance_id
        response = ec2.describe_instances(InstanceIds=[instance_id])

        # Check if instance exists in the response
        if response['Reservations']:
            instance = response['Reservations'][0]['Instances'][0]
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']

            # Print instance details
            print(f"Instance ID: {instance_id}")
            print(f"Instance Type: {instance_type}")
            return  instance_type
            #print(f"Instance {instance_id} exists.")
            #return True
        else:
            print(f"Instance {instance_id} does not exist.")
            return None
    except ClientError as e:
        # If an error occurs (e.g., instance doesn't exist or permission issues)
        if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
            print(f"Instance {instance_id} not found.")
            #return f"{instance_id} not found."
            return False
        else:
            print(f"An error occurred: {e}")
            return False
            
            
def get_attached_volumes(instance_id):
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
    # List of volumes attached to the instance
    volumes = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for block_device in instance['BlockDeviceMappings']:
                volume_id = block_device['Ebs']['VolumeId']
                volumes.append(volume_id)
    
    return volumes

# Function to get volume details such as IOPS, type, and size
def get_volume_details(volume_ids):
    volume_details = []
    
    # Fetch details for each volume
    for volume_id in volume_ids:
        volume = ec2_resource.Volume(volume_id)
        volume_info = {
            'VolumeId': volume_id,
            'Size': volume.size,  # Size in GiB
            'IOPS': volume.iops,  # IOPS for io1 or io2 types
            'VolumeType': volume.volume_type,  # Volume type (e.g., gp2, io1, etc.)
            'State': volume.state,
            'AvailabilityZone': volume.availability_zone
        }
        volume_details.append(volume_info)
    
    return volume_details

# Function to compare volumes
def compare_volumes(vol1_details, vol2_details):
    comparison_results = {}
    
    for key in vol1_details[0]:
        vol1_value = vol1_details[0][key]
        vol2_value = vol2_details[0][key]
        
        if vol1_value != vol2_value:
            comparison_results[key] = {
                'Instance 1': vol1_value,
                'Instance 2': vol2_value
            }
    
    return comparison_results
