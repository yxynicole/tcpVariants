# Project 3 - CS5700
https://david.choffnes.com/classes/cs4700fa20/project3.php
The original design of the Transmission Control Protocol (TCP) worked reliably, but was unable to provide acceptable performance in large and congested networks. Several TCP variants have been proposed since then (TCP Tahoe, Reno, NewReno, Vegas, BIC, CUBIC, SACK, and others) with mechanisms to control and avoid congestion. The objective of this project is for you to analyze the performance of these different TCP variants. You will use the NS-2 network simulator to perform experiments that will help you understand the behavior of the TCP variants under various load conditions and queuing algorithms.

## Code:
Template tcl files and a script called tcl_generator that creates and runs multiple simulations at once, plugging in specified parameters into the simulations

- Jeff wrote the original ex.1 template file and the template. 
- Jeff: Analyze_trace_file_create.csv.py analyzes multiple .tr files in a directory and code to calculates average throughput, RTT, and packet drop rate for each file
- Jeff: Parse_throughput_bytime.py creates a csv timeseries from a .tr file, time vs. average throughput
- Xinyu wrote ex_2 template, ex3_template, and the tcl_generator.py file

## Code to create graphs:
Xinyu - ex1_plot.ipynb
Ex2 and 3 Graphs created in Excel - Jeff

## Paper:
Xinyu worked on Experiment 1, Jeff worked on Experiment 2 and 3. 
