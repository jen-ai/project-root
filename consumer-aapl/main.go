package main

import (
	"log"
	"os"

	"github.com/streadway/amqp"
)

func main() {
	rabbitMQURL := os.Getenv("RABBITMQ_URL")
	queueName := os.Getenv("QUEUE_NAME")

	conn, err := amqp.Dial(rabbitMQURL)
	if err != nil {
		log.Fatalf("RabbitMQ bağlantısı başarısız: %s", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Kanal oluşturulamadı: %s", err)
	}
	defer ch.Close()

	msgs, err := ch.Consume(
		queueName,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Kuyruğa abone olunamadı: %s", err)
	}

	for msg := range msgs {
		log.Printf("Mesaj alındı: %s", msg.Body)
	}
}
