package org.example;

//  Створити застосунок для перегляду списку книг в магазинному каталозі і зміни ціни книги.
//  Початкові записи в списку книг (5 записів) створюються в програмному коді і є об'єктом класу HashMap.
//  Ключем записи є індекс ISBN книги (типу Integer), а значенням - що містить найменування книги, прізвище,
//  ім'я та по батькові (ПІБ) учасника, видавництво (всі записи типу String),
//  рік видання (типу int) і ціну книги (типу float).
//  Передбачити можливість сортування книг по видавництву або ціною, використовуючи ArrayList.

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
class books {
    private String title, author, publisher;
    private int year;
    private float price;

    public books(String title, String author, String publisher, int year, float price) {
        this.title = title;
        this.author = author;
        this.publisher = publisher;
        this.year = year;
        this.price = price;
    }

    @Override
    public String toString() {
        return "Назва: " + title + ", Автор: " + author + ", Видавець: " + publisher
                + ", Рік: " + year + ", Ціна: " + price;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public String getPublisher() {
        return publisher;
    }

    public int getYear() {
        return year;
    }

    public float getPrice() {
        return price;
    }

    public void setPrice(float price) {
        this.price = price;
    }
}

public class Ex3 {
    public static void main(String[] args) {

        Map<Integer, books> bookCatalog = new HashMap<>();
        bookCatalog.put(1, new books("Долина нарцисів", "Олена Петренко", "Українське видавництво", 2022, 40.0f));
        bookCatalog.put(2, new books("Місяць над Дніпром", "Іван Франко", "Літературне бюро", 1905, 28.0f));
        bookCatalog.put(3, new books("Земля козаків", "Сергій Жадан", "Грані-Т", 2017, 22.50f));
        bookCatalog.put(4, new books("Кобзар", "Тарас Шевченко", "Українське видавництво", 1840, 18.0f));

        List<books> booksList = new ArrayList<>(bookCatalog.values());

        Scanner scanner = new Scanner(System.in);
        int choice;
        do {
            System.out.println("1. Каталог книг");
            System.out.println("2. Зміна ціни книги");
            System.out.println("3. Сортування за видавництвом");
            System.out.println("4. Сортування за ціною");
            System.out.println("0. Вихід");
            System.out.print("Оберіть опцію: ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    displayBookCatalog(bookCatalog);
                    break;
                case 2:
                    changeBookPrice(scanner, bookCatalog);
                    break;
                case 3:
                    SortByPublisher(booksList);
                    break;
                case 4:
                    SortByPrice(booksList);
                    break;
                case 0:
                    System.out.println("Вихід");
                    break;
                default:
                    System.out.println("Невірний вибір. Спробуйте ще раз.");
            }
        } while (choice != 0);
    }

    public static void displayBooks(List<books> booksList) {
        for (books book : booksList) {
            System.out.println(book);
        }
    }

    public static void changeBookPrice(Scanner scanner, Map<Integer, books> bookCatalog) {
        System.out.print("Введіть ISBN книги для зміни ціни: ");
        int isbn = scanner.nextInt();
        if (bookCatalog.containsKey(isbn)) {
            System.out.print("Введіть нову ціну книги: ");
            float newPrice = scanner.nextFloat();
            books book = bookCatalog.get(isbn);
            book.setPrice(newPrice);  // Встановлюємо нову ціну, не створюючи новий об'єкт
            System.out.println("Ціну книги змінено.");
        } else {
            System.out.println("Книга не знайдена.");
        }
    }

    public static void SortByPublisher(List<books> booksList) {
        Collections.sort(booksList, (book1, book2) -> book1.getPublisher().compareTo(book2.getPublisher()));
        System.out.println("книги відсортовані за видавництвом:");
        displayBooks(booksList);
    }

    public static void SortByPrice(List<books> booksList) {
        Collections.sort(booksList, (book1, book2) -> Float.compare(book1.getPrice(), book2.getPrice()));
        System.out.println("книги відсортовані за ціною:");
        displayBooks(booksList);
    }

    public static void displayBookCatalog(Map<Integer, books> bookCatalog) {
        System.out.println("\nКаталог книг:");
        for (Map.Entry<Integer, books> entry : bookCatalog.entrySet()) {
            System.out.println("ISBN: " + entry.getKey() + ", " + entry.getValue());
        }
    }
}