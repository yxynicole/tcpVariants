#!/usr/bin/env python
import argparse
import os 

CBR_RATES = [1,2,3,4,5,6,7,8,9]

EXPERIMENTS = {
    'ex1':{
        'template':'ex1.template',
        'parameters':[
            'cbr_start_time', 'cbr_stop_time',
            'tcp_0_3_start_time', 'tcp_0_3_stop_time',
        ],
        'simulations': [
            [0,12,0,12],
            [1,12,1,12],
            [2,12,2,12],
            [0,12,1,12],
            [0,12,2,12],
            [0,12,3,12],
            [0,12,3.5,12],
            [.25,12,0,12],
            [.5,12,0,12],
            [1,12,0,12],
            [1.5,12,0,12],
        ],
        'variants':{
            'tahoe': {'tcp_variant': 'Agent/TCP'},
            'reno': {'tcp_variant': 'Agent/TCP/Reno'},
            'newreno': {'tcp_variant': 'Agent/TCP/Newreno'},
            'vegas': {'tcp_variant': 'Agent/TCP/Vegas'},
        }
    },
    'ex2':{
        'template':'ex2.template',
        'parameters':[
            'cbr_start_time', 'cbr_stop_time',
            'tcp_0_3_start_time', 'tcp_0_3_stop_time',
            'tcp_4_5_start_time', 'tcp_4_5_stop_time',
        ],
        'simulations':[
            [0,12,0,12,0,12],
            [0,12,0.5,12,0,12],
            [0,12,1.5,12,0,12],
            [0,12,1,12,1.5,12],
            [0,12,1,12,2,12],
            [0,12,0,12,.5,12],
            [0,12,0,12,1,12],
            [0,12,1.5,12,1,12],
            [0,12,2,12,1,12],
            [0,12,3,12,1,12],
        ],
        'variants':{
            'reno-reno': {'tcp_variant1':'Agent/TCP/Reno', 'tcp_variant2':'Agent/TCP/Reno'},
            'newreno-reno': {'tcp_variant1':'Agent/TCP/Newreno', 'tcp_variant2':'Agent/TCP/Reno'},
            'vegas-vegas': {'tcp_variant1':'Agent/TCP/Vegas', 'tcp_variant2':'Agent/TCP/Vegas'},
            'newreno-vegas': {'tcp_variant1':'Agent/TCP/Newreno', 'tcp_variant2':'Agent/TCP/Vegas'},
        }
    },
    'ex3':{
        'template':'ex3.template',
        'parameters':[
            'cbr_start_time', 'cbr_stop_time',
            'tcp_0_3_start_time', 'tcp_0_3_stop_time',
            'queue_algor'
        ],
        'simulations':[
            [.5,12,0,12,'RED'],
            [.5,12,0,12,'DropTail'],
            [.75,12,0,12,'RED'],
            [.75,12,0,12,'DropTail'],
        ],
        'variants':{
            'sack': {'tcp_variant': 'Agent/TCP/Sack1'},
            'reno': {'tcp_variant': 'Agent/TCP/Reno'},
        }
    }
}

def write_to(file, content):
    f = open(file, 'w')
    f.write(content)
    f.close()

def main(args):
    experiment = EXPERIMENTS[args.experiment]
    
    template = open(experiment['template']).read()
    parameters = experiment['parameters']
    simulations = experiment['simulations']

    os.system('mkdir -p output')
    # get index and simulation(array) at the same time
    for i, simulation in enumerate(simulations):
        format_args = dict(zip(parameters, simulation)) # format_args = {cbr_start_time:2, cbr_stop_time:0, ...}
        for cbr_rate in CBR_RATES:
            for name, variant in experiment['variants'].items(): # add tcp variant, cbr rate, outputfile into format_args
                format_args.update(variant)
                format_args['cbr_rate'] = cbr_rate
                format_args['output_file'] = 'output/{}_{}_cbr{}_simulation{}.tr'.format(args.experiment, name, cbr_rate, i)
                script_content = template.format(**format_args) # unpack arguments as key-value pairs 
                write_to('{}.tcl'.format(args.experiment), script_content)
                os.system('ns {}.tcl'.format(args.experiment))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
  
    parser.add_argument('--experiment','-e',choices=['ex1','ex2','ex3'], required=True)

    args = parser.parse_args()

    main(args)
