# АзБуки.ML API Documentation

Current stable API endpoint:

```
PLEASE CONTACT rsg.group.here@gmail.com TO GET ACCESS TO OUR API
```

Official API Demo: https://azbuki-ml.com/demo

_JavaScript XMLHttpRequest Example:_

```javascript
var xhr = new XMLHttpRequest();
xhr.open("POST", "${API_ENDPOINT}/sentiment", true);
xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

xhr.onreadystatechange = function() {
  if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
    console.log(this.response);
  }
}

xhr.send(JSON.stringify({ text: "Обичам да ям банани!" }));
```

_JavaScript Fetch API Example:_

```javascript
fetch("${API_ENDPOINT}/sentiment", {
  method: 'POST',
  headers: {
    "Accept": "application/json",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ text: "Обичам да ям банани!" })
}).then(resp => resp.json().then(console.log));
```

# JSON HTTP API:

The API works with standard HTTP POST requests, the body of which should be stringified JSON data. Usually you need to provide a `text` field and some additional fields for the different API routes according to this documentation.

## Text-to-Speech

_API Route:_
```
POST /SpeechSynthesizer
```

_Data:_
```js
{
  "text": "STRING", // REQUIRED
  "apiKey": "STRING", // REQUIRED
  "voice": "STRING - male|female|Rado|Gabbie" // OPTIONAL; Defaults to "male"
}
```

_Request body and headers:_
```js
{
  body: JSON.stringify({text, apiKey, [voice, ...]}),
  headers: {
    "Content-Type": "application/json"
  }
}
```

_Response body and headers:_
```js
{
  status: 200, // 500 | 200
  body: Buffer, // Buffer full of binary data in mp3 format. If there was an internal error (500) the buffer should be empty OR null.
  headers: {
    'Content-Disposition': `attachment; filename=${FILE-UID}.mp3`, // This header could be used to track the file generation logs based on the UUID - e.g. cost, characters synthesized, debugging info.
    .[...]
  }
}
```

_Example:_
```javascript
// Fetch API (DO NOT STORE YOUR API KEY IN A FRONT-END APPLICATION!)
fetch(endpoint, {
  method: 'POST',
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: input, apiKey: API_KEY, voice: 'Gabbie' })
}).then(resp => resp.binary().then(/* save it */));
```
```javascript
// Node.JS with `needle`
needle.post(
  endpoints,
  { text: input, apiKey: API_KEY, voice: 'Gabbie' },
  { json: true },
  function (error, response) {
    if (response.statusCode !== 200) {
      console.error(error);
      console.log(response.body);
    } else {
      fs.writeFileSync('output.mp3', response.body);
    }
  });
```

## Check sentence in Word Knowledge Graph db

_API Route:_
```
POST /sent
```

_Data:_
```json
{ "text": "STRING" }
```

