# Sieve Database

This repository contains an implementation of Sieve, a learned data-skipping index for data analytics. This project is a collaboration between researchers at Huazhong University of Science and Technology (HUST) and Huawei Cloud Engineers.

## Project Structure

- `bp_tree.py`: Contains the implementation of the B+ tree used in the database.
- `dataset_parser.py`: Contains functions for parsing and filtering the Wikipedia dataset.
- `datasets/`: Directory containing the filtered Wikipedia datasets.
- `main.py`: The main entry point of the application.
- `node.py`: Contains the `Node` class used in the B+ tree.
- `mysql_database.py`: Contains the `Database` class for interacting with the MySQL database.
- `wiki_server_side.py`: Server-side code for the Wikipedia dataset.

## Setup

To set up and run the project, follow these steps:

1. Install the required dependencies.
2. Run `main.py` to start the application.
