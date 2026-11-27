# Định dạng artifact Slides

**Mặc định là deck inline** (`deck.json` không có khoá `format`): mỗi slide tự mang style, không có `deck.css`. Các deck Lesson đều theo kiểu này. Template `.dc.html` trong Design System chỉ để tham khảo layout, không phải đích dựng.

## Tạo deck mới

1. Gọi Artifact `quickstart` với intent `slides`, rồi tạo deck từ `type_url` của loại Slides (có `title`, không file).
2. Cài Design System: `project/ds/<namespace viết thường>/tokens.json` (copy bằng entry `{"artifact": <địa chỉ DS>, "path": "project/tokens.json"}`) và một record trong `designSystems` của `deck.json`.
3. Khai báo font trong `faces` của `deck.json`: Be Vietnam Pro, Inter, JetBrains Mono (Google Fonts), và `syne` cho section divider.
4. Viết `deck.json` trước (đủ `order`), lưu cùng slide bìa, rồi đến các slide còn lại.

Mỗi slide là một file `project/slides/<id>.html` có đúng một `<section id="<id>">`, speaker notes trong một `<aside>` ở cuối.

## Giới hạn của deck inline

- Chỉ dùng thẻ `h1`–`h3`, `p`, `ul`/`ol`, `div`, `img`, `svg`, `table`, `hr`, `x-*`, và trong dòng `b`, `i`, `u`, `a`, `span`, `br`.
- Không dùng `repeat()`, `minmax()`, `max-width`, đơn vị `em` hoặc `rem`, `var()`, `animation`, số dòng của grid, `@import`. Viết cột grid rõ ra (`1fr 1fr 1fr`), dùng `width` thay `max-width`, dùng px.
- Không dùng `:lang()`, `::before`, `::after`, selector thuộc tính, `@media` theo ngôn ngữ. Không đặt được `lang="vi"` từng slide. Chữ tiếng Việt đặt font hiển thị Be Vietnam Pro, không viết in hoa.
- `<section>` là khung layout (flex hoặc grid). Không bọc thêm một `div` cao cố định chứa lưới.
- `display` chỉ dùng `flex`, `grid`, `block` hoặc `none`.
- Ảnh phải là asset đã upload (`/_blob/<id>`), không dùng URL hay `data:`.
- Pinned element nằm trong canvas 1920x1080. Hình trang trí vẽ bằng `<x-shape>`.

## Hiện từng phần theo click

Winnie muốn slide dày chữ hiện từng khối mỗi lần bấm, để học viên không đọc trước. Làm cho **mọi slide có từ hai khối trở lên** (hàng card, danh sách số, cột What/Why/When, bảng nhiều dòng, câu kết).

**Không làm** với: slide chỉ có ảnh hoặc sơ đồ một khối, divider, bìa, slide chỉ có một tiêu đề và một câu, slide hình học phụ thuộc nhau (ma trận 2x2 có trục, flow-shapes), slide đang ẩn.

**Cơ chế:** mỗi khối là phần tử `position:absolute` có `data-build-in="rise N"` (N là thứ tự bấm; cũng dùng được `fade`, `pop`). Không dùng `class="fragment"`, không thêm `deck.css`: đó là cơ chế của deck v5 và làm vỡ deck inline.

- Kicker và tiêu đề giữ trong luồng. Mỗi card, dòng, cột thành khối pinned: `box-sizing:border-box; position:absolute; left; top; width; height`. Bỏ `flex:1`, `height` cũ và wrapper lưới.
- Câu chú hoặc câu kết cuối cũng là một khối, bọc trong `<div style="margin:0">` rồi pin.
- Giữ `top + height <= 952` (lề 96px). Chữ dài hơn khung thì tăng `height`, không giảm cỡ chữ.
- Dùng `scripts/pin_lib.py` (`kids`, `pin`, `endof`, `balanced`).

