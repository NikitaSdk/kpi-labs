package org.example;

//Виведення рядка заданим шрифтом та заданого кольору у графічному вікні.
// У верхній панелі (Panel) "Керування виводом" задається напис (Label) "Текст:"
// та текстове поле (TextField), напис (Label) "Гарнітура:", список що розгортається (Choice)
// зі значеннями "Times New Roman" (шрифт по за замовчуванням), "Arial" і "Verdana", напис (Label)
// "Колір:" і список що розгортається (Choice) зі значеннями "Чорний" (за замовчуванням), "Червоний",
// "Зелений" і "Синій", а також кнопка (Button) "Вивести рядок". У нижній панелі (Canvas) "Виведення рядка"
// виводиться у графічному контексті у довільному місці порожній рядок. При заданні у верхній панелі
// тексту в текстовому полі, параметрів у списках, що розгортаються  і натисканні кнопки "Виведення рядка"
// рядок заданого вмісту і кольору виводиться заданим шрифтом у нижній панелі.

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.font.TextAttribute;
import java.text.AttributedString;

public class Ex1 extends Frame {
    private final Choice fontChoice;
    private final Choice colorChoice;
    private final TextField textField;
    private final Canvas canvas;
    public Ex1() {
        setTitle("Виведення рядка");
        setSize(400, 300);
        setLayout(new BorderLayout());

        Panel c_panel = new Panel();
        c_panel.setLayout(new FlowLayout());

        Label text = new Label("Текст:");
        textField = new TextField(15);
        Label font = new Label("Гарнітура:");
        fontChoice = new Choice();
        fontChoice.add("Times New Roman");
        fontChoice.add("Arial");
        fontChoice.add("Verdana");
        Label color = new Label("Колір:");
        colorChoice = new Choice();
        colorChoice.add("Чорний");
        colorChoice.add("Червоний");
        colorChoice.add("Зелений");
        colorChoice.add("Синій");
        Button drawButton = new Button("Вивести рядок");

        drawButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                draw_str();
            }
        });

        c_panel.add(text);
        c_panel.add(textField);
        c_panel.add(font);
        c_panel.add(fontChoice);
        c_panel.add(color);
        c_panel.add(colorChoice);
        c_panel.add(drawButton);

        add(c_panel, BorderLayout.NORTH);

        canvas = new Canvas();
        add(canvas, BorderLayout.CENTER);

        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                System.exit(0);
            }
        });
    }

    private void draw_str() {
        Graphics grph = canvas.getGraphics();
        grph.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());

        String text = textField.getText();
        String selectedFont = fontChoice.getSelectedItem();
        int fontSize = 20;
        int fontStyle = Font.PLAIN;

        Font font = new Font(selectedFont, fontStyle, fontSize);

        String my_color = colorChoice.getSelectedItem();
        Color color = get_colour(my_color);

        grph.setFont(font);
        grph.setColor(color);

        FontMetrics fm = grph.getFontMetrics();
        int x = (canvas.getWidth() - fm.stringWidth(text)) / 2;
        int y = (canvas.getHeight() - fm.getHeight()) / 2 + fm.getAscent();

        AttributedString as = new AttributedString(text);
        as.addAttribute(TextAttribute.FONT, font);
        as.addAttribute(TextAttribute.FOREGROUND, color);
        grph.drawString(as.getIterator(), x, y);
    }

    private Color get_colour(String color_name) {
        switch (color_name) {
            case "Чорний":
                return Color.BLACK;
            case "Червоний":
                return Color.RED;
            case "Зелений":
                return Color.GREEN;
            case "Синій":
                return Color.BLUE;
            default:
                return Color.BLACK;
        }
    }
    public static void Ex1 () {
        Ex1 app = new Ex1();
        app.setVisible(true);
    }
    public static void main(String[] args) {
        Ex1 app = new Ex1();
        app.setVisible(true);
    }
}
