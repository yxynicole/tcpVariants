#!/usr/bin/env python
import argparse
import os 

CBR_RATES = [1,2,3,4,5]
TCPS = {'tcp':'Agent/TCP'}


EXPERIMENTS = {
    'ex1':{
        'template':'ex1.template',
        'parameters':[
            'cbr_start_time', 'cbr_stop_time',
            'tcp_0_3_start_time', 'tcp_0_3_stop_time',
        ],
        'simulations': [
            [2,0,0,10],
            [2,2,2,10],
            [2,4,4,10],
            [2,0,0,6],
            [2,0,4,8],
            [2,2,6,6],
            [2,2,4,8],
            [2,0,0,2],
            [2,4,0,8],
            [2,4,6,8],
        ]
    },
    'ex2':{
        'template':'ex2.template',
        'parameters':[
            'cbr_start_time', 'cbr_stop_time',
            'tcp_0_3_start_time', 'tcp_0_3_stop_time',
            'tcp_4_5_start_time', 'tcp_4_5_stop_time',
        ],
        'simulations':[
            [2,0,0,10,10,2],
            [2,2,2,10,10,2],
            [2,4,4,10,10,2],
            [2,0,0,6,10,2],
            [2,0,4,8,10,2],
            [2,2,6,6,10,2],
            [2,2,4,8,10,2],
            [2,0,0,2,10,2],
            [2,4,0,8,10,2],
            [2,4,6,8,10,2],
        ]
    },
    'ex3':{
        'template':'ex3.template',
        'parameters':[
            'cbr_start_time', 'cbr_stop_time',
            'tcp_0_3_start_time', 'tcp_0_3_stop_time',
            'queue_algor'
        ],
        'simulations':[
            [2,0,0,10,'RAD'],
            [2,2,2,10,'DropTail'],
            [2,4,4,10,'RAD'],
            [2,0,0,6,'DropTail'],
            [2,0,4,8,'RAD'],
            [2,2,6,6,'DropTail'],
            [2,2,4,8,'RAD'],
            [2,0,0,2,'DropTail'],
            [2,4,0,8,'RAD'],
            [2,4,6,8,'DropTail'],
        ]
    }
}

def write_to(file, conent):
    f = open(file, 'w')
    f.write(conent)
    f.close()

def main(args):
    experiment = EXPERIMENTS[args.experiment]
    
    template = open(experiment['template']).read()
    parameters = experiment['parameters']
    simulations = experiment['simulations']

    os.system('mkdir -p output')

    for i, simulation in enumerate(simulations):
        format_args = dict(zip(parameters, simulation))
        for cbr_rate in CBR_RATES:
            for name, variant in TCPS.items():
                format_args['tcp_variant'] = variant
                format_args['cbr_rate'] = cbr_rate
                format_args['output_file'] = 'output/{}_{}_cbr{}_{}.tr'.format(args.experiment, name, cbr_rate, i)
                script_content = template.format(**format_args)
                write_to('{}.tcl'.format(args.experiment), script_content)
                os.system('ns {}.tcl'.format(args.experiment))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--experiment','-e', required=True)

    args = parser.parse_args()

    main(args)