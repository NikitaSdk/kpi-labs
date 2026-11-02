// Code extracted from the lab report (report.pdf)

// ---- fragment 1 ----
package org.example;

public class Food {
    private String name;
    private int calories;

    public Food(String name, int calories) {
        if (calories < 0) {

// ---- fragment 2 ----
        }
        this.name = name;
        this.calories = calories;
    }

    public String getName() {
        return name;
    }

    public int getCalories() {
        return calories;
    }
}

// ---- fragment 3 ----
package org.example;

public class Exercise {
    private String name;
    private int caloriesBurned;

    public Exercise(String name, int caloriesBurned) {
        if (caloriesBurned < 0) {

// ---- fragment 4 ----
        }
        this.name = name;
        this.caloriesBurned = caloriesBurned;
    }

    public String getName() {
        return name;
    }

    public int getCaloriesBurned() {
        return caloriesBurned;
    }
}

// ---- fragment 5 ----
package org.example;

public class CalculateCalories {

    public int calculateNetCalories(Food food, Exercise exercise) {
        int netCalories = food.getCalories() - exercise.getCaloriesBurned();

// ---- more fragments ----
// ---- fragment 1 ----
package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FoodTest {

    @Test
    void testAddFood() {
        Food apple = new Food("Apple", 52);

// ---- fragment 2 ----
package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ExerciseTest {

    @Test
    void testAddExercise() {
        Exercise running = new Exercise("Running", 300);

// ---- fragment 3 ----
package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculateTest {

    @Test
    void testCalculateTotalCalories() {
        Food apple = new Food("Apple", 52);
        Exercise running = new Exercise("Running", 300);
        CalculateCalories calculator = new CalculateCalories();

        int netCalories = calculator.calculateNetCalories(apple, running);
