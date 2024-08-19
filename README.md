# PR Showcase Template

Do you have a few favourite OSS projects that you have been contributing and want to highlight your contributions (in the form of PRs) in one place? Do you feel that you should advertise your open source contributions better but not comfortable to write self promotion posts on social media? I have the same problem too! Thus, I have created this script/ app that you could deploy on GitHub action to advertise your open source contributions on GitHub effortlessly.

You can see [how I use it on my GitHub repo here](https://github.com/Cheukting/contribution-board). And you can get your own by using [this cookiecutter template](https://github.com/Cheukting/pr_showcase_template).

## How to use this cookiecutter template

Follow [the instruction on cookiecutter documentation](https://cookiecutter.readthedocs.io/en/stable/installation.html) to install Python and cookiecutter. Then you can [create your own project](https://cookiecutter.readthedocs.io/en/stable/usage.html#works-directly-with-git-and-hg-mercurial-repos-too) by this command:

`cookiecutter https://github.com/Cheukting/pr_showcase_template`

After pressing enter, you will have the follow options to input:

- `project_name`: The name of your own project that is going to be generated.
- `project_slug`: recommend just accepting the default by pressing enter.
- `github_username`: your GitHub user name
- `showcase_repos`: the repos that you want to showcase, separated by a comma. They need to be the full name of the repo in the format of `<owner>/<repo_name>`. For example: "pandas-dev/pandas, numpy/numpy"
- `output_svg_name`: the file name of the svg file output.
- `pr_states`: options are "all", "open", "closed", wether only the "open" or "closed" PRs are shown, "all" will show both open and closed PRs.
- `output_style`: options are "full", "compact", if it is "full" it will show all the relevant PRs with title, if it is "compact" it will only show the PR counts for each repos.
- `board_title`: the title that will show at the top of the generated svg
- `twitter`: optional, your X (Twitter) handle e.g. @example
- `mastodon`: optional, your Mastodon handle e.g. @example@demo.org
- `linkedin`: optional, your LinkedIn profile page e.g. https://www.linkedin.com/in/<your_name>/

## Usage of the generated project

There are 2 main functionalities of this project:

1. Generate a board in svg format to showcase your open source contribution on GitHub. To create a public link to the svg file generated for use at your GitHub profile or your website, you have to enable GitHub pages (step 6 [here](https://docs.github.com/en/pages/quickstart#creating-your-website)) in the project repo where the svg file is located.

Example:

![Example of the svg output](https://cheuk.dev/contribution-board/output.svg)

2. [Optional] Announce to social media when you make a new PR or a PR got merged. To let the script get access to your social media account, tokens and secrets will need to be set up as environment variables (see next session).

General customisation can be down with changing the properties of `config.yml`. For more fine grain customisation, please see advance usage session.

## Set up access token as environment variables

The following tokens can be added as environment variables to add extra functionalities:

- `TOKEN`: GitHub token to increase the GitHub API request limits, useful for developing locally, can be omit when running on GitHub action. It will be something that starts with `Bearer github` followed by a unique sequence of characters. [Check here to learn how to create a GitHub access token for personal use](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

If you want the script to post to your social media on your behalf, you have to set up an API with the social media service and get access tokens or secrets. You will need to set up the the following if you want to:

- **Post to your Twitter/ X account**

  1. If you want to post to your Twitter/ X account, you will have to acquire 2 pairs of keys and secrets. First go to the [developer portal](https://developer.twitter.com/) to sign in and apply for the use of the API. Free tier is good enough for your own use here.

  2. After the app is approved, from your [dashboard](https://developer.x.com/en/portal/dashboard), click on the key icon under your Project App. It should bring you to the "Keys and tokens" page.

  3. There are many get of keys and tokens for different method of authentication. We will use only the "API Key and Secret" under "Consumer Keys" and "Access Token and Secret" under "Authentication Tokens". We will generate a pair of key/ token and secret for each of them and use them to set up the following environment variables:

  - `X_API_KEY`: The API keys from the "API Key and Secret"
  - `X_API_SECRET`: The API secret from the "API Key and Secret"
  - `X_ACCESS_TOKEN`: The access token from the "Access Token and Secret"
  - `X_ACCESS_SECRET`: The access secret from the "Access Token and Secret"

- **Post to your Mastodon account**

  - `MASTODON_TOKEN`: If you want to post to your Mastodon account when there is a new PR/ merged PR, then you have to provide your Mastodon handle in `config.py` and set up a token for access. Log in to your Mastodon account on the web browser and simply go to `https://<your_mastodon_domain>/settings/applications` to create a new application to obtain a Mastodon token. Make sure you have given `write` access to your application.

- **Post to your LinkedIn account**

  - `LINKEDIN_TOKEN`: If you want to post to your LinkedIn account when there is a new PR/ merged PR, then you have to follow the following steps and set up a token for access:

    1. [Create a page](https://www.linkedin.com/company/setup/new/), then [create an app](https://www.linkedin.com/developers/apps) associate with it on LinkedIn
    2. Select your app from the ["My App" page](https://www.linkedin.com/developers/apps) and get your app verified. Then under `Products` tab, request access of `Share on LinkedIn` and `Sign In with LinkedIn using OpenID Connect` under `Available products`.
    3. After getting emails that those are apprived (may take a couple of minutes), use the [LinkedIn Developer Portal Token Generator tool](https://www.linkedin.com/developers/tools/oauth/token-generator) to get a token, make sure all the permissions (email, openid, profile, w_member_social) are selected.
    4. Put your token in the environment variables as `LINKEDIN_TOKEN`.
    5. Please note that your token will expire in 60 days. So you may have to manually generate a new token and update it reguarly.

If you are running it on GitHub action, you will need to set up these variables as secrets. [Learn how to set up secrets in GitHub Action here.](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)

## Schedule running on GitHub action

Other than trigger by a `push` event, the GitHub action workflow is set to run every day at a certain time, the time is set randomly. To set your own time, you can do to the `generate_svg.yml` and chage the `cron` setting. To understand more about how to set the time and the best practice, [please see the guide on GitHub Action here](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule).

For new PR/ merged PR activities, only those which is happening within a day will trigger a post to social media if it has been set up/.

## Extra program needed

If you are developing locally, you will need a few extra program (not in Python) other than Python and the libraries listed at `requirements.txt` to run. They are:

- ImageMagick ([Install instruction](https://imagemagick.org/script/download.php))
- Potrace ([Intall instruction](https://potrace.sourceforge.net/#downloading))

You may want to install them before developing locally. With MacOS, both of them are also available via [Homebrew](https://brew.sh/). With Linux, you may already have ImageMagick, and Potrace is available via `apt get`.

## Advance Usage

For those who would like a "fully hackable" experience, you can work on the source code to modify to your heart content. There are 4 Python scripts in the `src/` directory:

- `main.py`: The entry point of the script, it will use teh GitHub API to make queries to get all the PRs that are relevant.
- `social.py`: The functionalities of posting of social media.
- `svg_gen.py`: Where the svg got generated.
- `validation.py`: Simple validation on setting in `config.yml`

Although you can do anything, I think the following maybe the ones that you want to customise:

- **Changing the post to social media text**: You can do so by looking into `gen_txt` function in `social.py`. The PR title, repo name and the link to the PR is available to use in creating the text.

- **Further customisation of the colours and layout of the svg file**: The style and format of the svg are generate with the code at `svg_gen.py`. You can modify or add any elements in the svg file. Beware that embedded pictures with `<image>` may not work due to the [Content Security Policy (CSP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) of where the final svg file is hosted (e.g. resources hosting provided by GitHub pages). Thus the avatars of the repo owners are not directly embedded as `<image>` but a svg trace is created for embedding into the board.

## Questions or Issues

Questions and suggestions are welcomed! Please [open an issue](https://github.com/Cheukting/pr_showcase_template/issues).

---

Created by [Cheuk](https://github.com/Cheukting) under [MIT license](https://opensource.org/license/mit). Please consider sponsoring Cheuk's work via [GitHub Sponsor](https://github.com/sponsors/Cheukting).
