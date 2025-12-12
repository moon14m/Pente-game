import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Ensure plots are saved to the current directory
# and use Agg backend for non-interactive environments
plt.switch_backend('Agg')

data = {
    'Depth': [1, 2, 3, 4],

    'Minimax_Time_ms': [15, 850, 48000, 2500000], 
    'Minimax_Nodes':   [360, 129000, 46000000, 16000000000],
    # Minimax memory is assumed to be the same as Alpha-Beta, as memory complexity 
    # (maximum depth * state size) is identical for both algorithms.
    'Minimax_Memory_MB': [2, 4, 15, 50], 
    
    
    'AlphaBeta_Time_ms': [10, 120, 2100, 45000],  
    'AlphaBeta_Nodes':   [360, 9000, 250000, 6000000],
    'AlphaBeta_Memory_MB': [2, 4, 15, 50],       
}

df = pd.DataFrame(data)


def generate_comparison_table(df):
    """Generates the main comparative table (for copy/pasting into the report)."""
    print("## 6.2.1 Quantitative Comparison Table ##")
    
    # Create the full comparison DataFrame
    comparison_df = pd.DataFrame({
        'Algorithm': ['Minimax (Est.)'] * len(df) + ['Alpha-Beta'] * len(df),
        'Depth': list(df['Depth']) * 2,
        'Avg Time (ms)': list(df['Minimax_Time_ms']) + list(df['AlphaBeta_Time_ms']),
        'Nodes Explored': list(df['Minimax_Nodes']) + list(df['AlphaBeta_Nodes']),
        # Uses the common memory values for both
        'Memory (MB)': list(df['Minimax_Memory_MB']) + list(df['AlphaBeta_Memory_MB']),
    })
    
    # --- Full Comparison Table ---
    print("\n--- FULL MINIMAX VS ALPHA-BETA COMPARISON TABLE (Raw) ---")
    print(comparison_df.to_string(index=False))
    
    # Custom format function for Nodes Explored to include thousands separator
    node_formatter = lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x
    
    # --- Alpha-Beta Scalability Table ---
    alpha_beta_only = comparison_df[comparison_df['Algorithm'] == 'Alpha-Beta'].reset_index(drop=True)
    
    print("\n--- LATEX FORMAT (Alpha-Beta Scalability Table) ---")
    latex_output_ab = alpha_beta_only[['Depth', 'Avg Time (ms)', 'Memory (MB)', 'Nodes Explored']].to_latex(
        index=False, 
        caption="Alpha-Beta Pruning Performance Metrics vs. Search Depth", 
        label="tab:alpha_beta_scalability",
        column_format="cccc",
        float_format={"Avg Time (ms)": "%.2f", "Memory (MB)": "%.2f", "Nodes Explored": node_formatter}
    )
    print(latex_output_ab)
    
    # --- Full Latex Comparison Table ---
    print("\n--- LATEX FORMAT (Minimax vs. Alpha-Beta Comparison Table) ---")
    full_latex_output = comparison_df[['Algorithm', 'Depth', 'Avg Time (ms)', 'Nodes Explored', 'Memory (MB)']].to_latex(
        index=False, 
        caption="Comparative Performance of Minimax vs. Alpha-Beta Pruning", 
        label="tab:minimax_comparison",
        column_format="cclll",
        float_format={"Avg Time (ms)": "%.2f", "Memory (MB)": "%.2f", "Nodes Explored": node_formatter}
    )
    print(full_latex_output)


def plot_results(df):
    """Generates the three required comparative graphs."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot 1: Execution Time Comparison
    axes[0].plot(df['Depth'], df['Minimax_Time_ms'], marker='o', label='Basic Minimax (Est.)', color='red', linestyle='--')
    axes[0].plot(df['Depth'], df['AlphaBeta_Time_ms'], marker='s', label='Alpha-Beta Pruning', color='green', linewidth=2)
    axes[0].set_yscale('log') # Log scale is vital
    axes[0].set_title('Execution Time vs Search Depth (Log Scale)')
    axes[0].set_ylabel('Time (ms)')
    axes[0].set_xlabel('Search Depth')
    axes[0].grid(True, which="both", ls="-", alpha=0.5)
    axes[0].legend()
    
    # Plot 2: Nodes Explored Comparison (Bar Chart)
    bar_width = 0.35
    index = np.arange(len(df['Depth']))
    
    axes[1].bar(index, df['Minimax_Nodes'], bar_width, label='Minimax Nodes (Est.)', color='salmon', alpha=0.7)
    axes[1].bar(index + bar_width, df['AlphaBeta_Nodes'], bar_width, label='Alpha-Beta Nodes', color='lightgreen')
    axes[1].set_yscale('log') 
    axes[1].set_title('Nodes Expanded Comparison (Pruning Efficiency)')
    axes[1].set_xticks(index + bar_width / 2)
    axes[1].set_xticklabels(df['Depth'])
    axes[1].set_ylabel('Nodes Explored (Log Scale)')
    axes[1].set_xlabel('Depth')
    axes[1].legend()
    
    # Plot 3: Alpha-Beta Empirical vs Theoretical Complexity
    b_star = 25 
    theoretical_y = [b_star**(d/2) for d in df['Depth']]
    
    # Scale the theoretical curve to match the empirical data at depth 1 for alignment
    scale_factor = df['AlphaBeta_Nodes'][0] / theoretical_y[0]
    theoretical_y = [y * scale_factor for y in theoretical_y]

    axes[2].plot(df['Depth'], df['AlphaBeta_Nodes'], marker='s', label='Empirical (Actual Nodes)', color='blue')
    axes[2].plot(df['Depth'], theoretical_y, linestyle=':', label=f'Theoretical $O(b^{{d/2}})$ where $b={b_star}$', color='black')
    axes[2].set_title('Alpha-Beta: Empirical vs Theoretical Complexity')
    axes[2].set_yscale('log')
    axes[2].set_xlabel('Depth')
    axes[2].set_ylabel('Nodes Explored (Log Scale)')
    axes[2].grid(True, which="both", ls="-", alpha=0.5)
    axes[2].legend()
    
    # Save the combined figure
    plt.tight_layout()
    plt.savefig('performance_comparison_plots.png')

if __name__ == '__main__':
    generate_comparison_table(df)
    plot_results(df)