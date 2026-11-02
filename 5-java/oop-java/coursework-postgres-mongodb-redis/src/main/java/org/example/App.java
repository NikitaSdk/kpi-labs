package org.example;

import ConnectDB.ConnectToPostgreSql;
import OperationwithDB.WorkWithPostgreSql;
import data.Student;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

import static ConnectDB.ConnectToPostgreSql.connect;

public class App{
    public static void main(String[] args) {
          try{
              Connection connection=ConnectToPostgreSql.connect();
              System.out.println("Opened database successfully");
              connection.close();

              WorkWithPostgreSql.createGroupsTable();
              WorkWithPostgreSql.createStudentsTable();
              //WorkWithPostgreSql.insertGroup("Da-11");
              WorkWithPostgreSql.insertGroup("Da-11");
              Student student=new Student();
              student.setFullName("Max pal");
              student.setGroup_id(1);
              WorkWithPostgreSql.insertStudent(student);
              //WorkWithPostgreSql.tester();
          } catch (SQLException e) {
              System.err.println(e.getClass().getName() + ": " + e.getMessage());
              System.exit(0);
          }


    }

    public static void menu()
    {
        System.out.println("Меню");
        System.out.println("Натисніть -1,якщо ви хочете створити таблицю");
        System.out.println("Натисніть -2,якщо ви хочете вставити ");
    }






    }

