# Layout

Đọc mục của đúng loại slide đang làm. Slide mới luôn bắt đầu từ một khuôn có sẵn rồi chỉ đổi nội dung.

Thứ tự tìm khuôn:

1. `templates/` của skill này (divider, lộ trình tuần, công cụ).
2. `project/templates/slide-deck/lesson-patterns/` trong Design System (đọc `README.md` ở đó): `method-what-why-when`, `cards-3-icons`, `cards-3-lineart`, `cards-3-numbered`, `steps-vertical`, `compare-2`, `code-and-list`. Mẫu đã có click reveal và kích thước pin đúng.
3. Bảng "Slide chuẩn trong các deck Lesson" trong cùng README, rồi đọc slide đó ở deck Lesson (`lesson-decks.md`) và chép cấu trúc. Báo Winnie để thêm mẫu mới vào Design System.

Làm theo slide thật đã đọc, không dựng lại theo trí nhớ. Nếu `templates/slide-deck/` và `slides/template.html` trong Design System khác nhau, báo Winnie thay vì tự chọn.

## Section divider (trang chương)

Khuôn: `templates/divider.html`. Mẫu thật: `divider-01` của deck Lesson 1, 3, 4, 5. Deck Lesson 2 làm sai trang này, không chép.

- Nền `#f5d028` full-bleed, nội dung căn giữa cả hai chiều, `padding:96px`, `gap:36px`. Không dùng `padding:0` kèm hai khối `flex:1`.
- Số phần (01, 02…) ghim góc trên trái: `top:52px; left:72px; width:700px`, font **Syne** 255px đậm 800, `line-height:1`, `letter-spacing:-10.2px`, màu `#1a1325`. Không dùng Be Vietnam Pro cho số. Phần phụ lục dùng chữ `A`.
- Tiêu đề `h2` rộng 1500px, Be Vietnam Pro 88px đậm 600, `line-height:1.2`, `letter-spacing:-1.8px`, căn giữa. Hai dòng: dòng một `#1a1325`, dòng hai bọc `<span>` màu `#4a24c4`. Một dòng thì cả dòng hoặc từ nhấn là `<span>` tím. Không dùng `#6b3fee` ở đây (không đủ tương phản trên vàng).
- Dòng phụ JetBrains Mono 24px, `letter-spacing:1.9px`, `#3d3552`, căn giữa, một câu ngắn.
- Chỉ có số, tiêu đề, dòng phụ. Không thêm icon, card, ảnh, đường kẻ.
- `deck.json` phải khai báo font `syne` trong `faces` (`src` trỏ `project/ds/<namespace>/fonts/Syne-VariableFont_wght.ttf`), nếu không số rơi về Arial.
- Divider nào cũng có speaker notes: nói phần này gồm gì và nối với phần trước.

## Danh sách số (slide quy trình)

Dùng cho PROCESS, "Cách làm", "Use case", NUMBERED có thứ tự. Mẫu: `how-audit.html` của deck Lesson 6.

- `<section>` là khung `display:grid; grid-template-columns:0.8fr 1fr; gap:96px; padding:96px`.
- Tiêu đề bên trái (rộng khoảng 527px, 64px). Bên phải là danh sách 01, 02… mỗi dòng cao đều, cách nhau bằng đường kẻ mảnh `#14121f26`, không dùng card.
- Số Be Vietnam Pro 48px đậm màu ink; chữ 32px đậm (28px khi có sáu dòng trở lên).

## Line-art feature card

Dùng cho ba đến bốn ý ngang hàng (bằng chứng, lý do, so sánh), mỗi ý một hình. Không dùng card chỉ có chữ. Mẫu: `lesson-patterns/cards-3-lineart.html`; ví dụ thật: `ai-diversity` của Lesson 4, `criteria.html`, `ex-audit-record.html`.

- Card: `display:flex; flex-direction:column; justify-content:space-between; gap:24px; flex:1; padding:36px`, nền trắng, viền 2px ink, bo 22px, hàng `align-items:stretch`.
- Vùng hình: `display:flex; flex-direction:column; align-items:center; justify-content:center; flex:1`, chứa SVG viewBox 200x140, nét 1.4, hiển thị `429x300` (cao 260 đến 300px), không nền riêng hay khung phụ.
- Khối chữ ở đáy: tiêu đề 40px đậm `#1a1325`, mô tả 28px `#3d3552`.
- **Không đánh số** khi các card ngang hàng. Chỉ thêm số (Be Vietnam Pro 44px, `#6b3fee`) khi card thật sự là các bước theo thứ tự; danh sách dọc cũng vậy.
- Tiêu đề giữ một dòng (rút ngắn chữ nếu cần), mô tả có `min-height` đủ cho dòng dài nhất (ví dụ 78px cho hai dòng 28px).

## Lộ trình tuần (agenda mỗi tuần một slide)

Khuôn: `templates/week.html`. Mẫu thật: `week-1.html` đến `week-6.html` của deck Lesson 0. Nội dung bullet viết theo `writing.md`, mục "Agenda tuần".

