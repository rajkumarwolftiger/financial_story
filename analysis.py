#!/usr/bin/env python3
"""
analysis.py

Simple script to process 2024 quarterly CAC data, compute averages,
and produce a benchmarking visualization saved to `outputs/cac_trend.png`.

This file is intended to be included in the repository PR for the
CAC Performance Analysis and Data Story.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    # 2024 quarterly CAC data (provided dataset)
    data = {
        "Quarter": ["Q1", "Q2", "Q3", "Q4"],
        "CAC": [225.38, 232.3, 231.35, 229.83],
    }

    df = pd.DataFrame(data)

    # Calculate average CAC and print (rounded to 2 decimals)
    average_cac = round(df["CAC"].mean(), 2)
    print(f"Average CAC: {average_cac:.2f}")

    # Create outputs directory
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)

    # Save the data as CSV for reproducibility
    csv_path = os.path.join(out_dir, "cac_2024.csv")
    df.to_csv(csv_path, index=False)

    # Visualization
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    ax = sns.lineplot(x="Quarter", y="CAC", data=df, marker="o", linewidth=2, markersize=8)

    # Add industry benchmark
    industry_target = 150
    ax.axhline(industry_target, color="red", linestyle="--", linewidth=2, label=f"Industry Target ({industry_target})")

    # Annotate points with CAC values
    for i, row in df.iterrows():
        ax.text(i, row["CAC"] + 1.5, f"{row['CAC']:.2f}", ha="center", fontsize=10)

    # Chart decoration
    ax.set_title("Quarterly Customer Acquisition Cost (CAC) Trend - 2024", fontsize=14)
    ax.set_xlabel("Quarter")
    ax.set_ylabel("CAC ($)")
    ax.set_ylim(min(industry_target, df["CAC"].min()) - 10, df["CAC"].max() + 10)
    ax.legend()

    out_png = os.path.join(out_dir, "cac_trend.png")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

    print(f"Saved CSV: {csv_path}")
    print(f"Saved visualization: {out_png}")
    # Print the exact average required in README verification
    # (ensures the value appears in outputs or logs)
    print(f"VERIFICATION_AVERAGE:{average_cac:.2f}")


if __name__ == "__main__":
    main()
