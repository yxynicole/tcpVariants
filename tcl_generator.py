#!/usr/bin/env python
import argparse
import os 

CBR_RATES = ['1mb','2mb','3mb','4mb','5mb']

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
            'tahoe':'Agent/TCP',
            'reno':'Agent/TCP/Reno',
            'newreno':'Agent/TCP/Newreno',
            'vegas':'Agent/TCP/Vegas'
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
            [0,10,0,12,0,10],
            [0,10,0.5,10,0,10],
            [0,10,1.5,10,0,10],
            [0,10,1,10,1.5,10],
            [0,10,1,10,2,10],
            [0,10,0,10,1,10],
            [0,10,0,10,1.5,10],
            [0,10,1.5,10,1,10],
            [0,10,2,10,1,10],
            [0,10,3,10,1,10],
        ],
       'variants':{
            'Reno_Reno':['Agent/TCP/Reno', 'Agent/TCP/Reno'],
            'NewReno_Reno':['Agent/TCP/Newreno', 'Agent/TCP/Reno'],
            'Vegas_Vegas':['Agent/TCP/Vegas', 'Agent/TCP/Vegas'],
            'NewReno_Vegas':['Agent/TCP/Newreno', 'Agent/TCP/Vegas'],
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
            'sack':'Agent/TCP/Sack1',
            'reno':'Agent/TCP/Reno',
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
                format_args['tcp_variant1'] = variant[0]
                format_args['tcp_variant2'] = variant[1]
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
