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
- `query_output.txt`: A file containing the resulting records from the queried key.

## Setup

To set up and run the project, follow these steps:

1. Install the required dependencies.
2. Run `main.py` to start the application.

## Notes
This implementation seeks to solve issues of querying speed for large datasets as well as reducing the storage requirement overhead needed to improve the speed. Traditionally, a simple B+ tree is implemented to quickly locate the desired key and determine the locations to find the corresponding data. However, by taking advantage of block trends, we can reduce a lot of space through the usage of partitioning and segmenting. For example, this implementation mirrors the Sieve research paper by utilizing a series of Wikipedia page information dumps. The viewcount is used as the key in this case. Pages with viewcounts from 1-200 are incredibly common. As a result, they are found in every single block we used in our dataset. Instead of having each key map to a list of pointers, we can define an interval called a partition that groups neighboring keys with the same pointer list. This improves querying speed by indexing through intervals faster than individual keys, and also improves storage usage. 

In our implementation, we found that even in the worst case, partitions and segmentations saved approximately 50% of the storage overhead compared to a traditional keymap, sometimes as much as 90% or more. A series of print methods have been added to the bp_tree class to reveal some of the internal structuring, including key-map distribution, partition and segment distribution, and memory utilization of both. Additionally, query speed improved by about 10-20% depending on how many blocks were included in the pointer list.

While this implementation is emulating a database, the results are similar to those found in the paper's findings.
