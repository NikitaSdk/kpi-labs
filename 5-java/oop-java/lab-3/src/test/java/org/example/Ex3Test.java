package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Ex3Test {
    String test1, test2, test3;
    @BeforeEach
    void setUp()
    {
        test1 = "myVariable";
        test2 = "if";
        test3 = "123Illegal";
    }
    @Test
    void testIdentifier() {
        String expected = Ex3.analyzeArgumentType(test1);
        String actual = "Identifier";
        assertEquals(expected,actual);
    }

    @Test
    void testKeyword() {
        String expected = Ex3.analyzeArgumentType(test2);
        String actual = "Keyword";
        assertEquals(expected,actual);
    }
    @Test
    void testIllegal() {
        String expected = Ex3.analyzeArgumentType(test3);
        String actual = "Illegal";
        assertEquals(expected,actual);
    }
}