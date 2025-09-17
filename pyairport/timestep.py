##@namespace timestep
"""
Manage simulation times

The simulation times are sampled over a fixed time-step (usually 5 seconds). This module helps converting \"real\" times to and from simulation time-steps. It also provides utilities to parse and write times in the HH:MM:SS format.
"""

## Simulation time-step in seconds (int)
TIMESTEP = 5


def of_seconds(t):
    """Converts to simulation time-steps.

    Args:
        t:  (int)  a time in seconds

    Returns:
        A time in simulation time-steps (int).
    """
    return t // TIMESTEP


def to_seconds(t: int) -> int:
    """Converts to seconds.

    Args:
        t:  (int)  a time in simulation time-steps

    Returns:
        A time in seconds (int).
    """
    return t * TIMESTEP


def to_hms(t):
    """Converts to HH:MM:SS format.

    Args:
        t:  (int)  a time in simulation time-steps

    Returns:
        A string formatted as HH:MM:SS for time-step `t`.
    """
    s = to_seconds(t)
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}"


def of_hms(str_hms):
    """Parse an HH:MM:SS string to time-steps.

    Args:
        str_hms:  (str)  a string of the form HH:MM:SS

    Returns:
        A time in simulation time-steps corresponding to `str_hms` (int)

    Raises:
        ValueError: if string @c str_hms is ill-formed.
    """
    h, m, s = str_hms.split(":")
    t = int(h) * 3600 + int(m) * 60 + int(s)
    return of_seconds(t)
