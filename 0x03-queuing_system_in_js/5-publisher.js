#!/usr/bin/yarn dev
// This script demonstrates how to publish messages to a Redis channel using the Redis Node.js client.
// The `yarn dev` shebang indicates the script is run in a development environment with Yarn.

import { createClient } from 'redis';
// Import the `createClient` function from the `redis` library to create a Redis client.

const client = createClient();
// Create a new Redis client instance to connect to the Redis server.

client.on('error', (err) => {
    // Listen for the 'error' event and log an error message if the client encounters connection issues.
    console.log('Redis client not connected to the server:', err.toString());
});

const publishMessage = (message, time) => {
    // Function to publish a message to the Redis channel 'holberton school channel' after a specified delay.
    setTimeout(() => {
        console.log(`About to send ${message}`);
        client.publish('holberton school channel', message);
        // Publish the message to the Redis channel.
    }, time);
};

client.on('connect', () => {
    // Listen for the 'connect' event and log a message when the client successfully connects to the server.
    console.log('Redis client connected to the server');
});

// Publish a series of messages with different delays to the 'holberton school channel'.
publishMessage('Holberton Student #1 starts course', 100); // Message published after 100ms.
publishMessage('Holberton Student #2 starts course', 200); // Message published after 200ms.
publishMessage('KILL_SERVER', 300); // Message to signal server termination published after 300ms.
publishMessage('Holberton Student #3 starts course', 400); // Message published after 400ms.
