# รับจ้างซ่อมรูปถ่ายหน้าศพ (The Funeral Photo Restorer)

คลิปเล่าเรื่องสยองขวัญแนวนอน 16:9 · ความยาวเป้าหมาย ~9–10 นาที · 28 ซีน
เล่าบุคคลที่ 1 (พีท) · ประโยคสั้น ตรงไปตรงมา · ดราม่าครอบครัว + สืบสวน + ความเชื่อไทย

---

## หลักการเล่าและสตอรี่บอร์ด (ถอดจากคลิปต้นแบบที่ส่งมา)

| เรื่อง | แนวทาง |
|---|---|
| **จังหวะภาพ** | เปลี่ยนช็อตทุก ~3–4 วินาที (ต้นแบบ: 145 ช็อตใน 10 นาที) → แต่ละซีนมี "ช็อตย่อย" 3–5 ช็อต ระบุไว้ใต้ Prompt |
| **ฮุก** | เปิดด้วยตัวเลขเงิน + คำถาม "คุณจะรับไหม" แล้วตอบทันที "ผมรับ" → เข้าเรื่องตัวเองเลย ไม่เกริ่นยาว |
| **ภาษา** | ประโยคสั้น 1 ลมหายใจ คำพูดธรรมดา ("ผม", "เอ็ง", "ลูก") สลับบทพูดตัวละครในเครื่องหมายคำพูด |
| **อารมณ์** | ทุกคืน: ปกติ → แปลก → พีค → ผ่อน (ตอนเช้า) แล้วค่อยไต่ระดับคืนถัดไป · มีฉากซึ้ง 1 จุด (หลานคุณยาย) คั่นก่อนเข้าส่วนระทึก |
| **ซับ** | ตัดเป็นวลีสั้น 3–8 คำต่อซับ ตัวขาว ไม่มีตัวหนังสือใหญ่บนภาพ (ยกเว้นเวลา/คืนที่) |
| **เสียง** | มีเสียงบรรยากาศต่ำ ๆ ใต้เสียงพากย์ตลอด (ห้องเงียบ นาฬิกา พัดลม) ไม่ปล่อยเงียบสนิท |

---

## ตัวละครอ้างอิง (ใช้คำบรรยายเดิมทุกซีน หน้าตาจะได้คงที่)

| ตัวละคร | คำบรรยายภาษาอังกฤษสำหรับ Prompt |
|---|---|
| **พีท** (28, อดีตกราฟิกดีไซเนอร์) | `PETE: a 28-year-old Thai man, simple round head, short black hair with a small fringe, thin rectangular glasses, light stubble, oversized grey hoodie, tired kind eyes` |
| **ลุงมั่น** (เจ้าของร้าน วัย 70) | `UNCLE MUN: an old Thai man in his 70s, bald head with white side hair, thick white eyebrows, round glasses on a cord, faded white short-sleeve shirt, brown slacks, walking cane` |
| **แม่พีท** | `PETE'S MOTHER: a frail Thai woman in her 50s, short grey-streaked hair, pale blue hospital gown, gentle smile` |
| **คุณยายผิน** (ในรูป) | `GRANDMA PIN: an elderly Thai woman in an old black-and-white portrait, hair in a neat bun, pale lace blouse, calm soft smile` |
| **ฝน** (หลานคุณยาย) | `FON: a Thai woman in her mid-20s, long straight hair tied back, black mourning blouse, red puffy eyes` |
| **เก่ง** (ผู้ตาย) | `KENG: a Thai man in his early 20s, short spiky hair, thin face, plain white T-shirt in an ID-card photo, faint purple bruise near left eye` |
| **ฆาตกร** (ชายในชุดกู้ภัย) | `THE KILLER: a broad-shouldered Thai man in his 40s, buzz cut, thick neck, small cold eyes, generic orange-and-black rescue volunteer vest over a dark shirt, no logos` |
| **ร้าน "เจริญศิลป์โฟโต้"** | `CHAROEN SIN PHOTO: a narrow two-storey old wooden Thai photo shop facing a temple gate, faded hand-painted sign, glass display of framed funeral portraits, steep creaky wooden staircase, upstairs workroom with an old beige computer, CRT monitor, flatbed scanner, incense holder, antique wooden bellows camera on a tripod` |

**คำท้าย Prompt ภาพทุกซีน (ใส่ตรงตามนี้):**
`minimalist 2D flat vector animation style, clean geometric character design, simple expressive faces, moody dim vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9`

> ซีนที่อยู่นอกร้าน (โรงพยาบาล, หน้าวัด) ยังคงใช้คำท้ายเดียวกันเพื่อคุมสไตล์ แต่บรรยายฉากในตัว Prompt ให้ชัด

---

# ส่วนที่ 1 — Google AI Studio Voice Director Prompt

> **วิธีใช้:** Google AI Studio → *Generate speech* → วางข้อความนี้ในช่อง **Style instructions** (โมเดล TTS ของ Gemini ไม่รับ System Instruction แบบโมเดลแชต)
> **เสียงแนะนำ:** `Iapetus` (ใส ชัด เป็นธรรมชาติ) หรือ `Umbriel` (สบาย ๆ แบบคนเล่า) — ทดลองกับซีน 1–3 ก่อน
> **เจนทีละ 3–4 ซีน** (ไม่เกิน ~1,400 ตัวอักษรต่อครั้ง) ใช้เสียงและ Style เดิมทุกครั้ง
> **ถ้าโมเดลอ่านแท็กออกเสียง** ให้เปลี่ยน `[pause: Xs]` เป็น `[short pause]` / `[medium pause]` / `[long pause]`

```text
# AUDIO PROFILE: "Pete — The Night-Shift Narrator"
A Thai man in his late 20s telling something that really happened to him. Natural,
grounded, conversational Central Thai. Not a radio host, not an actor — an ordinary
guy with a warm, slightly tired mid-range voice who is still a little shaken by
what he saw. Serious, sincere, never theatrical.

# THE SCENE
Late at night. He is sitting close to a single microphone in a small quiet room,
telling a friend the story for the first time. He remembers every detail. Some parts
still make his voice tighten; the part about his mother makes it soften.

# DIRECTOR'S NOTES
Language: Thai only. Read every word exactly as written. Numbers are already written
out as Thai words — read them as written.

Baseline delivery:
- Conversational pace, short sentences, one breath per line. Medium-low pitch.
- Plain, honest tone, like talking to a friend, not performing.
- End statements with a natural falling tone. Do not sing-song.

Suspense and pauses (very important):
- "..." means a real held silence, as if he is reluctant to say what comes next.
- [pause: Xs] or [short/medium/long pause] means total silence for that long.
  Never read any bracketed tag aloud.
- Before a reveal, slow down slightly and lower the volume. Say the scary word
  quietly, not loudly. Restraint is scarier than shouting.
- During danger, speed up with short, breathless phrases — but stay controlled.

Emotional colour:
- Talking about his mother and money: softer, a little ashamed, sincere.
- The granddaughter scene: gentle and moved, a slight catch in the throat.
- Horror moments: tense, hushed, close to the mic.
- The ending phone call: disbelief, the breath drains out of him.

Character voices (switch only when a bracketed tag asks for it, then return to Pete):
- [old woman, soft whisper]: Grandma Pin — very old, kind, breathy, slow, loving.
- [old man, gruff and shaky]: Uncle Mun — 70s, rough northern-Thai-flavoured
  warmth, slightly hoarse; in the final call, trembling with fear.
- [young woman, crying]: Fon — choked, grateful, breaking into tears.
- [killer, shouting]: a rough man in his 40s yelling through a door, aggressive,
  fake-friendly at first, then threatening. Loud but not distorted.
- [whispering, eerie]: barely audible, airy, slow.

Never: laugh, add words, add music cues, sound like an advertisement, or read tags.
```

