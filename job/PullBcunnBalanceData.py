"""
Pull Home Page Report Data (http://bcunn.com).

work flow:
    engine -> time job ->
                        pull job -> parse data -> save db
                        other job
    web(flask) -> read db -> expose REST
@author nickChen
"""

import requests
import sched

api_url = 'http://bcunn.com/Service/rpc.ashx'


def pull():
    resp = requests.post(api_url, data={'method': 'STOCK_FRAMES'})
    print resp
    if resp.status_code == 200:
        print "post 200"
        data = resp.json()
        if 'Code' in data:
            if data['Code'] == 1:
                doJob()
            else:
                print "Mess data:", data
        else:
            print "Error parse data"


def doJob():
    print "do job"


if __name__ == '__main__':
    pull()
