# compare.py
import glob
import matplotlib.pyplot as plt
import pandas as pd

def load(prefix):
    rows = []
    for path in sorted(glob.glob(f"{prefix}_*.csv")):
        df = pd.read_csv(path)
        busy = df[df["vehicles"] > 0]
        rows.append({
            "file": path,
            "avg_wait": busy["avg_wait_s"].mean(),
            "queue": busy["queue"].mean(),
            "max_queue": busy["queue"].max(),
        })
    return pd.DataFrame(rows)

fixed_sum = load("metrics_fixed")
adapt_sum = load("metrics_adaptive")

print("FIXED")
print(fixed_sum.to_string(index=False))
print("\nADAPTIVE")
print(adapt_sum.to_string(index=False))

print("\nSUMMARY (mean +/- std over seeds)")
for name, df in [("Fixed", fixed_sum), ("Adaptive", adapt_sum)]:
    print(f"{name}:")
    print(f"  avg wait: {df['avg_wait'].mean():.2f} +/- {df['avg_wait'].std():.2f} s")
    print(f"  queue:    {df['queue'].mean():.2f} +/- {df['queue'].std():.2f} veh")
    print(f"  max queue: {df['max_queue'].mean():.2f} veh")

# ---- time series: seed 1 of each controller, like the reference plot ----
fixed = pd.read_csv("metrics_fixed_1.csv")
adapt = pd.read_csv("metrics_adaptive_1.csv")

fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

ax[0].plot(fixed["step"], fixed["avg_wait_s"], label="Fixed", alpha=0.7)
ax[0].plot(adapt["step"], adapt["avg_wait_s"], label="Adaptive", alpha=0.7)
ax[0].set_ylabel("Avg wait (s)")
ax[0].set_title("Average waiting time per step")
ax[0].legend()

ax[1].plot(fixed["step"], fixed["queue"], label="Fixed", alpha=0.7)
ax[1].plot(adapt["step"], adapt["queue"], label="Adaptive", alpha=0.7)
ax[1].set_ylabel("Halting vehicles")
ax[1].set_xlabel("Sim step (s)")
ax[1].set_title("Queue length on all approaches")
ax[1].legend()

plt.tight_layout()
plt.savefig("comparison.png", dpi=150)
print("\ncomparison.png written")