---

# ส่วนที่ 2 — บทพากย์และภาพรายซีน (28 ซีน)

---

## ซีน 1 — 00:00–00:13 · คำถามเปิด

**🎙️ Voiceover Script**
```
[tone: calm, direct, slightly low]
ถ้ามีคนจ้างคุณ... คืนละห้าพันบาท
ให้มานั่งรีทัชรูปถ่ายหน้าศพ... ในร้านถ่ายรูปเก่า ๆ หน้าวัด... ตอนตีสอง
[pause: 0.6s]
โดยมีข้อแม้ข้อเดียว...
[tone: hushed]
ห้ามจ้องตาคนในรูป... นานเกินห้าวินาที
[pause: 1s]
คุณจะทำไหม?
```
**🔊 SFX:** นาฬิกาเดินติ๊กต็อกในห้องเงียบ · พัดลมเพดานหมุนเอื่อย ๆ · หมาเห่าไกล ๆ

**🖼️ Image Prompt**
```
Wide establishing shot at 2 AM of a narrow two-storey old wooden Thai photo shop
"Charoen Sin Photo" facing an ornate Thai temple gate across a quiet street, a single
dim yellow light glowing from the upstairs window, faded hand-painted sign, framed
black-and-white funeral portraits behind the dusty shop window, a lone street lamp,
stray dog silhouette, deep navy night sky, minimalist 2D flat vector animation style,
clean geometric character design, simple expressive faces, moody dim vintage Thai
photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ภาพกว้างร้านหน้าวัด ② ซูมหน้าต่างชั้นสองที่ไฟเปิด ③ ภาพใกล้รูปหน้าศพในตู้กระจก ④ ดวงตาในรูปหนึ่งรูป (ค้าง)

---

## ซีน 2 — 00:13–00:25 · "ผมรับ"

**🎙️ Voiceover Script**
```
[tone: honest, matter-of-fact]
ผมรับ.
[pause: 0.5s]
เพราะตอนนั้น... ผมไม่เหลือทางเลือกอะไรแล้ว
ผมชื่อพีท... อายุยี่สิบแปด
เคยเป็นกราฟิกดีไซเนอร์... จนบริษัทปิดตัว... เมื่อแปดเดือนก่อน
```
**🔊 SFX:** เสียงกล่องกระดาษวางลงพื้น · ประตูออฟฟิศปิด · เสียงถอนหายใจ

**🖼️ Image Prompt**
```
PETE: a 28-year-old Thai man, simple round head, short black hair with a small fringe,
thin rectangular glasses, light stubble, oversized grey hoodie, tired kind eyes, standing
on an empty city sidewalk holding a cardboard box with a desk lamp and a drawing tablet
sticking out, closed glass office door behind him with a "closed" sign, muted grey-blue
evening palette, minimalist 2D flat vector animation style, clean geometric character
design, simple expressive faces, moody dim vintage Thai photo studio interior, subtle
eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① พีทหันมาหากล้อง (แนะนำตัว) ② กล่องของในมือ ③ ป้ายบริษัทถูกปลด

---

## ซีน 3 — 00:25–00:42 · ค่าผ่าตัดแม่

**🎙️ Voiceover Script**
```
[tone: softer, a little ashamed]
เดือนที่แล้ว... หมอบอกว่าแม่ต้องผ่าตัดหัวใจ
ค่าใช้จ่ายรวม ๆ... สองแสนแปดหมื่นบาท
[pause: 0.6s]
เงินในบัญชีผม... เหลือไม่ถึงหมื่น
[pause: 0.5s]
แม่จับมือผมแล้วบอกว่า... "ไม่ต้องหรอกลูก แม่แก่แล้ว"
[pause: 0.8s]
ประโยคนั้น... ผมนอนไม่หลับไปทั้งอาทิตย์
```
**🔊 SFX:** เสียงเครื่องวัดชีพจรในโรงพยาบาล "ปี๊บ... ปี๊บ..." · รถเข็นผ่าน · แอร์หึ่ง

**🖼️ Image Prompt**
```
Interior of a Thai public hospital ward, PETE'S MOTHER: a frail Thai woman in her 50s
with short grey-streaked hair in a pale blue hospital gown lying in bed with a gentle
smile, holding PETE's hand, PETE in grey hoodie and thin glasses sitting on a plastic
stool looking down, heart monitor with a green line, a folded hospital bill on the
bedside table showing "280,000", soft cold fluorescent light, minimalist 2D flat vector
animation style, clean geometric character design, simple expressive faces, moody dim
vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① เครื่องวัดชีพจร ② ใบแจ้งค่าใช้จ่าย 280,000 ③ มือแม่จับมือพีท ④ พีทก้มหน้า

---

## ซีน 4 — 00:42–00:58 · ลุงมั่น และร้านเจริญศิลป์โฟโต้

**🎙️ Voiceover Script**
```
[tone: storytelling, a bit warmer]
จนวันหนึ่ง... ผมเห็นประกาศเล็ก ๆ ในกลุ่มเฟซบุ๊กของอำเภอ
"รับคนซ่อมรูปถ่าย กะดึก ค่าแรงดี"
[pause: 0.5s]
เจ้าของประกาศคือ... ลุงมั่น
เจ้าของร้านเจริญศิลป์โฟโต้... ร้านถ่ายรูปเก่าแก่หน้าวัด... ที่เปิดมาตั้งแต่รุ่นพ่อของแก
ลุงกำลังจะเข้าโรงพยาบาล... และต้องการคนเฝ้าร้านแทน
```
**🔊 SFX:** เสียงแจ้งเตือนมือถือ "ติ๊ง" · เสียงกริ่งประตูร้านกรุ๊งกริ๊ง · ไม้เท้าเคาะพื้น

**🖼️ Image Prompt**
```
Interior of the ground floor of an old wooden Thai photo shop, UNCLE MUN: an old Thai
man in his 70s, bald head with white side hair, thick white eyebrows, round glasses on
a cord, faded white short-sleeve shirt, brown slacks, leaning on a walking cane behind
a glass counter full of framed funeral portraits with black ribbons, PETE in grey hoodie
standing at the counter holding his phone, faded studio backdrop and an antique wooden
bellows camera on a tripod in the corner, warm dusty yellow light, minimalist 2D flat
vector animation style, clean geometric character design, simple expressive faces, moody
dim vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① หน้าจอมือถือโพสต์ประกาศ ② ป้ายร้านเก่า ③ ลุงมั่นยิ้มหลังเคาน์เตอร์ (ป้ายชื่อ) ④ กล้องไม้โบราณในมุมร้าน

