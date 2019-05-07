

import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2= session.resource('ec2')

def filter_instances(project):
    instances = []
    if project:
        filt= [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filt)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def cli():
    """Shotty messages snapshots"""

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@cli.group('snapshots')
def snapshots():
    """Commands for volumes"""


@cli.group('instances')
def instances():
    """Commands for instances"""



@snapshots.command('list')
@click.option('--project', default=None)

def list_snapshots(project):
    "List snapshots volumes"
    instances=filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(' , '.join((
                s.id,
                v.id,
                i.id,
                s.state,
                s.progress,
                s.start_time.strftime("%c")
                )))
    return

@volumes.command('list')
@click.option('--project', default=None)

def list_volumes(project):
    "List EC2 volumes"
    instances=filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print(' , '.join((
            v.id,
            i.id,
            v.state,
            str(v.size) + 'GiB',
            v.encrypted and "Encrypted" or "Not Envrypted"
            )))
    return



@instances.command('list')
@click.option('--project', default=None)

def list_instances(project):
    "List EC2 instances"
    instances=filter_instances(project)
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



@instances.command('snapshot', help="Create Snapshot for all volumes")
@click.option('--project', default=None)

def create_snapshot(project):
    "List EC2 instances"
    instances=filter_instances(project)
    for i in instances:
        print("Stopping {}".format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of {}".format(v.id))
            v.create_snapshot(Description="Created bySnapshot30000")

        print("Starting {}".format(i.id))
        i.start()
        i.wait_until_running()

    print("Job Done!!")

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
    cli()
