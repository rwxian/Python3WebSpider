"""
调度模块，用于调度代理测试模块、代理获取模块、代理接口模块
"""

import time
from multiprocessing import Process
from proxy_user.server import app
from proxy_user.getter import Getter
from proxy_user.tester import Tester


TESTER_CYCLE = 20
GETTER_CYCLE = 200
TESTER_ENABLED = True       # 测试模块
GETTER_ENABLED = True       # 获取模块
API_ENABLED = True          # 接口模块
API_HOST = 'localhost'
API_PORT = '8888'


class Scheduler:

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle:
        :return:
        """
        tester = Tester()
        while True:
            print('测试器开始执行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :return:
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启api
        :return:
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:              # 测试模块
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:              # 代理抓取模块
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:                 # 接口模块
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__ == '__main__':
    Scheduler().run()
