#include <Arduino.h>
// DHT Temperature & Humidity Sensor
// Unified Sensor Library Example
// Written by Tony DiCola for Adafruit Industries
// Released under an MIT license.

// REQUIRES the following Arduino libraries:
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2     // Digital pin connected to the DHT sensor 
// Feather HUZZAH ESP8266 note: use pins 3, 4, 5, 12, 13 or 14 --
// Pin 15 can work but DHT must be disconnected during program upload.

// Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11
//#define DHTTYPE    DHT22     // DHT 22 (AM2302)
//#define DHTTYPE    DHT21     // DHT 21 (AM2301)

// See guide for details on sensor wiring and usage:
//   https://learn.adafruit.com/dht/overview

DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;

void setup() {
  Serial.begin(9600);
  // Initialize device.
  dht.begin(); 
  // Serial.println(F("DHTxx Unified Sensor Example"));
  // Print temperature sensor details.
  byte flag=0;
  pinMode(LED_BUILTIN, OUTPUT);

  while (flag==0) //while signal not received
  {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on 
  delay(100);
  digitalWrite(LED_BUILTIN,LOW);   
  delay(100);       
    if (Serial.available() > 0) { // if there's any incoming byte
    flag = Serial.read();   // read the incoming byte and assign to flag
    for (int i=0; i<=5;i++){
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on 
      delay(500);                       // wait for half a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off 
      delay(500);
      }
    }
  }
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  // Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  // Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  // Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  // Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));
  Serial.println(F("11111111"));
  Serial.println(F("Hora [HH:MM:SS]; Temperatura[ºC];  Humedad[%];  OK?[I/O]"));
  // Set delay between sensor readings based on sensor details.
  delayMS = sensor.min_delay / 1000;

}

void loop() {
  // Delay between measurements.
  delay(delayMS);
  // Get temperature and humidity event
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  float temp=0;
  temp= event.temperature;
  dht.humidity().getEvent(&event);
  float humedad=0;
  humedad= event.relative_humidity;
  
  if (isnan(event.temperature)||isnan (event.relative_humidity)) {// If can't read, display error
    Serial.print(F("ERROR"));
    Serial.print(F(";"));
    Serial.print(F("ERROR"));
    Serial.println(F("0"));
  }
  else {// Else, print values
    Serial.print(temp);
    Serial.print(F(" ;"));
    Serial.print(humedad);
    Serial.print(F(" ;"));
    if(temp>27 || temp<17  || humedad>70 || event.relative_humidity<50 ) //If values are out of legal range, set alarm
    {
     Serial.println(F(" 1"));
    }
    else
    {
      Serial.println(F(" 0"));
    }
  }
}