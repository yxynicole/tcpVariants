#!/usr/bin/env python
# Project 3: 
# This program modifies argumetns in TCL script based on argument parsed from cmd-line  
import argparse
import os 

# experiment_num=1

def main(cmd_line_args):
    # open and read experiment2 templete
    template = open('ex3.template').read()
    
    # replace argumetns in the templete with parsed arguments from cod-line
    script_content = template.format(
        tcp_variant=cmd_line_args.tcp_variant, 
        cbr_rate=cmd_line_args.cbr_rate, 
        cbr_start_time=cmd_line_args.cbr_start_time,
        cbr_stop_time=cmd_line_args.cbr_stop_time,
        tcp_0_3_start_time=cmd_line_args.tcp_0_3_start_time,
        tcp_0_3_stop_time=cmd_line_args.tcp_0_3_stop_time,
        queue_algor=cmd_line_args.queue_algor
    )

    open("ex3.tcl", "w").write(script_content)
    #os.system("ns ex2.tcl")

if __name__ == '__main__':
    # parse arguments from cmd-line
    parser = argparse.ArgumentParser()
    # parser.add_argument('experiment_num')
    parser.add_argument('--tcp_variant', type=str, default='Agent/TCP')
    parser.add_argument('--cbr_rate', type=int)
    parser.add_argument('--cbr_start_time', type=int, default=0)
    parser.add_argument('--cbr_stop_time', type=int, default=10)
    parser.add_argument('--tcp_0_3_start_time', type=int, default=0)
    parser.add_argument('--tcp_0_3_stop_time', type=int, default=10)
    parser.add_argument('--queue_algor', type=str, default="DropTail")

    cmd_line_args = parser.parse_args()
    main(cmd_line_args)
