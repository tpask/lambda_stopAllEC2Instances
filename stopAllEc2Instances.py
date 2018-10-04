#stops all instances from all regions
# Note: you must have appropriate permissions for you lambda role AND
# set lambda function's "Basic Settings"/"Time out" to at least 30 seconds
# for function to have adequate time to make a list of all running instances


import boto3

def lambda_handler(event, context):
  filters = [ { 'Name': 'instance-state-name', 'Values': ['running'] } ]
  runningInstances=[]

  # make a list of all regions:
  regions = boto3.session.Session().get_available_regions('ec2')

  #loops through each region and make a list of all running instances
  for region in regions:
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(Filters=filters)
    for instance in instances:
      runningInstances.append(instance.id)
  
  #with a list of all running instances, 
  if bool(runningInstances):
    boto3.client('ec2', region_name=region).stop_instances(InstanceIds=runningInstances)
    print 'stopped your instances: ' + str(runningInstances)

