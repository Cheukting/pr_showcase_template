import requests
import json
import subprocess
import re


def add_bg(colors):
    """Adding a rectangle element as background"""
    if colors["bg_color"] is not None:
        return f'<rect width="100%" height="100%" rx="{colors["bg_r"]}" ry="{colors["bg_r"]}" fill="{colors["bg_color"]}" stroke="transparent" />'
    else:
        return ""


def add_title(colors, length=None):
    """Adding the title if not None. If length is set, the text will be stretched (or compressed) to set length"""
    m = colors["size"]
    fonts = "sans-serif" if colors["fonts"] is None else colors["fonts"]

    if colors["title"] is not None:
        if length is None:
            return f'<text x="{10*m}" y="{30*m}" fill="{colors["pri_color"]}" font-size="{22*m}" font-weight="bold" font-family="{fonts}">{colors["title"]}</text>'
        else:
            return f'<text x="{10*m}" y="{30*m}" fill="{colors["pri_color"]}" font-size="{22*m}" font-weight="bold" font-family="{fonts}" textLength="{length}" lengthAdjust="spacingAndGlyphs">{colors["title"]}</text>'
    else:
        return ""


def produce_avatar(url, id, colors, pos):
    """Download the avatar of the repo owner and calling external program to convert the png file to svg. Then read the svg created and transform it to certain scale and position to get ready for embedding into the board"""
    
    # download the avatar image
    img_data = requests.get(url).content
    with open(f"image/{id}.png", "wb") as handler:
        handler.write(img_data)

    # convert to svg with potrace with subprocess
    size, _ = eval(
        subprocess.check_output(
            ["convert", f"image/{id}.png", "-print", "%w, %h\n", "/dev/null"]
        )
    )
    subprocess.run(
        [
            "convert",
            f"image/{id}.png",
            "-background",
            "White",
            "-alpha",
            "Background",
            f"image/{id}.pnm",
        ]
    )
    subprocess.run(
        [
            "potrace",
            f"image/{id}.pnm",
            "-s",
            "-o",
            f"image/{id}.svg",
            "-C",
            f"{colors["sec_color"]}",
        ]
    )

    # read svg and return path elements
    m = colors["size"]
    with open(f"image/{id}.svg", "r") as handler:
        svg_txt = handler.read()
        elep = re.compile(r"<g [\s\S]+</g>")
        match = re.search(elep, svg_txt).group()
        scale = 30 * m / size
        match = re.sub(
            r"translate\([\s\S][^)]+\)",
            f'translate({pos["x"]},{pos["y"]+scale})',
            match,
        )
        match = re.sub(
            r"scale\([\s\S][^)]+\)", f"scale({.1*scale}, {-0.1*scale})", match
        )
        return match


def gen_full(all_prs, headers, colors):
    """Function to generate the board in the full style"""
    repo_cache = {}
    svgtext = add_bg(colors)
    m = colors["size"]
    t = 0 if colors["title"] is None else 35 * m
    svgtext += add_title(colors)

    fonts = "sans-serif" if colors["fonts"] is None else colors["fonts"]

    for i, pr in enumerate(all_prs):
        url = pr["repository_url"]
        if url not in repo_cache.keys():
            res = requests.get(url, headers=headers)
            res_context = json.loads(res.text)
            repo_cache.update({url: res_context})
        else:
            res_context = repo_cache[url]
        avatar = produce_avatar(
            res_context["owner"]["avatar_url"],
            res_context["owner"]["id"],
            colors,
            {"x": 10 * m, "y": t + (40 + i * 50) * m},
        )
        svgtext += f"""<a href="{res_context["html_url"]}" target="_blank">
        {avatar}
        <text x="{45*m}" y="{t+(20+i*50)*m}" fill="{colors["sec_color"]}" font-size="{15*m}" font-family="{fonts}">{res_context["full_name"]}</text>
      </a>\n<a href="{pr["html_url"]}" target="_blank">
        <text x="{45*m}" y="{t+(40+i*50)*m}" fill="{colors["pri_color"]}" font-size="{18*m}" font-family="{fonts}">{pr["title"]}</text>
      </a>\n"""

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <svg height="{t+(10+len(all_prs)*50)*m}" width="{500*m}" xmlns="http://www.w3.org/2000/svg">
    {svgtext}
    </svg>"""

    return content


def gen_compact(all_prs, headers, user, state, colors):
    """Function to generate the board in the compact style"""
    repo_cache = {}
    svgtext = add_bg(colors)
    m = colors["size"]
    t = 0 if colors["title"] is None else 35 * m

    for i, pr in enumerate(all_prs):
        url = pr["repository_url"]
        if url not in repo_cache.keys():
            res = requests.get(url, headers=headers)
            res_context = json.loads(res.text)
            repo_cache.update({url: {"count": 1, "content": res_context}})

        else:
            repo_cache[url]["count"] += 1

    fonts = "sans-serif" if colors["fonts"] is None else colors["fonts"]

    svgtext += add_title(colors, len(repo_cache) * 100 * m - 20 * m)

    for i, url in enumerate(repo_cache):
        res_context = repo_cache[url]["content"]
        avatar = produce_avatar(
            res_context["owner"]["avatar_url"],
            res_context["owner"]["id"],
            colors,
            {"x": (10 + i * 100) * m, "y": t + 40 * m},
        )
        svgtext += f"""<a href="{res_context["html_url"]}" target="_blank">
        {avatar}</a>
        <a href="{res_context["html_url"]}/pulls?q=author%3A{user}+{f"is%3A{state}" if state in ["open", "closed"] else ""}" target="_blank">
        <text x="{(45+i*100)*m}" y="{t+35*m}" fill="{colors["pri_color"]}" font-size="{20*m}" font-family="{fonts}">{repo_cache[url]["count"]} {"PR" if repo_cache[url]["count"] ==1 else "PRs"}</text>
      </a>\n"""

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <svg height="{t+55*m}" width="{len(repo_cache)*100*m}" xmlns="http://www.w3.org/2000/svg">
    {svgtext}
    </svg>"""

    return content
