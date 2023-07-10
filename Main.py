from InputsConfig import InputsConfig as p
from Event import Event, Queue
from Scheduler import Scheduler
from Statistics import Statistics
from Travel import Travel
import math
from decimal import Decimal

if p.model == 2:
    from Models.DPoS.BlockCommit import BlockCommit
    from Models.DPoS.Consensus import Consensus
    from Models.DPoS.Node import Node
    from Models.Incentives import Incentives

elif p.model == 1:
    from Models.PoS.BlockCommit import BlockCommit
    from Models.PoS.Consensus import Consensus
    from Models.PoS.Node import Node
    from Models.PoS.Incentives import Incentives

elif p.model == 0:
    from Models.Bitcoin.BlockCommit import BlockCommit
    from Models.Bitcoin.Consensus import Consensus
    from Models.Bitcoin.Node import Node
    from Models.Incentives import Incentives


############################################ Start Simulation ############################################


def main():
    for i in range(p.Runs):
        clock = 0  # set clock to 0 at the start of the simulation

        Node.generate_gensis_block()  # generate the gensis block for all miners

        if p.model == 2:
            current_block_producer = Consensus.Protocol()
            BlockCommit.generate_initial_events(current_block_producer)
        else:
            BlockCommit.generate_initial_events()

        travelling_vehicle = []
        count = 1
        while clock <= p.simTime:
            clock += 1
            Travel.coming(clock, travelling_vehicle)
            Travel.Travellling(clock, travelling_vehicle)
            Travel.drived(clock, travelling_vehicle)

            if p.model == 2:
                if clock % p.Rtime == 0:
                    count = 1
                    current_block_producer = Consensus.Protocol()

                if Queue.isEmpty() == 0:
                    for j in range(len(Queue.event_list)):
                        next_event = Queue.get_next_event()
                        if clock == Decimal(next_event.time).quantize(Decimal("1."), rounding="ROUND_HALF_UP"):
                            if count == 4:
                                count = 1
                            BlockCommit.handle_event(next_event, current_block_producer, count)
                            # print(count)
                            count += 1

                            Queue.remove_event(next_event)
                        j += 1
            else:
                if Queue.isEmpty() == 0:
                    for j in range(len(Queue.event_list)):
                        next_event = Queue.get_next_event()
                        if clock == Decimal(next_event.time).quantize(Decimal("1."), rounding="ROUND_HALF_UP"):
                            BlockCommit.handle_event(next_event)
                            Queue.remove_event(next_event)
                        j += 1
        # currentTime = 0
        # while not Queue.isEmpty() and currentTime <= p.simTime:
        #     next_event = Queue.get_next_event()
        #     # print(next_event.type, next_event.node, next_event.time)
        #     currentTime = next_event.time  # move clock to the time of the event
        #     BlockCommit.handle_event(next_event)
        #     Queue.remove_event(next_event)

        # print('---------')
        # for i in p.VEHICLE:
        #     print(i.id, i.time)
        # print('------------------')
        # for m in range(len(p.NODES)):
        #     for n in range(len(p.NODES[m].transactionsPool)):
        #         print(p.NODES[m].id, p.NODES[m].transactionsPool[n].size, p.NODES[m].transactionsPool[n].timestamp)
        #         count += 1
        # print('------------------')
        # count =0
        # for i in range(len(p.NODES)):
        #     # print('------------------')
        #     for j in range(len(p.NODES[i].blockchain)):
        #         # print(p.NODES[i].blockchain[j].id, p.NODES[i].blockchain[j].miner, p.NODES[i].blockchain[j].timestamp)
        #     # print('------------------')
        #         count += 1
        # print(count)
        # print('------------------')

        # for the AppendableBlock process transactions and
        # optionally verify the model implementation

        Consensus.fork_resolution()  # apply the longest chain to resolve the forks
        if p.model == 1:
            # distribute the rewards between the particiapting nodes
            Incentives.distribute_uncle_rewards()
        else:
            Incentives.distribute_rewards()
        # calculate the simulation results (e.g., block statstics and miners' rewards)
        Statistics.calculate()

        print(Statistics.trans, Statistics.latency, Statistics.block_used_rate)

        if p.model == 3:
            Statistics.print_to_excel(i, True)
            Statistics.reset()
        else:
            ########## reset all global variable before the next run #############
            Statistics.reset()  # reset all variables used to calculate the results
            Node.resetState()  # reset all the states (blockchains) for all nodes in the network
            fname = "(Allverify)1day_{0}M_{1}K.xlsx".format(
                p.Bsize / 1000000, p.Tn / 1000)
            # print all the simulation results in an excel file
            Statistics.print_to_excel(fname)
        fname = "(Allverify)1day_{0}M_{1}K.xlsx".format(
            p.Bsize / 1000000, p.Tn / 1000)
        # print all the simulation results in an excel file
        Statistics.print_to_excel(fname)
        Statistics.reset2()  # reset profit results


######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