---

## ซีน 5 — 00:58–01:20 · กฎเหล็กสามข้อ

**🎙️ Voiceover Script**
```
[old man, gruff and shaky]
"งานไม่ยากหรอก... แต่มีกฎสามข้อ... เอ็งต้องจำให้ขึ้นใจ"
[pause: 0.5s]
"ข้อหนึ่ง... ก่อนซ่อมรูปทุกครั้ง... จุดธูปหนึ่งดอก บอกกล่าวเขาก่อน... แล้วห้ามติหน้าตาคนตายเด็ดขาด"
"ข้อสอง... ห้ามจ้องตาคนในรูป... นานเกินห้าวินาที"
"ข้อสาม... หลังเที่ยงคืน... ใครมาเคาะ ห้ามเปิดประตูรับงานเพิ่ม"
[pause: 0.8s]
[tone: low, uneasy]
ผมหัวเราะในใจ... นึกว่าคนแก่ขี้กลัว
แต่ห้าพันต่อคืน... ผมไม่คิดจะถามอะไรอีก
```
**🔊 SFX:** ไฟแช็กจุดธูป "แชะ" · ระฆังวัดดังไกล ๆ หนึ่งครั้ง · นาฬิกาแขวนตีบอกเวลา

**🖼️ Image Prompt**
```
Close-up of UNCLE MUN's wrinkled hand holding up three fingers in front of PETE's face,
between them on the counter a small brass incense holder with one lit joss stick, a
stack of old photographs and a handwritten note card listing three rules in Thai,
UNCLE MUN's eyes serious behind round glasses, dusty warm light with a long shadow on
the wall behind, minimalist 2D flat vector animation style, clean geometric character
design, simple expressive faces, moody dim vintage Thai photo studio interior, subtle
eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① นิ้วหนึ่ง + ธูปหนึ่งดอก ② นิ้วสอง + ดวงตาในรูปถ่าย ③ นิ้วสาม + ประตูร้านปิด + นาฬิกา 00:00 ④ พีทยิ้มฝืด ๆ

---

## ซีน 6 — 01:20–01:38 · คืนที่หนึ่ง: ห้องทำงานชั้นสอง

**🎙️ Voiceover Script**
```
[tone: calm, observational]
คืนแรก... ผมขึ้นไปนั่งที่ห้องทำงานชั้นสอง
บันไดไม้แคบ ๆ... ลั่นเอี๊ยดทุกขั้น
ข้างบนมีคอมพิวเตอร์เครื่องเก่า... จอตู้สีครีม... สแกนเนอร์หนึ่งตัว
[pause: 0.5s]
และกระถางธูปเล็ก ๆ... วางอยู่ข้างแป้นพิมพ์
```
**🔊 SFX:** บันไดไม้ลั่นเอี๊ยดทีละขั้น · เสียงคอมพิวเตอร์เก่าบูตเครื่อง "หึ่ง... แกร๊ก" · พัดลมระบายความร้อนดังวี้ด

**🖼️ Image Prompt**
```
Upstairs workroom of an old wooden Thai photo shop at night, PETE in grey hoodie and
thin glasses sitting at a cluttered wooden desk facing an old beige computer with a
bulky CRT monitor glowing pale blue, flatbed scanner, a small incense holder beside the
keyboard, walls covered with old framed portraits, a single hanging bulb, steep wooden
staircase opening in the floor behind him disappearing into darkness, minimalist 2D flat
vector animation style, clean geometric character design, simple expressive faces, moody
dim vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① เท้าเหยียบบันไดไม้ ② จอ CRT สว่างขึ้น ③ ผนังเต็มไปด้วยรูปเก่า ④ ช่องบันไดมืดด้านหลังพีท

---

## ซีน 7 — 01:38–01:58 · รูปคุณยายที่เปียกน้ำ

**🎙️ Voiceover Script**
```
[tone: gentle]
งานแรกของผม... เป็นรูปขาวดำของคุณยายคนหนึ่ง
ชื่อเขียนไว้หลังรูปด้วยลายมือสั่น ๆ... "ยายผิน"
รูปเปียกน้ำมาจนหน้าเลือนไปครึ่งหนึ่ง... เหลือแค่ตาข้างเดียวกับรอยยิ้มจาง ๆ
[pause: 0.6s]
ผมทำตามกฎข้อหนึ่ง... จุดธูปหนึ่งดอก
[whispering]
"ขออนุญาตนะครับคุณยาย... ผมจะทำให้สวยที่สุด"
```
**🔊 SFX:** กระดาษรูปเก่ากรอบแกรบ · ไฟแช็กจุดธูป · เสียงสแกนเนอร์เลื่อนหัวอ่าน "วี้ดดด"

**🖼️ Image Prompt**
```
Top-down close-up on a wooden desk: a water-damaged black-and-white portrait of GRANDMA
PIN, an elderly Thai woman with hair in a neat bun and a lace blouse, half of her face
washed away into blurry stains, only one eye and a faint smile visible, shaky
handwriting on the back "ยายผิน", PETE's hands placing it on a flatbed scanner, one lit
joss stick with a thin curl of smoke beside it, minimalist 2D flat vector animation
style, clean geometric character design, simple expressive faces, moody dim vintage
Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① รูปเปียกในมือ ② ลายมือหลังรูป ③ จุดธูป ควันลอย ④ แสงสแกนเนอร์เลื่อนผ่านรูป

---

## ซีน 8 — 01:58–02:16 · รีทัชใบหน้า

**🎙️ Voiceover Script**
```
[tone: focused, calm]
ผมนั่งเติมใบหน้าคุณยายทีละนิด
แก้มทีละพิกเซล... ริ้วรอยทีละเส้น... ปอยผมทีละปอย
[pause: 0.5s]
เป็นงานที่ผมถนัดที่สุด... และผมเพลินจนลืมเวลา
[pause: 0.6s]
พอเงยหน้าดูนาฬิกาอีกที... ตีสองสิบห้า
```
**🔊 SFX:** คลิกเมาส์ถี่ ๆ · ปากกาแท็บเล็ตขีดเบา ๆ · นาฬิกาเดิน · ธูปไหม้ปะทุเบา ๆ

**🖼️ Image Prompt**
```
Over-the-shoulder view of PETE retouching on the old CRT monitor, a vintage photo
editing program open with the portrait of GRANDMA PIN being restored, left half of the
face already clean and gentle, right half still blurred and stained, cursor brush
hovering over the cheek, his reflection faint in the curved glass of the screen, a wall
clock in the background showing 2:15, minimalist 2D flat vector animation style, clean
geometric character design, simple expressive faces, moody dim vintage Thai photo studio
interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① หน้าจอ ก่อน/หลัง ② มือจับปากกาแท็บเล็ต ③ หน้าพีทจดจ่อ แสงจอสะท้อนแว่น ④ นาฬิกา 02:15

---

