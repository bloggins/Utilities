#!/usr/bin/env python3
import re
import argparse
import sys
from pathlib import Path

def parse_csharp_array(text):
    """
    Extracts bytes from a C# array that may contain:
    - Hex: 0x41, 0xFF
    - Decimal: 65, 255
    """

    # Try hex first
    hex_vals = re.findall(r"0x([0-9A-Fa-f]{2})", text)
    if hex_vals:
        return bytes(int(h, 16) for h in hex_vals)

    # Fallback to decimal
    dec_vals = re.findall(r"\b(\d{1,3})\b", text)
    if dec_vals:
        return bytes(int(d) & 0xFF for d in dec_vals)

    raise ValueError("No valid C# byte array found.")


def format_outputs(data):
    """Return formatted outputs in multiple languages."""

    hex_string = data.hex().upper()

    cs_array = ", ".join(f"0x{b:02X}" for b in data)
    vb_array = ", ".join(f"&H{b:02X}" for b in data)

    return {
        "byte_count": len(data),
        "hex_string": hex_string,
        "csharp_array": f"new byte[] {{ {cs_array} }};",
        "vb_array": f"Dim bytes() As Byte = {{ {vb_array} }}",
        "preview": " ".join(f"{b:02X}" for b in data[:32]) +
                   (" ..." if len(data) > 32 else "")
    }


def main():
    parser = argparse.ArgumentParser(description="Convert a C# byte[] array to a .bin file and output formats.")
    parser.add_argument("input", help="Text file containing C# byte array OR raw pasted array string.")
    parser.add_argument("-o", "--output", default="output.bin", help="Output .bin filename")
    parser.add_argument("--raw", action="store_true", help="Treat input argument as raw C# array string instead of filename")
    args = parser.parse_args()

    # Read input
    if args.raw:
        text = args.input
    else:
        text = Path(args.input).read_text()

    try:
        data = parse_csharp_array(text)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # Write binary file
    Path(args.output).write_bytes(data)

    # Format and print
    info = format_outputs(data)
    print("\n=== Conversion Complete ===")
    print(f"Output BIN: {args.output}")
    print(f"Bytes: {info['byte_count']}")
    print(f"Hex: {info['hex_string']}")
    print("\nC# Array:")
    print(info['csharp_array'])
    print("\nVB.NET Array:")
    print(info['vb_array'])
    print("\nPreview:")
    print(info['preview'])
    print("==========================\n")


if __name__ == "__main__":
    main()
