"""
visualize_components.py - Visualize connected component analysis results.

Generates:
  1. Connected component comparison bar chart across periods
  2. Component size distribution chart
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

PROJECT_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
COMPONENTS_DIR = os.path.join(PROJECT_ROOT, 'output', 'components')


def set_style():
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams.update({
        'figure.figsize': (12, 7),
        'font.size': 12,
        'figure.dpi': 150,
    })


def plot_component_comparison():
    """Bar chart comparing connected component metrics across periods."""
    comp_file = os.path.join(COMPONENTS_DIR, 'component_comparison.csv')
    if not os.path.exists(comp_file):
        print("[WARN] component_comparison.csv not found. Skipping.")
        return

    df = pd.read_csv(comp_file)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Chart 1: Number of components
    colors1 = ['#1976D2', '#F57C00', '#388E3C']
    axes[0].bar(df['period'], df['num_components'],
                color=colors1[:len(df)], alpha=0.85)
    axes[0].set_title('Number of Connected Components')
    axes[0].set_ylabel('Count')
    for i, v in enumerate(df['num_components']):
        axes[0].text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    # Chart 2: Largest component size
    axes[1].bar(df['period'], df['largest_component_size'],
                color=colors1[:len(df)], alpha=0.85)
    axes[1].set_title('Largest Component Size')
    axes[1].set_ylabel('Number of Vertices')
    for i, v in enumerate(df['largest_component_size']):
        axes[1].text(i, v + 1, str(v), ha='center', fontweight='bold')

    # Chart 3: Isolated nodes
    axes[2].bar(df['period'], df['isolated_nodes'],
                color=colors1[:len(df)], alpha=0.85)
    axes[2].set_title('Isolated Nodes')
    axes[2].set_ylabel('Count')
    for i, v in enumerate(df['isolated_nodes']):
        axes[2].text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    plt.suptitle('Connected Component Comparison Across Time Periods',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    outpath = os.path.join(COMPONENTS_DIR, 'component_comparison.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


def plot_component_size_distribution():
    """Distribution of component sizes for each period."""
    size_files = sorted(glob.glob(
        os.path.join(COMPONENTS_DIR, 'component_sizes_Period_*.csv')
    ))
    if not size_files:
        print("[WARN] No component_sizes files found. Skipping.")
        return

    fig, axes = plt.subplots(1, len(size_files),
                              figsize=(6 * len(size_files), 6))
    if len(size_files) == 1:
        axes = [axes]

    colors = ['#1565C0', '#E65100', '#2E7D32']

    for ax, fpath, color in zip(axes, size_files, colors):
        period = os.path.basename(fpath).replace('component_sizes_', '').replace('.csv', '')
        df = pd.read_csv(fpath)

        # Group by component size and count how many components have that size
        size_dist = df.groupby('size').size().reset_index(name='count')

        ax.bar(size_dist['size'].astype(str), size_dist['count'],
               color=color, alpha=0.85)
        ax.set_xlabel('Component Size')
        ax.set_ylabel('Number of Components')
        ax.set_title(f'Component Size Distribution — {period}')

        # Only show a subset of x-ticks if too many
        if len(size_dist) > 15:
            step = max(1, len(size_dist) // 10)
            ax.set_xticks(range(0, len(size_dist), step))

    plt.suptitle('Component Size Distribution by Period',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    outpath = os.path.join(COMPONENTS_DIR, 'component_size_distribution.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


def plot_connectivity_summary():
    """Stacked bar chart showing connected vs isolated nodes per period."""
    comp_file = os.path.join(COMPONENTS_DIR, 'component_comparison.csv')
    if not os.path.exists(comp_file):
        print("[WARN] component_comparison.csv not found. Skipping connectivity summary.")
        return

    df = pd.read_csv(comp_file)
    df['connected_nodes'] = df['total_vertices'] - df['isolated_nodes']

    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(df))
    ax.bar(x, df['connected_nodes'], label='Connected', color='#4CAF50', alpha=0.85)
    ax.bar(x, df['isolated_nodes'], bottom=df['connected_nodes'],
           label='Isolated', color='#F44336', alpha=0.85)

    ax.set_xticks(list(x))
    ax.set_xticklabels(df['period'])
    ax.set_ylabel('Number of Users')
    ax.set_title('Network Connectivity: Connected vs Isolated Users')
    ax.legend()

    plt.tight_layout()
    outpath = os.path.join(COMPONENTS_DIR, 'connectivity_summary.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


if __name__ == '__main__':
    print("=" * 60)
    print("  Generating Component Visualizations")
    print("=" * 60)
    set_style()
    plot_component_comparison()
    plot_component_size_distribution()
    plot_connectivity_summary()
    print("\n  Component visualizations complete.")