## ซีน 9 — 02:16–02:32 · ห้าวินาที

**🎙️ Voiceover Script**
```
[tone: slower, tightening]
เหลือส่วนสุดท้าย... ดวงตา
ผมซูมเข้าไป... เติมแววตาให้คุณยาย
[pause: 0.5s]
หนึ่ง... สอง... สาม...
[pause: 0.6s]
[hushed]
ผมลืมนับ.
```
**🔊 SFX:** นาฬิกาเดินดังขึ้นเรื่อย ๆ จนเหมือนอยู่ข้างหู · เสียงพัดลมคอมฯ ค่อย ๆ หายไป

**🖼️ Image Prompt**
```
Extreme close-up of the CRT monitor filling the frame with one restored eye of GRANDMA
PIN in black-and-white, soft and kind, the pixel grid faintly visible, PETE's glasses
reflection superimposed on the glass, the room around completely dark except the cold
screen glow, minimalist 2D flat vector animation style, clean geometric character design,
simple expressive faces, moody dim vintage Thai photo studio interior, subtle eerie
shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ดวงตาบนจอ ② ตัวเลข 1–2–3 ค่อย ๆ จาง (ซับ) ③ หน้าพีทนิ่ง ตาไม่กะพริบ

---

## ซีน 10 — 02:32–02:48 · รูม่านตาขยับ

**🎙️ Voiceover Script**
```
[tone: hushed, slow]
แล้วผมก็เห็นมัน...
รูม่านตาในรูป... ค่อย ๆ เลื่อน
จากที่มองตรงไปข้างหน้า...
[pause: 0.8s]
หันมามองที่ผม.
[pause: 1s]
มือผมแข็งค้างอยู่บนเมาส์... ขยับไม่ได้เลย
```
**🔊 SFX:** ความเงียบสนิท 1 วินาที · เสียงหึ่งไฟฟ้าแผ่ว ๆ จากจอ CRT · หัวใจเต้น

**🖼️ Image Prompt**
```
Same extreme close-up of GRANDMA PIN's black-and-white eye on the CRT screen, but the
pupil has shifted sideways and is now looking directly out at the viewer, faint glow
around the iris, PETE's frozen hand on an old beige mouse in the foreground, dark room,
minimalist 2D flat vector animation style, clean geometric character design, simple
expressive faces, moody dim vintage Thai photo studio interior, subtle eerie shadows,
16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ตาในรูปมองตรง ② (ช้า) รูม่านตาเลื่อนมาหากล้อง ③ มือแข็งบนเมาส์ ④ พีทกลั้นหายใจ

---

## ซีน 11 — 02:48–03:02 · เสียงจากลำโพงที่ไม่ได้เสียบปลั๊ก

**🎙️ Voiceover Script**
```
[tone: very low]
แล้วลำโพงข้างจอ... ก็มีเสียงออกมา
ทั้งที่สายของมัน... ห้อยอยู่ข้างโต๊ะ... ไม่ได้เสียบปลั๊ก
[pause: 0.8s]
[old woman, soft whisper]
"ขอบใจนะลูก... สวยเหมือนตอนสาว ๆ เลย"
```
**🔊 SFX:** เสียงซ่าแผ่ว ๆ จากลำโพง · เสียงกระซิบใส่รีเวิร์บเล็กน้อย · ธูปปะทุ "เปาะ"

**🖼️ Image Prompt**
```
Medium shot of the desk corner: two small beige computer speakers beside the CRT monitor,
their power cable dangling unplugged off the edge of the desk, faint sound-wave rings
drawn as pale circles coming out of one speaker, the restored portrait of GRANDMA PIN on
screen now smiling slightly wider, incense smoke bending toward the screen, minimalist 2D
flat vector animation style, clean geometric character design, simple expressive faces,
moody dim vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ลำโพง ② สายไฟห้อย ไม่ได้เสียบ ③ วงคลื่นเสียง ④ รอยยิ้มคุณยายบนจอ

---

## ซีน 12 — 03:02–03:14 · ถึงเช้า

**🎙️ Voiceover Script**
```
[tone: tired, shaken]
คืนนั้นผมนั่งนิ่งอยู่หน้าจอ... จนฟ้าสาง
ไม่กล้าลุก... ไม่กล้ามองจอ... และไม่กล้าปิดเครื่อง
[pause: 0.5s]
พอระฆังวัดตีตอนตีห้า... ผมถึงหายใจออก
```
**🔊 SFX:** ระฆังวัดยามเช้า · ไก่ขัน · นกร้อง · เสียงพระเดินบิณฑบาตไกล ๆ

**🖼️ Image Prompt**
```
Early dawn through the upstairs window of the old photo shop, pale blue and peach light,
PETE in grey hoodie slumped in his chair with dark circles under his eyes, hugging his
knees, the CRT monitor still on showing the finished portrait of GRANDMA PIN, outside the
window the temple roof with golden chofa ornaments and a monk walking with an alms bowl,
minimalist 2D flat vector animation style, clean geometric character design, simple
expressive faces, moody dim vintage Thai photo studio interior, subtle eerie shadows,
16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① หน้าต่าง ฟ้าเริ่มสว่าง ② พีทกอดเข่าบนเก้าอี้ ③ หลังคาโบสถ์ + พระบิณฑบาต

---

## ซีน 13 — 03:14–03:38 · หลานสาวคุณยาย

**🎙️ Voiceover Script**
```
[tone: gentle, slower]
สาย ๆ วันนั้น... หลานสาวคุณยายมารับรูป
เธอชื่อฝน... ใส่เสื้อดำ... ตาบวมมาจากบ้าน
พอผมยื่นกรอบรูปให้...
[pause: 0.8s]
เธอยืนนิ่งไปนาน... แล้วก็ร้องไห้โฮออกมากลางร้าน
[young woman, crying]
"ยายสั่งไว้ก่อนตาย... ว่าอยากมีรูปสวย ๆ ตั้งหน้าศพ... รูปเดียวที่มีก็เปียกน้ำตอนน้ำท่วม..."
"นี่มัน... หน้ายายตอนสาว ๆ เลยพี่"
```
**🔊 SFX:** กริ่งประตูร้าน · เสียงสะอื้น · เสียงกระดาษห่อกรอบรูป

