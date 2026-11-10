"""
visualize_degree.py - Visualize degree distributions and ranking comparisons.

Generates:
  1. Top 10 most active users bar chart
  2. Degree ranking comparison chart across periods
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RANKINGS_DIR = os.path.join(PROJECT_ROOT, 'output', 'rankings')
ACTIVITY_DIR = os.path.join(PROJECT_ROOT, 'output', 'activity')


def set_style():
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams.update({
        'figure.figsize': (12, 7),
        'font.size': 12,
        'figure.dpi': 150,
    })


def plot_top_active_users():
    """Horizontal bar chart showing top 10 most active users per period."""
    active_files = sorted(glob.glob(os.path.join(RANKINGS_DIR, 'top_active_Period_*.csv')))
    if not active_files:
        print("[WARN] No top_active files found. Skipping.")
        return

    fig, axes = plt.subplots(1, len(active_files),
                              figsize=(6 * len(active_files), 7))
    if len(active_files) == 1:
        axes = [axes]

    colors = ['#1565C0', '#E65100', '#2E7D32']

    for ax, fpath, color in zip(axes, active_files, colors):
        period = os.path.basename(fpath).replace('top_active_', '').replace('.csv', '')
        df = pd.read_csv(fpath).head(10)

        bars = ax.barh(range(len(df)), df['activity_score'],
                       color=color, alpha=0.85)
        ax.set_yticks(range(len(df)))
        ax.set_yticklabels([f"User {int(uid)}" for uid in df['user_id']])
        ax.set_xlabel('Activity Score (In + Out Degree)')
        ax.set_title(f'Top 10 Active Users — {period}')
        ax.invert_yaxis()  # Highest at top

        # Add value labels
        for bar, val in zip(bars, df['activity_score']):
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    str(int(val)), va='center', fontsize=9)

    plt.suptitle('Top 10 Most Active Users by Time Period',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    outpath = os.path.join(RANKINGS_DIR, 'top_active_users.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


def plot_degree_ranking_comparison():
    """Line chart showing how user rankings changed between periods."""
    comp_files = sorted(glob.glob(
        os.path.join(RANKINGS_DIR, 'ranking_comparison_*.csv')
    ))
    if not comp_files:
        print("[WARN] No ranking comparison files found. Skipping.")
        return

    for fpath in comp_files:
        fname = os.path.basename(fpath).replace('.csv', '')
        df = pd.read_csv(fpath)

        # Take top 30 by absolute rank change
        top_movers = df.reindex(df['rank_change'].abs().sort_values(ascending=False).index).head(30)

        fig, ax = plt.subplots(figsize=(14, 8))

        for _, row in top_movers.iterrows():
            color = '#4CAF50' if row['rank_change'] > 0 else '#F44336'
            ax.plot([1, 2], [row['rank_period1'], row['rank_period2']],
                    marker='o', color=color, alpha=0.6, linewidth=1.5)
            ax.annotate(f"U{int(row['user_id'])}",
                       (2, row['rank_period2']),
                       textcoords="offset points", xytext=(5, 0),
                       fontsize=7, alpha=0.7)

        ax.set_xticks([1, 2])
        labels = fname.replace('ranking_comparison_', '').split('_vs_')
        ax.set_xticklabels(labels if len(labels) == 2 else ['Period 1', 'Period 2'])
        ax.set_ylabel('Rank (lower = more active)')
        ax.set_title(f'Degree Ranking Changes — {fname}')
        ax.invert_yaxis()

        # Custom legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='#4CAF50', marker='o', label='Rank Improved'),
            Line2D([0], [0], color='#F44336', marker='o', label='Rank Declined'),
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        outpath = os.path.join(RANKINGS_DIR, f'{fname}.png')
        plt.savefig(outpath, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: {outpath}")


def plot_senders_vs_receivers():
    """Compare top senders and receivers side by side."""
    sender_files = sorted(glob.glob(os.path.join(RANKINGS_DIR, 'top_senders_Period_*.csv')))
    receiver_files = sorted(glob.glob(os.path.join(RANKINGS_DIR, 'top_receivers_Period_*.csv')))

    if not sender_files or not receiver_files:
        print("[WARN] Missing sender/receiver files. Skipping comparison.")
        return

    n_periods = min(len(sender_files), len(receiver_files))
    fig, axes = plt.subplots(n_periods, 2, figsize=(14, 5 * n_periods))
    if n_periods == 1:
        axes = [axes]

    for i in range(n_periods):
        senders = pd.read_csv(sender_files[i]).head(10)
        receivers = pd.read_csv(receiver_files[i]).head(10)
        period = os.path.basename(sender_files[i]).replace('top_senders_', '').replace('.csv', '')

        ax_s = axes[i][0] if n_periods > 1 else axes[0][0]
        ax_r = axes[i][1] if n_periods > 1 else axes[0][1]

        ax_s.barh(range(len(senders)), senders['emails_sent'],
                  color='#FF7043', alpha=0.85)
        ax_s.set_yticks(range(len(senders)))
        ax_s.set_yticklabels([f"User {int(u)}" for u in senders['user_id']])
        ax_s.set_title(f'Top Senders — {period}')
        ax_s.invert_yaxis()

        ax_r.barh(range(len(receivers)), receivers['emails_received'],
                  color='#42A5F5', alpha=0.85)
        ax_r.set_yticks(range(len(receivers)))
        ax_r.set_yticklabels([f"User {int(u)}" for u in receivers['user_id']])
        ax_r.set_title(f'Top Receivers — {period}')
        ax_r.invert_yaxis()

    plt.suptitle('Top Senders vs Receivers Comparison',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    outpath = os.path.join(RANKINGS_DIR, 'senders_vs_receivers.png')
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: {outpath}")


if __name__ == '__main__':
    print("=" * 60)
    print("  Generating Degree & Ranking Visualizations")
    print("=" * 60)
    set_style()
    plot_top_active_users()
    plot_degree_ranking_comparison()
    plot_senders_vs_receivers()
    print("\n  Degree visualizations complete.")
