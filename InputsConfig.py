class InputsConfig:
    """ Seclect the model to be simulated.
    0 : PoW
    1 : PoS
    2 : DPoS
    """
    model = 0

    ''' Input configurations for Bitcoin model '''
    if model == 0:
        ''' Block Parameters '''
        Binterval = 100  # Average time (in seconds)for creating a block in the blockchain 创建区块的平均间隔
        Bsize = 1  # The block size in MB 区块的大小
        Bdelay = 0.42  # average block propogation delay in seconds, 平均区块广播延迟 #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 12.5  # Reward for mining a block 挖出区块的奖励

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator 在模拟器中是否能够接受/不接受一笔交易
        Ttechnique = "Full"  # Full/Light to specify the way of modelling transactions
        Tn = 10  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tdelay = 5.1
        Tfee = 0.000062  # The average transaction fee
        Tsize = 0.000546  # The average transaction size  in MB
        B = 200  # kbps

        ''' Node Parameters '''
        Nn = 6  # the total number of nodes in the network
        NODES = []
        from Models.Bitcoin.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        NODES = [Node(id=0, hashPower=0), Node(id=1, hashPower=50), Node(
            id=2, hashPower=20), Node(id=3, hashPower=30), Node(id=4, hashPower=40),
                 Node(id=5, hashPower=60)]  # 定义每个节点的id和hash计算能力，在我们的模拟器中，节点分为车辆节点和RSU，还需要添加他们的通信范围属性
        # NODES = [Node(id=0, hashPower=0), Node(id=1, hashPower=50), Node(
        #     id=2, hashPower=20), Node(id=3, hashPower=30)]  # 定义每个节点的id和hash计算能力，在我们的模拟器中，节点分为车辆节点和RSU，还需要添加他们的通信范围属性

        '''Vehicle Parameters'''
        Vn = 100000
        VEHICLE = []
        from Models.Vehicle import LightVehicle
        VEHICLE = LightVehicle.create_vehicle(Vn)

        '''Road Parameters'''
        # 创建一个Road的对象数组
        Idelay = 0.2
        Road = [0] * 1000  # 从左向右行驶的车道
        length = len(Road)
        Traveltime = length // VEHICLE[0].speed
        Road[100] = NODES[1].id  # 设置RSU的位置
        Road[300] = NODES[2].id
        Road[500] = NODES[3].id
        Road[700] = NODES[4].id
        Road[900] = NODES[5].id

        ''' Simulation Parameters '''
        simTime = 10000  # the simulation length (in seconds)
        Runs = 1  # Number of simulation runs

    ''' Input configurations for Ethereum model '''
    if model == 1:
        ''' Block Parameters '''
        Binterval = 100  # Average time (in seconds)for creating a block in the blockchain 创建区块的平均间隔
        Bsize = 1  # The block size in MB 区块的大小
        Bdelay = 0.42  # average block propogation delay in seconds, 平均区块广播延迟 #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 12.5  # Reward for mining a block 挖出区块的奖励

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Full"  # Full/Light to specify the way of modelling transactions
        Tn = 20  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tdelay = 3
        # The transaction fee in Ethereum is calculated as: UsedGas X GasPrice
        Tsize = 0.000546  # The average transaction size  in MB
        Tfee = 0.000062  # The average transaction fee
        B = 200  # kbps

        ''' Drawing the values for gas related attributes (UsedGas and GasPrice, CPUTime) from fitted distributions '''

        ''' Uncles Parameters '''
        hasUncles = True  # boolean variable to indicate use of uncle mechansim or not
        Buncles = 2  # maximum number of uncle blocks allowed per block
        Ugenerations = 7  # the depth in which an uncle can be included in a block
        Ureward = 0
        UIreward = Breward / 32  # Reward for including an uncle

        ''' Node Parameters '''
        Nn = 6  # the total number of nodes in the network
        NODES = []
        from Models.PoS.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        NODES = [Node(id=0, stackPower=0), Node(id=1, stackPower=50), Node(
            id=2, stackPower=20), Node(id=3, stackPower=40), Node(id=4, stackPower=30),
                 Node(id=5, stackPower=60)]  # 定义每个节点的id和hash计算能力，在我们的模拟器中，节点分为车辆节点和RSU，还需要添加他们的通信范围属性

        '''Vehicle Parameters'''
        Vn = 100000
        VEHICLE = []
        from Models.Vehicle import LightVehicle
        VEHICLE = LightVehicle.create_vehicle(Vn)

        '''Road Parameters'''
        # 创建一个Road的对象数组
        Idelay = 0.5  # 消息广播的延迟，需要查找文献以设置具体值
        Road = [0] * 1000  # 从左向右行驶的车道
        length = len(Road)
        Traveltime = length // VEHICLE[0].speed
        Road[100] = NODES[1].id  # 设置RSU的位置
        Road[300] = NODES[2].id
        Road[500] = NODES[3].id
        Road[700] = NODES[4].id
        Road[900] = NODES[5].id

        ''' Simulation Parameters '''
        simTime = 10000  # the simulation length (in seconds)
        Runs = 1  # Number of simulation runs

    if model == 2:
        ''' Block Parameters '''
        Binterval = 100  # Average time (in seconds)for creating a block in the blockchain 创建区块的平均间隔
        Bsize = 1  # The block size in MB 区块的大小
        Bdelay = 0.42  # average block propogation delay in seconds, 平均区块广播延迟 #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 12.5  # Reward for mining a block 挖出区块的奖励

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator 在模拟器中是否能够接受/不接受一笔交易
        Ttechnique = "Full"  # Full/Light to specify the way of modelling transactions
        Tn = 10  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tdelay = 5.1
        Tfee = 0.000062  # The average transaction fee
        Tsize = 0.000546  # The average transaction size  in MB
        B = 200  # kbps

        ''' Node Parameters '''
        Nn = 6  # the total number of nodes in the network
        NODES = []
        from Models.Bitcoin.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        NODES = [Node(id=0, hashPower=0), Node(id=1, hashPower=50), Node(
            id=2, hashPower=20), Node(id=3, hashPower=40), Node(id=4, hashPower=30),
                 Node(id=5, hashPower=60)]  # 定义每个节点的id和hash计算能力，在我们的模拟器中，节点分为车辆节点和RSU，还需要添加他们的通信范围属性
        # NODES = [Node(id=0, hashPower=0), Node(id=1, hashPower=50), Node(
        #     id=2, hashPower=20), Node(id=3, hashPower=30)]  # 定义每个节点的id和hash计算能力，在我们的模拟器中，节点分为车辆节点和RSU，还需要添加他们的通信范围属性
        Rtime = 500  # 表示一轮选举的有效时间
        leader_num = (Nn - 1) * 2 // 3

        '''Vehicle Parameters'''
        Vn = 100000
        VEHICLE = []
        from Models.Vehicle import LightVehicle
        VEHICLE = LightVehicle.create_vehicle(Vn)

        '''Road Parameters'''
        # 创建一个Road的对象数组
        Idelay = 0.5  # 消息广播的延迟，需要查找文献以设置具体值
        Road = [0] * 1000  # 从左向右行驶的车道
        length = len(Road)
        Traveltime = length // VEHICLE[0].speed
        Road[100] = NODES[1].id  # 设置RSU的位置
        Road[300] = NODES[2].id
        Road[500] = NODES[3].id
        Road[700] = NODES[4].id
        Road[900] = NODES[5].id

        ''' Simulation Parameters '''
        simTime = 10000  # the simulation length (in seconds)
        Runs = 1  # Number of simulation runs