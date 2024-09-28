<p align="center">
  <h1 align="center"> pa2-lehra-do-prefetcher-team-gandiva </h1>

### Task 1: Implementing the Arbitrary Stride Prefetcher

## **Walkthrough of the Implementation**

The objective of this implementation was to develop an **Arbitrary Stride Prefetcher (ASP)** for the **Shared Translation Lookaside Buffer (STLB)**. Below is a detailed walkthrough of the implementation process:

### 1. **Defining the IP Tracker Class**

The ASP makes use of a class named `IP_TRACKER` to maintain records for each unique instruction pointer (IP). The class is defined with the following attributes:

- `ip`: Stores the instruction pointer value.
- `last_addr`: Holds the most recent address accessed by this IP.
- `last_stride`: Stores the stride calculated as the difference between consecutive addresses.
- `state`: Represents the state of the tracker in the stride prediction state machine.
- `access_time`: Keeps track of the last access time, used for the **Least Recently Used (LRU)** replacement policy.

This class is instantiated for each of the IPs tracked by the prefetcher, and a total of 64 such trackers are maintained.

### 2. **Prefetching Logic in the `stlb_prefetcher_operate()` Function**

The core logic is handled within the `stlb_prefetcher_operate()` function, which performs the following steps for each address accessed:

1. **Identify or Allocate IP Tracker**:
   - Search for the IP in the existing tracker table.
   - If the IP is not found and all trackers are in use, apply an **LRU replacement** to replace the least recently accessed tracker.
   - Initialize the tracker fields: `ip`, `last_addr`, `last_stride`, and set `state` to `INITIAL`.

2. **Calculate the Stride**:
   - Compute the stride as the difference between the current and previous address.

3. **State Machine Logic**:
   - The stride consistency is monitored through a state machine with four states:
     - **INITIAL**: The first reference; initializes the stride pattern.
     - **TRANSIENT**: If the stride pattern changes, temporarily mark as inconsistent.
     - **STEADY**: If the same stride is observed consecutively, mark the pattern as stable.
     - **NOPRED**: No reliable prediction; monitor until consistent strides are observed.

    - **Figure 1: State machine implemented:**

<p align="center">
  <img src="state machine.png" alt="State machine" style="width:60%;"/>
</p>

1. **Prefetching**:
   - Prefetching is initiated only if the stride pattern is in the `STEADY` state.
   - The number of prefetches is determined by a parameter called `PREFETCH_DEGREE`.
   - For each calculated prefetch address, the `prefetch_translation()` function is called to prefetch the addresses into the STLB.

### 3. **Final Statistics Collection**

The `stlb_prefetcher_final_stats()` function outputs a summary of the prefetcher's performance. It reports the final prefetch degree and any other relevant statistics.

## **Building and Running the Prefetcher**

### **Build Command**

To build the prefetcher with the required configuration:

```bash
./build_champsim.sh no asp 1
```

This command specifies:

- `no`: No additional optimizations or configurations.
- `asp`: The Arbitrary Stride Prefetcher for the STLB.
- `1`: Number of CPU cores to use.

### **Run Command**

To execute the binary with the appropriate parameters:

```bash
./bin/no-asp-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces given/traces/trace1.champsimtrace.xz > output/task1/no-asp-1core_degree_8.log
```

This command runs the simulator with:

- **Warmup Instructions**: 25,000,000
- **Simulation Instructions**: 25,000,000
- **Trace File**: `trace1.champsimtrace.xz`
- **Output Log**: Stores the results in `output/task1/no-asp-1core_degree_8.log`

## **Experimental Results**

### 1. **Speedup Analysis**

The speedup is calculated as:

Speedup = (IPC of Prefetcher) / (IPC of Baseline without Prefetching)

We varied the **Prefetch Degree** from 2 to 10 and observed the effect on IPC. The following graph depicts the **Speedup vs. Prefetch Degree**.

**Table 1: STLB Speedup Comparison**

| Prefetch Degree | ASP Prefetcher Speedup |
|-----------------|----------------------- |
| 2               |  [ASP Value]           |
| 4               |  [ASP Value]           |
| 6               |  [ASP Value]           |
| 8               |  [ASP Value]           |
| 10              |  [ASP Value]           |

**Figure 2: Speedup vs. Prefetch Degree**
<p align="center">
  <img src="dummy_graph_speedup.png" alt="Speedup Graph" style="width:60%;"/>
</p>

### 2. **STLB MPKI Analysis**

STLB MPKI (Misses Per Kilo Instructions) was calculated for different Prefetch Degrees and compared with the baseline where no prefetching was used. The results are summarized in the table below:

**Table 2: STLB MPKI Comparison**

| Prefetch Degree | Baseline (No Prefetching) | ASP Prefetcher MPKI |
|-----------------|-------------------------- |---------------------|
| 2               | [Baseline Value]          | [ASP Value]         |
| 4               | [Baseline Value]          | [ASP Value]         |
| 6               | [Baseline Value]          | [ASP Value]         |
| 8               | [Baseline Value]          | [ASP Value]         |
| 10              | [Baseline Value]          | [ASP Value]         |

**Figure 3: STLB MPKI Comparison Graph**
<p align="center">
  <img src="dummy_graph_mpki.png" alt="MPKI Graph" style="width:60%;"/>
</p>

### 3. **Key Observations**

- The **Speedup** peaked at **Prefetch Degree = 8** and statyed constant beyond that point.
- The **STLB MPKI** decreased to minimum at Degree 8, indicating fewer misses and improved prefetching efficiency. But after this point it remains mostly constatnt as extra prefecth requests were dropped by the pre fecther itself.

## **Conclusion**

The Arbitrary Stride Prefetcher (ASP) successfully reduced STLB misses and improved the overall performance. Optimal performance was observed at **Prefetch Degree 8**, where both speedup and MPKI were optimized. Further tuning of the state machine and replacement policies may provide additional improvements.

---
