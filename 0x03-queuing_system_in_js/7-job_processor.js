#!/usr/bin/yarn dev
// This script demonstrates how to use the Kue library to create and process jobs for sending push notifications.
// The `yarn dev` shebang ensures the script runs in a development environment with Yarn.

import { createQueue, Job } from 'kue';
// Import `createQueue` to create a job queue and `Job` for defining job-related operations.

const BLACKLISTED_NUMBERS = ['4153518780', '4153518781'];
// Array of blacklisted phone numbers. Notifications to these numbers will not be sent.

const queue = createQueue();
// Create a job queue using Kue.

/**
 * Sends a push notification to a user.
 * @param {String} phoneNumber - The phone number to send the notification to.
 * @param {String} message - The message to include in the notification.
 * @param {Job} job - The job instance for tracking progress.
 * @param {*} done - Callback to mark the job as completed or failed.
 */
const sendNotification = (phoneNumber, message, job, done) => {
    let total = 2, pending = 2; // Total steps for sending the notification.
    let sendInterval = setInterval(() => {
        if (total - pending <= total / 2) {
            // Report job progress when half of the total steps are completed.
            job.progress(total - pending, total);
        }
        if (BLACKLISTED_NUMBERS.includes(phoneNumber)) {
            // If the phone number is blacklisted, log an error and stop further processing.
            done(new Error(`Phone number ${phoneNumber} is blacklisted`));
            clearInterval(sendInterval); // Clear the interval to stop the process.
            return;
        }
        if (total === pending) {
            // Log the notification details when starting the process.
            console.log(
                `Sending notification to ${phoneNumber},`,
                `with message: ${message}`,
            );
        }
        --pending || done(); // Decrement the pending steps and mark the job as done if no steps remain.
        pending || clearInterval(sendInterval); // Clear the interval once all steps are completed.
    }, 1000); // Execute the steps with a 1-second interval.
};

queue.process('push_notification_code_2', 2, (job, done) => {
    // Process jobs in the 'push_notification_code_2' queue with a concurrency of 2.
    sendNotification(job.data.phoneNumber, job.data.message, job, done);
});