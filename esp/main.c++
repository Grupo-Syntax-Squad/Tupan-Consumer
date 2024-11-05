#include <ArduinoMqttClient.h>
#include <WiFi.h>
#include <ArduinoJson.h>

char ssid[] = "MecWell";        // your network SSID (name)
char pass[] = "smmsmmsmm";    // your network password (use for WPA, or use as key for WEP)

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "192.168.241.167";
int        port     = 1883;
const char topic[]  = "env/sample";

// ms
const long interval = 300;
unsigned long previousMillis = 0;

int count = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only

  }

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


void loop() {
  // call poll() regularly to allow the library to send MQTT keep alive which

  mqttClient.poll();
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {

    // save the last time a message was sent
    previousMillis = currentMillis;
    
    String macAddress = WiFi.macAddress();
    StaticJsonDocument<200> payload;
    payload["mac"] = macAddress;
    payload["timestamp"] = millis();
    payload["temperature"] = random(20, 30);
    payload["amount_of_rain"] = random(20, 30);
    payload["wind_speed"] = random(20, 30);

    Serial.print("Mac Address: ");
    Serial.println(macAddress);
    
    Serial.print("Sending payload to topic: ");
    Serial.println(topic);
    Serial.println(payload.as<String>());

    mqttClient.beginMessage(topic);
    mqttClient.print(payload.as<String>());
    mqttClient.endMessage();
  }
}