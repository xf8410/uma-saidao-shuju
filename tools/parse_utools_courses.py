#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse U-tools (ウマ娘.攻略.tools) /race/courses/<id> pages into structured course geometry data.

Source: https://ウマ娘.攻略.tools/race/courses/<course_id>  (140 pages fetched 2026-09-11)
Usage:  python3 parse_utools_courses.py <html_dir> <out_json>
"""
import re, json, glob, os, sys


def strip_noise(html):
    html = html.replace('<!-- -->', '')
    html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.S)
    html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.S)
    return html


def textof(seg):
    t = re.sub(r'<[^>]+>', '', seg)
    return re.sub(r'\s+', '', t)


def label_pairs(seg):
    """Extract (label, body) pairs from labelLine components."""
    out = []
    for m in re.finditer(
        r'labelLine_component_labelLine__label__\w+">(.*?)</div><div class="labelLine_component_labelLine__body__\w+">(.*?)</div>',
        seg, flags=re.S):
        out.append((textof(m.group(1)), textof(m.group(2))))
    return out


def split_range(s):
    m = re.match(r'(\d[\d,]*)m\s*~\s*(\d[\d,]*)m', s.replace(',', ''))
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def parse_file(path):
    cid = os.path.basename(path).replace('.html', '')
    raw = open(path, encoding='utf-8').read()
    t = re.search(r'<title>(.*?)</title>', raw, flags=re.S)
    title = t.group(1).split(' | ')[0].strip() if t else ''
    body = strip_noise(raw)

    data = {"course_id": int(cid), "title": title, "segments": [], "phases": [],
            "keep_zone": None, "races": [], "basic": {}}

    heads = [(m.start(), textof(m.group(1))) for m in re.finditer(
        r'headlineLight_component_headlineLight__text__\w+">(.*?)</h2>', body, flags=re.S)]
    for i, (pos, name) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(body)
        seg = body[pos:end]
        pairs = label_pairs(seg)
        if name == '基本データ':
            for k, v in pairs:
                data['basic'][k] = v
        elif name == 'コース構成':
            for k, v in pairs:
                r = split_range(v)
                if r:
                    data['segments'].append({"name": k, "from_m": r[0], "to_m": r[1]})
        elif name in ('フェーズ', 'ポジショニング', '展開'):
            for k, v in pairs:
                r = split_range(v)
                if r:
                    data['phases'].append({"name": k, "from_m": r[0], "to_m": r[1]})
        else:
            for k, v in pairs:
                if 'キープ' in k:
                    data['keep_zone'] = v

    for m in re.finditer(
        r'raceDetailItem_component_raceDetailItem__h2c7F" href="/race/races/(\d+)">.*?img alt="(.*?)" '
        r'loading.*?__distance__\w+">(.*?)</div><div class="raceDetailItem_component_raceDetailItem__grade__\w+[^"]*">(.*?)</div>'
        r'.*?__fan__\w+"><span>([\d,]+)</span>.*?__ground__\w+[^"]*">(.*?)</div>',
        body, flags=re.S):
        rid, name, dist, grade, fans, ground = m.groups()
        data['races'].append({
            "race_id": int(rid), "name": name.strip(),
            "distance": textof(dist), "grade": textof(grade),
            "fans": int(fans.replace(',', '')), "ground": textof(ground),
        })

    b = data['basic']
    m = re.match(r'([\d,]+)m（(.*?)）', b.get('距離', '').replace(',', ''))
    if m:
        data['distance_m'] = int(m.group(1))
        data['distance_class'] = m.group(2)
    data['venue'] = b.get('レース場', '')
    data['surface'] = b.get('コース', '')
    data['rotation'] = b.get('周回', '')
    data['bonus'] = b.get('補正ステータス', '')
    return data


def main():
    html_dir = sys.argv[1] if len(sys.argv) > 1 else '/tmp/courses'
    out_json = sys.argv[2] if len(sys.argv) > 2 else '/tmp/parsed_courses.json'
    results = []
    for path in sorted(glob.glob(os.path.join(html_dir, '*.html')),
                       key=lambda p: int(os.path.basename(p).split('.')[0]) if os.path.basename(p).split('.')[0].isdigit() else 0):
        try:
            results.append(parse_file(path))
        except Exception as e:
            print(f"PARSE FAIL {path}: {e}")
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    race_ids = sorted({r['race_id'] for c in results for r in c['races']})
    with open(os.path.join(os.path.dirname(out_json), 'race_ids.txt'), 'w') as f:
        f.write('\n'.join(map(str, race_ids)))
    print(f"parsed {len(results)} courses, {len(race_ids)} unique races")
    s = results[0]
    print(json.dumps({k: s[k] for k in ('course_id', 'title', 'venue', 'distance_m', 'distance_class', 'surface', 'rotation', 'segments', 'phases', 'keep_zone')}, ensure_ascii=False)[:700])
    print('races sample:', json.dumps(s['races'][:2], ensure_ascii=False))


if __name__ == '__main__':
    main()
