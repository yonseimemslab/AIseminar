#include <LiquidCrystal.h>

// Setup the LiquidCrystal library with the pin numbers we have
// physically connected the module to.
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

// The analog pin the TMP36's Vout (sense) pin is connected to.
// The resolution is 10 mV / degree centigrade with a 
// 500 mV offset to allow for negative temperatures.
const int temperature_pin = A0;

const float baseline_temp = 19.0; // room temperature in Celcius
const float temp_resolution = 1.0;      // temperature resolution

const int period = 500;     // total cycle length in ms
const int n_samples = 100;  // # samples to be averaged

const int min_led = 8;      // pin holding the coldest led
const int max_led = 13;     // pin holding the hottest led



void setup() {
    lcd.begin(16, 2);   // Setup # LCD columns and rows
    Serial.begin(9600); // specify serial port baud rate
    
    // set the LED pins as outputs
    for(int pin = min_led; pin <= max_led; pin++){
        pinMode(pin ,OUTPUT);
        digitalWrite(pin, LOW);
    }
    for(int pin = A4; pin <= A5; pin++){
        pinMode(pin ,OUTPUT);
        digitalWrite(pin, LOW);
    }
    
    while (Serial.available() > 0);
}

void loop() {
    /*
    // make several measurements to reduce the noise
    float temperature = 0.0;
    for (int i = 0; i < n_samples; ++i) {
        int adc_reading = analogRead(temperature_pin);  
        float voltage = adc_reading * 5.0 / 1024.0;
        temperature += (voltage - 0.5) * 100 ;
        delay(0.5);
    }
    temperature *= 1.0 / n_samples;
    */

    float temperature = 0.0;
    // read temperature from serial port
    if (Serial.available() > 0)
        temperature = Serial.parseFloat();
    
    // write the temperature to
    
    // ...serial port     
    //Serial.println(temperature);
    
    // ...LCD                              
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("  Temp= ");
    lcd.print(temperature, 1);
    lcd.print("C");

    lcd.setCursor(0, 1);
    lcd.print("  t= ");
    lcd.print(millis() / 1000, 10);
    lcd.print("sec");

    // ...and LED strip

    for (int i = 1; i <= 2; ++i) {
        if (temperature >= baseline_temp + i * temp_resolution)
            digitalWrite(A4 + (i-1), HIGH);
        else
            digitalWrite(A4 + (i-1), LOW);
    }
    for (int i = 3; i <= 8; ++i) {
        if (temperature >= baseline_temp + i * temp_resolution)
            digitalWrite(min_led + (i-3), HIGH);
        else
            digitalWrite(min_led + (i-3), LOW);
    }

    // wait before the next loop
    delay(period - (millis() % period));
}
