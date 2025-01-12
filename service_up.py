import json

import boto3

def list_ecs_services(cluster_name1):
    ecs_client = boto3.client('ecs', region_name='ap-south-2')
    
    try:
        response = ecs_client.list_services(
            cluster=cluster_name1,
            maxResults=55
        )
        print(response)
        return response.get('serviceArns', [])
    except Exception as e:
        return []

def register_ecs_scalable_target(cluster_name, service_name, min_capacity, max_capacity):
    ecs_client = boto3.client('application-autoscaling', region_name='ap-south-2')
    
    try:
        response = ecs_client.register_scalable_target(
            ServiceNamespace='ecs',
            ResourceId=f'service/{cluster_name}/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            MinCapacity=1,
            MaxCapacity=2
        )
        return response
    except Exception as e:
        return f"Error registering scalable target: {e}"

def create_update_scaling_policy(client, cluster_name, service_name, metric_name, target_value):
    policy_name = f'ECSAutoScalingPolicy-{metric_name}'
    response = client.put_scaling_policy(
        PolicyName=policy_name,
        ServiceNamespace='ecs',
        ResourceId=f'service/{cluster_name}/{service_name}',
        ScalableDimension='ecs:service:DesiredCount',
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': target_value,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': metric_name
            },
            'ScaleOutCooldown': 300
        }
    )
    return response

def delete_ecs_scaling_policy(client, cluster_name, service_name,dc):
    #ecs_client = boto3.client('application-autoscaling', region_name='ap-south-2')
    #policy_name = f'ECSAutoScalingPolicy-{metric_name}'
    DesiredCount=dc
    try:
        ecs = boto3.client('ecs',region_name='ap-south-2')

        # Update the service desired count to 0
        response = ecs.update_service(
                    cluster=cluster_name,
                    service=service_name,
                    desiredCount=DesiredCount
        )

        return response
    except Exception as e:
        return f"Error deleting scaling policy: {e}"   

def update_ecs_service_autoscaling(cluster_name, service_name, target_cpu, target_memory,dc):
    ecs_client = boto3.client('ecs', region_name='ap-south-2')
    ecs_client1 = boto3.client('application-autoscaling', region_name='ap-south-2')

    try:
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
         )
        # Create or update ECS service scaling policies
        delete_ecs_scaling_policy('ecs', cluster_name, service_name,dc)
        create_update_scaling_policy(ecs_client1, cluster_name, service_name, 'ECSServiceAverageCPUUtilization', target_cpu)
        create_update_scaling_policy(ecs_client1, cluster_name, service_name, 'ECSServiceAverageMemoryUtilization', target_memory)
        return response
    except Exception as e:
        return f"Error updating service auto-scaling: {e}"

def lambda_handler(event, context):
    cluster_name1 = "ILDR-ECS-Nysa------------P3"
    service_arns = list_ecs_services(cluster_name1)
    service_names = [arn.split('/')[-1] for arn in service_arns]
    print("ECS Services in the cluster:")
    for name in service_names:
        print(name)
        print('\n')
        cluster_name = "ILDR-ECS-Nysa------------P3"
        service_name = name
        target_cpu = 70.0
        target_memory = 70.0
        min_capacity=1
        max_capacity=2
        dc=1
        
        register_response = register_ecs_scalable_target(cluster_name, service_name, min_capacity, max_capacity)
        if isinstance(register_response, str):
            print(register_response)
            return

        response = update_ecs_service_autoscaling(cluster_name, service_name, target_cpu, target_memory,dc)
    
        if isinstance(response, str):
            print(response)
        else:
            print(f"Auto-scaling configuration updated successfully: {response['service']['serviceArn']}")
            
if __name__ == "__main__":
    lambda_handler(None, None)






