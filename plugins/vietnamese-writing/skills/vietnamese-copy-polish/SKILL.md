---
name: vietnamese-copy-polish
description: "Chuốt copy marketing tiếng Việt cho Facebook, TikTok, YouTube, Zalo, email, web. Dùng khi nói 'chuốt caption', 'sửa bài đăng', 'viết content'; không dùng cho tài liệu giảng dạy."
license: MIT
metadata:
  author: ducpt
  homepage: https://ducpt.com
  version: "1.0.0"
---

# Vietnamese Copy Polish

AI-written Vietnamese is easy to spot: translated idioms, long dashes, stiff formal pronouns and no clear ask. This skill finds those problems with a script, then fixes them by hand.

## Step 1. Lint

Save the copy to a file and run:

```bash
python3 "<this skill>/scripts/check_copy.py" post.txt --platform facebook
```

The script reports: en dash and em dash characters (always replace them), sentences over 35 words, share of words without diacritics, repeated words, missing call to action, and length versus the platform target. Platforms: facebook, tiktok, youtube-title, youtube-description, zalo, email, web.

## Step 2. Rewrite rules

1. Replace every en dash (U+2013) and em dash (U+2014) with a comma, a colon or a full stop. Hyphens inside words (live-edge, 3-tier) are fine.
2. Pick one pronoun pair and keep it (mình / bạn, em / anh chị, chúng tôi / quý khách). Do not mix.
3. Cut translated phrases: "trong thế giới ngày nay", "hãy cùng khám phá", "không chỉ... mà còn..." used as decoration, "một cách hiệu quả".
4. First line must carry a number, a contrast or a concrete scene. No greetings as a hook.
5. Short and long sentences alternate. One idea per sentence.
6. End with exactly one clear ask (comment a keyword, click the link, reply "OK", call the number).
7. Keep brand names, prices and dates exactly as given.

## Step 3. Return

Return the rewritten copy first, then a short list of what changed and why, then the lint result of the new version (run the script again). The new version must show zero dash errors.

## Platform targets (characters)

| Platform | Target |
|---|---|
| facebook | 400 to 1500 |
| tiktok | 80 to 300 |
| youtube-title | 40 to 70 |
| youtube-description | 300 to 1500 |
| zalo | 150 to 600 |
| email | 500 to 2000 |
| web | 800 and up |
