package tests

import (
	"context"
	"gRPC/factorial"
	"gRPC/utils"
	"github.com/alicebob/miniredis/v2"
	"github.com/go-redis/redis/v8"
	"github.com/stretchr/testify/assert"
	"google.golang.org/grpc"
	"net"
	"testing"
)

func TestCalculateFactorial(t *testing.T) {
	// start a local Redis server for testing
	mr, err := miniredis.Run()
	if err != nil {
		t.Fatal(err)
	}
	defer mr.Close()

	// create Redis client and save test data
	rdb := redis.NewClient(&redis.Options{
		Addr: mr.Addr(),
	})

	defer rdb.Close()
	err = rdb.Set(context.Background(), "5", "120", 0).Err()
	if err != nil {
		t.Fatal(err)
	}

	// create gRPC server and register Factorial service
	srv := grpc.NewServer()
	server := &factorial.Server{RedisClient: rdb}
	utils.RegisterFactorialServer(srv, server)
	defer srv.Stop()

	// start gRPC server
	l, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatal(err)
	}
	defer l.Close()
	go srv.Serve(l)

	// create gRPC client
	conn, err := grpc.Dial(l.Addr().String(), grpc.WithInsecure())
	if err != nil {
		t.Fatal(err)
	}
	defer conn.Close()

	// create Factorial client
	client := utils.NewFactorialClient(conn)
	// test successful calculation
	req := &utils.FactorialRequest{Number: 4}
	res, err := client.CalculateFactorial(context.Background(), req)
	assert.NoError(t, err)
	assert.Equal(t, "24", res.Result)

	// test calculation from cache
	req = &utils.FactorialRequest{Number: 5}
	res, err = client.CalculateFactorial(context.Background(), req)
	assert.NoError(t, err)
	assert.Equal(t, "120", res.Result)

	// test error handling
	req = &utils.FactorialRequest{Number: -5}
	res, err = client.CalculateFactorial(context.Background(), req)
	assert.Equal(t, "1", res.Result)
}
