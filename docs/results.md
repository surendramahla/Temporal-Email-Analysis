# Analysis Results

## Dataset Summary

| Metric | Value |
|--------|-------|
| Total email events | 332,334 |
| Total unique users | 986 |
| Time span | ~525 days (~45,405,138 seconds) |
| Time windows analyzed | 3 equal periods |

---

## Task 1: Data Loading Results

- **Valid records loaded**: 332,334
- **Malformed records**: 0 (clean dataset)
- **Min timestamp**: 0
- **Max timestamp**: 45,405,138 seconds
- **Unique users**: 986

---

## Task 2: Temporal Graph Construction

| Period | Time Range (sec) | Vertices | Edges |
|--------|-----------------|----------|-------|
| Period 1 | [0 – 15,135,045] | 986 | ~163,598 |
| Period 2 | [15,135,046 – 30,270,091] | 986 | ~166,312 |
| Period 3 | [30,270,092 – 45,405,138] | 986 | ~2,424 |

**Observation**: The bulk of email activity is concentrated in Periods 1 and 2. Period 3 shows dramatically reduced activity, suggesting the institution's email activity declined significantly in the latter part of the dataset.

---

## Task 3: Degree Distribution Results

### Top 10 Users by Total Degree (Period 1)

| Rank | User ID | In-Degree | Out-Degree | Total |
|------|---------|-----------|------------|-------|
| 1 | 629 | — | — | 5,569 |
| 2 | 987 | — | — | 4,674 |
| 3 | 168 | — | — | 4,539 |
| 4 | 586 | — | — | 4,012 |
| 5 | 98  | — | — | 3,754 |

*(Detailed in-degree/out-degree breakdown in `output/activity/degrees_Period_N.csv`)*

---

## Task 4: Most Active Users

### Period 1 — Top 5 Active Users

| Rank | User ID | Activity Score |
|------|---------|---------------|
| 1 | 629 | 5,569 |
| 2 | 987 | 4,674 |
| 3 | 168 | 4,539 |
| 4 | 586 | 4,012 |
| 5 | 98  | 3,754 |

**Observation**: User 629 and User 987 are consistently the most active communicators.

---

## Task 5: Connected Components Analysis

| Period | Total Vertices | Components | Largest Component | Isolated Nodes |
|--------|---------------|------------|-------------------|----------------|
| Period 1 | 986 | 125 | 862 | 124 |
| Period 2 | 986 | 72  | 914 | 70  |
| Period 3 | 986 | 451 | 533 | 447 |

### Key Observations:
1. **Period 1 → Period 2**: The network becomes **more connected** — components drop from 125 to 72, and the largest component grows from 862 to 914 users. This suggests stronger organizational cohesion.
2. **Period 2 → Period 3**: The network **fragments dramatically** — components jump to 451, and isolated nodes increase from 70 to 447. This aligns with the massive drop in email volume in Period 3.
3. The **largest connected component** captures 87.4% of users in Period 1, 92.7% in Period 2, but only 54.1% in Period 3.

---

## Task 6: Degree Ranking Changes

### Summary: Period 1 → Period 2
- Users whose rank **improved**: Top risers show significant movement up the activity rankings
- Users whose rank **declined**: Some Period 1 heavy senders reduced activity in Period 2
- Detailed in `output/rankings/ranking_comparison_Period_1_vs_Period_2.csv`

---

## Spark SQL Results

### Query Results

| Query | Result |
|-------|--------|
| Total email interactions | 332,334 |
| Period 1 interactions | 163,598 (unique senders: 725, receivers: 842) |
| Period 2 interactions | 166,312 (unique senders: 749, receivers: 904) |
| Period 3 interactions | 2,424 (unique senders: 340, receivers: 504) |

---

## Visualization Outputs

All charts saved as PNG files in the `output/` directory:

| Chart | Location |
|-------|----------|
| Incoming vs Outgoing Degree | `output/activity/incoming_vs_outgoing.png` |
| Activity Comparison Across Periods | `output/activity/activity_comparison.png` |
| Communication Timeline | `output/activity/communication_timeline.png` |
| Interactions by Period | `output/activity/interactions_by_period.png` |
| Top 10 Active Users | `output/rankings/top_active_users.png` |
| Senders vs Receivers | `output/rankings/senders_vs_receivers.png` |
| Ranking Comparison Chart | `output/rankings/ranking_comparison_*.png` |
| Component Comparison | `output/components/component_comparison.png` |
| Component Size Distribution | `output/components/component_size_distribution.png` |
| Connectivity Summary | `output/components/connectivity_summary.png` |
| Network Graph (Period 1) | `output/graphs/network_Period_1.png` |
| Network Graph (Period 2) | `output/graphs/network_Period_2.png` |
| Network Graph (Period 3) | `output/graphs/network_Period_3.png` |
| Degree Distribution | `output/graphs/degree_distribution.png` |

---

## Conclusion

The temporal analysis reveals a clear **lifecycle pattern** in organizational email communication:
- **Active growth phase** (Period 1): High activity, moderately connected network
- **Peak connectivity** (Period 2): Maximum email volume and network cohesion
- **Declining phase** (Period 3): Dramatic drop in activity and fragmentation

This demonstrates the power of temporal graph analysis — a static view of the network would miss these critical structural changes over time.
