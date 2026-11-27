# Quy tắc hình ảnh

Đọc file này trước khi dựng hoặc sửa giao diện của bất kỳ slide nào. README của Design System là nguồn đúng nhất; file này ghi các điểm Winnie đã chốt thêm.

## Chung

- Không thêm layout, font hay cỡ chữ mới nếu chưa được yêu cầu.
- Chữ nhỏ nhất **24px** (README Design System ghi 18px, skill theo mức nghiêm hơn).
- Cỡ chữ và màu lấy theo token. Tương phản đạt WCAG 2.1 AA.
- Không emoji.

## Màu nền

Deck toàn nền trắng thì nhàm. Slide nội dung được dùng nền đen hoặc tím để đổi nhịp, theo vai trò cố định (Winnie chốt trên deck Lesson 0).

| Nền | Mã màu | Dùng cho |
|---|---|---|
| Vàng | `#f5d028` (`--yellow`) | **Chỉ section divider.** Statement hay slide nội dung không dùng vàng |
| Đen | `#1a1325` (`--ink`) | Slide ít chữ cần người học dừng lại: câu hỏi mở đầu, công cụ |
| Tím | `#4a24c4` (`--purple-deep`) | Slide chuyển ý, statement, đối tượng. Milestone và takeaway giữ tím của mẫu (`--sienna`) và vẫn tính là nền đậm |
| Trắng | `#ffffff` | Mặc định. Slide nhiều chữ, nhiều số liệu, so sánh, bảng, danh sách |

**Hai slide nền đậm (đen, tím) không đứng liền nhau** (“cảm giác rất là nặng nề”).

- Trước khi đổi nền, xem slide đang hiện ngay trước và ngay sau trong `order` của `deck.json` (bỏ qua slide có `hidden`). Đổi thứ tự, ẩn hoặc bỏ ẩn slide thì kiểm lại.
- Chuỗi slide cùng khuôn đứng liền nhau (ví dụ sáu slide tuần) giữ nền trắng. Không đổi cả chuỗi sang đen, tím hay nửa đen nửa trắng.

**Đổi nền một slide đã có** (chỉ đổi màu, giữ chữ, bố cục, click reveal và notes):

- Đổi `background` của `<section>`.
- Chữ nằm trực tiếp trên nền: kicker và tiêu đề `#ffffff`, từ nhấn `#d9ccff` (tím nhạt; chưa có token trong Design System). Không dùng `#6b3fee` làm chữ trên nền đậm. Không dùng vàng làm từ nhấn, vì vàng dành cho section.
- Card giữ nền trắng, chữ trong card giữ nguyên màu.
- Line-art nằm trực tiếp trên nền đổi `stroke` sang `#ffffff`. Logo và ảnh màu tối đặt trong card trắng.
- Tương phản đã tính: trắng trên đen 18:1, trắng trên `#4a24c4` 9:1, `#d9ccff` trên đen 12:1.

Deck chưa dùng quy tắc này thì đề xuất slide nào đổi, thử trước một hai slide cho Winnie xem rồi mới áp phần còn lại.

## Kicker

| Slide | Màu kicker |
|---|---|
| Slide thường nền trắng, dòng năm ở bìa | `--ink` (không dùng sienna) |
| Slide thường nền đen hoặc tím | trắng |
| Slide What/Why/When (Method), kể cả nhãn WHAT, WHY, WHEN | `#4a24c4` theo template |

## Card

- Mọi card và khung (specimen, mẫu chữ, thẻ bài tập) nền trắng, viền 2px `--ink`, bo `--radius-lg` (22px). Outline ghi "square corners" thì vẫn theo Design System. Không dùng ô viền xám bo 12px.
- **Card trong cùng một hàng phải cùng cấp:** không card nào nền đen, vàng hay tím nhạt, không card nào nhấn riêng, kể cả hàng so sánh hai bên. Không card nào có nền `--ink` hay chữ vàng. Nhấn mạnh bằng nội dung: số hoặc nhãn màu tím, icon ✓ và ✕, hoặc một dòng chốt bên dưới.
- Ngoại lệ duy nhất: trong sơ đồ (tree, flow), một node gốc nền đen chữ trắng, các node còn lại trắng.
- Sửa deck cũ: chạy `scripts/fix_cards.py` (xem `SKILL.md`). Nếu sửa tay, quét `background:#1A1325`, `#F5D028`, `#EAE0FF` trên các `div` có `border-radius:22px`, đổi về trắng, chữ trắng thành mực, nhãn vàng thành tím đậm `#4A24C4`.
- Các card trong một hàng căn thẳng hàng: số, tiêu đề, mô tả bắt đầu cùng một mức.
- Hai card hoặc khung so sánh đặt cạnh nhau phải cùng chiều cao: đặt `height` đủ cho khối dài hơn, `display:flex; flex-direction:column; justify-content:center`.

## Icon và line-art

- Icon chỉ lấy từ fonts.google.com/icons (Material Symbols Rounded) hoặc `<x-icon>`.
- Ngoại lệ: khung icon của slide What/Why/When và **mọi icon đặt trong khung riêng** dùng line-art, vẽ theo đúng nội dung slide đó (không dùng chung một icon).
- Line-art: SVG `viewBox="0 0 200 140"`, `fill:none`, đầu nét và góc bo tròn, không tô màu, không gradient, có `role="img"` và `aria-label`. Vẽ tay bằng hình cơ bản. Độ dày nét và kích thước theo từng layout trong `layouts.md`.

## Bố cục dọc

- Kicker, tiêu đề và câu lead giữ chỗ cố định ở trên. Phần còn lại (hình, card, khung, so sánh) nằm giữa theo chiều dọc của khoảng trống còn lại.
- Không đặt `justify-content:center` lên cả slide, vì tiêu đề sẽ trôi theo nội dung. Ngoại lệ: slide lộ trình tuần (cột trái căn giữa theo chiều cao slide), section divider, statement.
- Không áp quy tắc căn giữa vùng content cho cover, section divider, milestone, statement, và slide đã có một hàng cao gần kín canvas (ví dụ ảnh điện thoại 888px).
- Hàng có nhiều khối cao thấp khác nhau (hình SVG cạnh khung chữ): `align-items:center`, không `flex-start`.
- Hàng trạng thái (default, hover, disabled…) phải khác nhau nhìn thấy được (viền nhạt cho disabled, nét đứt cho loading hoặc empty).