**🖼️ Image Prompt**
```
Ground floor of the old photo shop in soft morning light, FON: a Thai woman in her
mid-20s with long straight hair tied back, black mourning blouse and red puffy eyes,
holding a framed restored portrait of GRANDMA PIN smiling beautifully, tears running down
her cheeks, PETE behind the glass counter looking moved and awkward, sunlight dust
particles, a small white jasmine garland on the frame, minimalist 2D flat vector animation
style, clean geometric character design, simple expressive faces, moody dim vintage Thai
photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ฝนเปิดประตูเข้าร้าน ② ยื่นกรอบรูป ③ ใบหน้าฝน น้ำตาไหล ④ รูปคุณยายในกรอบ (ยิ้ม)

---

## ซีน 14 — 03:38–03:52 · งานนี้... อาจไม่แย่

**🎙️ Voiceover Script**
```
[tone: reflective, warm]
วันนั้นผมเพิ่งเข้าใจ...
รูปหน้าศพ... ไม่ได้มีไว้ให้คนตายดู
มันมีไว้ให้คนที่ยังอยู่... ได้จำเขาในวันที่สวยที่สุด
[pause: 0.6s]
ผมบอกตัวเองว่า... ก็แค่ตาฝาด
[pause: 0.4s]
ผมคิดผิด.
```
**🔊 SFX:** โมบายลมหน้าร้านกรุ๊งกริ๊ง · เสียงถนนยามสาย

**🖼️ Image Prompt**
```
PETE standing alone in the doorway of the old photo shop looking across the street at
the temple, a funeral pavilion (sala) with white flower stands and a large framed portrait
on an altar visible inside the temple grounds, soft late-morning light, his long shadow
stretching back into the dim shop where the portraits on the wall seem to watch him,
minimalist 2D flat vector animation style, clean geometric character design, simple
expressive faces, moody dim vintage Thai photo studio interior, subtle eerie shadows,
16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ศาลาสวดศพในวัด รูปคุณยายบนโต๊ะหมู่ ② พีทยิ้มบาง ๆ ③ (ตัด) เงารูปบนผนังร้านด้านหลังเขา

---

## ซีน 15 — 03:52–04:12 · คืนที่สอง: ซองใต้ประตู

**🎙️ Voiceover Script**
```
[tone: calm, then uneasy]
คืนที่สอง... เที่ยงคืนสี่สิบ
ผมได้ยินเสียง... "แซ่ก"... ดังมาจากชั้นล่าง
[pause: 0.6s]
พอเดินลงไปดู... มีซองสีน้ำตาลซองหนึ่ง... ถูกสอดเข้ามาใต้ประตูร้าน
ข้างนอกเงียบสนิท... ไม่มีเสียงรถ... ไม่มีเสียงฝีเท้า... ไม่มีใครเลย
```
**🔊 SFX:** กระดาษถูไถกับพื้นไม้ "แซ่ก" · ฝีเท้าลงบันไดไม้ช้า ๆ · หมาหอนไกล ๆ

**🖼️ Image Prompt**
```
Low angle at floor level of the dark ground floor of the old photo shop, a brown paper
envelope lying just inside the closed wooden folding door, a thin strip of street light
leaking under the door, PETE's feet in slippers on the last step of the wooden staircase
in the background, framed funeral portraits on the walls lit only by the cold street
light, minimalist 2D flat vector animation style, clean geometric character design,
simple expressive faces, moody dim vintage Thai photo studio interior, subtle eerie
shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① นาฬิกา 00:40 ② ซองไถเข้ามาใต้ประตู ③ เท้าพีทลงบันได ④ ช่องแสงใต้ประตู ไม่มีเงาคน

---

## ซีน 16 — 04:12–04:34 · รูปใบขับขี่ของ "เก่ง"

**🎙️ Voiceover Script**
```
[tone: low, careful]
ในซองมีรูปใบขับขี่เก่า ๆ ของผู้ชายคนหนึ่ง... ชื่อเก่ง... อายุยี่สิบสาม
มีเงินสดสามพันบาท... เปียกชื้นเหมือนเพิ่งแช่น้ำ
และกระดาษโน้ตหนึ่งแผ่น
[whispering]
"ช่วยลบรอยช้ำบนหน้าให้หน่อย... พรุ่งนี้จะเอาไปตั้งงานศพ"
[pause: 0.6s]
ผมนึกถึงกฎข้อสาม... แต่ผมไม่ได้เปิดประตูนี่... มันสอดเข้ามาเอง
แล้วสามพันบาท... ก็คือค่ายาแม่อีกหนึ่งอาทิตย์
```
**🔊 SFX:** ฉีกซองกระดาษ · ธนบัตรเปียกแปะ ๆ · เสียงหยดน้ำหยดลงพื้น "ติ๋ง"

**🖼️ Image Prompt**
```
Top-down view of a dark wooden desk lit by a desk lamp: an opened brown envelope, an
old Thai driver's license style ID photo of KENG, a Thai man in his early 20s with short
spiky hair and a thin face in a plain white T-shirt with a faint purple bruise near his
left eye, three damp crumpled 1000-baht notes with water drops, a small handwritten note
in Thai, a wet ring stain spreading on the wood, minimalist 2D flat vector animation
style, clean geometric character design, simple expressive faces, moody dim vintage Thai
photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① รูปเก่ง (ป้ายชื่อ) ② ธนบัตรเปียก น้ำหยด ③ โน้ตลายมือ ④ พีทลังเล มองประตู

---

## ซีน 17 — 04:34–04:52 · จุดธูปบอกกล่าว

**🎙️ Voiceover Script**
```
[tone: calm, focused]
ผมจุดธูปหนึ่งดอกตามกฎ
"ขออนุญาตนะครับพี่เก่ง..."
[pause: 0.5s]
ผมสแกนรูปเข้าเครื่อง... หน้าเขาเขียวช้ำ... ปากแตก
ผมเกือบหลุดปากว่า "โห... หน้าเละขนาดนี้"
[pause: 0.6s]
[hushed]
แต่ผมนึกถึงกฎข้อหนึ่งได้ทัน... เลยกลืนคำนั้นลงคอไป
ธูปในกระถาง... ไหม้ไวผิดปกติ
```
**🔊 SFX:** จุดไฟแช็ก · สแกนเนอร์ทำงาน · ธูปไหม้ฉ่าเร็ว ๆ

**🖼️ Image Prompt**
```
Medium shot of PETE at the desk pressing his palms together in a respectful wai toward
a single lit joss stick, the CRT monitor beside him showing KENG's scanned ID photo
enlarged, bruise visible, the joss stick burning unusually fast with a long glowing ember
and thick smoke curling toward the screen, dark workroom, minimalist 2D flat vector
animation style, clean geometric character design, simple expressive faces, moody dim
vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ไหว้ธูป ② รูปเก่งบนจอ ③ พีทปิดปากตัวเอง ④ ธูปไหม้เร็วผิดปกติ

---

## ซีน 18 — 04:52–05:12 · ซูมพันเปอร์เซ็นต์

**🎙️ Voiceover Script**
```
[tone: focused, slowly tensing]
รอยช้ำส่วนใหญ่อยู่ใต้ตาซ้าย
ผมเลยซูมเข้าไป... สองร้อย... ห้าร้อย... หนึ่งพันเปอร์เซ็นต์
[pause: 0.5s]
ตอนนั้นเองที่ผมเห็น...
ในกระจกตาของเก่ง... มีอะไรสะท้อนอยู่
เป็นภาพเล็ก ๆ... เหมือนภาพสุดท้าย... ที่ตาคู่นั้นเห็นก่อนตาย
```
**🔊 SFX:** คลิกซูมทีละขั้น "แต๊ก... แต๊ก... แต๊ก" · หึ่งไฟฟ้าดังขึ้น

**🖼️ Image Prompt**
```
The CRT monitor showing the photo editor zoom indicator "1000%", the frame filled with
the pixelated dark eye of KENG, inside the glossy cornea a tiny curved reflection of a
scene is barely visible, PETE leaning very close to the glass with his glasses pushed up,
cold blue screen light on his face, minimalist 2D flat vector animation style, clean
geometric character design, simple expressive faces, moody dim vintage Thai photo studio
interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ตัวเลขซูม 200 → 500 → 1000% ② ดวงตาเป็นพิกเซล ③ เงาสะท้อนเล็ก ๆ ในกระจกตา ④ พีทโน้มเข้าหาจอ

