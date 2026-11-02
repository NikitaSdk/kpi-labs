// Code extracted from the lab report (report.pdf)

// ---- fragment 1 ----
package org.example;

public class Food {
    public String name;
    public int calories;

    public Food(String name, int calories) {
        if (calories < 0) {

// ---- fragment 2 ----
            this.calories = 0;
        }
else {
            this.name = name;
            this.calories = calories;
        }
    }

    public int getCalories() {
        return calories;
    }

    public String getName() {
        return name;
    }

    public void increaseCalories(int extra) {
        calories += extra;
    }
}

// ---- fragment 3 ----
package org.example;

public class Exercise {
    public String name;
    public int caloriesBurned;

    public Exercise(String name, int caloriesBurned) {
        if (caloriesBurned < 0) {

// ---- fragment 4 ----
            this.caloriesBurned = 0;
        } else {
            this.name = name;
            this.caloriesBurned = caloriesBurned;
        }
    }

    public int getCaloriesBurned() {
        return caloriesBurned;
    }

    public String getName() {
        return name;
    }

    public void decreaseCaloriesBurned(int amount) {
        caloriesBurned -= amount;
    }
}

// ---- fragment 5 ----
package org.example;
public class Food {
    private String name;
    private int calories;
    public Food(String name, int calories) {
        this.name = name;
        this.calories = Math.max(calories, 0);
    }
    public String getName() {
        return name;
    }
    public int getCalories() {
        return calories;
    }
}

// ---- fragment 6 ----
package org.example;

public class Exercise {
    private String name;
    private int caloriesBurned;

    public Exercise(String name, int caloriesBurned) {
        this.name = name;
        this.caloriesBurned = Math.max(caloriesBurned, 0);
    }

    public String getName() {
        return name;
    }

    public int getCaloriesBurned() {
        return caloriesBurned;
  }
}

// ---- more fragments ----
// ---- fragment 1 ----
package org.example;
import java.util.ArrayList;
import java.util.List;
public class Calculate {
    public List<Food> foods = new ArrayList<>();
    public List<Exercise> exercises = new ArrayList<>();

    public void addFood(Food food) {
        foods.add(food);
    }
    public void addExercise(Exercise exercise) {
        exercises.add(exercise);
    }
    public int getTotalCalories() {
        int total = 0;
        for (Food food : foods) {
            total += food.calories;
        }
        return total;
    }
    public int getTotalBurnedCalories() {
        int totalBurned = 0;
        for (Exercise exercise : exercises) {
            totalBurned += exercise.caloriesBurned;
        }
        return totalBurned;
    }
    public int calculateNetCalories() {
        int totalCalories = getTotalCalories();
        int totalBurned = getTotalBurnedCalories();
        return totalCalories – totalBurned;
    }
}

// ---- fragment 2 ----
package org.example;

import java.util.ArrayList;
import java.util.List;

public class Calculate {
    private List<Food> foods = new ArrayList<>();
    private List<Exercise> exercises = new ArrayList<>();

    public void addFood(Food food) {
        foods.add(food);
    }

    public void addExercise(Exercise exercise) {
        exercises.add(exercise);
    }

    public int getTotalCalories() {
        return foods.stream().mapToInt(Food::getCalories).sum();
    }

    public int getTotalBurnedCalories() {
        return exercises.stream().mapToInt(Exercise::getCaloriesBurned).sum();
    }

    public int calculateNetCalories() {
        int netCalories = getTotalCalories() - getTotalBurnedCalories();
        return Math.max(netCalories, 0);
    }
}
