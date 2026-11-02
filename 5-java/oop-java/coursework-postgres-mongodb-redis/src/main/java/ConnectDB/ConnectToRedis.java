package ConnectDB;

import redis.clients.jedis.Jedis;

public class ConnectToRedis {
    Jedis jedis = new Jedis("http://localhost:6379/");
}
