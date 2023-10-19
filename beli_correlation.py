#!/usr/local/bin/python3

import urllib.request, json, math, sys
from tqdm.contrib.concurrent import process_map

def get_user_id(user, retries=4):
    try:
        with urllib.request.urlopen(f"https://beli.cleverapps.io/api/user/member/?&username__iexact={user}", timeout=2) as resp:
            data = json.load(resp)
            assert len(data["results"]) == 1
        return (user, data["results"][0]["id"])
    except Exception as e:
        if retries > 0:
            return get_user_id(user, retries-1)
        print(f"Failed to get user id for {user}: {e}")

def get_corr(id1, id2, retries=4):
    try:
        with urllib.request.urlopen(f"https://beli.cleverapps.io/api/corr/{id1}/{id2}", timeout=2) as resp:
            return (id1, id2, float(resp.read()))
    except Exception as e:
        if retries > 0:
            return get_corr(id1, id2, retries-1)
        print(f"Failed to get corr for ({id1}, {id2}): {e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_names.txt output.html")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        users = f.read().splitlines()
    users.sort()

    user_ids = {}
    for user, id in process_map(get_user_id, users, max_workers=10):
        user_ids[user] = id

    corrs = {}
    pairs = []
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            pairs.append((user_ids[users[i]], user_ids[users[j]]))
    for id1, id2, corr in process_map(get_corr, *zip(*pairs), max_workers=10):
        corrs[(id1, id2)] = corr
        corrs[(id2, id1)] = corr

    print(user_ids)
    print(corrs)

    def user_link(user):
        return f"<a href='https://app.beliapp.com/lists/{user}' target='_blank'>{user}</a>"

    def corr(user1, user2):
        if user1 == user2:
            return "<td>-</td>"
        val = corrs[(user_ids[user1], user_ids[user2])]
        r = 0 if val > 0 else int(-255 * val)
        g = 0 if val < 0 else int(255 * val)
        return f"<td style='background-color: rgb({255 - g}, {255 - r}, {255 - r - g});'>{val:.1%}</td>"

    with open(sys.argv[2], 'w') as out:
        out.write("""
<!doctype html>

<html lang="en">
<head>
<style>
    table, th, td {
        border: 1px solid black;
    }
    td {
        padding: 1em;
    }
    tr:first-child div {
        writing-mode: vertical-rl;
        white-space:nowrap;
        transform:scale(-1);
    }
    body {
        font-family: monospace;
        text-align: center;
    }
</style>
</head>
<body>
<table>
    <tr>
        <td></td>
        """ + "".join(f"<td><div>{user_link(user)}</div></td>" for user in users) + """
    </tr>
    """ + "".join(f"<tr><td>{user_link(user1)}</td>{''.join(corr(user1, user2) for user2 in users)}</tr>" for user1 in users) + """
</table>
</body>
""")