---

## ซีน 19 — 05:12–05:32 · เงาสะท้อนในกระจกตา

**🎙️ Voiceover Script**
```
[tone: very low, slow]
ผมปรับความคมชัด... ทีละนิด
ภาพในกระจกตาค่อย ๆ ชัดขึ้น
[pause: 0.8s]
มันคือผู้ชายตัวใหญ่คนหนึ่ง... ใส่เสื้อกั๊กกู้ภัยสีส้ม
กำลังเงื้อท่อนเหล็ก... ขึ้นสูงเหนือหัว
[pause: 1s]
[whispering]
เก่ง... ไม่ได้รถล้มตาย
```
**🔊 SFX:** เสียงหัวใจเต้นดังขึ้น · โทนต่ำยาว (หรือเสียงลมหวีด) · ความเงียบก่อนประโยคสุดท้าย

**🖼️ Image Prompt**
```
A curved fisheye-like reflection inside a dark eye filling the frame: THE KILLER, a
broad-shouldered Thai man in his 40s with a buzz cut and thick neck wearing a generic
orange-and-black rescue volunteer vest with no logos, silhouetted against a roadside
street lamp at night, raising a metal pipe high above his head, a fallen motorcycle
behind him, rendered as a distorted mirror image, no blood, minimalist 2D flat vector
animation style, clean geometric character design, simple expressive faces, moody dim
vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① แถบความคมชัดเลื่อน ② ภาพในตาค่อย ๆ ชัด ③ เสื้อกั๊กสีส้ม ④ ท่อนเหล็กเงื้อสูง (ค้าง ไม่แสดงการฟาด)

---

## ซีน 20 — 05:32–05:56 · ข่าวที่ไม่ตรงกับภาพ

**🎙️ Voiceover Script**
```
[tone: investigative, tense]
ผมรีบหยิบมือถือ... เสิร์ชชื่อเก่ง
เจอข่าวท้องถิ่นเมื่อสามวันก่อน
"หนุ่มขี่มอเตอร์ไซค์ล้ม... หัวฟาดขอบถนน... เสียชีวิตคาที่"
[pause: 0.5s]
ในรูปประกอบข่าว... มีอาสากู้ภัยคนหนึ่ง... ยืนข้างร่างที่คลุมผ้าขาว
[pause: 0.8s]
[hushed]
ผู้ชายคนเดียวกัน... กับในกระจกตา
เขาเป็นคนพบศพ... และเป็นคนให้ข่าว
```
**🔊 SFX:** เสียงแตะจอมือถือ · เลื่อนหน้าจอ · โทนต่ำค้าง

**🖼️ Image Prompt**
```
Close-up of PETE's hand holding a smartphone in the dark, the screen showing a local Thai
news webpage with a headline about a motorcycle accident and a photo of a roadside scene
with a white sheet covering a body and THE KILLER in his orange-and-black rescue volunteer
vest standing beside it calmly, the CRT monitor in the background still showing the
reflection in KENG's eye, cold screen glow, minimalist 2D flat vector animation style,
clean geometric character design, simple expressive faces, moody dim vintage Thai photo
studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① พิมพ์ชื่อ "เก่ง" ② พาดหัวข่าว ③ รูปประกอบ: กู้ภัยยืนข้างผ้าขาว ④ เทียบภาพ: ข่าว / กระจกตา (แบ่งจอ)

---

## ซีน 21 — 05:56–06:16 · โทรศัพท์ที่ไม่ควรโทร

**🎙️ Voiceover Script**
```
[tone: regretful]
ผมทำเรื่องโง่ที่สุดในชีวิต...
ผมโทรไปเบอร์ศูนย์กู้ภัยที่อยู่ท้ายข่าว... ถามว่าใครเป็นคนพบศพเก่ง
[pause: 0.5s]
ปลายสายเงียบไปนาน...
[killer, low and calm]
"น้องถามทำไมครับ... แล้วน้องอยู่ร้านไหน"
[pause: 0.8s]
ผมวางสายทันที.
แต่ผมรู้... ว่าผมพูดชื่อร้านออกไปแล้ว ตั้งแต่ประโยคแรก
```
**🔊 SFX:** เสียงรอสาย "ตู๊ด... ตู๊ด..." · เสียงปลายสายมีลมหายใจหนัก ๆ · วางสาย "ติ๊ด"

**🖼️ Image Prompt**
```
Split-screen composition: left side PETE in the dark upstairs workroom holding a phone to
his ear, eyes wide behind his glasses, right side a dim roadside rescue volunteer station
at night with THE KILLER in his orange-and-black vest holding a phone, his face half in
shadow with a slow cold smile, a parked rescue pickup truck with an amber light behind
him, minimalist 2D flat vector animation style, clean geometric character design, simple
expressive faces, moody dim vintage Thai photo studio interior, subtle eerie shadows,
16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① พีทโทร ② ปลายสาย: มือหนา ๆ ถือโทรศัพท์ ③ ครึ่งหน้าฆาตกรยิ้ม ④ พีทวางสาย มือสั่น

---

## ซีน 22 — 06:16–06:36 · คืนที่สาม: เสียงบันได

**🎙️ Voiceover Script**
```
[tone: tense, quiet]
คืนที่สาม... ตีหนึ่งครึ่ง
ผมก๊อปรูปเก่งกับภาพที่ซูมไว้... ลงแฟลชไดรฟ์
ตั้งใจว่าเช้านี้... จะเอาไปให้ตำรวจ
[pause: 0.8s]
แล้วผมก็ได้ยิน...
[whispering]
เอี๊ยด...
[tone: very low]
บันไดไม้ขั้นแรก... ลั่น
ทั้งที่ประตูร้านข้างล่าง... ผมล็อกไว้เอง
```
**🔊 SFX:** เสียงไฟล์ก๊อปเสร็จ "ติ๊ง" · บันไดไม้ลั่นขั้นแรก · ความเงียบ · ลั่นอีกขั้น

**🖼️ Image Prompt**
```
Interior of the upstairs workroom at 1:30 AM, PETE frozen at the desk holding a small USB
flash drive, the CRT screen glowing, his head turned toward the dark opening of the steep
wooden staircase in the floor behind him, a faint orange glow of a flashlight climbing
the wall of the stairwell from below, wall clock showing 1:30, minimalist 2D flat vector
animation style, clean geometric character design, simple expressive faces, moody dim
vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① แถบก๊อปไฟล์ 100% ② ถอดแฟลชไดรฟ์ ③ ช่องบันไดมืด แสงไฟฉายสีส้มไต่ขึ้น ④ พีทหันขวับ

