# Project Overview

## Temporal Email Interaction Analysis Using Apache Spark GraphX

### 1. Introduction

This project implements a Big Data analytics pipeline that analyzes temporal email communication patterns within a European research institution. Using Apache Spark GraphX and Spark SQL, the project constructs temporal directed graphs from the email-Eu-core-temporal dataset and performs comprehensive graph analytics across multiple time windows.

### 2. Background

Email communication is a fundamental medium of information exchange in organizations. Analyzing email patterns reveals:
- **Organizational hierarchies**: Who communicates with whom and how frequently
- **Temporal dynamics**: How communication patterns change over time
- **Key influencers**: Users who send or receive the most emails
- **Network connectivity**: How well-connected the organization is

### 3. Dataset

The **email-Eu-core-temporal** dataset from SNAP (Stanford Network Analysis Project) contains 332,334 directed email events between 986 users. Each record has three fields:
- Source user ID (sender)
- Destination user ID (receiver)
- Unix timestamp (when the email was sent)

### 4. Methodology

The analysis follows these steps:

1. **Data Ingestion**: Load and validate the raw text data using Spark RDDs
2. **Temporal Segmentation**: Divide the dataset into time windows
3. **Graph Construction**: Build directed GraphX graphs for each window
4. **Degree Analysis**: Compute in-degree, out-degree, and total degree per user
5. **Activity Ranking**: Identify top senders, receivers, and active users
6. **Connectivity Analysis**: Use connected components to assess network structure
7. **Ranking Comparison**: Track how user importance changes over time
8. **SQL Queries**: Perform aggregation queries using Spark SQL
9. **Visualization**: Generate charts using Python (Matplotlib, NetworkX)

### 5. Key Concepts

#### Graph Theory
- **Vertex**: Represents a user (email sender or receiver)
- **Edge**: Represents a directed email interaction from source to destination
- **In-Degree**: Number of incoming edges (emails received)
- **Out-Degree**: Number of outgoing edges (emails sent)
- **Connected Component**: A maximal set of vertices that are mutually reachable (treating edges as undirected)

#### Apache Spark GraphX
GraphX is Spark's library for graph-parallel computation. It extends the Spark RDD abstraction with a new Graph abstraction: a directed multigraph with properties attached to each vertex and edge.

#### Temporal Analysis
By splitting the dataset into time windows, we can observe how communication patterns evolve. This reveals trends such as:
- Users who become more/less active over time
- Changes in network connectivity
- Shifts in communication hubs

### 6. Expected Outcomes
- CSV files with detailed degree distributions and rankings for each time period
- Comparative analysis showing changes across time windows
- Professional visualizations including network graphs, bar charts, and timelines
