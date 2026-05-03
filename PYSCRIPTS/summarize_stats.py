import pandas as pd
import matplotlib.pyplot as plt

def temp_dist_hist(data, bins=30):
    avg_mean_temp = data['mean_temp'].mean()
    avg_std_temp = data['std_temp'].mean()
    print(f"Average Mean Temperature: {avg_mean_temp:.2f}")
    print(f"Average Standard Deviation of Temperature: {avg_std_temp:.2f}")
    fig, ax = plt.subplots(dpi = 600)
    ax.hist(data['mean_temp'], bins=bins, edgecolor='black')
    ax.set_xlabel('Mean Temperature')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of Mean Temperatures, avg mean: {(avg_mean_temp):.2f}, avg std: {(avg_std_temp):.2f}')
    plt.savefig("PLOTS/mean_temp_histogram.png")

def temp_limit_breaches(data):
    """
    Computes how many buildings have at least 50% of their interior temperatures above 18°C or below 15°C respectively.
    """
    above_18 = (data['pct_above_18'] > 50).sum()
    below_15 = (data['pct_below_15'] > 50).sum()
    print(f"Buildings with >50% of interior temperatures above 18°C: {above_18}")
    print(f"Buildings with >50% of interior temperatures below 15°C: {below_15}")

if __name__ == "__main__":
    data = pd.read_csv('OUTPUTS/full_stats1.csv', skipinitialspace=True)
    temp_dist_hist(data)
    temp_limit_breaches(data)
