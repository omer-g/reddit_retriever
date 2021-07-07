
# Reddit Retriever

Retrieves submissions and comments from a chosen subreddit, in a specified time frame and saves data in a `.xls` file (and optionally a `.csv`).

Submissions are ordered by date. The comments of each submission are arranged according to popularity (descending) or date (oldest to newest). The text of submissions and comments is placed under the same `body` column (in the Pushshift API there is a `body` for comments and `selftext` for submissions). See code for more details.

## Requirements
The following libraries are required: `pandas`, `paws`

## Installation
1. Create and activate a ```virtualenv``` (optional)
2. Run:
   ```
   pip install -r requirements.txt
   ```
## Usage
Set parameters in ```reddit_retriever.py``` and run:
```python reddit_retriever.py```

## License
Available under [MIT](https://choosealicense.com/licenses/mit/) license
