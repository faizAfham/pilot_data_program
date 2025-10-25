import socket, struct, zlib, time
import numpy as np

UDP_IP = "127.0.0.1"
UDP_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

CHUNK_SAMPLES = 1024
FMT = 1  # int8 IQ

start_time = time.time()

for seq in range(100):  # simulate 100 chunks
    timestamp_ms = int((time.time() - start_time) * 1000)  # relative ms
    t = np.arange(CHUNK_SAMPLES, dtype=np.float32)/200000.0
    I = (127*np.cos(2*np.pi*10000*t)).astype(np.int8)
    Q = (127*np.sin(2*np.pi*10000*t)).astype(np.int8)
    payload = np.empty((CHUNK_SAMPLES*2,), dtype=np.int8)
    payload[0::2] = I
    payload[1::2] = Q
    payload_bytes = payload.tobytes()
    crc = zlib.crc32(payload_bytes) & 0xffffffff
    payload_len = len(payload_bytes)
    hdr = struct.pack("<I I H B I I", seq, timestamp_ms, CHUNK_SAMPLES, FMT, payload_len, crc)
    sock.sendto(hdr + payload_bytes, (UDP_IP, UDP_PORT))
    print(f"Sent chunk seq={seq}")
    time.sleep(0.01)  # simulate delay between chunks

