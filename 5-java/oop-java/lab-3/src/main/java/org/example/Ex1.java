package org.example;
import java.util.Scanner;

//    Створіть програму для шифрування\розшифровки тексту методом Цезаря. У ньому ключем є ціле число,
//    а шифрування\розшифровка полягає в сумовуванні\відніманні кодів символів відкритого тексту\криптотексту з ключем.

public class Ex1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введіть текст для шифрування: ");
        String plaintext = scanner.nextLine();

        System.out.print("Введіть ключ (ціле число): ");
        int key = scanner.nextInt();

        String ciphertext = encrypt(plaintext, key);
        System.out.println("Зашифрований текст: " + ciphertext);

        String decryptedText = decrypt(ciphertext, key);
        System.out.println("Розшифрований текст: " + decryptedText);

        scanner.close();
    }

    public static String encrypt(String text, int key) {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            char encryptedChar = (char) (ch + key);
            result.append(encryptedChar);
        }
        return result.toString();
    }
    public static String decrypt(String text, int key) {
        return encrypt(text, -key);
    }
}
