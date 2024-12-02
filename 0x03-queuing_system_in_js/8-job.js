#!/usr/bin/yarn dev
// This script demonstrates how to create push notification jobs in a Kue queue.
// The `yarn dev` shebang indicates the script is intended for a development environment.

import { Queue, Job } from 'kue';
// Import `Queue` for managing the job queue and `Job` for job operations.

/**
 * Creates push notification jobs from the array of jobs info.
 * @param {Job[]} jobs - Array of job objects containing job data (e.g., phoneNumber, message).
 * @param {Queue} queue - The Kue queue instance to which jobs will be added.
 * @throws Will throw an error if `jobs` is not an array.
 */
export const createPushNotificationsJobs = (jobs, queue) => {
    if (!(jobs instanceof Array)) {
        // Validate that the `jobs` parameter is an array.
        throw new Error('Jobs is not an array');
    }

    for (const jobInfo of jobs) {
        // Iterate through each job info object in the array.
        const job = queue.create('push_notification_code_3', jobInfo);
        // Create a new job of type 'push_notification_code_3' with the provided job data.

        job
            .on('enqueue', () => {
                // Event listener for when the job is added to the queue.
                console.log('Notification job created:', job.id);
            })
            .on('complete', () => {
                // Event listener for when the job completes successfully.
                console.log('Notification job', job.id, 'completed');
            })
            .on('failed', (err) => {
                // Event listener for when the job fails.
                console.log(
                    'Notification job',
                    job.id,
                    'failed:',
                    err.message || err.toString()
                );
            })
            .on('progress', (progress, _data) => {
                // Event listener for job progress updates.
                console.log('Notification job', job.id, `${progress}% complete`);
            });

        job.save();
        // Save the job to the queue so it can be processed.
    }
};

export default createPushNotificationsJobs;
// Export the function for use in other modules.
