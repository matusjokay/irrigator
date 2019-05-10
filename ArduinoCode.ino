#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <BH1750.h>
#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT22
#define D3_teplota 3
#define BMP280_ADRESA (0x76)
DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(D3_teplota);
DallasTemperature sensors(&oneWire);

// inicializacia senzoru BMP z kniznice
Adafruit_BMP280 bmp;

// inicializacia senzoru BH1750 z kniznice
BH1750 luxSenzor;

int pin_A0_vlhkost_pody = A0;
int pin_A1_dazdovy = A1;
const int sensorMin = 0;     // sensor minimum
const int sensorMax = 1024;  // sensor maximum
int pin_A3_vhkostHD38 = A3;

byte  znak;

void setup () {
  Serial.begin (9600);
  Serial1.begin (9600);
  sensors.begin();
  if (!bmp.begin(BMP280_ADRESA)) {
    Serial.println("BMP280 senzor nenalezen, zkontrolujte zapojeni!");
    Serial1.println("X");
    while (1);
  }
  luxSenzor.begin();
  dht.begin();
}

void loop() {
  if (Serial1.available()) {
    delay(10);
    while (Serial1.available() > 0) {
      znak = Serial1.read();
      switch (znak) {
        case 65:  // 'A'
          vlhkost_pody1();
          break;
        case 66:  // 'B'
          vlhkost_pody2();
          break;
        case 67:  // 'C'
          dazdovy_senzor();
          break;
        case 68:  // 'D'
          vlhkost_vzduchu();
          break;
        case 69:  // 'E'
          teplota_vzduchu();
          break;
        case 70:  //'F'
          senzor_teploty1();
          break;
        case 71:  //'G'
          senzor_teploty2();
          break;
        case 72:  //'H'
          barometricky_tlak();
          break;
        case 73:  //'I'
          intenzita_svetla();
          break;
      }
    }
  }
}

// funkcia pre senzor vlhkosti pody
void vlhkost_pody1() {
  int vlhkost_pody_Value = analogRead(pin_A0_vlhkost_pody);
  int percent = convertToPercent(vlhkost_pody_Value);

  Serial1.print(percent);
  Serial.print(percent);

  delay(1000);
}

int convertToPercent(int value) {
  int percentValue = 0;
  percentValue = map(value, 1023, 456, 0, 100);
  if (percentValue > 100)
    percentValue = 100;
  return percentValue;
}

// funkcia pre dazdovy senzor
void dazdovy_senzor() {
  int sensorReading = analogRead(pin_A1_dazdovy);
  byte range =  map(sensorReading, sensorMin, sensorMax, 0, 3);
  Serial1.print(range);

  delay(1000);
}

void vlhkost_pody2() {
  int sensorValue = analogRead(pin_A3_vhkostHD38);
  int  percent = convertToPercent(sensorValue);
  Serial1.print(percent);

  delay(1000);
}

//senzor dht22
void vlhkost_vzduchu() {
  float vlhkost = dht.readHumidity();

  if (isnan(vlhkost)) {
    Serial.println(F("X"));
    return;
  }


  Serial1.print(vlhkost);
  Serial.print(vlhkost);

  delay(1000);
}

//senzor dht 22
void teplota_vzduchu() {

  float teplota = dht.readTemperature();

  if (isnan(teplota)) {
    Serial.println(F("X"));
    return;
  }

  Serial1.print(teplota);
  Serial.print(teplota);

  delay(1000);
}

// teplotny senzor ds18b20
void senzor_teploty1()
{
  // požádáme senzor o hodnotu teploty
  sensors.requestTemperatures();

  float teplota = sensors.getTempCByIndex(0);
  Serial1.print(teplota);
  Serial.print(sensors.getTempCByIndex(0));

  delay(1000);
}

void senzor_teploty2() {
  float teplota = bmp.readTemperature();
  Serial1.print(teplota);
  Serial.print(teplota);

  delay(1000);
}

void barometricky_tlak() {
  int korekcia = 32;
  float tlak = (bmp.readPressure() / 100.00) + korekcia;
  Serial1.print(tlak);
  Serial.print(tlak);

  delay(1000);
}


void intenzita_svetla() {
  uint16_t lux = luxSenzor.readLightLevel();

  Serial1.print(lux);
  Serial.print(lux);

  delay(1000);
}
