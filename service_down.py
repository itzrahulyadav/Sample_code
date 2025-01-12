import json

import boto3

def list_ecs_services(cluster_name1):
    ecs_client = boto3.client('ecs', region_name='ap-south-1')
    
    try:
        response = ecs_client.list_services(
            cluster=cluster_name1,
            maxResults=10
        )
        return response.get('serviceArns', [])
    except Exception as e:
        return []

def deregister_ecs_scalable_target(client, cluster_name, service_name):
    ecs_client = boto3.client('application-autoscaling', region_name='ap-south-1')
    
    try:
        response = ecs_client.deregister_scalable_target(
            ResourceId=f'service/{cluster_name}/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            ServiceNamespace='ecs',
        )
        return response
    except Exception as e:
        return f"Error deregistering scalable target: {e}"
	  
def delete_ecs_scaling_policy1(client, cluster_name, service_name):
    try:
        ecs = boto3.client('ecs',region_name='ap-south-1')

        # Update the service desired count to 0
        response = ecs.update_service(
                    cluster=cluster_name,
                    service=service_name,
                    desiredCount=0
        )
        return response
    except Exception as e:
        return f"Error deleting scaling policy: {e}" 

def stop_ecs_services_and_tasks_with_tag(id):

    ecs = boto3.client('ecs', region_name='ap-south-1')
    
    # Replace these values with your specific cluster name and service name
    cluster_name = 'IL-ECS-Nysa------------P3'
    service_name = 'id'

    # List tasks for the specified ECS service
    try:
        response = ecs.list_tasks(
            cluster=cluster_name,
            serviceName=id,
            desiredStatus='RUNNING'  
        )
    
        if 'taskArns' in response:
            task_arns = response['taskArns']
            print(f"Tasks for ECS service '{service_name}' in cluster '{cluster_name}':")
            for task_arn in task_arns:
                print(task_arn)
                response = ecs.stop_task(
                     cluster='IL-ECS-Nysa------------P3',
                     task= task_arn
                )
    
        else:
            print(f"No tasks found for ECS service '{service_name}' in cluster '{cluster_name}'.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")        
        
def lambda_handler(event, context):
    cluster_name1 = "IL-ECS-Nysa------------P3"
    service_arns = list_ecs_services(cluster_name1)
    service_names = [arn.split('/')[-1] for arn in service_arns]
    #print(service_names)
    print("ECS Services in the cluster:")
    for name in service_names:
        print(name)
        print('\n')
        cluster_name = "IL-ECS-Nysa------------P3"
        service_name = name

        response = deregister_ecs_scalable_target('ecs', cluster_name, service_name)
        response = delete_ecs_scaling_policy1('application-autoscaling', cluster_name, service_name)
        stop_ecs_services_and_tasks_with_tag(name)
        if isinstance(response, str):
            print(response)
        else:
            print(f"Auto-scaling configuration updated successfully")
        
