<p align="center">
  <h1 align="center"> ChampSim </h1>
  <p> ChampSim is a trace-based simulator for a microarchitecture study. You find the required trace files at (https://drive.google.com/drive/folders/1JmFmXRZ1A517KtmiZvpBwobfb79dk_GM?usp=sharing) <p>
</p>

## Tested Environment & Dependencies

- Ubuntu 18.04.6 LTS and above
- Linux Kernel 5.4.0 and above
- GCC 7.5.0
  
# Add your own data prefetchers and TLB prefetcher

**Copy the respective template**
```
$ cp prefetcher/asp.cc prefetcher/asp.stlb_pref
$ cp prefetcher/ip_stride.cc prefetcher/ip_stride.l1d_pref
$ cp prefetcher/complex_stride.cc prefetcher/complex_stride.l1d_pref
$ cp prefetcher/next_line.cc prefetcher/next_line.l1d_pref
$ cp prefetcher/optimized.cc prefetcher/optimized.l1d_pref
```

# Compile

To makes things simper, you are only required to specify three parameters: L1D prefetcher, STLB prefetcher, and the number of cores. 
For example, `./build_champsim.sh no no 1` builds a single-core processor with no L1 data prefetcher or STLB prefetcher.
```
$ ./build_champsim.sh ip_stride asp 1

$ ./build_champsim.sh ${L1D_PREFETCHER} ${STLB_PREFETCHER} ${NUM_CORE}
```

In case you need to modify the L2C/LLC prefetchers, you can manually change it in `./build_champsim.sh`

# Run simulation

**Single-core simulation**
```
./[BINARY] -warmup_instructions [N_WARM] -simulation_instructions [N_SIM] [TRACE_DIR]/[TRACE]
$ ./ip_stride-asp-1core -warmup_instructions 25000000 -simulation_instructions 25000000 ../traces/trace1.champsimtrace.xz

${BINARY}: ChampSim binary compiled by "build_champsim.sh" (ip_stride-asp-1core)
${N_WARM}: number of instructions for warmup (25 million)
${N_SIM}:  number of instructinos for detailed simulation (25 million)
${TRACE_DIR}: directory where the trace is located (../traces/)
${TRACE}: trace name (trace1.champsimtrace.xz)
```

# Evaluate Simulations

ChampSim measures the IPC (Instruction Per Cycle) value as a performance metric. <br>
There are some other useful metrics printed out at the end of simulation. <be>


## Steps to download gc version 7 in ubuntu:
1. Sudo apt update
2. sudo add-apt-repository Ra.buntu-t@olchain-g/test
3. vim /etc/apt/sources list
4. sude nano /etc/apt/sources list
5. Update the last line with deb (arch=amd64] http://archive.ubuntu.com/ubuntu focal main universe
6. sudo add-apt-repository ppa:ubuntu-toolchain-r/test
7. sudo apt-get install gcc-7
8. sudo apt-get install g++-7
9. sudo update-alternatives -install /usr/bin/g++ g++ /usr/bin/g++-7 0
10. sudo update-alternatives -install /us/bin/gce gc /ust/bin/gcc-7 0
    
--In case the GCC and G++ is already present in /us/bin(run /gcc-7 -v in /us/bin) installed and alternative is set then run

1. sudo update-alternatives -config g++
2. sudo update-alternatives --config gcc
