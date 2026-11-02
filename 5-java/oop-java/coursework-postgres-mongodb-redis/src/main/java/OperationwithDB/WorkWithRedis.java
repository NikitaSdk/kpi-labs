package OperationwithDB;

import ConnectDB.ConnectToPostgreSql;
import ConnectDB.ConnectToRedis;
import redis.clients.jedis.Jedis;


public class WorkWithRedis {
    public static void addStudentLog(String day) {
        Jedis jedis = new Jedis("http://localhost:6379/");
        System.out.println("Server is running: " + jedis.ping());

        // Set a key-value pair

        jedis.set(day, "addedStudent1");
        jedis.append(day, " deletedStudent1");

        // Get the value for a key
        String value = jedis.get(day);
        System.out.println("Value for key 'day': " + value);
    }
}
