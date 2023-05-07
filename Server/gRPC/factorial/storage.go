package factorial

import (
	"context"
	"gRPC/utils"
)

type Storage interface {
	getFactorialFromCache(n string) (string, error)
	saveFactorialToCache(n string, result string) error
	CalculateFactorial(ctx context.Context, req *utils.FactorialRequest) (*utils.FactorialResponse, error)
}
