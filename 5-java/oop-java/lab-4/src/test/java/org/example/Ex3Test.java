package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Ex3Test {
    // Допоміжний метод для перевірки, чи книги відсортовані за видавництвом
    private boolean isSortedByPublisher(List<books> booksList) {
        for (int i = 0; i < booksList.size() - 1; i++) {
            if (booksList.get(i).getPublisher().compareTo(booksList.get(i + 1).getPublisher()) > 0) {
                return false;
            }
        }
        return true;
    }

    // Допоміжний метод для перевірки, чи книги відсортовані за ціною
    private boolean isSortedByPrice(List<books> booksList) {
        for (int i = 0; i < booksList.size() - 1; i++) {
            if (Float.compare(booksList.get(i).getPrice(), booksList.get(i + 1).getPrice()) > 0) {
                return false;
            }
        }
        return true;
    }
}