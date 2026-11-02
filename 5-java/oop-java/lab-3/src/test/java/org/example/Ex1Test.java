package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Ex1Test {

    String encr_text;
    String decr_text;
    int key;
    @BeforeEach
    void setUp()
    {
        encr_text = "Hello World";
        decr_text = "Khoor#Zruog";
        key = 3;

    }
    @Test
    void encrypt() {
        String expected = Ex1.encrypt(encr_text, key);
        String actual = decr_text;
        assertEquals(expected,actual);
    }

    @Test
    void decrypt() {
        String expected = Ex1.decrypt(decr_text, key);
        String actual = encr_text;
        assertEquals(expected,actual);
    }
}