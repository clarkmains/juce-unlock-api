# JUCE Framework Online Unlock API Simulator

A simple AWS serverless JUCE Framework Online Unlock API Simulator deployed with [AWS SAM](https://aws.amazon.com/serverless/sam/).

## Overview

This repository contains code to deploy an simulation of the JUCE Framework Online Unlock service as a serverless application on AWS.

This can be useful for solo developers or small teams to simulate the online unlock service for audio applications and plugins developed with the JUCE Framework.

This approach offers the following advantages -

- Uses an Amazon CA-signed Certificate, so no messing around with self-signed certificates
- Deploys in a reproducable manner in under 1 minute via infrastructure code
- Can be used by multiple developers and environments simultaneously
- Can be deployed multiple times to facilitate multiple apps

Parameters such as password are all exposed in clear text though, so this is obviously not a production system.

**IMPORTANT** - before deploying, be sure you read the [AWS Free Tier](https://aws.amazon.com/free) docs and understand the limitations.

## Requirements

In addition to the requirements of the JUCE Framework, the following is required -

- An AWS Account and some familiarity with AWS
- [AWS SAM](https://aws.amazon.com/serverless/sam/) installed
- Python 3.8 installed

## Deploy the AWS SAM Application Stack

From the root of this repository, run the following commands -

    sam build
    sam deploy --guided

You will be guided through the initial deployment of the AWS SAM Application. The defaults are suitable for most of the prompts, but be sure to configure the following options appropriately -

Use the AWS Region that is most appropriate for your location:

    AWS Region [us-east-1]: eu-west-1

Specify the CIDR Range for your network, this may be your own IP or a comma separated list of multiple IPs if you are working with other developers:

    Parameter AllowedIpRanges []: 48.129.53.185/32

The stack will take around a minute to deploy, after which the outputs will be displayed:

    Outputs
    --------------------------------------------------------------------------------
    Key           UnlockApiEndpoint
    Description   Unlock API endpoint URL
    Value         https://xtjt1rwgi6.execute-api.eu-west-1.amazonaws.com/Prod/unlock
    --------------------------------------------------------------------------------

Take a note of this value as it will be required during the tutorial.

## Complete the JUCE Tutorial

Throughout this document we refer to the official JUCE Tutorial [Unlock your plugins through online registration](https://docs.juce.com/master/tutorial_online_unlock_status.html).

If you are already familiar with the JUCE online unlock service you probably don't need to actually follow the tutorial described here, but this part uses the tutorial to describe how to integrate the simulator with your application.

Follow the tutorial to the praragraph describing an update to the `getServerAuthenticationURL()` function. Use the value from the UnlockApiEndpoint Output you noted earlier.

The end result will be something like this:

    juce::URL getServerAuthenticationURL() override
    {
        return juce::URL ("https://psdr5l669l.execute-api.eu-west-1.amazonaws.com/Prod/unlock");
    }

Continue to follow the tutorial until you reach the section headed "Setting up the back end server". It is worthwhile reading this section to understand what is going on under the hood but there is no need to follow any of the setup instructions as we have already deployed our back end api.

Continue to the end of the section where a test procedure is described in the paragraph beginning:

> If all works properly, launch the application and attempt authorisation by submitting an arbitrary email and password combination..

Follow this step and you should be able to test the back end api we have deployed in AWS.

Continue on to the section headed "Generating security keys".

Generate the Keys and update the `getPublicKey` function as described. Once you have the Unlock Key for the product, take a note of the key and stop at this step. Now we need to update the AWS SAM Application with the Unlock Key.

Run a SAM Guided Deploy again:

    sam deploy --guided

Step through the arguments, accepting the existing values until you get to the Parameter `UserKey`.

Paste in the Unlock Key that was generated:

    Parameter UserKey [UNLOCK_KEY_PLACEHOLDER]: #2f61e449565fe57d828d5be0e78...

Step through the remaining arguments and allow the deployment of the stack update to proceed. This should only take a few seconds.

Configuration is now complete. You can proceed with the remainder of the tutorial and should be able to successfully emulate online registration and unlock of the tutorial application!

## Delete the AWS SAM Application Stack

To delete the resources you have deployed - open the AWS Console and navigate to the "Stacks" view of the "CloudFormation" service. You should see a Stack with the name you chose to use during the deployment step earlier. Select it and click the Delete button.

That's all folks :)
