package factorial

import (
	"context"
	"gRPC/utils"
	"github.com/go-redis/redis/v8"
	"log"
)

// Server is the implementation of the proto interface.
type Server struct {
	RedisClient *redis.Client
}

// getFactorialFromCache gets the utils of a given integer from Redis cache.
func (s *Server) getFactorialFromCache(n string) (string, error) {
	result, err := s.RedisClient.Get(context.Background(), n).Bytes()
	if err == redis.Nil {
		return "", err
	}
	if err != nil {
		return "", err
	}
	return string(result), nil
}

// saveFactorialToCache saves the utils of a given integer to Redis cache.
func (s *Server) saveFactorialToCache(n string, result string) error {
	err := s.RedisClient.Set(context.Background(), n, result, -1).Err()
	if err != nil {
		return err
	}
	return nil
}

// CalculateFactorial calculates the utils of a given integer.
func (s *Server) CalculateFactorial(ctx context.Context, req *utils.FactorialRequest) (*utils.FactorialResponse, error) {
	log.Printf("Calculating utils for number %d", req.Number)

	result, err := s.getFactorialFromCache(req.String())
	if err != nil {
		log.Printf("Error getting utils from cache: %v", err)
		resultValue := utils.CalculateFactorial(req.Number)
		result = resultValue.String()

		err = s.saveFactorialToCache(req.String(), result)
		if err != nil {
			log.Printf("Error saving utils to cache: %v", err)
		}
	}
	return &utils.FactorialResponse{Result: result}, nil
}
