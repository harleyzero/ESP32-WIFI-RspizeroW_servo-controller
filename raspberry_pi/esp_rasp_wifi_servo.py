#ESP32-c3のシリアルポートから打ち込んだ数字0-180を
#Wifiでraspiに送信してサーボをその角度にする

import pigpio
import socket

pi = pigpio.pi()
SERVO_PIN = 18
LED_PIN = 24

pi.set_mode(LED_PIN, pigpio.OUTPUT)

def set_angle(angle):
    pulse = int(600 + (angle / 180.0) * 1600)
    pi.set_servo_pulsewidth(SERVO_PIN, pulse)
    
    if angle > 120:
        pi.write(LED_PIN, 1)
        print(f"{angle}度 → LED点灯")
    else:
        pi.write(LED_PIN, 0)
        print(f"{angle}度 → LED消灯")

# サーバー起動
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5000))  # ポート5000で待ち受け
server.listen(1)
print("ESP32からの接続を待っています...")

try:
    while True:
        conn, addr = server.accept()
        print(f"接続されました: {addr}")
        
        with conn:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                
                try:
                    angle = float(data)
                    if 0 <= angle <= 180:
                        set_angle(angle)
                        conn.sendall(f"OK:{angle}\n".encode())
                    else:
                        print("範囲外の角度")
                        conn.sendall(b"ERROR:out of range\n")
                except ValueError:
                    print(f"不正なデータ: {data}")
                    conn.sendall(b"ERROR:invalid\n")

finally:
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    pi.write(LED_PIN, 0)
    pi.stop()
    server.close()
    print("終了しました")
