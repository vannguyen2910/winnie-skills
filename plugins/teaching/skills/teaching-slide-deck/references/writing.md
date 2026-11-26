# Viết chữ trên slide và speaker notes

## Biên tập tiếng Việt (bắt buộc, gồm cả notes)

Quy tắc trong `CLAUDE.md` của dự án thắng file này.

- Có skill `vi-edit` thì gọi nó, nó tự điều phối cả chuỗi và chạy lint.
- Chưa có thì gọi theo thứ tự, bằng tên đầy đủ: `vietnamese-writing:translationese-cleaner-vi`, `vietnamese-writing:style-guide-vi`, `vietnamese-writing:grammar-checker-vi`, `vietnamese-writing:humanizer-vi`, rồi `vietnamese-writing:vi-voice` cuối cùng.
- Có `lint_vi.py` thì chạy trên file đã đổi và sửa hết ERROR.
- Không dùng `vietnamese-copy-polish` cho nội dung dạy học.
- Không sửa code, URL, tên sản phẩm. Giữ số liệu, nguồn, ID, `[to confirm]` và mức chắc chắn.
- Dấu nháy cong “ ” và ’ trong chữ người đọc.

**Viết lại nhiều slide hoặc đổi giọng:** gửi hai ba mẫu trước và sau cho Winnie duyệt rồi mới áp cả deck. Học từ những câu Winnie đã sửa trực tiếp trên deck.

## Giọng

Qua hết checklist và lint vẫn có thể nghe như máy. Giọng Winnie đã duyệt:

- Viết như đang nói trên lớp: câu ngắn, ví dụ cụ thể trước.
- Giữ tiếng Anh ở những chữ team vẫn nói (check, findings, share, feedback, implementation).
- Không lặp một khuôn câu (kiểu “AI làm X, rồi bạn kiểm tra”) quá hai lần.
- Không mở notes bằng “Chúng ta đi qua bốn ý theo thứ tự” rồi đọc lại bullet.
- Không thêm câu nối rỗng (“Biết sẽ học gì rồi, phần cuối nói về cách học”).
- Không lặp cùng một câu rào đón qua nhiều slide.

## Chữ trên slide

- Một ý một slide: kicker, tiêu đề, nội dung; số 01/02/03 và callout "Ví dụ" khi cần.
- Mỗi dòng một thông điệp, đọc được trong một cái nhìn.
- Không ghi thời lượng (trừ slide milestone của activity).
- Không nêu tên công cụ AI cụ thể, trừ khi là tên nguồn trích hoặc Winnie yêu cầu (slide công cụ).

### Agenda tuần (bullet của slide lộ trình)

- Bốn dòng, mỗi dòng là **một mục trong agenda**: một chủ đề về tư duy hoặc cách làm việc với AI. Giọng bao quát và có tầm nhìn, cùng kiểu với hai slide “Góc nhìn hiện tại về AI” (`context.html`, `context-2.html`) của deck Lesson 0.
- **Không viết thành danh sách task, không nêu tên method** (Break the brief, blind synthesis, UX Audit…), không viết kiểu “học xong làm được gì”.
- Ví dụ đã duyệt (tuần “Insights you can trust”):
  - Từ dữ liệu rời rạc đến hiểu biết có căn cứ
  - Vai trò của phán đoán khi AI tổng hợp thay bạn
  - Hiểu người dùng để cả team cùng nhìn ra cơ hội
  - Minh bạch giữa điều đã kiểm chứng và điều còn là giả định
- Chủ đề phải có trong lesson của tuần đó, **đối chiếu với deck đang dùng của lesson** (`order` trong `deck.json`, không tính phụ lục). File lesson có thể còn nội dung đã gỡ khỏi deck.
- Method và việc AI làm gì, người học kiểm tra hoặc quyết định gì: nói trong speaker notes.
- Gửi bản chữ cho Winnie duyệt trước khi đưa lên deck.

## Speaker notes

Mục tiêu: Winnie đọc là nói được ngay khi đang đứng dạy.

- Văn bản thuần: không markdown, in đậm, heading, hay nhãn đầu đoạn (không "Nói:", "Ví dụ:"). Chuyển từ outline thì bỏ dấu `>` và `**`.
- Đoạn ngắn 1–3 câu, cách nhau một dòng trống. Cả bản khoảng 150–200 từ; dài hơn chỉ khi slide dày.
- **Slide hiện theo click: viết đúng thứ tự khối hiện ra**, ví dụ đặt ngay sau khối nó minh hoạ, câu chuyển tiếp và câu hỏi ở cuối.
- Có gì nói nấy: câu nối với slide trước, nội dung, giới hạn của quy tắc, chuẩn đánh giá. Bỏ phần slide không cần. Ý không bắt buộc ghi "(tùy chọn)".
- Nói tới đâu viết tới đó thành câu. Chỉ dùng danh sách "- " khi người nghe cần đếm từng mục (ví dụ ba câu hỏi chấm điểm).
- Câu hỏi cho lớp (nếu có) đứng cuối, bắt đầu bằng "Câu hỏi cho lớp:", chỉ một câu hỏi, gắn với case của học viên. Dạy 1:1 thì "Câu hỏi cho bạn:".
- Không thêm phần thời gian trừ khi Winnie yêu cầu.
- Xưng hô: "chúng ta" cho cả nhóm, "bạn" khi nói trực tiếp với học viên. Không dùng "mình" cho cả nhóm. Lời thoại hỏi người được phỏng vấn trong “ ” giữ nguyên "bạn".

Ví dụ đã duyệt:

```text
Tuần này chúng ta xử lý đống evidence note của tuần 2.

AI synthesis từ evidence note, bạn mở note gốc ra check. Insight nào không chỉ được câu nào trong note thì bỏ.

AI làm bản đầu rất nhanh, nên phán đoán mới là phần của bạn. Trước khi đưa note cho AI, bạn viết ra team đang cần quyết định chuyện gì.

Persona, journey map và opportunity giúp cả team nhìn chung một bức tranh. AI viết, bạn chấm điểm và chọn, rồi đưa vào insight hub.

Dòng nào có insight đứng sau thì ghi insight ID, chưa có thì ghi assumption. Nói rõ vậy người khác mới tin được.
```
