# Thali – private calorie & macro log (offline PWA)

Log food, calories, protein, carbs, fat and fibre, plus water and weight. Includes Indian and international foods.
Your log stays on the phone. Nothing is sent anywhere unless you turn on automatic sync, which goes to your own private GitHub repository.

## Install (once)
1. This repository (`vnsr/thali`) is public, but your food log never goes into it.
2. Repo → **Settings → Pages** → Source: "Deploy from a branch", branch `main`, folder `/ (root)` → Save.
3. After about a minute, open **https://vnsr.github.io/thali/** in **Safari** on the iPhone.
4. Share button → **Add to Home Screen**. Always open Thali from that icon. The home-screen app keeps its own data, separate from Safari.
5. Open it once while online, wait about 10 seconds so the food database and barcode reader (about 2 MB) are saved, and close it. After that it works in airplane mode.
6. Repeat on your partner's iPhone. To keep both phones in step, set up sync first (see below).

## First start
- **Phone 1:** Set up my profile → name, sex, birth year, height, weight, activity, goal. The app calculates the targets (see "Targets" below).
- **Phone 2:** tap "Already use Thali on another phone? Turn on sync first", connect sync, and the existing profiles arrive. Then tap the name at the top → **+ Add profile** for the second person → select it with "On this phone".
- Each phone shows one profile at a time (tap the name at the top to switch). Your own foods, recipes and scanned products are shared by everyone.

## Logging
- **+ (Add)** or the + on a meal → search → pick → choose a portion (1 roti, 1 katori, 1 Brötchen, grams…) → Add. The sheet stays open, so you can add a whole meal; tap Done.
- Search understands English, Hindi/Gujarati and German words: *aloo, bataka, dahi, rotli, chawal, Käse, Haferflocken, Brötchen…*
- **Recent** shows what you usually have at that meal, with the portion you used last time. **☆** keeps a food in Favourites.
- **Same as yesterday** on an empty meal copies yesterday's breakfast/lunch/etc.
- **Not found?** Closest matches appear, Open Food Facts is searched automatically, and **Estimate from ingredients** builds it from parts (e.g. milk + matcha + sugar) and saves it for next time.
- **Quick add** is for a number only (restaurant meal, office cake).
- Tap any entry to change the amount, the meal or the day, or to delete it (Undo appears for 5 s).
- Water: tap + for each glass. Tap the amount on the Water card to change the daily target and glass size. Weight: "Log weight" on Today.

## Barcode scanning
Tap the barcode icon in search (or Foods → My foods → Scan barcode). Point the camera at the barcode.
If the live camera doesn't work, use **Take a photo** or **Type the number**.
The product is looked up at Open Food Facts and saved on the phone (and synced), so the next scan works offline.
If a product is missing, the app opens "New food" with the barcode filled in. Copy the values from the label
(Brennwert kcal, Eiweiß, Kohlenhydrate, Fett, Ballaststoffe), and the next scan will find it.

## Recipes
Foods → Recipes → + New recipe. Add each ingredient with its **raw** weight (dal, oil, ghee, onion…). Then enter
the **cooked weight** (weigh the pot after cooking, minus the pot) and the number of portions. Thali works out kcal and
macros per portion and per 100 g. To log it, search its name and pick "1 portion", "1 katori", or grams.

## Shopping list & pantry (v1.1)
The **Shop** tab is shared by both phones (not per profile).
- **Shopping list:** type `2 Milch`, `paneer 400g` or `Bananen x6`; the amount is split off and the item is sorted into its aisle (Fruit & veg, Dairy, Indian store…). Change an item's aisle once and Thali remembers it. **Usuals** are the things you buy most often, one tap to re-add. Tick items in the shop, then **Clear**. **Share list** sends it as text (WhatsApp, Notes…).
- **Pantry:** what is at home, with an optional best-before date ("Use soon" shows anything due within 7 days). Tap the state to cycle *In stock → Running low → Out*. Low and out items go onto the shopping list automatically (can be turned off in Settings); clearing them from the list puts them back *In stock*.
- **From a recipe:** open a recipe → **Shop for this recipe** → pick the ingredients you need. Items already in stock or on the list start unticked. Any food also has a **Shopping list** button.
- Synced in `thali/household.json`; included in backups.

## Food database
Everything here works offline.

| Source | What | Count |
|---|---|---|
| **THALI** (curated) | Everyday Indian (incl. Gujarati farsan), German and international foods with home portions (roti, katori, Brötchen…), including your usual dishes, café drinks and bubble tea | 452 |
| **INDB** | Indian Nutrient Databank (Jaacks et al. 2024): standard recipes. 156 rows with impossible values (e.g. deep-frying oil counted fully) were removed | 858 |
| **USDA** | USDA SR Legacy: generic ingredients and foods (public domain) | 7,233 |
| **OFF** | Packaged products you scan or find online (Open Food Facts) | grows |

Online (needs internet):
- **Search packaged products**: Open Food Facts, with German products first (can be changed in Settings).
- **Search USDA online**: FoodData Central, including prepared foods. Uses the shared `DEMO_KEY`. For more searches, get a free key at api.data.gov/signup and paste it in Settings → Online sources.
- **Check for database update** (Settings or Foods → Database) downloads the latest built-in database from this repository. The app also refreshes it automatically in the background.

