#!/usr/bin/env python3
"""
_data/profile.yml 을 읽어 GitHub 프로필 README(donggyu-kang/donggyu-kang)를 생성한다.

  python bin/build-profile-readme.py            # 표준 출력
  python bin/build-profile-readme.py out/README.md

이력서(resume.html)와 같은 데이터를 쓰되, 프로필에는 요약본(summary / profile_tech)만 싣는다.
"""
import sys
import urllib.parse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data" / "profile.yml"


def badge(label, color, logo, logo_color, style="flat-square", href=None):
    text = urllib.parse.quote(label).replace("-", "--").replace("_", "__")
    url = f"https://img.shields.io/badge/{text}-{color}?style={style}&logo={logo}&logoColor={logo_color}"
    img = f'<img src="{url}" />'
    return f'<a href="{href}">{img}</a>' if href else img


def render(d):
    c = d["contacts"]
    blog = c["blog"].rstrip("/")
    out = []
    w = out.append

    # ── 헤더 배너 (assets/header.svg 는 프로필 레포에서 직접 관리) ──
    w(f'<a href="{c["github"]}"><img src="./assets/header.svg" width="100%" '
      f'alt="{d["name_en"]} — {d["role"]}" /></a>')
    w("")
    w('<div align="center">')
    w("")
    w(f'[![Resume](https://img.shields.io/badge/%EC%9D%B4%EB%A0%A5%EC%84%9C-10B981?style=for-the-badge&logo=readdotcv&logoColor=white)]({blog}/resume)')
    w(f'[![Blog](https://img.shields.io/badge/Tech%20Blog-0f172a?style=for-the-badge&logo=github&logoColor=white)]({blog})')
    w(f'[![Email](https://img.shields.io/badge/{urllib.parse.quote(c["email"])}-0f172a?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{c["email"]})')
    w("")
    w("</div>")
    w("")
    w("<br>")
    w("")

    # ── About ──
    w("## About Me")
    w("")
    w(d["about"]["profile_lead"])
    w(d["about"]["profile_sub"])
    w("")
    for h in d["highlights"]:
        w(f'- **{h["title"]}** — {h["body"]}')
    w("")
    w("<br>")
    w("")

    # ── Tech Stack ──
    w("## Tech Stack")
    w("")
    w("<table>")
    for row in d["skills"]:
        if not row.get("badges"):
            continue
        w("  <tr>")
        w(f'    <th align="left" width="150">{row["label"]}</th>')
        w("    <td>")
        for b in row["badges"]:
            w(f"      {badge(*b)}")
        w("    </td>")
        w("  </tr>")
    w("</table>")
    w("")
    w("<br>")
    w("")

    # ── Projects (표) ──
    w("## Projects")
    w("")
    w("| 프로젝트 | 소개 | 기술 |")
    w("|:--|:--|:--|")
    for p in d["projects"]:
        cell = f'**[{p["name"]}]({p["url"]})**'
        if p.get("award"):
            cell += f'<br><sub>{p["award"].split(" — ")[0]}</sub>'
        elif p.get("status") == "wip":
            cell += "<br><sub>진행 중</sub>"
        tech = " ".join(f"`{t}`" for t in p["profile_tech"])
        w(f'| {cell} | {p["oneline"]} | {tech} |')
    w("")
    w(f'<sub>각 프로젝트에서 무엇을 어떻게 했는지는 '
      f'<a href="{blog}/resume">이력서</a>에 자세히 정리해 두었습니다.</sub>')
    w("")
    w("<br>")
    w("")

    # ── Awards & Certifications ──
    w("## Awards & Certifications")
    w("")
    w("| 구분 | 내용 | 기관 | 일자 |")
    w("|:--|:--|:--|:--|")
    for a in d["awards"]:
        w(f'| 수상 | TABA 10기 프로젝트 **{a["title"].replace("프로젝트 ", "")}** | {a["short_org"]} | {a["period"]} |')
    for ct in d["certifications"]:
        w(f'| 자격증 | **{ct["name"]}** | {ct["org"]} | {ct["period"]} |')
    w("")
    w("<br>")
    w("")
    w('<div align="center">')
    w(f'  <sub>더 자세한 내용은 <a href="{blog}/resume">이력서</a>에 정리해 두었습니다. '
      f'궁금한 점은 <a href="mailto:{c["email"]}">메일</a> 주세요.</sub>')
    w("</div>")
    w("")
    w("<!-- 이 파일은 donggyu-kang.github.io/_data/profile.yml 에서 자동 생성됩니다. 직접 수정하지 마세요. -->")

    return "\n".join(out) + "\n"


def main():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    text = render(data)
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path} ({len(text)} bytes)")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
