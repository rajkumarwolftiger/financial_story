import marimo

__generated_with = "0.1.0"
app = marimo.App()


@app.cell
def __():
    """
    Marimo Interactive Data Analysis Notebook
    
    Email for verification: 24f1002577@ds.study.iitm.ac.in
    
    This notebook demonstrates interactive data analysis with:
    - Variable dependencies across cells
    - Interactive slider widgets
    - Dynamic markdown output
    - Data flow documentation
    """
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    return mo, pd, np, plt


@app.cell
def __(mo):
    """
    CELL 2: User Input - Interactive Slider Widget
    
    This cell creates an interactive slider to control analysis parameters.
    The slider value flows downstream to cells that use 'threshold_value'.
    """
    mo.md("""
    # Customer Acquisition Cost (CAC) Interactive Analysis
    
    **Verification Email:** 24f1002577@ds.study.iitm.ac.in
    
    Use the slider below to dynamically adjust the CAC threshold for channel optimization.
    """)
    
    # Interactive slider: CAC threshold (ranges from 100 to 250)
    threshold_slider = mo.ui.slider(
        value=180,
        start=100,
        stop=250,
        step=5,
        label="Select CAC Threshold ($):"
    )
    
    mo.md(f"""
    **Current Threshold:** ${threshold_slider.value}
    
    This threshold determines which channels are considered "efficient" (CAC below threshold).
    """)
    
    return threshold_slider


@app.cell
def __(mo):
    """
    CELL 3: Load and Prepare Dataset
    
    This cell loads the 2024 quarterly CAC data.
    Dependency: None (source data)
    Data flows to: cells analyzing channel performance
    """
    
    # 2024 Quarterly CAC Data
    data_dict = {
        "Quarter": ["Q1", "Q2", "Q3", "Q4"],
        "CAC": [225.38, 232.30, 231.35, 229.83],
        "Channel": ["Paid Search", "Social Ads", "Organic", "Referral"],
    }
    
    cac_data = pd.DataFrame(data_dict)
    
    # Add a simulated channel cost efficiency score (0-100)
    np.random.seed(42)
    cac_data["Efficiency_Score"] = np.random.randint(40, 90, len(cac_data))
    
    return cac_data


@app.cell
def __(cac_data, threshold_slider, mo):
    """
    CELL 4: Dynamic Analysis Based on Threshold
    
    DEPENDENCIES:
    - cac_data (from Cell 3): Source dataset
    - threshold_slider.value (from Cell 2): User-selected threshold
    
    This cell filters the dataset based on the slider value and generates
    dynamic markdown output that updates in real-time as the slider changes.
    """
    
    threshold = threshold_slider.value
    
    # Filter channels by CAC threshold
    efficient_channels = cac_data[cac_data["CAC"] <= threshold]
    inefficient_channels = cac_data[cac_data["CAC"] > threshold]
    
    average_cac = cac_data["CAC"].mean()
    
    # Dynamic markdown output based on threshold
    analysis_text = f"""
    ## Analysis Results (Threshold: ${threshold})
    
    **Average CAC (2024):** ${average_cac:.2f}
    
    **Industry Benchmark:** $150
    
    **Channels Below Threshold (${threshold}):** {len(efficient_channels)}
    
    **Channels Above Threshold (${threshold}):** {len(inefficient_channels)}
    
    ### Efficient Channels (CAC ≤ ${threshold}):
    """
    
    if len(efficient_channels) > 0:
        for idx, row in efficient_channels.iterrows():
            analysis_text += f"\n- **{row['Channel']}** (Q{row['Quarter'][-1]}): ${row['CAC']:.2f} - Efficiency: {row['Efficiency_Score']}/100"
    else:
        analysis_text += "\n*No channels meet this threshold. Consider raising the threshold.*"
    
    analysis_text += f"\n\n### Inefficient Channels (CAC > ${threshold}):\n"
    
    if len(inefficient_channels) > 0:
        for idx, row in inefficient_channels.iterrows():
            analysis_text += f"\n- **{row['Channel']}** (Q{row['Quarter'][-1]}): ${row['CAC']:.2f} - Efficiency: {row['Efficiency_Score']}/100"
    else:
        analysis_text += "\n*All channels meet the threshold. Consider lowering for stricter filtering.*"
    
    mo.md(analysis_text)
    
    return threshold, efficient_channels, inefficient_channels, average_cac


@app.cell
def __(cac_data, mo):
    """
    CELL 5: Data Summary Table
    
    DEPENDENCY: cac_data (from Cell 3)
    
    Displays the dataset in a formatted table.
    """
    
    mo.md("""
    ## Dataset Summary
    
    The table below shows the quarterly CAC data with efficiency scores:
    """)
    
    # Create a formatted table
    table_html = cac_data.to_html(index=False)
    mo.md(table_html)
    
    return None


@app.cell
def __(cac_data, mo, plt):
    """
    CELL 6: Visualization
    
    DEPENDENCY: cac_data (from Cell 3)
    
    Creates a bar chart showing CAC by channel.
    """
    
    mo.md("""
    ## CAC by Channel Visualization
    """)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    channels = cac_data["Channel"].unique()
    cac_values = cac_data.groupby("Channel")["CAC"].mean()
    
    bars = ax.bar(cac_values.index, cac_values.values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    # Add benchmark line
    ax.axhline(y=150, color='red', linestyle='--', linewidth=2, label='Industry Benchmark ($150)')
    
    ax.set_title('Average CAC by Channel - 2024', fontsize=14, fontweight='bold')
    ax.set_xlabel('Channel')
    ax.set_ylabel('CAC ($)')
    ax.set_ylim(0, max(cac_values.values) + 30)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.2f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('marimo_cac_analysis.png', dpi=200)
    plt.show()
    
    return fig


@app.cell
def __(mo, average_cac):
    """
    CELL 7: Summary & Recommendations
    
    DEPENDENCY: average_cac (from Cell 4)
    
    Provides final recommendations based on the analysis.
    """
    
    gap_to_benchmark = average_cac - 150
    percent_above = (gap_to_benchmark / 150) * 100
    
    mo.md(f"""
    ## Summary & Recommendations
    
    ### Key Metrics:
    - **Average CAC:** ${average_cac:.2f}
    - **Industry Benchmark:** $150
    - **Gap:** ${gap_to_benchmark:.2f} ({percent_above:.1f}% above benchmark)
    
    ### Recommendation: Optimize Digital Marketing Channels
    
    1. **Identify High-Efficiency Channels:** Use the slider above to find channels with CAC ≤ your target threshold.
    2. **Reallocate Budget:** Move spend from inefficient to efficient channels.
    3. **Test & Iterate:** Run A/B tests to improve conversion rates and lower CAC.
    4. **Monitor Performance:** Track CAC weekly and adjust strategies monthly.
    
    ### Expected Outcome:
    By implementing these optimizations, the company can reduce CAC by 30-35% within 6-9 months,
    reaching closer to the industry benchmark of $150.
    
    ---
    
    **Verification Email:** 24f1002577@ds.study.iitm.ac.in
    
    **LLM Assistance:** This notebook was created with assistance from Jules (ChatGPT Codex) and GitHub Copilot.
    """)
    
    return None


if __name__ == "__main__":
    app.run()
