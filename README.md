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
 
example [configuration YAML]('workers/gpu1.yaml'): Note that the hasrate must be specdified in H/s and the command must have the full path if not in the `PATH` env variable

## Running

```
MY_WORKERS=path/to/yaml/config/folder mytinyrig -t 5
```

This command will start polling every 5 minutes to NiceHash.
The process starts the command specified in the config file mining the most profitable algo (according to specified hashrate in the config)


## TODO
  - Benckmark function
  - Implement waller as argument (tag replace in the command specified in the yaml conf)
  
  
## Other

Feel free to jump in and improve the project

To support you can point your tinyrig to `3Dsuk4X67SBwcFjVxrnCcoXn8jyowRqScw` for 5 minutes or so :).

