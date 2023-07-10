import random
from InputsConfig import InputsConfig as p  # import导入的是类，导入后就可以使用该类定义的属性值和函数
from Event import Event, Queue
from Scheduler import Scheduler
from Statistics import Statistics
from decimal import Decimal
from Models.Network import Network
from Models.Information import FullInformation as FI


class Travel():

    def coming(clock, TravellingVehicle):  # 判断车辆是否到达
        for i in p.VEHICLE:
            if clock == i.time:
                FI.create_information(i)
                TravellingVehicle.append(i)

    def Travellling(clock, TravellingVehicle):
        receiver = p.NODES[0]  # 初始RSU，不具备传输能力，用来标记车辆附件是否存在RSU

        for j in range(len(TravellingVehicle)):
            if clock == (
                    TravellingVehicle[j].time + Decimal(TravellingVehicle[j].informationPool[0].timestamp[1]).quantize(
                    Decimal("1."), rounding="ROUND_HALF_UP")) and TravellingVehicle[j].informationPool[0].if_send == 0:
                TravellingVehicle[j].location = (clock - TravellingVehicle[j].time) * TravellingVehicle[j].speed

                #  计算车辆在当前所在位置的通信范围的上下限
                location1 = TravellingVehicle[j].location - TravellingVehicle[j].communication
                if location1 < 0:
                    location1 = 0
                location2 = TravellingVehicle[j].location + TravellingVehicle[j].communication
                if location2 > p.length:
                    location2 = p.length
                rsu_location = 0

                # 在车辆的通信范围内寻找是否存在RSU
                for z in range(location1, location2):
                    if p.Road[z] != 0:
                        for x in p.NODES:
                            if p.Road[z] == x.id:
                                receiver = x
                                rsu_location = z
                                break
                        break
                if receiver.id == 0:
                    TravellingVehicle[j].informationPool[0].timestamp[1] += 1
                    continue

                tr = (TravellingVehicle[j].informationPool[0].size * 1000 / p.B) + Network.information_prop_delay()
                if TravellingVehicle[j].location <= rsu_location:
                    tl = (rsu_location - TravellingVehicle[j].location + TravellingVehicle[j].communication) / \
                         TravellingVehicle[j].speed
                else:
                    tl = (TravellingVehicle[j].communication - TravellingVehicle[j].location + rsu_location) / \
                         TravellingVehicle[j].speed

                if tr <= tl:
                    TravellingVehicle[j].informationPool[0].if_send = 1
                    TravellingVehicle[j].informationPool[0].timestamp[1] += Network.information_prop_delay() + tr
                    FI.execute_information(TravellingVehicle[j].informationPool[0], receiver)
                else:
                    TravellingVehicle[j].informationPool[0].timestamp[1] += random.randrange(1, 5)

                receiver = p.NODES[0]

    def drived(clock, TravellingVehicle):
        if TravellingVehicle is not None:  # 判断车辆是否驶离道路
            for i in TravellingVehicle[::-1]:
                if clock - i.time > p.Traveltime:
                    # print('*****************')
                    # print('id为', i.id, '的车辆在', clock, '时间点驶离道路', i.time, i.informationPool[0].timestamp[1])
                    # print('*****************')
                    TravellingVehicle.remove(i)

        # for m in range(len(p.NODES)):
        #     for n in range(len(p.NODES[m].transactionsPool)):
        #         print(p.NODES[m].id, p.NODES[m].transactionsPool[n].id, p.NODES[m].transactionsPool[n].timestamp)

# class main():
#     clock = 0
#     TravellingVehicle = []
#     while clock < p.simTime:
#         clock += 1
#         Travel.coming(clock, TravellingVehicle)
#         Travel.Travellling(clock, TravellingVehicle)
#         Travel.drived(clock, TravellingVehicle)
#
#     for m in range(len(p.NODES)):
#         for n in range(len(p.NODES[m].transactionsPool)):
#             print(p.NODES[m].id, p.NODES[m].transactionsPool[n].id, p.NODES[m].transactionsPool[n].timestamp)
