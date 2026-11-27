---
name: vietnamese-transcript-cleaner
description: "Làm sạch transcript, phụ đề SRT/VTT tiếng Việt và tóm tắt quyết định, việc cần làm. Dùng khi nói 'bóc băng', 'gỡ băng', 'tóm tắt cuộc họp', 'thêm dấu'."
license: MIT
metadata:
  author: ducpt
  homepage: https://ducpt.com
  version: "1.0.0"
---

# Vietnamese Transcript Cleaner

Raw Vietnamese captions are hard to read: lines break mid sentence, diacritics are missing, names are misheard and there is no punctuation. This skill turns them into a clean document plus a useful summary.

## Step 1. Normalize the file

If the input is an `.srt` or `.vtt` file, run the bundled script first. It strips numbering and cue timing, merges short cues into paragraphs and keeps one timestamp per paragraph:

```bash
python3 "<this skill>/scripts/clean_subs.py" input.srt > merged.txt
python3 "<this skill>/scripts/clean_subs.py" input.vtt --gap 2.5 --max-chars 600 > merged.txt
```

`--gap` starts a new paragraph when the silence between cues is longer than N seconds (default 2.0).
If the input is plain text, skip this step.

## Step 2. Clean the language (work paragraph by paragraph)

1. Restore diacritics only when the intended word is unambiguous from context. If two readings are plausible (for example "ban" could be "bạn", "bán" or "bàn"), pick the one that fits the sentence and mark truly unclear spots with `[?]`.
2. Add punctuation and capitalization. Vietnamese sentences in speech are long; split at natural pauses.
3. Remove fillers that carry no meaning: "ờ", "ừm", "à thì", "kiểu như là" when repeated, "đúng không" used as a tic. Keep them only if the user wants a verbatim transcript.
4. Fix misheard proper nouns using a glossary. Ask the user once for names of people, brands and products if many are garbled.
5. Never change numbers, prices, dates or commitments. If a number is unclear, keep it and flag `[?]`.

## Step 3. Speakers

If the source has no speaker labels, infer turns from context (questions and answers, "anh", "em", self-introductions) and label them `Người 1`, `Người 2` unless names are known. Say clearly that labels are inferred.

## Step 4. Output format

```
# <Title of the meeting or video>
Thời lượng: <hh:mm:ss> · Người nói: <list>

## Tóm tắt (5 dòng)
## Quyết định
## Việc cần làm
| Việc | Người làm | Hạn |
## Bản ghi đã làm sạch
[00:00:12] Người 1: ...
```

Write the summary in the same language as the transcript. Keep the cleaned transcript complete; do not summarize inside it.

## Quality checks before returning

- No paragraph longer than about 120 words.
- Every action item has an owner or is marked "chưa rõ người làm".
- Count of `[?]` marks is reported at the end so the user knows how much to review.
