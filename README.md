# fasel-db

قاعدة بيانات تلقائية لموقع FaselHD تتحدث كل 10 دقائق عبر GitHub Actions.

## الفئات
| الملف | الفئة |
|-------|-------|
| data/movies.json | أفلام أجنبي |
| data/series.json | مسلسلات أجنبية |
| data/hindi.json | أفلام هندي |
| data/asian_movies.json | أفلام آسيوي |
| data/anime_movies.json | أفلام أنمي |
| data/asian_series.json | مسلسلات آسيوية |
| data/tvshows.json | برامج تلفزيونية |
| data/anime.json | أنمي |

## هيكل البيانات
```json
[
  {
    "name": "اسم العمل",
    "img": "رابط الصورة",
    "link": "رابط الصفحة",
    "category": "series"
  }
]
```

## المنطق
- **أول تشغيل:** يسحب كل الصفحات كاملاً
- **التشغيلات التالية:** يتوقف ذكياً عند أول صفحة كل محتواها موجود بالفعل
