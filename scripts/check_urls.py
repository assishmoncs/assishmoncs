import urllib.request

urls = [
    "https://raw.githubusercontent.com/assishmoncs/assishmoncs/main/assets/profile-header.svg",
    "https://raw.githubusercontent.com/assishmoncs/assishmoncs/output/github-contribution-grid-snake.svg",
    "https://leetcard.jacoblin.cool/assishmoncs?theme=dark&font=Inter",
    "https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=26&duration=2500&pause=1000&color=58A6FF&center=true&vCenter=true&width=620&lines=Hi+there%2C+I'm+Assish+%F0%9F%91%8B",
    "https://komarev.com/ghpvc/?username=assishmoncs&label=Profile%20Views&color=58a6ff&style=flat-square",
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"OK ({resp.status}): {u[:60]}")
    except Exception as e:
        print(f"FAILED ({e}): {u[:60]}")
