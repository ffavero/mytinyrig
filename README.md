# mytinyrig

Very simple way to switch to the most profitable NiceHash algorithm
Python should be platform independente, I've only tested the in OSX and Linux.

## install

```
git clone https://github.com/ffavero/mytinyrig
cd mytinyrig
python setup.py install
```

## Configuration

Prepare your own yaml file configurations.
Each yaml configuration file in a scpecified folder will start a worker.
You can have a file for nvidia GPUs, one for AMD GPUs (if you have a mixed card rig) and one for the CPU (if you are greedy as me and you want the 0.03 mBTC/day more).
Or you can have a file for each of your card if your card have different yield in different algo (mind to configure the `command` in the configuration to select the specific card)

example [configuration YAML](https://github.com/ffavero/mytinyrig/blob/master/mytinyrig/workers/gpu1.yaml): Note that the hasrate must be specdified in H/s and the command must have the full path if not in the `PATH` env variable

## Running

```
MY_WORKERS=path/to/yaml/config/folder mytinyrig -t 5 -w <NH_WALLET>
```

or if you don't like setting environment variables

```
mytinyrig -t 5 -w <NH_WALLET> -c path/to/yaml/config/folder
```

This command will start polling every 5 minutes to NiceHash.
The process starts the command specified in the config file mining the most profitable algo (according to specified hashrate in the config)


### Arguments

```
mytinyrig -h
usage: mytinyrig [-h] [-d] [-w WALLET] [-r {eu,usa,hk,jp,in,br}]
                   [-t POLTIME] [-n N_AVG] [-l LOGDIR] [-c CONFDIR]

optional arguments:
  -h, --help            show this help message and exit
  -d, --dump            Print an empty yaml worker file
  -w WALLET, --wallet WALLET
                        Nicehash wallet address
  -r {eu,usa,hk,jp,in,br}, --region {eu,usa,hk,jp,in,br}
                        Nicehash servers region
  -t POLTIME, --time POLTIME
                        Polling time in minutes
  -n N_AVG, --n-mean N_AVG
                        Number of polls saved to compute the mean
                        profitability
  -l LOGDIR, --logdir LOGDIR
                        Logs output folder
  -c CONFDIR, --confdir CONFDIR
                        Folder containing the workers yaml configurations
```

## TODO
  - Benckmark function


## Other

Feel free to jump in and improve the project

To support you can point your tinyrig to `3Dsuk4X67SBwcFjVxrnCcoXn8jyowRqScw` for 5 minutes or so :).
