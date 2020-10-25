#Create a simulator object
set ns [new Simulator]

#Open the trace file
set tf [open ex3_output.tr w]
$ns trace-all $tf

#Define a 'finish' procedure
proc finish {} {
	global ns tf 
	$ns flush-trace 
	#close the trace file
	close $tf
	exit 0
}

#Create independent variables
set queue_algor "RED"
set tcp_variant ""
set cbr_rate 0
set cbr_start_time 0
set cbr_stop_time 5
set tcp_0_3_start_time 0
set tcp_0_3_stop_time 5

#Create six nodes 
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

#Create links between the nodes 
$ns duplex-link $n0 $n1 10Mb 10ms $queue_algor
$ns duplex-link $n1 $n2 10Mb 10ms $queue_algor
$ns duplex-link $n1 $n4 10Mb 10ms $queue_algor
$ns duplex-link $n5 $n2 10Mb 10ms $queue_algor
$ns duplex-link $n2 $n3 10Mb 10ms $queue_algor

#Set Queue Size of link (n2-n3) to 10 
#$ns queue-limit $n2 $n3 10

#Setup a UDP connection between n4 and n5
set udp [new Agent/UDP]
$ns attach-agent $n4 $udp
set null [new Agent/Null]
$ns attach-agent $n5 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate cbr_rate
$cbr set random_ false

#Setup a TCP connection between n0 and n3
set tcp_0_3 [new Agent/TCP]
$tcp_0_3 set class_ 2
$ns attach-agent $n0 $tcp_0_3
set sink [new Agent/TCPSink]
$ns attach-agent $n3 $sink
$ns connect $tcp_0_3 $sink
$tcp_0_3 set fid_ 1

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp_0_3
$ftp set type_ FTP

#Schedule events for the CBR and FTP agents
$ns at cbr_start_time "$cbr start"
$ns at tcp_0_3_start_time "$ftp start"
$ns at tcp_0_3_stop_time "$ftp stop"
$ns at cbr_stop_time "$cbr stop"


#Call the finish procedure after 5 seconds of simulation time
$ns at 5.0 "finish"

#Run the simulation
$ns run
