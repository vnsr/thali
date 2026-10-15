"""Builds Thali's offline food database files from:
 - curated.txt (Thali curated list)
 - INDB (Indian Nutrient Databank, Jaacks et al. 2024) – filtered for implausible values
 - USDA SR Legacy (via tempo-food-db, public-domain USDA rows only)
Output: data/foods-thali.json, data/foods-indb.json, data/foods-usda.json, data/db-version.json
Row format: [id, name, kcal, protein, carbs, fat, fibre, portions, tags, aliases, category]
"""
import csv, json, re, sys, datetime, openpyxl, unicodedata

OUT = sys.argv[1]
DBV = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat()

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:40]

def r2(x):
    if x is None: return None
    x = float(x)
    return round(x, 2) if x < 10 else round(x, 1) if x < 100 else round(x)

def r1(x):
    x = float(x or 0)
    return round(x, 1) if x < 100 else round(x)

NV = re.compile(r'\b(chicken|mutton|lamb|fish|prawn|shrimp|keema|meat|beef|pork|crab|mackerel|sardine|tuna|salmon|liver|goat|kheema|murgh|gosht|machli|machchi|bacon|ham|turkey|duck|squid|lobster|anchov|veal|venison|sausage|salami|pepperoni|frankfurter|bologna|chorizo|gelatin)', re.I)
EGG = re.compile(r'\b(egg|eggs|anda|omelette|omelet)\b', re.I)

# ---------- curated ----------
MIC={}
for line in open('/home/claude/build/curated-micros.txt',encoding='utf-8'):
    if line.startswith('#') or '|' not in line: continue
    nm,v=line.rstrip('\n').split('|');MIC[nm.strip()]=[float(x) for x in v.split()]
