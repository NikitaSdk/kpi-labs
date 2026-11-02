package org.example;

//Виведення фігур у графічному вікні. У вікні визначено рядок меню (MenuBar),
// в якому визначено два меню (Menu) – "Колір" та "Вивід". У меню "Колір"
// визначено два пункти меню "Зелений" і "Синій". У меню "Вивід" визначено
// три пункти меню (CheckBoxMenuItem): "Квадрат", "Коло", і "Трикутник". У панелі (Canvas)
// вікна виводиться в графічному контексті вибрана в меню "Вивід" фігура.
// При виборі пункту першого меню вся фігура забарвлюється заданим кольором.

import java.awt.*;
import java.awt.event.*;

public class Ex2 extends Frame {

    private final Canvas canvas;
    private final CheckboxMenuItem squareMenuItem;
    private final CheckboxMenuItem circleMenuItem;
    private final CheckboxMenuItem triangleMenuItem;
    private Color selectedColor = Color.BLACK;
    private String selectedFigure = null;

    public Ex2() {
        setTitle("Виведення фігур");
        setSize(400, 300);
        setLayout(new BorderLayout());

        // Створення рядка меню
        MenuBar bar = new MenuBar();
        setMenuBar(bar);

        // Меню "Колір"
        Menu c_menu = new Menu("Колір");
        MenuItem green_colour_menu = new MenuItem("Зелений");
        MenuItem blue_colour_menu = new MenuItem("Синій");

        green_colour_menu.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                selectedColor = Color.GREEN;
                drawSelectedFigure();
            }
        });
        blue_colour_menu.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                selectedColor = Color.BLUE;
                drawSelectedFigure();
            }
        });
        c_menu.add(green_colour_menu);
        c_menu.add(blue_colour_menu);

        Menu drawMenu = new Menu("Вивід");
        squareMenuItem = new CheckboxMenuItem("Квадрат");
        circleMenuItem = new CheckboxMenuItem("Коло");
        triangleMenuItem = new CheckboxMenuItem("Трикутник");

        squareMenuItem.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                if (squareMenuItem.getState()) {
                    selectedFigure = "Квадрат";
                    drawSelectedFigure();
                }
            }
        });

        circleMenuItem.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                if (circleMenuItem.getState()) {
                    selectedFigure = "Коло";
                    drawSelectedFigure();
                }
            }
        });

        triangleMenuItem.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                if (triangleMenuItem.getState()) {
                    selectedFigure = "Трикутник";
                    drawSelectedFigure();
                }
            }
        });

        drawMenu.add(squareMenuItem);
        drawMenu.add(circleMenuItem);
        drawMenu.add(triangleMenuItem);

        bar.add(c_menu);
        bar.add(drawMenu);

        // Панель для виведення фігур
        canvas = new Canvas();
        add(canvas, BorderLayout.CENTER);

        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent windowEvent) {
                System.exit(0);
            }
        });
    }
    private void drawSelectedFigure() {
        Graphics g = canvas.getGraphics();
        g.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());

        if (selectedFigure != null) {
            g.setColor(selectedColor);
            switch (selectedFigure) {
                case "Квадрат":
                    g.fillRect(100, 100, 200, 200);
                    break;
                case "Коло":
                    g.fillOval(100, 100, 200, 200);
                    break;
                case "Трикутник":
                    int[] xPoints = {100, 300, 200};
                    int[] yPoints = {300, 300, 100};
                    g.fillPolygon(xPoints, yPoints, 3);
                    break;
            }
        }
    }
    public static void main(String[] args) {
        Ex2 app = new Ex2();
        app.setVisible(true);
    }
}
