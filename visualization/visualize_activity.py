"""
visualize_activity.py - Visualize email activity patterns across time windows.

Generates:
  1. Incoming vs Outgoing email interaction bar chart
  2. User activity comparison across time windows
  3. Communication activity timeline
"""

import os
import sys
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving to file

# Resolve project root (parent of visualization/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ACTIVITY_DIR = os.path.join(PROJECT_ROOT, 'output', 'activity')
GRAPHS_DIR   = os.path.join(PROJECT_ROOT, 'output', 'graphs')

def set_style():
    """Apply a professional matplotlib style."""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams.update({
        'figure.figsize': (12, 7),
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.dpi': 150,
    })

def plot_incoming_vs_outgoing():
    """Bar chart comparing incoming vs outgoing emails for top users."""
    degree_files = sorted(glob.glob(os.path.join(ACTIVITY_DIR, 'degrees_Period_*.csv')))
    if not degree_files:
        print("[WARN] No degree files found. Skipping incoming vs outgoing chart.")
        return

    fig, axes = plt.subplots(1, len(degree_files), figsize=(6 * len(degree_files), 7))
    if len(degree_files) == 1:
        axes = [axes]

    colors_in  = '#2196F3'   # Blue
    colors_out = '#FF5722'   # Orange-red

    for ax, fpath in zip(axes, degree_files):
        period = os.path.basename(fpath).replace('degrees_', '').replace('.csv', '')
        df = pd.read_csv(fpath)
        top = df.nlargest(15, 'total_degree')

        x = range(len(top))
        width = 0.35
        ax.bar([i - width/2 for i in x], top['in_degree'], width,
               label='Incoming', color=colors_in, alpha=0.85)
        ax.bar([i + width/2 for i in x], top['out_degree'], width,
               label='Outgoing', color=colors_out, alpha=0.85)

        ax.set_xlabel('User ID')
        ax.set_ylabel('Email Count')
        ax.set_title(f'In vs Out Degree — {period}')
        ax.set_xticks(list(x))
        ax.set_xticklabels(top['user_id'].astype(str), rotation=45, ha='right')
        ax.legend()

    plt.suptitle('Incoming vs Outgoing Email Interactions (Top 15 Users)',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    outpath = os.path.join(ACTIVITY_DIR, 'incoming_vs_outgoing.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


def plot_activity_comparison():
    """Compare user activity scores across time windows."""
    degree_files = sorted(glob.glob(os.path.join(ACTIVITY_DIR, 'degrees_Period_*.csv')))
    if len(degree_files) < 2:
        print("[WARN] Need at least 2 period files for comparison. Skipping.")
        return

    # Merge all periods on user_id
    merged = None
    periods = []
    for fpath in degree_files:
        period = os.path.basename(fpath).replace('degrees_', '').replace('.csv', '')
        periods.append(period)
        df = pd.read_csv(fpath)[['user_id', 'total_degree']].rename(
            columns={'total_degree': period}
        )
        if merged is None:
            merged = df
        else:
            merged = merged.merge(df, on='user_id', how='outer').fillna(0)

    # Sum across periods and take top 20
    merged['total'] = merged[periods].sum(axis=1)
    top = merged.nlargest(20, 'total')

    fig, ax = plt.subplots(figsize=(14, 7))
    x = range(len(top))
    width = 0.8 / len(periods)
    colors = ['#1976D2', '#F57C00', '#388E3C', '#7B1FA2', '#D32F2F']

    for i, period in enumerate(periods):
        offset = (i - len(periods)/2 + 0.5) * width
        ax.bar([xi + offset for xi in x], top[period], width,
               label=period, color=colors[i % len(colors)], alpha=0.85)

    ax.set_xlabel('User ID')
    ax.set_ylabel('Total Degree (Activity Score)')
    ax.set_title('User Activity Comparison Across Time Windows')
    ax.set_xticks(list(x))
    ax.set_xticklabels(top['user_id'].astype(int).astype(str), rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    outpath = os.path.join(ACTIVITY_DIR, 'activity_comparison.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


def plot_communication_timeline():
    """Plot communication activity over time using edge timestamp data."""
    edge_files = sorted(glob.glob(os.path.join(GRAPHS_DIR, 'edges_Period_*.csv')))
    if not edge_files:
        print("[WARN] No edge files found. Skipping timeline chart.")
        return

    all_edges = []
    for fpath in edge_files:
        df = pd.read_csv(fpath)
        if 'timestamp' in df.columns:
            all_edges.append(df)

    if not all_edges:
        print("[WARN] No timestamp data in edge files. Skipping timeline.")
        return

    combined = pd.concat(all_edges, ignore_index=True)
    combined['datetime'] = pd.to_datetime(combined['timestamp'], unit='s')
    combined['date'] = combined['datetime'].dt.date

    daily_counts = combined.groupby('date').size().reset_index(name='email_count')
    daily_counts['date'] = pd.to_datetime(daily_counts['date'])

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.fill_between(daily_counts['date'], daily_counts['email_count'],
                    alpha=0.3, color='#1976D2')
    ax.plot(daily_counts['date'], daily_counts['email_count'],
            color='#1976D2', linewidth=1.5)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Emails')
    ax.set_title('Communication Activity Timeline')
    plt.xticks(rotation=45)
    plt.tight_layout()
    outpath = os.path.join(ACTIVITY_DIR, 'communication_timeline.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


def plot_interactions_by_period():
    """Bar chart of total interactions per time period from SQL output."""
    sql_file = os.path.join(ACTIVITY_DIR, 'sql_interactions_by_period.csv')
    if not os.path.exists(sql_file):
        print("[WARN] sql_interactions_by_period.csv not found. Skipping.")
        return

    df = pd.read_csv(sql_file)
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['#1976D2', '#F57C00', '#388E3C', '#7B1FA2', '#D32F2F']
    bars = ax.bar(df['period'], df['total_interactions'],
                  color=colors[:len(df)], alpha=0.85)

    # Add value labels on bars
    for bar, val in zip(bars, df['total_interactions']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                f'{int(val):,}', ha='center', va='bottom', fontweight='bold')

    ax.set_xlabel('Time Period')
    ax.set_ylabel('Total Email Interactions')
    ax.set_title('Email Interactions by Time Period')
    plt.tight_layout()
    outpath = os.path.join(ACTIVITY_DIR, 'interactions_by_period.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


if __name__ == '__main__':
    print("=" * 60)
    print("  Generating Activity Visualizations")
    print("=" * 60)
    set_style()
    plot_incoming_vs_outgoing()
    plot_activity_comparison()
    plot_communication_timeline()
    plot_interactions_by_period()
    print("\n  Activity visualizations complete.")
