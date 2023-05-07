package redis

import (
	"context"
	"gRPC/internal/config"
	"github.com/go-redis/redis/v8"
)

// getRedisClient returns a Redis client.
func GetRedisClient(conf config.StorageConfig) *redis.Client {
	rdb := redis.NewClient(&redis.Options{
		Addr: conf.Addr,
		Password: conf.Password,
		DB: conf.DB,
	})
	err := rdb.Ping(context.Background()).Err()
	if err != nil {
		panic(err)
	}
	return rdb
}
