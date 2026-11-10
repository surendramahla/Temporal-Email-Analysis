# Viva Questions and Answers

## Temporal Email Interaction Analysis Using Apache Spark GraphX

---

## SECTION 1: Apache Spark

**Q1. What is Apache Spark and why is it used for Big Data processing?**

Apache Spark is an open-source, distributed computing framework designed for fast, large-scale data processing. It is used because:
- It processes data **in-memory** (RAM), making it up to 100× faster than Hadoop MapReduce for iterative jobs
- Supports multiple APIs: RDD, DataFrame/SQL, GraphX, MLlib, Streaming
- Runs on a single machine (local mode) or a cluster
- Fault-tolerant through RDD lineage graphs
- In this project, Spark processes 332,334 email records and builds graphs on a single Windows machine using `local[*]` mode

---

**Q2. What is the difference between Spark's driver and executor?**

| Component | Role |
|-----------|------|
| **Driver** | The main program; creates SparkContext, plans DAG, schedules tasks |
| **Executor** | JVM processes on worker nodes that actually run tasks and store data |

In local mode (`local[*]`), both driver and executors run in the same JVM process.

---

**Q3. What is a DAG in Spark and why is it important?**

A **Directed Acyclic Graph (DAG)** is Spark's execution plan — a graph of transformations and actions.
- Spark builds the DAG lazily when you define transformations
- The DAG Scheduler optimizes the plan by pipelining narrow transformations
- It divides the DAG into **stages** separated by shuffle operations
- This lazy evaluation avoids unnecessary computations

---

**Q4. What is the difference between transformations and actions in Spark?**

| | Transformations | Actions |
|-|----------------|---------|
| Execution | Lazy (deferred) | Eager (triggers computation) |
| Returns | New RDD/DataFrame | Value or side effect |
| Examples | `map`, `filter`, `groupBy` | `count`, `collect`, `show`, `save` |

In this project: `filter()` and `map()` are transformations; `count()` and `collect()` are actions.

---

**Q5. What is SparkContext vs SparkSession?**

- **SparkContext** (Spark 1.x): Entry point for RDD operations
- **SparkSession** (Spark 2.x+): Unified entry point for all Spark functionality (includes SparkContext, SQLContext, HiveContext)
- In Spark 3.x, `SparkSession.builder()` is preferred; `spark.sparkContext` gives you the underlying SparkContext

---

## SECTION 2: Hadoop MapReduce vs Spark

**Q6. How does Apache Spark differ from Hadoop MapReduce?**

| Feature | Hadoop MapReduce | Apache Spark |
|---------|-----------------|--------------|
| Speed | Slower (disk I/O between stages) | Faster (in-memory processing) |
| Programming model | Only Map and Reduce | RDD, DataFrame, SQL, GraphX, MLlib |
| Fault tolerance | Replication in HDFS | RDD lineage |
| Iteration | Requires multiple MR jobs | Keeps data in memory |
| Ease of use | Verbose Java code | Concise Scala/Python/R APIs |
| Real-time | Not native | Spark Streaming |

---

**Q7. Can Spark replace Hadoop completely?**

Not entirely. Spark:
- Does **not** provide a distributed file system (needs HDFS, S3, or local FS)
- Does **not** handle very large datasets that don't fit in cluster memory as efficiently as MapReduce
- Spark typically runs **on top of** Hadoop YARN for resource management and uses HDFS for storage

---

## SECTION 3: RDD (Resilient Distributed Dataset)

**Q8. What is an RDD and what are its key properties?**

An RDD (Resilient Distributed Dataset) is Spark's fundamental data abstraction:
- **Resilient**: Fault-tolerant via lineage — if a partition is lost, it can be recomputed
- **Distributed**: Partitioned across cluster nodes
- **Dataset**: Collection of records (any type)
- **Immutable**: Once created, cannot be modified; transformations create new RDDs
- **Lazily evaluated**: Computations are triggered only by actions

---

**Q9. What is the difference between narrow and wide transformations?**

| | Narrow Transformation | Wide Transformation |
|-|----------------------|---------------------|
| Data movement | Each partition maps to one output partition | Requires data shuffle across partitions |
| Examples | `map`, `filter`, `flatMap` | `groupByKey`, `reduceByKey`, `join` |
| Stage boundary | No | Yes (starts new stage) |
| Performance | Faster | Slower (network I/O) |

---

**Q10. When should you use `cache()` vs `persist()` in Spark?**

- `cache()` stores the RDD in memory (equivalent to `persist(MEMORY_ONLY)`)
- `persist()` allows specifying storage level: MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY, etc.
- Use caching when an RDD is used **multiple times** in the application to avoid recomputation
- In this project: `emailEvents.cache()` is used since it is accessed for all 6 tasks

---

## SECTION 4: Scala

**Q11. What makes Scala suitable for Apache Spark?**