_Example:_
```javascript
fetch("${API_ENDPOINT}/sent", {
  method: 'POST',
  headers: { "Accept": "application/json", "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Той спортува всеки ден." })
}).then(resp => resp.json().then(console.log));

/// RESPONSE:
[
    ["той", null, 1, "именителен падеж", "той", "+вин. не`го, +крат. го, +дат. +остар. не`му, +крат. му, +лично мест.\n#1 За заместване на лице или предмет от мъжки род, за които се говори. _Исках да се срещна с доцент Харалампиев, но когато отидох, той беше излязъл. Тръгнахме за друг ресторант, но той пък беше затворен. Виждал ли си моя квартирант? — Изобщо не съм го виждал. Не съм виждал нито него, нито пък приятелката му._\n#2 За посочване на лица от мъжки род; този, това. _– Той — посочи към мене баща ми — ще дойде с тебе, а другият остава тук._", null, "pronominal_personal", "той\nтой\nнего\nго\nнему # Остаряла форма\nнего\nму\n"],
    ["спортува", null, 0, "сег.вр., 3л., ед.ч. \nДруги форми: \nverb_intransitive_imperfective, мин.св.вр., 2л., ед.ч.; \nverb_intransitive_imperfective, мин.св.вр., 3л., ед.ч.; \n", "спортувам", "спортуваш, +несв. Занимавам се със спорт. _Хубаво е да спортуваш._+същ. [[спортуване]], +ср.", null, "verb_intransitive_imperfective", "ам, [^аъиеоуяю]ам\n\nам\nаш\nа\nаме\nате\nат\n\nах\nа\nа\nахме\nахте\nаха\n\nах\nаше\nаше\nахме\nахте\nаха\n\nай\nайте\n\nал\nалия\nалият\nала\nалата\nало\nалото\nали\nалите\n\nал\nалия\nалият\nала\nалата\nало\nалото\nали\nалите\n\nан\nания\nаният\nана\nаната\nано\nаното\nани\nаните\n\nащ\nащия\nащият\nаща\nащата\nащо\nащото\nащи\nащите\n\nайки\n"],
    ["всеки", null, 1, "м.р., ед.ч. \nДруги форми: \npronominal_general, дателен падеж, предложна форма; \n", "всеки", "вся`ка, вся`ко, +мн. все`ки, _обобщ. мест._\n#1 Като +прил., само +ед. Който и да е елемент измежду елементите в една група, без изключение. _Всяка жена обича красивото. Всеки възпитан човек би постъпил така. Всяка вечер съм у тях. Не всяка година ходя на почивка._\n#2 Като +прил., само +мн. В съчетание с _числ._ бройни — която и да е група от елементи измежду елементите в по-обща група, без изключение. _На всеки два часа се стряскаше._\n#3 Като +същ., само +ед. все`ки, +вин. +остар. все`киго, +дат. +остар. все`киму. Което и да е лице без оглед на пола му измежду лицата в една група, без изключение. _Така всеки знае. Искам да се срещна с всеки от вас поотделно. Това всекиго може да обиди. Всекиму добро струва._\n* _За всеки случай._ — Евентуално.\n* _На всяка цена._ — Непременно.\n* _По всяка вероятност._ — Вероятно.", "(обобщ.мест.) всеки един, дядо и баба\n(обобщ.мест.) кой да е, какъв да е, всякакъв", "pronominal_general", "всеки\nвсеки\n-\n-\nвсекиго\nвсекиму\nвсеки\nвсяка\n-\nвсяко\n-\n- # Няма форма за множествено число.\n-\n"],
    ["ден", null, 1, "ед.ч.", "ден", "деня`т, деня`, +мн. дни, (два) де`на и дни, +м.\n#1 Светлата част от денонощието от сутринта до вечерта. _Цял ден се разхождах из гората._\n#2 Денонощие. _След два дни заминаваме._\n#3 Период, определен за извършване на нещо. _Почивен ден. Пазарен ден. Сватбен ден._\n#4 Само +мн. Време, живот. _Прекарвам дните си в размисли и терзания. Безгрижни детски дни._\n#5 +Спец. В астрономията — промеждутък от време, необходим за завъртането на небесното тяло около оста му, или периодът, когато е огрявано от Слънцето.\n#6 Дата, свързана с някакво събитие или празник. _Рожден ден. Ден на родилната помощ._\n* _Бял ден._ — Добър, спокоен, уреден живот.\n* _Ден до пладне._ — Кратко време, за малко.\n* _Ден за ден._ — Без перспективи за бъдещето.\n* _Дните ми са преброени._ — Малко ми остава да живея, скоро ще умра.\n* _Добър ден!_ — За израз на подигравка, ако някой възприема нещо известно като ново.\n* _Имам дни._ — Ще живея още.\n* _За черни дни._ — В случай на нужда, при необходимост.\n* _И утре е ден._ — За подчертаване, че някаква работа може да се отложи.\n* _Силен на деня._ — Влиятелен, властен.\n* _Утрешния ден._ — Бъдещето.\n* _До ден днешен._ — До днес, до този момент.\n* _Тия дни._ — В близко време; скоро.", "дата, денонощие\nсветлина, видело, слънце", "noun_male", "ен, ден\nен\nеня\nенят\nни\nните\nена, ни\n-\n"]
]
```

## Check word in Word Knowledge Graph db

_API Route:_
```
POST /word
```

_Data:_
```json
{ "text": "STRING" }
```

_Example:_
```javascript
fetch("${API_ENDPOINT}/word", {
  method: 'POST',
  headers: { "Accept": "application/json", "Content-Type": "application/json" },
  body: JSON.stringify({ text: "аванпост" })
}).then(resp => resp.json().then(console.log));

