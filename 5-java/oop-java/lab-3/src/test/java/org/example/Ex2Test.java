package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Ex2Test {

    String text;
    @BeforeEach
    void setUp() {
        text = "Cat";
    }
    @Test
    void convertToUnicode() {
        String expected = Ex2.convertToUnicode(text);
        String actual = "u0043u0061u0074";
        assertEquals(expected,actual);
    }
}