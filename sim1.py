from abc import *
from fractions import Fraction
import matplotlib.pyplot as plt
import copy, os, datetime, time, numpy
from sympy import Symbol, solve

# 월드 클래스
class VirtualWorld:
    def __init__(self, measuring_time:int=10, interval=100, debug=False):
        '''
        가상 세계를 설정합니다.

        Args:
            measuring_time : 측정 시간
            interval : 시간 정확도 (1/interval초 마다 측정합니다.)
            debug : 디버그 정보 출력 여부
        '''

        self.measuring_time = measuring_time
        self.interval = interval
        self.debug = debug
        self.start_time = time.time()

        self.objs = {}
        self.events = []

    def add_square(self, name:str, pos:int, m:int=1, v:int=0) -> dict:
        '''
        가상의 물체인 정사각형을 세계에 추가합니다. 

        Args:
            name: 물체의 고유 이름
            pos: 물체의 초기 위치
            m: 물체의 질량 (kg)
            v: 물체의 속도 (m/s)

        Returns:
            생성한 물체의 개체(pos, type, m, v, Ek, p, before_pos)
        '''
        self.objs[name] = {
            "pos" : pos,
            "type" : "square",
            "m" : m,
            "v" : v,
            "Ek" : (1/2) * m * (v ** 2),
            "p" : 0,
            "before_pos": 0
        }
        return self.objs[name]

    def add_wall(self, name:str, pos:int) -> dict:
        '''
        가상의 물체인 벽을 세계에 추가합니다.
        벽은 해당 위치에 고정되어 움직이지 않습니다.

        Args:
            name: 물체의 고유 이름
            pos: 물체의 위치

        Returns:
            생성한 물체의 개체(pos, type)
        '''

        self.objs[name] = {
            "pos" : pos,
            "type" : "wall"
        }
        
    def event_force_object(self, name, F, time:list):
        '''
        물체에 지정한 힘을 주어진 시간동안 가합니다.

        Args:
            name: 힘을 가할 물체
            F: 힘 (N)
            time: 힘을 가하는 시간 ([시작 시간, 끝 시간])
        '''

        self.events.append({
            'objName' : name,
            'F' : F,
            'time' : time
        })

    def start(self):
        '''
        실험을 시작합니다. 생성된 물체와 추가된 이벤트를 진행시킵니다.
        실험이 끝나면 실험 결과를 그래프로 띄웁니다.
        '''
        obj_result = {}
        objs = self.objs
        events = self.events

        graphTypes = ['pos', 'v', 'Ek', 'p']
        time_result = {}
        for graphType in graphTypes:
            time_result[graphType] = {}
            for objName in objs:
                time_result[graphType][objName] = []

        if self.debug:
            print(f"작업 시작 : {self.start_time}")
                

        # 메인 루프
        for i in range(0, (self.measuring_time*self.interval)+1):
            # 디버그용 로그
            if self.debug:
                # os.system('cls')
                for objName in objs.keys():
                    now_time = f'{i // self.interval}초 {i % self.interval}/{self.interval}'
                    print(f'[{i}/{self.measuring_time*self.interval+1}]', end=" ")
                    print(f'{now_time} 초', end=" ")
                    print(f"pos:{objs[objName]['pos']}m, v:{objs[objName]['v']}m/s, Ek:{objs[objName]['Ek']}, p:{objs[objName]['p']}N")
            
            #기록 
            obj_result[i] = {}

            for objName in objs.keys():
                # print(objs)
                obj = objs[objName]
                # print('{0:.5f}'.format(objs[objName]['v']))
                # print(obj['v'])
                try:
                    obj_result[i][objName].append({
                        'pos' : obj['pos'],
                        'v' : obj['v'],
                        'Ek' : obj['Ek'],
                        'p' : obj['p']
                    })
                except KeyError:
                    obj_result[i][objName]=[]
                    obj_result[i][objName].append({
                        'pos' : obj['pos'],
                        'v' : obj['v'],
                        'Ek' : obj['Ek'],
                        'p' : obj['p']
                    })

                for graphType in graphTypes:
                    time_result[graphType][objName].append(obj[graphType])

            # 이벤트 계산
            for event in events:
                event_time = range(event["time"][0] * self.interval, event["time"][1] * self.interval)
                if i in event_time:
                    obj = objs[event['objName']]
                    obj["p"] += event["F"] / self.interval
                    obj["v"] = obj["p"] / obj["m"]
                    obj["Ek"] = (1/2) * obj["m"] * (obj["v"] ** 2)
            
            # 물체 위치 계산
            for objName in objs.keys():
                obj = objs[objName]
                obj['before_pos'] = obj['pos']
                obj['pos'] += obj['v'] / self.interval

        if self.debug:
            print(f"소모 시간 : {time.time() - self.start_time}s")

        # 그래프
        arange = numpy.arange(0, self.measuring_time + (1/self.interval), 1/self.interval)
        plt.subplots(constrained_layout=True)

        # 위치 그래프
        plt.subplot(2, 2, 1)
        plt.xlabel('time')
        plt.ylabel('position(m)')
        plt.title('Position Graph')
        for objName in objs:
            plt.plot(arange, time_result["pos"][objName], label=objName)
        plt.legend()

        # 속도 그래프
        plt.subplot(2, 2, 2)
        plt.xlabel('time')
        plt.ylabel('speed(m/s)')
        plt.title('Speed Graph')
        for objName in objs:
            plt.plot(arange, time_result["v"][objName], label=objName)
        plt.legend()

        # 운동 에너지 그래프
        plt.subplot(2, 2, 3)
        plt.xlabel('time')
        plt.ylabel('Kinetic energy(J)')
        plt.title('Kinetic energy Graph')
        for objName in objs:
            plt.plot(arange, time_result["Ek"][objName], label=objName)
        plt.legend()

        # 운동량 그래프
        plt.subplot(2, 2, 4)
        plt.xlabel('time')
        plt.ylabel('momentu(N·s)')
        plt.title('momentum Graph')
        for objName in objs:
            plt.plot(arange, time_result["p"][objName], label=objName)
        plt.legend()
            

        # plt.plot(, test_res_pos)
        plt.show()

        

if __name__ == '__main__':
    world = VirtualWorld(15, 60, debug=True)
    world.add_square('one', 0, 1)
    world.event_force_object("one", 5, [1,8])
    world.add_square('two', 0, 2)
    world.event_force_object("two", 20, [4,8])
    world.start()