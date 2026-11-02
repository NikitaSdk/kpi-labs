package org.example;

// Побудувати програму для роботи з класом для зберігання даних про повідомлення в форумі (автор, тема, текст,
// час, дата створення та редагування). Програма повинна забезпечувати функції введення, редагування, виведення значень.

import java.util.Scanner;

class Message {
    private String author, topic, text, create_t, edit_t;

    public Message(String author, String topic, String text, String creationTime, String editTime) {
        this.author = author;
        this.topic = topic;
        this.text = text;
        this.create_t = creationTime;
        this.edit_t = editTime;
    }

    public void displayMessage() {
        System.out.println("автор: " + author);
        System.out.println("тема: " + topic);
        System.out.println("текст: " + text);
        System.out.println("час створення: " + create_t);
        System.out.println("час редагування: " + edit_t);
    }

    public void editMessage(String newText, String editTime) {
        this.text = newText;
        this.edit_t = editTime;
    }
}

public class Ex1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Message message = null;

        while (true) {
            System.out.println("Оберіть опцію:");
            System.out.println("1. Введення інформації");
            System.out.println("2. Редагування інформації");
            System.out.println("3. Виведення інформації");
            System.out.println("0. Вихід");

            int choice = scanner.nextInt();
            scanner.nextLine(); // consume the newline character

            switch (choice) {
                case 1:
                    System.out.println("Введіть автора:");
                    String author = scanner.nextLine();

                    System.out.println("Введіть тему:");
                    String topic = scanner.nextLine();

                    System.out.println("Введіть текст:");
                    String text = scanner.nextLine();

                    System.out.println("Введіть час створення:");
                    String creationTime = scanner.nextLine();

                    String editTime = "ще не редагувалося";

                    message = new Message(author, topic, text, creationTime, editTime);

                    System.out.println("\nСтворене повідомлення:");
                    message.displayMessage();
                    break;

                case 2:
                    if (message != null) {
                        System.out.println("Введіть новий текст для редагування:");
                        String newText = scanner.nextLine();

                        System.out.println("Введіть час редагування:");
                        String newEditTime = scanner.nextLine();

                        message.editMessage(newText, newEditTime);

                        System.out.println("\nВідредаговане повідомлення:");
                        message.displayMessage();
                    } else {
                        System.out.println("Спочатку введіть інформацію (опція 1).");
                    }
                    break;

                case 3:
                    if (message != null) {
                        System.out.println("\nІнформація про повідомлення:");
                        message.displayMessage();
                    } else {
                        System.out.println("Спочатку введіть інформацію (опція 1).");
                    }
                    break;

                case 0:
                    System.out.println("Вихід");
                    scanner.close();
                    System.exit(0);
                    break;

                default:
                    System.out.println("Невірний вибір. Спробуйте ще раз.");
            }
        }
    }
}