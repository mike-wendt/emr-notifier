#!/usr/bin/env python

import boto
import time
import logging

# AWS credentials
aws_id = 'AWS'
aws_secret = 'S3cR3t'

# AWS SNS topic name
sns_topic = "EMR-Notifier"

def sendNotification( jobflowid, message ):
  # Create new topic
  topic = sns.create_topic(sns_topic)
  
  # Retrieve TopicArn
  arn = topic['CreateTopicResponse']['CreateTopicResult']['TopicArn']
  
  # Generate subject for notification
  subject = "Status Update - %s" % jobflowid
  
  # Publish notification
  sns.publish(arn, message, subject)
  
  # Print log message
  logging.info("Sent notification about %s" % jobflowid)

# List to keep jobflowids that have notifications sent for them
notified_run = []
notified_wait = []

# Messages
message_instances = "All slaves terminated in jobflow."
message_waiting = "Jobflow status changed to waiting."

# Configure logging
logging.basicConfig(filename="log.notifier", level=20, format="%(asctime)s %(levelname)s - %(message)s")
logging.info("Notifier initialized")

# Connect to SNS/EMR
sns = boto.connect_sns(aws_id,aws_secret)
emr = boto.connect_emr(aws_id,aws_secret)

# Loop forever checking jobs
while True:
  # Get current running tasks
  run = emr.describe_jobflows(['RUNNING'])
  
  # Process each jobflow to check number of instances
  for job in run:
    if int(job.__dict__.get('instancegroups')[1].__dict__.get('instancerunningcount')) == 0:
      if notified_run.count( job.jobflowid ) == 0:
        notified_run.append( job.jobflowid )
        sendNotification( job.jobflowid, message_instances )
    if notified_wait.count( job.jobflowid ) != 0:
      notified_wait.remove( job.jobflowid )
  
  # Log processing
  logging.info("%d running jobflows checked" % len(run))
  
  # Get current waiting tasks
  wait = emr.describe_jobflows(['WAITING'])
  
  # Process each jobflow to check number of instances
  for job in wait:
      if notified_wait.count( job.jobflowid ) == 0:
        notified_wait.append( job.jobflowid )
        sendNotification( job.jobflowid, message_waiting )
  
  # Log processing
  logging.info("%d waiting jobflows checked" % len(wait))
  
  # Wait to check again
  time.sleep(30)
