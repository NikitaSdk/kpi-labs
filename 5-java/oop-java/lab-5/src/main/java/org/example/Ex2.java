package org.example;

// Побудувати програму для роботи з класом Час.
// Програма повинна забезпечувати функції збільшення/зменшення на 1 годину,
// хвилину, секунду, введення/виведення значень.
import java.util.Scanner;

class Time {
    private int hours, minutes, seconds;

    public Time(int hours, int minutes, int seconds) {
        this.hours = hours;
        this.minutes = minutes;
        this.seconds = seconds;
    }

    public void showTime() {
        System.out.printf("%02d:%02d:%02d\n", hours, minutes, seconds);
    }

    public void changeTime(int option, int changeType) {
        switch (option) {
            case 1:
                changeHours(changeType);
                break;
            case 2:
                changeMinutes(changeType);
                break;
            case 3:
                changeSeconds(changeType);
                break;
            default:
                System.out.println("Неправильний вибір опції.");
        }
    }

    private void changeHours(int changeType) {
        if (changeType == 1) {
            hours = (hours + 1) % 24;
        } else if (changeType == 2) {
            hours = (hours - 1 + 24) % 24;
        }
    }

    private void changeMinutes(int changeType) {
        if (changeType == 1) {
            minutes = (minutes + 1) % 60;
            if (minutes == 0) {
                changeHours(1);
            }
        } else if (changeType == 2) {
            minutes = (minutes - 1 + 60) % 60;
            if (minutes == 59) {
                changeHours(2);
            }
        }
    }

    private void changeSeconds(int changeType) {
        if (changeType == 1) {
            seconds = (seconds + 1) % 60;
            if (seconds == 0) {
                changeMinutes(1);
            }
        } else if (changeType == 2) {
            seconds = (seconds - 1 + 60) % 60;
            if (seconds == 59) {
                changeMinutes(2);
            }
        }
    }
}

public class Ex2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int hours, minutes, seconds;

        System.out.println("Введіть години (0-23):");
        hours = scanner.nextInt();
        while (hours < 0 || hours > 23) {
            System.out.println("Неправильне значення. Введіть години знову (0-23):");
            hours = scanner.nextInt();
        }

        System.out.println("Введіть хвилини (0-59):");
        minutes = scanner.nextInt();
        while (minutes < 0 || minutes > 59) {
            System.out.println("Неправильне значення. Введіть хвилини знову (0-59):");
            minutes = scanner.nextInt();
        }

        System.out.println("Введіть секунди (0-59):");
        seconds = scanner.nextInt();
        while (seconds < 0 || seconds > 59) {
            System.out.println("Неправильне значення. Введіть секунди знову (0-59):");
            seconds = scanner.nextInt();
        }

        Time time = new Time(hours, minutes, seconds);
        System.out.println("\nВаш час:");
        time.showTime();

        int option;
        int changeType;

        do {
            System.out.println("\nМеню:");
            System.out.println("1 - Змінити години");
            System.out.println("2 - Змінити хвилини");
            System.out.println("3 - Змінити секунди");
            System.out.println("0 - Завершити");
            option = scanner.nextInt();

            if (option != 0) {
                System.out.println("Виберіть дію:");
                System.out.println("1 - Збільшити");
                System.out.println("2 - Зменшити");
                changeType = scanner.nextInt();

                time.changeTime(option, changeType);

                System.out.println("\nОновлений час:");
                time.showTime();
            }
        } while (option != 0);
        scanner.close();
    }
}