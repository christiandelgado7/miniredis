Engineering Redis Challenge
==========================

## Objective

Redis is an in-memory NoSQL data store that supports operations or “commands” on data structures such as sets, lists and hashes. Your objective is to implement a service that supports a subset of the Redis command set. That is, you are to build a “mini redis”.

This has two parts -- first, the implementation of Redis commands and the underlying data structure to support them, and second, support for calling this “mini redis” over the network.


## Command List

This is the list of Redis's commands implemented in this exercise:

   1. SET key value
   2. SET key value EX seconds (need not implement other SET options)
   3. GET key
   4. DEL key
   5. DBSIZE
   6. INCR key
   7. ZADD key score member
   8. ZCARD key
   9. ZRANK key member
   10. ZRANGE key start stop

The command definitions are all available at [http://redis.io/commands].

## Getting started

- Create and activate a virtualenv using Python 2.7 (or bigger).

- Install the dependencies listed in the requirements.txt file:
    > pip install -r requirements.txt

- Start the miniredis server:
    > cd miniredis
    > python server.py
    
- The app can be access by any HTTP client throw the URL (if you don't select --no-rest):    
    > http://localhost:8080?cmd={command}
 
## Server Run Options

#### As Python process

You can run the MiniRedis server as a python execution using the script `server.py`. Using Python 2.7 or higher.

This script accepts the follow arguments as optionals: 

  > python server.py [-p P] [--no-cmd | --no-rest]
  
  - -p XXXX       select which port number will be used for the REST API
  - --no-cmd      don't open shell console
  - --no-rest     don't start HTTP Server for REST API
  - -h            show the help message for each argument


#### As Docker container

You can also run the MiniRedis server as a Docker container. 

If you have docker installed in your computer, you can use the Makefile to build and run the container.

- Build docker image:
    > make build
- run the container:
    > make run
- run the container in background:
    > make run-detached

## UnitTest

There is a script for test all the method in the MiniRedis server (`./test/test_miniredist.py`). 

- To run the test use:
  > python -m unittest discover -v

## Requirements

This app was developed using this environment: 

Python version
--------------
* Python 2.7.12

Python libraries
----------------

* Flask==0.12.1

