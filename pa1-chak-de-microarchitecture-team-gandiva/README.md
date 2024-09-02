# CS683 2024 Assignment 1
> **Note:** {workspace}= "pa1-chak-de-microarchitecture-team-gandiva/"

### Team members
* Soumik Dutta (23m0826)
* Sm Arif Ali (23m0822)

### System details on which we are performing all the tests:

* Processor: Intel(R) Core(TM) i7-14650HX
* Hyper threading is turned off ( Script: {workspace}/scripts/hyper_thread_toggle.sh )
*  CPU frequency: 5.2 GHz
* Cache:
    * L1 D cache: 48 KB
        * Line size: 64 B
        * Associativity: 12
        * Number of sets: 64
    * L1 I cache: 32 KB
        * Line size: 64 B
        * Associativity: 8
        * Number of sets: 64
    * L2 cache: 2 MB
        * Line size: 64 B
        * Associativity: 16
        * Number of sets: 2048
    * L3 cache: 30 MB
        * Line size: 64 B
        * Associativity: 12
        * Number of sets: 40960


### Testing values:
 * Element size: 8 Bytes [ size of Double ] 
 * Max Tile size = 55x55 (i.e. $\sqrt((48*1024/2)/8)$) [ As $2B^2<C$ where $C= 48 KByte$ ] 
 * Tile sizes: [0,4,8,16,32,48,56,64]
 * Matrix sizes: [1000,3000,5000,10000,15000,20000]
 * Averaged over 5 rounds each

# Part 1:


 