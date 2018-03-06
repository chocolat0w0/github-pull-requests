#!/usr/bin/env python

# use Github GraphQL API.
# need Python 3
# pip install requests

import requests, netrc, subprocess, re
from datetime import datetime as dt

# use Github Application Token
# write Github Application Token in .netrc file
# --------
# .netrc
# machine api.github.com
#    login your_account
#    password your_token
# --------
my_netrc = netrc.netrc()
userid, a, passwd = my_netrc.authenticators('api.github.com')
headers = {"Authorization": "Bearer {}".format(passwd)}

git_origin = subprocess.run('git config --get remote.origin.url', stdout=subprocess.PIPE, shell=True)
git_origin_str = git_origin.stdout.decode('utf-8')
match = list(re.finditer(r'.*:(.*)/(.*)\.git', git_origin_str))[0]
groups = match.groups()
git_owner = groups[0]
git_repository = groups[1]


def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# The GraphQL query
# escape string { } to {{ }}
query = '''
{{
  repository(owner: "{owner}", name: "{repository}") {{
    pullRequests(last: 20, states: OPEN, orderBy: {{field: CREATED_AT, direction: DESC}}) {{
      edges {{
        node {{
          number
          createdAt
          title
          author {{
            login
          }}
          url
          headRefName
        }}
      }}
    }}
  }}
}}
'''.format(owner=git_owner, repository=git_repository)

result = run_query(query)
prs = result['data']['repository']['pullRequests']['edges']

for pr in prs:
    node = pr['node']
    print('{} {} {} {}'.format('{0:4d}'.format(node['number']),
                               dt.strptime(node['createdAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d'),
                               node['author']['login'].ljust(16),
                               node['title']))
