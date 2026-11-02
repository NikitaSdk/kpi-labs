//Дано ціле тризначне число. Знайти суму і добуток його цифр.
import java.util.Scanner;
public class Ex3
{
    public static void main(String[] args)
    {
        // Створюємо об'єкт Scanner для зчитування введених даних
        Scanner input = new Scanner(System.in);
        // Введення тризначного числа
        System.out.print("Введіть тризначне число: ");
        int number = input.nextInt();
        if ( number <= 0 ){
            number =  Math.abs(number);
            int digit1 = number / 100;
            int digit2 = (number / 10) % 10;
            int digit3 = number % 10;
            // Знаходження суми цифр
            int sum = digit1 + digit2 + digit3;
            System.out.println("Сума цифр: " + sum);
            // Знаходження добутку цифр
            int prod = digit1 * digit2 * digit3;
            System.out.println("Добуток цифр: " + prod);
            return;
        }
        // Розбиваємо число на цифри
        int digit1 = number / 100;
        int digit2 = (number / 10) % 10;
        int digit3 = number % 10;
        // Знаходження суми цифр
        int sum = digit1 + digit2 + digit3;
        System.out.println("Сума цифр: " + sum);
        // Знаходження добутку цифр
        int prod = digit1 * digit2 * digit3;
        System.out.println("Добуток цифр: " + prod);
    }
}