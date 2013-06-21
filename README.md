# EMR Notifier

## Purpose
The purpose of this Python script is to run until stopped; checking the running jobflows in EMR. If it finds a jobflow that has all of it's slave nodes terminated (i.e. when spot price increases past your bid price) it sends a notification to the SNS topic 'EMR-Notifier'.

**Update:** This will also send a notification when a job is in the waiting state. When a job leaves the waiting state and resumes running the notification flag for that job is reset so if the job re-enters the waiting state another notification is sent.

## Configuration
1. Set AWS ID/secret at the beginning of `notifier.py`
2. Create a SNS topic and subscribe all people who should be notfied
3. Set SNS topic name at beginning of `notifier.py`

## Use
`./notifier.py`
This will create a log file `log.notifier` in the same directory logging it's progress.

## Implementation
This script uses Python and boto.
