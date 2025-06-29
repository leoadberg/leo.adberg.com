#!/usr/bin/python3 
USER = "f69d5871-2932-4f68-9157-38b9733ff5a9"
API = "https://backoffice-service-t57o3dxfca-nn.a.run.app/api"
TOKEN       = f"{API}/token/refresh/"
RESTAURANTS = f"{API}/get-ranking/?user={USER}&category=RES"
NOTES       = f"{API}/datauserbusinesstext-sparse/?field__name=NOTES&user={USER}"
IMAGEURL    = f"{API}/user-business-photo/?user={USER}&business="
OUTPUT = "food"

regions = [
    ("la", "Los Angeles", 34, -118, 2),
    ("bay", "Bay Area", 37.7, -122.4, 2),
    ("ny", "New York", 40.7, -74, 5),
    ("japan", "Japan", 35.7, 139.7, 10),
    ("london", "London", 51, 0, 2),
    ("paris", "Paris", 49, 2, 2),
    ("singapore", "Singapore", 1, 104, 2),
    ("georgia", "Georgia", 42, 44, 4),
    ("other", "Other", 0, 0, 10000),
]

import urllib.request, json, math, os
from tqdm.contrib.concurrent import process_map

assert "BELI_AUTH" in os.environ

def get_token():
    req = urllib.request.Request(TOKEN)
    req.add_header("content-type", "application/json")
    req.data = bytes('{"refresh": "' + os.environ["BELI_AUTH"] + '"}', encoding='utf8')
    with urllib.request.urlopen(req, timeout=4) as res:
        return json.load(res)["access"]


def get(url, token, retries=1):
    try:
        req = urllib.request.Request(url)
        req.add_header("authorization", "Bearer " + token)
        with urllib.request.urlopen(req, timeout=4) as res:
            return json.load(res)
    except Exception as e:
        if retries > 0:
            return get(url, retries-1)
        print(f"Failed to get {url=}")
        raise


def getImages(tup, retries=4):
    r, token = tup
    try:
        id = r["business"]["id"]
        return get(IMAGEURL+str(id), token)["results"]
    except Exception as e:
        if retries > 0:
            return getImages(r, retries-1)
        print(f"Failed to get photos for {r=}")
        return []

if __name__ == "__main__":
    token = get_token()
    data = get(RESTAURANTS, token)["results"]

    notes = get(NOTES, token)
    notes = notes["results"]
    notesmap = {}
    for item in notes:
        if item["user"] == USER:
            notesmap[item["business"]] = item["value"]

    for item in data:
        business_id = item["business"]["id"]
        if business_id in notesmap:
            item["notes"] = notesmap[business_id]

    for i, im in enumerate(process_map(getImages, [(r, token) for r in data], max_workers=50)):
        data[i]["images"] = im

    data.sort(key=lambda r: (-r["score"], r["business"]["name"]))

    filters = ""
    for name, disp, _, _, _ in regions:
        filters += f"""
<input type="checkbox" name="{name}" id="{name}" checked onclick="setFilter('{name}', this.checked)"/>
<label for="{name}">{disp}</label>
    """

    body = ""
    for i, r in enumerate(data):
        b = r["business"]
        id = b["id"]
        lat = float(b["lat"])
        lon = float(b["lng"])
        region = "Other"
        for name, _, _lat, _lon, radius in regions:
            if math.sqrt((lat - _lat) ** 2 + (lon - _lon) ** 2) < radius:
                region = name
                break
        else:
            assert False

        city = b["city"]
        neighborhood = b["neighborhood"]
        price = b["price"]
        subtext = city
        if neighborhood is not None:
            subtext = neighborhood + ", " + subtext
        if price is not None:
            subtext = "$" * price + "  |  " + subtext

        images = ""
        for j, im in enumerate(r.get("images", [])):
            if j != 0:
                images += ", "
            images += f"""<a target="_blank" class="photo" href="{im["image"]}">{im["description"]}</a>"""

        score = r["score"]
        color = "good"
        if score < 6.7:
            color = "fine"
        if score < 3.5:
            color = "bad"

        note = ""
        if "notes" in r:
            note = f"""<div class="note">"{r["notes"]}"</div>"""

        body += f"""
<tr class="{region}">
<td style="text-align: right">{i+1}.</td>
<td style="text-align: left; padding-right: 20px">
    <div><a href="https://maps.google.com/maps?q={b["name"]}&sll={lat},{lon}&ll={lat},{lon}" target="_blank">{b["name"]}</a></div>
    <div style="white-space: pre;">{subtext}</div>
    <div>{images}</div>
    {note}
</td>
<td class="{color}">{score:.1f}</td>
<td style="text-align: right"></td>
</tr>
        """

    with open(OUTPUT, 'w') as out:
        out.write("""
<!doctype html>

<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-TMCQ9H77TR"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-TMCQ9H77TR');
  </script>

  <meta charset="utf-8">

  <title>Leo's Restaurant Reviews</title>
  <meta name="description" content="Leo's Restaurant Reviews">
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
}

a:not(.photo) {
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

.good {
  color: #45cc18;
}

.fine {
  color: #e2cc25;
}

.bad {
  color: #e22525;
}

.note {
  font-style: italic;
  padding-top: 0.5em;
}

</style>

</head>

<body>
    <div id="Home" class="tabcontent" style="display: block;">
        <name>Leo's Restaurant Ratings</name>
        <br>
        <table>
            <tr><td colspan="4">
                """ + filters + """
            </td></tr>
            """ + body + """
            <tr><td></td><td><div style="text-align: left">
            Legend:
            <p class="good">Would go again of my own accord</p>
            <p class="fine">Might go again if someone else wanted to go</p>
            <p class="bad">Would refuse to go again</p>
            </div></td></tr>
        </table>
    </div>
</body>

<script>
function setFilter(name, checked) {
    document.querySelectorAll('.' + name).forEach(function(e) {
        e.hidden = !checked;
    });
}

if (window.location.hash.length > 1) {
    for (const name of """ + str([r[0] for r in regions]) + """) {
        const e = document.getElementById(name)
        e.checked = "#" + name == window.location.hash
        e.onclick()
    }
}
</script>
</html>
""")
# for r in data:
