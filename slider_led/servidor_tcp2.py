import socket
import serial

# --- CONFIGURACIÓN ---
SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE    = 9600

HOST = "0.0.0.0"
PORT = 5001
# ----------------------

def parse_cmd(cmd: str):
    cmd = cmd.strip().upper()

    if not cmd.startswith("LED"):
        return (False, None)

    if len(cmd) < 6:  # mínimo "LED1:0"
        return (False, None)

    led_char = cmd[3:4]
    if led_char not in ("1", "2", "3", "4"):
        return (False, None)

    if ":" not in cmd:
        return (False, None)

    parts = cmd.split(":", 1)
    if len(parts) != 2:
        return (False, None)

    try:
        val = int(parts[1])
    except:
        return (False, None)

    if val < 0: val = 0
    if val > 255: val = 255

    return (True, f"LED{led_char}:{val}")

def main():
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    ser.reset_input_buffer()

    print(f"Conectado a Arduino en {SERIAL_PORT} a {BAUDRATE} baudios")
    print(f"Servidor LED2 escuchando en {HOST}:{PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                if not data:
                    continue

                raw = data.decode("utf-8", errors="ignore").strip()
                ok, cmd = parse_cmd(raw)

                if not ok:
                    conn.sendall(b"ERR:CMD\n")
                    continue

                ser.write((cmd + "\n").encode("utf-8"))
                ser.flush()

                resp = ser.readline().decode("utf-8", errors="ignore").strip()
                if not resp:
                    resp = "ERR:TIMEOUT"

                conn.sendall((resp + "\n").encode("utf-8"))

if __name__ == "__main__":
    main() 
