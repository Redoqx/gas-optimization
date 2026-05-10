"""
Generate 4 visualisasi Bagian 4.6 untuk dataset 50 kontrak.
Output: results_50/figures/chart1–chart4.png

Run: conda run -n gas_opt python scripts/generate_visualisasi_50.py
"""

import sys, json
import numpy as np
from pathlib import Path
from scipy.stats import spearmanr

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

ROOT        = Path(__file__).parent.parent
RESULTS_DIR = ROOT / 'results_50'
FIGURES_DIR = RESULTS_DIR / 'figures'
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DETECTOR_NAMES = [
    'redundant_sload', 'unoptimized_loop', 'string_vs_bytes32',
    'public_vs_external', 'unchecked_arithmetic', 'dead_code',
]
DOMAINS = ['DeFi', 'NFT', 'Token', 'Governance', 'Utility']
GAS_DETECTORS_SLITHER = {
    'costly-loop', 'dead-code', 'unused-return',
    'cache-array-length', 'storage-array', 'redundant-statements',
}

# ── Load data ──────────────────────────────────────────────────────────────
with open(RESULTS_DIR / 'pekan2_detector_results.json', encoding='utf-8') as f:
    p2 = json.load(f)
with open(RESULTS_DIR / 'pekan3_gas_benchmark.json', encoding='utf-8') as f:
    bench = json.load(f)
with open(RESULTS_DIR / 'pekan3_slither_results.json', encoding='utf-8') as f:
    slither_results = json.load(f)

compiled = [r for r in p2 if r.get('compile_ok', True)]
GAS_DIFF = {r['pattern']: r['diff_gas']  for r in bench}

est_savings = {
    r['nama']: sum(r.get(d, 0) * GAS_DIFF.get(d, 0) for d in DETECTOR_NAMES)
    for r in compiled
}

plt.rcParams.update({
    'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 11,
    'figure.dpi': 120, 'savefig.dpi': 150, 'savefig.bbox': 'tight',
})

print(f"Dataset: {len(compiled)} contracts, {len(DOMAINS)} domains")


# ── Chart 1: Bar — Gas Savings per Anti-Pattern ───────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
patterns  = [r['pattern']  for r in bench]
pct_saves = [r['pct_save'] for r in bench]
colors    = ['#2ecc71' if p > 0 else '#bdc3c7' for p in pct_saves]

bars = ax.bar(range(len(patterns)), pct_saves, color=colors,
              edgecolor='white', linewidth=0.8)
for bar, val in zip(bars, pct_saves):
    if val > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title('Gas Savings per Anti-Pattern\n(Benchmark Hardhat, optimizer=off, solc 0.8.20)', pad=12)
ax.set_ylabel('Penghematan Gas (%)')
ax.set_xlabel('Anti-Pattern')
ax.set_xticks(range(len(patterns)))
ax.set_xticklabels(patterns, rotation=20, ha='right')
ax.set_ylim(0, max(pct_saves) * 1.18)
ax.axhline(0, color='black', linewidth=0.7)
ax.legend(handles=[
    mpatches.Patch(color='#2ecc71', label='Penghematan positif'),
    mpatches.Patch(color='#bdc3c7', label='Tidak ada penghematan (dead_code)'),
], loc='upper left')
ax.grid(axis='y', alpha=0.35)
fig.tight_layout()
out1 = FIGURES_DIR / 'chart1_gas_savings_per_pattern.png'
fig.savefig(out1)
plt.close(fig)
print(f"[OK] Chart 1 -> {out1.relative_to(ROOT)}")


# ── Chart 2: Venn — Our Tool (50 kontrak) vs Slither ─────────────────────
our_n   = sum(1 for r in compiled if sum(r.get(d, 0) for d in DETECTOR_NAMES) > 0)
slith_n = sum(
    1 for v in slither_results.values()
    if any(x in GAS_DETECTORS_SLITHER for x in v.get('all_detectors', []))
)

fig, ax = plt.subplots(figsize=(7, 5))
c_our   = plt.Circle((0.37, 0.5), 0.30, color='#3498db', alpha=0.45)
c_slith = plt.Circle((0.63, 0.5), 0.30, color='#e74c3c', alpha=0.45)
ax.add_patch(c_our)
ax.add_patch(c_slith)
ax.text(0.27, 0.50, str(our_n),   ha='center', va='center',
        fontsize=18, fontweight='bold', color='#1a5276')
ax.text(0.73, 0.50, str(slith_n), ha='center', va='center',
        fontsize=18, fontweight='bold', color='#922b21')
ax.text(0.50, 0.50, '0', ha='center', va='center', fontsize=16, color='#555')
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Venn Diagram: Kontrak dengan Gas Findings\n(Our Tool, 50 kontrak vs Slither, 10 sampel DeFi)', pad=12)
ax.text(0.50, 0.10,
        '*Slither 0 findings: ketidakkompatibilan pragma solidity 0.4.x',
        ha='center', va='center', fontsize=9, color='#777', style='italic')
