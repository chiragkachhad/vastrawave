#!/usr/bin/env python3
"""Product-only transparent cutouts for VastraWave.
Input photos are on a near-uniform studio-grey background. GrabCut finds the
foreground; for mannequin shots we also remove the near-white mannequin so only
the garment remains. Output: cropped transparent WebP files.
"""
from pathlib import Path
import cv2, numpy as np, sys

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets" / "img"
OUT = IMG / "cutouts"

# id, source, output-relative-path, remove near-white mannequin?
JOBS = [
    ("CR101", "c1-corset-black.jpg", "front/CR101.webp", True),
    ("CR102", "c2-corset-lace.jpg", "front/CR102.webp", True),
    ("LW201", "d1-dress-floral.jpg", "front/LW201.webp", True),
    ("LW202", "d2-gown-wine.jpg", "front/LW202.webp", True),
    ("LW203", "d3-top-cream.jpg", "front/LW203.webp", False),
    ("WB301", "w1-palazzo-cream.jpg", "front/WB301.webp", False),
    ("WB302", "w2-skirt-denim.jpg", "front/WB302.webp", False),
    ("TS301", "t1-tee-white.jpg", "front/TS301.webp", False),
    ("TS302", "t2-tee-graphic.jpg", "front/TS302.webp", False),
    ("MS401", "m1-shirt-check.jpg", "front/MS401.webp", False),
    ("MS402", "m2-shirt-formal.jpg", "front/MS402.webp", False),
    ("MB501", "mb1-jeans-men.jpg", "front/MB501.webp", False),
    ("MB502", "mb2-jogger-olive.jpg", "front/MB502.webp", False),
    # Existing real back photo (flat product shot)
    ("TS301", "a1-tee-back.jpg", "back/TS301.webp", False),
]
# Generated side/back raw photos are picked up automatically:
# assets/img/views/{ID}-side.jpg -> assets/img/cutouts/side/{ID}.webp, etc.
MANNEQUIN_IDS = {"CR101", "CR102", "LW201", "LW202"}

# CR102 ki purani catalogue photo asal me BACK view thi. Agar generated sahi
# front maujud hai to use front banao aur purani photo ko back view rakho.
if (IMG / "views" / "CR102-front.jpg").exists():
    JOBS = [
        (pid, "views/CR102-front.jpg" if pid == "CR102" and rel == "front/CR102.webp" else fn, rel, rw)
        for pid, fn, rel, rw in JOBS
    ]
    JOBS.append(("CR102", "c2-corset-lace.jpg", "back/CR102.webp", True))

def largest(mask):
    mask = mask.astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n <= 1:
        return mask
    return (lab == (1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA])))).astype(np.uint8)

def fill_holes(mask):
    inv = (1 - mask).astype(np.uint8)
    n, lab = cv2.connectedComponents(inv, 4)
    border = set(np.unique(np.concatenate([lab[0,:], lab[-1,:], lab[:,0], lab[:,-1]])).tolist())
    out = mask.copy()
    for i in range(1, n):
        if i not in border:
            out[lab == i] = 1
    return out

def cutout(src: Path, remove_white=False):
    bgr = cv2.imread(str(src), cv2.IMREAD_COLOR)
    if bgr is None:
        raise FileNotFoundError(src)
    work = cv2.resize(bgr, (512, 512), interpolation=cv2.INTER_AREA)
    gc_mask = np.zeros((512,512), np.uint8)
    bgd = np.zeros((1,65), np.float64); fgd = np.zeros((1,65), np.float64)
    cv2.grabCut(work, gc_mask, (18, 8, 476, 496), bgd, fgd, 7, cv2.GC_INIT_WITH_RECT)
    mask = np.where((gc_mask == 2) | (gc_mask == 0), 0, 1).astype(np.uint8)
    mask = fill_holes(largest(mask))

    if src.name == "c2-corset-lace.jpg" or src.name.startswith("CR102-"):
        # Maroon garment has strong red dominance; this cleanly separates it
        # from the ivory mannequin (tested side-by-side against white-removal).
        rgb = cv2.cvtColor(work, cv2.COLOR_BGR2RGB).astype(np.int16)
        mx, mn = rgb.max(axis=2), rgb.min(axis=2)
        redness = rgb[:, :, 0] - np.maximum(rgb[:, :, 1], rgb[:, :, 2])
        red_mask = (((redness > 8) & ((mx - mn) > 35)) | (mx < 125)).astype(np.uint8)
        mask = largest(np.minimum(mask, red_mask))
    elif remove_white:
        rgb = cv2.cvtColor(work, cv2.COLOR_BGR2RGB).astype(np.int16)
        mx, mn = rgb.max(axis=2), rgb.min(axis=2)
        white = (mn > 205) & ((mx - mn) < 22)
        candidate = np.where(white, 0, mask).astype(np.uint8)
        candidate = cv2.morphologyEx(candidate, cv2.MORPH_CLOSE, np.ones((3,3), np.uint8), iterations=1)
        mask = fill_holes(largest(candidate))

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3,3), np.uint8), iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((2,2), np.uint8), iterations=1)
    alpha = cv2.GaussianBlur((mask * 255).astype(np.uint8), (3,3), 0)
    rgba = cv2.cvtColor(work, cv2.COLOR_BGR2BGRA); rgba[:, :, 3] = alpha
    ys, xs = np.where(alpha > 8)
    if len(xs) == 0:
        raise RuntimeError(f"empty mask: {src}")
    pad = 6
    y0, y1 = max(0, ys.min()-pad), min(512, ys.max()+pad+1)
    x0, x1 = max(0, xs.min()-pad), min(512, xs.max()+pad+1)
    return rgba[y0:y1, x0:x1]

def save(rgba, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    ok, buf = cv2.imencode(".webp", rgba, [cv2.IMWRITE_WEBP_QUALITY, 92])
    if not ok:
        raise RuntimeError(f"webp encode failed: {dst}")
    dst.write_bytes(buf.tobytes())

def main():
    done = []
    for pid, fn, rel, rw in JOBS:
        rgba = cutout(IMG / fn, rw)
        dst = OUT / rel
        save(rgba, dst)
        done.append((rel, rgba.shape[1], rgba.shape[0], dst.stat().st_size))
        print("✓", rel, f"{rgba.shape[1]}x{rgba.shape[0]}", f"{dst.stat().st_size//1024} KB")
    views = IMG / "views"
    if views.exists():
        for src in sorted(views.glob("*.jpg")) + sorted(views.glob("*.png")):
            # CR101-side.jpg / CR101-back.jpg
            stem = src.stem
            if "-" not in stem: continue
            pid, kind = stem.rsplit("-", 1)
            if kind not in {"side", "back"}: continue
            rgba = cutout(src, pid in MANNEQUIN_IDS)
            dst = OUT / kind / f"{pid}.webp"
            save(rgba, dst)
            done.append((f"{kind}/{pid}.webp", rgba.shape[1], rgba.shape[0], dst.stat().st_size))
            print("✓", f"{kind}/{pid}.webp", f"{rgba.shape[1]}x{rgba.shape[0]}", f"{dst.stat().st_size//1024} KB")
    print(f"DONE {len(done)} cutouts")

if __name__ == "__main__":
    main()
