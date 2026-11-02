package org.example;

//   26)
//   Сформувати масив b, елементами якого є елементи вихідного одновимірного масиву a,
//   розташовані в зворотному порядку.
import java.util.Scanner;
public class Ex5 {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Введення розміру масиву a
        System.out.print("Введіть розмір масиву a: ");
        int size = scanner.nextInt();

        // Введення елементів масиву a
        Object[] a = new Object[size];
        System.out.println("Введіть елементи масиву a:");

        for (int i = 0; i < size; i++) {
            System.out.print("a[" + i + "]: ");
            if (scanner.hasNextInt()) {
                a[i] = scanner.nextInt();
            }
            else {
                a[i] = scanner.next();
            }
        }

        Object[] b = new Object[size];
        b = revArray(a, b);

        for (int i = 0; i < b.length; i++) {
            System.out.println("B[" + i + "]: " + b[i]);
        }
    }

    public static Object[] revArray(Object[] A, Object[] B) {
        for (int i = 0; i < A.length; i++) {
            B[i] = A[A.length - 1 - i];
        }
        return B;
    }
}
