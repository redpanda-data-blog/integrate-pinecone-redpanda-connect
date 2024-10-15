# Redpanda Connect Example: Social Media Comment Monitor

This repository contains all the code you need to run the example from this article on the Redpanda blog (link still needed).

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/kkoppenhaver/redpanda-connect-example.git
   cd redpanda-connect-example
   ```

2. Install dependencies with Poetry:
   ```sh
   poetry install
   ```

## Configuration

1. Set up a Redpanda Connect cluster and create a topic.
2. `cp .env.example .env` and fill out the `.env` file with all of the configuration variables from Redpanda and Pinecone.

## Usage

1. Activate the Poetry environment:
   ```sh
   poetry shell
   ```

2. Run the script to populate your Redpand topic with comments:
   ```sh
   python producer.py
   ```

3. Once your sample comments are in Pinecone, you can run the following script to evaluate a new comment:
   ```sh
   python comment_checker.py
   ```
