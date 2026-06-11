//ESP32-c3のシリアルポートから打ち込んだ数字0-180を
//Wifiでraspiに送信してサーボをその角度にする
#include <WiFi.h>

const char* ssid     = "Buffalo-G-3270";
const char* password = "nsgb7fjkx47tx";
const char* host     = "192.168.11.30";
const int   port     = 5000;

WiFiClient client;

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.print("WiFi接続中...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi接続完了！");
    Serial.print("IPアドレス: ");
    Serial.println(WiFi.localIP());
    Serial.println("角度を入力してください（0〜180）:");
}

void loop() {
    if (Serial.available()) {
        String input = Serial.readStringUntil('\n');
        input.trim();
        
        float angle = input.toFloat();
        
        if (angle < 0 || angle > 180) {
            Serial.println("ERROR: 0〜180の範囲で入力してください");
            return;
        }
        
        if (client.connect(host, port)) {
            client.println(input);
            Serial.print("送信しました: ");
            Serial.println(input);
            
            long timeout = millis() + 3000;
            while (client.available() == 0) {
                if (millis() > timeout) {
                    Serial.println("タイムアウト");
                    client.stop();
                    return;
                }
            }
            
            String response = client.readStringUntil('\n');
            Serial.print("ラズパイの返答: ");
            Serial.println(response);
            
            client.stop();
        } else {
            Serial.println("ERROR: ラズパイに接続できません");
        }
    }
}