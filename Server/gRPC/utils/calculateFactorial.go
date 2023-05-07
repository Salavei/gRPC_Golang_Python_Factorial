package utils

import (
	"math/big"
)

// calculateFactorial returns the utils of a given integer.
func CalculateFactorial(n int64) *big.Int {
	result := big.NewInt(1)
	for i := int64(2); i <= n; i++ {
		result.Mul(result, big.NewInt(i))
	}
	return result
}