| Kiểu slide | Khối (px, canvas rộng 1920, lề 96) |
|---|---|
| Danh sách số, tiêu đề trái (agenda, how-audit) | N dòng ở `left 917`, `width 907`, cao `888/N`, `top = 96 + cao*i` (5 dòng: cao 177) |
| Hai card | `left 96 và 976`, `width 848`, `top 300 đến 360`, cao 500 đến 560 |
| Ba card | `left 96 + 584*i`, `width 560`, `top 300 đến 340`, cao 440 đến 640 |
| Ba card có số lớn | `left 96 + 586*i`, `width 554`, `top 300`, cao 540 |
| Bốn card nhỏ | `left 96 + 438*i`, `width 414`, `top 360`, cao 300 |
| Sáu card (3 x 2) | `left 96 + 584*(i%3)`, `top 300 + 274*(i//3)`, `width 560`, cao 250 |
| Bảng nhiều dòng | mỗi dòng một khối, `left 96`, `width 1728`, dòng cao 80 (đầu bảng 48) |
| Bốn thẻ và ba mũi tên | thẻ `left 96/548/1000/1452`, `width 372`; mũi tên chen giữa, `width 48` |

## Dựng slide bằng script

- Không rút chữ từ HTML có sẵn bằng regex rồi dựng lại cả slide; lỗi kiểu này từng để lại `div` không đóng và slide bị khoá chỉ đọc. Dựng từ dữ liệu viết rõ (tiêu đề, mô tả, notes). Sửa slide đã có thì thay đúng đoạn cần đổi.
- Sau khi sửa, số `<div` phải bằng số `</div>` trong từng file (`check_deck.py` kiểm).
- Giữ danh sách các slide làm tay hoặc Winnie đã chỉnh, để script bỏ qua.

## Sửa deck đang có người chỉnh

Winnie sửa trực tiếp trên trang, và có thể có phiên trả lời comment đang sửa cùng lúc.

- Trước **mỗi** lần lưu, đọc lại đúng file sắp sửa và sửa trên bản vừa đọc.
- Chỉ gửi những file đã đổi. Không dựng lại cả deck rồi ghi đè.
- Giữ chỉnh sửa của Winnie (nhãn bìa, phần đã xoá, chữ đã đổi). Lần lưu bị từ chối thì đọc lại bản mới rồi áp lại đúng thay đổi của mình.
- Lần lưu báo đã thay một bản vừa lưu từ trang thì nói rõ file nào bị thay.
- Slide bị đổi phong cách mà bạn không làm thì đọc lại rồi mới sửa tiếp, và nói với Winnie.
- "Giống slide N": mở slide N đếm theo thứ tự **hiện tại** trong `deck.json`, chép khuôn của nó.
- Comment: trả lời đúng thread bằng ArtifactComments, một dòng gọn, không tự đóng thread. Deck thuộc tổ chức khác thì không trả lời được từ đây; báo Winnie.
- Winnie sửa tay cùng một chỗ ở nhiều deck thì ghi quy tắc đó vào skill này.

## Xem trước và kiểm tra

- Bố cục: ghép các `<section>` thành một trang HTML cục bộ (`margin:0` cho `p`, `h1`–`h3`, `*{box-sizing:border-box}`, mỗi slide 1920x1080) rồi chụp bằng trình duyệt headless, hoặc Playwright nếu máy đã cài. Không tự cài thêm. Cách này chỉ xấp xỉ.
- Click reveal: mở Present (nút play). Phím Right hiện thêm một khối, hết khối thì sang slide kế; phím Left lùi về slide trước. Ảnh chụp ngay sau lần bấm đầu có thể còn mờ.
- Khi giao, nói rõ slide nào đã xem ở Present và slide nào chưa; không xem được thì ghi "chưa xem trong trình xem thật".

## Deck có khoá `format` (v5)

Chỉ áp cho deck đã dùng định dạng này.

- `project/deck.css` khai báo mọi token đang dùng (`:root { --ink: ...; }`) và các class layout. Slide dùng class, không dùng `#id`, không `@import`.
- Giá trị của các khuôn trong `layouts.md` đưa vào class, giữ đúng từng giá trị.
- Căn giữa vùng content: bọc phần dưới tiêu đề trong `<div class="bodyx">`, với `.bodyx { flex:1; display:flex; flex-direction:column; justify-content:center; }`, chỉ cho `class="slide"`.
- Card trong specimen dùng class `.frame` (bo 22px, viền 2px ink).
