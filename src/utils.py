"""
Shared formatting utilities for the RealEstate Pipeline.

Provides consistent K/M suffix formatting for large numbers, used across
statistical logs, business insights, and chart labels.
"""


def format_number(value: float, decimals: int = 1) -> str:
    """
    Format a number using K/M suffixes for readability.

    Examples
    --------
    625256.41  -> '625.3K'
    1200000.0  -> '1.20M'
    342.86     -> '342.86'

    Parameters
    ----------
    value : float
        The numeric value to format.
    decimals : int, default=1
        Decimal places to use for the K-range (M-range always uses 2).

    Returns
    -------
    str
        Human-readable formatted string.
    """
    abs_value = abs(value)

    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs_value >= 1_000:
        return f"{value / 1_000:.{decimals}f}K"
    return f"{value:,.2f}"


def format_money(value: float, decimals: int = 1) -> str:
    """
    Format a currency value with a '$' prefix using K/M suffixes.

    Examples
    --------
    625256.41  -> '$625.3K'
    1200000.0  -> '$1.20M'

    Parameters
    ----------
    value : float
        The monetary value to format.
    decimals : int, default=1
        Decimal places to use for the K-range.

    Returns
    -------
    str
        Formatted currency string.
    """
    return f"${format_number(value, decimals)}"