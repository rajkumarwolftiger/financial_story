# analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# Step 1: Store quarterly CAC data
# =========================
data = {
    "Quarter": ["Q1", "Q2", "Q3", "Q4"],
    "CAC": [230.3, 229.35, 227.83, 230.88]
}

df = pd.DataFrame(data)

# Calculate average CAC
average_cac = df["CAC"].mean()
print(f"Average CAC: {average_cac:.2f}")

# =========================
# Step 2: Create a professional line chart
# =========================
sns.set(style="whitegrid", palette="muted")
plt.figure(figsize=(10,6))

# Plot the CAC trend
sns.lineplot(x="Quarter", y="CAC", data=df, marker="o", linewidth=2, markersize=8, label="Quarterly CAC")

# Add industry benchmark line
industry_target = 150
plt.axhline(industry_target, color="red", linestyle="--", linewidth=2, label="Industry Target (150)")

# Chart title and labels
plt.title("Quarterly Customer Acquisition Cost (CAC) Trend - 2024", fontsize=16)
plt.xlabel("Quarter", fontsize=12)
plt.ylabel("CAC ($)", fontsize=12)
plt.legend()
plt.xticks(df["Quarter"])
plt.ylim(140, max(df["CAC"].max() + 10, industry_target + 10))

# Save the visualization as a PNG
plt.tight_layout()
plt.savefig("cac_visualization.png")
plt.show()

print("Visualization saved as 'cac_visualization.png'.")
