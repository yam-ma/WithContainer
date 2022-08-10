import logging.handlers
import logging
import json
import numpy as np
import pygrib
import pywgrib2_s
import boto3
import os
import datetime
import glob

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    #-------------------------
    # event受け渡しのテスト
    #-------------------------
    print("key1", event["key1"])
    print("key2", event["key2"])
    print("key3", event["key2"])
    print("context", context)

    
    #-------------
    # logの設定
    #-------------
    log = logging.getLogger(__name__)
    
    logging.basicConfig(
        level=logging.INFO,
        force=True,
        handlers=None,
        format='%(asctime)s %(filename)s %(levelname)s %(message)s'
    )

    
    now = datetime.datetime.utcnow()
    deliver_time = datetime.datetime(now.year, now.month, now.day, 5, 0, 0)
    + datetime.timedelta(hours = 1)                                                                         
    deliver_time = deliver_time.strftime('%Y%m%d%H%M%S')   

    #------------------------
    # tmp fileを作るテスト
    #------------------------
    tagid = event['key1']
    fname = "/tmp/storm"+deliver_time + "_" + tagid
    print("fname", fname)
    event_tagids = []

    with open(fname, "wt") as f:
        f.write(tagid)

    flist = glob.glob("/tmp/storm*_???")
    print(flist)

    for fname in flist:
        
        with open(fname, "r") as f:
            event_tagids += f.readlines()

    print("event_tagids", event_tagids)

    command = "ls /tmp/storm*_???"
    os.system(command)

    if set(event_tagids) == set(['100', '200', '300']):
        os.system("rm -f /tmp/storm*_???")
    
    log.info("Hello world!")
    
    template = os.path.dirname(__file__) + "/MSM_template.grb"
    output = os.path.dirname(__file__) + "/out_test.grib"
    result = os.path.dirname(__file__) + "/out_test.grb"
    output = "/tmp/out_test.grib"
    result = "/tmp/out_test.grb"

    grbs = pygrib.open(template)

    for grb in grbs:
        print(grb)
        print(grb.latlons())
        data = grb.values

    newdata = np.full((data.shape[0], data.shape[1]), 100)
    a = pywgrib2_s.write(output, template, 1, new_data = newdata,
                         var = "TMP", ftime = "6 hour fcst", time0 = deliver_time)
    pywgrib2_s.close(output)
    a = pywgrib2_s.write(output, template, 1, new_data = newdata,
                         var = "SSTMI", ftime = "12 hour fcst", time0 = deliver_time, Append = True)
    pywgrib2_s.close(output)
    log.info(a)

    #
    # centerを移動する                                                     
    #                                                                   
    command = "wgrib2 -set center 253 " + output + " -grib " + result
    os.system(command)

    with open(result, "rb") as f:
        data = f.read()

    
    bucket = {"storm-ex"}
    s3 = boto3.resource('s3')
    key = "storm.grb"

    obj = s3.Object("storm-ex", key)
    obj.put(Body = data)
        
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }

if __name__ == "__main__":

    event = {}
    context = ""
    lambda_handler(event, context)