/// RESPONSE:
[["аванпост", null, 1, "ед.ч.", "аванпост", null, null, "noun_male", "0, [^аъиеоуяю]\n0\nа\nът\nове\nовете\nа\n-\n"]]
```

## Part of Speech tagging

_API Route:_
```
POST /pos
```

_Data:_
```json
{ "text": "STRING" }
```

_Example:_
```javascript
fetch("${API_ENDPOINT}/pos", {
  method: 'POST',
  headers: { "Accept": "application/json", "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Петър плет плете." })
}).then(resp => resp.json().then(console.log));

/// RESPONSE:
[
    [
        ["Петър", "PROPN", "Npmsi", "петър", "nsubj", 3], 
        ["плет", "NOUN", "Ncmsi", "плет", "nmod", 1], 
        ["плете", "VERB", "Vpitf-r3s", "плета-(се)", "root", 0]
    ]
]
```

- Universal multilingual labels reference: https://universaldependencies.org/u/pos/
- Bulgarian-specific tagset reference: https://github.com/AzBuki-ML/public-data/blob/master/pos_tagset/pos_tagset.json

## Comma predictions

_API Route:_
```
POST /pnct
```

_Data:_
```json
{ "text": "STRING" }
```

_Example:_
```javascript
fetch("${API_ENDPOINT}/pnct", {
  method: 'POST',
  headers: { "Accept": "application/json", "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Ясно е че децата които растат с домашни любимци се учат в ранна възраст да проявяват отговорно отношение." })
}).then(resp => resp.json().then(console.log));

/// RESPONSE:
[ "Ясно", "е", ",COMMA", "че", "децата", ",COMMA", "които", "растат", "с", "домашни", "любимци", ",COMMA", "се", "учат", "в", "ранна", "възраст", "да", "проявяват", "отговорно", "отношение" ]
```

## Sentiment analysis

Positive/Negative and Neutral/Expressive evaluation.

_API Route:_
```
POST /sentiment
```

_Data:_
```json
{ "text": "STRING" }
```

_Example:_
```javascript
fetch("${API_ENDPOINT}/sentiment", {
  method: 'POST',
  headers: { "Accept": "application/json", "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Обичам да ям сладолед!" })
}).then(resp => resp.json().then(console.log));

/// RESPONSE:
[
    13.865050315856934, // N < 0.5: neutral; N > 0.5: expressive;
    13.826891899108887  // N < 0.5: negative; N > 0.5: positivie;
]
```

## Positive/Negative word lexicons

_API Route:_
```
POST /lex
```

_Data:_
```json
{ "text": "STRING" }
```

_Example:_
```javascript
fetch("${API_ENDPOINT}/lex", {
  method: 'POST',
  headers: { "Accept": "application/json", "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Обичам морето, ала мразя, когато изгарям." })
}).then(resp => resp.json().then(console.log));

/// RESPONSE
[
    {"coefficient": 0.166, "count": 1, "dictionary": {"мразя": 1}, "total_words": 6, "unique_count": 1}, // negative
    {"coefficient": 0.166, "count": 1, "dictionary": {"обичам": 1}, "total_words": 6, "unique_count": 1} // positive
]
```

## Text Generation and Smart Suggestions

Generates `amount` number of words that cloud come after the inputted `text` in natural speech.

_API Route:_
```
POST /gen
```

_Data:_
```json
{
  "text": "STRING",
  "amount": "INTEGER"
}
```

- The `amount` field is **optional**. It defaults to `3`.

_Example:_
```javascript
fetch("${API_ENDPOINT}/gen", {
  method: 'POST',
  headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: "Да бъдеш или да", amount: 2 })
}).then(resp => resp.json().then(console.log));