---

## ซีน 23 — 06:36–06:58 · ผู้มาเยือนหลังเที่ยงคืน

**🎙️ Voiceover Script**
```
[tone: urgent, hushed]
ผมวิ่งไปล็อกประตูห้องทำงาน... ลากโต๊ะมาดันไว้
[pause: 0.4s]
ปัง! ปัง! ปัง!
[killer, shouting]
"น้อง! กู้ภัยครับ! พี่เอาแฟลชไดรฟ์มาส่งงานเพิ่ม! เปิดประตูหน่อย!"
[pause: 0.6s]
[tone: low, fast]
กฎข้อสาม... หลังเที่ยงคืน ห้ามเปิดประตูรับงานเพิ่ม
ตอนนั้นผมเพิ่งเข้าใจ... ว่ากฎข้อนั้นไม่ได้มีไว้กันผี
```
**🔊 SFX:** ลากโต๊ะไม้ครูดพื้น · ทุบประตูไม้ดังสนั่น 3 ครั้ง · เสียงตะโกนอู้อี้ผ่านประตู

**🖼️ Image Prompt**
```
PETE pushing a heavy wooden desk against a shaking wooden door in the cramped upstairs
workroom, the door vibrating with impact lines drawn around it, an orange flashlight beam
leaking through the gap under the door, the shadow of two large feet visible in the gap,
framed portraits on the wall tilted by the shaking, minimalist 2D flat vector animation
style, clean geometric character design, simple expressive faces, moody dim vintage Thai
photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① พีทลากโต๊ะ ② ประตูสั่นจากการทุบ ③ เงาเท้าใต้ประตู ④ รูปบนผนังเอียง

---

## ซีน 24 — 07:00–07:20 · ชะแลง

**🎙️ Voiceover Script**
```
[urgent, breathless]
ผมกดเบอร์หนึ่งเก้าหนึ่ง... มือสั่นจนกดผิดสองรอบ
[pause: 0.3s]
เสียงทุบเงียบไป...
แล้วก็มีเสียงเหล็ก... งัดเข้ามาที่ร่องประตู
[killer, shouting]
"ไอ้เด็กเวร! มึงไม่น่ายุ่งเรื่องของกูเลย!"
[pause: 0.4s]
แกร๊ก! ประตูไม้แตก... โต๊ะถูกดันกระเด็น
```
**🔊 SFX:** กดโทรศัพท์ · ชะแลงงัดไม้ดังเอี๊ยดดด · ไม้แตก "แคร็ก" · โต๊ะล้ม ของหล่นกระจาย

**🖼️ Image Prompt**
```
Close-up of the edge of the wooden door as the flat end of an iron crowbar is wedged
through the splintering gap, wood chips flying as flat geometric shards, PETE in the
background backing away against the wall with his phone to his ear, the desk sliding
across the floor, harsh orange light bursting through the crack, minimalist 2D flat
vector animation style, clean geometric character design, simple expressive faces,
moody dim vintage Thai photo studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① หน้าจอโทร 191 ② ปลายชะแลงโผล่ร่องประตู ③ ประตูแตก ④ โต๊ะกระเด็น

---

## ซีน 25 — 07:20–07:38 · มีด

**🎙️ Voiceover Script**
```
[urgent, breathless]
เขาพุ่งเข้ามา... ตัวใหญ่จนบังแสงไฟทั้งห้อง
ในมือมีมีดเล่มหนึ่ง... สะท้อนแสงจอคอม
ผมถอยจนหลังชนกล้องไม้โบราณของลุงมั่น... ไม่มีทางหนีแล้ว
[pause: 0.5s]
[tone: very low]
เขาเงื้อมีดขึ้น...
```
**🔊 SFX:** ฝีเท้าหนักพุ่งเข้ามา · ขาตั้งกล้องไม้ลั่น · หัวใจเต้นรัว แล้วหยุด

**🖼️ Image Prompt**
```
Low-angle dramatic shot from behind PETE pressed against an antique wooden bellows camera
on a tripod, THE KILLER, a broad-shouldered Thai man in his 40s with buzz cut wearing an
orange-and-black rescue volunteer vest, filling the broken doorway and raising a knife,
the blade catching the cold blue glow of the CRT monitor, his shadow stretching huge over
the portraits on the wall, no blood, minimalist 2D flat vector animation style, clean
geometric character design, simple expressive faces, moody dim vintage Thai photo studio
interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ร่างใหญ่บังประตู ② มีดสะท้อนแสงจอ ③ หลังพีทชนกล้องโบราณ ④ มีดเงื้อสูง (ค้าง)

---

## ซีน 26 — 07:38–08:04 · แสงแฟลช

**🎙️ Voiceover Script**
```
[tone: sudden, then hushed]
แปลบ!
[pause: 0.5s]
แฟลชของกล้องโบราณข้างหลังผม... สว่างวาบขึ้นเอง
ทั้งห้องขาวโพลน...
[pause: 0.8s]
[whispering]
และในแสงนั้น... มีผู้ชายคนหนึ่งยืนขวางหน้าผมไว้
เสื้อยืดสีขาว... เปื้อนเลือดเต็มตัว
[pause: 0.6s]
เก่ง.
```
**🔊 SFX:** แฟลชหลอดแมกนีเซียมโบราณ "ฟึ่บ-แปลบ" · เสียงหวีดในหูหลังแสงจ้า · ความเงียบ

**🖼️ Image Prompt**
```
The whole frame washed in white flash light, high-contrast silhouettes: the antique
bellows camera's flash pan bursting with light behind PETE, and between PETE and THE
KILLER stands the translucent pale figure of KENG, a young Thai man with short spiky hair
in a white T-shirt stained dark red, arms spread to shield PETE, back to the camera,
THE KILLER recoiling with his arm over his eyes, minimalist 2D flat vector animation style,
clean geometric character design, simple expressive faces, moody dim vintage Thai photo
studio interior, subtle eerie shadows, 16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① แฟลชระเบิดแสง (ขาวทั้งจอ 2–3 เฟรม) ② เงาเก่งกางแขน ③ ฆาตกรยกแขนบังตา ④ หน้าเก่งหันมองพีทแวบหนึ่ง (เศร้า ไม่น่ากลัว)

---

## ซีน 27 — 08:04–08:30 · ตกบันได

**🎙️ Voiceover Script**
```
[urgent]
ผู้ชายคนนั้นร้องลั่น... ยกแขนปิดตา... ถอยหลังพรวด
ส้นเท้าเขาพลาดขอบบันได...
[pause: 0.4s]
แล้วร่างทั้งร่าง... ก็ร่วงลงบันไดไม้ชันไปทั้งตัว
โครม... โครม... แล้วก็เงียบ
[pause: 1s]
[tone: tired, calmer]
สิบนาทีต่อมา... เสียงไซเรนก็ดังมาถึงหน้าวัด
เขานอนสลบอยู่ตีนบันได... ตำรวจใส่กุญแจมือเขาไปทั้งอย่างนั้น
ส่วนแฟลชไดรฟ์ในมือผม... กลายเป็นหลักฐานชิ้นสำคัญ
```
**🔊 SFX:** ร้องตกใจ · กลิ้งตกบันไดไม้ดังโครมคราม · ความเงียบ · ไซเรนตำรวจไกลแล้วใกล้ · วิทยุสื่อสาร

