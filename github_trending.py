import requests
import datetime


def get_repos_url():
    return 'https://api.github.com/search/repositories'


def get_issues_url(repo_owner, repo_name):
    return 'https://api.github.com/repos/{}/{}/issues'.format(
        repo_owner, repo_name
    )


def get_trending_repositories(top_size=20):
    repos_url = get_repos_url()

    week_ago_date_str = (
            datetime.date.today() - datetime.timedelta(days=7)
    ).isoformat()
    request_params = {
        'q': 'created:>{}'.format(week_ago_date_str),
        'sort': 'stars',
        'order': 'desc',
        'per_page': top_size
    }

    response = requests.get(url=repos_url, params=request_params)
    if response.ok:
        return response.json().get('items')


def get_open_issues_amount(repo_owner, repo_name):
    issues_url = get_issues_url(repo_owner, repo_name)

    response = requests.get(url=issues_url)
    if response.ok:
        return len(response.json())


def get_issues_by_list(repos_list):
    for repo in repos_list:
        repo['issues_count'] = get_open_issues_amount(
            repo_owner=repo.get('owner').get('login'),
            repo_name=repo.get('name')
        )

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
                issues=repo['issues_count'] or 'Unknown',
            )
        )


if __name__ == '__main__':
    repos_list = get_trending_repositories(top_size=20)
    if not repos_list:
        exit("Can't get repos list")

    repos_list = get_issues_by_list(repos_list)
    print_repos(repos_list)
