package org.example;
import java.util.Scanner;

//    22)
//    Сформувати масив b,елементами якого є значення індексів елементів вихідного одновимірного масиву a
//    в порядку убування значень елементів.


public class Ex4 {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Введення розміру масиву A
        System.out.print("Введіть розмір масиву A: ");
        int size = scanner.nextInt();

        // Введення елементів масиву A
        float[] A = new float[size];
        System.out.println("Введіть елементи масиву A:");

        for (int i = 0; i < size; i++) {
            System.out.print("A[" + i + "]: ");
            A[i] = scanner.nextFloat();
        }

        System.out.println("Масив B :");
        int[] B = new int[size];
        B = IndexArray(A, B);
        for (int i = 0; i < B.length; i++) {
            System.out.println("B[" + i + "]: " + B[i]);
        }
    }

    public static int[] IndexArray(float[] A, int[] B) {
        // Копіюємо масив A індексів
        for (int i = 0; i < B.length; i++) {
            B[i] = i;
        }
        // Сортуємо масив A та відповідні індекси в масиві B за спаданням
        for (int i = 0; i < A.length - 1; i++) {
            for (int j = 0; j < A.length - i - 1; j++) {
                if (A[j] < A[j + 1]) {
                    // Обмін значень між елементами масиву A
                    float tempA = A[j];
                    A[j] = A[j + 1];
                    A[j + 1] = tempA;

                    // Обмін відповідних індексів в масиві B
                    int tempB = B[j];
                    B[j] = B[j + 1];
                    B[j + 1] = tempB;
                }
            }
        }
        return B;
    }
}
