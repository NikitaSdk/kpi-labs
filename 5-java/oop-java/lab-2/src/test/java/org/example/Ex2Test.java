package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Ex2Test {

    float a[], b[],c[];


    @BeforeEach
    void setUp() {
        a = new float[] {1,2,3,4,5}; // масив зрост
        b = new float[] {5,4,3,2,1}; // масив спад
        c = new float[] {7,3,8,2,9}; // масив зміш
    }
    @Test
    void checkIncr() {
        int expected = Ex2.checkOrder(a);
        int actual = 1;
        assertEquals(expected,actual);
    }
    @Test
    void checkDecr() {
        int expected = Ex2.checkOrder(b);
        int actual = 2;
        assertEquals(expected,actual);
    }
    @Test
    void checkNotSort() {
        int expected = Ex2.checkOrder(c);
        int actual = 0;
        assertEquals(expected,actual); ////перевірка очікуваного і реального результату роботи функції.
    }
}