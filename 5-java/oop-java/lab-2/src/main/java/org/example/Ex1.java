package org.example;

// 7)
// Визначити абсолютне значення найменшої різниці між двома будь-якими
// значеннями елементів вихідного одновимірного масиву a

import java.util.Scanner;
public class  Ex1 {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введіть розмір масиву: ");
        int size = scanner.nextInt();
        float[] a = new float[size];
        System.out.println("Введіть елементи масиву:");
        for (int i = 0; i < size; i++) {
            System.out.print("Елемент " + (i + 1) + ": ");
            a[i] = scanner.nextFloat();
        }
        float minDifference = findMinDifference(a);
        System.out.println("Найменша різниця між елементами: " + minDifference);
        scanner.close();
    }
    static float findMinDifference(float[] arr) {
        if (arr.length < 2) {
            System.out.println("Масив повинен містити принаймні два елементи.");
            return -1.0f;
        }
        float minDifference = Math.abs(arr[1] - arr[0]);
        for (int i = 2; i < arr.length; i++)
        {
            float difference = Math.abs(arr[i] - arr[i - 1]);
            if (difference < minDifference) {
                minDifference = difference;
            }
        }
        return minDifference;
    }
}