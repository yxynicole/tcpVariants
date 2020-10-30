# Project 3

# Node where the TCP traffic is originating from
TCP_SEND_NODE = "0"

# Calculates packet drop rate
# A dropped packet is a tcp or ack packet that begins with a "d" in the tracefile
# Packet drop rate = num_dropped_packets / num_outgoing_tcp_packets
def calculate_packet_drop_rate(trace_data):

    num_dropped_packets = 0.0
    num_outgoing_tcp_packets = 0.0

    for line in trace_data:
        parsed_line = line.split() #splits by whitespace
        if is_dropped_packet(parsed_line):
            num_dropped_packets += 1
        elif is_outgoing_tcp_packet(parsed_line, TCP_SEND_NODE):
            num_outgoing_tcp_packets += 1

    return num_dropped_packets / num_outgoing_tcp_packets

# Assumes TCP packet data portion is 1000 bytes for now
# Note: We can update this function to account for varying packet sizes if necessary
# num_seconds is the number of seconds the simulation is run for
# Returns average throughput in Megabits / seconds
def calculate_average_throughput(trace_data, num_seconds):

    packets_received = 0

    for line in trace_data:
        parsed_line = line.split() #splits by whitespace
        if parsed_line[0] == "r" and parsed_line[3] == "3" and parsed_line[4] == "tcp":
            packets_received += 1

    print(str(packets_received))
    #Assumes each tcp packet has 1000 bytes of data
    return packets_received * 8 / 1000 / num_seconds

# Determines if the line is a dropped tcp (including ack) packets
# Returns True if yes, False otherwise
def is_dropped_packet(line):
    return line[0] == "d" and ("tcp" in line or "ack" in line)


# Takes in a line from the tracefile and a node number and determines
# if the line is dequeing a TCP packet from the node. Returns True if yes,
# False otherwise
def is_outgoing_tcp_packet(line, send_node):
    return line[0] == "-" and line[2] == send_node and line[4] == "tcp"

# Take in a line from the tracefile, a node number, and sequence number
# and returns True if the line represents an ack back to that node for
# the specified sequence number, False otherwise
def is_tcp_ack(line, send_node):
    return line[0] == "r" and line[3] == TCP_SEND_NODE and \
       line[4] == "ack"


# Takes in a full tracefile and calculates the average RTT for TCP packets
# originating from node 0 in Experiment 1
# Packets that are re-transmitted are not counted, as the acks will be
# ambiguous
def calculate_average_RTT(trace_data):

    # Dictionary of tcp waiting to pair
    # {seq_num, time sent in seconds}
    waiting_to_pair = {}

    # Dictionary to store successful round trips
    # {Key, Value}
    # {string, int}
    # {Sequence number of outgoing TCP packet, RTT}
    round_trips = {}

    # Stores sequence numbers associated with re-transmitted TCP packets_sent
    # Re-transimitted TCP packets should not be included in the RTT average_RTT
    # because these packets will be ambigious
    retransmission_seq_num = []

    send_time = 0 # will be updated below
    rec_ack_time = 0 # will be updated below

    for i in range (len(trace_data)):
        parsed_line = trace_data[i].split() # splits by whitespace
        if is_outgoing_tcp_packet(parsed_line, TCP_SEND_NODE):
            send_time = float(parsed_line[1])
            seq_num = parsed_line[10]
            if seq_num in waiting_to_pair.keys() or seq_num in round_trips.keys():
                retransmission_seq_num.append(seq_num)
            elif seq_num in retransmission_seq_num: # retransmission
                continue
            else:
                waiting_to_pair[seq_num] = send_time
                continue

        elif is_tcp_ack(parsed_line, TCP_SEND_NODE):
            seq_num_rec = parsed_line[10]
            rec_ack_time = float(parsed_line[1])
            round_trips[seq_num_rec] = rec_ack_time - waiting_to_pair[seq_num_rec]

    keyList = round_trips.keys()

    for key in keyList:
        if key in retransmission_seq_num:
            round_trips.pop(key)

    return (sum(round_trips.values()) / len(round_trips))


if __name__ == '__main__':
    tracefile = open("out.tr", "r")
    trace_data = tracefile.readlines()
    print("Num items in line: " + str(len(trace_data[0].split())))

    packet_drop_rate = calculate_packet_drop_rate(trace_data)
    average_throughput = calculate_average_throughput(trace_data, 12.0)
    average_RTT = calculate_average_RTT(trace_data)
    tracefile.close()
    print("The packet drop rate is: " + str(packet_drop_rate))
    print("The average throughput in megabits per second is " + str(average_throughput))
    print("The average RTT for TCP packets in seconds is: " + str(average_RTT))
