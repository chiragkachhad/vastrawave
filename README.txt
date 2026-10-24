============================================================
  ADMIN PANEL KO PASSWORD SE LOCK KARNA  (5 minute)
============================================================

KYUN: bina lock ke koi bhi aapki site par admin.html ya
tools/product-manager.html khol kar products delete kar sakta hai.

NOTE: admin.html, label.html aur product-manager.html pehle se PASSWORD se
band hain (admin-lock.js). Ye .htaccess uske UPAR ki extra security hai.

--------------------------------------------
TARIKA 1 — cPanel se (sabse aasan, bina file ke)
--------------------------------------------
1. cPanel login -> "Directory Privacy" (ya "Password Protect
   Directories") kholein
2. "tools" folder chunein -> checkbox "Password protect this
   directory" -> username/password set karein
3. Ab alag se admin.html aur label.html lock karne hon to:
   File Manager -> public_html -> "admin.html" par right click
   nahi hota, isliye TARIKA 2 use karein.

--------------------------------------------
TARIKA 2 — .htaccess file se (root pages ke liye)
--------------------------------------------
1. Apna cPanel username dekhein (upar right corner me likha hota
   hai, jaise "abc123").

2. Ye file:  security/.htaccess.root
   Upload karein:  public_html/.htaccess
   (naam se shuru ka dot hatana mat bhoolna — .htaccess)

3. public_html/.htaccess khol kar edit karein:
      AuthUserFile "/home/USERNAME/.htpasswd"
   USERNAME ki jagah apna cPanel username:
      AuthUserFile "/home/abc123/.htpasswd"

4. Ab .htpasswd banayein. cPanel -> "Terminal" ya
   "Password Protect Directories" tool se, ya ye command:
      htpasswd -c /home/abc123/.htpasswd storeadmin
   (do baar password poochhega)

   Terminal na ho to online generator use karein:
      search: "htpasswd generator"
   aur bani hui line (jaise  storeadmin:$apr1$xyz...  )
   ko .htpasswd file me paste kar ke public_html ke BAHAR
   /home/abc123/ me upload karein.

5. Tools folder ke liye:
      security/.htaccess.tools  ->  public_html/tools/.htaccess
   (usme bhi USERNAME badlein)

6. TEST: browser me kholein  aapkisite.com/admin.html
   Password maangna chahiye. Nahi maange to path galat hai.

--------------------------------------------
DHYAN
--------------------------------------------
* .htpasswd hamesha public_html ke BAHAR rakhein
  (/home/username/ me), tabhi surakshit hai.
* Agar 500 error aaye to AuthUserFile ka path galat hai —
  file ko .htaccess.bak kar dein, site theek ho jayegi.
* Password ek hi jagah hai: assets/js/admin-lock.js  ->  var PASS = "..."
  (admin.html, label.html, tools/product-manager.html — sab par yahi lagta hai)
* Netlify (testing) par .htaccess kaam nahi karta — wahan
  sirf admin-lock.js wala password hai (jo aapne set kiya hai) — wo har jagah lagega. Asli hosting
  par hi lock kaam karega.
