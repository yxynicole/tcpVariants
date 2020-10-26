# tcpVariants
Performance Analysis of TCP Variants 
## Xinyu done:
* pass in values like TCP variant, cbr bandwidth,etc., from command line to TCL.file
  * `ex1Perfo.tcl`, `ex2Fairness.tcl`, `ex3Queuing.tcl` are used to duplicate their template files(e.g.`ex1.template`) respectively. Each tcl generator(e.g. `ex1_tcl_generator.python`) replaces values within the template file with arguments passed from the command line by using format function in Python. 
  * But this method is so inconvenient since we need to type a lot of arguments in command line. So instead of parsing arguments from the command line,  I hard-coded arguments in `tcl_generator.py`. These arguments are fabricated. 
  * type 'python tcl_generator.py -e <ex3>', out.tr files are all saved into a `output` directory. 
## Xinyu todo:
- [ ] the random number aspect so the flows start at different times

## Jeff todo:
- [ ] review trace file analysis code to calculate drops, average bandwith, and round trip time for experiment 1
- [ ] review experiment 2 and 3 and determine what tweaks to will be need to tracefile analysis code
- [ ] time series plot of TCP to confirm it is conforming to expected pattern

## Not assigned yet todo:
- [ ] script to kickoff analysis of relevant files and to determine average across all simulations
- [ ] writing of actual paper sections
