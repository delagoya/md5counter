from __future__ import print_function
import boto3
from chalicelib import db

ddb = boto3.resource("dynamodb")
c  = db.DDBMd5Counter(ddb.Table("md5counter"))


print("SUCCESS=",c.get_success())
print("SUCCESS=",c.incr_success())
print("RESET", c.reset_counters())
