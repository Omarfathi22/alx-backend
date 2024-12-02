#!/usr/bin/yarn dev
// This is a shebang line that indicates the script should be executed using the `yarn dev` command.
// It assumes that the development environment is set up to run the script with Yarn.

import { createClient } from 'redis';

const client = createClient();

client.on('error', (err) => {

    console.log('Redis client not connected to the server:', err.toString());
});

client.on('connect', () => {

    console.log('Redis client connected to the server');
});