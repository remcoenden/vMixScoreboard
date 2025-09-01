# AnatecIndor Python Script

Purpose
- Provide vMixScoreboard.py with live data from an Anatec indoor scoreboard when the “AnatecIndor” source is selected.

How it works
- Host device (e.g., Raspberry Pi) connects its UART RX to the scoreboard data line.
- The module listens for frames delimited by “{” (start) and “}” (end).
- From each complete frame, it extracts:
    - Home score: bytes 17:19
    - Guest score: bytes 11 + 10
    - Minutes: bytes 19:21
    - Seconds: bytes 14 + 13
    - Shot Clock: bytes 0:2
- The extracted values are returned to the caller (vMixScoreboard.py) as the current scoreboard state.

Integration
- This file is not a standalone tool or CLI.
- vMixScoreboard.py imports and calls it whenever the AnatecIndor scoreboard is selected, then consumes the returned minutes, seconds, home score, and guest score.

Serial connection
- Connect UART RX to the scoreboard data output through the correct level/interface (TTL/RS-232/RS-485 as required by your hardware).
- Use the serial port and parameters that match the scoreboard controller. Configure these in your environment or code as appropriate.

Troubleshooting
- Verify the serial device path and permissions.
- Confirm the raw stream contains frames starting with “{” and ending with “}”.
- If values are incorrect, re-check byte positions against your controller’s protocol and adjust the byte indices in code.

Notes
- Byte positions are 1-based within the delimited frame.
- Field sizes and encoding depend on the specific Anatec controller; adjust parsing if your model differs.
- Keep this file alongside vMixScoreboard.py so the “AnatecIndor” option remains available.
