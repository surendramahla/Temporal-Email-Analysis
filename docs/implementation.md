# Implementation Details

## Module-by-Module Implementation Guide

### 1. DataLoader.scala

**Purpose**: Load and validate the email-Eu-core-temporal dataset.

**Key Implementation Details**:
- Uses `SparkContext.textFile()` to read the dataset as an RDD of strings
- Each line is parsed into an `EmailEvent(source: Long, destination: Long, timestamp: Long)` case class
- Filters out comment lines (starting with `#` or `%`) and blank lines
- Validates that all IDs and timestamps are non-negative
- Reports the count of valid records, unique users, and timestamp range
- Handles missing files with a descriptive error message

**Spark Operations Used**:
- `textFile()` — read file into RDD
- `map()` — transform each line
- `filter()` — remove invalid records
- `flatMap()` — extract unique user IDs
- `distinct()` — deduplicate
- `count()` — count records
- `min()` / `max()` — find timestamp range

---

### 2. TemporalGraphBuilder.scala

**Purpose**: Construct directed GraphX graphs for specified time windows.

**Key Implementation Details**:
- `computeTimeWindows()`: Divides the full timestamp range into N equal windows
- `buildGraph()`: Filters events to a specific window and constructs a GraphX `Graph[String, Long]`
  - Vertices: all users from the full dataset (preserves isolated vertices)
  - Edges: email interactions within the time window
  - Edge attribute: Unix timestamp of the email
- `exportEdgeList()`: Writes edge data to CSV for Python visualization

**GraphX API Used**:
- `Graph(vertices, edges, defaultVertexAttr)` — construct a graph
- `graph.vertices` — access vertex RDD
- `graph.edges` — access edge RDD

---

### 3. UserActivityAnalyzer.scala

**Purpose**: Identify and rank the most active users in each time window.

**Activity Score Formula**: `Activity Score = In-Degree + Out-Degree`

**Key Implementation Details**:
- Uses `graph.inDegrees` and `graph.outDegrees` to get degree RDDs
- Collects to driver and computes activity scores
- Produces three ranked lists per period: top active, top senders, top receivers
- Exports to CSV files

**Design Choice**: Collecting degree data to driver is safe here because the dataset has only 986 users.

---

### 4. ConnectedComponentsAnalyzer.scala

**Purpose**: Analyze network connectivity using connected components.

**Key Implementation Details**:
- Uses `graph.connectedComponents()` which assigns each vertex the lowest vertex ID in its component
- This treats the graph as **undirected** — an important distinction for directed email graphs
- Counts: total components, largest component size, isolated nodes (components of size 1)
- Exports per-period statistics and cross-period comparison

**Important Note**: In a directed email graph, user A emailing user B doesn't mean B can reach A. However, `connectedComponents()` ignores edge direction, which is standard for measuring overall network connectivity.

---

### 5. DegreeRankingAnalyzer.scala

**Purpose**: Compute degree distributions and compare rankings across periods.

**Key Implementation Details**:
- `computeDegrees()`: Returns `DegreeInfo(userId, inDegree, outDegree, totalDegree)` for every user
- `compareRankings()`: 
  - Ranks users by total degree in each period
  - Finds users common to both periods
  - Computes rank change = rank_in_period1 - rank_in_period2
  - Positive change = user moved up (improved rank)
  - Sorts by absolute rank change
- Exports ranking comparison and top movers (risers and fallers)

---

### 6. SparkSQLAnalyzer.scala

**Purpose**: Perform structured queries using Spark SQL DataFrames and SQL syntax.

**Key Implementation Details**:
- Converts RDD[EmailEvent] to DataFrame using `toDF()`
- Registers temporary views: `email_events` and `email_events_with_period`
- Uses a UDF to assign time period labels based on timestamp
- Executes 7 SQL queries:
  1. Total email interactions (COUNT)
  2. Emails sent by each user (GROUP BY, COUNT)
  3. Emails received by each user (GROUP BY, COUNT)
  4. Top active users (UNION ALL, SUM)
  5. Interactions by time period (GROUP BY, COUNT DISTINCT)
  6. Average emails per user (AVG, subquery)
  7. Top users per period (ROW_NUMBER window function)

**SQL Features Demonstrated**:
- `COUNT(*)`, `SUM()`, `AVG()` — aggregate functions
- `GROUP BY`, `ORDER BY` — grouping and sorting
- `UNION ALL` — combining result sets
- `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` — window functions
- Subqueries and temporary views

---

### 7. Main.scala

**Purpose**: Orchestrate all analysis tasks in sequence.

**Execution Flow**:
1. Load configuration from `config/application.properties`
2. Create SparkSession with `local[*]` master
3. Task 1: Load and validate email events
4. Task 2: Construct temporal graphs for each time window
5. Task 3: Compute degree distributions → export to CSV
6. Task 4: Rank most active users → export to CSV
7. Task 5: Analyze connected components → export to CSV
8. Task 6: Compare degree rankings → export to CSV
9. Run Spark SQL analysis → export to CSV
10. Export edge lists for visualization
11. Stop SparkSession

---

## Python Visualization Scripts

### visualize_activity.py
- Incoming vs outgoing degree bar chart
- User activity comparison across time windows
- Communication activity timeline
- Interactions by period bar chart

### visualize_degree.py
- Top 10 most active users horizontal bar chart
- Degree ranking comparison (slope chart)
- Senders vs receivers comparison

### visualize_components.py
- Connected component comparison bar chart
- Component size distribution
- Connectivity summary (connected vs isolated)

### visualize_network.py
- Email communication network graph using NetworkX spring layout
- Node size proportional to degree
- Node color based on in-degree
- Degree distribution histogram
