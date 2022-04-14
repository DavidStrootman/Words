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
        Serial.print("Binary output: ");
        Serial.println(num, BIN);
        Serial.print("Decimal output: ");
        Serial.println(num, DEC);
    }

    void a_unittest(int x, int y) {
        Serial.print("test_output: ");
        bool test = false;
        test = x + y == 3;
        Serial.println(test);
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
