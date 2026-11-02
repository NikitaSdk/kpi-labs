package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.LinkedList;
import java.util.Scanner;
import java.util.TreeSet;

public class Ex2Test {

    @Test
    public void testIsPersonInQueue() {
        LinkedList<QueuePerson> queueList = new LinkedList<>();
        Ex2.initializeQueue(queueList, new TreeSet<>());

        // Перевірка, чи правильно розпізнається особа в черзі
        assertTrue(Ex2.isPersonInQueue(queueList, "Іванов", "Іван", "Іванович"), "Особа повинна бути в черзі");

        // Перевірка, чи правильно розпізнається відсутня особа в черзі
        assertFalse(Ex2.isPersonInQueue(queueList, "Невідомий", "Невідомий", "Невідомий"), "Особа не повинна бути в черзі");
    }

    @Test
    public void testAddQueuePerson() {
        LinkedList<QueuePerson> queueList = new LinkedList<>();
        TreeSet<QueuePerson> queueSet = new TreeSet<>();
        Ex2.initializeQueue(queueList, queueSet);

        // Підготовка введених даних для нового черговика
        InputStream in = new ByteArrayInputStream("6\nНовий\nОсоба\nПо батькові\nМісто6\nВулиця6\n6\n666".getBytes());
        System.setIn(in);

        // Запуск методу AddQueuePerson
        Ex2.addQueuePerson(queueList, new Scanner(System.in));

        // Перевірка, чи був доданий новий черговик
        assertTrue(Ex2.isPersonInQueue(queueList, "Новий", "Особа", "По батькові"), "Новий черговик повинен бути в черзі");
    }
}