ax.legend(
    handles=[
        mpatches.Patch(color='#3498db', alpha=0.6, label=f'Our Tool ({our_n}/50 kontrak)'),
        mpatches.Patch(color='#e74c3c', alpha=0.6, label=f'Slither ({slith_n}/10 sampel)'),
    ],
    loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=2,
)
fig.tight_layout()
out2 = FIGURES_DIR / 'chart2_venn_our_vs_slither.png'
fig.savefig(out2)
plt.close(fig)
print(f"[OK] Chart 2 -> {out2.relative_to(ROOT)}")


# ── Chart 3: Heatmap — Pattern Frequency per Domain ──────────────────────
matrix = []
for domain in DOMAINS:
    row = [
        sum(r.get(det, 0) for r in compiled if r['domain'] == domain)
        for det in DETECTOR_NAMES
    ]
    matrix.append(row)
mat = np.array(matrix)

det_labels = [
    'redundant\nsload', 'unoptimized\nloop', 'string\nvs bytes32',
    'public\nvs external', 'unchecked\narithmetic', 'dead\ncode',
]

fig, ax = plt.subplots(figsize=(10, 4.5))
im = ax.imshow(mat, cmap='YlOrRd', aspect='auto')
ax.set_xticks(range(len(DETECTOR_NAMES)))
ax.set_xticklabels(det_labels, fontsize=9)
ax.set_yticks(range(len(DOMAINS)))
ax.set_yticklabels(DOMAINS)
for i in range(len(DOMAINS)):
    for j in range(len(DETECTOR_NAMES)):
        v = mat[i, j]
        ax.text(j, i, str(v), ha='center', va='center',
                fontsize=11, fontweight='bold',
                color='white' if v > mat.max() * 0.6 else 'black')
plt.colorbar(im, ax=ax, label='Jumlah Findings')
ax.set_title('Heatmap: Frekuensi Anti-Pattern per Domain\n(50 Kontrak, 10 per Domain)', pad=12)
fig.tight_layout()
out3 = FIGURES_DIR / 'chart3_heatmap_domain_pattern.png'
fig.savefig(out3)
plt.close(fig)
print(f"[OK] Chart 3 -> {out3.relative_to(ROOT)}")

# Print matrix for verification
print("\n  Heatmap values:")
print(f"  {'Domain':<14} " + " ".join(f"{'rs':>5} {'ul':>5} {'sb':>5} {'pe':>5} {'ua':>5} {'dc':>5}"))
for domain, row in zip(DOMAINS, matrix):
    print(f"  {domain:<14} " + " ".join(f"{v:>5}" for v in row))


# ── Chart 4: Scatter — LOC vs Total Findings ─────────────────────────────
DOMAIN_COLORS = {
    'DeFi': '#3498db', 'NFT': '#e74c3c', 'Token': '#2ecc71',
    'Governance': '#f39c12', 'Utility': '#9b59b6',
}

all_locs   = [r['loc'] for r in compiled]
all_totals = [sum(r.get(d, 0) for d in DETECTOR_NAMES) for r in compiled]
rho, p_rho = spearmanr(all_locs, all_totals)

fig, ax = plt.subplots(figsize=(8, 5.5))
for domain in DOMAINS:
    dr = [r for r in compiled if r['domain'] == domain]
    xs = [r['loc'] for r in dr]
    ys = [sum(r.get(d, 0) for d in DETECTOR_NAMES) for r in dr]
    ax.scatter(xs, ys, c=DOMAIN_COLORS[domain], label=domain,
               alpha=0.78, s=65, edgecolors='white', linewidth=0.5)

# Trend line
z      = np.polyfit(all_locs, all_totals, 1)
x_line = np.linspace(min(all_locs), max(all_locs), 100)
ax.plot(x_line, np.poly1d(z)(x_line), 'k--', alpha=0.4, linewidth=1.2,
        label='Trend (linear fit)')

sig_mark = 'signifikan (p<0.05)' if p_rho < 0.05 else 'tidak signifikan'
ax.set_xlabel('Lines of Code (LOC)')
ax.set_ylabel('Total Findings')
ax.set_title(
    f'Scatter: LOC vs Total Anti-Pattern Findings\n'
    f'(Spearman rho = {rho:+.3f}, p = {p_rho:.3f} — {sig_mark})',
    pad=12,
)
ax.legend(loc='upper right', fontsize=9)
ax.grid(alpha=0.25)
fig.tight_layout()
out4 = FIGURES_DIR / 'chart4_scatter_loc_findings.png'
fig.savefig(out4)
plt.close(fig)
print(f"[OK] Chart 4 -> {out4.relative_to(ROOT)}")
print(f"   Spearman rho = {rho:+.4f}, p = {p_rho:.4f} ({'SIGNIFIKAN' if p_rho < 0.05 else 'tidak signifikan'})")

print(f"\n[DONE] Semua chart tersimpan di results_50/figures/")
