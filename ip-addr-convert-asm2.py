import socket
import struct

def ip_to_little_endian(ip_address):
    """Converts a dotted-decimal IP address to little-endian hex."""
    packed_ip = socket.inet_aton(ip_address) # Convert IP to packed bytes
    little_endian_ip = packed_ip[::-1] # Reverse the bytes for little-endian
    hex_ip = little_endian_ip.hex() # Convert to hexadecimal
    return hex_ip

# Example usage
ip_address = "172.16.0.153"
little_endian_hex = ip_to_little_endian(ip_address)
print(f"The little-endian hex representation of {ip_address} is: {little_endian_hex}")

def little_endian_to_ip(hex_ip):
    """Converts a little-endian hex IP address to dotted-decimal."""
    little_endian_bytes = bytes.fromhex(hex_ip) # Convert hex to bytes
    big_endian_bytes = little_endian_bytes[::-1] # Reverse the bytes for big-endian
    ip_address = socket.inet_ntoa(big_endian_bytes) # Convert bytes to IP
    return ip_address

# Example usage
hex_ip = "6401a8c0"
dotted_ip = little_endian_to_ip(hex_ip)
print(f"The dotted-decimal representation of {hex_ip} is: {dotted_ip}")