import requests
import jsoncsv
import csv
import os
import json
import time

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIX8ZQEAAAAA48y88V5DjkyC%2FXJEn%2BVVrpLKlLY%3DJxeEjgjOsCdKKFwzGCeP2THIHunTaHviZf9jdZgbo5Mz898FAx'

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(NFT OR "non-fungible token") -gn -gm -tag -DROP -WINNER -giveaway -claim -is:retweet -is:reply -has:links','tweet.fields': 'id,text,author_id,created_at,public_metrics,source','max_results': 100}
next_token = {}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    if "next_token" in json_response["meta"]:
        query_params["next_token"] = json_response["meta"]["next_token"]
    else:
        return False
    print(json.dumps(json_response, indent=4, sort_keys=True))
    
    
    jsoncsv.append_to_csv(json_response, "data.csv")
    return True


if __name__ == "__main__":
    csvFile = open("data.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    # #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(['author id', 'created_at', 'id', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet'])
     
    csvFile.close()
    while main():
        time.sleep(6)