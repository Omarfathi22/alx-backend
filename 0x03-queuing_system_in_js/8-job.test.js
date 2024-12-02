#!/usr/bin/yarn test
// This script is used for testing the `createPushNotificationsJobs` function
// using Mocha and Chai for unit testing.

import sinon from 'sinon';
import { expect } from 'chai';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job.js'; // Import the function to be tested

describe('createPushNotificationsJobs', () => {
    const BIG_BROTHER = sinon.spy(console); // Spy on console.log to monitor calls
    const QUEUE = createQueue({ name: 'push_notification_code_test' }); // Create a test queue

    before(() => {
        // Enable the test mode for the queue before the tests
        QUEUE.testMode.enter(true);
    });

    after(() => {
        // Clear and exit test mode after tests are complete
        QUEUE.testMode.clear();
        QUEUE.testMode.exit();
    });

    afterEach(() => {
        // Reset the spy on console.log after each test
        BIG_BROTHER.log.resetHistory();
    });

    it('displays an error message if jobs is not an array', () => {
        // Test case to ensure an error is thrown when jobs is not an array
        expect(
            createPushNotificationsJobs.bind(createPushNotificationsJobs, {}, QUEUE)
        ).to.throw('Jobs is not an array');
    });

    it('adds jobs to the queue with the correct type', (done) => {
        // Test case to ensure jobs are added to the queue with the correct data and type
        expect(QUEUE.testMode.jobs.length).to.equal(0);
        const jobInfos = [
            {
                phoneNumber: '44556677889',
                message: 'Use the code 1982 to verify your account',
            },
            {
                phoneNumber: '98877665544',
                message: 'Use the code 1738 to verify your account',
            },
        ];
        createPushNotificationsJobs(jobInfos, QUEUE); // Create the jobs
        expect(QUEUE.testMode.jobs.length).to.equal(2); // Ensure 2 jobs are created
        expect(QUEUE.testMode.jobs[0].data).to.deep.equal(jobInfos[0]); // Check job data
        expect(QUEUE.testMode.jobs[0].type).to.equal('push_notification_code_3'); // Check job type
        QUEUE.process('push_notification_code_3', () => {
            // Process the job and check if the correct log is made
            expect(
                BIG_BROTHER.log
                    .calledWith('Notification job created:', QUEUE.testMode.jobs[0].id)
            ).to.be.true;
            done(); // Call done() to signal test completion
        });
    });

    it('registers the progress event handler for a job', (done) => {
        // Test case to ensure progress events are handled correctly
        QUEUE.testMode.jobs[0].addListener('progress', () => {
            // Check if the progress log is called
            expect(
                BIG_BROTHER.log
                    .calledWith('Notification job', QUEUE.testMode.jobs[0].id, '25% complete')
            ).to.be.true;
            done(); // Call done() to signal test completion
        });
        QUEUE.testMode.jobs[0].emit('progress', 25); // Emit a progress event
    });

    it('registers the failed event handler for a job', (done) => {
        // Test case to ensure failed events are handled correctly
        QUEUE.testMode.jobs[0].addListener('failed', () => {
            // Check if the failure log is called with the error message
            expect(
                BIG_BROTHER.log
                    .calledWith('Notification job', QUEUE.testMode.jobs[0].id, 'failed:', 'Failed to send')
            ).to.be.true;
            done(); // Call done() to signal test completion
        });
        QUEUE.testMode.jobs[0].emit('failed', new Error('Failed to send')); // Emit a failure event
    });

    it('registers the complete event handler for a job', (done) => {
        // Test case to ensure complete events are handled correctly
        QUEUE.testMode.jobs[0].addListener('complete', () => {
            // Check if the completion log is called
            expect(
                BIG_BROTHER.log
                    .calledWith('Notification job', QUEUE.testMode.jobs[0].id, 'completed')
            ).to.be.true;
            done(); // Call done() to signal test completion
        });
        QUEUE.testMode.jobs[0].emit('complete'); // Emit a completion event
    });
});