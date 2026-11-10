"""
visualize_network.py - Visualize the email communication network graph
using NetworkX and Matplotlib.

Generates:
  1. Email communication network graph for each period
  2. Combined multi-period network visualization
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import networkx as nx
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GRAPHS_DIR   = os.path.join(PROJECT_ROOT, 'output', 'graphs')


def set_style():
    plt.rcParams.update({
        'figure.figsize': (12, 10),
        'font.size': 10,
        'figure.dpi': 150,
    })


def plot_network_graph():
    """Render the email communication network for each period."""
    edge_files = sorted(glob.glob(os.path.join(GRAPHS_DIR, 'edges_Period_*.csv')))
    if not edge_files:
        print("[WARN] No edge files found. Skipping network visualization.")
        return

    for fpath in edge_files:
        period = os.path.basename(fpath).replace('edges_', '').replace('.csv', '')
        df = pd.read_csv(fpath)

        if df.empty:
            print(f"  [SKIP] {period}: no edges")
            continue

        # Build directed graph
        G = nx.DiGraph()
        for _, row in df.iterrows():
            G.add_edge(int(row['source']), int(row['destination']))

        # For very large graphs, sample edges for visualization clarity
        if G.number_of_edges() > 5000:
            print(f"  [INFO] {period}: {G.number_of_edges()} edges — sampling top 200 nodes")
            # Keep only top 200 nodes by degree
            top_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:200]
            top_node_ids = set(n for n, _ in top_nodes)
            G = G.subgraph(top_node_ids).copy()

        fig, ax = plt.subplots(figsize=(14, 12))

        # Use spring layout for node positioning
        pos = nx.spring_layout(G, k=0.3, iterations=50, seed=42)

        # Node sizes proportional to degree
        degrees = dict(G.degree())
        max_deg = max(degrees.values()) if degrees else 1
        node_sizes = [30 + 200 * (degrees.get(n, 0) / max_deg) for n in G.nodes()]

        # Node colors by in-degree
        in_degrees = dict(G.in_degree())
        node_colors = [in_degrees.get(n, 0) for n in G.nodes()]

        # Draw
        nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.1,
                                edge_color='#90A4AE', arrows=True,
                                arrowsize=5, width=0.3)
        nodes = nx.draw_networkx_nodes(G, pos, ax=ax,
                                        node_size=node_sizes,
                                        node_color=node_colors,
                                        cmap=plt.cm.YlOrRd,
                                        alpha=0.8)

        # Add labels for top 15 nodes by degree
        top_labels = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:15]
        label_dict = {n: str(n) for n, _ in top_labels}
        nx.draw_networkx_labels(G, pos, label_dict, ax=ax,
                                 font_size=7, font_weight='bold')

        plt.colorbar(nodes, ax=ax, label='In-Degree', shrink=0.6)
        ax.set_title(f'Email Communication Network — {period}\n'
                     f'Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}',
                     fontsize=14, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()
        outpath = os.path.join(GRAPHS_DIR, f'network_{period}.png')
        plt.savefig(outpath, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {outpath}")


def plot_degree_distribution():
    """Plot the degree distribution of the network."""
    edge_files = sorted(glob.glob(os.path.join(GRAPHS_DIR, 'edges_Period_*.csv')))
    if not edge_files:
        return

    fig, ax = plt.subplots(figsize=(12, 7))
    colors = ['#1976D2', '#F57C00', '#388E3C']

    for fpath, color in zip(edge_files, colors):
        period = os.path.basename(fpath).replace('edges_', '').replace('.csv', '')
        df = pd.read_csv(fpath)
        if df.empty:
            continue

        G = nx.DiGraph()
        for _, row in df.iterrows():
            G.add_edge(int(row['source']), int(row['destination']))

        degrees = [d for _, d in G.degree()]
        if not degrees:
            continue

        # Histogram
        bins = min(50, max(degrees) - min(degrees) + 1)
        ax.hist(degrees, bins=bins, alpha=0.5, label=period, color=color,
                edgecolor='white', linewidth=0.5)

    ax.set_xlabel('Degree')
    ax.set_ylabel('Number of Nodes')
    ax.set_title('Degree Distribution Across Time Periods')
    ax.legend()
    ax.set_yscale('log')

    plt.tight_layout()
    outpath = os.path.join(GRAPHS_DIR, 'degree_distribution.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


if __name__ == '__main__':
    print("=" * 60)
    print("  Generating Network Visualizations")
    print("=" * 60)
    set_style()
    plot_network_graph()
    plot_degree_distribution()
    print("\n  Network visualizations complete.")
