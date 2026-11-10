# Temporal Email Interaction Analysis Using Apache Spark GraphX

## 📋 Project Introduction

This project performs **temporal analysis of email communication patterns** using the email-Eu-core-temporal dataset from the Stanford Network Analysis Project (SNAP). The application leverages Apache Spark GraphX to construct directed temporal graphs and analyze how email interaction patterns evolve across different time windows.

## 🎯 Problem Statement

In large organizations, understanding email communication patterns is critical for:
- Identifying key communicators and influencers
- Detecting changes in organizational structure over time
- Understanding information flow and collaboration networks
- Recognizing isolated individuals or departments

Traditional static analysis fails to capture the **temporal dimension** of communication. This project addresses this gap by analyzing how communication patterns **change over time** using graph analytics.

## 📌 Objectives

1. **Load and validate** the email-Eu-core-temporal dataset using Spark RDDs
2. **Construct temporal directed graphs** for configurable time windows using GraphX
3. **Calculate degree distributions** (in-degree, out-degree, total degree) for all users
4. **Identify the most active users** (top senders, receivers, and overall) per time period
5. **Analyze connected components** and compare network connectivity across periods
6. **Compare degree rankings** across time periods to identify rising/declining users
7. **Perform SQL-based analysis** using Spark SQL with aggregate functions
8. **Visualize results** using Python (Pandas, Matplotlib, NetworkX)

## 📊 Dataset Description

