package org.example;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Ex1Test {
    float[] a;
    @BeforeEach
    void setUp() {
        a = new float[] {1,2,10,15,18};
    }

    @Test
    void findMinDifference()
    {
        float expected = Ex1.findMinDifference(a);
        float actual = 1;
        assertEquals(expected,actual); //перевірка очікуваного і реального результату роботи функції.
    }
}