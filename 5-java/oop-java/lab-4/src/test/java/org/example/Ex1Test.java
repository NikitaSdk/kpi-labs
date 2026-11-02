package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Ex1Test {

    @Test
    public void testDeleteBook() {
        Map<Integer, Book> libraryCatalog = new HashMap<>();
        Ex1.initializeLibrary(libraryCatalog);

        // Введення ISBN для видалення
        InputStream in = new ByteArrayInputStream("2".getBytes());
        System.setIn(in);

        // Запуск методу Delete_b
        Ex1.Delete_b(libraryCatalog, new Scanner(System.in));

        // Перевірка, чи була видалена книга з каталогу
        assertNull(libraryCatalog.get(2), "Книга з ISBN 2 повинна бути видалена");
    }

}

