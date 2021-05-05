from abc import *
import matplotlib.pyplot as plt
import copy
# 에러 클래스


# 월드 클래스
class VirtualWorld:
    """
    가상 세계를 설정합니다.

    Args:
        measuring_time (초) : 측정할 시간을 설정합니다.
        event_logging_type (전체|충돌|속도|위치) : 표시할 로그의 종류를 설정합니다.
        μ : 마찰저항 (㎏ㆍs/㎡)
    """

    def __init__(self, measuring_time:int=10, event_logging_type:str = "전체", μ:int = 0):
        if measuring_time < 1:
            print("측정 시간은 1초보다 많아야 합니다.")
            raise ValueError
            return

        self.event_logging_type = event_logging_type
        self.measuring_time = measuring_time
        self.objects = {}

        self.events = {}
        for i in range(0, self.measuring_time):
            self.events[i] = {}


    def add_object(self, name, pos:int=0, m:int=1, v:int=0):
        """
        물체를 세계에 추가합니다.

        Args:
            pos: 위치
            m : 질량
            v : 속도
        """

        self.objects[name] = {"pos" : pos, "m" : m, "v" : v, "p" : 0, "before_pos": 0}
        for i in range(1, self.measuring_time):
            self.events[i][name] = {}

    def add_wall(self, name, pos):
        '''
        벽을 세계에 추가합니다.

        Args:
            name: 이름
            pos : 위치
        '''
        

    def event_force_object(self, name, F, time:tuple):
        """
        물체에 지정된 시간동안 힘을 가합니다.
        
        Args:
            name : 물체의 이름
            F : 가할 힘의 크기
            time : 힘을 가하는 시간 ex.(1,2) -> 1초부터 2초까지
        """
        for i in time:
            self.events[i][name]['F'] = F

    def event_accelerate_object(self, name, a, time:tuple):
        """
        물체에 지정된 시간동안 가속할 만큼의 힘을 가합니다.

        Args:
            name : 물체의 이름
            a : 가할 가속도의 크기
            time : 힘을 가하는 시간 ex.(1,2)
        """
        for i in time:
            self.events[i][name]['a'] = a

    def start(self):
        '''
        계산을 시작합니다.
        '''
        result = {}
        collision_range = {}

        # 시간 별 계산
        for i in range(0, self.measuring_time):
            events = self.events[i]
            result[i] = {}
            collision_range[i] = {}
  
            # 물체 별 
            for obj_name in self.objects:
                obj = self.objects[obj_name]
                
                # 물체 이벤트 계산
                if obj_name in events.keys():
                    obj_event = events[obj_name]

                    if "F" in obj_event:
                        obj["p"] = obj["p"] + obj_event["F"]

                    if "a" in obj_event:
                        obj["p"] = obj["p"] + (obj_event("a") * obj["m"])


                # 물체 이동 계산
                before_pos = obj["pos"]
                obj["pos"] = obj["pos"] + obj["p"]
                collision_range[i][obj_name] = [before_pos, obj["pos"]]
                print(collision_range)

                # 계산 결과
                result[i][obj_name] = copy.deepcopy(obj)

        # print(result)

            

    # def event_get_object_info(self, name, time:int):
    #     """
    #     해당 시간의 물체의 상태를 출력합니다.

    #     Args:
    #         물체 : 물체

    #     Returns:
    #         dict : {
    #             name: "이름",
    #             m : 질량,
    #             v : 속도,
    #             a : 가속도,
    #             pos : 위치,
    #             F : 힘
    #         }
    #     """

if __name__ == '__main__':
    world = VirtualWorld(10)
    world.add_object('one')
    world.event_force_object("one", 1, {1,1})
    world.event_force_object("one", -1, {3,3})
    world.start()