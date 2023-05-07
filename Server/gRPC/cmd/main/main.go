package main

import (
	"fmt"
	"gRPC/internal/config"
	"google.golang.org/grpc"
	"log"
	"net"
	"gRPC/factorial"
	clienRedis "gRPC/pkg/client/redis"
	"gRPC/utils"
)

func main() {
	cfg := config.GetConfig()
	redisClient := clienRedis.GetRedisClient(cfg.Storage)
	defer redisClient.Close()

	grpcServer := grpc.NewServer()
	server := &factorial.Server{RedisClient: redisClient}
	utils.RegisterFactorialServer(grpcServer, server)

	bindIP := cfg.Listen.BindIP
	bindPort := cfg.Listen.Port

	listen, err := net.Listen("tcp", fmt.Sprintf("%s:%s", bindIP, bindPort))
	if err != nil {
		log.Fatalf("could not listen to %s:%s: %v", bindIP, bindPort, err)
	}
	log.Printf("server starting and listen to %s:%s", bindIP, bindPort)
	log.Fatal(grpcServer.Serve(listen))
}
