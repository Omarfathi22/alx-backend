#!/usr/bin/yarn dev
// This script is designed to interact with a Redis server, utilizing the Redis Node.js client library.

import { createClient, print } from 'redis';

const client = createClient();

client.on('error', (err) => {
    console.log('Redis client not connected to the server:', err.toString());
});

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

const setNewSchool = (schoolName, value) => {
    // This function sets a key-value pair in Redis. The `print` function logs the result of the operation.
    client.SET(schoolName, value, print);
};

const displaySchoolValue = (schoolName) => {
    // This function retrieves the value of a specified key from Redis and logs it to the console.
    client.GET(schoolName, (_err, reply) => {
        console.log(reply);
    });
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
