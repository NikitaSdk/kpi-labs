package org.example;

//   Аналіз типів аргументів, що задаються під час запуску програми.
//   Якщо аргумент є правильним ідентифікатором Java
//   (шаблон: складається з латинських букв, цифр і символів "$" і "_",
//   що вважаються буквами, і, крім  того, перший символ є літерою), то його тип
//   "Identifier", якщо аргумент є ключовим словом Java (для прикладу задати кілька
//   ключових слів Java, "if", "for", "while", "do" і "else"), то його тип "Keyword",
//   інакше його тип вважається "Illegal". Програма виводить кількість заданих аргументів
//   і для кожного аргументу його тип і значення.

public class Ex3 {
    public static void main(String[] args) {
        System.out.println("Кількість аргументів: " + args.length);
        for (String arg : args) {
            String type = analyzeArgumentType(arg);
            System.out.println("Тип: " + type + ", Значення: " + arg);
        }
    }
    public static String analyzeArgumentType(String arg) {
        if (isJavaKeyword(arg)) {
            return "Keyword";
        }
        else if (isJavaIdentifier(arg)) {
            return "Identifier";
        }
        else {
            return "Illegal";
        }
    }
    public static boolean isJavaIdentifier(String str) {
        if (Character.isDigit(str.charAt(0))) {
            return false;
        }
        for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);
            if (!Character.isLetter(ch) && !Character.isDigit(ch) && ch != '$' && ch != '_' && (i != 0 || !Character.isLetter(ch))) {
                return false;
            }
        }
        return true;
    }
    public static boolean isJavaKeyword(String str) {
        String[] keywords = {"if", "for", "while", "do", "else"};
        for (String keyword : keywords) {
            if (str.equals(keyword)) {
                return true;
            }
        }
        return false;
    }
}



