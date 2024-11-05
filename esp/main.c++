#include <ArduinoMqttClient.h>
#include <WiFi.h>
#include <ArduinoJson.h>

char ssid[] = "nome_da_rede";        // your network SSID (name)
char pass[] = "senha_da_rede";    // your network password (use for WPA, or use as key for WEP)
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "test.mosquitto.org";
int        port     = 1883;
const char topic[]  = "syntax/squad";

// ms
const long interval = 3600;
unsigned long previousMillis = 0;

int count = 0;
void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only

  }

  connectWiFi();
  connectMqtt();
}
void connectWiFi() {
  // attempt to connect to Wifi network:
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  Serial.println(pass);

  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();
}
void connectMqtt() {
  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

StaticJsonDocument<200> makePayload() {
  String macAddress = WiFi.macAddress();
  StaticJsonDocument<200> payload;
  payload["mac"] = macAddress;
  payload["timestamp"] = millis();
  JsonObject data = payload.createNestedObject("data");
  data["temperature"] = random(20, 30);
  data["amount_of_rain"] = random(20, 30);
  data["wind_speed"] = random(20, 30);
  return payload;
}
void sendPayload(StaticJsonDocument<200> payload) {
  String macAddress = WiFi.macAddress();
  Serial.print("Mac Address: ");
  Serial.println(macAddress);

  Serial.print("Sending this json: ");
  Serial.println(payload.as<String>());

  Serial.print("Sending payload to topic: ");
  Serial.println(topic);
  Serial.println(payload.as<String>());

  mqttClient.beginMessage(topic);
  mqttClient.print(payload.as<String>());
  mqttClient.endMessage();
}
void loop() {
  // call poll() regularly to allow the library to send MQTT keep alive which

  mqttClient.poll();
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {

    // save the last time a message was sent
    previousMillis = currentMillis;
    
    StaticJsonDocument<200> payload = makePayload();
    sendPayload(payload);
  }
}