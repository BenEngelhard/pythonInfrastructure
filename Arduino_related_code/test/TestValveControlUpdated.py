"""
water_dispenser.py
──────────────────
Python controller for the 2-channel Arduino UNO water dispenser.
2

Requirements:
    pip install pyserial

Usage examples:
    python water_dispenser.py              # interactive CLI (auto-detect port)
    python water_dispenser.py --port COM4  # Windows explicit port
    python water_dispenser.py --port /dev/ttyUSB0  # Linux / Mac
"""

import serial
import serial.tools.list_ports
import time
import argparse
import sys


# ── Serial helpers ─────────────────────────────────────────────────────────────

def find_arduino_port() -> str | None:
    """Try to auto-detect the Arduino's serial port."""
    for port in serial.tools.list_ports.comports():
        desc = port.description.lower()
        if "arduino" in desc or "ch340" in desc or "cp210" in desc or "uno" in desc:
            return port.device
    return None


def connect(port: str | None = None, baud: int = 9600, timeout: float = 3.0) -> serial.Serial:
    if port is None:
        port = find_arduino_port()
        if port is None:
            raise RuntimeError(
                "Could not auto-detect Arduino. "
                "Pass --port explicitly (e.g. --port COM4 or --port /dev/ttyUSB0)."
            )
        print(f"[info] Auto-detected Arduino on {port}")

    try:
        ser = serial.Serial(
            port,
            baud,
            timeout=timeout,
            dsrdtr=False,      # ← prevent DTR toggling on open
            rtscts=False,
        )
        # Explicitly lower DTR so the Arduino does NOT reset when we connect
        ser.dtr = False

    except serial.SerialException as e:
        if "PermissionError" in str(e) or "Access is denied" in str(e):
            print(f"[error] Port {port} is already in use.")
            print("[hint]  • Close the Arduino IDE Serial Monitor.")
            print("[hint]  • End any leftover python.exe in Task Manager.")
            print("[hint]  • Unplug and replug the USB cable, then try again.")
            sys.exit(1)
        raise

    # Give the Arduino a moment to settle (no reset, but UART needs ~100 ms)
    time.sleep(0.5)
    ser.reset_input_buffer()   # discard any garbage bytes

    # Read the READY greeting (Arduino sends this on power-on / reset)
    # If we prevented the reset, there may be no greeting – that's fine.
    ser.timeout = 1.0
    greeting = ser.readline().decode("utf-8", errors="replace").strip()
    ser.timeout = timeout

    if greeting == "READY":
        print(f"[info] Arduino ready on {port} @ {baud} baud")
    else:
        # No greeting means DTR-reset was successfully suppressed – still OK
        print(f"[info] Connected to {port} @ {baud} baud")
        if greeting:
            print(f"[info] First message: '{greeting}'")

    return ser


def flush_input(ser: serial.Serial) -> None:
    """Discard any bytes sitting in the receive buffer before sending a command."""
    ser.reset_input_buffer()


def send_command(ser: serial.Serial, cmd: str, wait_ms: int = 100) -> str:
    """
    Flush stale input, send a newline-terminated command, and return
    the first meaningful response line from the Arduino.

    wait_ms: extra settling time (ms) before reading – helps with slow responses.
    """
    flush_input(ser)
    ser.write((cmd + "\n").encode("utf-8"))

    if wait_ms > 0:
        time.sleep(wait_ms / 1000.0)

    response = ser.readline().decode("utf-8", errors="replace").strip()

    # Drain any extra lines (e.g. debug output) so they don't pollute next call
    ser.timeout = 0.1
    while True:
        extra = ser.readline().decode("utf-8", errors="replace").strip()
        if not extra:
            break
    ser.timeout = 3.0

    return response


# ── High-level API ─────────────────────────────────────────────────────────────

def dispense(ser: serial.Serial, channel: int, duration_ms: int) -> str:
    """
    Open solenoid valve on `channel` (1 or 2) for `duration_ms` milliseconds.
    The Arduino auto-closes the valve after the timer – even if Python crashes.
    """
    if channel not in (1, 2):
        raise ValueError("channel must be 1 or 2")
    if not (1 <= duration_ms <= 60_000):
        raise ValueError("duration_ms must be between 1 and 60 000")

    response = send_command(ser, f"OPEN {channel} {duration_ms}")
    print(f"[dispense] ch{channel}  {duration_ms} ms  →  {response}")
    return response


def dispense_seconds(ser: serial.Serial, channel: int, seconds: float) -> str:
    """Convenience wrapper – duration in seconds instead of milliseconds."""
    return dispense(ser, channel, int(seconds * 1000))


def close_valve(ser: serial.Serial, channel: int) -> str:
    """Force-close a valve immediately."""
    response = send_command(ser, f"CLOSE {channel}")
    print(f"[close]    ch{channel}  →  {response}")
    return response


def get_status(ser: serial.Serial) -> str:
    """Query and print the current state of both valves."""
    response = send_command(ser, "STATUS")
    print(f"[status]   {response}")
    return response


# ── Interactive CLI ────────────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════════╗
║   Water Dispenser Controller     ║
╠══════════════════════════════════╣
║  1  Dispense – Channel 1         ║
║  2  Dispense – Channel 2         ║
║  3  Dispense – Both channels     ║
║  4  Force-close a channel        ║
║  5  Check status                 ║
║  q  Quit                         ║
╚══════════════════════════════════╝
"""


def ask_duration() -> float:
    while True:
        try:
            val = float(input("  Duration (seconds, e.g. 1.5): "))
            if 0 < val <= 60:
                return val
            print("  Please enter a value between 0 and 60.")
        except ValueError:
            print("  Invalid input – enter a number.")


def interactive_cli(ser: serial.Serial):
    print(MENU)
    while True:
        choice = input("Select option: ").strip().lower()

        if choice == "1":
            secs = ask_duration()
            dispense_seconds(ser, 1, secs)

        elif choice == "2":
            secs = ask_duration()
            dispense_seconds(ser, 2, secs)

        elif choice == "3":
            secs = ask_duration()
            dispense_seconds(ser, 1, secs)
            dispense_seconds(ser, 2, secs)

        elif choice == "4":
            ch = input("  Which channel to close? (1/2): ").strip()
            if ch in ("1", "2"):
                close_valve(ser, int(ch))
            else:
                print("  Invalid channel.")

        elif choice == "5":
            get_status(ser)

        elif choice in ("q", "quit", "exit"):
            print("Closing all valves and exiting…")
            close_valve(ser, 1)
            close_valve(ser, 2)
            break

        else:
            print("  Unknown option.")

        print()  # blank line for readability


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Water Dispenser Controller")
    parser.add_argument("--port", help="Serial port (e.g. COM5 or /dev/ttyUSB0)", default="COM5")
    parser.add_argument("--baud", type=int, default=9600)
    args = parser.parse_args()

    try:
        ser = connect(port=args.port, baud=args.baud)
    except RuntimeError as e:
        print(f"[error] {e}")
        sys.exit(1)

    try:
        interactive_cli(ser)
    except KeyboardInterrupt:
        print("\n[info] Interrupted – closing valves.")
        close_valve(ser, 1)
        close_valve(ser, 2)
    finally:
        ser.close()
        print("[info] Serial port closed.")


if __name__ == "__main__":
    main()