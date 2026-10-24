# Vastraa — Men & Women Fashion Store (Demo Build)

Client ka business: **Corsets · Ladies Wear · T-Shirts · Shirts · Bottoms** — ek hi store, **Women / Men** sections ke saath.
Plus: **har order ka shipping label print** — delivery partner ko dene ke liye.

Ye **static site** hai — koi database nahi, koi monthly platform fee, koi commission nahi.
Bas hosting par upload kar do aur chal padegi.

---

## Pages

| File | Kya hai |
|---|---|
| `index.html` | Home — hero, **Shop Women / Shop Men banners**, categories, new arrivals, men's picks, recently viewed |
| `shop.html` | 13 products + filters (**Gender**, category, size, colour, price) + 6 sort options + live search |
| `product.html` | PDP — gallery, size × colour variants, **size chart modal**, **delivery estimate + live countdown**, trust badges, prepaid badge, WhatsApp order, recently viewed |
| `cart.html` | Cart — qty, coupon `VASTRAA10`, prepaid hint, free-shipping bar |
| `checkout.html` | Address form + payment (COD/UPI/Card) + **extra 5% off on prepaid** + weight/pieces auto-calc |
| `success.html` | Order confirm + tracking timeline |
| `about.html` | Shipping, exchange, size guide, privacy, terms, contact |
| `admin.html` | Orders + courier/AWB + status + **🖨️ Print label** + inventory + KPIs |
| `label.html` | Print-ready shipping labels (4×6 thermal ya A4 — 2 per page) |

## Catalogue (13 products)

| Section | Category | Products |
|---|---|---|
| **Women** | Corsets | Satin Bustier ₹1,299 · Lace Overbust ₹1,799 |
| **Women** | Ladies Wear | Floral Midi Dress ₹1,499 · Sequin Gown ₹2,999 · Peplum Top ₹899 |
| **Women** | Bottoms | Flared Palazzo ₹899 · Denim Skirt ₹1,199 |
| **Unisex** | T-Shirts | Oversized Boxy Tee ₹999 (240 GSM) · Graphic Tee ₹999 |
| **Men** | Shirts | Checkered Casual ₹1,299 · Solid Formal ₹1,299 |
| **Men** | Bottoms | Slim Fit Jeans ₹1,899 · Cargo Joggers ₹1,399 |

**Size scales category ke hisaab se alag (asli variant system):**
- Corsets / Ladies Wear / T-Shirts / Shirts → `S M L XL XXL`
- Men's Bottoms (jeans, joggers) → `28 30 32 34 36` (waist inches)
- Women's Bottoms (palazzo, skirt) → `S M L XL XXL` with waist/hip chart

Unisex products (tees) **Men aur Women dono** filters me dikhte hain.

## Conversion features (Foomer-style, par behtar)

1. **Delivery estimate + live countdown** — "Delivery between Wed 30 Sep and Sat 3 Oct · Order within 04:47:21" → urgency
2. **Extra 5% off on prepaid** — COD se prepaid par lane ke liye (Razorpay Magic Checkout wala concept); checkout me method badalte hi total update
3. **Trust badges row** on PDP — free shipping / 7-day exchange / COD
4. **Size chart inline modal** (alag page nahi — customer PDP chhodta hi nahi); har category ka alag chart
5. **Recently viewed** — home + PDP par
6. **Rotating offer bar** — 3 offers ghoomte hain
7. **Honest pricing** — "MRP ₹4,997 → 80% off" jaisa fake discount nahi; real compare-at price
8. **Gender navigation** — header me Women / Men / New / Sale

## 🏷️ Shipping Label — kaise use karein

1. Order aaye (ya `admin.html` me **"Add sample order"**)
2. Us row me **Courier** select karein + **AWB** daalein
3. **🖨️ Print** → `label.html` → **Print labels**

Label par: Ship To (naam, address, phone, pin) · **COD: COLLECT ₹X** / PREPAID · weight (auto) · pieces ·
contents · courier + **AWB barcode** · Ship From / Return to · "Handle with care".
Options: **4×6 thermal** ya **A4 (2/page)**; saare orders ke liye "Print all labels".

> Real courier API (Shiprocket/Delhivery) lagaane par AWB auto-generate hoga — alag paid add-on
> (Standard package me, ₹18K Starter me nahi).

## Client ka data kahan hai

1. **`assets/js/data.js` → `CONFIG`** — `name`, `tagline`, `phone`, `pickupAddress`, `pickupPhone`, `gstin`,
   `freeShippingAbove`, `shippingCharge`, `prepaidPercent`, `dispatchBeforeHour`, `coupon`, `couriers`, `announces`
2. **`assets/js/data.js` → `PRODUCTS`** — `id, name, gender, category, chartKey?, price, mrp, rating, reviews,
   badge, wt, img, gallery[], colours[], sizes[], stock{}, fabric, care, extra, model, desc, highlights[]`

## Demo me kya real hai, kya nahi

**Real:** search, filters (gender + waist sizes), variants, out-of-stock sizes, cart, coupon, prepaid discount,
checkout validation, order ID, weight auto-calc, **shipping label + barcode**, WhatsApp ordering, wishlist,
size chart, recently viewed, delivery countdown, mobile-first responsive.

**Nahi hai (paid add-ons):** Razorpay live keys, Shiprocket/Delhivery API, Msg91/Interakt SMS-WhatsApp API,
GST invoice PDF, admin login, real database.

## Kaise chalayein / live karein

```bash
cd vastraa && python3 -m http.server 8000     # local demo
# ya seedha index.html par double-click — bina server ke bhi chalega
```

Live: domain (~₹1,000/saal) + shared hosting (~₹2,500–₹4,000/saal) → `public_html` me upload
(ya Netlify/Vercel — free). `CONFIG.phone` me client ka number daalo.

## Handover line (client ko)

> "Aapki site ready hai — Women (corsets, dresses, tops, bottoms) aur Men (tees, shirts, jeans, joggers)
> dono ek hi store me. Jaise hi order aata hai, admin me ek click se **shipping label print** ho jata hai.
> ₹18,000 one-time me main live kar dunga + 1 ghante ki training. Har mahine ₹1,000–₹1,500 me naye products,
> banners aur updates main sambhal lunga."

**Competitor pitch point:** jo brand aapne reference diya (thefoomer.in) wo Shopify par hai — Indian sellers ko
Shopify Payments na milne ki wajah se har order par **2% extra platform fee** lagti hai [1](https://razorpay.com/blog/razorpay-shopify-payment-gateway-pricing-explained/), plus monthly plan.
Ye build **0% commission** hai — sirf payment gateway ka ~2%.

---
Built as a demo — brand name, prices aur photos placeholder hain.
