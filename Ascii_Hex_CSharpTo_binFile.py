#!/usr/bin/env python3
import re
import argparse

def parse_csharp_array(text):
    # Extract everything between { ... }
    match = re.search(r'\{(.*?)\}', text, re.DOTALL)
    if not match:
        raise ValueError("Could not find { ... } containing byte values.")

    content = match.group(1)

    # Match:
    #  - "text"   → ASCII string
    #  - 'A'      → single char
    #  - 0xFF     → hex
    #  - 123      → decimal
    token_pattern = r'"[^"]*"|\'[^\']\'|0x[0-9A-Fa-f]+|\d+'
    tokens = re.findall(token_pattern, content)

    data = bytearray()

    for token in tokens:
        token = token.strip()

        # ASCII string: "text"
        if token.startswith('"') and token.endswith('"'):
            string_content = token[1:-1]
            data.extend(string_content.encode('utf-8'))
            continue

        # Char literal: 'A'
        if token.startswith("'") and token.endswith("'") and len(token) == 3:
            data.append(ord(token[1]))
            continue

        # Hex: 0xNN
        if token.lower().startswith("0x"):
            value = int(token, 16)
        else:
            # Decimal
            value = int(token)

        if not (0 <= value <= 255):
            raise ValueError(f"Byte out of range 0–255: {token}")

        data.append(value)

    return data

def print_output_size(data, output_path):
    size_bytes = len(data)
    size_kb = size_bytes / 1024

    print("\n===== Output Info =====")
    print(f"File:          {output_path}")
    print(f"Byte Count:    {size_bytes} bytes")
    print(f"Size (KB):     {size_kb:.2f} KB")
    print(f"Hex Count:     {size_bytes}")
    print(f"Dec Count:     {size_bytes}")
    print("=======================\n")

def main():
    parser = argparse.ArgumentParser(description="Convert C# byte[] (hex, dec, ASCII) into binary")
    parser.add_argument("input", help="Input file containing C# byte[] array")
    parser.add_argument("output", help="Output .bin file")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    data = parse_csharp_array(text)

    with open(args.output, "wb") as f:
        f.write(data)

    print_output_size(data, args.output)

if __name__ == "__main__":
    main()