rows, ids, cat = [], set(), ''
for line in open('/home/claude/build/curated.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if not line.strip():
        continue
    if line.startswith('#'):
        t = line[1:].strip()
        if not t.startswith('Thali') and not t.startswith('name'):
            cat = t
        continue
    parts = [p.strip() for p in line.split('|')]
    name, nums, portions, tags, aliases = parts[0], parts[1], parts[2], parts[3], parts[4]
    k, p, c, f, fi = [float(x) for x in nums.split()]
    calc = 4 * c + 4 * p + 9 * f + 2 * fi
    if k > 30 and abs(calc - k) / k > 0.22 and 'beer' not in name.lower() and 'wine' not in name.lower() and 'whisky' not in name.lower() and 'prosecco' not in name.lower() and 'bier' not in name.lower():
        print('CHECK curated energy', name, k, round(calc), file=sys.stderr)
    fid = 't:' + slug(name)
    assert fid not in ids, fid
    ids.add(fid)
    ps = []
    for seg in portions.split(';'):
        if not seg.strip():
            continue
        lab, g = seg.rsplit('=', 1)
        ps.append([lab.strip(), float(g)])
    assert name in MIC, 'no micros for '+name
    rows.append([fid, name, r1(k), r1(p), r1(c), r1(f), r1(fi), ps, tags, aliases, cat, MIC[name]])
json.dump(rows, open(f'{OUT}/foods-thali.json', 'w'), ensure_ascii=False, separators=(',', ':'))
n_thali = len(rows)

# ---------- INDB ----------
wb = openpyxl.load_workbook('/home/claude/data/indb/repo/INDB.xlsx', read_only=True)
ws = wb.worksheets[0]
it = ws.iter_rows(values_only=True)
h = next(it)
I = {k: i for i, k in enumerate(h)}
SWEETDRY = re.compile(r'(burfi|barfi|ladoo|laddu|chikki|halwa|namak para|mathri|murukku|chakli|chivda|chiwda|nuts|sev\b|biscuit|cookie|cake|toffee|fudge|chocolate|peanut|sesame|til|coconut|panjiri|pinni|gajak)', re.I)
indb, drop = [], []
for r in it:
    code, name = r[I['food_code']], (r[I['food_name']] or '').strip()
    if not code or not name:
        continue
    k = r[I['energy_kcal']] or 0
    p, c, f, fi = (r[I[x]] or 0 for x in ('protein_g', 'carb_g', 'fat_g', 'fibre_g'))
    calc = 4 * c + 4 * p + 9 * f + 2 * fi
    reason = None
    if k <= 0: reason = 'no energy'
    elif f > 35 and not SWEETDRY.search(name): reason = 'frying oil overcounted'
    elif k > 560: reason = 'implausible energy'
    elif abs(calc - k) / k > 0.2 and k > 40: reason = 'energy mismatch'
    if reason:
        drop.append((code, name, round(k), round(f), reason))
        continue
    ps = []
    unit = (r[I['servings_unit']] or '').strip()
    sk = r[I['unit_serving_energy_kcal']] or 0
    g = sk / k * 100 if k else 0
    if unit and 15 <= g <= 600:
        ps.append(['1 ' + unit, round(g)])
    tags = 'n' if NV.search(name) else ('e' if EGG.search(name) and 'eggless' not in name.lower() and 'vegetarian' not in name.lower() else '')
    mic=[r2(r[I['calcium_mg']]), r2(r[I['iron_mg']]), None, None]  # IFCT vitamin D values for plant foods are implausible; B12 not in INDB
    indb.append(['i:' + code, re.sub(r'\s+', ' ', name), r1(k), r1(p), r1(c), r1(f), r1(fi), ps, tags, '', 'Indian dishes (INDB)', mic])
json.dump(indb, open(f'{OUT}/foods-indb.json', 'w'), ensure_ascii=False, separators=(',', ':'))
with open('/home/claude/build/indb-dropped.csv', 'w') as fh:
    csv.writer(fh).writerows([('code', 'name', 'kcal', 'fat', 'reason')] + drop)

# ---------- USDA SR Legacy ----------
CAT = {'Liha ja linnuliha': 'Meat & poultry', 'Köögivili': 'Vegetables', 'Leivad ja pagarittooted': 'Bread & bakery',
       'Valmistoidud': 'Prepared foods', 'Puuviljad ja marjad': 'Fruit & berries', 'Magustoidud ja küpsetised': 'Sweets & baked goods',
       'Joogid': 'Drinks', 'Piimatooted': 'Dairy', 'Kaunviljad': 'Legumes', 'Kala ja mereannid': 'Fish & seafood',
       'Rasvad ja õlid': 'Fats & oils', 'Hommikusöögid': 'Breakfast cereals', 'Teravili ja pasta': 'Grains & pasta',
       'Pähklid ja seemned': 'Nuts & seeds', 'Supid': 'Soups', 'Snäkid ja suupisted': 'Snacks', 'Kartulid ja mugulad': 'Potatoes & tubers',
       'Kastmed ja maitsed': 'Sauces & condiments', 'Vürtsid ja maitseained': 'Spices & herbs', 'Munad': 'Eggs', 'Salatid': 'Salads'}
usda = []
UM = json.load(open('/home/claude/build/usda-micros.json'))
for x in csv.DictReader(open('/home/claude/data/tempo/package/data/tempolife-foods.csv', encoding='utf-8')):
    if x['source'] != 'usda_sr_legacy':
        continue
    k = float(x['calories'] or 0)
    cat = CAT.get(x['category'], 'Other')
    name = x['name'].strip()
    tags = 'n' if cat in ('Meat & poultry', 'Fish & seafood') or NV.search(name) else ('e' if cat == 'Eggs' else '')
    um = UM.get('u:' + x['id'])
    usda.append(['u:' + x['id'], name, r1(k), r1(x['protein']), r1(x['carbs']), r1(x['fat']), r1(x['fiber']), [], tags, '', cat, [r2(v) for v in um] if um else None])
json.dump(usda, open(f'{OUT}/foods-usda.json', 'w'), ensure_ascii=False, separators=(',', ':'))

json.dump({'version': DBV, 'counts': {'thali': n_thali, 'indb': len(indb), 'usda': len(usda)}},
          open(f'{OUT}/db-version.json', 'w'))
print('thali', n_thali, 'indb', len(indb), 'dropped', len(drop), 'usda', len(usda))
