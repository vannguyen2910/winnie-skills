---
name: screens-from-recording
description: "Turn a screen recording of an app (phone or web) into clean, named screenshots inside an AI Product Workspace project: extract one frame per screen with ffmpeg, drop duplicates and transitions, group the frames by journey, blur personal details with the owner's approval, save them to work/assets/<journey>/NN-name.jpg and log the AI use. Use when the user has a recording, video or screen capture of a walk-through and needs screenshots from it, says 'extract screenshots from my recording', 'lấy ảnh màn hình từ video', 'tách frame', 'quay màn hình', or before a heuristic evaluation, user flow, task analysis or journey map when the screens only exist as a video, even if they do not say 'skill'."
license: MIT
---

# Screens from a recording

Evidence work for a product workspace folder (has `AGENTS.md`, `work/`). Read `AGENTS.md` first: its rules win over this skill. Read `context/data-rules.md` if it exists.

## Why this shape
A recording holds everything the owner did, including addresses, names, driver photos and card numbers. Screens that go into the project must be one clean frame per step, free of personal data, and traceable to the recording. So the AI cuts candidates in a scratch folder, the owner approves them, and only then do they enter `work/assets/`.

## Privacy first
- The raw recording belongs in `work/sources/_raw-private/` (or anywhere outside the project). The AI does not read that folder. Ask the owner once, in chat: "May I process this one recording and look at the frames?" Do not start without a yes. Say what you will do: cut frames, look at them, blur personal details.
- Candidates go to the session scratch folder, never straight into the project.
- Blurring is mandatory for personal data. The owner confirms each blurred screen at full size before it counts.
- Never copy the recording into the project or into any AI-readable folder.

## Steps
1. **Check tools:** `ffmpeg` and `ffprobe` (`brew install ffmpeg` if missing). Ask for the recording's path, the app, the device, the app version and the date of the walk-through; these go into the log.
2. **Cut candidates:**
   ```
   python3 <this skill>/scripts/extract_frames.py <recording> --out-dir <scratch>/candidates
   ```
   It keeps one frame each time the screen settles on something new, and writes `manifest.json` with the times. Tune it, do not edit it: too many frames, raise `--new` (6 default); frames missing, lower `--new`; frames caught mid-animation, raise `--settle` or lower `--fps`.
3. **Look at every candidate** at full size. Drop duplicates, loading skeletons that are not themselves a screen worth keeping, half-finished transitions and notification banners. Keep a loading state only if it is a step of the flow. Scrolled screens: keep the frame that shows the point under review, and say it is partial.
4. **Group by journey** using the journeys in `work/current-user-flow/` or the owner's words, in the order the user went. If the owner has no journeys yet, propose them and wait for a yes.
5. **Blur personal details.** List what you see (names, addresses, phone numbers, driver photos, card and booking numbers, QR codes) and where, then blur with a mosaic, as in the existing screens:
   ```
   ffmpeg -y -i in.jpg -vf "split[a][b];[b]crop=W:H:X:Y,scale=iw/24:ih/24,scale=W:H:flags=neighbor[c];[a][c]overlay=X:Y" out.jpg
   ```
   (X, Y, W, H in pixels of the original.) Show the owner the result. If a face or number is still readable, blur more.
6. **Name and save.** `work/assets/journey-<n>-<name>/NN-short-name.jpg`, two digits in journey order, lowercase words joined by hyphens (`04-payment-methods.jpg`). Never overwrite an existing file; if the folder exists, continue the numbering. Keep each file under 2 MB (resize with `sips -Z 2556` if needed).
7. **Log it** in `work/ai-use-log.md`: date, tool, what was asked, how many screens were kept, "Not yet checked at full size" until the owner says so.
8. **Report:** how many frames were found and how many kept, per journey; which screens are partial; what was blurred; what you are unsure about; where the files are.

## What the owner still has to do
- Say yes to processing the recording.
- Confirm the blur on every screen.
- Tell the AI which journey each screen belongs to if it is not obvious.

## Known quirks
- Phone recordings show a touch-indicator circle and a recording dot in the status bar. They are not removed; mention it to the owner.
- A screen that shows for under about a third of a second may be missed. Raise `--fps` (for example `--fps 6`) and run again.
- The first frame of a recording is often the home screen mid-launch; check it.
- If frames look sideways, the recording has odd rotation metadata: re-export the recording from the phone or tell the owner.
