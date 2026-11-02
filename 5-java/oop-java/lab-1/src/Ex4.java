//Дано сторони прямокутника, знайти його діагональ, периметр.
import java.util.Scanner;
public class Ex4
{
    public static void main(String[] args)
    {
        Scanner input = new Scanner(System.in);
        // Введення сторін прямокутника
        System.out.print("Введіть довжину прямокутника: ");
        double length = input.nextDouble();
        System.out.print("Введіть ширину прямокутника: ");
        double width = input.nextDouble();
        //перевірка на коррекність вводу даних
        if ( length <=0 || width <= 0 ) {
            System.out.println("Введено некоректні значення ширини та довжиши");
            return;
        }
        // Периметр прямокутника
        double perimeter = 2 * (length + width);
        System.out.println("Периметр прямокутника: " + perimeter);
        // Діагональ прямокутника
        double diagonal = Math.sqrt( Math.pow(length, 2) + Math.pow(width, 2) );
        System.out.println("Діагональ прямокутника: " + diagonal);
    }
}