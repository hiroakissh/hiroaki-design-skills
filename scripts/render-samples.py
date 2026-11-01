#!/usr/bin/env python3
"""Build standalone HTML from authored examples; this does not interpret SKILL.md."""

import argparse
import json
import re
from html import escape
from design_tokens import ROOT, css, load


def text(value):
    return escape(str(value), quote=True)


def substitutions(name, data, catalog):
    values = {"skill_count": str(len(catalog["skills"]))}
    if name == "hiro-design-app":
        cards = []
        for project in data["projects"]:
            title, detail, progress = (text(project[key]) for key in ("name", "detail", "progress"))
            cards.append('<li><button class="project-choice" data-project-tasks="'+text(json.dumps(project["tasks"], ensure_ascii=False))+'" data-project-name="'+title+'" data-project-detail="'+detail+'" data-project-progress="'+progress+'"><strong>'+title+'</strong><small>'+detail+'</small><span class="row"><span class="progress" aria-hidden="true"><span style="width:'+progress+'%"></span></span><small class="number">'+progress+'%</small></span></button></li>')
        values["project_cards"] = "\n".join(cards)
        values["task_rows"] = "".join('<li><label><input type="checkbox">'+text(task)+'</label></li>' for task in data["next"])
        values.update({"first_"+key: text(data["projects"][0][source]) for key, source in (("name","name"),("detail","detail"),("progress","progress"))})
    elif name == "hiro-design-webapp":
        rows = []
        for project in data["projects"]:
            title, category, status, progress = (text(project[key]) for key in ("name", "category", "status", "progress"))
            rows.append('<tr data-name="'+title+'" data-status="'+status+'"><td><label><input type="checkbox" aria-label="'+title+'を選択">'+title+'</label></td><td>'+category+'</td><td><span class="status" data-status="'+status+'">'+status+'</span></td><td class="num"><span class="row"><span class="progress" aria-hidden="true"><span style="width:'+progress+'%"></span></span><span>'+progress+'%</span></span></td></tr>')
        values["table_rows"] = "\n".join(rows)
        values["project_count"] = str(len(data["projects"]))
        values["active_count"] = str(sum(project["status"] == "進行中" for project in data["projects"]))
        values["review_count"] = str(sum(project["status"] == "確認待ち" for project in data["projects"]))
    elif name == "hiro-design-report":
        bars, rows = [], []
        for index, item in enumerate(data["alternatives"]):
            y = 29 + index * 53
            percent = item["completion"]
            bars.append('<text x="0" y="'+str(y+15)+'">'+text(item["name"])+'</text><rect class="bar-track" x="60" y="'+str(y)+'" width="220" height="22" rx="3"/><rect class="'+('bar-main' if index==0 else 'bar-other')+'" x="60" y="'+str(y)+'" width="'+str(220*percent/100)+'" height="22" rx="3"/><text x="350" y="'+str(y+15)+'" text-anchor="end">'+str(percent)+'%</text>')
            rows.append('<tr><td>'+text(item["name"])+'</td><td class="num">'+str(percent)+'%</td><td class="num">'+str(item["seconds"])+'秒</td></tr>')
        values.update({key:text(data[key]) for key in ("title","subtitle","source")})
        values.update(chart_bars="\n".join(bars), comparison_rows="\n".join(rows))
    elif name == "hiro-design-website":
        values["skill_links"] = "\n".join('<a class="skill-link" href="../'+skill["name"]+'/index.html"><h3>'+text(skill["title"])+'</h3><p>'+text(skill["summary"])+'</p></a>' for skill in catalog["skills"])
    return values


def page(title, body, styles, script, kind="gallery"):
    initial_theme = "document.documentElement.dataset.theme=new URLSearchParams(location.search).get('theme')==='dark'?'dark':'light';"
    footer = 'サンプルは用途ごとの適用例です。成果物の形式と確認範囲は各確認記録をご覧ください。' if kind=='gallery' else '<a href="brief.md">固定依頼文</a> / <a href="review.md">確認記録</a> / <a href="../index.html">サンプル一覧</a>'
    return '<!doctype html>\n<html lang="ja" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+text(title)+' — Hiroaki Design Skills</title><script>'+initial_theme+'</script><style>\n'+styles+'\n</style></head><body data-sample="'+text(kind)+'"><a class="skip-link" href="#main">本文へ移動</a><header class="sample-bar"><div><strong>'+text(title)+'</strong><p>Atmospheric Graphite v1.0 / Light・Darkの実装例</p></div><div class="theme-controls" role="group" aria-label="配色モード"><button data-set-theme="light" aria-pressed="true">Light</button><button data-set-theme="dark" aria-pressed="false">Dark</button></div></header><main id="main" class="sample-main">'+body+'</main><footer class="sample-footer">'+footer+'</footer><script>\n'+script+'\n</script></body></html>\n'


def expected_files(root=ROOT):
    catalog = json.loads((root / "source/catalog.json").read_text(encoding="utf-8"))
    styles = css(load(root)) + (root / "samples/shared/sample.css").read_text(encoding="utf-8")
    script = (root / "samples/shared/sample.js").read_text(encoding="utf-8")
    outputs, cards = {}, []
    for skill in catalog["skills"]:
        name = skill["name"]
        folder = root / "samples" / name
        data = json.loads((folder / "data.json").read_text(encoding="utf-8")) if (folder / "data.json").exists() else {}
        body = (folder / "template.html").read_text(encoding="utf-8")
        for key, value in substitutions(name, data, catalog).items():
            body = body.replace("{{"+key+"}}", value)
        if re.search(r"\{\{[a-z_]+\}\}", body):
            raise ValueError("Unresolved template field in " + name)
        local_styles = (folder / "sample.css").read_text(encoding="utf-8") if (folder / "sample.css").exists() else ""
        local_script = (folder / "sample.js").read_text(encoding="utf-8") if (folder / "sample.js").exists() else ""
        outputs["samples/"+name+"/index.html"] = page(skill["title"]+" / サンプル", body, styles+local_styles, script+("\n"+local_script if local_script else ""), name)
        cards.append('<article class="gallery-card"><a href="'+name+'/index.html"><img src="'+name+'/preview-light.jpg" alt="'+text(skill["title"])+'のLight表示" loading="lazy"><h2>'+text(skill["title"])+'</h2></a><p class="muted" style="font-size:14px;margin:10px 0">'+text(skill["summary"])+'</p><div class="row"><a href="'+name+'/index.html?theme=light">Lightで開く</a><a href="'+name+'/index.html?theme=dark">Darkで開く</a></div></article>')
    gallery = '<div class="page-heading"><div><p class="section-label">用途から、実際の表示を見る</p><h1>Hiroaki Design Skills</h1><p>共通の配色と、それぞれに合う情報の形。</p></div><span class="brand-tag">'+str(len(catalog["skills"]))+' skills</span></div><div class="gallery-grid">'+"\n".join(cards)+'</div>'
    outputs["samples/index.html"] = page("サンプル一覧", gallery, styles, script)
    return outputs


def build(check=False, root=ROOT):
    stale = []
    for name, content in expected_files(root).items():
        path = root / name
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            stale.append(name)
            if not check:
                path.write_text(content, encoding="utf-8")
    return stale


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = build(args.check)
    if args.check and stale:
        raise SystemExit("Sample HTML is stale:\n" + "\n".join(stale))
    print("Sample HTML is current." if args.check else "Built {} standalone HTML samples and their gallery. Capture both theme previews after inspection.".format(len(expected_files())-1))
