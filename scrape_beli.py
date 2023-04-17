#!/usr/local/bin/python3

URL = "https://beli.cleverapps.io/api/rank-list/f69d5871-2932-4f68-9157-38b9733ff5a9/"
IMAGEURL = "https://beli.cleverapps.io/api/user-business-photo/?user=f69d5871-2932-4f68-9157-38b9733ff5a9&business="
OUTPUT = "food"

regions = [
    ("la", "Los Angeles", 34, -118, 2),
    ("bay", "Bay Area", 37.7, -122.4, 2),
    ("ny", "New York", 40.7, -74, 5),
    ("japan", "Japan", 35.7, 139.7, 10),
    ("other", "Other", 0, 0, 10000),
]

import urllib.request, json, math
from tqdm.contrib.concurrent import process_map

def getImages(r, retries=4):
    try:
        with urllib.request.urlopen(IMAGEURL+str(r["business__id"]), timeout=2) as imageurl:
            imagedata = json.load(imageurl)
        return imagedata["results"]
    except Exception as e:
        if retries > 0:
            return getImages(r, retries-1)
        print("Failed to get photos for " + r["business__name"])
        return []
    # print(r["business__name"])

if __name__ == "__main__":
    with urllib.request.urlopen(URL) as url:
        data = json.load(url)

    data.append({
      "business__id": -1,
      "business__name": "El Primo Tacos",
      "score": 10,
      "business__neighborhood": "Venice",
      "business__city": "Los Angeles, CA",
      "business__lat": 33.99858,
      "business__lng": -118.46253,
      "business__price": 1,
    })

    for i, im in enumerate(process_map(getImages, data, max_workers=50)):
        data[i]["images"] = im

    data.sort(key=lambda r: (-r["score"], r["business__name"]))

    filters = ""
    for name, disp, _, _, _ in regions:
        filters += f"""
<input type="checkbox" name="{name}" id="{name}" checked onclick="setFilter('{name}', this.checked)"/>
<label for="{name}">{disp}</label>
    """

    body = ""
    for i, r in enumerate(data):
        id = r["business__id"]
        lat = float(r["business__lat"])
        lon = float(r["business__lng"])
        region = "Other"
        for name, _, _lat, _lon, radius in regions:
            if math.sqrt((lat - _lat) ** 2 + (lon - _lon) ** 2) < radius:
                region = name
                break
        else:
            assert False

        city = r.get("business__city")
        neighborhood = r.get("business__neighborhood")
        price = r.get("business__price")
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

        body += f"""
<tr class="{region}">
<td style="text-align: right">{i+1}.</td>
<td style="text-align: left; padding-right: 20px">
    <div><a href="https://maps.google.com/maps?q={r["business__name"]}&sll={lat},{lon}&ll={lat},{lon}" target="_blank">{r["business__name"]}</a></div>
    <div style="white-space: pre;">{subtext}</div>
    <div>{images}</div>
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
