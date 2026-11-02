package org.example;
import java.util.Scanner;

//  16)
//  Виведіть на дисплей значення тих елементів масивів a і b, які є тільки в одному з масивів, і відсутні в іншому масиві
//  (передбачається, що і масив a, і масив b є множинами, тобто кожен з них не містить елементів з однаковими значеннями).

public class Ex3 {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введіть розмір першого масиву: ");
        int size1 = scanner.nextInt();
        Object[] array1 = new Object[size1];
        System.out.println("Введіть елементи першого масиву:");
        for (int i = 0; i < size1; i++) {
            System.out.print("Елемент" + (i + 1) + ": ");
            if (scanner.hasNextInt()) {
                array1[i] = scanner.nextInt();
            }
            else {
                array1[i] = scanner.next();
            }
        }

        System.out.print("Введіть розмір другого масиву: ");
        int size2 = scanner.nextInt();
        Object[] array2 = new Object[size2];
        System.out.println("Введіть елементи другого масиву:");
        for (int i = 0; i < size2; i++) {
            System.out.print("Елемент" + (i + 1) + ": ");
            if (scanner.hasNextInt()) {
                array2[i] = scanner.nextInt();
            }
            else {
                array2[i] = scanner.next();
            }
        }

        // Вивід елементів
        System.out.println("Перший масив:");
        printArray(array1);
        System.out.println("Другий масив:");
        printArray(array2);

        // Визначення унікальних елементів та їх запис в масив C
        Object[] arrayC = findUniqueElements(array1, array2);
        System.out.println("Унікальні елементи ");
        printArray(arrayC);

        scanner.close();
    }

    public static void printArray(Object[] array) {
        for (Object element : array) {
            System.out.print(element + " ");
        }
        System.out.println();
    }

    public static Object[] findUniqueElements(Object[] arrayA, Object[] arrayB) {
        int sizeC = arrayA.length + arrayB.length;
        Object[] arrayC = new Object[sizeC];
        int indexC = 0;

        for (int i = 0; i < arrayA.length; i++) {
            Object valueA = arrayA[i];
            boolean isUnique = true;
            // Перевірка, чи є елемент з arrayA унікальним відносно arrayB
            for (int j = 0; j < arrayB.length; j++) {
                Object valueB = arrayB[j];
                if (valueA.equals(valueB)) {
                    isUnique = false;
                    break;
                }
            }
            // Якщо елемент унікальний, додаємо його до arrayC
            if (isUnique) {
                arrayC[indexC] = valueA;
                indexC++;
            }
        }
        for (int i = 0; i < arrayB.length; i++) {
            Object valueB = arrayB[i];
            boolean isUnique = true;

            // Перевірка, чи є елемент з arrayB унікальним відносно arrayA
            for (int j = 0; j < arrayA.length; j++) {
                Object valueA = arrayA[j];
                if (valueB.equals(valueA)) {
                    isUnique = false;
                    break;
                }
            }
            // Якщо елемент унікальний, додаємо його до arrayC
            if (isUnique) {
                arrayC[indexC] = valueB;
                indexC++;
            }
        }
        Object[] resultArray = new Object[indexC];
        System.arraycopy(arrayC, 0, resultArray, 0, indexC);
        return resultArray;
    }
}

