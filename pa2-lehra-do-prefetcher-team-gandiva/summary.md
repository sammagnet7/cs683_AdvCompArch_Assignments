<p align="center">
  <h1 align="center"> pa2-lehra-do-prefetcher-team-gandiva </h1>

### Task1: Implementing the Arbitrary Stride Prefetcher

The problem involves modifying the `asp.stlb_pref` file to implement an Arbitrary Stride Prefetcher (ASP) for the Shared Translation Lookaside Buffer (STLB). The core mechanism for ASP leverages the concept of tracking address strides using a Reference Prediction Table (RPT). The objective is to dynamically calculate strides based on memory access patterns and prefetch addresses based on observed patterns.

Let's walk through the implementation step-by-step:

1. **Define the `IP_TRACKER` class**:  
   Each `IP_TRACKER` will maintain metadata for a particular instruction pointer (IP). This will include:
   - Instruction pointer
   - Last Address
   - Last Stride
   - State for tracking stride consistency

2. **Initialize the Prefetcher**:  
   The `stlb_prefetcher_initialize` function will initialize necessary data structures. The function should reset all trackers to a clean state.

3. **Implement Prefetcher Logic in `stlb_prefetcher_operate`**:  
   This is where we calculate the stride, determine the state, and initiate prefetches.  
   - **Stride Calculation**: Compute the stride for the current memory access.
   - **State Update**: Change the state based on the stride's consistency.
   - **Prefetch Address Calculation**: If the state indicates a stable stride, calculate the next prefetch address.

### Code Implementation
Here's a basic implementation for the `asp.stlb_pref` file:

```cpp
// Define states for stride consistency
#define INITIAL 0
#define STEADY 1
#define TRANSIENT 2
#define NO_PRED 3

// IP_TRACKER Class Definition
class IP_TRACKER
{
public:
    uint64_t ip;          // Instruction pointer
    uint64_t last_addr;   // Last address referenced
    int64_t last_stride;  // Last stride calculated
    int state;            // State of the tracker

    IP_TRACKER() {
        ip = 0;
        last_addr = 0;
        last_stride = 0;
        state = INITIAL;
    }
};

// Array of IP_TRACKER objects
IP_TRACKER trackers[IP_TRACKER_COUNT];

// ------------------------- Initialize the prefetcher ------------------------- //
void CACHE::stlb_prefetcher_initialize()
{
    cout << "CPU " << cpu << " STLB arbitrary stride prefetcher" << endl;
    for (int i = 0; i < IP_TRACKER_COUNT; i++) {
        trackers[i] = IP_TRACKER(); // Initialize each tracker
    }
}

// --------------- This is the main prefetcher operate function ---------------- //
void CACHE::stlb_prefetcher_operate(uint64_t addr, uint64_t ip, uint8_t cache_hit, uint8_t type, uint64_t prefetch_id, uint8_t instruction)
{
    // Search for the IP in the tracker table
    int tracker_index = -1;
    for (int i = 0; i < IP_TRACKER_COUNT; i++) {
        if (trackers[i].ip == ip || trackers[i].ip == 0) {
            tracker_index = i;
            break;
        }
    }

    if (tracker_index == -1) return; // No available tracker

    IP_TRACKER *tracker = &trackers[tracker_index];

    // Update the tracker IP if it's a new entry
    if (tracker->ip == 0) {
        tracker->ip = ip;
        tracker->last_addr = addr;
        tracker->state = INITIAL;
        return;
    }

    // Calculate the stride
    int64_t stride = addr - tracker->last_addr;

    // State machine logic to handle stride consistency
    switch (tracker->state) {
    case INITIAL:
        if (stride != 0) {
            tracker->last_stride = stride;
            tracker->state = TRANSIENT;
        }
        break;

    case TRANSIENT:
        if (stride == tracker->last_stride) {
            tracker->state = STEADY;
        } else {
            tracker->last_stride = stride;
        }
        break;

    case STEADY:
        if (stride != tracker->last_stride) {
            tracker->state = INITIAL;
        }
        break;

    default:
        tracker->state = INITIAL;
        break;
    }

    tracker->last_addr = addr;

    // Prefetch logic: Prefetch only if in the STEADY state
    if (tracker->state == STEADY) {
        for (int i = 1; i <= PREFETCH_DEGREE; i++) {
            uint64_t pf_address = addr + (i * tracker->last_stride);

            // Prefetch the calculated address
            prefetch_translation(ip, pf_address, (int)2, 0, prefetch_id, instruction);
        }
    }

    return;
}
```

### Explanation of Implementation:
1. **IP_TRACKER Class**: Contains metadata for a given instruction pointer (IP). The class tracks:
   - `ip`: Instruction Pointer (PC value).
   - `last_addr`: The last address referenced by this instruction.
   - `last_stride`: Calculated stride between successive addresses.
   - `state`: State of the tracker (INITIAL, TRANSIENT, STEADY).

2. **`stlb_prefetcher_operate` Function**:
   - Finds the appropriate IP tracker or creates a new one.
   - Computes the stride and updates the state machine.
   - If the state is `STEADY`, initiates prefetches using the stride.

3. **Prefetch Calculation**: Uses the stride to prefetch multiple addresses. The degree of prefetching is controlled using the `PREFETCH_DEGREE` macro.

This approach follows the principles outlined in the problem statement and leverages the RPT-like structure to implement arbitrary stride prefetching in the TLB.

---

