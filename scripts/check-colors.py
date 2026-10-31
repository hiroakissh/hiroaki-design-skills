#!/usr/bin/env python3
"""Validate the declared color pairs without modifying the palette."""

from design_tokens import load, measurements


if __name__ == "__main__":
    rows = measurements(load())
    failed = ["{} {}/{}: {:.4f} < {}".format(*row) for row in rows if row[3] < row[4]]
    if failed:
        raise SystemExit("Contrast checks failed:\n" + "\n".join(failed))
    print("Passed {} declared contrast pairs across Light/Dark. This is not a full WCAG conformance audit.".format(len(rows)))
