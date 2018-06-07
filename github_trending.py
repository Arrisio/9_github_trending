import requests
import datetime as DT
import constants
from urllib.parse import urljoin


def get_trending_repositories(top_size=20):
    repos_url = urljoin(constants.GITHUB_API_URL, constants.REPO_URL_PATH)

    week_ago_date_str = (DT.date.today() - DT.timedelta(days=7)).isoformat()
    request_params = {
        'q': 'created:>{}'.format(week_ago_date_str),
        'sort': 'stars',
        'order': 'desc',
        'per_page': top_size
    }

    request_response = requests.get(url=repos_url, params=request_params)

    if request_response.ok:
        return request_response.json()['items']
    else:
        raise ValueError("Can't get repos list")


def get_open_issues_amount(repo_owner, repo_name):
    issues_url = urljoin(
        constants.GITHUB_API_URL,
        constants.ISSUES_URL_PATH.format(repo_owner, repo_name)
    )

    request_response = requests.get(url=issues_url)
    if request_response.ok:
        return len(request_response.json())
    else:
        raise ValueError("Can't get issues for this repository")


def get_issues_by_list(repos_list):
    for repo in repos_list:
        try:
            repo['issues_cnt'] = get_open_issues_amount(
                repo_owner=repo.get('owner').get('login'),
                repo_name=repo.get('name')
            )
        except ValueError:
            repo['issues_cnt'] = "Unknown"

    return repos_list


def print_repos(repos_list):
    print('Popular projects on Github')
    print('{:^75} | {:^10} | {:^10}'.format('URL', 'STARS', 'ISSUES'))
    print('-' * 115)
    row_template = '{url:<75} | {stars:^10} | {issues:^10}'
    for repo in repos_list:
        print(
            row_template.format(
                url=repo['html_url'],
                stars=repo['stargazers_count'],
                issues=repo['issues_cnt'],
            )
        )


if __name__ == '__main__':
    try:
        repos_list = get_trending_repositories(top_size=20)
    except ValueError as request_error:
        exit(request_error)

    repos_list = get_issues_by_list(repos_list)
    print_repos(repos_list)
