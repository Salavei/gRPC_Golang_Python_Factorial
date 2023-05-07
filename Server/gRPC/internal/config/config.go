package config

import (
	"fmt"
	"github.com/ilyakaznacheev/cleanenv"
	"log"
	"os"
	"sync"
)

type Config struct {
	Listen  struct {
		Type   string `yaml:"type" env-required:"port"`
		BindIP string `yaml:"bind_ip" env-required:"127.0.0.1"`
		Port   string `yaml:"port" env-required:"8080"`
	} `yaml:"listen"`
	Storage StorageConfig `yaml:"storage"`
}

type StorageConfig struct {
	Addr     string `yaml:"addr"`
	Password string `yaml:"password"`
	DB       int `yaml:"db"`
}

var instance *Config
var once sync.Once

func GetConfig() *Config {
	once.Do(func() {
		log.Println("read application configuration")
		instance = &Config{}
		if err := cleanenv.ReadConfig("config.yml", instance); err != nil {
			help, _ := cleanenv.GetDescription(instance, nil)
			log.Println(help)
			log.Fatal(err)
		}
	})
	instance.Storage.Addr = fmt.Sprintf("%s:6379", os.Getenv("DB_HOST"))
	return instance
}