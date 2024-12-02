#!/usr/bin/yarn dev
// This script is designed to interact with a Redis server using the Redis client for Node.js.
// The `yarn dev` shebang is used to execute the script in a development environment with Yarn.

import { promisify } from 'util';
// Import the `promisify` function from the `util` module to convert callback-based functions to promises.

import { createClient, print } from 'redis';
// Import `createClient` to create a Redis client and `print` to log the results of Redis operations.

const client = createClient();
// Create a new Redis client to connect to the server.

client.on('error', (err) => {
    // Listen for 'error' events and log a message if the client cannot connect to the server.
    console.log('Redis client not connected to the server:', err.toString());
});

const setNewSchool = (schoolName, value) => {
    // Function to set a key-value pair in Redis. Uses the `SET` command with the `print` callback to log the result.
    client.SET(schoolName, value, print);
};

const displaySchoolValue = async (schoolName) => {
    // Function to retrieve the value of a key from Redis.
    // Uses `promisify` to convert the callback-based `GET` function into a promise.
    console.log(await promisify(client.GET).bind(client)(schoolName));
};

async function main() {
    // Main function to execute Redis operations in sequence.
    await displaySchoolValue('Holberton'); // Display the value of the 'Holberton' key (if it exists).
    setNewSchool('HolbertonSanFrancisco', '100'); // Set a new key-value pair in Redis.
    await displaySchoolValue('HolbertonSanFrancisco'); // Display the value of the 'HolbertonSanFrancisco' key.
}

client.on('connect', async () => {

    console.log('Redis client connected to the server');
    await main();
});
