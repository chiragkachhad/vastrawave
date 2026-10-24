# VastraWave — GitHub Pages (4 files wali website)

Is folder ki **4 HTML files** hi poori website hain. Koi folder upload nahi karna —
har file ke andar uska design, code aur photos band hain.

| File | Kya hai |
|------|---------|
| `index.html` | Main page — rail par latke kapde (side-angle rack, hover 3D) |
| `shop.html` | Shop + Product page + Info/About (product: `shop.html?id=CR101`) |
| `cart.html` | Cart + Checkout + Order success |
| `admin.html` | Admin — Orders, Shipping Labels, Product Manager (password wahi purana) |

## GitHub par update kaise karein
1. Repo **vastrawave** kholein → **Add file → Upload files**
2. Ye 4 files ek saath select karke upload karein (purani `index.html` / `shop.html`
   apne aap replace ho jayengi, `cart.html` / `admin.html` nayi jud jayengi)
3. **Commit changes** dabayein — 1–2 minute me site update:
   https://chiragkachhad.github.io/vastrawave/

## Note
- Admin: `admin.html` kholte hi password aayega (wahi purana wala). Repo public hai,
  isliye ye admin demo-level suraksha hai — asal business ke liye baad me proper
  hosting + backend lagega.
- Orders/cart customer ke browser (localStorage) me save hote hain — GitHub Pages
  par server nahi hota, isliye admin me wahi orders dikhenge jo usi browser se bane hon.
- Poora project (saare alag pages + assets) `vastraa.zip` me surakshit hai —
  jab domain/hosting aayegi to wahi lagega. Ye 4 files dobara banani hon to:
  `python3 tools/build_github.py`
