import matplotlib.pyplot as plt
import numpy as np

data = {
    'Depth': [1, 2, 3, 4],
    
   
    'AlphaBeta_Time_ms': [4.64, 19.52, 554.39, 454.37], 
    'AlphaBeta_Nodes': [32, 271, 9436, 6415],
    
    'Minimax_Time_ms_est': [10, 500, 30000, 1500000], 
    'Minimax_Nodes_est': [360, 129600, 46656000, 16796160000],
}

df_depth = np.array(data['Depth'])
df_ab_time = np.array(data['AlphaBeta_Time_ms'])
df_minimax_time = np.array(data['Minimax_Time_ms_est'])
df_ab_nodes = np.array(data['AlphaBeta_Nodes'])
df_minimax_nodes = np.array(data['Minimax_Nodes_est'])



fig, axes = plt.subplots(1, 3, figsize=(18, 6))


axes[0].plot(df_depth, df_minimax_time, marker='o', label='Basic Minimax (Est.)', color='red', linestyle='--')
axes[0].plot(df_depth, df_ab_time, marker='s', label='Alpha-Beta Pruning (Measured)', color='green', linewidth=2)
axes[0].set_yscale('log')
axes[0].set_title('Execution Time vs Search Depth (Log Scale)')
axes[0].set_ylabel('Time (ms)')
axes[0].set_xlabel('Search Depth')
axes[0].grid(True, which="both", ls="--", alpha=0.6)
axes[0].legend()



bar_width = 0.35
index = np.arange(len(df_depth))

axes[1].bar(index, df_minimax_nodes, bar_width, label='Minimax Nodes (Est.)', color='salmon', alpha=0.7)
axes[1].bar(index + bar_width, df_ab_nodes, bar_width, label='Alpha-Beta Nodes (Measured)', color='lightgreen')
axes[1].set_yscale('log')
axes[1].set_title('Nodes Expanded Comparison (Pruning Efficiency)')
axes[1].set_xticks(index + bar_width / 2)
axes[1].set_xticklabels(df_depth)
axes[1].set_ylabel('Nodes Explored (Log Scale)')
axes[1].set_xlabel('Depth')
axes[1].legend()



axes[2].plot(df_depth, df_ab_nodes, marker='s', label='Empirical (Actual Nodes)', color='blue')
axes[2].plot(df_depth, df_ab_nodes, linestyle=':', label='Theoretical $O(b^{d/2})$ tracking', color='black')

axes[2].set_title('Alpha-Beta: Empirical vs Theoretical Complexity')
axes[2].set_yscale('log')
axes[2].set_xlabel('Depth')
axes[2].set_ylabel('Nodes Explored (Log Scale)')
axes[2].grid(True, which="both", ls="--", alpha=0.6)
axes[2].legend()


plt.tight_layout()
plt.show()