- Spark itself is written in Scala
- Scala provides concise, expressive functional programming constructs
- **Type safety** at compile time catches errors early
- **Pattern matching** simplifies case class parsing
- Seamless Java interoperability
- Closures and higher-order functions integrate naturally with Spark's functional API

---

**Q12. What is a case class in Scala?**

A case class is a special class that:
- Auto-generates `equals`, `hashCode`, `toString`, `copy` methods
- Is immutable by default
- Supports pattern matching
- Example from this project:
  ```scala
  case class EmailEvent(source: Long, destination: Long, timestamp: Long)
  ```

---

**Q13. What is the difference between `map` and `flatMap` in Scala/Spark?**

- `map(f)`: applies `f` to each element, returns one result per element
- `flatMap(f)`: applies `f` to each element where `f` returns a collection, then flattens results

Example:
```scala
// map: RDD[(Long, Long)] — one pair per event
events.map(e => (e.source, e.destination))

// flatMap: RDD[Long] — two IDs per event, flattened
events.flatMap(e => Seq(e.source, e.destination))
```

---

## SECTION 5: Spark SQL

**Q14. What is a Spark DataFrame and how does it differ from an RDD?**

| | RDD | DataFrame |
|-|-----|-----------|
| Schema | No schema | Has named columns with types |
| Optimization | User-controlled | Catalyst optimizer |
| API | Functional (map, filter) | SQL-like (select, groupBy) |
| Serialization | Java/Kryo | Tungsten binary format |
| Performance | Good | Better (Catalyst + Tungsten) |

---

**Q15. What is a temporary view in Spark SQL?**

A temporary view is a named alias for a DataFrame that can be queried using SQL:
```scala
emailDF.createOrReplaceTempView("email_events")
spark.sql("SELECT COUNT(*) FROM email_events").show()
```
It exists only for the duration of the SparkSession and is not persisted to disk.

---

**Q16. What SQL aggregate functions are used in this project?**

| Function | Purpose |
|----------|---------|
| `COUNT(*)` | Count total email events |
| `SUM()` | Sum email counts per user |
| `AVG()` | Average emails sent per user |
| `GROUP BY` | Group by user or period |
| `ORDER BY` | Sort by activity |
| `ROW_NUMBER() OVER (PARTITION BY)` | Rank users within each period |
| `COUNT(DISTINCT)` | Count unique senders/receivers |

---

## SECTION 6: GraphX

**Q17. What is Apache Spark GraphX?**

GraphX is Spark's library for graph-parallel computation. It extends the RDD abstraction with a **property graph** model:
- Each vertex has an ID (VertexId = Long) and an attribute
- Each edge has a source, destination, and attribute
- Provides built-in graph algorithms: PageRank, ConnectedComponents, TriangleCount, etc.
- Uses the **Pregel API** for iterative graph computations

---

**Q18. How is a GraphX graph constructed in this project?**

```scala
// Create vertices RDD: (VertexId, attribute)
val vertices: RDD[(VertexId, String)] = events
  .flatMap(e => Seq(e.source, e.destination))
  .distinct()
  .map(uid => (uid, s"User_$uid"))

// Create edges RDD: Edge(srcId, dstId, attribute)
val edges: RDD[Edge[Long]] = windowEvents
  .map(e => Edge(e.source, e.destination, e.timestamp))

// Build graph
val graph = Graph(vertices, edges, "Unknown")
```

---

**Q19. What is in-degree and out-degree in a directed graph?**

- **In-degree** of vertex v: Number of edges pointing **into** v (emails received)
- **Out-degree** of vertex v: Number of edges going **out from** v (emails sent)
- **Total degree** = in-degree + out-degree = total email interactions

In GraphX:
```scala
val inDeg:  RDD[(VertexId, Int)] = graph.inDegrees
val outDeg: RDD[(VertexId, Int)] = graph.outDegrees
```

---

**Q20. What is the Activity Score used in this project?**

**Activity Score = In-Degree + Out-Degree**

This metric captures a user's total communication volume — both as a sender and receiver. A high activity score indicates a key communicator or hub in the organization.

---

## SECTION 7: Connected Components

**Q21. What are connected components in a graph?**

A connected component is a **maximal set of vertices** such that there is a path between any two vertices in the set (treating edges as undirected).

For example, if user A emails B, and B emails C, then {A, B, C} form one connected component.

---

**Q22. How does GraphX's `connectedComponents()` work?**

GraphX uses a **label propagation** algorithm via Pregel:
1. Each vertex initializes its label with its own ID
2. Iteratively: each vertex adopts the **minimum** label among itself and its neighbors
3. After convergence, all vertices in the same component have the same label (the lowest vertex ID in the component)

**Important**: This treats the graph as **undirected** — it ignores edge direction.

---

**Q23. What do the connected component results reveal in this project?**

| Period | Components | Largest | Isolated |
|--------|-----------|---------|---------|
| Period 1 | 125 | 862 nodes | 124 |
| Period 2 | 72 | 914 nodes | 70 |
| Period 3 | 451 | 533 nodes | 447 |

