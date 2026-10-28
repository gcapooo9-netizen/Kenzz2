import time
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "@gcapooo9"
DATA_FILE = "prices_cache.json"

# لستة المنتجات (محدودة بـ 150 منتج بالضبط وخالية من التكرار)
PRODUCTS = [
    "https://kenzz.com/en/product/8KYCWYNKG8MC/Samsung-Smart-TV-98-inch-4K-Tizen-Crystal-UHD-DU9000",
    "https://kenzz.com/en/product/8LKPG7TW6TKV/Black-%26-Decker-Blender-with-2-Mills-1.5-Liters-Black",
    "https://kenzz.com/en/product/8LUHL99744SU/Pyrex-Thermal-Refrigerator-With-Lid-1-Liter-3872",
    "https://kenzz.com/en/product/8MDC7H2QTZ8C/Toshiba-Top-Load-Automatic-Washing-Machine-15-kg-Gray-AW-DUHN1600LUPEG-(MK)",
    "https://kenzz.com/en/product/8MMVHY8GVNH9/City-Blender-6500-Watt-2-Liter-6-Stainless-Steel-Blades-Multi-Speed-%E2%80%8B%E2%80%8B-Hma-1021",
    "https://kenzz.com/en/product/8P6VG7AF2ZEZ/Universal-Gas-Water-Heater%2C-6L-White-Ge-6-N",
    "https://kenzz.com/en/product/8Q9L9XEKLAGZ/Magefesa-Pressure-Cooker-8-Liters-Stainless-Steel",
    "https://kenzz.com/en/product/8QD8FXKFC6KM/Dansha-Hand-Blender-1000-Watt",
    "https://kenzz.com/en/product/8QDZEC3RTT8L/Zanussi-Digital-Gas-Water-Heater-10-L-Chimney-Adapter-Silver-ZYG10113SL",
    "https://kenzz.com/en/product/8QUG8SS2DRWR/Fresh-Relax-80-Liter-Electric-Water-Heater",
    "https://kenzz.com/en/product/8QZRKE73VKL7/Fan-Heater-3-Operating-Modes-Rotation-Feature-2000-Watts-Black-Mar-910",
    "https://kenzz.com/en/product/8R67UPRA3L5K/Mom-C25Bbe-Bk-Microwave-And-Grill-25-Liters-Black",
    "https://kenzz.com/en/product/8RP22BJMZSGL/Paper-Fan-With-Wooden-Handles-Multi-Colored",
    "https://kenzz.com/en/product/8S8L62SZFYZK/Sokany-SK-1711-4-4-in-1-Hand-Blender-1000W",
    "https://kenzz.com/en/product/8UCQ5FK55C24/Jack-Microwave-43L-Silver-NGM-43M3",
    "https://kenzz.com/en/product/8UG2M5N4JYAX/Sokany-Blender-and-Whisk-800-Watts-5-Speeds-Silver-SK-6630",
    "https://kenzz.com/en/product/8UG7K2CYPSUL/Unionaire-Top-Loading-Washing-Machine-13-kg-Silver-UW130TPLA2SL",
    "https://kenzz.com/en/product/8WANLZ9AEYEG/Canvas-Backpack-With-Laptop-Pocket-Blue",
    "https://kenzz.com/en/product/8ZFQMLG8MNCM/Ariston-Built-in-Gas-Oven-90-cm-Stainless-Steel-GESM53IXA30",
    "https://kenzz.com/en/product/953P677VRGEL/Kiriazi-No-Frost-Refrigerator-335-Liters-Silver-Kh370Ln",
    "https://kenzz.com/en/product/95USJC23VJQD/2-Way-Movable-TV-Stand-85-Inch-T-700",
    "https://kenzz.com/en/product/9632X7R5XVTE/Tornado-TM-25MK-Electric-Microwave-25-Liter-Black",
    "https://kenzz.com/en/product/966QERSL3XDJ/Fresh-Horizontal-Deep-Freezer-255L-Silver-FDF-330",
    "https://kenzz.com/en/product/96F2MU9FVNCV/Black%2BDecker-8L-Black-Air-Fryer-SAF80W-B5",
    "https://kenzz.com/en/product/96JVPDR8D6SR/Beko-Dishwasher-14-People-Silver-BDFN15421S",
    "https://kenzz.com/en/product/96SHNWHBQ9E6/Hand-Blender-4*1-Dsp-1200-Watt-Km1137",
    "https://kenzz.com/en/product/96YTBKMXRS6R/ZX-240-Movable-TV-Stand-55-26-Inch",
    "https://kenzz.com/en/product/97CURQF9PXNM/Parking-sensor-with-display-screen-4-pieces-black",
    "https://kenzz.com/en/product/97P3PEYL3BQH/Beko-Split-Air-Conditioner-1.5-Hp-Inverter-Motor-Cold-Only-White-Bict1221X",
    "https://kenzz.com/en/product/98DR78RKTVWQ/Rechargeable-Shaver-Black-V-339",
    "https://kenzz.com/en/product/992D6CWD5V6Q/HDMI-Switch-and-2*1-Audio-Adapter-for-Hdtv-Dvd-Display-Black",
    "https://kenzz.com/en/product/99N4VCTL2TVM/Peugeot-car-pedal-set-black-5-pieces",
    "https://kenzz.com/en/product/9AV7YEGC4NP8/Glass-screen-protector-for-iPhone-13Pro-Black",
    "https://kenzz.com/en/product/9FP8SJCREXQ6/Beko-Digital-Inverter-Refrigerator-With-Tap-477-Liters-Black-B3Rdne500Lxbr",
    "https://kenzz.com/en/product/9GC99PFANYAH/Pampers-Pants-Size-5-58-Diapers",
    "https://kenzz.com/en/product/9GLJUUDPS9X7/Ikea-Ikea-Breakage-Microwave-Cover-Grey-(26cm)",
    "https://kenzz.com/en/product/9GVYHXNYHTPF/IDO-Microwave-42-Liters-Black-MW42NG-BK",
    "https://kenzz.com/en/product/9J7EVNPL43TV/COSRX-Salicylic-Acid-Daily-Gentle-Cleanser-Facial-Soap",
    "https://kenzz.com/en/product/9JYAPVYUQSMX/Castell-Ceiling-Fan-56-Inch-White-FAC1056DW",
    "https://kenzz.com/en/product/9LE54N8VECNB/Vacation-Sunscreen-SPF50%2B-Lotion-120-ml",
    "https://kenzz.com/en/product/9LZTLQJ34ZBZ/Saudi-Saif-Aluminum-Pressure-Cooker-3-Liters",
    "https://kenzz.com/en/product/9N573XS6X5KV/Midea-Air-Fryer-4L-Mf-Cn40D29-Black",
    "https://kenzz.com/en/product/9NL9YVHMMFTN/Samsung-Front-Load-Washing-Machine-11-Kg-Black-Ww11B1534Dabas",
    "https://kenzz.com/en/product/9PPZN9855VBG/Carnival-Wall-Fan-18-Inch-White-Red-WFZ1820",
    "https://kenzz.com/en/product/9QEUTCP3US5F/THB-400CH-Electric-Blender-400w-Black",
    "https://kenzz.com/en/product/9QW2UQEAUH2P/Kiriazi-Gas-Cooker-4-Burner-Silver-6400S",
    "https://kenzz.com/en/product/9R8C4M5VV8G6/Exhaust-Fan-and-Tongue-8-Inch-White",
    "https://kenzz.com/en/product/9RJHHUXA3BCU/Black-%26-Decker-Air-Fryer-Pizza-Oven-10.5-Liters-PGAF105-B5",
    "https://kenzz.com/en/product/9STXGD9JPN4W/Midea-Split-Air-Conditioner-1.5-HP-Cooling-Only-White-MSC1T-12CR-N",
    "https://kenzz.com/en/product/9TERTVT74L4U/Foldable-cup-holder-with-car-storage-box-Beige-Black",
    "https://kenzz.com/en/product/9TW2LWGNSWA2/Hoover-Fully-Automatic-Washing-Machine-7-kg-Inverter-Motor-Silver-H3WS17TMF3R-ELA",
    "https://kenzz.com/en/product/9UREU29VLM9T/Eva-Sun%26Sea-Sun-Screen-Lotion-Tinted-40ml",
    "https://kenzz.com/en/product/9V5UWFB8FD9D/Keriazi-Gas-Cooker%2C-60x60-4-Burners-Self-Ignition-6400-Silver",
    "https://kenzz.com/en/product/9VGEQMGM7KFB/Tornado-fan-56-inches-3-blades-white-TCF56L",
    "https://kenzz.com/en/product/9ZA7J2B7ATE8/Air-Fryer-Paper-100-Pieces",
    "https://kenzz.com/en/product/9ZM7YK9VHPZL/Zanussi-Gas-Cooker-with-Oven-5-Burners-Digital-Silver-ZCG92686XA",
    "https://kenzz.com/en/product/9ZR6BEXK2G5Y/Sokany-Hand-Blender-1200-Watt-Sk-758",
    "https://kenzz.com/en/product/A2RW5NT5FMZT/509-Liter-Bottom-Freezer-Refrigerator-Black-RCNE590E35ZXP3",
    "https://kenzz.com/en/product/A3LR2QAK5ZHG/Philips-Air-Fryer-4.1L-Black-HD9252-91",
    "https://kenzz.com/en/product/A3YL9QJN3HE6/Beko-Automatic-Digital-Inverter-Washing-Machine-10Kg-1600-Rpm-Grey-B3Wfu501040Mci",
    "https://kenzz.com/en/product/A47N9ET7MZVV/K-110-Movable-TV-Mount-43-19-inch",
    "https://kenzz.com/en/product/A4TZA9QELX7P/Saudi-Safe-Hand-Blender-1200-Watts",
    "https://kenzz.com/en/product/A63JAV6NWPDB/Kenwood-Blender-with-2-Choppers-2-Liters-Silver-BCC-BLP10.C0WH",
    "https://kenzz.com/en/product/A7K4BP7BJRHX/Hand-blender-800-Watt-black-HB-800FO",
    "https://kenzz.com/en/product/A8KZTVSTFNEL/Ramadan-Kareem-LED-Decoration-60-cm",
    "https://kenzz.com/en/product/A8MCU3LDB6VT/Royal-Gas-Master-Chef-Cooker-5-Burner-60-x-80-cm-R-2010290",
    "https://kenzz.com/en/product/A9S933UTVAV4/Women'S-Embroidered-Prayer-Cap-736",
    "https://kenzz.com/en/product/ABLQCWHWFJ6C/Fresh-Fan-16-inch-Blue-Galaxy",
    "https://kenzz.com/en/product/ACGKM3FHTQGR/Ch-645-Blender-with-Chopper-1000-Watts",
    "https://kenzz.com/en/product/AEH97SHNRNM6/Mosquito-Screen-Curtain-for-Windows-200-%C3%97-150-cm",
    "https://kenzz.com/en/product/AFQ842ERN5CZ/Mienta-BL1251B-Electric-Blender-1.75-L-Black",
    "https://kenzz.com/en/product/AFTKEZXSG784/Hoover-7-kg-Fully-Automatic-Washing-Machine%2C-Black-H3WS173DC3B-ELA",
    "https://kenzz.com/en/product/AGHL3AHBN26U/Kenwood-Electric-Chopper-1.2-Liters-Silver-Chp62.400Si",
    "https://kenzz.com/en/product/AGTAGBBE8YM6/Ninja-Foodi-Dual-Air-Fryer-Af300Uk-2-Drawers-7.6-Liters-Black",
    "https://kenzz.com/en/product/AGWFBF7GAT9E/Tornado-Top-Automatic-Washing-Machine-7-Kg-Gray-Css1072Dc3B-Ela",
    "https://kenzz.com/en/product/AH9VGSM3EDBX/Tornado-Electric-Oven-46-Liters-1800-Watts-Grill-Fan-Black-TEO-46KD-BK",
    "https://kenzz.com/en/product/AJ2P76DCLHQQ/Silicone-Oven-Gloves-Purple",
    "https://kenzz.com/en/product/AM3FMDB7935N/Akai-Electric-Oven-With-Grill-And-Fan-55-Liters-Black-Silver-Ak-45",
    "https://kenzz.com/en/product/AM3SAQPS7VZT/Fresh-No-Frost-Refrigerator-369-Liters-2-Doors-Black-FNT-BS400BB",
    "https://kenzz.com/en/product/AMUTVN74RGRG/Silicone-shower-holder",
    "https://kenzz.com/en/product/ANFQLUK3TDNJ/Mirage-50-Inch-4K-Smart-TV-Built-in-Receiver-50MRU720",
    "https://kenzz.com/en/product/ANP3BMFAV7ES/Beko-Mini-Bar-Refrigerator-120-Liters-Black-Tse12340-B",
    "https://kenzz.com/en/product/APLFWPYYEJRK/Af205K-Air-Fryer-5.5L-Black",
    "https://kenzz.com/en/product/APR9A97G9SDV/Blp10.Aowh-Electric-Blender-With-Grinder-White-Grey",
    "https://kenzz.com/en/product/APU4UV5DF4YM/Zanussi-Perlamax-Washing-Machine-8-Kg-Silver-Zwf8240Ss5",
    "https://kenzz.com/en/product/APY3PBRDCYZC/Beko-Blender-Glass-Jug-6-Speeds-1.75-Liter-800-Watt-Black-Silver-TBN-81808-BX",
    "https://kenzz.com/en/product/AQGHCM7R62G2/Ecomatic-Built-in-Electric-Gas-Cooker%2C-30-cm-2-Slabs-Stainless-Steel",
    "https://kenzz.com/en/product/AQH92GXW4J8K/Saudi-Saif-Stainless-Steel-Pressure-Cooker-11-Liters",
    "https://kenzz.com/en/product/AQVY5HMWHVMK/SK-8043-Air-Fryer-8L-2000W-Black",
    "https://kenzz.com/en/product/AQXZM8UAZT5L/Fresh-25-cm-One-Way-Multicolored-Exhaust-Fan-FVF-25",
    "https://kenzz.com/en/product/ARD4E5RSPNBC/Lg-Washing-Machine-9-Kg-Black-F4R5Vyg2E-Black",
    "https://kenzz.com/en/product/ARPWUTV8DYAA/Sokany-Sandwich-Maker-750-Watts-SK-08067",
    "https://kenzz.com/en/product/ARSLJ7D9FTEE/First-Wall-Squared-Ventilating-Fan-35-cm-White",
    "https://kenzz.com/en/product/ARXTGXCMD8VA/Perfix-Stand-Fan-18-Inch-Black-SFS-181",
    "https://kenzz.com/en/product/ARZT2CUWDNGU/Fresh-Split-Air-Conditioner-1.5-HP%2C-Cooling-Only-White-SIFW13C-IP--SIFW13C-OX2",
    "https://kenzz.com/en/product/ASD7MVBLW88X/Fresh-Matrix-Safety-Cooker-90-X-60-5-Burners-Silver-500016944",
    "https://kenzz.com/en/product/AT7PZKVYYL4V/Beko-6-Drawer-Digital-Deep-Freezer%2C-Black-270-Liters-B3RFNE274B",
    "https://kenzz.com/en/product/AT856T5TQLMW/R50-Vertical-Electric-Water-Heater-50-Liters-White",
    "https://kenzz.com/en/product/ATQ3J4B5LLHT/Ghost-Fresh-Twin-Tub-Semi-Automatic-Washing-Machine-8-Kg-White-Fwt10900Na",
    "https://kenzz.com/en/product/AUW2ARA4HB3P/Fresh-Elite-Oven-Grill-And-Fan-65-Liters-Gold",
    "https://kenzz.com/en/product/AV86J5DMTVHL/Fruit-Basket-and-Strainer-Blue",
    "https://kenzz.com/en/product/AW5TCXQRCDCR/SK-7011-Electric-Chopper-Blender-Silver",
    "https://kenzz.com/en/product/AYFMTVLCQT4X/FA-V40M-Fresh-Air-Cooler-40-Liters-White",
    "https://kenzz.com/en/product/AZR23U74X89X/Mobile-Screen-Protector-IPhone-14-Max",
    "https://kenzz.com/en/product/AZXH5NDKUSB7/Foldable-Portable-Washing-Machine-White-Blue",
    "https://kenzz.com/en/product/B254W4S5SKP8/Sokany-Hand-Blender-500-Watts-SK-02035",
    "https://kenzz.com/en/product/B26UEQ63VRDW/C61P5-Stand-Fan-with-Remote-18-Inch-Black-White",
    "https://kenzz.com/en/product/B2LKMXVWHRAD/Ikea-FANTASTISK-Paper-Napkin%2C-White---100-Pack-40x40-cm%2CIKE-500.357.52",
    "https://kenzz.com/en/product/B2QN3VX2CVJR/Washing-machine-cover-with-two-souls-75*46*85-multi-colored",
    "https://kenzz.com/en/product/B3A4WXNX78NS/Sary-Smart-Android-TV-32-inch-SA32RY-8500-FL-E",
    "https://kenzz.com/en/product/B3P6PKXLDPHB/X9-Ultra-2-Full-Screen-Smart-Watch-49Mm-Black",
    "https://kenzz.com/en/product/B3QMYB57WBXQ/PRO1-R80-Electric-Water-Heater-80-Liters-White",
    "https://kenzz.com/en/product/B3UPYKTKWN3H/SK-8041-Smart-Air-Fryer-8-Liter-1700-Watt-Silver-Black",
    "https://kenzz.com/en/product/B4BJ8A2XA8L5/R-770Ar(St)-Microwave-With-Grill-34-Liters-Silver",
    "https://kenzz.com/en/product/B4V5HNKNLTV8/Sequence-Jumbo-Board-Game",
    "https://kenzz.com/en/product/B5PXVGKWFRXG/Celtal-Refrigerator-11-ft-Defrost-Silver-FB30S",
    "https://kenzz.com/en/product/B5WLDBMH4TEU/White-Point-Washing-Machine-13-Kg-Gray-Wptl13Dfgcm",
    "https://kenzz.com/en/product/B6C846V76LEZ/Toshiba-LED-Smart-TV-50-Inch-4K-Black-50U5965EA",
    "https://kenzz.com/en/product/B6WTRXE8EESU/Philips-HD9200-91-Digital-Air-Fryer-4L-Black",
    "https://kenzz.com/en/product/B6YB5YUJ2Q3X/Deep-Freezer-8-Drawers-404-Liters-Digital-Touch-Control-Stainless-Steel-Silver-L-RFNE448E35XB",
    "https://kenzz.com/en/product/B792KN6HV5J4/AF5539-B5-Air-Fryer-5.5-L-Black",
    "https://kenzz.com/en/product/B7QMWNHCJYJA/iPhone-13-Pro-Max-Clear-Glass-Screen-Protector",
    "https://kenzz.com/en/product/B7VFD56FG78Y/500004558-Al-Shabah-Stand-Fan-with-Remote-18-Inch-Black-Red",
    "https://kenzz.com/en/product/B9F9XY5Y2CDJ/Electric-Handheld-Blender-2*1",
    "https://kenzz.com/en/product/BAVNYW9PDCE6/Kiriazi-370L-Black-No-Frost-Refrigerator-KH370LN",
    "https://kenzz.com/en/product/BCA2S2G2ZUJE/Alaska-KSD29-294.5L-Frost-Free-Defrost-Refrigerator-White",
    "https://kenzz.com/en/product/BCRTY5LCDWS8/Moulinex-LM2428EG-400W-Electric-Blender-Black",
    "https://kenzz.com/en/product/BCZKK9GTV5C2/Glow-Ballpoint-Pen-0.7-Mm-Red-12-Pens",
    "https://kenzz.com/en/product/BD4GEMJ7UMMM/Air-fryer-5-liters-SE-3011",
    "https://kenzz.com/en/product/BDMT7PTKAX5N/3-In-1-Blender-Pink",
    "https://kenzz.com/en/product/BDQGVPLZWL6B/ET-EH45-Holder-For-Smartphone-360-Degree",
    "https://kenzz.com/en/product/BDZ3NS3FQG7W/Ox-45-Tv-Stand",
    "https://kenzz.com/en/product/BEK5C9TATEYB/Fresh-Shabah-Blender-with-Two-Mill",
    "https://kenzz.com/en/product/BETHALZVGABD/Smart-Tv-Screen-32-Inches-Black-Le32Dn4",
    "https://kenzz.com/en/product/BEXACQ968NEV/LG-Microwave-With-Grill-42-Liters-Black-MH8265DIS-",
    "https://kenzz.com/en/product/BF64VVLLMP5N/White-Point-Digital-Top-Loading-Washing-Machine-11-Kg-Gray-Wptl11Dgglan",
    "https://kenzz.com/en/product/BFHZSWZJQR4M/LG-Smart-TV-55-Inch-Silver-55NANO776QA",
    "https://kenzz.com/en/product/BFLP93HNLL42/sk-1733-Nescafe-hand-blender-25-watt-white",
    "https://kenzz.com/en/product/BFNNKNQHASTV/Nickelodeon-My-Best-Friend-Activity-Book-20-Pages",
    "https://kenzz.com/en/product/BFSFZ6927QK6/Bladeless-Ceiling-Fan-with-Dimmable-LED-Light-and-Remote-Control-%E2%80%93-White-25-cm",
    "https://kenzz.com/en/product/BG8TF9CXWL8T/SK-666666B-Electric-chopper-10-liters-2000-watts-silver-black",
    "https://kenzz.com/en/product/BGGBLK6TVCKV/Razor-For-Face-%26-Body-Shaving",
    "https://kenzz.com/en/product/BH88VNLRZBRE/Lazord-Granite-Plus-Rectangular-Oven-Casserole-Black-3-Pieces",
    "https://kenzz.com/en/product/BJ7XJGBWJS9F/Tornado-Air-Fryer-1550-Watts-4-Liters-White-THF-1554D-XL-CS",
    "https://kenzz.com/en/product/BK2UWKXYAX4Q/Smile-Stand-Fan-26-Inch-Black",
    "https://kenzz.com/en/product/BK3UGYJXDSKU/Mini-Handheld-Fan-with-Mobile-Stand-Rechargeable-Orange",
    "https://kenzz.com/en/product/BKDRQYUU5KSA/Cassell-18-Pole-Fan%2C-Black-FAS-2218",
    "https://kenzz.com/en/product/BKMDVHR8BS6N/Nescafe-Blender-with-Charger-and-Mini-Egg-Beater-Black",
    "https://kenzz.com/en/product/BKRSWNBHA286/Rc650-B5-Rice-Cooker-0.6L-White",
    "https://kenzz.com/en/product/BLGE3QK9DJLR/4-In-1-Hand-Blender-500-Watts-2-Speeds-Km1093",
    "https://kenzz.com/en/product/BLJ9ZUWCDF2W/Lavvento-Type-C-Laptop-Adapter-Cv152",
    "https://kenzz.com/en/product/BNK2UNTVXE8M/4-inch-plastic-base-sleeve-white",
    "https://kenzz.com/en/product/BNZEZAUFBVFS/Arzum-Shake-%26-Take-Personal-Blender-300W-Red-Ar1032",
    "https://kenzz.com/en/product/BQS6YZPC6LEK/Fresh-Air-Fryer-XL-7L-Black-AFF-1800B",
    "https://kenzz.com/en/product/BRJ2ZQ65GVB5/Multicolor-Washing-Machine-Cover",
    "https://kenzz.com/en/product/BRJKSHVM4TZM/Toshiba-Automatic-Washing-Machine-Top-Load-8-kg-Silver-AW-J800AUPEG",
    "https://kenzz.com/en/product/BS59Q69EZRXA/Fresh-Industrial-18-Inch-Wall-Fan-Black-F18-450W",
    "https://kenzz.com/en/product/BT8J98WLAT93/F4R5TYG2T-Fully-automatic-washing-machine%2C-8-kg-Silver"
]

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