/// RESPONSE
["не", "бъдеш"]
```

# Deprecated: GET Requests REST API:

_JavaScript Example:_

```javascript
fetch("${API_ENDPOINT}/api?sentiment=" + "Обичам да ям банани!")
  .then(resp => resp.json().then(console.log));
```

## Check sentence in Word Knowledge Graph db

_Usage (Deprecated):_
```
GET /api?sent=SENTENCE
```

_Example:_
```
GET /api?sent=Той%20спортува%20всеки%20ден

[
    ["той", null, 1, "именителен падеж", "той", "+вин. не`го, +крат. го, +дат. +остар. не`му, +крат. му, +лично мест.\n#1 За заместване на лице или предмет от мъжки род, за които се говори. _Исках да се срещна с доцент Харалампиев, но когато отидох, той беше излязъл. Тръгнахме за друг ресторант, но той пък беше затворен. Виждал ли си моя квартирант? — Изобщо не съм го виждал. Не съм виждал нито него, нито пък приятелката му._\n#2 За посочване на лица от мъжки род; този, това. _– Той — посочи към мене баща ми — ще дойде с тебе, а другият остава тук._", null, "pronominal_personal", "той\nтой\nнего\nго\nнему # Остаряла форма\nнего\nму\n"],
    ["спортува", null, 0, "сег.вр., 3л., ед.ч. \nДруги форми: \nverb_intransitive_imperfective, мин.св.вр., 2л., ед.ч.; \nverb_intransitive_imperfective, мин.св.вр., 3л., ед.ч.; \n", "спортувам", "спортуваш, +несв. Занимавам се със спорт. _Хубаво е да спортуваш._+същ. [[спортуване]], +ср.", null, "verb_intransitive_imperfective", "ам, [^аъиеоуяю]ам\n\nам\nаш\nа\nаме\nате\nат\n\nах\nа\nа\nахме\nахте\nаха\n\nах\nаше\nаше\nахме\nахте\nаха\n\nай\nайте\n\nал\nалия\nалият\nала\nалата\nало\nалото\nали\nалите\n\nал\nалия\nалият\nала\nалата\nало\nалото\nали\nалите\n\nан\nания\nаният\nана\nаната\nано\nаното\nани\nаните\n\nащ\nащия\nащият\nаща\nащата\nащо\nащото\nащи\nащите\n\nайки\n"],
    ["всеки", null, 1, "м.р., ед.ч. \nДруги форми: \npronominal_general, дателен падеж, предложна форма; \n", "всеки", "вся`ка, вся`ко, +мн. все`ки, _обобщ. мест._\n#1 Като +прил., само +ед. Който и да е елемент измежду елементите в една група, без изключение. _Всяка жена обича красивото. Всеки възпитан човек би постъпил така. Всяка вечер съм у тях. Не всяка година ходя на почивка._\n#2 Като +прил., само +мн. В съчетание с _числ._ бройни — която и да е група от елементи измежду елементите в по-обща група, без изключение. _На всеки два часа се стряскаше._\n#3 Като +същ., само +ед. все`ки, +вин. +остар. все`киго, +дат. +остар. все`киму. Което и да е лице без оглед на пола му измежду лицата в една група, без изключение. _Така всеки знае. Искам да се срещна с всеки от вас поотделно. Това всекиго може да обиди. Всекиму добро струва._\n* _За всеки случай._ — Евентуално.\n* _На всяка цена._ — Непременно.\n* _По всяка вероятност._ — Вероятно.", "(обобщ.мест.) всеки един, дядо и баба\n(обобщ.мест.) кой да е, какъв да е, всякакъв", "pronominal_general", "всеки\nвсеки\n-\n-\nвсекиго\nвсекиму\nвсеки\nвсяка\n-\nвсяко\n-\n- # Няма форма за множествено число.\n-\n"],
    ["ден", null, 1, "ед.ч.", "ден", "деня`т, деня`, +мн. дни, (два) де`на и дни, +м.\n#1 Светлата част от денонощието от сутринта до вечерта. _Цял ден се разхождах из гората._\n#2 Денонощие. _След два дни заминаваме._\n#3 Период, определен за извършване на нещо. _Почивен ден. Пазарен ден. Сватбен ден._\n#4 Само +мн. Време, живот. _Прекарвам дните си в размисли и терзания. Безгрижни детски дни._\n#5 +Спец. В астрономията — промеждутък от време, необходим за завъртането на небесното тяло около оста му, или периодът, когато е огрявано от Слънцето.\n#6 Дата, свързана с някакво събитие или празник. _Рожден ден. Ден на родилната помощ._\n* _Бял ден._ — Добър, спокоен, уреден живот.\n* _Ден до пладне._ — Кратко време, за малко.\n* _Ден за ден._ — Без перспективи за бъдещето.\n* _Дните ми са преброени._ — Малко ми остава да живея, скоро ще умра.\n* _Добър ден!_ — За израз на подигравка, ако някой възприема нещо известно като ново.\n* _Имам дни._ — Ще живея още.\n* _За черни дни._ — В случай на нужда, при необходимост.\n* _И утре е ден._ — За подчертаване, че някаква работа може да се отложи.\n* _Силен на деня._ — Влиятелен, властен.\n* _Утрешния ден._ — Бъдещето.\n* _До ден днешен._ — До днес, до този момент.\n* _Тия дни._ — В близко време; скоро.", "дата, денонощие\nсветлина, видело, слънце", "noun_male", "ен, ден\nен\nеня\nенят\nни\nните\nена, ни\n-\n"]
]
```

## Check word in Word Knowledge Graph db

_Usage (Deprecated):_
```
GET /api?word=WORD
```

_Example:_
```
GET /api?word=аванпост

