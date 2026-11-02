package org.example;

// 22. Зміна написи у графічному вікні. У центрі верхньої панелі (Canvas) "Виведення напису"
// у графічному контексті виводиться довільний напис. У нижній панелі (Panel) "Параметри напису"
// задаються такі компоненти: напис (Label) "Текст:", текстове поле (TextField), напис (Label) "Колір:",
// чотири радіокнопки (Checkbox) зі значеннями: "Чорний" (колір за замовчуванням), "Червоний",
// "Зелений" і "Синій", напис (Label) "Розмір:", три радіокнопки (Checkbox) зі значеннями: "10pt",
// "12pt" (розмір за замовчуванням) і "14pt ", напис (Label) "Координата X:", текстове поле (TextField),
// напис (Label) "Координата Y:", текстове поле (TextField), а також кнопка (Button) "Вивести рядок".
// Спочатку в текстових полях "Координата X:" та "Координата Y:" встановлюються координати початку
// базової лінії напису (текстові поля задані як нередаговані). Під час введення даних напис змінює
// текст, колір та/або розмір. При натисканні мишею в області верхньої панелі в текстових полях
// виводяться координати точки натискання і напис перемальовується в цій точці.



import java.awt.*;
import java.awt.event.*;

public class Ex4 extends Frame {

    private final Canvas canvas;
    private final TextField input_txt;
    private final CheckboxGroup color_checkbox;
    private final CheckboxGroup size_checkbox;
    private final TextField x_input;
    private final TextField y_input;

    private String text = "Hi Bob!";
    private Color selectedColor = Color.BLACK;
    private int chosen_size = 12;
    private int textX = 150;
    private int textY = 100;

    public Ex4() {
        setTitle("Зміна напису");
        setSize(400, 300);
        setLayout(new BorderLayout());

        canvas = new Canvas();
        canvas.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                Show_coord(e.getX(), e.getY());
            }
        });
        add(canvas, BorderLayout.CENTER);

        Panel controlPanel = new Panel();
        controlPanel.setLayout(new FlowLayout());

        Label text_label = new Label("Текст:");
        input_txt = new TextField(text, 20);
        input_txt.setEditable(true);
        Label label_colour = new Label("Колір:");
        color_checkbox = new CheckboxGroup();
        Create_colour_checkbox(controlPanel);
        Label label_ssize = new Label("Розмір:");
        size_checkbox = new CheckboxGroup();
        Create_size_checkbox(controlPanel);
        Label coord_x = new Label("Координата X:");
        x_input = new TextField(String.valueOf(textX), 4);
        Label coord_y = new Label("Координата Y:");
        y_input = new TextField(String.valueOf(textY), 4);
        Button drawButton = new Button("Вивести напис");

        drawButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                Update_txt_stat();
                Draw();
            }
        });
        controlPanel.add(text_label);
        controlPanel.add(input_txt);
        controlPanel.add(label_colour);
        Create_colour_checkbox(controlPanel);
        controlPanel.add(label_ssize);
        Create_size_checkbox(controlPanel);
        controlPanel.add(coord_x);
        controlPanel.add(x_input);
        controlPanel.add(coord_y);
        controlPanel.add(y_input);
        controlPanel.add(drawButton);

        add(controlPanel, BorderLayout.SOUTH);
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent windowEvent) {
                System.exit(0);
            }
        });
    }
    private Checkbox Create_checkbox(String label, boolean initialState, CheckboxGroup group) {
        Checkbox checkbox = new Checkbox(label, group, initialState);
        checkbox.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                Update_txt_stat();
                Draw();
            }
        });
        return checkbox;
    }
    private void Create_colour_checkbox(Panel panel) {
        Add_ifnotexists(panel, "Чорний", true, color_checkbox);
        Add_ifnotexists(panel, "Червоний", false, color_checkbox);
        Add_ifnotexists(panel, "Зелений", false, color_checkbox);
        Add_ifnotexists(panel, "Синій", false, color_checkbox);
    }
    private void Create_size_checkbox(Panel panel) {
        Add_ifnotexists(panel, "10pt", false, size_checkbox);
        Add_ifnotexists(panel, "12pt", true, size_checkbox);
        Add_ifnotexists(panel, "14pt", false, size_checkbox);
    }
    private void Add_ifnotexists(Panel panel, String label, boolean initialState, CheckboxGroup group) {
        Checkbox existingCheckbox = Find_bylabel(panel, label);
        if (existingCheckbox == null) {
            panel.add(Create_checkbox(label, initialState, group));
        }
    }
    private Checkbox Find_bylabel(Panel panel, String label) {
        for (Component component : panel.getComponents()) {
            if (component instanceof Checkbox && ((Checkbox) component).getLabel().equals(label)) {
                return (Checkbox) component;
            }
        }
        return null;
    }
    private void Update_txt_stat() {
        text = input_txt.getText();
        selectedColor = Get_colour();
        chosen_size = Get_size();
        textX = Integer.parseInt(x_input.getText());
        textY = Integer.parseInt(y_input.getText());
    }
    private Color Get_colour() {
        Checkbox selectedCheckbox = color_checkbox.getSelectedCheckbox();
        if (selectedCheckbox != null) {
            switch (selectedCheckbox.getLabel()) {
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
        return Color.BLACK;
    }
    private int Get_size() {
        Checkbox selectedCheckbox = size_checkbox.getSelectedCheckbox();
        if (selectedCheckbox != null) {
            switch (selectedCheckbox.getLabel()) {
                case "10pt":
                    return 10;
                case "14pt":
                    return 14;
                default:
                    return 12;
            }
        }
        return 12;
    }
    private void Draw() {
        Graphics g = canvas.getGraphics();
        g.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
        g.setColor(selectedColor);
        g.setFont(new Font("Arial", Font.PLAIN, chosen_size));
        g.drawString(text, textX, textY);
    }
    private void Show_coord(int x, int y) {
        x_input.setText(String.valueOf(x));
        y_input.setText(String.valueOf(y));
    }

    public static void main(String[] args) {
        Ex4 app = new Ex4();
        app.setVisible(true);
    }
}
