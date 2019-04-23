from gevent import monkey

monkey.patch_ssl()

from multiprocessing import Pool, Queue
import gevent
import requests
from requests.exceptions import ConnectTimeout
from config import get_header, TEST_URL, TIME_OUT, RETRY_TIMES, MAX_GEVENTS, MAX_PROCESSES
import json

"""
最大进程数:MAX_PROCESSES -- P
每个进程使用最大协程数:MAX_GEVENTS -- G
sum = P * G
待检测IP格式{'iptype':'','ip':'','port':''},
"""

# 检测协议类型
# ip检测函数(协程处理单元)
# 多协程启动与回收(进程目标函数)
# 利用进程池启动与回收进程





# ip检测函数(协程处理单元)
def test_ip(IP, test_url=TEST_URL):
    proxies = {str(IP['type']).lower(): str(IP['type']).lower() + '://' + str(IP['ip']) + ':' + str(IP['port'])}
    # 检测ip对目标url的有效性
    for i in range(RETRY_TIMES):
        try:
            headers = get_header()
            r = requests.get(url=test_url, headers=headers, proxies=proxies, timeout=TIME_OUT)
            resip = json.loads(r.text)
            if r.status_code == 200 and resip['origin'].split(',')[0] == str(IP['ip']):
                print(str(IP['ip']) + ':' + str(IP['port']))
                return (True,IP)
        except ConnectTimeout:
            continue
        except Exception as e:
            print(e, str(IP['ip']) + ':' + str(IP['port']), '无效')
            return False
    # print(str(IP['ip']) + ':' + str(IP['port']), '无效')


# 多协程启动与回收(进程目标函数)
def start_gevent(tasks):
    sg = []  # 协程列表
    for i in range(len(tasks)):
        if not bool(tasks[i]):
            break
        g = gevent.spawn(test_ip, tasks[i], TEST_URL)
        sg.append(g)
    gevent.joinall(sg)


# 利用进程池启动与回收进程
def start_process(queue):
    pool = Pool(20)
    tasks = []
    while True:
        empty = False
        for i in range(20):
            if not queue.empty():
                tasks.append(queue.get())
            else:
                empty = True
                break


        pool.apply_async(func=start_gevent, args=(tasks,))
        if empty == True:
            break
        tasks = []
    pool.close()
    pool.join()


if __name__ == '__main__':
    ips = [
        {'ip': '124.160.56.76', 'port': '57651', 'type': 'HTTPS'},
        {'ip': '1.20.100.130', 'port': '40504', 'type': 'HTTPS'},
        {'ip': '182.150.35.173', 'port': '80', 'type': 'HTTPS'},
        {'ip': '116.209.55.16', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '111.177.183.139', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '112.85.131.158', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '111.177.184.134', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '106.9.170.89', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '119.102.28.171', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '111.177.163.0', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '114.80.62.134', 'port': '8080', 'type': 'HTTPS'},
        {'ip': '222.208.101.25', 'port': '808', 'type': 'HTTPS'},
        {'ip': '1.20.102.56', 'port': '40922', 'type': 'HTTPS'},
        {'ip': '1.20.103.248', 'port': '52574', 'type': 'HTTPS'},
        {'ip': '111.177.167.172', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '111.177.172.96', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '119.102.28.187', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '59.37.33.62', 'port': '50686', 'type': 'HTTP'},
        {'ip': '218.91.112.9', 'port': '9999', 'type': 'HTTPS'},
        {'ip': '1.83.126.250', 'port': '8118', 'type': 'HTTPS'},
        {'ip': '121.13.252.60', 'port': '41564', 'type': 'HTTPS'},
        {'ip': '221.1.200.242', 'port': '61957', 'type': 'HTTPS'},
        {'ip': '223.99.214.21', 'port': '53281', 'type': 'HTTPS'},
        {'ip': '1.20.100.219', 'port': '39043', 'type': 'HTTPS'}
    ]
    print(len(ips))
    queue = Queue()
    for i in ips:
        queue.put(i)
    start_process(queue)
