# Capture method

Headless Chrome from Bash. Save to the session scratchpad first, view the image, then copy the keeper into `work/competitor-screens/`.

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1440,900 --virtual-time-budget=15000 \
  --screenshot=<scratchpad>/shots/<name>.png "<url>"
```

- Long pages: raise the height (1800, 2600, 3600) so the whole page is in one image. Check the bottom; install-app and cookie pop-ups can cover it.
- macOS has no `timeout`. If a page hangs, kill the Chrome process and record the page as not captured.
- Look at every image with the Read tool before keeping it.
- Mobile layouts are not captured here; real phone screens are the owner's.

## File names
`NN-feature-product-platform.png`, NN = checklist row (two digits), platform `web` or `app`. Examples: `03-search-adplist-web.png`, `11-mentor-signup-codementor-web.png`. One more shot of the same screen: add `-2`.

## Not captured (record, do not work around)
Blank "email us" pages, 403/404, hangs, login walls, CAPTCHAs. Write the URL, what happened and `unknown` in the log. Do not retry with other user agents or tricks.
