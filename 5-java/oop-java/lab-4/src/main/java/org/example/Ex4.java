package org.example;

//  Створити застосунок для вибірки елемента з стека з пріоритетами.
//  Стек (5 записів) створюються в програмному коді і є об'єктом класу LinkedList.
//  Запис в стек є об'єктом StackMember, що містить найменування програми (типу String),
//  обсяг пам'яті для програми в мегабайтах (типу int) і пріоритет програми (типу int).
//  Записи в стеці упорядковано відповідно до пріоритету і черговик
//  додається першим в чергу свого пріоритету.

import java.util.Collections;
import java.util.LinkedList;
import java.util.Scanner;

class Stack implements Comparable<Stack> {
    private String programName;
    private int memorySize;
    private int priority;

    public Stack(String programName, int memorySize, int priority) {
        this.programName = programName;
        this.memorySize = memorySize;
        this.priority = priority;
    }

    public String getProgramName() {
        return programName;
    }

    public int getMemorySize() {
        return memorySize;
    }

    public int getPriority() {
        return priority;
    }

    @Override
    public int compareTo(Stack other) {
        return Integer.compare(other.priority, this.priority);
    }

    @Override
    public String toString() {
        return "програма: " + programName + ", память: " + memorySize + " приорітет: " + priority;
    }
}

public class Ex4 {
    public static void main(String[] args) {
        LinkedList<Stack> priorityStack = new LinkedList<>();
        initializeStack(priorityStack);

        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("Оберіть опцію:");
            System.out.println("1. Показати стек");
            System.out.println("2. Додати елемент до стеку");
            System.out.println("3. Видалити елемент зі стеку");
            System.out.println("4. Вийти");

            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.println("Стек:");
                    displayStack(priorityStack);
                    break;
                case 2:
                    System.out.println("Введіть назву програми:");
                    String name = scanner.next();
                    System.out.println("Введіть обсяг пам'яті (в мегабайтах):");
                    int memory = scanner.nextInt();
                    System.out.println("Введіть пріоритет:");
                    int priority = scanner.nextInt();

                    priorityStack.add(new Stack(name, memory, priority));
                    Collections.sort(priorityStack);
                    System.out.println("Елемент додано до стеку.");
                    break;
                case 3:
                    if (!priorityStack.isEmpty()) {
                        Stack removedProgram = popFromPriorityStack(priorityStack);
                        System.out.println("Елемент, прибраний зі стеку:");
                        System.out.println(removedProgram);
                    } else {
                        System.out.println("Стек порожній.");
                    }
                    break;
                case 4:
                    System.out.println("Програма завершила роботу.");
                    System.exit(0);
                default:
                    System.out.println("Некоректний вибір. Спробуйте ще раз.");
                    break;
            }
        }

    }

    public static void initializeStack(LinkedList<Stack> priorityStack) {
        priorityStack.add(new Stack("chrom", 50, 3));
        priorityStack.add(new Stack("opera", 30, 1));
        priorityStack.add(new Stack("excel", 40, 2));
        priorityStack.add(new Stack("word", 20, 4));
        priorityStack.add(new Stack("firefox", 60, 3));
    }

    public static Stack popFromPriorityStack(LinkedList<Stack> priorityStack) {
        return priorityStack.pop();
    }

    public static void displayStack(LinkedList<Stack> priorityStack) {
        for (Stack stackMember : priorityStack) {
            System.out.println(stackMember);
        }
    }
}