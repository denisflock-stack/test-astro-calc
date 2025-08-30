from __future__ import annotations
import math

__all__ = ["dec_to_dms360", "format_dms360"]

def _normalize360(x: float) -> float:
    if math.isnan(x) or math.isinf(x):
        raise ValueError("Angle must be finite.")
    x = math.fmod(x, 360.0)
    if x < 0:
        x += 360.0
    return x

def dec_to_dms360(value_deg: float, *, sec_precision: int = 3) -> tuple[int, int, float]:
    """Convert decimal degrees to DMS for angles on [0,360)."""
    x = _normalize360(value_deg)
    total_sec = x * 3600.0
    # round half up (avoid banker's rounding)
    q = 10 ** sec_precision
    sec_rounded = math.floor(total_sec * q + 0.5) / q

    deg = int(sec_rounded // 3600)
    rem = sec_rounded - deg * 3600
    minute = int(rem // 60)
    second = rem - minute * 60

    # cascade checks
    if second >= 60 - 10 ** (-sec_precision):
        second = 0.0
        minute += 1
    if minute >= 60:
        minute = 0
        deg += 1
    if deg >= 360:
        deg = 0

    return deg, minute, round(second, sec_precision)

def format_dms360(value_deg: float, *, sec_precision: int = 3,
                  zero_pad: bool = True, symbols: tuple[str, str, str] = ("°", "′", "″")) -> str:
    d, m, s = dec_to_dms360(value_deg, sec_precision=sec_precision)
    deg_sym, min_sym, sec_sym = symbols
    if zero_pad:
        m_str = f"{m:02d}"
        s_fmt = f"{{:0{2 + (1 + sec_precision if sec_precision > 0 else 0)}.{sec_precision}f}}"
        s_str = s_fmt.format(s) if sec_precision > 0 else f"{int(round(s)):02d}"
    else:
        m_str = str(m)
        s_str = f"{s:.{sec_precision}f}" if sec_precision > 0 else str(int(round(s)))
    return f"{d}{deg_sym} {m_str}{min_sym} {s_str}{sec_sym}"
