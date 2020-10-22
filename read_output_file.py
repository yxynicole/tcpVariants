# Project 3

# Node where the TCP traffic is originating from
TCP_SEND_NODE = "0"

# Calculates the number of dropped packets
# A dropped packet is a tcp or ack packet that begins with a "d" in the tracefile
def calculate_num_dropped_packets(trace_data):

    num_dropped_packets = 0

    for line in trace_data:
        if line[0] == "d" and ("tcp" in line or "ack" in line):
            num_dropped_packets += 1

    return num_dropped_packets

# Assumes TCP packet data portion is 1000 bytes for now
# Note: We can update this function to account for varying packet sizes if necessary
# num_seconds is the number of seconds the simulation is run for
# Returns average throughput in KB / seconds
def calculate_average_throughput(trace_data, num_seconds):

    packets_sent = 0

    for line in trace_data:
        parsed_line = line.split() #splits by whitespace
        if parsed_line[0] == "-" and parsed_line[2] == TCP_SEND_NODE and parsed_line[4] == "tcp":
            packets_sent += 1

    return packets_sent / 1000.00 / num_seconds

# Takes in a line from the tracefile and a node number and determines
# if the line is dequeing a TCP packet from the node
def is_outgoing_tcp_packet(line, send_node):
    return line[0] == "-" and line[2] == send_node and line[4] == "tcp"

# Take in a line from the tracefile, a node number, and sequence number
# and returns True if the line represents an ack back to that node for
# the specified sequence number, False otherwise
def is_tcp_ack(line, send_node, seq_num):
    return line[0] == "r" and line[3] == TCP_SEND_NODE and \
       line[4] == "ack" and line[10] == seq_num


# Takes in a full tracefile and calculates the average RTT for TCP packets
# originating from node 0 in Experiment 1
# Packets that are re-transmitted are not counted, as the acks will be
# ambiguous
def calculate_average_RTT(trace_data):

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
            if seq_num in round_trips.keys(): #retransmission, don't count in avg
                round_trips.pop(seq_num) #remove the seq_num from the list of successful RTTs
                retransmission_seq_num.append(seq_num)
                continue
            elif seq_num in retransmission_seq_num: # retransmission
                continue
            else:
                next_line_num = i + 1
                for j in range(next_line_num, len(trace_data)):
                    potential_ack_line = trace_data[j].split() # splits by whitespace
                    if is_tcp_ack(potential_ack_line, TCP_SEND_NODE, seq_num):
                        rec_ack_time = float(potential_ack_line[1])
                        round_trips[seq_num] = rec_ack_time - send_time
                        break

    return (sum(round_trips.values()) / len(round_trips))


if __name__ == '__main__':
    tracefile = open("out.tr", "r")
    trace_data = tracefile.readlines()
    print("Num items in line: " + str(len(trace_data[0].split())))

    num_dropped_packets = calculate_num_dropped_packets(trace_data)
    average_throughput = calculate_average_throughput(trace_data, 5)
    average_RTT = calculate_average_RTT(trace_data)
    tracefile.close()
    print("The number of dropped packets is: " + str(num_dropped_packets))
    print("The average throughput in KB/second is: " + str(average_throughput))
    print("The average RTT for TCP packets is: " + str(average_RTT))

