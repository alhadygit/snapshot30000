

import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2= session.resource('ec2')

@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None)

def list_instances(project):
    "List EC2 instances"
    instances = []
    if project:
        filt= [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filt)
    else:
        instances = ec2.instances.all()
    for i in instances:
        tags = {  t['Key']:t['Value'] for t in i.tags or []  }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project'  ,'<no project>'))))
    return

@instances.command('stop')
@click.option('--project', default=None)

def Stop_instances(project):
    "Stop EC2 instances"
    instances = []
    if project:
        filt= [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filt)
    else:
        instances = ec2.instances.all()
    for i in instances:
        print('Stopping {}...'.format(i.id))
        i.stop()


@instances.command('start')
@click.option('--project', default=None)

def Start_instances(project):
    "Start EC2 instances"
    instances = []
    if project:
        filt= [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filt)
    else:
        instances = ec2.instances.all()
    for i in instances:
        print('Starting {}...'.format(i.id))
        i.start()


if __name__ == '__main__':
    instances()
