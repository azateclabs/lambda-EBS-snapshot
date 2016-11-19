import boto3
import re
import datetime

ec = boto3.client('ec2')
iam = boto3.client('iam')

"""
Questa funzione controlla le snapshop che hanno il tag "DeleteOn" con la data odierna in formato YYYY-MM-DD.
Dovrebbe essere lanciata almeno una volta al giorno.
"""

def lambda_handler(event, context):
    account_ids = ['<accountid>']
    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['DeleteOn']},
        {'Name': 'tag-value', 'Values': [delete_on]},
    ]
    snapshot_response = ec.describe_snapshots(OwnerIds=account_ids, Filters=filters)


    for snap in snapshot_response['Snapshots']:
        print "Sto cancellando la snapshot %s" % snap['SnapshotId']
        ec.delete_snapshot(SnapshotId=snap['SnapshotId'])
