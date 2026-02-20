#!/usr/bin/env python3
import base64

def base64_to_bin(b64_string, output_file):
    # Decode Base64 into raw bytes
    data = base64.b64decode(b64_string)

    # Write to a .bin file
    with open(output_file, "wb") as f:
        f.write(data)

    print(f"[+] Wrote {len(data)} bytes to {output_file}")

def main():
    # Example
    b64_input = input("Enter Base64 string: ").strip()
    output_path = "output.bin"

    base64_to_bin(b64_input, output_path)

if __name__ == "__main__":
    main()