- `<section>`: `display:flex; flex-direction:column; justify-content:center; gap:24px; padding:96px; background:#ffffff`.
- Cột trái: kicker “Tuần N” (JetBrains Mono 24px, `#1a1325`); `h2` rộng 720px, 72px, hai dòng, dòng hai `#6b3fee`; line-art riêng theo nội dung tuần (nét 1.4, `#1a1325`, hiển thị 400x280).
- Cột phải: bốn dòng pinned `left:917px; width:907px; height:192px; top:156/348/540/732`, `rise 1` đến `rise 4`. Mỗi dòng gồm dấu tích SVG 40x40 (nét 3.5, `#6b3fee`) và chữ Inter 32px rộng 830px, `gap:32px`. Ba dòng đầu có `border-bottom:1px solid #14121f26`.
- Không thêm nhãn “Bạn sẽ học” phía trên danh sách.
- Cả chuỗi giữ nền trắng. Sửa nội dung slide đã có thì giữ nguyên tên tuần và layout, trừ khi Winnie yêu cầu đổi.

## Công cụ (ba card có logo)

Khuôn: `templates/tools.html`. Mẫu thật: `tools.html` của deck Lesson 0 (nền đen).

- Ba card trắng pinned `left 96/680/1264; top 300; width 560; height 600`, mỗi card một click. Vùng logo `flex:1` căn giữa; đáy là tên nhóm 40px và một câu 28px `#3d3552` có `min-height:84px`.
- Một card cho một nhóm công cụ. Một logo thì 180x180; nhiều logo xếp một hàng, khoảng 112x112, `gap:48px`; tăng cỡ logo nào có viền trống trong file cho cân mắt.
- **Logo lấy từ file thật, không tự vẽ.** Tìm trong repo trước. Phải tải về thì hỏi Winnie trước (tên file, nguồn, dung lượng). Mở SVG kiểm không có script hay link ngoài, lưu vào `assets/logos/` của lesson kèm `SOURCES.md` (nguồn, ngày, giấy phép; chưa kiểm thì ghi `[to confirm]`), rồi upload làm asset của deck.
- Mô tả viết chung chung: công cụ dùng để làm gì trong khoá. Không nêu tính năng cụ thể hay thứ phụ thuộc gói tài khoản, vì học viên có thể dùng tài khoản miễn phí.
- Tên công cụ AI chỉ nêu trên slide này khi Winnie yêu cầu. File lesson vẫn dùng "công cụ AI".

## What/Why/When (layout Method)

Slide "X là gì?" theo layout Method (class `method`) của `templates/slide-deck/SlideDeck.dc.html`, không tự biến tấu. Mẫu: `lesson-patterns/method-what-why-when.html`; ví dụ thật: Lesson 1 `hub-purpose`, Lesson 3 `persona-what`, Lesson 4 `hmw-what`, Lesson 6 `what-audit`.

- Hàng đầu: trái là kicker (ví dụ "Định nghĩa") và tiêu đề 72px, dòng "là gì?" màu `#6b3fee`; phải là khung icon 460x230, viền 5px ink, bo 20px.
- Ba cột: viền trên 4px ink, `padding-top` 32px, cách nhau 72px (`left 96/696/1296`, `width 528`, `top 520`, cao 420), hiện lần lượt theo click.
- Nhãn WHAT, WHY, WHEN: JetBrains Mono 24px, `letter-spacing` 1px, cách chữ 24px.
- Nội dung là đoạn văn thường (Inter 28px, `line-height` 1.6, cách đoạn 32px), không chấm tròn đầu dòng. "Không cần khi:" và "Nếu thiếu:" giữ trong đoạn.
- Icon line-art theo nội dung slide: hiển thị `240x168`, nét `#1a1325` dày 1.7. Icon lưới 8 ô của template chỉ dành cho Crazy 8s.
- Kiểu thẻ What/Why/Ẩn dụ (`github-what`, `md-file`) và slide "X là gì?" của Lesson 5 (bullet trái, hình phải) là layout khác, để nguyên.

## Bìa

- Nhãn trên bìa là giai đoạn design process (Discover, Define, Develop, Deliver), lấy từ thư mục của lesson (`01-discover` đến `04-deliver`). Không dùng "Day N" hay "Sau bài X".
- Bên phải chỉ có ảnh. Không chồng tên giảng viên hay lớp phủ màu; tên đã nằm ở dòng năm bên trái.
- Ảnh từ nguồn miễn phí (Pexels, Unsplash), kiểm giấy phép trên trang ảnh. Không dùng ảnh có logo, thương hiệu hoặc tên riêng thật trên màn hình. Cần ảnh có màn hình của bài: lấy ảnh điện thoại màn hình trống rồi ghép màn hình của bài. Lưu ảnh gốc, bản ghép và giấy phép vào `assets/` của lesson (ghi trong `SOURCES.md`), upload bản cuối làm asset.
