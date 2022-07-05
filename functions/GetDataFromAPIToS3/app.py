#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import urllib.parse
import boto3
import requests
import logging
import os


# Environment variables
URL = os.environ['Url']
S3_BUCKET = os.environ['S3Bucket']
LOG_LEVEL = os.environ['LogLevel']
FILENAME = os.environ['Filename']

# Log settings
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
s3 = boto3.client('s3')


# Lambda function handler
def lambda_handler(event, context):
    logger.info('## EVENT')
    logger.info(event)

    bucket=S3_BUCKET
    object_key=FILENAME
    

    try:
        res = requests.get(URL)
        response = s3.put_object( 
            Bucket=bucket,
            Key=object_key,
            Body=bytes(json.dumps(res.json()).encode('UTF-8'))
        )

    except Exception as e:
        print(e)
        print('Error writing object {} to bucket {}. Make sure the bucket exisist and the lambda has appropricate permission.'.format(object_key, bucket))
        raise e

    s3url = 's3://{}/{}'.format(S3_BUCKET, FILENAME)
    logger.info('## OUTPUT FILE PATH')
    logger.info(s3url)
        
        
    return {'statusCode': 200,
                'outputfile': {
                    "bucket": bucket,
                    "key": object_key
                }
            }   