**🖼️ Image Prompt**
```
Ground floor of the old photo shop at night lit by red and blue police lights through
the open front door, THE KILLER lying unconscious at the bottom of the steep wooden
staircase with a crowbar beside him, two Thai police officers in brown uniforms
handcuffing him, PETE standing at the top of the stairs holding the USB flash drive,
a single framed portrait of KENG leaning against the shop counter, no blood, minimalist
2D flat vector animation style, clean geometric character design, simple expressive
faces, moody dim vintage Thai photo studio interior, subtle eerie shadows, 16:9
widescreen --ar 16:9
```
**🎬 ช็อตย่อย:** ① ส้นเท้าพลาดขอบบันได ② (นอกจอ) เสียงกลิ้งตก + เงาบนผนัง ③ ไฟไซเรนสาดเข้าร้าน ④ พีทยื่นแฟลชไดรฟ์ให้ตำรวจ

---

## ซีน 28 — 08:30–09:30 · หนึ่งเดือนต่อมา... และโทรศัพท์จากลุงมั่น

**🎙️ Voiceover Script**
```
[tone: warm, relieved]
หนึ่งเดือนต่อมา... แม่ผ่าตัดเสร็จเรียบร้อย
หมอบอกว่าหัวใจแม่... แข็งแรงกว่าเดิมเยอะ
ส่วนผม... ตัดสินใจรับช่วงร้านเจริญศิลป์โฟโต้ต่อจากลุงมั่น
งานซ่อมรูปหน้าศพ... กลายเป็นงานที่ผมภูมิใจที่สุด
[pause: 0.8s]
[tone: calm, then slowly darkening]
จนเย็นวันหนึ่ง... ขณะที่ผมนั่งทำงานอยู่ชั้นสอง
ลุงมั่นโทรมาจากโรงพยาบาล
[old man, gruff and shaky]
"ไอ้พีท... เอ็งยังนั่งทำงานอยู่ชั้นสองเหรอ"
"คอมพิวเตอร์เครื่องนั้นน่ะ... มันพังไปตั้งแต่ห้าปีก่อนแล้ว"
"ลุงถอดฮาร์ดดิสก์ทิ้งไปตั้งนานแล้ว..."
[pause: 1s]
[old man, trembling, fearful]
"แล้วสามคืนที่ผ่านมา... เอ็งเปิดโปรแกรมซ่อมรูป... จากเครื่องไหน?!"
[pause: 2s]
```
**🔊 SFX:** นกร้องยามเย็น · เสียงโทรศัพท์บ้านแบบเก่าดังกริ๊ง · ช่วงพูดของลุงมั่น: พัดลมคอมฯ ที่เคยดัง ค่อย ๆ เงียบหายไป · จบด้วยความเงียบสนิท แล้วตัดดำ

**🖼️ Image Prompt**
```
Upstairs workroom of the old photo shop at dusk with warm orange window light turning
cold, PETE in grey hoodie holding an old phone receiver to his ear, his face drained of
color, the old beige computer case beside the desk has its side panel open revealing an
empty dusty slot where the hard drive should be, cobwebs inside, yet the CRT monitor is
still glowing pale blue showing the photo editor with a new blank portrait file open,
minimalist 2D flat vector animation style, clean geometric character design, simple
expressive faces, moody dim vintage Thai photo studio interior, subtle eerie shadows,
16:9 widescreen --ar 16:9
```
**🎬 ช็อตย่อย:**
① แม่ยิ้มบนเตียง หลังผ่าตัด (สว่าง อบอุ่น) ② พีทเปิดร้าน ป้าย "เจริญศิลป์โฟโต้" ③ ผนังร้านมีรูปคุณยายผินกับรูปเก่งในกรอบ (ยิ้ม) ④ โทรศัพท์ดัง ⑤ หน้าพีทซีด ⑥ ข้างเคสคอม: ช่องฮาร์ดดิสก์ว่าง หยากไย่ ⑦ จอ CRT ยังสว่างอยู่... เปิดไฟล์รูปใหม่ขึ้นมาเอง ⑧ ตัดดำ

> 📝 **End card (2 วิ):** พื้นดำ ข้อความ "รับจ้างซ่อมรูปถ่ายหน้าศพ" — ไม่มีเสียงพากย์

---

## สรุปโครงเรื่องและเวลา

| ช่วง | ซีน | เวลาโดยประมาณ | อารมณ์ |
|---|---|---|---|
| The Hook | 1–5 | 00:00–01:20 | สงสัย → เห็นใจ (แม่) → อยากรู้ (กฎ 3 ข้อ) |
| คืนที่ 1 · รูปคุณยาย | 6–14 | 01:20–03:52 | สงบ → ขนลุก (ตาขยับ) → ซึ้ง (หลานสาว) |
| คืนที่ 2 · กระจกตา | 15–21 | 03:52–06:16 | สงสัย → ช็อก (เงาในตา) → สืบ → พลาด (โทรศัพท์) |
| คืนที่ 3 · ผู้มาเยือน | 22–27 | 06:16–08:30 | กดดัน → ระทึก → ปาฏิหาริย์ (แฟลช) → โล่ง |
| Ending & Cliffhanger | 28 | 08:30–09:30 | อบอุ่น → เย็นวาบ → ตัดจบ |

**ปมที่ปูไว้ (เพื่อให้ตอนจบหักมุมแล้ว "แฟร์")**
- จอ CRT "บูตเครื่องเสียงแปลก ๆ" (ซีน 6) และลำโพงไม่ได้เสียบปลั๊กแต่มีเสียง (ซีน 11) → ใบ้ว่าเครื่องนี้ไม่ได้ทำงานด้วยไฟฟ้าปกติ
- ซองถูกสอดใต้ประตูโดยไม่มีคน และเงินเปียกน้ำ (ซีน 15–16) → เก่งมาเอง
- กล้องไม้โบราณถูกโชว์ตั้งแต่ซีน 4 → ได้ใช้ในซีน 26
- กฎข้อสาม "ห้ามเปิดประตูหลังเที่ยงคืน" ถูกตีความใหม่ในซีน 23 ว่าไม่ได้มีไว้กันผีอย่างเดียว

**ข้อควรระวังในการผลิต**
- ฉากรุนแรง (ซีน 19, 25–27) ไม่แสดงการฟาด/แทงจริง ใช้ภาพค้างก่อนลงมือ แสงแฟลช และเสียงแทน → ลดความเสี่ยงถูกจำกัดอายุผู้ชม
- เสื้อกู้ภัยในภาพ **ห้ามใส่โลโก้มูลนิธิจริง** (ใช้สีส้ม-ดำทั่วไป) เพื่อไม่ให้พาดพิงองค์กรจริง
- เบอร์ "191" เป็นเบอร์แจ้งเหตุจริงของไทย ใช้ได้ในบท
