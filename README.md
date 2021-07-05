
# Reddit Retriever

Reddit Retriever is a Python script that uses PushShift API to get submissions and comments from a chosen subreddit, in a specified time frame and saves the data in a `.xls` or `.csv` file. Each submission is followed by its comments arranged according to popularity or date. The body text of submissions and comments is placed under the same column. See code for more details.

## Requirements
The following libraries are required: `pandas`, `paws`

## Installation
1. Create and activate a ```virtualenv``` (optional)
2. Type in terminal:
   ```
   pip install -r requirements.txt
   ```

## License
Available under [MIT](https://choosealicense.com/licenses/mit/) license