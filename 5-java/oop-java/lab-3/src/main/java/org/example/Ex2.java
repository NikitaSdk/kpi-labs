package org.example;

//  Створіть програму для визначення коду введеного символу в 16-ном представлені в форматі ‘uXXXX’.
//  Забезпечте циклічність виконання програми до введення символу пробіл.
//  Перевірте правильність роботи програми,скориставшись нею для отримання кодів символів
//  в будь-якому слові (наприклад,"cat") і
//  вивівши на екран слово з отриманих кодів.

import java.util.Scanner;

public class Ex2 {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print("Введіть слово або букву (або пробіл для завершення): ");
            String input = scanner.nextLine();
            if (input.trim().isEmpty() || input.equals(" ")) {
                System.out.println("Програма завершена.");
                break;
            }
            String unicodeCodes = convertToUnicode(input);
            System.out.println("Коди: " + unicodeCodes);
        }
        scanner.close();
    }

    public static String convertToUnicode(String input) {
        StringBuilder unicodeCodes = new StringBuilder();

        for (char ch : input.toCharArray()) {
            unicodeCodes.append(String.format("u%04X", (int) ch));
        }
        return unicodeCodes.toString();
    }
}




