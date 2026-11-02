package org.example;

//  Створити клас «Вікно», що включає координати (left, top, right, bottom) і колір вікна,
//  та клас «Вікно з текстом», що включає поля текст, колір тексту у вікні.

import java.util.Scanner;

class Window {
    private int left, right, up, down;
    private String col_window;

    public Window(int left, int up, int right, int down, String col_window) {
        this.left = left;
        this.up = up;
        this.right = right;
        this.down = down;
        this.col_window = col_window;
    }

    public void displayWindowInfo() {
        System.out.println("координати: (" + left + ", " + up + ", " + right + ", " + down + ")");
        System.out.println("колір: " + col_window);
    }
}

class TextWindow extends Window {
    private String text, text_col;

    public TextWindow(int left, int top, int right, int bottom, String window_col, String text, String text_col) {
        super(left, top, right, bottom, window_col);
        this.text = text;
        this.text_col = text_col;
    }

    public void displayTextWindowInfo() {
        super.displayWindowInfo();
        System.out.println("текст: " + text);
        System.out.println("колір тексту: " + text_col);
    }
}

public class Ex3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Введіть координати та колір вікна:");
        System.out.print("left: ");
        int left = scanner.nextInt();
        System.out.print("up: ");
        int up = scanner.nextInt();
        System.out.print("right: ");
        int right = scanner.nextInt();
        System.out.print("down: ");
        int down = scanner.nextInt();
        System.out.print("колір вікна: ");
        String windowColor = scanner.next();

        Window window = new Window(left, up, right, down, windowColor);

        System.out.println("Інформація про вікно:");
        window.displayWindowInfo();
        System.out.println();

        // Введення тексту та колору тексту для другого об'єкта TextWindow
        System.out.println("Введіть текст та колір тексту:");
        System.out.print("текст: ");
        String text = scanner.next();
        System.out.print("колір тексту: ");
        String textColor = scanner.next();

        TextWindow textWindow = new TextWindow(left, up, right, down, windowColor, text, textColor);

        System.out.println("\nІнформація про текстове вікно:");
        textWindow.displayTextWindowInfo();

        scanner.close();
    }
}