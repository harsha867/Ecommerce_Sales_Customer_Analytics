from ucimlrepo import fetch_ucirepo
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)

dataset = fetch_ucirepo(id=352)
df = dataset.data.features.copy()

# UCI returns the 8 transaction columns in this dataset.
df.to_excel(OUT / "Online Retail.xlsx", index=False)
print(f"Saved {len(df):,} rows to {OUT/'Online Retail.xlsx'}")
