# ESP32-WIFI-RaspizeroW Servo Controller

ESP32-C3（XIAO）とRaspberry Pi Zero WをWiFi経由で接続し、サーボモーターを制御するプロジェクト。

## 構成
XIAO ESP32-C3
↓ WiFi
Raspberry Pi Zero W
↓
サーボ S3071 2BBMG

## ハードウェア

- Raspberry Pi Zero W
- XIAO ESP32-C3
- サーボモーター：S3071 2BBMG
- LED（GPIO24、120度超えで点灯）

## ピン配線

### サーボ（Raspberry Pi）
| サーボ | Raspberry Pi |
|---|---|
| 茶（GND） | Pin 6 |
| 赤（VCC） | 外部5V |
| オレンジ（信号） | Pin 12（GPIO18） |

### LED（Raspberry Pi）
| | Raspberry Pi |
|---|---|
| +（330Ω経由） | Pin 18（GPIO24） |
| - | GND |

## 使い方

### Raspberry Pi側
​```bash
sudo systemctl start pigpiod
python3 raspberry_pi/esp_rasp_wifi_servo.py
​```

### ESP32側
1. `esp32/sketch_jun11a.ino` をArduino IDEで開く
2. SSIDとパスワードを書き換える
3. XIAO ESP32-C3に書き込む
4. シリアルモニタで角度（0〜180）を入力

## 動作環境

- Raspberry Pi OS
- Python 3
- pigpio
- Arduino IDE 2.x
- ESP32 board package 2.0.17
