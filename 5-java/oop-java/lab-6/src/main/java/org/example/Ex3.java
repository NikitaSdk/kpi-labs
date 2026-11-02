package org.example;
import java.awt.*;
import java.awt.event.*;

// Переміщення фігур у графічному вікні. У центрі верхньої панелі (Canvas) "Виведення зображення"
// у графічному контексті задається прямокутник. У нижній панелі (Panel) "Переміщення зображення"
// задаються наступні компоненти: напис (Label) "Колір:", список, що розгортається (Choice)
// зі значеннями "Чорний" (за замовчуванням), "Червоний", "Зелений" і "Синій", а також чотири
// перемикачі (CheckboxGroup): "Вліво", "Вгору" "Вправо" і "Вниз"
// та кнопка (Button) "Перемістити". При виборі кольору прямокутник
// перемальовується заданим кольором, а при натисканні однієї з чотирьох
// радіокнопок зображення стрибкоподібно (на 10 пікселів) переміщується у цьому напрямку.




public class Ex3 extends Frame {

    private final Canvas canvas;
    private final Choice col_choice;
    private final CheckboxGroup dir_checkbox;
    private Color my_colour = Color.BLACK;
    private int rect_X = 150;
    private int rect_Y = 100;
    private static final int RECTANGLE_WIDTH = 100;
    private static final int RECTANGLE_HEIGHT = 50;
    private static final int MOVE_DISTANCE = 10;

    public Ex3() {
        setTitle("Переміщення зображення");
        setSize(400, 300);
        setLayout(new BorderLayout());

        canvas = new Canvas();
        add(canvas, BorderLayout.CENTER);

        Panel c_panel = new Panel();
        c_panel.setLayout(new FlowLayout());

        Label colorLabel = new Label("Колір:");
        col_choice = new Choice();
        col_choice.add("Чорний");
        col_choice.add("Червоний");
        col_choice.add("Зелений");
        col_choice.add("Синій");

        col_choice.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                my_colour = getColorByName(col_choice.getSelectedItem());
                drawRectangle();
            }
        });

        dir_checkbox = new CheckboxGroup();
        Checkbox left_box = new Checkbox("Вліво", dir_checkbox, false);
        Checkbox right_box = new Checkbox("Вправо", dir_checkbox, false);
        Checkbox up_box = new Checkbox("Вгору", dir_checkbox, false);
        Checkbox down_box = new Checkbox("Вниз", dir_checkbox, false);

        Button button_move = new Button("Перемістити");
        button_move.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                moveRectangle();
            }
        });

        c_panel.add(colorLabel);
        c_panel.add(col_choice);
        c_panel.add(left_box);
        c_panel.add(up_box);
        c_panel.add(right_box);
        c_panel.add(down_box);
        c_panel.add(button_move);
        add(c_panel, BorderLayout.SOUTH);
        drawRectangle();

        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent windowEvent) {
                System.exit(0);
            }
        });
    }

    private void drawRectangle() {
        Graphics g = canvas.getGraphics();
        if (g != null) {
            g.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
            g.setColor(my_colour);
            g.fillRect(rect_X, rect_Y, RECTANGLE_WIDTH, RECTANGLE_HEIGHT);
        }
    }

    private void moveRectangle() {
        Checkbox selectedCheckbox = dir_checkbox.getSelectedCheckbox();
        if (selectedCheckbox != null) {
            switch (selectedCheckbox.getLabel()) {
                case "Вліво":
                    rect_X -= MOVE_DISTANCE;
                    break;
                case "Вгору":
                    rect_Y -= MOVE_DISTANCE;
                    break;
                case "Вправо":
                    rect_X += MOVE_DISTANCE;
                    break;
                case "Вниз":
                    rect_Y += MOVE_DISTANCE;
                    break;
            }
            drawRectangle();
        }
    }

    private Color getColorByName(String colorName) {
        switch (colorName) {
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

    public static void main(String[] args) {
        Ex3 app = new Ex3();
        app.setVisible(true);
    }
}