How accurate it is: packaged-food labels are the most exact. THALI values are estimates for typical home recipes. INDB uses textbook recipes, and home cooking with more oil or ghee comes out higher.
For your own dishes, a recipe gives the best numbers. Anything can be adjusted with "Copy to my foods & adjust".

## Targets
Mifflin–St Jeor basal rate × activity factor, ± goal (0.25 kg/week ≈ 275 kcal/day), plus any "extra kcal" (e.g. breastfeeding).
Protein = g per kg body weight (default 1.6), fat = share of calories (default 30%), carbs = the rest, fibre 30 g.
The latest logged weight is used, so targets follow your weight. You can also set your own targets (profile → "Set my own targets").
This is an estimate (±10%). After 2–3 weeks, check the weight trend in Trends and adjust.

## Automatic sync (both phones)
Uses the same setup as Yupu baby. **You can reuse the private data repository and tokens you already set up for Yupu baby.**
Thali writes only to a separate `thali/` folder.
On each phone: Settings → Automatic sync → Repository `username/my-app-data` → paste that phone's token → **Test and turn on**.
(Or create a new private repo plus fine-grained tokens with Repository access: only that repo; Contents: Read and write.)
Files: `thali/YYYY-MM.json` (entries per month), `thali/profiles.json`, `thali/foods.json` (own foods, recipes, scanned products), `thali/household.json` (shopping list and pantry).
Syncs when the app opens, about 15 s after each change, and every minute while open. iPhone doesn't allow background sync.
Turn sync on first on the phone that already has data, then on the second phone.

## Backups
Settings → Backup → **Back up to Files** (save it to iCloud Drive). **Import backup** merges a backup, so nothing is overwritten by older data.
**Export CSV** gives a spreadsheet of all entries. iOS can clear web-app storage in rare cases; with sync on, the private repo is your backup.

## Updating the app
Replace the files in this repo. The phone picks up the new version on the second launch while online.

## Files
`index.html` (the app), `sw.js` (offline cache), `manifest.webmanifest`, icons, `data/` (food database),
`lib/` (zxing-wasm barcode reader, MIT licence), `tools/` (curated food list source and the database build script).

## Credits & licences
- Indian Nutrient Databank (INDB): Jaacks LM et al., *Current Developments in Nutrition* 2024, github.com/lindsayjaacks/Indian-Nutrient-Databank-INDB-
- USDA FoodData Central SR Legacy: public domain (rows taken from the CC-BY-4.0 `tempo-food-db` package by TempoLife).
- Open Food Facts: data under the Open Database License (ODbL), openfoodfacts.org
- zxing-wasm: MIT licence (lib/zxing-LICENSE.txt)
- Calorie targets are estimates, not medical advice.

## v1.2.2 (15 Oct 2026)
- **Water target right on Today:** tap the amount on the Water card (e.g. “750 / 3000 ml ✎”) to pick 1,5–4 L or an exact amount, and the glass size. Per profile, synced.

## v1.2.1 (15 Oct 2026)
- The bottom bar and the header now stay put when scrolling or pulling past the top/bottom on iPhone; only the content area scrolls.

## v1.2.0 (15 Oct 2026)
- **Not in the database? Thali now helps:**
  - **Closest matches**: when your exact words find little, foods that match some of the words are shown (e.g. "iced matcha with honey" → matcha latte, matcha powder, honey).
  - **Searches online automatically**: if the offline list finds fewer than 3 foods, Open Food Facts is asked straight away (when online).
  - **Estimate from ingredients**: "Not found? → Estimate … from ingredients". Thali suggests ingredients from the words you typed (matcha powder, honey…); add or adjust the grams (1 ml ≈ 1 g for drinks), then Add. It is saved as your recipe, so the next search finds it directly and it syncs to the other phone.
- **33 new drinks**: matcha milk tea, matcha latte (café / unsweetened / oat), matcha powder, bubble tea, milk tea, Thai iced tea, chai latte, iced latte, iced coffee, Frappuccino, Indian cold coffee, green/black/herbal tea, milkshakes, smoothie, badam milk, falooda, sugarcane juice, jaljeera, kombucha, energy drinks, Fanta/Sprite, Spezi, Club-Mate, bottled iced tea, Radler, protein shake.

## v1.1.0 (15 Oct 2026)
New **Shop** tab: shared shopping list sorted by aisle (amount parsing, usuals, share as text, remembered aisles) and a pantry with stock states and best-before dates.
Running low → list → bought → back in stock. "Shop for this recipe" and a Shopping list button on every food. Synced and backed up.

## v1.0.0 (15 Oct 2026)
First version: profiles with calculated or manual targets, meals, search across about 8,500 offline foods, Open Food Facts and USDA online search,
barcode scanning (camera, photo or typing), own foods, recipe builder, favourites, recent foods, copying yesterday's meals, quick add, water, weight,
trends (calories, protein, macro split, weight trend, top calorie sources), GitHub sync, backup/import, CSV export, light/dark theme, and a vegetarian filter.
