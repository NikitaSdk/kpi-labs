//У двозначному цілому числі поміняйте цифри місцями, знайдіть його квадратний корінь і найближче до кореня ціле.
import java.util.Scanner;
public class Ex1
{
    public static void main( String[] args )
    {
        // Введення двозначного цілого числа
        Scanner input = new Scanner(System.in);
        System.out.print("Введіть двозначне ціле число: ");
        int inputNumber = input .nextInt();

        if ( inputNumber < 0)
        {
            inputNumber =  inputNumber * (-1);
            int tensDigit = inputNumber / 10;
            int unitsDigit = inputNumber % 10;
            int swappedNumber = unitsDigit * 10 + tensDigit;
            // Знайдемо квадратний корінь і найближче до кореня ціле число
            double square = Math.sqrt(swappedNumber);
            int nearestInteger = (int) Math.round(square);
            // Виведемо результат
            System.out.println("Поміняне число: " + swappedNumber * (-1));
            System.out.println("Квадратний корінь: " + square);
            System.out.println("Найближче до кореня ціле число: " + nearestInteger);
            return;

        }
        // Поміняємо цифри місцями
        int tensDigit = inputNumber / 10;
        int unitsDigit = inputNumber % 10;
        int swappedNumber = unitsDigit * 10 + tensDigit;
        // Знайдемо квадратний корінь і найближче до кореня ціле число
        double square = Math.sqrt(swappedNumber);
        int nearestInteger = (int) Math.round(square);
        // Виведемо результат
        System.out.println("Поміняне число: " + swappedNumber);
        System.out.println("Квадратний корінь: " + square);
        System.out.println("Найближче до кореня ціле число: " + nearestInteger);
    }
}