[["аванпост", null, 1, "ед.ч.", "аванпост", null, null, "noun_male", "0, [^аъиеоуяю]\n0\nа\nът\nове\nовете\nа\n-\n"]]
```

## Part of Speech tagging

_Usage (Deprecated):_
```
GET /api?pos=SENTENCE
```

_Example:_
```
GET /api?pos=Петър плет плете

[
    [
        ["Петър", "PROPN", "Npmsi", "петър", "nsubj", 3], 
        ["плет", "NOUN", "Ncmsi", "плет", "nmod", 1], 
        ["плете", "VERB", "Vpitf-r3s", "плета-(се)", "root", 0]
    ]
]
```

- Universal multilingual labels reference: https://universaldependencies.org/u/pos/
- Bulgarian-specific tagset reference: https://github.com/AzBuki-ML/public-data/blob/master/pos_tagset/pos_tagset.json

## Comma predictions

_Usage (Deprecated):_
```
GET /api?pnct=SENTENCE
```

_Example:_
```
GET /api?pnct=Ясно е че децата които растат с домашни любимци се учат в ранна възраст да проявяват отговорно отношение

[
    "Ясно", "е", ",COMMA", "че", "децата", ",COMMA", "които", "растат", "с", "домашни", "любимци", ",COMMA", "се", "учат", "в", "ранна", "възраст", "да", "проявяват", "отговорно", "отношение"
]
```

## Sentiment analysis

Positive/Negative and Neutral/Expressive evaluation.

_Usage (Deprecated):_

```
GET /api?sentiment=SENTENCE
```

_Example:_
```
GET /api?sentiment=Обичам да ям сладолед

[
    13.865050315856934, // N < 0.5: neutral; N > 0.5: expressive;
    13.826891899108887  // N < 0.5: negative; N > 0.5: positivie;
]
```

## Positive/Negative word lexicons

_Usage (Deprecated):_
```
GET /api?lex=SENTENCE
```

_Example:_
```
GET /api?lex=Обичам морето, ала мразя, когато изгарям

[
    {"coefficient": 0.166, "count": 1, "dictionary": {"мразя": 1}, "total_words": 6, "unique_count": 1}, // negative
    {"coefficient": 0.166, "count": 1, "dictionary": {"обичам": 1}, "total_words": 6, "unique_count": 1} // positive
]
```
