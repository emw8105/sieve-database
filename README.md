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

## Sources
### Dataset:
- Description: The dataset used to demonstrate the proficiency of Sieve's algorithms, as featured in the paper. We specifically utilized a subset of data from the Wikimedia pagecounts, filtered to exclude non-English pages and pages with a view count of 1.
- Download Link: [Wikimedia Pagecounts Raw Data](https://dumps.wikimedia.org/other/pagecounts-raw/)
- Date: July 1, 2016
- Files:
  - pagecounts-20160701-000000.gz (72MB)
  - pagecounts-20160701-010000.gz (84MB)
  - pagecounts-20160701-020000.gz (90MB)
  - pagecounts-20160701-030000.gz (85MB)
- Direct Link: [July 1, 2016 Data Slice](https://dumps.wikimedia.org/other/pagecounts-raw/2016/2016-07/)

### Research Paper:
- Title: Sieve: A Learned Data-Skipping Index for Data Analytics
- Authors: Yulai Tong, Jiazhen Liu, Hua Wang, Ke Zhou, Rongfeng He, Qin Zhang, Cheng Wang
- DOI: 10.14778/3611479.3611520
- Link: [Sieve Research Paper](https://dl.acm.org/doi/10.14778/3611479.3611520)

## Notes
This implementation seeks to solve issues of querying speed for large datasets as well as reducing the storage requirement overhead needed to improve the speed. Traditionally, a simple B+ tree is implemented to quickly locate the desired key and determine the locations to find the corresponding data. However, by taking advantage of block trends, we can reduce a lot of space through the usage of partitioning and segmenting. For example, this implementation mirrors the Sieve research paper by utilizing a series of Wikipedia page information dumps. The viewcount is used as the key in this case. Pages with viewcounts from 1-200 are incredibly common. As a result, they are found in every single block we used in our dataset. Instead of having each key map to a list of pointers, we can define an interval called a partition that groups neighboring keys with the same pointer list. This improves querying speed by indexing through intervals faster than individual keys, and also improves storage usage. 

In our implementation, we found that even in the worst case, partitions and segmentations saved approximately 50% of the storage overhead compared to a traditional keymap, sometimes as much as 90% or more. A series of print methods have been added to the bp_tree class to reveal some of the internal structuring, including key-map distribution, partition and segment distribution, and memory utilization of both. Additionally, query speed improved by about 10-20% depending on how many blocks were included in the pointer list.

While this implementation is emulating a database, the results are similar to those found in the paper's findings.
