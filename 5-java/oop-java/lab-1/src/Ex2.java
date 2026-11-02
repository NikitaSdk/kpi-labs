//Дана площа квадрата. Знайти сторону даного квадрата і мінімальну цілу сторону квадрата,
//в який вихідний квадрат може бути вписаний.
import java.util.Scanner;

public class Ex2 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        // Введення площі квадрата
        System.out.print("Введіть площу квадрата: ");
        double squareArea = input.nextDouble();
        // Перевірка, чи введено додатне значення площі
        if (squareArea <= 0) {
            System.out.println("Введено некоректне значення площі");
            return;
        }
        // Знаходження сторони вихідного квадрата
        double sideLength = Math.sqrt(squareArea);
        System.out.println("Сторона вихідного квадрата: " + sideLength);
        // Знаходження мінімальної цілої сторони квадрата
        double minIntegerSide = Math.floor(Math.sqrt(squareArea));
        System.out.println("Мінімальна ціла сторона квадрата: " + minIntegerSide);
    }
}

