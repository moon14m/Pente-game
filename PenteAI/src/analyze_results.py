import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==========================================
# 1. RAW DATA (*** REPLACE THIS WITH YOUR ACTUAL LOGS ***)
# ==========================================
# Use YOUR measured Time and Node values for Alpha-Beta Pruning.
# Minimax data is estimated to highlight the pruning benefit.
data = {
    'Depth': [1, 2, 3, 4],
    
    # Minimax (Estimated - Should be much slower than Alpha-Beta)
    'Minimax_Time_ms': [15, 850, 48000, 2500000], 
    'Minimax_Nodes':   [360, 129000, 46000000, 16000000000],
    
    # Alpha-Beta Pruning (Use YOUR MEASURED values here)
    'AlphaBeta_Time_ms': [10.2, 185.5, 3450.9, 78000.1],  
    'AlphaBeta_Nodes':   [360, 15000, 310000, 7500000],
    'AlphaBeta_Memory_MB': [5, 10, 20, 35], # Use estimates or actual data
}

df = pd.DataFrame(data)

# ==========================================
# 2. GENERATE TABLES (For Section 6.2)
# ==========================================
def generate_comparison_table():
    """Generates the main comparative table in console and LaTeX format."""
    print("## 6.2.1 Quantitative Comparison Table ##")
    
    # Filter only Alpha-Beta for the clean scalability analysis
    alpha_beta_only = df[['Depth', 'AlphaBeta_Time_ms', 'AlphaBeta_Memory_MB', 'AlphaBeta_Nodes']].copy()
    alpha_beta_only.columns = ['Depth', 'Avg Time (ms)', 'Memory (MB)', 'Nodes Explored']
    
    print("\n--- COMPARISON TABLE FOR REPORT (Alpha-Beta Scalability) ---")
    print(alpha_beta_only.to_string(index=False))
    
    print("\n--- LATEX TABLE OUTPUT (For professional reports) ---")
    print(alpha_beta_only.to_latex(
        index=False, 
        caption="Alpha-Beta Performance Metrics vs. Search Depth", 
        float_format="%.2f"
    ))

# ==========================================
# 3. GENERATE GRAPHS (For Section 6.2 & 6.3)
# ==========================================
def plot_results():
    """Generates the three required comparative graphs."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # --- Graph A: Execution Time vs Search Depth (Section 6.2) ---
    axes[0].plot(df['Depth'], df['Minimax_Time_ms'], marker='o', label='Basic Minimax (Est.)', color='red', linestyle='--')
    axes[0].plot(df['Depth'], df['AlphaBeta_Time_ms'], marker='s', label='Alpha-Beta Pruning', color='green', linewidth=2)
    axes[0].set_yscale('log')
    axes[0].set_title('Execution Time vs Search Depth (Log Scale)')
    axes[0].set_ylabel('Time (ms)')
    axes[0].set_xlabel('Search Depth')
    axes[0].grid(True, which="both", ls="-", alpha=0.5)
    axes[0].legend()
    # 

    # --- Graph B: Pruning Efficiency / Nodes Expanded (Section 6.2) ---
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
    # 

    # --- Graph C: Empirical vs Theoretical Complexity (Section 6.3) ---
    # Theoretical curve fit for Alpha-Beta: O(b^(d/2))
    b_star = 25 # Estimated effective branching factor
    theoretical_y = [b_star**(d/2) for d in df['Depth']]
    
    scale_factor = df['AlphaBeta_Nodes'][0] / theoretical_y[0]
    theoretical_y = [y * scale_factor for y in theoretical_y]

    axes[2].plot(df['Depth'], df['AlphaBeta_Nodes'], marker='s', label='Empirical (Actual Nodes)', color='blue')
    axes[2].plot(df['Depth'], theoretical_y, linestyle=':', label=f'Theoretical $O(b^{{d/2}})$ where $b={b_star}$', color='black')
    axes[2].set_title('Alpha-Beta: Empirical vs Theoretical Complexity')
    axes[2].set_yscale('log')
    axes[2].set_xlabel('Depth')
    axes[2].set_ylabel('Nodes Explored (Log Scale)')
    axes[2].legend()
    # 

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("--- PENTE AI RESULTS ANALYSIS ---")
    generate_comparison_table()
    plot_results()