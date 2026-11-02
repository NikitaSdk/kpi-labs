package org.example;

//  Аналіз аргументів, що задаються під час запуску програми.
//  Програма визначає тип аргумент - ціле число або рядок (шаблон: цілим числом
//  вважається рядок, яка містить цифри і, крім того, першим символом рядка може
//  бути цифра, знак "+" або "-"). Потім серед аргументів-чисел шукається максимальне
//  число. Програма виводить кількість заданих аргументів, їх значення, кількість
//  аргументів-чисел і значення максимального числа.

public class Ex4 {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Не вказані аргументи.");
            return;
        }
        int numberOfNumbers = 0;
        double maxNumber = Double.NEGATIVE_INFINITY;
        System.out.println("Кількість аргументів: " + args.length);
        for (String arg : args) {
            System.out.println("Аргумент: " + arg + ", Тип: " + analyzeArgumentType(arg));
            if (isNumeric(arg.replace(',', '.'))) {
                numberOfNumbers++;
                double currentNumber = Double.parseDouble(arg.replace(',', '.'));
                if (currentNumber > maxNumber) {
                    maxNumber = currentNumber;
                }
            }
        }
        System.out.println("Кількість аргументів-чисел: " + numberOfNumbers);
        System.out.print("Максимальне число: ");
        if (numberOfNumbers > 0) {
            System.out.println(maxNumber);
        } else {
            System.out.println("немає");
        }
    }
    public static String analyzeArgumentType(String arg) {
        if (isNumeric(arg)) {
            return "Число";
        } else {
            return "Рядок";
        }
    }
    public static boolean isNumeric(String s) {
        try {
            Double.parseDouble(s);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
}