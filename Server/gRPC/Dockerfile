FROM golang:1.19-alpine

# Set the Current Working Directory inside the container
WORKDIR /usr/src/app

# We want to populate the module cache based on the go.{mod,sum} files.
COPY go.mod .
COPY go.sum .

RUN go mod download


COPY . .

# Build the Go app
RUN go build -o ./cmd/main ./cmd/main

RUN chmod +x ./cmd/main

CMD ["./cmd/main/main"]
