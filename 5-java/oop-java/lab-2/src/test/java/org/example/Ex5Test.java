package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Ex5Test {
    Object []a, b, c;

    @BeforeEach
    void setUp() {
        a = new Object[] {"a",-6,6,23,8};
        b = new Object[] {8,23,6,-6,"a"};
        c = new Object[5];

    }
    @Test
    void revArray() {
        Object[] expected = Ex5.revArray(a,c);
        Object[] actual = b;
        assertArrayEquals(expected,actual);
    }
}