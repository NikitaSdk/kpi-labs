package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Ex4Test {

    float []a;
    int []b;
    int []c;

    @BeforeEach
    void setUp() {
        a = new float[] {67,44,90,5,3};
        b = new int[] {2,0,1,3,4};
        c = new int[5];
    }
    @Test
    void indexArray() {
        int[] expected = Ex4.IndexArray(a,c);
        int[] actual = b;
        assertArrayEquals(expected,actual); ////перевірка очікуваного і реального результату роботи функції.
    }
}