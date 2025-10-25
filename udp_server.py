import socket, struct, zlib, os

STORE_DIR = "server_storage"
os.makedirs(STORE_DIR, exist_ok=True)

UDP_PORT = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))
print("UDP server listening on port", UDP_PORT)

while True:
    data, addr = sock.recvfrom(65536)
    hdr = data[:19]
    seq = struct.unpack_from("<I", hdr, 0)[0]
    payload_len = struct.unpack_from("<I", hdr, 11)[0]
    payload = data[19:19+payload_len]
    crc = struct.unpack_from("<I", hdr, 15)[0]

    # Integrity check
    if zlib.crc32(payload) & 0xffffffff != crc:
        print(f"Corrupted chunk {seq}")
        continue

    # Save payload
    fname = os.path.join(STORE_DIR, f"{seq:06d}.chunk")
    with open(fname, "wb") as f:
        f.write(payload)
    print(f"Stored chunk seq={seq}")

