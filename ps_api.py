import datetime
import calendar
import json
import pandas
from psaw import PushshiftAPI


SUBREDDIT = "progun"

# Date in ISO format "YYYY-MM-DD" (ex: "2016-06-12")
START_DATE = "2016-06-12"
END_DATE = "2016-06-14"

# Number of days after end date to request comments
EXTRA_DAYS_FOR_COMMENTS = 7

# Change to True to also create a csv file
CREATE_CSV = False

# OPTIONAL query string (only searches submissions)
QUERY = None


def date_to_epoch(date_iso, delta_days = None):
    if not date_iso:
        return None
    dt = datetime.date.fromisoformat(date_iso)
    if delta_days:
        delta = datetime.timedelta(days=delta_days)
        dt += delta
    return calendar.timegm(dt.timetuple())


def print_response(response):
    try:
        print(json.dumps(response.json(), indent=4, sort_keys=True))
    except Exception as e:
        print("Did not receive parsable json.\nError:", e)


def _gen_field_str(FIELD, first=False):
    if not FIELD:
        return ""
    return FIELD if first == True else "_" + FIELD


def generate_excel(result, create_csv=False):
    try:
        panda_df = pandas.DataFrame(result)
        
        now = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        sr = _gen_field_str(SUBREDDIT, first=True)
        q = _gen_field_str(QUERY)
        s = _gen_field_str(START_DATE)
        e = _gen_field_str(END_DATE)

        file_name = f"{sr}{s}{q}_to{e}_on{now}"
        panda_df.to_excel(file_name + ".xlsx")
        if create_csv:
            panda_df.to_csv(file_name + ".csv")
    except Exception as e:
        print("Could not generate file.\nError:", e)


def get_date(epoch):
    datetime_date = datetime.datetime.fromtimestamp(epoch)
    return datetime_date.strftime("%m-%d-%Y_%H-%M-%S")


def full_name_to_id(name):
    if "_" in name:
        name = name.split("_")[1]
    return name


if __name__=="__main__":
    pushshift_api = PushshiftAPI()

    comment_fields = ["id","author", "body","link_id", "created_utc",
                      "parent_id", "subreddit", "score"]
    submission_fields = ["id", "created_utc", "author", "selftext",
        "subreddit", "title", "score", "num_comments", "full_link"]
    kargs = {
        "subreddit": SUBREDDIT,
        "q": QUERY,
        "after": date_to_epoch(START_DATE),
        "before": date_to_epoch(END_DATE),
        "size": 500,
    }

    kargs_comment = dict(kargs)
    kargs_comment["fields"] = comment_fields
    kargs_comment["before"] = date_to_epoch(END_DATE, EXTRA_DAYS_FOR_COMMENTS)
    kargs_submission = dict(kargs)
    kargs_submission["fields"] = submission_fields

    full_comments = list(pushshift_api.search_comments(**kargs_comment))
    full_submissions = list(pushshift_api.search_submissions(**kargs_submission))
    full_submissions.sort(key=lambda k: k.d_['created_utc'])
    submissions = [submission.d_ for submission in full_submissions]

    result = []
    for submission in submissions:
        submission["type"] = "submission"
        submission["date_posted"] = get_date(submission["created_utc"])
        submission["body"] = submission["selftext"]
        submission.pop("selftext", None)
        result.append(submission)

        submission_id = submission["id"]
        submission_comments = [obj.d_ for obj in full_comments
                               if submission_id in obj.d_["link_id"]]
        submission_comments.sort(key=lambda k: k['created_utc'])
        for i in range(len(submission_comments)):
            submission_comments[i]["type"] = "comment"
            link_id = submission_comments[i]["link_id"]
            submission_comments[i]["link_id"] = full_name_to_id(link_id)
            
            # In case API returns fullname
            comment_id = submission_comments[i]["id"]
            submission_comments[i]["id"] = full_name_to_id(comment_id)
            submission_comments[i]["full_link"] = submission["full_link"] + comment_id
            epoch = submission_comments[i]["created_utc"]
            submission_comments[i]["date_posted"] = get_date(epoch)   
            submission_comments[i]["title"] = submission["title"]
        result += submission_comments
    generate_excel(result, create_csv=CREATE_CSV)
