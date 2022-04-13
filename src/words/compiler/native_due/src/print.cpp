#include <Arduino.h>

extern "C" {
    int ledPin = 13;
    void serial_begin() {
        pinMode(ledPin, OUTPUT);
        delay(1000);                  // waits for a second
        Serial.begin(9600);
        delay(1000);                  // waits for a second
    }

    void print_num(int num) {
        Serial.print(num);
    }

    void blink_led() {
//        digitalWrite(ledPin, HIGH);   // sets the LED on
//        delay(200);                  // waits for a second
//        digitalWrite(ledPin, LOW);    // sets the LED off
//        delay(200);                  // waits for a second
//        digitalWrite(ledPin, HIGH);   // sets the LED on
//        delay(200);                  // waits for a second
//        digitalWrite(ledPin, LOW);    // sets the LED off
//        delay(200);                  // waits for a second
    }
    void inf_blink() {
        while (true) {
            delay(1000);                  // waits for a second
            digitalWrite(ledPin, HIGH);   // sets the LED on
            delay(1000);                  // waits for a second
            digitalWrite(ledPin, LOW);    // sets the LED off
        }
    }
}
