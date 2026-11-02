package org.example;

//   Створити застосунок для перегляду списку книг і видалення книг в бібліотечному каталозі.
//   Початкові записи в списку (5 записів) є об'єктами класу HashMap, де ключем є індекс ISBN книги (типу Integer),
//   а значенням - об'єкт Book, що містить найменування книги, прізвище та ім'я учасника, видавництво (всі поля типу String),
//   рік видання (типу int) і ціну книги (типу double). Передбачити можливість сортування
//   книг по 2-3 полях, для чого використовувати ArrayList.

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;


class Book {
    String title, author, publisher;
    int publication_year;
    double price;

    public Book( String title, String author, String publisher, int public_year, double price) {
        this.title = title;
        this.author = author;
        this.publisher = publisher;
        this.publication_year = public_year;
        this.price = price;
    }

    @Override
    public String toString() {
        return "Назва книги: " + title + ", Автор: " + author + ", Видавництво: " + publisher + ", Рік видання: " + publication_year + ", Ціна: " + price;
    }
    public String getTitle() {
        return title;
    }
    public int getPublication_year() {
        return publication_year;
    }
    public double getPrice() {
        return price;
    }
}
public class Ex1 {

    public static void main(String[] args) {
        Map<Integer, Book> lib_catalog = new HashMap<>();
        initializeLibrary(lib_catalog);
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("\n1. Каталог книг");
            System.out.println("2. Сортування книг");
            System.out.println("3. Видалення книги");
            System.out.println("4. Додати книгу");
            System.out.println("5. Вихід");
            System.out.print("Оберіть цифру: ");

            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    displayLibraryCatalog(lib_catalog);
                    break;
                case 2:
                    sortLibraryCatalog(lib_catalog);
                    break;
                case 3:
                    Delete_b(lib_catalog, scanner);
                    break;
                case 4:
                    Add_book(lib_catalog, scanner);
                    break;
                case 5:
                    System.out.println("Вихід");
                    System.exit(0);
                default:
                    System.out.println("Введено некоректне значення");
            }
        }
    }

    public static void initializeLibrary(Map<Integer, Book > libraryCatalog) {
        libraryCatalog.put(1, new Book("Програмування Java", "Іван Петренко", "Видавництво УкрАБВ", 2020, 29.67));
        libraryCatalog.put(2, new Book("Структури БД", "Марія Коваленко", "Видавництво УкрXYZ", 2018, 40));
        libraryCatalog.put(3, new Book("Програмування Python", "Олег Іванов", "Видавництво Укр123", 2019, 24));
        libraryCatalog.put(4, new Book("Веб сайти", "Аліна Сидоренко", "Видавництво Укр456", 2021, 46.65));
        libraryCatalog.put(5, new Book("Вивчення штучного інтелекту", "Світлана Григоренко", "Видавництво Укр789", 2017, 54.89));
    }
    public static void displayLibraryCatalog(Map<Integer, Book > libraryCatalog) {
        System.out.println("\nБібліотечний каталог:");
        for (Map.Entry<Integer, Book > entry : libraryCatalog.entrySet()) {
            System.out.println("ISBN: " + entry.getKey() + ", " + entry.getValue());
        }
    }
    public static void sortLibraryCatalog(Map<Integer, Book > libraryCatalog) {
        List<Book > sorted_books = new ArrayList<>(libraryCatalog.values());
        System.out.println("\nСортування :");
        System.out.println("1. Відсортувати за назвою");
        System.out.println("2. Відсортувати за роком видання");
        System.out.println("3. Відсортувати за ціною");
        System.out.print("Оберіть сортування: ");

        Scanner scanner = new Scanner(System.in);
        int sortChoice = scanner.nextInt();

        switch (sortChoice) {
            case 1:
                sorted_books.sort(Comparator.comparing(Book ::getTitle));
                break;
            case 2:
                sorted_books.sort(Comparator.comparingInt(Book ::getPublication_year));
                break;
            case 3:
                sorted_books.sort(Comparator.comparingDouble(Book ::getPrice));
                break;
            default:
                System.out.println("Введено некоректне значення.");
                return;
        }

        System.out.println("\nВідсортований бібліотечний каталог:");
        for (org.example.Book  book : sorted_books) {
            System.out.println(book);
        }
    }
    public static void Delete_b(Map<Integer, Book > libraryCatalog, Scanner scanner) {
        System.out.print("Введіть ISBN книги, яку хочете видалити: ");
        int isbnToDelete = scanner.nextInt();
        if (libraryCatalog.containsKey(isbnToDelete)) {
            libraryCatalog.remove(isbnToDelete);
            System.out.println("Книга з ISBN " + isbnToDelete + " видалена.");
        }
        else {
            System.out.println("Книга з ISBN " + isbnToDelete + " відсутня в каталозі.");
        }
    }
    public static void Add_book(Map<Integer, Book> libraryCatalog, Scanner scanner) {
        System.out.println("Введіть дані для нової книги:");
        System.out.print("Назва: ");
        String title = scanner.nextLine();
        System.out.print("Автор: ");
        String author = scanner.nextLine();
        System.out.print("Видавництво: ");
        String publisher = scanner.nextLine();
        System.out.print("Рік видання: ");
        int year = scanner.nextInt();
        System.out.print("Ціна: ");
        double price = scanner.nextDouble();
        int newISBN = libraryCatalog.size() + 1;

        Book newBook = new Book(title, author, publisher, year, price);
        libraryCatalog.put(newISBN, newBook);

        System.out.println("Нова книга додана з ISBN " + newISBN);
    }
}
