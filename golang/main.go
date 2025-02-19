package main

import (
	"fmt"
	"io"
	"net/http"
)

var jokeBody string // Package-level variable to store the joke

func welcome(w http.ResponseWriter, _ *http.Request) {
	fmt.Fprintf(w, "Hope you are doing good, just know you do not need stupid people to shine")
}

func getJoke(w http.ResponseWriter, _ *http.Request) {
	fmt.Fprintf(w, jokeBody) // Use the package-level variable
}

func main() {
	// Fetch the joke from the API
	response, err := http.Get("https://official-joke-api.appspot.com/random_joke")
	if err != nil {
		fmt.Println("Error fetching joke:", err)
		return
	}
	defer response.Body.Close() // Ensure the response body is closed

	// Read the response body
	body, err := io.ReadAll(response.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		return
	}

	// Store the joke in the package-level variable
	jokeBody = string(body)

	// fmt.Println("Response body:", jokeBody)

	// Set up HTTP handlers
	http.HandleFunc("/welcome", welcome)       // Root endpoint
	http.HandleFunc("/", getJoke)   // Joke endpoint

	// Start the HTTP server
	fmt.Println("Server started at :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Error starting server:", err)
	}
}