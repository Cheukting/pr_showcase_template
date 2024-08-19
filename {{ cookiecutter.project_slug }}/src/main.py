import requests
import yaml
import os

from svg_gen import gen_full, gen_compact
from validation import input_val
from social import post_to_social

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

input_val(config)

headers = {"Authorization": os.environ["TOKEN"]}

all_prs = []

for repo in config["repos"]:
    if config["state"] in ["open", "closed"]:
        res = requests.get(
            f'https://api.github.com/search/issues?q=repo:{repo}+type:pr+author:{config['username']}+state:{config['state']}',
            headers=headers,
        )
    else:
        res = requests.get(
            f'https://api.github.com/search/issues?q=repo:{repo}+type:pr+author:{config['username']}',
            headers=headers,
        )
    res_context = res.json()
    all_prs += res_context["items"]

with open(config["output"], "w") as file:
    if config["style"] == "compact":
        file.write(
            gen_compact(
                all_prs,
                headers,
                config["username"],
                config["state"],
                config["apperance"],
            )
        )
    else:
        file.write(gen_full(all_prs, headers, config["apperance"]))

print(f'{config["output"]} has been generated.')
print()

if (
    config["social"]["twitter"] is not None
    or config["social"]["mastodon"] is not None
    or config["social"]["linkedin"] is not None
):
    post_to_social(all_prs, config["social"])
