import requests
import os
from datetime import datetime, timezone, timedelta
from requests_oauthlib import OAuth1

now = datetime.now(timezone.utc)


def gen_txt(type, pr):
    pr_info = {
        "repo": pr["repository_url"].split("/")[-1],
        "link": pr["url"],
        "title": pr["title"],
    }
    if type == "new":
        return f'I have made a new contribution "{pr_info["title"]}" to #{pr_info["repo"]}! See it at {pr_info["link"]}'
    elif type == "merged":
        return f'My contribution "{pr_info["title"]}" at #{pr_info["repo"]} have been accepted! See it at {pr_info["link"]}'


def post_to_twitter(text):
    url = "https://api.x.com/2/tweets"

    auth = OAuth1(
        f'{os.environ["X_API_KEY"]}',
        f'{os.environ["X_API_SECRET"]}',
        f'{os.environ["X_ACCESS_TOKEN"]}',
        f'{os.environ["X_ACCESS_SECRET"]}',
    )

    headers = {
        "Content-Type": "application/json",
    }
    return requests.post(url, headers=headers, auth=auth, json={"text": text})


def post_to_mastodon(text, domain):
    headers = {
        "Authorization": f'Bearer {os.environ["MASTODON_TOKEN"]}',
        "Content-Type": "application/json",
    }
    return requests.post(
        f"https://{domain}/api/v1/statuses", headers=headers, json={"status": text}
    )


def post_to_linkedin(text):
    res = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={
            "Authorization": f"Bearer {os.environ["LINKEDIN_TOKEN"]}",
            "Content-Type": "application/json",
        },
    )
    handle = res.json()["sub"]
    content = {
        "author": f"urn:li:person:{handle}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    headers = {
        "Authorization": f"Bearer {os.environ["LINKEDIN_TOKEN"]}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    return requests.post(
        f"https://api.linkedin.com/v2/ugcPosts", headers=headers, json=content
    )


def feedback(url, text, res):
    if res.ok:
        print(f"Posted to {url} with:")
        print(text)
    else:
        print(f"Failed to post to {url}. Error:")
        print(res.text)
    print()


def post_to_each_social(pr, accounts, type):
    text = gen_txt(type, pr)
    for key, value in accounts.items():
        match key:
            case "twitter":
                if value is not None:
                    url = f'https://x.com/{value.strip("@")}'
                    feedback(url, text, post_to_twitter(text))
            case "mastodon":
                if value is not None:
                    domain = value.split("@")[-1]
                    acc = value.split("@")[-2]
                    url = f"https://{domain}/@{acc}"
                    feedback(url, text, post_to_mastodon(text, domain))
            case "linkedin":
                if value is not None:
                    feedback(value, text, post_to_linkedin(text))


def post_to_social(prs, accounts):
    for pr in prs:
        if pr["state"] == "open":
            created = datetime.fromisoformat(pr["created_at"])
            if now - created < timedelta(days=1):
                post_to_each_social(pr, accounts, "new")
        elif pr["state"] == "closed" and pr["pull_request"]["merged_at"] is not None:
            merged = datetime.fromisoformat(pr["pull_request"]["merged_at"])
            if now - merged < timedelta(days=1):
                post_to_each_social(pr, accounts, "merged")
