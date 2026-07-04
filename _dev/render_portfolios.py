"""Render data analyst portfolio PDFs to PNG images for layout review."""
from __future__ import annotations

import sys
from pathlib import Path

import fitz  # pymupdf

SRC_DIR = Path(r"C:\Users\서윤범\Desktop\무료 공개 포트폴리오\무료 공개 포트폴리오(무료 배포 자료는 매월 업데이트 됩니다.)")
OUT_DIR = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\_dev\portfolio_previews")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Map source filename → output slug (ascii) for easier reading.
TARGETS: dict[str, str] = {
    "23년_데이터분석가_신입_합격 포트폴리오(1).pdf": "23_da_newgrad_1",
    "23년_데이터분석가_신입_합격 포트폴리오.pdf": "23_da_newgrad_2",
    "23년_카카오_데이터분석가_신입_합격 포트폴리오.pdf": "23_kakao_da",
    "23년_쿠팡_데이터분석가_신입_합격 포트폴리오(1).pdf": "23_coupang_da_1",
    "23년_쿠팡_데이터분석가_신입_합격 포트폴리오.pdf": "23_coupang_da_2",
    "24년_데이터분석가_신입_합격 포트폴리오.pdf의 사본.pdf": "24_da_newgrad",
    "24년_야놀자_데이터분석가_신입_합격 포트폴리오.pdf": "24_yanolja_da",
    "24년_차병원_데이터분석가_신입_합격 포트폴리오.pdf": "24_chabiomed_da",
    "쿠팡_데이터분석가_경력_합격_포트폴리오.pdf": "coupang_da_exp",
}

DPI = 90  # keep files small but legible


def render(src: Path, slug: str) -> tuple[int, list[Path]]:
    doc = fitz.open(src)
    paths: list[Path] = []
    zoom = DPI / 72
    matrix = fitz.Matrix(zoom, zoom)
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out = OUT_DIR / f"{slug}_p{i:02d}.png"
        pix.save(out)
        paths.append(out)
    n = doc.page_count
    doc.close()
    return n, paths


def main() -> None:
    summary: list[str] = []
    for fname, slug in TARGETS.items():
        src = SRC_DIR / fname
        if not src.exists():
            summary.append(f"MISSING: {fname}")
            continue
        n, paths = render(src, slug)
        summary.append(f"{slug}: {n} pages, first={paths[0].name}, last={paths[-1].name}")
        print(summary[-1], flush=True)
    (OUT_DIR / "_index.txt").write_text("\n".join(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
