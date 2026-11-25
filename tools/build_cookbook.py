"""Builds data/cookbook.json (Thali's built-in Cookbook) from tools/cookbook-src.json.
For each ingredient with a fid, the per-100 g values [kcal, protein, carbs, fat, fibre] and the
egg/meat tags are copied from the built-in database files, so the app can compute nutrition offline.
Run from the repository root:  python3 tools/build_cookbook.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db = {}
for key in ('thali', 'indb', 'usda'):
    for r in json.load(open(os.path.join(ROOT, 'data', f'foods-{key}.json'), encoding='utf-8')):
        db[r[0]] = r

src = json.load(open(os.path.join(ROOT, 'tools', 'cookbook-src.json'), encoding='utf-8'))
out, ids = [], set()
for rec in src['recipes']:
    assert rec['id'].startswith('r:cb-'), rec['id']
    assert rec['id'] not in ids, rec['id']
    ids.add(rec['id'])
    ings = []
    for x in rec['ing']:
        y = {'name': x['name'], 'amt': x.get('amt'), 'u': x.get('u', ''), 'g': x['g'], 'fid': x.get('fid', '')}
        if y['fid']:
            r = db.get(y['fid'])
            if not r:
                sys.exit(f"{rec['name']}: unknown food id {y['fid']}")
            y['n'] = r[2:7]
            y['tags'] = r[8] if len(r) > 8 else ''
        else:
            y['n'] = x['n']
            y['tags'] = x.get('tags', '')
        ings.append(y)
    tot = [sum(i['n'][k] * i['g'] / 100 for i in ings) for k in range(5)]
    sv = rec['servings']
    print(f"{rec['name']}: {round(tot[0])} kcal, {round(tot[1])} g protein → per {rec['unit']}: "
          f"{round(tot[0] / sv)} kcal, {round(tot[1] / sv, 1)} g protein")
    out.append({**{k: v for k, v in rec.items() if k != 'ing'}, 'ing': ings})

json.dump({'version': max(r['ts'] for r in src['recipes'])[:10], 'recipes': out},
          open(os.path.join(ROOT, 'data', 'cookbook.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('wrote data/cookbook.json with', len(out), 'recipes')
