from gevent import monkey
monkey.patch_all(socket=False, dns=False, time=False, select=False, thread=False, os=False, ssl=True, httplib=False,
              subprocess=False, sys=False, aggressive=False, Event=False,
              builtins=False, signal=False)


from multiprocessing import Pool, Queue, Process
import requests
import gevent
import time

# if __name__ == '__main__':
#     def Socket(url):
#         headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'Accept-Language': 'en',
#             'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)'
#         }
#         res = requests.get(url=url,headers=headers)
#         print(res.headers)
#
#     def add_gevent(urls):
#         gs = []
#         for i in range(len(urls)):
#             gs.append(gevent.spawn(Socket,urls[i]))
#         gevent.joinall(gs)
#
#
#     urls = [
#         ['https://www.baidu.com',
#         'http://bbs.nga.cn/'],
#         ['https://blog.csdn.net/handsomekang/article/details/40297775',
#         'https://www.cnblogs.com/whylinux/p/9865791.html'],
#         ['https://blog.csdn.net/wangjianno2/article/details/51708658',
#         'https://blog.csdn.net/yanpenggong/article/details/83009318'],
#         ['https://www.cnblogs.com/heiguu/p/10056798.html',
#         'https://blog.51cto.com/xmdevops/1862085']
#     ]
#
#     pool = Pool(4)
#
#     for i in range(len(urls)):
#         pool.apply(func=add_gevent,args=(urls[i],))
#
#     pool.close()
#     pool.join()


q = Queue()
for x in range(100):
    q.put(x)

def f1(msg):
    print(str(msg))

def add_gevent(tasks):
    s = []
    for x in range(10):
        s.append(gevent.spawn(f1,tasks[x]))
    gevent.joinall(s)

def start_process(queue):
    pool = Pool(5)
    tasks = []
    while True:
        for i in range(10):
            if queue.empty():
                break
            tasks.append(queue.get())

        if queue.empty():
            break
        pool.apply_async(func=add_gevent, args=(tasks,))
        tasks.clear()
if __name__ == '__main__':
    start_process(q)