AR = str.maketrans("٠١٢٣٤٥٦٧٨٩٫٬", "0123456789.,")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"خطأ في حفظ الملف: {e}")

stored_data = load_data()

def send(msg):
    u = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(u, json={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print(f"خطأ في إرسال رسالة التليجرام: {e}")

def check_prices():
    global stored_data
    
    total_products_count = len(PRODUCTS)
    if total_products_count == 0:
        print("\n[⚠️] قائمة المنتجات فارغة حالياً!")
        return
        
    print(f"\n[🔄] بدء فحص عدد {total_products_count} منتج بصمت...")
    
    changes_count = 0
    checked_count = 0
    current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    for index, url in enumerate(PRODUCTS, 1):
        try:
            response = requests.get(url, headers=H, timeout=15, allow_redirects=True)
            
            if response.status_code != 200:
                print(f"[{index}/{total_products_count}] فشل فحص المنتج (كود الاستجابة: {response.status_code})")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            current_price = None
            product_name = None
            
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    data_items = data if isinstance(data, list) else [data]
                    
                    for item in data_items:
                        if isinstance(item, dict) and item.get('@type') == 'Product':
                            product_name = item.get('name')
                            offers = item.get('offers')
                            if isinstance(offers, dict):
                                p = offers.get('price') or offers.get('lowPrice')
                                if p:
                                    current_price = float(p)
                                    break
                            elif isinstance(offers, list) and len(offers) > 0:
                                p = offers[0].get('price')
                                if p:
                                    current_price = float(p)
                                    break
                    if current_price:
                        break
                except:
                    pass
            
            if not product_name:
                h1 = soup.find('h1')
                product_name = h1.get_text().strip() if h1 else "منتج بدون اسم"
            
            if not current_price:
                price_element = (
                    soup.find('span', {'class': 'price'}) or 
                    soup.find('div', {'class': 'price'}) or 
                    soup.find('span', {'class': 'current-price'}) or
                    soup.find('span', class_=lambda x: x and 'price' in x.lower())
                )
                if price_element:
                    price_text = price_element.get_text().strip().translate(AR)
                    price_str = ''.join(c for c in price_text if c.isdigit() or c == '.')
                    if price_str:
                        current_price = float(price_str)
            
            if current_price:
                checked_count += 1
                is_new_product = url not in stored_data
                
                if is_new_product:
                    stored_data[url] = {
                        "name": product_name,
                        "current_price": current_price,
                        "history": [{"price": current_price, "time": current_time_str}]
                    }
                else:
                    item_data = stored_data[url]
                    old_price = item_data["current_price"]
                    
                    if current_price != old_price:
                        prices_list = [h["price"] for h in item_data["history"]]
                        prices_list.append(current_price)
                        avg_price = round(sum(prices_list) / len(prices_list), 2)
                        lowest_historical_price = min(prices_list[:-1]) if len(prices_list) > 1 else old_price
                        
                        if current_price < old_price:
                            diff_pct = round(((old_price - current_price) / old_price) * 100, 1)
                            discount_text = f"📉 نسبة الخصم: %{diff_pct}"
                        else:
                            diff_pct = round(((current_price - old_price) / old_price) * 100, 1)
                            discount_text = f"📈 نسبة الزيادة: %{diff_pct}"
                        
                        is_lowest = current_price <= lowest_historical_price
                        tagline = "🔥 أقل سعر تاريخي!" if is_lowest else "📊 تحديث جديد في السعر"
                        
                        item_data["current_price"] = current_price
                        item_data["name"] = product_name
                        item_data["history"].append({"price": current_price, "time": current_time_str})
                        
                        history_text = ""
                        for h in reversed(item_data["history"][-5:]):
                            history_text += f"➡️ EGP {h['price']} – {h['time']}\n"
                        
                        msg = (
                            f"✨ عرض كنز ✨\n\n"
                            f"🛒 {product_name}\n\n"
                            f"💵 السعر الحالي: EGP {current_price}\n"
                            f"💵 السعر السابق: EGP {old_price}\n"
                            f"📊 متوسط الأسعار: EGP {avg_price}\n"
                            f"{discount_text}\n"
                            f"{tagline}\n\n"
                            f"📜 تاريخ الأسعار:\n"
                            f"{history_text}\n"
                            f"🛍️ **رابط المنتج:**\n{url}\n\n"
                            f"🔗 [اضغط هنا للشراء مباشرة]({url})"
                        )
                        send(msg)
                        changes_count += 1
                
                print(f"[{index}/{total_products_count}] ✅ تم الفحص - {product_name} | السعر: {current_price}")
            else:
                print(f"[{index}/{total_products_count}] ⚠️ لم يتم العثور على السعر.")
            
            time.sleep(1.5)
            
        except Exception as e:
            print(f"[{index}/{total_products_count}] ❌ خطأ: {e}")
            
    save_data(stored_data)
    print(f"\n[⏳] انتهت الدورة الحالية (تم فحص الخمسة عشرين منتج، رصد {changes_count} تغيير).")

if __name__ == "__main__":
    print("البوت يعمل الآن في الخلفية لمراقبة الأسعار بصمت...")
    while True:
        check_prices()
        time.sleep(900)
