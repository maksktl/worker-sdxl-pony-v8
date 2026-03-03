# Гайд по промптам для WAI-NSFW-illustrious-SDXL v16

Рекомендации по написанию промптов для генерации аниме/хентай изображений.
Применимо к WAI-NSFW-illustrious-SDXL и другим Illustrious-based моделям.

---

## Содержание

1. [Основы промптинга](#1-основы-промптинга)
2. [Порядок тегов](#2-порядок-тегов)
3. [Quality теги и настройки](#3-quality-теги-и-настройки)
4. [Rating теги](#4-rating-теги)
5. [Negative prompt](#5-negative-prompt)
6. [Персонажи из аниме](#6-персонажи-из-аниме)
7. [NSFW теги и позы для секса](#7-nsfw-теги-и-позы-для-секса)
8. [Камера, ракурсы и композиция](#8-камера-ракурсы-и-композиция)
9. [Стилизация и художники](#9-стилизация-и-художники)
10. [Фоны и окружение](#10-фоны-и-окружение)
11. [Эффекты и динамика](#11-эффекты-и-динамика)
12. [Структура CASE](#12-структура-case-для-сложных-сцен)
13. [Частые ошибки](#13-частые-ошибки)
14. [Примеры готовых промптов](#14-примеры-готовых-промптов)
15. [Полезные ссылки](#15-полезные-ссылки)

---

## 1. Основы промптинга

Модель обучена на датасете **Danbooru 2023**. Используйте **danbooru-теги**, разделённые запятыми.

### Ключевые правила

- **Только строчные буквы**: `masterpiece`, не `Masterpiece`
- **Запятые обязательны**: модель обучена с запятыми, без них теги путаются
- **Используйте danbooru-теги**: `striped shirt, collared shirt` вместо `striped collared shirt`
- **Нижние подчёркивания опциональны**: `open_mouth` = `open mouth`
- **Лимит токенов**: SDXL обрабатывает максимум 75 токенов. Более длинные промпты разбиваются на блоки по 75, что может снизить качество
- **Короткие промпты > длинные**: чем больше тегов, тем больше шанс, что модель проигнорирует какой-то из них
- **Первые слова важнее**: модель уделяет больше внимания тегам в начале промпта

> **Источник**: [Illustrious Prompting Guide by wolf999](https://civitai.com/articles/10962/illustrious-prompting-guide-or-v01-or-generate-anime-art-with-ai)

### Экранирование спецсимволов

Скобки `()` и двоеточия `:` — спецсимволы для весов. Если они часть тега, экранируй:

```
watercolor \(medium\)
astolfo \(fate\)
\:p
\:\)
```

> **Источник**: [Illustrious Prompt Guide (Optimized & Complete)](https://civitai.com/articles/16016/illustrious-prompt-guide-optimized-and-complete)

---

## 2. Порядок тегов

Illustrious обучен на данных в определённом порядке. Соблюдение порядка даёт лучшие результаты:

```
кол-во персонажей, имя персонажа, рейтинг, основные теги, художник, quality score, year modifier
```

### Пример:

```
1girl, asuka langley soryu \(evangelion\), explicit, red hair, blue eyes, plugsuit, bedroom, masterpiece, newest
```

Разбивка:
1. **Кол-во** = `1girl`
2. **Персонаж** = `asuka langley soryu \(evangelion\)`
3. **Рейтинг** = `explicit`
4. **Основные теги** = `red hair, blue eyes, plugsuit, bedroom`
5. **Художник** = (опционально)
6. **Quality** = `masterpiece`
7. **Year** = `newest`

> **Источник**: [Illustrious Prompting Guide by wolf999](https://civitai.com/articles/10962/illustrious-prompting-guide-or-v01-or-generate-anime-art-with-ai)

---

## 3. Quality теги и настройки

### Наш дефолтный positive prefix (уже встроен в API при `add_quality_tags: true`):

```
masterpiece, best quality, amazing quality, very aesthetic, absurdres, newest
```

### Что означают quality теги:

| Тег | Значение |
|-----|----------|
| `worst quality` | Нижние 8% по качеству |
| `bad quality` | Нижние 20% |
| `average quality` | 60% |
| `good quality` | 92% |
| `masterpiece` | Топ 100% |

### Что означают year теги:

| Тег | Период |
|-----|--------|
| `oldest` | ~2017 |
| `old` | ~2019 |
| `modern` | ~2020 |
| `recent` | ~2022 |
| `newest` | ~2023 |

Используй `newest` — это самый свежий и качественный стиль.

### Рекомендуемые настройки WAI-NSFW v16:

| Параметр | Значение |
|----------|----------|
| **Sampler** | Euler a |
| **CFG** | 5-7 (дефолт 6.0) |
| **Steps** | 15-30 (дефолт 28) |
| **Разрешение** | > 1024x1024 (дефолт 832x1216) |

> **Источник**: [WAI-illustrious-SDXL v16 — CivitAI](https://civitai.com/models/827184/wai-illustrious-sdxl)

---

## 4. Rating теги

Danbooru имеет 4 уровня рейтинга. Используй их для контроля NSFW:

| Тег | Описание |
|-----|----------|
| `general` | SFW для всех |
| `sensitive` | Лёгкий фансервис |
| `questionable` | Сексуально провокационное |
| `explicit` | NSFW / для взрослых |

**Для генерации хентая**: добавь `explicit` в positive prompt.
**Для SFW генерации**: добавь `nsfw` в negative prompt.

> **Источник**: [Illustrious Prompt Guide (Optimized & Complete)](https://civitai.com/articles/16016/illustrious-prompt-guide-optimized-and-complete)

---

## 5. Negative prompt

### Философия

Не перегружай negative prompt 30+ тегами — это непредсказуемо. Лучше писать точные positive промпты.

### Наш дефолтный negative prompt (встроен в API):

```
bad quality, worst quality, worst detail, sketch, censor, lowres, (bad anatomy:1.2), jpeg artifacts, signature, watermark, old, oldest, censored, bar_censor, extra digits, fewer digits, extra arms, missing arms, too many fingers, fused fingers, missing fingers, ugly, blurry
```

### Минимальный надёжный набор (по wolf999):

```
lowres, worst quality, multiple views, text, watermark, signature, comic
```

### Расширенный набор (по Tips for Illustrious XL):

```
lowres, (bad), bad anatomy, bad hands, extra digits, multiple views, fewer, extra, missing, text, error, worst quality, jpeg artifacts, low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, artistic error, username, scan
```

### Полезные anti-теги:

| Тег | Предотвращает |
|-----|--------------|
| `monochrome, greyscale` | Чёрно-белые изображения |
| `multiple views` | Множественные ракурсы одного персонажа |
| `text, watermark, signature` | Текст и водяные знаки |
| `comic, 4koma` | Панели комиксов |
| `censored, bar_censor, censor` | Цензурирование |

> **Источники**:
> - [Illustrious Prompting Guide by wolf999](https://civitai.com/articles/10962/illustrious-prompting-guide-or-v01-or-generate-anime-art-with-ai)
> - [Tips for Illustrious XL Prompting](https://civitai.com/articles/8380/tips-for-illustrious-xl-prompting-updates)

---

## 6. Персонажи из аниме

### Формат имён

Имена персонажей на Danbooru записаны в **японском порядке** (фамилия, имя):

```
# Правильно:
asuka langley soryu \(evangelion\)
katsuragi misato

# Неправильно:
soryu asuka langley
misato katsuragi
```

> **Важно**: WAI-NSFW v16 знает **5058+ персонажей** (включая разные костюмы). Просто напиши имя и франшизу.

### Как указывать персонажа:

```
character_name \(franchise\)
```

### Примеры:

```
1girl, boa hancock \(one piece\), explicit, ...
1girl, hinata hyuuga \(naruto\), explicit, ...
1girl, zero two \(darling in the franxx\), explicit, ...
1girl, makima \(chainsaw man\), explicit, ...
1girl, yor briar \(spy x family\), explicit, ...
```

### Что делать, если персонаж не распознаётся:

- Добавь описание внешности: цвет волос, глаз, причёска, характерные черты
- Используй LoRA для конкретного персонажа
- Правило: тег должен иметь **100+ изображений на Danbooru** чтобы модель его знала

### Полезные ресурсы:

- [Список распознаваемых персонажей Illustrious XL](https://civitai.com/articles/10242/illustrious-xl-v01-recognized-characters-list) — таблица с цветовой маркировкой
- [WAI-NSFW Character Prompt Generator](https://huggingface.co/spaces/flagrantia/character_select_saa) — плагин для подбора персонажей
- [Список персонажей WAI-NSFW](https://huggingface.co/datasets/sieecc/WAI-NSFW-illustrious-SDXL/tree/main) — тестированные персонажи

> **Источники**:
> - [Illustrious XL Recognized Characters List](https://civitai.com/articles/10242/illustrious-xl-v01-recognized-characters-list)
> - [WAI-illustrious-SDXL v16](https://civitai.com/models/827184/wai-illustrious-sdxl)
> - [Arctenox's Simple Prompt Guide](https://civitai.com/articles/23210/arctenoxs-simple-prompt-guide-for-illustrious)

---

## 7. NSFW теги и позы для секса

### Базовые NSFW теги

| Тег | Описание |
|-----|----------|
| `nude` | Обнажённая |
| `completely nude` | Полностью обнажённая |
| `breasts` | Грудь |
| `nipples` | Соски |
| `pussy` | Гениталии (жен.) |
| `penis` | Гениталии (муж.) |
| `anus` | Анус |
| `clitoris` | Клитор |
| `vaginal` | Вагинальный секс (важнее чем тег `sex`!) |
| `anal` | Анальный секс |
| `oral` | Оральный секс |
| `sex` | Секс (общий тег) |
| `pov` | От первого лица |

### Размер груди

```
flat chest, small breasts, medium breasts, large breasts, huge breasts
```

### Сексуальные позиции (Danbooru tags)

#### Сзади (sex from behind)

| Тег | Описание |
|-----|----------|
| `doggystyle` | Догги-стайл |
| `bent over` | Наклонённая вперёд |
| `prone bone` | Лёжа на животе |
| `standing sex` | Секс стоя |
| `top-down bottom-up` | Попа вверх, голова внизу |

#### Сверху (girl on top)

| Тег | Описание |
|-----|----------|
| `cowgirl position` | Поза наездницы |
| `reverse cowgirl position` | Обратная наездница |
| `squatting cowgirl position` | Наездница на корточках |
| `amazon position` | Амазонка |
| `upright straddle` | Вертикальное оседлание |
| `reverse upright straddle` | Обратное вертикальное оседлание |

#### Снизу (boy on top)

| Тег | Описание |
|-----|----------|
| `missionary` | Миссионерская |
| `mating press` | Прижатие (ноги к голове) |
| `anvil position` | Наковальня |
| `legs up` | Ноги вверх |
| `folded` | Складка (колени к груди) |
| `full nelson` | Фулл нельсон |
| `piledriver` | Пайлдрайвер |
| `standing missionary` | Стоячая миссионерская |

#### Другие

| Тег | Описание |
|-----|----------|
| `69` | 69 |
| `spooning` | На боку (ложки) |
| `suspended congress` | На весу |
| `spitroast` | С двух сторон |
| `mounting` | Оседлание |

### Дополнительные NSFW теги

| Тег | Описание |
|-----|----------|
| `cum` | Сперма |
| `cum in pussy / mouth / ass` | Кончить внутрь |
| `cum on body / face / breasts` | Кончить на тело |
| `creampie` | Кримпай |
| `overflow` | Перелив |
| `spread legs` | Раздвинутые ноги |
| `spread pussy` | Раздвинутая вагина |
| `ahegao` | Ахегао (лицо) |
| `fucked silly` | Обезумевшее выражение |
| `tongue out` | Высунутый язык |
| `drooling` | Слюноотделение |
| `open mouth` | Открытый рот |
| `heavy breathing` | Тяжёлое дыхание |
| `blush` | Румянец |
| `sweat` | Пот |
| `tears` | Слёзы |
| `trembling` | Дрожь |

### Тег `disembodied` — продвинутый приём

Для гибких ракурсов без блокировки обзора:

- `disembodied hands` — руки без тела (для grab, spread и т.д.)
- `disembodied penis` — для пенетрации с невозможных ракурсов
- `disembodied tongue` — для лизания

> **Источники**:
> - [Danbooru: Tag Group — Sexual Positions](https://danbooru.donmai.us/wiki_pages/tag_group:sexual_positions)
> - [Danbooru: Tag Group — Sex Acts](https://danbooru.donmai.us/wiki_pages/tag_group:sex_acts)
> - [Helpful Tags for Image Generation — NSFW](https://civitai.com/articles/8284/guide-helpful-tags-for-image-generation-sdxlpony-sfw-and-nsfw)
> - [Prompting for XXX Poses: A Guide and Library](https://civitai.com/articles/18929/prompting-for-xxx-poses-a-guide-and-library)
> - [Prompt Notebook — Scenes](https://civitai.com/articles/3160/prompt-notebook)

---

## 8. Камера, ракурсы и композиция

### Базовые ракурсы

| Тег | Описание |
|-----|----------|
| `straight-on` | Вид спереди |
| `from side` | Вид сбоку |
| `from above` | Вид сверху |
| `from below` | Вид снизу (часто ракурс на промежность) |
| `from behind` | Вид сзади |
| `three-quarter view` | 3/4 вид |
| `dutch angle` | Наклонённый кадр (добавляет динамику) |

### Кадрирование

| Тег | Описание |
|-----|----------|
| `full body` | С головы до пят |
| `upper body` | Верхняя часть тела |
| `lower body` | Нижняя часть тела |
| `cowboy shot` | От бёдер и выше |
| `portrait` | От груди/подмышек и выше |
| `close-up` | Крупный план |
| `head out of frame` | Голова за кадром |

### Специальные ракурсы

| Тег | Описание |
|-----|----------|
| `pov` | От первого лица |
| `isometric` | Изометрия |
| `fisheye` | Рыбий глаз |
| `symmetry` | Симметричная композиция |
| `vanishing point` | С точкой схода |
| `overhead view` | Вид сверху (top-down) |
| `low angle view` | Вид снизу |

### Освещение

```
cinematic light, backlighting, rim lighting, soft lighting, harsh lighting,
dramatic light, soft shadows, harsh shadows, volumetric lighting
```

> **Источники**:
> - [Illustrious Prompt Guide (Optimized & Complete)](https://civitai.com/articles/16016/illustrious-prompt-guide-optimized-and-complete)
> - [Tips for Illustrious XL Prompting — Angles/Lighting](https://civitai.com/articles/8380/tips-for-illustrious-xl-prompting-updates)
> - [Helpful Tags for Image Generation — Camera Angles](https://civitai.com/articles/8284/guide-helpful-tags-for-image-generation-sdxlpony-sfw-and-nsfw)

---

## 9. Стилизация и художники

### Художественные медиумы

```
traditional media, watercolor \(medium\), graphite \(medium\),
colored pencil \(medium\), millipen \(medium\), marker \(medium\),
photo \(medium\), painting \(medium\)
```

### Стили эпох

```
1980s \(style\), 2000s \(style\), retro artstyle, pc-98 \(style\),
anime screenshot, game cg
```

### Как использовать художников

Найди художника на [Danbooru Related Tags](https://danbooru.donmai.us/related_tag) — введи интересующий тег, категория "artist", сортировка по частоте.

**Правило**: у художника должно быть **100+ изображений** на Danbooru, чтобы стиль распознавался.

Можно комбинировать стили и использовать веса:

```
(traditional media:0.5)     -- 50% традиционная медиа
(artist_name:0.7)           -- 70% влияние стиля художника
```

### Галереи стилей WAI-NSFW:

- [300 стилей для WAI-NSFW](https://huggingface.co/datasets/sieecc/SOKI/blob/main/300Styles-waiNSFW.html) — скачай HTML и открой в браузере
- [Artists for Illustrious XL](https://civitai.com/articles/9309/artists-for-illustrious-xl) — удобный браузер стилей

> **Источники**:
> - [Illustrious Prompting Guide — Style Tags](https://civitai.com/articles/10962/illustrious-prompting-guide-or-v01-or-generate-anime-art-with-ai)
> - [Just Another Guide for Beginners — Change the Style](https://civitai.com/articles/8635/just-another-image-generation-guide-for-beginners-pony-diffusion-v6-xl-and-illustrious)

---

## 10. Фоны и окружение

### Простые фоны (для фокуса на персонаже)

```
white background, simple background, gradient background,
halftone background, stripped background, argyle background
```

### Рамки и границы

```
ornate frame, lace border, ornate border
```

### Сцены окружения

```
bedroom, bathroom, school, classroom, outdoors, onsen,
pool, beach, forest, alley, rooftop, kitchen, office
```

### Атмосфера

```
indoors, outdoors, night, sunset, sunrise, dawn, dusk,
rain, snow, wind, sunny, cloudy
```

### Совет

Большинство AI-генераций выглядят "фейковыми" из-за слишком детальных фонов.
Настоящие аниме-художники редко рисуют сложные интерьеры — используй `simple background` или `white background` для аутентичного стиля.

> **Источник**: [Illustrious Prompting Guide — Background/Border Tags](https://civitai.com/articles/10962/illustrious-prompting-guide-or-v01-or-generate-anime-art-with-ai)

---

## 11. Эффекты и динамика

### Визуальные эффекты

```
blurry foreground, blurry background, depth of field,
glitch, bloom, spot color, chromatic aberration
```

### Динамика для NSFW сцен

| Тег | Описание |
|-----|----------|
| `motion lines` | Линии движения |
| `emphasis lines` | Линии акцента |
| `speed lines` | Линии скорости |
| `bouncing breasts` | Подпрыгивающая грудь |
| `bouncing ass` | Подпрыгивающая попа |
| `ass ripple` | Рябь на ягодицах |
| `motion blur` | Размытие движения |
| `afterimage` | Послеобраз |

### Выражения тела (для горячих сцен)

```
sweat, sweating profusely, sparkling sweat, wet,
blush, full-face blush, body blush, heavy breathing,
steaming body, trembling, twitching
```

> **Источник**: [Prompt Notebook — Scenes](https://civitai.com/articles/3160/prompt-notebook)

---

## 12. Структура CASE для сложных сцен

Для сложных промптов используй структуру **CASE** (Composition, Action, Subject, Environment):

### 1. Composition (Композиция)
- Quality теги
- Стиль
- Камера / ракурс
- Кол-во персонажей

### 2. Action (Действие)
- Секс-акт / поза
- Положение тела

### 3. Subject (Субъект)
- Тело (тип, размер груди, цвет кожи)
- Лицо (цвет глаз, причёска)
- Выражение (эмоция, рот, глаза)
- Одежда

### 4. Environment (Окружение)
- Помещение / улица
- Освещение / время суток
- Погода
- Объекты

### Пример CASE-промпта:

```
masterpiece, best quality, very aesthetic, newest, from above, 1girl, 1boy,
cowgirl position, vaginal, sex, pov,
large breasts, long black hair, blue eyes, ahegao, blush, sweat, tongue out,
bedroom, night, dim lighting, messy bed
```

> **Источник**: [Prompt Notebook — Structure](https://civitai.com/articles/3160/prompt-notebook)

---

## 13. Частые ошибки

### НЕ делай:

| Ошибка | Правильно |
|--------|-----------|
| Заглавные буквы `Masterpiece` | `masterpiece` |
| Без запятых `nude large breasts` | `nude, large breasts` |
| Обратный порядок имён `Misato Katsuragi` | `katsuragi misato` |
| 30+ тегов в negative prompt | Максимум 10-15 самых важных |
| Теги несуществующие на Danbooru | Проверяй на [danbooru.donmai.us/tags](https://danbooru.donmai.us/tags) |
| Теги с <100 изображений | Эффект непредсказуем |
| `highres`, `absurdres` в positive | По данным тестов — бесполезны или непредсказуемы |
| Описывать то, что не в кадре | Tag what you see, not what you know |

### Управление приоритетом (если тег игнорируется):

1. **Сделай промпт короче** — убери лишнее
2. **Перемести важный тег в начало** промпта
3. **Используй веса**: `(blue hair:1.2)` — +20% приоритет

> **Источники**:
> - [Just Another Guide — Prompt Engineering Tips](https://civitai.com/articles/8635/just-another-image-generation-guide-for-beginners-pony-diffusion-v6-xl-and-illustrious)
> - [Illustrious Prompting Guide — Bad Tags](https://civitai.com/articles/10962/illustrious-prompting-guide-or-v01-or-generate-anime-art-with-ai)

---

## 14. Примеры готовых промптов

### Простой NSFW (соло)

```json
{
  "prompt": "1girl, explicit, nude, large breasts, long black hair, blue eyes, blush, looking at viewer, lying on back, spread legs, on bed, bedroom, night, masterpiece, newest",
  "guidance_scale": 6.0,
  "num_inference_steps": 28
}
```

### Каноничный персонаж

```json
{
  "prompt": "1girl, boa hancock \(one piece\), explicit, nude, large breasts, long black hair, blue eyes, blush, standing, looking at viewer, simple background, masterpiece, newest",
  "guidance_scale": 6.0
}
```

### Секс-сцена (миссионерская)

```json
{
  "prompt": "1girl, 1boy, explicit, missionary, vaginal, sex, pov, nude, large breasts, blush, ahegao, tongue out, sweat, on bed, bedroom, from above, masterpiece, newest",
  "guidance_scale": 6.0
}
```

### Секс-сцена (догги-стайл)

```json
{
  "prompt": "1girl, 1boy, explicit, doggystyle, sex from behind, vaginal, nude, large breasts, long hair, blush, open mouth, sweat, from side, bedroom, masterpiece, newest",
  "guidance_scale": 6.0
}
```

### Секс-сцена (наездница)

```json
{
  "prompt": "1girl, 1boy, explicit, cowgirl position, girl on top, vaginal, pov, nude, large breasts, bouncing breasts, ahegao, blush, sweat, from below, masterpiece, newest",
  "guidance_scale": 6.0
}
```

### Каноничный персонаж + секс

```json
{
  "prompt": "1girl, 1boy, hinata hyuuga \(naruto\), explicit, missionary, vaginal, sex, nude, large breasts, blush, tears, sweat, open mouth, bedroom, from above, masterpiece, newest",
  "guidance_scale": 6.0
}
```

### Стилизованная сцена

```json
{
  "prompt": "1girl, explicit, nude, large breasts, cowboy shot, looking at viewer, blush, anime screenshot, volumetric lighting, depth of field, simple background, masterpiece, newest",
  "guidance_scale": 6.0
}
```

---

## 15. Полезные ссылки

### Гайды по промптингу

| Ресурс | Описание |
|--------|----------|
| [Illustrious Prompting Guide (wolf999)](https://civitai.com/articles/10962/illustrious-prompting-guide-or-v01-or-generate-anime-art-with-ai) | Самый подробный гайд по Illustrious промптингу |
| [Illustrious Prompt Guide (Optimized)](https://civitai.com/articles/16016/illustrious-prompt-guide-optimized-and-complete) | Оптимизированная версия гайда wolf999 |
| [Tips for Illustrious XL Prompting](https://civitai.com/articles/8380/tips-for-illustrious-xl-prompting-updates) | Советы + структура промптов + примеры |
| [Arctenox's Simple Prompt Guide](https://civitai.com/articles/23210/arctenoxs-simple-prompt-guide-for-illustrious) | Простой гайд для начинающих |
| [Just Another Guide for Beginners](https://civitai.com/articles/8635/just-another-image-generation-guide-for-beginners-pony-diffusion-v6-xl-and-illustrious) | Гайд для новичков (Pony + Illustrious) |
| [Prompt Notebook (CASE Structure)](https://civitai.com/articles/3160/prompt-notebook) | Продвинутая структура промптов CASE |

### NSFW специфика

| Ресурс | Описание |
|--------|----------|
| [Prompting for XXX Poses: A Guide and Library](https://civitai.com/articles/18929/prompting-for-xxx-poses-a-guide-and-library) | Библиотека поз для Illustrious |
| [Helpful Tags — SFW & NSFW](https://civitai.com/articles/8284/guide-helpful-tags-for-image-generation-sdxlpony-sfw-and-nsfw) | NSFW теги и приёмы |
| [Danbooru: Sexual Positions](https://danbooru.donmai.us/wiki_pages/tag_group:sexual_positions) | Полный список поз (Danbooru wiki) |
| [Danbooru: Sex Acts](https://danbooru.donmai.us/wiki_pages/tag_group:sex_acts) | Полный список секс-актов |

### Персонажи и стили

| Ресурс | Описание |
|--------|----------|
| [Recognized Characters List](https://civitai.com/articles/10242/illustrious-xl-v01-recognized-characters-list) | Список распознаваемых персонажей |
| [WAI Character Prompt Generator](https://huggingface.co/spaces/flagrantia/character_select_saa) | Генератор промптов персонажей |
| [Artists for Illustrious XL](https://civitai.com/articles/9309/artists-for-illustrious-xl) | Галерея стилей художников |
| [300 Styles WAI-NSFW](https://huggingface.co/datasets/sieecc/SOKI/blob/main/300Styles-waiNSFW.html) | 300 стилей (скачай HTML) |

### Danbooru справочники

| Ресурс | Описание |
|--------|----------|
| [Danbooru Tag Groups](https://danbooru.donmai.us/wiki_pages/tag_groups) | Все группы тегов |
| [Danbooru Tags](https://danbooru.donmai.us/tags) | Поиск по тегам |
| [Danbooru Related Tags](https://danbooru.donmai.us/related_tag) | Поиск связанных тегов / художников |
| [Danbooru Wiki](https://danbooru.donmai.us/wiki_pages) | Объяснение тегов |
| [Illustrious Visual Dictionary](https://civitai.com/articles/7819/illustrious-xl-v01-visual-dictionary) | Визуальный словарь тегов Illustrious |
