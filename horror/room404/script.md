# เสียงเคาะจากห้อง 404 (The Knock from Room 404)

คลิปเล่าเรื่องสยองขวัญแนวนอน 16:9 · ความยาวเป้าหมาย ~7 นาที · 24 ซีน
โทน: ระทึกขวัญ สืบสวน ความเชื่อผีไทย · บรรยากาศ: อพาร์ตเมนต์เก่า ฝนพรำ นีออนเขียวหม่น + เหลืองซีด

---

## ตัวละครอ้างอิง (Character Reference — ใช้คำบรรยายเดิมทุกซีนเพื่อให้หน้าตาคงที่)

| ตัวละคร | คำบรรยายภาษาอังกฤษสำหรับ Prompt |
|---|---|
| **เอก** (ช่างซ่อมบำรุงกะดึก 30 ปี) | `EK: a 30-year-old Thai man, short messy black hair, light stubble, tired sharp eyes, faded navy-blue maintenance work shirt with a name patch, tool belt, holding a small LED flashlight` |
| **เสี่ยวิโรจน์** (เจ้าของตึก) | `THE LANDLORD: a heavyset Thai man in his 60s, slicked-back grey hair, thick gold chain, white undershirt under an open dark batik shirt, heavy jowls, small cold eyes` |
| **ป้าศรี** (แม่บ้านเก่าแก่) | `PA SRI: a thin elderly Thai housekeeper in her 60s, grey hair in a tight bun, faded floral blouse, checkered pha-sin sarong, worn apron, deeply lined anxious face` |
| **ดาว** (ลูกสาวเจ้าของตึก) | `DAO: an emaciated Thai woman in her early 20s, sunken cheeks, long tangled black hair, torn pale-blue shirt, wrists and ankles bound with nylon rope, duct tape hanging from her mouth` |
| **ผีชุดขาว** (วิญญาณในผนัง) | `THE WOMAN IN WHITE: a pale grey-skinned woman in a long white cotton nightgown, very long wet black hair, no visible wounds on her neck, face mostly hidden` |
| **ห้อง 404 / ตึก** | `a rundown 1990s Thai low-rise apartment block, stained concrete, mint-green tiled corridors, flickering fluorescent tubes, rusted steel accordion gates, wooden door numbered 404 with a rusty padlock and faded red talisman paper` |

**คำท้าย Prompt ภาพทุกซีน (ใส่ตรงตามนี้):**
`cinematic Thai horror film style, moody teal and sickly yellow lighting, 35mm film grain, photorealistic, 8k, --ar 16:9`

---

# ส่วนที่ 1 — Google AI Studio Voice Director Prompt

