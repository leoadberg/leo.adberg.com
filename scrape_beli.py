#!/usr/bin/python3

URL = "https://beli.cleverapps.io/api/rank-list/f69d5871-2932-4f68-9157-38b9733ff5a9/"
OUTPUT = "food"

import urllib.request, json
with urllib.request.urlopen(URL) as url:
    data = json.load(url)

body = ""
for i, r in enumerate(data):
    body += f"""
<tr>
<td style="text-align: right">{i+1}.</td>
<td style="text-align: left; padding-right: 20px">
    <div><a href="https://maps.google.com/maps?q={r["business__name"]}&sll={r["business__lat"]},{r["business__lng"]}&ll={r["business__lat"]},{r["business__lng"]}" target="_blank">{r["business__name"]}</a></div>
    <div>{r["business__neighborhood"]}, {r["business__city"]}</div>
</td>
<td style="">{r["score"]:.1f}</td>
<td style="text-align: right"></td>
</tr>
    """

with open(OUTPUT, 'w') as out:
    out.write("""
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Leo's Restaurant Recommendations</title>
  <meta name="description" content="Leo's Restaurant Recommendations">
  <meta name="author" content="Leo Adberg">

  <style>

  * {
    font-family: HelveticaNeue-Light;
    font-style: normal;
    font-variant-ligatures: normal;
    font-variant-caps: normal;
    font-variant-numeric: normal;
    font-weight: normal;
    font-stretch: normal;
    background-color: #ffffff;
  }
  /* Style the tab */
div.tab {
    overflow: hidden;
    border: 0px;
    text-align: center;
    margin: 0;
    margin-bottom: 30px;
}

/* Style the buttons inside the tab */
div.tab button {
    background-color: inherit;
    color: #a0a0a0;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    transition: 0.3s;
    margin: 0 auto;
    display: inline;
    width: 200px;
    font-size: 16px;
}

/* Change background color of buttons on hover */
div.tab button:hover {
    /*background-color: #ddd;*/
    color: #2e2e2e;
}

svg {
  fill: #000000;
  transition: 0.3s;
}

svg:hover {
  fill: #555555;
  transition: 0.3s;
}

/* Create an active/current tablink class */
div.tab button.active {
    /*background-color: #ccc;*/
    color: #2e2e2e;
}

/* Style the tab content */
.tabcontent {
    display: none;
    padding: 6px 12px;
    border: 0px;
    border-top: none;
    text-align: center;
    margin: 0 auto;
    color: #5e5e5e;
    width: 75%;
}

name {
  font-size: 60px;
}

h {
  font-size: 30px;
}

ti {
  font-size: 20px;
  line-height: 30px;
}

te {
  font-size: 14px;
}

div.copy {
  margin-top: 20px;
  font-size: 12px;
  text-align: center;
  color: #5e5e5e;
}

a {
  color: #222222;
  font-weight: bold;
  text-decoration: none;
}

@media (prefers-color-scheme: dark) {
  * {
    background-color: #222222;
  }
  a {
    color: #ffffff;
  }
  .tabcontent {
    color: #cccccc;
  }
  div.tab button.active {
    color: #ffffff;
  }
  div.tab button:hover {
    color: #ffffff;
  }
  div.tab button {
    color: #a0a0a0;
  }
  svg {
    fill: #aaaaaa;
  }
  svg:hover {
    fill: #ffffff;
  }
  div.copy {
    color: #cccccc;
  }
}

td {
  vertical-align: top;
  padding: 10px;
}

</style>

</head>

<body>
<div id="Home" class="tabcontent" style="display: block;">
  <name>Leo's Restaurant Ratings</name>
  <br>
  <table>
""" + body + """
</table>
</div>
</body>
</html>
""")
# for r in data:
