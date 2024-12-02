#!/usr/bin/yarn dev
// This script creates an Express API to manage a product catalog and handle stock reservations.
// It interacts with Redis to store and manage stock data.

import express from 'express';
import { promisify } from 'util'; // For converting Redis client methods to promises
import { createClient } from 'redis'; // To interact with Redis

// Sample list of products
const listProducts = [
    {
        itemId: 1,
        itemName: 'Suitcase 250',
        price: 50,
        initialAvailableQuantity: 4
    },
    {
        itemId: 2,
        itemName: 'Suitcase 450',
        price: 100,
        initialAvailableQuantity: 10
    },
    {
        itemId: 3,
        itemName: 'Suitcase 650',
        price: 350,
        initialAvailableQuantity: 2
    },
    {
        itemId: 4,
        itemName: 'Suitcase 1050',
        price: 550,
        initialAvailableQuantity: 5
    },
];

// Helper function to get a product by its ID
const getItemById = (id) => {
    const item = listProducts.find(obj => obj.itemId === id);
    if (item) {
        return Object.fromEntries(Object.entries(item)); // Return the product as an object
    }
};

// Initialize Express application
const app = express();

// Create a Redis client for managing stock reservations
const client = createClient();
const PORT = 1245;

// Function to reserve stock for a given product
/**
 * Modifies the reserved stock for a given item.
 * @param {number} itemId - The id of the item.
 * @param {number} stock - The stock of the item.
 */
const reserveStockById = async (itemId, stock) => {
    return promisify(client.SET).bind(client)(`item.${itemId}`, stock); // Set stock value in Redis
};

// Function to get the current reserved stock for a given product
/**
 * Retrieves the reserved stock for a given item.
 * @param {number} itemId - The id of the item.
 * @returns {Promise<String>}
 */
const getCurrentReservedStockById = async (itemId) => {
    return promisify(client.GET).bind(client)(`item.${itemId}`); // Get stock value from Redis
};

// Route to get the list of all products
app.get('/list_products', (_, res) => {
    res.json(listProducts); // Return all products as JSON
});

// Route to get the details of a single product by ID
app.get('/list_products/:itemId(\\d+)', (req, res) => {
    const itemId = Number.parseInt(req.params.itemId); // Parse the item ID from the URL
    const productItem = getItemById(Number.parseInt(itemId)); // Find the product by its ID

    if (!productItem) {
        res.json({ status: 'Product not found' }); // Return an error if product not found
        return;
    }

    // Retrieve the current reserved stock for the product
    getCurrentReservedStockById(itemId)
        .then((result) => Number.parseInt(result || 0)) // Convert result to an integer, defaulting to 0
        .then((reservedStock) => {
            productItem.currentQuantity = productItem.initialAvailableQuantity - reservedStock; // Calculate available quantity
            res.json(productItem); // Return the product details with the available stock
        });
});

// Route to reserve stock for a product by ID
app.get('/reserve_product/:itemId', (req, res) => {
    const itemId = Number.parseInt(req.params.itemId); // Parse the item ID from the URL
    const productItem = getItemById(Number.parseInt(itemId)); // Find the product by its ID

    if (!productItem) {
        res.json({ status: 'Product not found' }); // Return an error if product not found
        return;
    }

    // Check current reserved stock for the product
    getCurrentReservedStockById(itemId)
        .then((result) => Number.parseInt(result || 0)) // Convert result to an integer, defaulting to 0
        .then((reservedStock) => {
            // If the reserved stock is equal to or greater than the available stock, reject the reservation
            if (reservedStock >= productItem.initialAvailableQuantity) {
                res.json({ status: 'Not enough stock available', itemId });
                return;
            }

            // Otherwise, reserve 1 more unit and update the Redis stock
            reserveStockById(itemId, reservedStock + 1)
                .then(() => {
                    res.json({ status: 'Reservation confirmed', itemId }); // Confirm reservation
                });
        });
});

// Function to reset all product stock in Redis to 0
const resetProductsStock = () => {
    return Promise.all(
        listProducts.map(
            item => promisify(client.SET).bind(client)(`item.${item.itemId}`, 0), // Set stock to 0 for all items
        )
    );
};

// Start the server and reset the stock before listening
app.listen(PORT, () => {
    resetProductsStock()
        .then(() => {
            console.log(`API available on localhost port ${PORT}`); // Log that the server is running
        });
});

export default app; // Export the app for testing or further use