package org.example;

// Створити клас Фігура, яка має координати розташування і віртуальний метод переміщення.
// Створіть пов'язаний з ним клас - Еліпс.

import java.util.Scanner;

class Figure {
    protected int x, y;

    public Figure(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void Move_figure(int d_x, int d_y) {
        this.x += d_x;
        this.y += d_y;
        System.out.println("нові координати: (" + this.x + ", " + this.y + ")");
    }
}

class Ellipse extends Figure {
    public Ellipse(int x, int y) {
        super(x, y);
    }

    @Override
    public void Move_figure(int d_x, int d_y) {
        super.Move_figure(d_x, d_y);
        System.out.println("нове положення еліпса (" + x + ", " + y + ")");
    }
}

public class Ex4 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Зчитування початкових координат
        System.out.print("Введіть початкові координати еліпса (x y): ");
        int initialX = scanner.nextInt();
        int initialY = scanner.nextInt();

        // Створення екземпляра класу еліпс
        Ellipse ellipse = new Ellipse(initialX, initialY);

        // Зчитування координат для зсуву
        System.out.print("Введіть зсув координат (d_x d_y): ");
        int deltaX = scanner.nextInt();
        int deltaY = scanner.nextInt();

        // Метод переміщення
        ellipse.Move_figure(deltaX, deltaY);

        scanner.close();
    }
}