> **วิธีใช้ใน AI Studio:** เมนู *Generate speech* → ช่อง **Style instructions** (โมเดล TTS ของ Gemini ไม่รับ System Instruction แบบโมเดลแชต ให้วางข้อความนี้ในช่องสไตล์ หรือวางไว้ "เหนือบท" ตามรูปแบบ Director's notes ด้านล่าง)
> **เสียงแนะนำ:** `Charon` (ทุ้ม สุขุม) หรือ `Algenib` (ทุ้มแหบ) — ลองทั้งคู่กับซีน 1 ก่อนเจนทั้งเรื่อง
> **แบ่งเจนทีละ 2–4 ซีน** (ไม่เกิน ~1,400 ตัวอักษรต่อครั้ง) บทยาวเกินโมเดลมักตัดจบกลางทาง
> **ถ้าโมเดลอ่านแท็กออกเสียง** (เช่น อ่านคำว่า "pause") ให้เปลี่ยนแท็กหยุดเป็นแบบมาตรฐาน `[short pause]` / `[medium pause]` / `[long pause]` แทนตัวเลขวินาที

```text
# AUDIO PROFILE: "The Midnight Storyteller"
A seasoned Thai male ghost-story narrator in his late 40s, the kind of voice that
hosts a famous late-night Thai radio horror program. Deep, low, warm baritone with
a slight gravel in the lower register. He sounds calm, unhurried and completely in
control — never theatrical, never screaming. His calmness is what makes listeners
afraid.

# THE SCENE
Two o'clock in the morning in a small, dark recording booth in Bangkok. Rain is
tapping on the window. A single desk lamp. He leans close to the microphone, as if
telling this story to one listener who is sitting alone in a dark room. He knows
how the story ends, and he is in no hurry to get there.

# DIRECTOR'S NOTES
Language: Thai only. Natural, polite, spoken Central Thai. Pronounce every word
exactly as spelled; numbers are written out as Thai words — read them as written.

Baseline delivery:
- Low pitch, close-mic intimacy, soft volume. Speak about 15% slower than normal
  conversation.
- Let sentences end on a falling, heavy tone, as if setting something down quietly.
- Breathe audibly but gently before important lines. Silence is part of the story.

Pacing and pauses (critical):
- "..." means a held, pressured silence — stop completely, do not trail off.
- A line break means a short breath.
- [pause: Xs] or [short/medium/long pause] means total silence for that duration.
  Never read any bracketed tag aloud.
- Before every reveal, slow down word by word, then deliver the key word softly,
  not loudly. Fear comes from restraint.

Light and shade (ผ่อนหนักผ่อนเบา):
- Exposition and flashback: warm, curious, almost conversational, like recalling
  something that happened to a friend.
- Building dread: tighten the voice, lower the volume, shorten the breaths.
- Panic or chase moments: faster, breathless, clipped phrases, rising tension —
  but still controlled, never shouting.
- Aftermath: tired, quiet, slightly sad and reflective.

Character voices (switch only when a bracketed tag asks for it):
- [whispering]: drop almost to breath, very close to the mic, airy, slow.
- [old woman, trembling whisper]: Pa Sri — frail, shaky, frightened, conspiratorial.
- [landlord, cold and smooth]: slow, oily, menacing calm, a hint of a smile.
- [weak, hoarse]: Dao — dry throat, cracked, barely able to speak.
- [ghostly whisper, far away]: the spirit — thin, breathy, slightly delayed,
  emotionless but gentle, as if from behind a wall.
- Sound words such as "ก๊อก... ก๊อก... ก๊อก..." are spoken softly and evenly, with
  a full second of silence between each one, imitating a slow knock.

Never: laugh, add words, add music cues, or read tags. Never sound like an
advertisement or a news reader. The tone is a story told in the dark.
```

---

# ส่วนที่ 2 — บทพากย์และภาพรายซีน (24 ซีน)

---

## ซีน 1 — 00:00–00:18 · Cold Open: ประตูที่ไม่ควรเปิด

**🎙️ Voiceover Script**
```
[tone: tense, low pitch, slow]
ตีสอง... สิบเจ็ดนาที
[pause: 1s]
ฝนยังตกไม่หยุด... ตั้งแต่หัวค่ำ
[pause: 0.8s]
ทางเดินชั้นสี่ ของอพาร์ตเมนต์เก่าแห่งนี้... เงียบจนได้ยินเสียงไฟนีออน... กะพริบ
[pause: 1s]
และที่หน้าประตูห้องสุดทางเดิน... ชายคนหนึ่ง... กำลังยืนตัวสั่น
```

**🔊 SFX:** ฝนตกพรำกระทบหลังคาสังกะสี · เสียงหึ่ง/แปะ ๆ ของหลอดนีออนกะพริบ · น้ำหยดจากรางน้ำ · ลมหวีดเบา ๆ ผ่านช่องลม

**🖼️ Image Prompt**
```
Wide establishing shot down a long, narrow fourth-floor corridor of a rundown 1990s
Thai apartment block at 2 AM, mint-green wall tiles stained with mildew, wet concrete
floor reflecting light, one fluorescent tube flickering overhead, rain pouring past
an open breezeway on the left, at the far end a lone silhouette of EK: a 30-year-old
Thai man in a faded navy-blue maintenance shirt with a tool belt, standing before a
wooden door numbered 404 with faded red talisman paper, low camera height, deep
shadows, cinematic Thai horror film style, moody teal and sickly yellow lighting,
35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Very slow dolly forward down the corridor toward the man; fluorescent light flickers irregularly; rain streaks fall in the breezeway; no character movement except a slight shoulder tremble.`

---

## ซีน 2 — 00:18–00:38 · แม่กุญแจขึ้นสนิม

**🎙️ Voiceover Script**
```
[tone: hushed, deliberate]
เขาชื่อ... เอก
ช่างซ่อมบำรุงกะดึก... อายุสามสิบปี
[pause: 0.8s]
ในมือของเขา... คือกุญแจสำรอง... ที่เขาแอบขโมยมา
[pause: 1s]
ส่วนตรงหน้า... คือห้องสี่ศูนย์สี่
ห้องที่ถูกล็อกปิดตาย... มาสามปีเต็ม
[pause: 1.2s]
[slower, almost whispering]
แกร๊ก...
```

**🔊 SFX:** พวงกุญแจกระทบกัน · ไขกุญแจฝืด ๆ เสียงเหล็กขูดสนิม · แม่กุญแจหลุด "แกร๊ก" · หัวใจเต้นช้า ๆ เริ่มดังขึ้น

**🖼️ Image Prompt**
```
Extreme close-up of trembling male hands of a Thai maintenance worker inserting a
small brass key into a heavily rusted padlock on a steel hasp, flaking orange rust,
a torn red Thai talisman paper with black yantra script glued across the door gap,
flashlight beam clenched under his arm casting a harsh cone, raindrops on his
knuckles, door number 404 blurred in the background, shallow depth of field,
cinematic Thai horror film style, moody teal and sickly yellow lighting, 35mm film
grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Macro shot, the key turns slowly with resistance, the padlock snaps open and swings down, the talisman paper tears slightly; subtle handheld shake.`

---

## ซีน 3 — 00:38–01:00 · กลิ่นธูป และเสียงเคาะ

**🎙️ Voiceover Script**
```
[tone: tense, low pitch]
ทันทีที่ประตูแง้มออก...
กลิ่นแรกที่ลอยมาปะทะจมูก... คือกลิ่นธูป
[pause: 0.8s]
แต่ใต้กลิ่นธูปนั้น... มีอีกกลิ่นหนึ่ง
คาว... เหมือนเลือด
[pause: 1.5s]
แล้วเสียงนั้น... ก็ดังขึ้น
[pause: 1s]
[whispering, eerie, even rhythm]
ก๊อก... ก๊อก... ก๊อก...
[pause: 1.5s]
[tone: low, ominous]
มันไม่ได้ดังมาจากประตู... มันดังมาจาก... ในตู้เสื้อผ้า
```

**🔊 SFX:** บานพับประตูครางยาว · ฝนเงียบลงกะทันหัน (ดรอปเสียงบรรยากาศ) · เคาะไม้ทึบ 3 ครั้งเว้นจังหวะเท่ากัน · ลมหายใจกลั้นของเอก

**🖼️ Image Prompt**
```
Over-the-shoulder shot from behind EK as the door of room 404 creaks open into
darkness, thin wisps of incense smoke curling out into the corridor, inside an
abandoned Thai studio room with a sheet-covered bed, dusty floor, a burnt-out joss
stick holder on a small shelf, and at the far wall a tall old teak wardrobe with
its doors shut, flashlight beam landing on the wardrobe, the wardrobe door slightly
vibrating, cinematic Thai horror film style, moody teal and sickly yellow lighting,
35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Door swings open slowly, smoke drifts toward camera, slow push-in on the wardrobe; on each knock the wardrobe door gives a tiny jolt; hold on the wardrobe, then hard cut to black for the title card.`

> 📝 **Title card (1.5 วิ):** "เสียงเคาะจากห้อง 404" ตัวอักษรขาวซีดบนพื้นดำ

---

## ซีน 4 — 01:00–01:15 · ย้อนกลับไปสองคืนก่อน

**🎙️ Voiceover Script**
```
[tone: calm, storytelling, warmer]
แต่ก่อนจะไปถึงคำตอบว่าอะไรอยู่ในตู้นั้น...
[pause: 0.8s]
เราต้องย้อนกลับไป... สองคืนก่อนหน้า
[pause: 0.6s]
คืนแรกที่เอก... เริ่มงานที่ตึกหลังนี้
```

**🔊 SFX:** เสียงม้วนเทปกรอกลับ/ลมหวีดย้อน (ทรานซิชัน) · ฝนเบาลง · รถมอเตอร์ไซค์ขับผ่านถนนเปียกไกล ๆ

**🖼️ Image Prompt**
```
Exterior wide shot at dusk of a five-storey rundown Thai apartment building on a
narrow soi, rain-slicked street, tangled electrical wires overhead, a buzzing green
neon sign reading in Thai "ห้องพักรายเดือน", laundry hanging from rusted balcony
grilles, a 7-Eleven glow in the distance, EK walking toward the gate with a
backpack, cinematic Thai horror film style, moody teal and sickly yellow lighting,
35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Slow crane down from the building's top floor to street level as EK walks in from the right; neon sign buzzes and flickers; light rain.`

---

## ซีน 5 — 01:15–01:38 · คำสั่งของเจ้าของตึก

**🎙️ Voiceover Script**
```
[tone: calm narration]
เจ้าของตึก... คือเสี่ยวิโรจน์
ชายวัยหกสิบ... ผู้มีรอยยิ้มที่ไม่เคยไปถึงดวงตา
[pause: 0.8s]
[landlord, cold and smooth]
"งานแกมีแค่นี้... ไฟเสีย ท่อตัน ซ่อมให้หมด"
[pause: 0.5s]
"แต่ห้องสี่ศูนย์สี่... ห้ามเข้าใกล้เด็ดขาด... ท่อน้ำมันแตก"
[pause: 1s]
[tone: low, suspicious]
แปลก... ห้องที่ท่อแตกมาสามปี... ทำไมพื้นทางเดินหน้าห้อง... กลับแห้งสนิท
```

**🔊 SFX:** ห้องทำงานเล็ก พัดลมเพดานหมุนเอี๊ยด · พวงกุญแจถูกโยนลงโต๊ะไม้ · ทีวีมวยไทยเปิดเบา ๆ

**🖼️ Image Prompt**
```
Medium shot in a cramped Thai landlord's ground-floor office, THE LANDLORD: a
heavyset Thai man in his 60s with slicked-back grey hair, thick gold chain, white
undershirt under an open dark batik shirt, sitting behind a cluttered wooden desk,
smiling thinly but with cold eyes, pointing a fat finger at EK standing across the
desk, a wall board of hanging room keys where the hook for 404 is empty, a small
Buddha shrine with fresh marigolds, ceiling fan above, cinematic Thai horror film
style, moody teal and sickly yellow lighting, 35mm film grain, photorealistic, 8k,
--ar 16:9
```
**🎬 Motion Prompt:** `Slow push-in on the landlord's face as he speaks; ceiling fan shadows sweep across the desk; finish with a quick rack focus to the empty key hook labeled 404.`

---

## ซีน 6 — 01:38–02:00 · ผู้หญิงที่ระเบียง

**🎙️ Voiceover Script**
```
[tone: hushed, building dread]
คืนนั้น... ราวเที่ยงคืน
เอกเดินตรวจไฟที่ลานจอดรถด้านหลังตึก
[pause: 0.8s]
แล้วเขาก็เงยหน้าขึ้นไปเห็น...
[pause: 1.2s]
ผู้หญิงคนหนึ่ง... ในชุดนอนสีขาว
ยืนหันหลัง... อยู่ที่ระเบียงชั้นสี่
[pause: 0.8s]
[whispering]
ค่อย ๆ... แปรงผมยาวสีดำ... ช้า ๆ... ทีละครั้ง
[pause: 1s]
[tone: low]
ระเบียงนั้น... เป็นของห้องสี่ศูนย์สี่
```

**🔊 SFX:** ฝนพรำ · เสียงแปรงหวีลากผ่านเส้นผม (เบามาก ใกล้หู) · จิ้งหรีดเงียบลงทันที · ลมหวีด

**🖼️ Image Prompt**
```
Low-angle shot from a wet rear parking lot looking up at the fourth-floor balcony of
an old Thai apartment block at midnight, rusted balcony grille, THE WOMAN IN WHITE:
a pale woman in a long white cotton nightgown with very long wet black hair standing
with her back to the camera, slowly brushing her hair with an old wooden brush,
backlit by a dim sickly yellow glow from inside the sealed room, rain streaks in the
foreground, EK small in the bottom of the frame looking up with a flashlight,
cinematic Thai horror film style, moody teal and sickly yellow lighting, 35mm film
grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Slow tilt up from EK to the balcony; the woman brushes her hair in slow, unnatural, perfectly repeated strokes; she never turns; rain falls steadily.`

---

## ซีน 7 — 02:00–02:18 · สมุดป้อมยาม

**🎙️ Voiceover Script**
```
[tone: curious, slightly faster]
เอกรีบเดินกลับไปที่ป้อมยามหน้าตึก
เปิดสมุดรายชื่อผู้เช่าเล่มหนา... ไล่นิ้วลงทีละบรรทัด
[pause: 0.8s]
ห้องสี่ศูนย์หนึ่ง... สี่ศูนย์สอง... สี่ศูนย์สาม...
[pause: 1s]
[tone: low, chilled]
ห้องสี่ศูนย์สี่... ว่างเปล่า
[pause: 0.5s]
ไม่มีชื่อผู้เช่า... มาตั้งแต่สามปีก่อน
```

**🔊 SFX:** พลิกหน้ากระดาษเก่า · วิทยุสื่อสารซ่า ๆ · นาฬิกาแขวนเดินติ๊กต็อก · ยุงบินใกล้หู

**🖼️ Image Prompt**
```
Top-down close-up of an old yellowed Thai tenant logbook on a guard booth desk,
handwritten Thai names in blue ballpoint, EK's finger stopping at a row labeled 404
which is completely blank, a dusty 3-year-old date stamp above it, a cheap desk lamp
casting a sickly yellow pool of light, a cup of instant coffee and a walkie-talkie
beside it, rain-streaked window reflection, cinematic Thai horror film style, moody
teal and sickly yellow lighting, 35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Overhead camera tracks the finger sliding down the page and stops on the blank 404 row; lamp flickers once.`

---

## ซีน 8 — 02:18–02:32 · ระเบียงว่างเปล่า

**🎙️ Voiceover Script**
```
[tone: low, unsettled]
เขาวิ่งกลับไปดูอีกครั้ง
[pause: 0.8s]
ระเบียงนั้น... ว่างเปล่า
[pause: 0.8s]
มีเพียงผ้าม่านขาด ๆ... ที่ยังไหวอยู่เบา ๆ
[pause: 0.6s]
ทั้งที่ประตูกระจก... ถูกตอกตะปูปิดตายจากด้านนอก
```

**🔊 SFX:** ฝีเท้าวิ่งบนพื้นเปียก · หอบหายใจ · ผ้าม่านพลิ้ว · ดรอปเสียงบรรยากาศเหลือแต่ฝน

**🖼️ Image Prompt**
```
Telephoto shot of an empty fourth-floor balcony of an old Thai apartment, rusted
grille, sliding glass door boarded shut with crossed wooden planks and nails, a torn
white curtain still swaying gently behind the glass though there is no wind, a single
long black hair caught on the railing glistening with rain, cinematic Thai horror
film style, moody teal and sickly yellow lighting, 35mm film grain, photorealistic,
8k, --ar 16:9
```
**🎬 Motion Prompt:** `Static locked-off shot; only the curtain sways slowly; a slow imperceptible zoom-in over 6 seconds.`

---

## ซีน 9 — 02:32–02:52 · คืนที่สอง: เสียงร้องไห้

**🎙️ Voiceover Script**
```
[tone: calm, then tightening]
คืนที่สอง... เอกพยายามบอกตัวเองว่า... เขาแค่ตาฝาด
[pause: 0.8s]
จนกระทั่งตอนตีหนึ่ง... ขณะเปลี่ยนหลอดไฟที่ทางเดินชั้นสี่
[pause: 1s]
[whispering]
เขาได้ยินเสียง... ผู้หญิงร้องไห้
[pause: 0.8s]
สะอื้น... แผ่ว ๆ... อยู่หลังประตูห้องสี่ศูนย์สี่
```

**🔊 SFX:** บันไดอะลูมิเนียมลั่นเอี๊ยด · หมุนหลอดนีออนเข้าขั้ว · เสียงสะอื้นของผู้หญิงอู้อี้หลังประตูไม้ · ฝนพรำ

**🖼️ Image Prompt**
```
Medium shot of EK on a short aluminium step ladder in the mint-green fourth-floor
corridor, holding a new fluorescent tube, frozen mid-motion and turning his head
toward the door of room 404 at the end of the hall, his face half lit by sickly
yellow light, fear dawning in his eyes, the door slightly out of focus with its
red talisman paper, cinematic Thai horror film style, moody teal and sickly yellow
lighting, 35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `EK slowly turns his head toward the door; camera drifts sideways to align the door behind him; the corridor light buzzes and dims.`

---

## ซีน 10 — 02:52–03:12 · ตาแมว

**🎙️ Voiceover Script**
```
[tone: slow, extremely tense]
เอกค่อย ๆ ย่องเข้าไป...
ก้มลง... แล้วเอาตาข้างหนึ่ง... แนบกับตาแมวบนประตู
[pause: 1.5s]
ข้างในมืดสนิท...
[pause: 1s]
[barely audible]
แล้วความมืดนั้น... ก็ขยับ
[pause: 1.2s]
[sharp intake of breath, then low and fast]
ใบหน้าซีดเผือก... แนบอยู่อีกฝั่งของตาแมว
ดวงตาเบิกโพลง... จ้องสวนกลับมา
[pause: 0.6s]
พร้อมรอยยิ้ม... ที่ฉีกกว้าง... จนถึงใบหู
```

**🔊 SFX:** หัวใจเต้นดังขึ้นเรื่อย ๆ · เสียงร้องไห้หยุดกะทันหัน · ความเงียบสนิท 1 วิ · เสียงกระแทกเบา ๆ ที่ประตู (ไม่ใช่จัมป์สแกร์ดัง ใช้เสียงต่ำทุ้ม)

**🖼️ Image Prompt**
```
Extreme close-up POV through a fisheye door peephole, distorted circular view, a
pale grey female face pressed against the other side of the lens, wide unblinking
bloodshot eyes, an unnaturally wide stretched smile, wet black hair strands framing
the face, the room behind her pitch black, barrel distortion and vignette, cinematic
Thai horror film style, moody teal and sickly yellow lighting, 35mm film grain,
photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Fisheye view starts black; a pale face slowly fades in from the darkness until it fills the lens; the smile widens almost imperceptibly; hold 2 seconds, then a sudden cut to black.`

---

## ซีน 11 — 03:12–03:28 · ป้าศรี

**🎙️ Voiceover Script**
```
[tone: tired, slightly breathless, then calmer]
เอกไม่ได้นอนทั้งคืน
[pause: 0.6s]
เช้ามา... เขาตรงไปหาคนเดียวในตึก... ที่อยู่ที่นี่นานที่สุด
[pause: 0.6s]
ป้าศรี... แม่บ้านที่ทำงานที่ตึกนี้มาเกือบยี่สิบปี
[pause: 0.8s]
พอได้ยินคำว่า... สี่ศูนย์สี่
ไม้กวาดในมือป้า... ก็หล่นลงพื้น
```

**🔊 SFX:** เสียงเช้าตรู่: นกกระจอก, ฝนซา, กวาดใบไม้ · ไม้กวาดทางมะพร้าวหล่นกระทบพื้นปูน

**🖼️ Image Prompt**
```
Morning medium two-shot in a damp concrete stairwell of an old Thai apartment, grey
overcast light through a ventilation block wall, PA SRI: a thin elderly Thai
housekeeper with grey hair in a tight bun, faded floral blouse, checkered sarong and
worn apron, her coconut-rib broom falling from her hands, eyes wide with fear, EK
facing her with dark circles under his eyes, wet footprints on the stairs, cinematic
Thai horror film style, moody teal and sickly yellow lighting, 35mm film grain,
photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `The broom slips from Pa Sri's hands and clatters down two steps in slow motion; she glances nervously up the stairwell.`

---

## ซีน 12 — 03:28–03:52 · ผ้ายันต์สีแดง

**🎙️ Voiceover Script**
```
[tone: low, hushed]
ป้าศรีดึงเอกเข้าไปในห้องเก็บของ... ปิดประตู
แล้วล้วงอะไรบางอย่างออกมาจากกระเป๋าเสื้อ
[pause: 0.8s]
เศษผ้ายันต์... สีแดงคล้ำ... ขาดวิ่น
[pause: 1s]
[old woman, trembling whisper]
"สามปีก่อน... เสี่ยเขาเรียกหมอผีมาทำพิธีที่ห้องนั้น"
[pause: 0.5s]
"ผู้หญิงชื่อดาว... เมียน้อยเสี่ย... ผูกคอตายในตู้เสื้อผ้า"
[pause: 0.8s]
"หมอผีสะกดวิญญาณไว้... ใครเปิดห้อง... ของแตกนะลูก"
```

**🔊 SFX:** ประตูห้องเก็บของปิดเบา ๆ · ผ้าแห้งกรอบถูกคลี่ · เสียงลมหายใจสั่นของคนแก่ · หยดน้ำ

**🖼️ Image Prompt**
```
Tight close-up in a dim cleaning-supply storeroom lit by a single bare yellow bulb,
PA SRI's wrinkled trembling hands unfolding a torn piece of faded dark-red cloth
covered with black hand-drawn Thai yantra symbols and Khmer-style script, edges burnt
and frayed, EK's face leaning in out of focus behind, mop buckets and bleach bottles
on shelves, cinematic Thai horror film style, moody teal and sickly yellow lighting,
35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Slow push-in on the cloth as it is unfolded; the bare bulb sways slightly, moving shadows across the yantra script.`

---

## ซีน 13 — 03:52–04:08 · สิ่งที่ไม่เข้ากัน

**🎙️ Voiceover Script**
```
[tone: thoughtful, investigative]
แต่ยิ่งฟัง... เอกยิ่งเอะใจ
[pause: 0.8s]
ถ้าผู้หญิงคนนั้นผูกคอตาย...
ทำไมคอของผู้หญิงที่ระเบียง... ถึงขาวเนียน... ไม่มีรอยเชือกแม้แต่นิดเดียว
[pause: 1s]
และเสียงเคาะนั่น...
[whispering, even rhythm]
ก๊อก... ก๊อก... ก๊อก...
[pause: 0.8s]
[tone: low, certain]
มันไม่ใช่เสียงหลอกหลอน... มันฟังเหมือนคน... ที่กำลังขอให้ใครสักคนช่วย
```

**🔊 SFX:** โทนต่ำยาว (drone เบามาก หรือใช้เสียงฝนแทน) · เคาะไม้ 3 ครั้ง (เสียงจำจากซีน 3 แบบก้องในหัว)

**🖼️ Image Prompt**
```
Moody split-composition close-up of EK sitting alone on the edge of a narrow bed in
his tiny staff room at night, staring at the torn red yantra cloth in his hands,
behind him on the wall his phone flashlight projects a soft shadow, a faint ghostly
reflection in the dark window shows the woman in white's bare unmarked neck,
cinematic Thai horror film style, moody teal and sickly yellow lighting, 35mm film
grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Slow arc around EK as he thinks; the reflection in the window fades in and out; rain runs down the glass.`

---

## ซีน 14 — 04:08–04:25 · ขโมยกุญแจ

**🎙️ Voiceover Script**
```
[tone: tense, slightly faster]
คืนที่สาม... ตอนที่เสี่ยวิโรจน์ออกไปกินเหล้า
เอกแอบเข้าไปในห้องทำงาน... ค้นลิ้นชักทีละชั้น
[pause: 0.6s]
กุญแจสำรองห้องสี่ศูนย์สี่... ถูกซ่อนอยู่ใต้กล่องพระ
[pause: 0.8s]
[tone: low]
และในห้องเก็บของหลังโต๊ะ... มีถุงปูนซีเมนต์... ที่เปิดใช้ไปแล้วครึ่งถุง
ข้าง ๆ กัน... คือขวดน้ำ... กับข้าวกล่อง... ที่ยังไม่หมดอายุ
```

**🔊 SFX:** ลิ้นชักไม้ลาก · ค้นของกุกกัก · กุญแจหยิบขึ้นเบา ๆ · มอเตอร์ไซค์ผ่านหน้าตึก (ความเสี่ยงถูกจับได้)

**🖼️ Image Prompt**
```
Low-key interior night shot of the landlord's empty office, EK crouching behind the
desk with a flashlight in his mouth, pulling a single brass key labeled "404" from
under a small Buddha amulet box, in the background through an open storeroom door
the flashlight reveals a half-used bag of cement, a trowel crusted with dried
concrete, a pack of bottled water and fresh convenience-store rice boxes, cinematic
Thai horror film style, moody teal and sickly yellow lighting, 35mm film grain,
photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Handheld, EK lifts the key; the flashlight beam swings toward the storeroom and slowly pans over the cement bag and the food; headlights sweep across the window.`

---

## ซีน 15 — 04:25–04:42 · กลับมาที่ห้อง 404

**🎙️ Voiceover Script**
```
[tone: low, rhythmic, dread]
และนั่นคือเหตุผล... ที่ตอนนี้เอก... ยืนอยู่ในห้องสี่ศูนย์สี่
[pause: 1s]
กลิ่นธูป... กลิ่นคาว...
[pause: 0.6s]
[whispering]
ก๊อก... ก๊อก... ก๊อก...
[pause: 1s]
[tone: tense, slow]
เขาเอื้อมมือ... ไปจับลูกบิดตู้เสื้อผ้า
นับหนึ่ง... สอง...
[pause: 0.8s]
[urgent, breathless]
แล้วกระชากเปิดออก!
```

**🔊 SFX:** ฝนกลับมาดัง · เคาะ 3 ครั้งใกล้ขึ้น · หัวใจเต้นเร็วขึ้น · บานพับตู้ไม้สักกระชากเปิด "ปึง"

**🖼️ Image Prompt**
```
Medium close-up inside room 404, EK's hand gripping the tarnished brass handle of an
old teak wardrobe, his face sweating and lit from below by the flashlight, faded red
yantra cloths nailed around the wardrobe frame, ash from old incense sticks on the
floor, thin smoke in the beam, cinematic Thai horror film style, moody teal and
sickly yellow lighting, 35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Slow push-in on EK's hand; the knocks visibly shake the wardrobe door; on "กระชาก" a fast whip as the door swings open toward camera.`

---

## ซีน 16 — 04:42–05:02 · สิ่งที่อยู่ในตู้

**🎙️ Voiceover Script**
```
[pause: 1s]
[tone: stunned, low]
สิ่งที่อยู่ในตู้... ไม่ใช่ผี
[pause: 1.2s]
มันคือผู้หญิงคนหนึ่ง... ผอมจนเห็นกระดูกแก้ม
มือและเท้าถูกมัดด้วยเชือกไนลอน... ปากถูกปิดด้วยเทปกาว
[pause: 0.8s]
หน้าผากของเธอแตกเป็นแผล... จากการเอาหัว... โขกผนังตู้... ซ้ำแล้วซ้ำเล่า
[pause: 0.8s]
[weak, hoarse]
"ช่วย... ด้วย..."
```

**🔊 SFX:** เสียงหายใจแหบ ๆ ของผู้หญิง · ดึงเทปกาวออก · เสียงเชือกเสียดสี · ฝนพรำ

**🖼️ Image Prompt**
```
Interior of a cramped old teak wardrobe lit by a harsh flashlight beam, DAO: an
emaciated Thai woman in her early 20s with sunken cheeks and long tangled black hair,
torn pale-blue shirt, wrists and ankles bound with blue nylon rope, duct tape half
peeled from her mouth, a small bruise on her forehead, terrified eyes squinting into
the light, scratch marks on the inner wardrobe wall, non-graphic, cinematic Thai
horror film style, moody teal and sickly yellow lighting, 35mm film grain,
photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Flashlight beam trembles over the woman; she slowly lifts her head and squints into the light; dust particles float in the beam.`

---

## ซีน 17 — 05:02–05:18 · ประตูปิดกระแทก

**🎙️ Voiceover Script**
```
[urgent, breathless]
เอกรีบดึงมีดคัตเตอร์ออกจากเข็มขัด... ตัดเชือก
[pause: 0.5s]
แต่ยังไม่ทันได้ตัดเส้นที่สอง...
[pause: 0.6s]
ปัง!
[pause: 1s]
[tone: low, dread]
ประตูห้องปิดกระแทก... ไฟฉายในมือ... ดับพรึ่บ
[pause: 1.2s]
แสงเดียวที่เหลือ... คือแสงฟ้าแลบ... ที่สาดเข้ามาทางหน้าต่าง
[pause: 0.6s]
และในแสงนั้น... มีคนยืนขวางประตูอยู่
```

**🔊 SFX:** ใบคัตเตอร์ดันออก "แกร๊ก ๆ" · ตัดเชือก · ประตูกระแทกดังสนั่น · คลิกไฟฉายดับ · ฟ้าร้องครืนไกล ๆ แล้วฟ้าผ่าใกล้

**🖼️ Image Prompt**
```
Dark room 404 lit only by a cold teal lightning flash through a boarded window, the
silhouette of THE LANDLORD: a heavyset Thai man in his 60s with slicked-back grey
hair and gold chain, standing in the closed doorway holding a long-handled
sledgehammer across his body, his face half revealed with a cruel calm smile, EK in
the foreground crouched by the open wardrobe shielding DAO, cinematic Thai horror
film style, moody teal and sickly yellow lighting, 35mm film grain, photorealistic,
8k, --ar 16:9
```
**🎬 Motion Prompt:** `Total darkness, then two lightning flashes reveal the landlord in the doorway, slightly closer on the second flash; the sledgehammer head lowers to the floor with a heavy drag.`

---

## ซีน 18 — 05:18–05:42 · ความจริงจากปากเจ้าของตึก

**🎙️ Voiceover Script**
```
[landlord, cold and smooth]
"บอกแล้ว... ว่าห้ามเข้าใกล้"
[pause: 1s]
[tone: low narration]
เสี่ยวิโรจน์ลากค้อนปอนด์... เดินเข้ามาช้า ๆ
[pause: 0.6s]
[landlord, cold and smooth]
"ข่าวลือเรื่องผีดาว... ฉันปล่อยเอง"
"ใครได้ยินเสียงร้องไห้... ก็จะคิดว่าผี... ไม่มีใครกล้าเปิด"
[pause: 0.8s]
"นังดาวมันเป็นลูกฉันเอง... มันกลับมาเจอ... สิ่งที่ฉันเก็บไว้ในผนังห้องนี้"
[pause: 1s]
[tone: low, chilling]
ผนังห้องที่ถูกฉาบปูนใหม่... เพียงด้านเดียว
```

**🔊 SFX:** หัวค้อนลากบนพื้นปูน "ครืด..." · ฝีเท้าหนัก ๆ · ฝนกระหน่ำ · ฟ้าร้องต่ำ

**🖼️ Image Prompt**
```
Low-angle dramatic shot of THE LANDLORD advancing through dark room 404, dragging a
sledgehammer along the concrete floor, lightning revealing his sweating face and
cold smile, behind him one wall is noticeably different: freshly patched, uneven
grey cement plaster with hairline cracks and a faint damp stain shaped like a human
outline, old red yantra cloths nailed in a line across it, cinematic Thai horror
film style, moody teal and sickly yellow lighting, 35mm film grain, photorealistic,
8k, --ar 16:9
```
**🎬 Motion Prompt:** `Slow backward dolly as the landlord walks toward camera; lightning pulses; behind him the damp stain on the cement wall seems to darken slightly with each flash.`

---

## ซีน 19 — 05:42–05:58 · เงาบนเพดาน

**🎙️ Voiceover Script**
```
[tone: slow, very low]
แต่เอก... ไม่ได้มองที่ค้อนในมือเสี่ยแล้ว
[pause: 1s]
สายตาของเขา... จ้องอยู่ที่เพดาน... ด้านหลังชายคนนั้น
[pause: 1.2s]
[whispering]
เงาดำทมิฬ... บางอย่าง
กำลังค่อย ๆ... คลานลงมาตามผนัง
[pause: 0.6s]
แขนขายาวผิดรูป... ผมยาวสีดำ... ห้อยลงมา... เกือบแตะไหล่ของเขา
```

**🔊 SFX:** ปูนร่อนหล่นเป็นเม็ดเล็ก ๆ · เสียงข้อกระดูกลั่นเบา ๆ (ระวังไม่ให้ดังเกิน) · เสียงหายใจลึกเย็นเฉียบด้านหลัง · ฝนเงียบลง

**🖼️ Image Prompt**
```
Wide shot inside dark room 404 from EK's low point of view, THE LANDLORD in the
foreground mid-frame unaware, behind and above him a tall pitch-black humanoid
shadow with elongated limbs crawling head-first down the cracked cement wall from
the ceiling, long wet black hair hanging down toward the landlord's shoulder, flakes
of cement falling, faint white nightgown fabric visible within the darkness,
cinematic Thai horror film style, moody teal and sickly yellow lighting, 35mm film
grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `The shadow descends the wall in slow, jerky, spider-like movements; cement dust trickles; the landlord stays still in the foreground; camera holds steady with a subtle slow zoom.`

---

## ซีน 20 — 05:58–06:14 · เฉลยความจริง

**🎙️ Voiceover Script**
```
[tone: low, reflective, revelation]
ในวินาทีนั้น... เอกเข้าใจทุกอย่าง
[pause: 1s]
ผู้หญิงชุดขาวที่ระเบียง... ใบหน้าที่ตาแมว...
ไม่เคยเป็นดาวเลย
[pause: 0.8s]
เธอคือวิญญาณของผู้หญิง... ที่ถูกฆ่า... แล้วโบกปูนไว้ในผนังห้องนี้เมื่อสามปีก่อน
[pause: 1s]
ตลอดสามคืน... เธอไม่ได้หลอกเขา
[pause: 0.6s]
[slower, softer]
เธอกำลัง... เรียกเขามาช่วยดาว
```

**🔊 SFX:** ทุกอย่างเงียบลงเหลือเพียงเสียงลมหายใจ · เสียงกระซิบซ้อนหลายชั้นแผ่ว ๆ (ฟังไม่ออก) · หยดน้ำ

**🖼️ Image Prompt**
```
Ethereal flashback montage frame, double exposure: the woman in white brushing her
hair on the balcony, the grinning face in the peephole, and a translucent pale woman
standing inside a cross-section of a concrete wall with her eyes closed, all layered
over EK's wide-eyed realizing face, soft teal glow, no gore, cinematic Thai horror
film style, moody teal and sickly yellow lighting, 35mm film grain, photorealistic,
8k, --ar 16:9
```
**🎬 Motion Prompt:** `Slow cross-dissolve between the three ghost images over EK's face; slight slow-motion; end on the wall woman opening her eyes.`

---

## ซีน 21 — 06:14–06:34 · ในความมืด

**🎙️ Voiceover Script**
```
[tone: tense, slow]
เสี่ยวิโรจน์ยกค้อนขึ้นสูง...
[pause: 0.8s]
แต่ยังไม่ทันได้ฟาดลงมา...
[pause: 0.6s]
ฟ้าผ่าเปรี้ยง... ไฟทั้งตึกดับสนิท
[pause: 1.5s]
[whispering, eerie]
ในความมืด... มีเพียงเสียงกรีดร้องสั้น ๆ...
แล้วตามด้วยเสียง... กร๊อบ
[pause: 2s]
[tone: low]
ค้อนปอนด์... หล่นกระแทกพื้น
แล้วทุกอย่าง... ก็เงียบ
```

**🔊 SFX:** ฟ้าผ่าใกล้มาก · ไฟดับ (hum ตัดหาย) · เสียงร้องสั้นถูกตัดกลางคัน · เสียงกระดูกหัก "กร๊อบ" เบาและห้วน · ค้อนเหล็กกระแทกพื้นปูน · ความเงียบ 2 วิ

**🖼️ Image Prompt**
```
Almost entirely black frame, a single faint lightning afterglow through the boarded
window reveals only the edge of a sledgehammer lying on the concrete floor and the
landlord's gold chain glinting beside it, a long strand of black hair trailing away
into darkness, no body visible, no gore, cinematic Thai horror film style, moody teal
and sickly yellow lighting, 35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Hold on black for 2 seconds; a dim flicker reveals the fallen sledgehammer and gold chain; the strand of hair slowly slides away out of frame.`

---

## ซีน 22 — 06:34–06:52 · หนีออกจากตึก

**🎙️ Voiceover Script**
```
[urgent, breathless]
เอกไม่รอให้ไฟกลับมา
เขาตัดเชือกเส้นสุดท้าย... อุ้มดาวขึ้นหลัง... แล้ววิ่ง
[pause: 0.6s]
ลงบันไดสี่ชั้น... ฝ่าสายฝน... ออกไปยังถนน
[pause: 1s]
[tone: tired, calmer]
เช้ามืดวันนั้น... ตำรวจทุบผนังห้องสี่ศูนย์สี่
และพบโครงกระดูกของหญิงสาว... ที่หายตัวไปเมื่อสามปีก่อน
[pause: 0.8s]
ส่วนเสี่ยวิโรจน์... ถูกพบในสภาพคอหัก... กลางห้อง... โดยไม่มีใครอธิบายได้
```

**🔊 SFX:** ฝีเท้าวิ่งลงบันไดเหล็ก · หอบหายใจ · ฝนกระหน่ำกลางแจ้ง · ไซเรนตำรวจไกล ๆ แล้วใกล้ขึ้น · วิทยุตำรวจ

**🖼️ Image Prompt**
```
Exterior night wide shot in heavy rain, EK staggering out of the apartment gate onto
the flooded soi carrying the emaciated DAO on his back, both soaked, red and blue
police lights reflecting on the wet street and the building's stained facade, the
fourth-floor window of room 404 dark above them, a faint white figure barely visible
behind its glass, cinematic Thai horror film style, moody teal and sickly yellow
lighting, 35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Tracking shot moving backward as EK runs toward camera; police lights pulse; slow tilt up at the end to the dark fourth-floor window where a white figure fades away.`

---

## ซีน 23 — 06:52–07:10 · หนึ่งเดือนต่อมา: ทำบุญ

**🎙️ Voiceover Script**
```
[tone: warm, quiet, slightly sad]
หนึ่งเดือนต่อมา...
เอกกับดาว... ไปทำบุญที่วัดเล็ก ๆ แห่งหนึ่ง
[pause: 0.8s]
พวกเขาบังสุกุล... กรวดน้ำ... อุทิศส่วนกุศลให้วิญญาณดวงนั้น
[pause: 0.8s]
ผู้หญิงที่ไม่มีใครรู้จักชื่อ...
แต่ช่วยชีวิตคนคนหนึ่ง... ไว้จากในผนัง
```

**🔊 SFX:** เสียงพระสวดเบา ๆ ไกล ๆ (หรือเงียบ) · กระดิ่งลมในวัด · นกร้องยามเช้า · น้ำรินจากคนโทกรวดน้ำ

**🖼️ Image Prompt**
```
Soft daylight medium shot in a small Thai temple sala, EK in a clean white shirt and
DAO, healthier but still thin, in a modest white blouse, kneeling side by side,
pouring water from a small brass kruat nam vessel into a bowl in a merit-transfer
ritual, an urn with a small framed photo silhouette and marigold garlands in front
of them, an orange-robed monk blurred in the background, gentle muted palette with
lingering teal shadows, cinematic Thai horror film style, moody teal and sickly
yellow lighting, 35mm film grain, photorealistic, 8k, --ar 16:9
```
**🎬 Motion Prompt:** `Gentle slow dolly sideways; the water pours in a thin stream; incense smoke rises softly; a calm, peaceful moment.`

---

## ซีน 24 — 07:10–07:35 · เสียงเคาะครั้งสุดท้าย

**🎙️ Voiceover Script**
```
[tone: calm, then slowly darkening]
คืนนั้น... เอกนอนอยู่ในห้องเช่าใหม่
ห้องเล็ก ๆ ที่เงียบสงบ... ครั้งแรกในรอบหลายสัปดาห์
[pause: 1.2s]
จนกระทั่ง...
[pause: 1.5s]
[whispering, eerie, even rhythm]
ก๊อก... ก๊อก... ก๊อก...
[pause: 1.5s]
[tone: very low]
เสียงนั้นดังมาจาก... ในตู้เสื้อผ้า... ในห้องของเขาเอง
[pause: 2s]
[ghostly whisper, far away]
"ขอบคุณนะ..."
[pause: 2.5s]
```

**🔊 SFX:** ฝนพรำเบา ๆ · นาฬิกาปลุกเดินติ๊กต็อก · เคาะไม้ 3 ครั้งเบา ๆ · ความเงียบ · เสียงกระซิบ "ขอบคุณนะ" ใส่รีเวิร์บเบา · ตัดเสียงทุกอย่างพร้อมภาพดำ

**🖼️ Image Prompt**
```
Dim bedroom at night in a small new Thai rental room, EK lying awake on his side in
bed, eyes open toward the camera, behind him across the room a plain white modern
wardrobe with its door open just a crack, a thin sliver of darkness inside, at the
very edge of the gap a few strands of long black hair and the faint pale fingertips
of a hand, streetlight through rain-streaked curtains, cinematic Thai horror film
style, moody teal and sickly yellow lighting, 35mm film grain, photorealistic, 8k,
--ar 16:9
```
**🎬 Motion Prompt:** `Extremely slow push-in past EK toward the wardrobe gap; on the third knock the door eases open one more centimeter; on the whisper, the fingertips gently withdraw into the darkness; smash cut to black.`

> 📝 **End card:** พื้นดำ ข้อความ "บางเสียงเคาะ... ไม่ได้ต้องการให้คุณกลัว" (ค้าง 3 วิ) — ไม่มีเสียงพากย์

---

## สรุปความยาวและการผลิต

| ช่วง | ซีน | เวลาโดยประมาณ |
|---|---|---|
| The Hook | 1–3 | 00:00–01:00 |
| Setup & Mystery | 4–8 | 01:00–02:32 |
| Peephole & Red Herring | 9–14 | 02:32–04:25 |
| Climax & Twist | 15–21 | 04:25–06:34 |
| Resolution & Ending Hook | 22–24 | 06:34–07:35 |

**ทิปการผลิต**
- **ปมที่ปูไว้ให้คนดูเดา (ควรให้กล้องค้างนานพอ):** พื้นหน้าห้องแห้ง (ซีน 5), ตะขอกุญแจ 404 ว่าง (5), คอไม่มีรอยเชือก (6, 13), ข้าวกล่องยังไม่หมดอายุ + ถุงปูน (14), ผนังฉาบปูนใหม่ด้านเดียว (18) — ทำให้ตอนเฉลยรู้สึก "แฟร์"
- **จัมป์สแกร์จริงมีแค่จุดเดียว** (ซีน 10 ตาแมว) ที่เหลือใช้ความเงียบและการค้างภาพ ตามโทน "ไม่ตุ้งแช่พร่ำเพรื่อ"
- **ความรุนแรง:** ฉากเจ้าของตึกเสียชีวิตเกิดในความมืด ใช้เสียงแทนภาพ ปลอดภัยต่อนโยบาย YouTube (ไม่ติด age-restriction ง่าย)
- **เสียงพากย์:** เจนทีละ 2–4 ซีนด้วยสไตล์เดียวกันและเสียงเดียวกันทุกครั้ง แล้วต่อไฟล์ใน editor; เว้นช่วงเงียบตามแท็กไว้ให้ SFX ทำงาน
- **ภาพ → วิดีโอ:** เจนภาพนิ่งด้วย Midjourney/Flux โดยใช้คำบรรยายตัวละครเดิมทุกครั้ง (หรือ `--cref` ภาพเอกจากซีน 1) แล้วนำไป Kling/Runway แบบ image-to-video พร้อม Motion Prompt ของซีนนั้น คลิปละ 5–10 วิ
