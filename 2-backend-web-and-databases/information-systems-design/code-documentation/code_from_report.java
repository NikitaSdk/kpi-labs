// Code extracted from the lab report (report.pdf)

// ---- fragment 1 ----
public class Food {
    private String name;
    private int calories;

// ---- fragment 2 ----
    public Food(String name, int calories) {
        this.name = name;
        this.calories = calories;
    }

// ---- fragment 3 ----
    public String getName() {
        return name;
    }

// ---- fragment 4 ----
    public int getCalories() {
        return calories;
    }
}

// ---- fragment 5 ----
public class Exercise {
    private String name;
    private int caloriesBurned;

// ---- fragment 6 ----
    public Exercise(String name, int caloriesBurned) {
        this.name = name;
        this.caloriesBurned = caloriesBurned;
    }

// ---- fragment 7 ----
    public String getName() {
        return name;
    }

// ---- fragment 8 ----
    public int getCaloriesBurned() {
        return caloriesBurned;
    }
}

// ---- fragment 9 ----
public class Calculate {
    private int totalIntake;
    private int totalBurned;

// ---- fragment 10 ----
    public void addFood(Food food) {
        totalIntake += food.getCalories();
    }

// ---- fragment 11 ----
    public void addExercise(Exercise exercise) {
        totalBurned += exercise.getCaloriesBurned();
    }

// ---- fragment 12 ----
    public int getNetCalories() {
        return totalIntake - totalBurned;
    }

// ---- fragment 13 ----
    public static void main(String[] args) {
        Food apple = new Food("Apple", 95);
        Exercise running = new Exercise("Running", 200);

        Calculate calculator = new Calculate();
        calculator.addFood(apple);
        calculator.addExercise(running);

        System.out.println("Net calories: " + calculator.getNetCalories());
    }
}
