package org.example;

import org.junit.Before;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Ex4Test {

    String type1, type2;

    @BeforeEach
    void setUP(){
        type1 = "123";
        type2 = "abc";
    }
    @Test
    void testAnalyzeArgumentType() {
        String expected1 = Ex4.analyzeArgumentType(type1);
        String actual1 = "Число";
        String expected2 = Ex4.analyzeArgumentType(type2);
        String actual2 = "Рядок";

        assertEquals(expected1, actual1);
        assertEquals(expected2, actual2);

    }
    @Test
    void testIsInteger() {
        assertTrue(Ex4.isNumeric(type1));
        assertFalse(Ex4.isNumeric(type2));

    }
}