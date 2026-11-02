package org.example;
//  12)
//  Визначити, чи утворюють значення елементів вихідного одновимірного масиву a:
//  строго зростаючу послідовність (ai < ai+1),
//  строго спадну послідовність (ai > ai+1) або елементи масиву не впорядковані,
//  і вивести для кожного випадку відповідне повідомлення.

import java.util.Scanner;
public class Ex2 {
    public static void main(String[] args)
    {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введіть розмір масиву: ");
        int size = scanner.nextInt();
        float[] a = new float[size];
        System.out.println("Введіть елементи масиву:");
        for (int i = 0; i < size; i++) {
            System.out.print("Елемент " + (i + 1) + ": ");
            a[i] = scanner.nextFloat();
        }
        int b = checkOrder(a);

        if (b==1) {
            System.out.println("Елементи утворюють строго зростаючу послідовність.");
        }
        else if (b==2) {
            System.out.println("Елементи утворюють строго спадаючу послідовність.");
        }
        else {
             System.out.println("Елементи масиву не впорядковані.");
        }
        scanner.close();
    }
    static int checkOrder(float[] arr) {
        int a = 0;
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] < arr[i + 1]) { // зростаюча
                if (a == 2) {
                    a = 0;
                    break;
                }
                a = 1;
            }
            else if (arr[i] > arr[i + 1]) { // спадаюча
                if (a == 1) {
                    a = 0;
                    break;
                }
                a = 2;
            }
        }
        return a;
    }
}

