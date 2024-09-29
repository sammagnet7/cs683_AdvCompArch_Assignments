<p align="center">
  <h1 align="center"> pa2-lehra-do-prefetcher-team-gandiva </h1>

## Task 1: TLB Prefetching

### **Implementing the Arbitrary Stride Prefetcher**

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
# Navigate to the ChampSim directory
cd path/to/champsim

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

---
## Task 2: Data Prefetcher

### **IP-Stride and Complex-Stride Prefetcher Implementation Analysis**

#### **2.1 Overview of Prefetcher Designs**

Two types of stride-based prefetchers were implemented and evaluated in the **ChampSim** simulation environment: **IP-Stride Prefetcher** and **Complex-Stride Prefetcher**. This section outlines the step-by-step procedure for implementing each prefetcher, along with performance analysis and comparisons.

---

#### **2.2 Implementation Steps**

##### **2.2.1 IP-Stride Prefetcher Implementation**

1. **Implement the Prefetcher Logic**:
   - The IP-Stride prefetcher tracks stride patterns for each instruction pointer (IP) and issues prefetches based on consistent strides.
   - State machine for tracking `INITIAL`, `TRANSIENT`, `STEADY`, and `NOPRED` states.
   - Prefetches are issued within the same 4KB page to avoid cross-page pollution.

2. **Build and Execute**:
   - Use the following commands to build and execute the prefetcher:

   ```bash
   # Navigate to the ChampSim directory
   cd path/to/champsim

   # Build the IP-Stride Prefetcher
   ./build_champsim.sh ip_stride no 1

   # Run the simulation with the given trace and configurations
    ./bin/ip_stride-no-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces ../given/traces/trace2.champsimtrace.xz   
    ```

>##### **Key Takeaways**

  IP-Stride prefetcher is a basic yet efficient mechanism for leveraging consistent stride patterns, making it suitable for workloads dominated by sequential memory access. However, it may fall short in scenarios with non-linear or complex access patterns, where more advanced prefetching strategies like the Complex-Stride prefetcher would be more effective.

##### **2.2.2 Complex-Stride Prefetcher Implementation**

1. **Implement the Prefetcher Logic**:
   - The Complex-Stride Prefetcher extends the IP-Stride by incorporating **delta-strides**.
   - Track stride changes **pattern** for each IP, using a **confidence metric** to gauge prediction reliability.
   - Implement a signature-based indexing mechanism for storing and retrieving complex stride patterns.

2. **Build and Execute**:
   - Use the following commands to build and execute the Complex-Stride Prefetcher:

   ```bash
   # Build the Complex-Stride Prefetcher
   ./build_champsim.sh complex_stride no 1

   # Run the simulation with the given trace and configurations
   ./bin/complex_stride-no-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces ../given/traces/trace2.champsimtrace.xz
   ```

>##### **Key Takeaways**

  This implementation showcases a robust stride prefetcher that can handle both regular and complex stride patterns, making it well-suited for modern applications with diverse memory access behaviors.

---

#### **2.3 Performance Metrics and Evaluation**

The performance of the implemented prefetchers was evaluated against a **baseline (no prefetcher)**. The key metrics used for comparison are:

##### **2.3.1 Speedup Analysis**

- **IP-Stride Speedup**: IP-Stride was compared to the baseline and achieved a speedup of `X%` for the given trace.
- **Complex-Stride Speedup**: Complex-Stride prefetcher outperformed the baseline and IP-Stride, with a speedup of `Y%`.

| **Prefetcher**         | **Speedup (%)** |
|------------------------|----------------|
| **No Prefetcher**      | 1              |
| **IP-Stride**          | X              |
| **Complex-Stride**     | Y              |

- **Plot Placeholder**:
  ![Speedup Analysis](./speedup_analysis.png)

##### **2.3.2 L1D MPKI Analysis**

- **Baseline**: Without any prefetching, the L1D Misses Per 1000 Instructions (MPKI) was observed to be `Z`.
- **IP-Stride**: The IP-Stride prefetcher reduced L1D MPKI by `X%` over the baseline.
- **Complex-Stride**: The Complex-Stride prefetcher demonstrated a more significant reduction in L1D MPKI compared to IP-Stride and baseline.

| **Prefetcher**         | **L1D MPKI (Total)** | **L1D MPKI (Load)** |
|------------------------|----------------------|---------------------|
| **No Prefetcher**      | Z                    | Z_load              |
| **IP-Stride**          | A                    | A_load              |
| **Complex-Stride**     | B                    | B_load              |

- **Plot Placeholder**:
  ![L1D MPKI Analysis](./mpki_analysis.png)

---

#### **2.4 Comparative Analysis**

The results show that **Complex-Stride Prefetcher** performs better than the **IP-Stride Prefetcher** for the given trace2, with lower L1D MPKI and higher speedup. The additional complexity of handling strides' **historical patterns** and maintaining a confidence-based state tracking mechanism allows the Complex-Stride Prefetcher to better adapt to varying memory access patterns.

---

#### **2.5 Conclusion**

The **Complex-Stride Prefetcher** outperforms the **IP-Stride Prefetcher** and the **Baseline** in terms of both **speedup** and **L1D MPKI reduction** in case of running trace2. This highlights its effectiveness in handling complex memory access patterns, making it suitable for workloads with irregular and non-linear memory references.

---