| Property | Value |
|----------|-------|
| **Name** | email-Eu-core-temporal |
| **Source** | [SNAP](https://snap.stanford.edu/data/email-Eu-core-temporal.html) |
| **Nodes (Users)** | 986 |
| **Edges (Email Events)** | 332,334 |
| **Type** | Directed, Temporal |
| **Format** | `source_id  destination_id  unix_timestamp` |

The dataset captures email communications within a large European research institution. Each record represents a directed email from one user to another at a specific point in time.

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Apache Spark | 3.3.4 | Distributed computing framework |
| Spark GraphX | 3.3.4 | Graph analytics on Spark |
| Spark SQL | 3.3.4 | Structured data queries |
| Scala | 2.12 | Primary programming language |
| Java | 8 | JVM runtime |
| SBT | 1.9.7 | Scala build tool |
| Python | 3.11 | Visualization scripts |
| Pandas | ≥1.5 | Data manipulation |
| Matplotlib | ≥3.6 | Chart generation |
| NetworkX | ≥3.0 | Network graph visualization |

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     INPUT LAYER                          │
│  email-Eu-core-temporal.txt (332,334 email records)     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  PROCESSING LAYER                        │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ DataLoader   │  │ GraphBuilder │  │ SparkSQL     │   │
│  │ (RDD Parse)  │→ │ (GraphX)     │→ │ (DataFrames) │   │
│  └─────────────┘  └──────┬───────┘  └──────────────┘   │
│                          │                               │
│  ┌─────────────┐  ┌──────▼───────┐  ┌──────────────┐   │
│  │ Activity    │  │ Degree       │  │ Connected    │    │
│  │ Analyzer    │  │ Ranking      │  │ Components   │    │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
│                                                          │
│              Apache Spark (local[*])                     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   OUTPUT LAYER                           │
│                                                          │
│  CSV Files → Python Visualization → PNG Charts           │
│  (activity/, rankings/, components/, graphs/)            │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Folder Structure

```
Temporal-Email-Analysis/
│
├── dataset/                          # Input dataset
│   ├── email-Eu-core-temporal.txt    # Email interaction data
│   └── README.md                     # Dataset documentation
│
├── src/main/scala/com/emailanalytics/ # Scala source code
│   ├── Main.scala                     # Entry point / orchestrator
│   ├── DataLoader.scala               # RDD-based data loading
│   ├── TemporalGraphBuilder.scala     # GraphX graph construction
│   ├── UserActivityAnalyzer.scala     # Activity ranking analysis
│   ├── ConnectedComponentsAnalyzer.scala # Component analysis
│   ├── DegreeRankingAnalyzer.scala    # Degree computation & comparison
│   └── SparkSQLAnalyzer.scala         # Spark SQL queries
│
├── visualization/                     # Python visualization scripts
│   ├── visualize_activity.py          # Activity charts
│   ├── visualize_degree.py            # Degree & ranking charts
│   ├── visualize_components.py        # Component charts
│   └── visualize_network.py           # Network graph rendering
│
├── output/                            # Generated output
│   ├── activity/                      # Degree data, activity CSVs, charts
│   ├── rankings/                      # User ranking CSVs and charts
│   ├── components/                    # Component analysis CSVs and charts
│   └── graphs/                        # Edge lists and network charts
│
├── config/
│   └── application.properties         # Configurable parameters
│
├── docs/                              # Academic documentation
│   ├── project_overview.md
│   ├── implementation.md
│   ├── results.md
│   └── viva_questions.md
│
├── scripts/
│   ├── run_project.bat                # Build + Run + Visualize
│   └── run_visualizations.bat         # Run only visualizations
│
├── build.sbt                          # SBT build configuration
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

## 🔧 Implementation Details

### Task 1: Load Temporal Email Events
- Reads the dataset using `SparkContext.textFile()`
- Parses each line into `EmailEvent(source, destination, timestamp)`
- Validates records and removes malformed entries
- Reports total records, unique users, and timestamp range

### Task 2: Construct Temporal Graphs
- Computes evenly-spaced time window boundaries
- Creates a separate directed GraphX `Graph` for each window
- Vertices represent users; edges represent email interactions
- Preserves isolated vertices present in the full dataset

### Task 3: Calculate Degree Distributions
- Computes in-degree (incoming emails), out-degree (outgoing emails), and total degree
- Exports results to CSV sorted by total degree

### Task 4: Identify Most Active Users
- Activity Score = In-Degree + Out-Degree
- Ranks top 10 senders, receivers, and overall active users per period
- Exports to separate CSV files

### Task 5: Connected Components Analysis
- Uses `graph.connectedComponents()` (treats graph as undirected for connectivity)
- Reports: number of components, largest component size, isolated nodes
- Compares connectivity changes across time periods

### Task 6: Degree Ranking Comparison
- Assigns ranks based on total degree within each period
- Computes rank changes between consecutive periods
- Identifies top risers and fallers

### Spark SQL Analysis
- Creates a temporary SQL view `email_events`
- Executes 7 SQL queries using COUNT, SUM, AVG, GROUP BY, ORDER BY
- Uses window functions (ROW_NUMBER) for per-period top-N analysis

## 🔬 Algorithms Used

| Algorithm | Purpose | Library |
|-----------|---------|---------|
| Degree Counting | In/Out/Total degree per vertex | GraphX (inDegrees, outDegrees) |
| Connected Components | Identify connected groups | GraphX connectedComponents() |
| Ranking with Sorting | Top-N users | Scala Array sorting |
| Time Windowing | Temporal segmentation | Custom implementation |
| Spring Layout | Network visualization | NetworkX |

## 🚀 How to Install Dependencies

### Prerequisites
1. **Java 8** (OpenJDK or Oracle JDK)
2. **Apache Spark 3.3.4** with Hadoop 3.x
3. **SBT 1.9.7** (Scala Build Tool)
4. **Python 3.11** with pip
5. **winutils.exe** for Windows Hadoop compatibility

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Verify Installation
```bash
java -version          # Should show 1.8.x
spark-submit --version # Should show 3.3.4
sbt --version          # Should show 1.9.7
python --version       # Should show 3.11.x
```

## ▶️ How to Run the Project

### Option 1: Full Pipeline (Recommended)
```bash
cd scripts
run_project.bat
```

### Option 2: Step by Step

**Compile:**
```bash
sbt clean compile package
```

**Run Spark Application:**
```bash
spark-submit --class com.emailanalytics.Main --master "local[*]" --driver-memory 2g target/scala-2.12/temporal-email-analysis_2.12-1.0.jar
```

**Generate Visualizations:**
```bash
python visualization/visualize_activity.py
python visualization/visualize_degree.py
python visualization/visualize_components.py
python visualization/visualize_network.py
```

## 📈 Output Descriptions

### CSV Outputs
| File | Description |
|------|-------------|
| `degrees_Period_N.csv` | In/out/total degree for all users in period N |
| `top_active_Period_N.csv` | Top 10 most active users in period N |
| `top_senders_Period_N.csv` | Top 10 email senders in period N |
| `top_receivers_Period_N.csv` | Top 10 email receivers in period N |
| `component_summary_Period_N.csv` | Connected component statistics |
| `component_comparison.csv` | Cross-period component comparison |
| `ranking_comparison_*.csv` | Degree ranking changes between periods |
| `sql_*.csv` | Spark SQL query results |

### Visualization Outputs
| Chart | File |
|-------|------|
| Incoming vs Outgoing Degree | `output/activity/incoming_vs_outgoing.png` |
| Activity Comparison | `output/activity/activity_comparison.png` |
| Communication Timeline | `output/activity/communication_timeline.png` |
| Top Active Users | `output/rankings/top_active_users.png` |
| Ranking Comparison | `output/rankings/ranking_comparison_*.png` |
| Component Comparison | `output/components/component_comparison.png` |
| Network Graph | `output/graphs/network_Period_N.png` |

## 📸 Screenshots

*After running the project, screenshots of the generated charts can be found in the `output/` subdirectories.*

## 🏁 Conclusion

This project demonstrates the application of graph analytics to temporal email communication data. By combining Apache Spark GraphX for distributed graph computation with Spark SQL for structured queries, we successfully:

- Analyzed 332,334 email interactions across 986 users
- Identified key communicators and how their influence changes over time
- Discovered connectivity patterns and isolated users
- Generated professional visualizations of communication networks

The temporal dimension reveals patterns invisible in static analysis, such as users who become more or less central over time.

## 🔮 Future Enhancements

1. **PageRank Analysis**: Implement GraphX PageRank to identify most influential users
2. **Community Detection**: Use Label Propagation or Louvain algorithm
3. **Anomaly Detection**: Identify unusual communication spikes
4. **Real-time Processing**: Integrate with Kafka for streaming analysis
5. **Machine Learning**: Use Spark MLlib for predictive communication models
6. **Interactive Dashboard**: Build a web dashboard with D3.js
7. **Weighted Edges**: Aggregate multiple emails between same users
8. **Department Analysis**: Incorporate department labels if available
