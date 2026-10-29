#!/usr/bin/env python3
"""Step 7: publication figures (PNG, 300 dpi).

Real-series exponent paths are drawn at month-end resolution only and are never
written to disk as data; figures are raster images so plotted coordinates cannot
be read back at full precision.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                              # noqa: E402
import matplotlib.dates as mdates                                           # noqa: E402
import numpy as np                                                          # noqa: E402
import pandas as pd                                                         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib import config as C                                                 # noqa: E402
from lib.core import load_data, design_from_df, cums, rolling, expanding, slopes_window   # noqa: E402

OI = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "red": "#D55E00",
      "purple": "#CC79A7", "sky": "#56B4E9", "black": "#222222", "grey": "#8C8C8C"}
# Start from matplotlib's built-in defaults, ignoring any user or site matplotlibrc, and use
# DejaVu Sans (bundled with matplotlib), so the figures are identical in any environment with
# the pinned matplotlib version.
matplotlib.rcdefaults()
plt.rcParams.update({"font.family": "DejaVu Sans", "text.hinting": "default", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "legend.frameon": False, "figure.dpi": 100, "savefig.dpi": 300,
                     "axes.edgecolor": "#444444", "axes.linewidth": 0.6})
FIG = ROOT / "figures"


def bands(plaus, key, which="plausible"):
    lo, hi, med = [], [], []
    for f in sorted(glob.glob(str(ROOT / "cache" / "null_*.npz"))):
        z = np.load(f); mid = json.loads(str(z["model"]))["id"]
        if (mid in plaus) == (which == "plausible"):
            q = z[f"band_{key}"]; lo.append(q[0]); hi.append(q[4]); med.append(q[2])
    return np.min(lo, 0), np.max(hi, 0), np.median(med, 0)


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("wrote", name)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    a = ap.parse_args()
    FIG.mkdir(exist_ok=True)
    out = ROOT / "outputs"
    df = load_data(Path(a.csv), require_frozen=not a.allow_different_sample)
    D = design_from_df(df); y = np.log(df.price_usd.to_numpy(float)); Sy, Sxy = cums(D, y)
    P = json.loads((out / "plausible_models.json").read_text())
    plaus = set(P["plausible"])

    # ---------------- Figure 1: three estimators, each against its own plausible-family band
    def inside(obs, lo, hi):
        ok = np.isfinite(obs) & np.isfinite(lo)
        return float(np.mean((obs[ok] >= lo[ok]) & (obs[ok] <= hi[ok])))
    ev = D.roll_eval[5]
    me = D.month_end[D.month_end >= 365]
    me17 = D.month_end[D.month_end >= D.i_post + 365]
    panels = [("roll5", D.dates[ev], rolling(D, Sy, Sxy, 5, ev), "Rolling 5-year window", OI["blue"]),
              ("exp", D.dates[me], expanding(D, Sy, Sxy, me), "Expanding from genesis", OI["black"]),
              ("exp17", D.dates[me17], expanding(D, Sy, Sxy, me17, start=D.i_post), "Expanding from 1 Jan 2017", OI["orange"])]
    fig, axs = plt.subplots(3, 1, figsize=(7.2, 6.4), sharex=True)
    for axx, (key, dts, obs, lab, col) in zip(axs, panels):
        lo, hi, _ = bands(plaus, key); xlo, xhi, _ = bands(plaus, key, "extremes")
        axx.fill_between(dts, xlo, xhi, color=OI["grey"], alpha=0.10, lw=0,
                         label="pointwise 95% range, all 48 models" if key == "roll5" else None)
        axx.fill_between(dts, lo, hi, color=OI["grey"], alpha=0.30, lw=0,
                         label="pointwise 95% range, 12 screened models" if key == "roll5" else None)
        axx.axhline(C.B_FULL_V08, color=OI["black"], lw=0.7, ls=(0, (4, 3)))
        axx.plot(dts, obs, color=col, lw=1.6)
        axx.text(0.005, 0.88, lab, transform=axx.transAxes, fontsize=8, fontweight="bold", color=col)
        axx.set_ylim(-1, 12); axx.set_ylabel("B")
        print(f"fig1 {key}: share of month-ends inside plausible band = {inside(obs, lo, hi):.3f}")
    axs[0].text(D.dates[ev][-1], C.B_FULL_V08 + 0.3, f"full-history B = {C.B_FULL_V08:.2f}", ha="right", fontsize=7.5)
    axs[0].legend(loc="lower left", fontsize=7, ncol=2)
    axs[0].set_title("Except just after the 2011 and 2017 peaks, each estimator stays inside its constant-exponent range")
    axs[-1].xaxis.set_major_locator(mdates.YearLocator(2))
    save(fig, "fig1_estimators_null_bands")

    # ---------------- Figure 2: window length small multiples
    fig, axs = plt.subplots(len(C.ROLL_YEARS), 1, figsize=(7.2, 7.6), sharex=True)
    for axx, L in zip(axs, C.ROLL_YEARS):
        ev = D.roll_eval[L]; lo, hi, _ = bands(plaus, f"roll{L}")
        axx.fill_between(D.dates[ev], lo, hi, color=OI["grey"], alpha=0.28, lw=0)
        axx.axhline(C.B_FULL_V08, color=OI["black"], lw=0.7, ls=(0, (4, 3)))
        obs = rolling(D, Sy, Sxy, L, ev)
        axx.plot(D.dates[ev], obs, color=OI["blue"], lw=1.5)
        print(f"fig2 roll{L}: share inside plausible band = {inside(obs, lo, hi):.3f}")
        axx.text(0.005, 0.86, f"{L}-year window", transform=axx.transAxes, fontsize=8, fontweight="bold")
        axx.set_ylim(min(-3, np.nanmin(lo) - 0.5), max(13, np.nanmax(hi) + 0.5)); axx.set_ylabel("B")
    axs[0].set_title("Shorter windows swing more, and every path stays inside its constant-B band")
    axs[-1].xaxis.set_major_locator(mdates.YearLocator(2))
    save(fig, "fig2_window_length")

    # ---------------- Figure 3: start-date sensitivity
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    sidx = D.year_start_idx
    lo, hi, _ = bands(plaus, "start_B")
    starts = D.dates[sidx]
    ax.fill_between(starts, lo, hi, color=OI["grey"], alpha=0.28, lw=0, label="95% range, screened models (B constant)")
    ax.axhline(C.B_FULL_V08, color=OI["black"], lw=0.7, ls=(0, (4, 3)))
    sb = slopes_window(D, Sy, Sxy, sidx, np.full(len(sidx), D.n - 1))
    print(f"fig3 start_B: share inside plausible band = {inside(sb, lo, hi):.3f}")
    ax.plot(starts, sb, "o-", color=OI["blue"], lw=1.5, ms=4, label="B from 1 January of each year to 2026-08-14")
    ax.set_ylabel("Fitted exponent B"); ax.set_xlabel("Regression start date")
    ax.set_title("Start-date sensitivity is what persistent residuals produce under a constant exponent")
    ax.legend(loc="lower left", fontsize=7.5)
    save(fig, "fig3_start_date")

    # ---------------- Figure 4: p-values by null model
    cal = pd.read_csv(out / "calibration.csv"); mt = pd.read_csv(out / "maxT.csv"); scr = pd.read_csv(out / "screening.csv")
    order = scr.sort_values(["plausible", "maha_p"], ascending=[False, False])
    show = list(order[order.plausible].model) + ["rw|cyc0.0|lam1", "ar0.997|cyc0.0|lam0", "ar0.990|cyc0.0|lam0", "frac0.6|cyc0.0|lam1"]
    stats = [("d17", "Post-2017 minus full B", OI["blue"]), ("curv", "Curvature in ln t (principal)", OI["orange"]),
             ("mean5", "Mean rolling-5y B, five checkpoints 2022-26", OI["green"]), ("r5_2025", "Rolling-5y B, end 2025", OI["purple"]),
             ("rmin5", "Minimum of rolling-5y path", OI["sky"])]
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    for j, mid in enumerate(show):
        yy = len(show) - j
        for s, lab, col in stats:
            p = cal[(cal.model == mid) & (cal.stat == s)].p_one_sided.iloc[0]
            ax.scatter(max(p, 5e-4), yy, color=col, s=18, zorder=3, label=lab if j == 0 else None)
        pa = mt[mt.model == mid].adjusted_p.iloc[0]
        ax.scatter(max(pa, 5e-4), yy, marker="D", facecolor="white", edgecolor=OI["black"], s=26, zorder=4,
                   label="Battery, multiplicity-adjusted (secondary)" if j == 0 else None)
    ax.set_yticks(range(len(show), 0, -1)); ax.set_yticklabels(show, fontsize=7.5)
    ax.axhline(len(show) - len(order[order.plausible]) + 0.5, color=OI["grey"], lw=0.6)
    ax.axvline(0.05, color=OI["red"], lw=0.8, ls=(0, (4, 3)))
    ax.set_xscale("log"); ax.set_xlim(4e-4, 1.05); ax.set_xlabel("One-sided p-value (evidence of a lower recent exponent to the left)")
    n_sig = int((mt[mt.plausible].adjusted_p < 0.05).sum()); n_pl = int(mt.plausible.sum())
    curv_rej = int((cal[(cal.stat == "curv") & cal.plausible].p_one_sided < 0.05).sum())
    ax.set_title(("The principal curvature test rejects under none of the " if curv_rej == 0 else f"The principal curvature test rejects under {curv_rej} of the ")
                 + f"{n_pl} screened models; the adjusted battery under {n_sig}")
    ax.legend(loc="lower left", fontsize=7, ncol=2, bbox_to_anchor=(0, -0.30))
    ax.text(1.0, len(show) + 0.4, "screened models above the line; screened-out examples below", ha="right", fontsize=7, color=OI["grey"])
    save(fig, "fig4_pvalues_by_null")

    # ---------------- Figure 5: power curves, family-wide and model-specific critical values
    pw = pd.read_csv(out / "power_curves.csv")
    tests = [("curv", "Curvature in ln t (principal)", OI["orange"]), ("d17", "Post-2017 minus full B", OI["blue"]),
             ("mean5", "Mean rolling-5y B (five checkpoints)", OI["green"]), ("rend5", "Rolling-5y B at cutoff", OI["purple"]),
             ("rend10", "Rolling-10y B at cutoff", OI["red"]), ("exp_drop", "Expanding-B drop from peak", OI["grey"]),
             ("brk_maxadj", "Break detector (max change)", OI["sky"]),
             ("maxT_battery", "Battery, adjusted (secondary)", OI["black"])]
    fig, axs = plt.subplots(2, 2, figsize=(7.4, 6.2), sharey=True, sharex=True)
    rows = [("reject_family", "Critical value valid for every\nscreened model"),
            ("reject_model", "Critical value from the true\nmodel (oracle)")]
    for i, (col_, rlab) in enumerate(rows):
        for j, (shape, ttl) in enumerate(zip(C.SHAPES, ["Decline spread across the whole sample",
                                                       "Decline concentrated after 2017"])):
            axx = axs[i, j]
            for k, lab, col in tests:
                sub = pw[(pw["shape"] == shape) & (pw["test"] == k)]
                if sub[col_].isna().all():
                    continue
                g = sub.groupby("delta")[col_]
                m_, lo_, hi_ = g.mean(), g.min(), g.max()
                axx.plot(m_.index, m_.values, "-o", color=col, ms=2.5, lw=1.3, label=lab)
                if k == ("curv" if col_ == "reject_family" else "maxT_battery"):
                    axx.fill_between(m_.index, lo_.values, hi_.values, color=col, alpha=0.12, lw=0)
            axx.axhline(0.05, color=OI["red"], lw=0.7, ls=(0, (4, 3)))
            axx.set_ylim(0, 1); axx.set_xlim(0, 3.05)
            if i == 0:
                axx.set_title(ttl, fontsize=9)
            if i == 1:
                axx.set_xlabel("Total decline in local exponent, D")
            if j == 0:
                axx.set_ylabel(f"{rlab}\n\nRejection rate at 5%", fontsize=8)
    axs[1, 1].legend(fontsize=6.6, loc="upper left")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.suptitle("No test reliably detects even a large decline in the exponent", x=0.01, y=0.995, ha="left",
                 fontsize=10, fontweight="bold")
    fig.text(0.01, 0.955, "Lines: mean over the 12 screened models. Shading: range across models for the best test in each row. Dashed: 5% size.",
             fontsize=7.5, color="#555555")
    save(fig, "fig5_power_curves")

    # ---------------- Figure 6: interval coverage
    hc = pd.read_csv(out / "hac_coverage.csv").sort_values(["plausible", "cover_nw365"], ascending=[False, True])
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    yy = np.arange(len(hc), 0, -1)
    for col, lab, c_ in [("cover_nw365", "Newey-West, 365-day lag (v0.8)", OI["blue"]),
                         ("cover_nw1461", "Newey-West, 1,461-day lag", OI["sky"]),
                         ("cover_boot365", "365-day block bootstrap (v0.8)", OI["orange"])]:
        ax.scatter(hc[col], yy, color=c_, s=20, label=lab, zorder=3)
    n_pl = int(hc.plausible.sum())
    ax.axhline(len(hc) - n_pl + 0.5, color=OI["grey"], lw=0.6)
    ax.text(0.01, len(hc) - n_pl + 0.62, "screened models above; screened-out examples below",
            fontsize=7, color="#555555", va="bottom")
    ax.axvline(0.95, color=OI["black"], lw=0.8, ls=(0, (4, 3))); ax.text(0.95, len(hc) + 0.6, "nominal 95%", ha="center", fontsize=7.5)
    ax.set_yticks(yy); ax.set_yticklabels(hc.model, fontsize=7.5); ax.set_xlim(0, 1.02)
    ax.set_xlabel("Share of simulated constant-B histories whose 95% interval contains the true B")
    under = int((hc[hc.plausible].cover_nw365 < 0.90).sum())
    ax.set_title(f"Under {under} of {n_pl} screened models, v0.8's 95% intervals miss the true exponent too often")
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.13), fontsize=7, ncol=3)
    save(fig, "fig6_interval_coverage")

    # ---------------- Figure 7: asymmetry
    rep = json.loads((out / "reproduction.json").read_text())
    ep = rep["halving_epochs"]; asy = pd.read_csv(out / "asymmetry.csv")
    fig, axs = plt.subplots(1, 2, figsize=(8.0, 3.3), gridspec_kw={"width_ratios": [1.1, 1], "wspace": 0.75})
    ax = axs[0]
    for i, e_ in enumerate(ep):
        filled = e_["complete"]
        ax.scatter(i, e_["max_resid_ln"], color=OI["blue"], s=28, facecolor=OI["blue"] if filled else "white", zorder=3)
        ax.scatter(i, e_["min_resid_ln"], color=OI["red"], s=28, facecolor=OI["red"] if filled else "white", zorder=3)
    ax.plot(range(len(ep)), [e_["max_resid_ln"] for e_ in ep], color=OI["blue"], lw=0.8)
    ax.plot(range(len(ep)), [e_["min_resid_ln"] for e_ in ep], color=OI["red"], lw=0.8)
    ax.axhline(0, color=OI["black"], lw=0.6)
    ax.set_xticks(range(len(ep))); ax.set_xticklabels([f"E{i}" for i in range(len(ep))])
    ax.set_ylabel("Residual from full-history fit (ln)"); ax.set_xlabel("Halving epoch (hollow = partial)")
    ax.text(2.1, ep[2]["max_resid_ln"] + 0.15, "epoch maximum", color=OI["blue"], fontsize=7.5)
    ax.text(2.1, ep[2]["min_resid_ln"] + 0.15, "epoch minimum", color=OI["red"], fontsize=7.5)
    ax.set_title("Highs fall each epoch; lows barely move", fontsize=9)
    ax = axs[1]
    keys = [("Aq", "Quantile asymmetry"), ("Lw", "Lower-quantile slope"), ("Aep_E1_3", "Epoch asymmetry, E1-E3"),
            ("Aep_E0_3", "Epoch asymmetry, E0-E3"), ("Aep_E0_4", "Epoch asymmetry, E0-E4")]
    for j, (k, lab) in enumerate(keys):
        for v_, col, off in [("symmetric", OI["blue"], -0.12), ("skewed", OI["orange"], 0.12)]:
            sub = asy[(asy.stat == k) & (asy.variant == v_)]
            floor = 1.0 / sub.n.max()                     # Monte Carlo resolution: p = 0 means p < 1/n
            g = sub.p_directional.clip(lower=floor)
            ax.plot([g.min(), g.max()], [len(keys) - j + off] * 2, color=col, lw=2.2, alpha=0.6)
            ax.scatter(g.median(), len(keys) - j + off, color=col, s=16, zorder=3,
                       marker="<" if g.median() <= floor else "o",
                       label=("symmetric shrinking null" if v_ == "symmetric" else "skewed shrinking null") if j == 0 else None)
    ax.set_yticks(range(len(keys), 0, -1)); ax.set_yticklabels([l for _, l in keys], fontsize=7.5)
    ax.axvline(0.05, color=OI["red"], lw=0.8, ls=(0, (4, 3))); ax.set_xscale("log"); ax.set_xlim(1e-3, 1)
    ax.text(1.15e-3, len(keys) + 0.05, "< marks p below Monte\nCarlo resolution (1/400)", fontsize=6.5, color="#555555")
    ax.set_xlabel("One-sided p (range over screened models)")
    ax.set_title("Asymmetry against shrinking nulls", fontsize=9)
    ax.legend(fontsize=6.8, loc="lower right"); ax.set_ylim(0.2, len(keys) + 0.5)
    fig.suptitle("Highs compress more than lows, but decisively only when the incomplete current epoch is counted", x=0.01, y=1.04, ha="left",
                 fontsize=10, fontweight="bold")
    save(fig, "fig7_asymmetry")


if __name__ == "__main__":
    main()
