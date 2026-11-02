package ConnectDB;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnectToPostgreSql {
     private static final String JDBC_URL="jdbc:postgresql://localhost:5432/students";
    private static final String USERNAME="postgres";
     private static final String PASSWORD="postgres";
//     public ConnectToPostgreSql()
//     {
//          jdbcUrl="jdbc:postgresql://localhost:5432/students";
//          username="postgres";
//          password="postgres";
//     }
     public static Connection connect()throws SQLException{
         try{
             Class.forName("org.postgresql.Driver");
             return DriverManager.getConnection(JDBC_URL,USERNAME,PASSWORD);
         }
         catch (ClassNotFoundException e) {
             throw new SQLException("PostgreSQL JDBC Driver not found", e);
         }
     }

//     public static void ConnectToDB()
//     {
//         String jdbcUrl="jdbc:postgresql://localhost:5432/students";
//         String username = "postgres";
//         String password = "postgres";
//          try(Connection connection = DriverManager.getConnection(jdbcUrl,username,password))
//          {
//               System.out.println("Connected to the database!");
//          }
//          catch (SQLException e)
//          {
//               e.printStackTrace();
//          }
//     }
}
