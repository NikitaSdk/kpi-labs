package org.example;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Ex3Test {

    Object[]a, b;

    @BeforeEach
    void setUp() {
        a = new Object[] {0,"a",8};
        b = new Object[] {"b",7,8};
    }
    @Test
    void findUniqueElements() {

        Object[] expected = Ex3.findUniqueElements(a,b);
        Object[] actual = {0,"a","b",7};
        assertArrayEquals(expected,actual); //перевірка очікуваного і реального результату роботи функції.
    }
}