package org.example;

//  Створити застосунок для перегляду списку черговиків. Початкові записи в списку (5 записів)
//  створюються в програмному коді і є об'єктом класу LinkedList.
//  Запис списку є об'єктом QueuePerson, що містить поля прізвища, імені та по батькові
//  черговика (типу String), поле типу AddressValue для адреси черговика і пріоритет черговика (типу int).
//  У свою чергу, поле типу AddressValue містить три поля типу String: найменування міста,
//  найменування вулиці та номер будинку, а також поле типу int - номер квартири (якщо номер
//  квартири дорівнює 0, будинок, в якому проживає суб'єкт, не має квартир). Записи в черзі мають бути
//  упорядковані відповідно до пріоритету і черговик додається останнім в чергу свого пріоритету.
//  Забезпечити, щоб в черзі не було повторення по ПІБ черговика

import java.util.LinkedList;
import java.util.ListIterator;
import java.util.Scanner;
import java.util.TreeSet;

class AddressValue {
    String city;
    String street;
    int houseNumber;
    int apartmentNumber;

    public AddressValue(String city, String street, int houseNumber, int apartmentNumber) {
        this.city = city;
        this.street = street;
        this.houseNumber = houseNumber;

        if (apartmentNumber != 0) {
            this.apartmentNumber = apartmentNumber;
        } else {
            System.out.println("Номер квартири не може бути 0 (не має квартир)");
            this.apartmentNumber = 0;
        }
    }
}

class QueuePerson implements Comparable<QueuePerson> {
    String lastName;
    String firstName;
    String middleName;
    AddressValue address;
    int priority;

    public QueuePerson(String lastName, String firstName, String middleName, AddressValue address, int priority) {
        this.lastName = lastName;
        this.firstName = firstName;
        this.middleName = middleName;
        this.address = address;
        this.priority = priority;
    }

    @Override
    public int compareTo(QueuePerson o) {
        int result = Integer.compare(this.priority, o.priority);
        if (result == 0) {
            result = this.lastName.compareTo(o.lastName);
            if (result == 0) {
                result = this.firstName.compareTo(o.firstName);
                if (result == 0) {
                    result = this.middleName.compareTo(o.middleName);
                }
            }
        }
        return result;
    }

}
public class Ex2 {
    public static void main(String[] args) {
        LinkedList<QueuePerson> queueList = new LinkedList<>();
        TreeSet<QueuePerson> queueSet = new TreeSet<>();

        initializeQueue(queueList, queueSet);

        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("\n1. Список ");
            System.out.println("2. Додати черговика");
            System.out.println("3. Вихід");
            System.out.print("Оберіть цифру: ");

            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    displayQueueList(queueList);
                    break;
                case 2:
                    addQueuePerson(queueList, scanner);
                    break;
                case 3:
                    System.out.println("Вихід");
                    System.exit(0);
                default:
                    System.out.println("Введено некоректне значення");
            }
        }
    }

    public static void initializeQueue(LinkedList<QueuePerson> queueList, TreeSet<QueuePerson> queueSet) {
        queueSet.add(new QueuePerson("Іванов", "Іван", "Іванович", new AddressValue("Місто1", "Вулиця1", 1, 234), 3));
        queueSet.add(new QueuePerson("Петров", "Олесь", "Якович", new AddressValue("Місто2", "Вулиця2", 2, 202), 1));
        queueSet.add(new QueuePerson("Сидоров", "Максим", "Федорович", new AddressValue("Місто3", "Вулиця3", 3, 453), 2));
        queueSet.add(new QueuePerson("Іванов", "Марк", "Іванович", new AddressValue("Місто4", "Вулиця4", 4, 404), 4));
        queueSet.add(new QueuePerson("Міков", "Олександр", "Миронович", new AddressValue("Місто5", "Вулиця5", 5, 505), 5));
        queueList.addAll(queueSet);
    }

    public static void displayQueueList(LinkedList<QueuePerson> queueList) {
        System.out.println("\nСписок ");
        for (QueuePerson person : queueList) {
            System.out.println("Пріоритет: " + person.priority + ", Ім'я: " + person.lastName + " " +
                    person.firstName + " " + person.middleName +
                    ", Адреса: " + person.address.city + ", " + person.address.street + ", " +
                    person.address.houseNumber + ", " + person.address.apartmentNumber);
        }
    }
    public static boolean isPersonInQueue(LinkedList<QueuePerson> queueList, String lastName, String firstName, String middleName) {
        for (QueuePerson person : queueList) {
            if (person.lastName.equals(lastName) && person.firstName.equals(firstName) && person.middleName.equals(middleName)) {
                return true;
            }
        }
        return false;
    }
    static void addQueuePerson(LinkedList<QueuePerson> queueList, Scanner scanner) {
        System.out.println("Введіть дані для нового черговика:");
        System.out.print("Пріоритет: ");
        int priority = scanner.nextInt();
        scanner.nextLine();
        System.out.print("Прізвище: ");
        String lastName = scanner.nextLine();
        System.out.print("Ім'я: ");
        String firstName = scanner.nextLine();
        System.out.print("По батькові: ");
        String middleName = scanner.nextLine();

        // Перевірка наявності елемента в черзі
        if (isPersonInQueue(queueList, lastName, firstName, middleName)) {
            System.out.println("Такий елемент вже існує в черзі.");
            return;
        }

        System.out.print("Місто: ");
        String city = scanner.nextLine();
        System.out.print("Вулиця: ");
        String street = scanner.nextLine();
        System.out.print("Номер будинку: ");
        int houseNumber = scanner.nextInt();
        System.out.print("Номер квартири: ");
        int apartmentNumber = scanner.nextInt();

        if (apartmentNumber == 0) {
            System.out.println("Будинок, в якому проживає суб'єкт, не має квартир.");
            return;
        }
        AddressValue address = new AddressValue(city, street, houseNumber, apartmentNumber);
        QueuePerson newPerson = new QueuePerson(lastName, firstName, middleName, address, priority);
        ListIterator<QueuePerson> iterator = queueList.listIterator();
        while (iterator.hasNext()) {
            if (iterator.next().compareTo(newPerson) > 0) {
                iterator.previous();
                iterator.add(newPerson);
                System.out.println("Новий черговик доданий з пріоритетом " + priority);
                return;
            }
        }
        queueList.addLast(newPerson);
        System.out.println("Новий черговик доданий з пріоритетом " + priority);
    }
}