- Period 2 has the **most connected** network (fewest components, largest main component)
- Period 3 shows **severe fragmentation** — 447 isolated nodes — matching the drop in email volume (only 2,424 emails in Period 3 vs 163,598 in Period 1)

---

## SECTION 8: Directed Graphs and Temporal Analysis

**Q24. What is a directed graph and why is it appropriate for email data?**

A directed graph (digraph) has edges with a direction: A → B means A sent an email to B, but it doesn't imply B sent an email to A. This is appropriate for email data because:
- Sending ≠ Receiving
- Direction reveals information flow and hierarchies
- In-degree and out-degree have different meanings (received vs sent)

---

**Q25. What is a temporal graph?**

A temporal graph is a graph where edges (and possibly vertices) have associated timestamps. It captures how the network structure evolves over time. In this project:
- Each email event has a Unix timestamp
- We split time into windows and build a static graph per window
- Comparing these graphs reveals temporal patterns

---

**Q26. What are the advantages of temporal graph analysis over static analysis?**

| Static Analysis | Temporal Analysis |
|----------------|-----------------|
| Single snapshot | Multiple time windows |
| Misses trends | Reveals growth, decline |
| No rank changes | Shows who becomes more/less important |
| No lifecycle | Captures seasonal patterns |

---

## SECTION 9: Kafka

**Q27. What is Apache Kafka and how could it extend this project?**

Apache Kafka is a **distributed event streaming platform** used for real-time data pipelines.

In a real-time extension of this project:
- Email events would be published to a **Kafka topic** as they occur
- **Spark Structured Streaming** would subscribe to the topic
- Temporal graphs would be updated in near-real-time
- This enables live monitoring of communication patterns

Key Kafka concepts:
- **Topic**: Named stream of records
- **Producer**: Publishes records to topics
- **Consumer**: Subscribes and processes records
- **Broker**: Kafka server that stores records
- **Partition**: Topic divided for parallelism

---

**Q28. What is the difference between batch processing (this project) and stream processing (Kafka + Spark Streaming)?**

| | Batch Processing | Stream Processing |
|-|-----------------|-----------------|
| Latency | Hours to minutes | Seconds to milliseconds |
| Data | Historical (bounded) | Live (unbounded) |
| Tools | Spark RDD/SQL | Kafka + Spark Streaming |
| Use case | Offline analysis | Real-time monitoring |

---

## SECTION 10: Spark MLlib

**Q29. What is Spark MLlib and how could it be applied to this project?**

Spark MLlib is Spark's distributed machine learning library. Potential applications:
- **Clustering (K-Means)**: Group users by communication patterns
- **Classification**: Predict if a user is an "influencer" or "peripheral" based on graph features
- **Anomaly Detection**: Flag unusual email volumes or patterns
- **Graph Embeddings**: Use node2vec features for link prediction
- **Time Series Forecasting**: Predict future email volumes per user

---

**Q30. What is the difference between supervised and unsupervised machine learning in the context of email analysis?**

| | Supervised | Unsupervised |
|-|-----------|-------------|
| Labels needed | Yes (e.g., spam/not spam) | No |
| Goal | Predict class or value | Discover structure |
| Algorithms | SVM, Random Forest | K-Means, PCA |
| Email use case | Spam detection, importance scoring | User clustering, community detection |

---

## BONUS QUESTIONS

**Q31. What is the Pregel API in GraphX?**

Pregel is a bulk-synchronous message-passing interface for iterative graph algorithms. Each vertex:
1. Receives messages from neighbors
2. Updates its state
3. Sends messages to neighbors

Repeat until convergence or max iterations. GraphX's `connectedComponents()` and `pageRank()` are both implemented using Pregel.

---

**Q32. Why does `spark.sql.shuffle.partitions=4` matter for local mode?**

By default, Spark uses 200 shuffle partitions. On a local machine with a small dataset, 200 tiny tasks adds overhead. Setting it to 4 (matching typical CPU cores) improves performance by reducing task management overhead.

---

**Q33. What is the difference between `groupByKey` and `reduceByKey`?**

- `groupByKey`: Shuffles **all values** to the reducer — high network I/O
- `reduceByKey`: Pre-aggregates values on each partition **before** shuffling — much more efficient
- Always prefer `reduceByKey` when possible for performance

---

**Q34. What does `local[*]` mean as a Spark master?**

`local[*]` runs Spark locally using **as many threads as CPU cores** on the machine. Options:
- `local` — single thread
- `local[2]` — 2 threads
- `local[*]` — all available cores
- `spark://host:7077` — standalone cluster
- `yarn` — Hadoop YARN cluster

---

**Q35. What happens if the dataset file is missing when you run the application?**

The `DataLoader.loadEmailEvents()` method checks if the file exists before calling `sc.textFile()`. If missing, it prints a clear error message with the download URL and returns an empty RDD. The `Main` checks if the RDD is empty and exits gracefully with an informative message — no `NullPointerException` or cryptic Spark errors.
