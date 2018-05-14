"""
Pull Home Page Report Data (http://bcunn.com).

work flow:
    engine -> time job ->
                        pull job -> parse data -> save db
                        other job
    web(flask) -> read db -> expose REST


id - coin

107 - 币村积分 / BCUN
208 - 溯源积分 / ACU
209 - EOSlend / EOSlend
@author nickChen
"""

import requests
import schedule
import threading
import time
import datetime
import util.DBUtil as db_util

api_url = 'http://bcunn.com/Service/rpc.ashx'

db_map = {}


def check_time():
    if 9 <= datetime.datetime.now().hour < 21:
        return True
    return False


def pull():
    if not check_time():
        return
    resp = requests.post(api_url, data={'method': 'STOCK_FRAMES'})
    print(resp)
    if resp.status_code == 200:
        print("post 200")
        data = resp.json()
        if 'Code' in data:
            if data['Code'] == 0:
                do_job(data)
            else:
                print("Mess data:", data)
        else:
            print("Error parse data")


def get_db(db_name):
    if db_name not in db_map:
        db_map[db_name] = db_util.db[db_name]
    return db_map[db_name]


def do_job(data):
    print("do job")
    for item in data['Data']:
        key = 'coin' + str(item['Id'])
        item['Time'] = data['Time']
        get_db(key).save(item)


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def engine():
    schedule.every(2).seconds.do(run_threaded, pull)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    engine()
