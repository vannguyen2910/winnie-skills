# Quick check

Quiz ngắn để học viên đổi nhịp và tự xem còn nhớ gì (chốt 2026-11-27). Đây là bước kiểm tra hiểu bài, không tính là activity theo Rule LP-3.

## Số câu và vị trí

- Mỗi lesson 2 đến 3 câu, không chấm điểm. Không thêm nhiều hơn vì học viên dễ thấy áp lực.
- Một câu ở giữa buổi, ngay sau phần vừa dạy. Một câu cuối buổi, trước Q&A. Câu thứ ba (nếu có) đặt sau một phần lý thuyết dài.
- Mỗi chỗ có một slide mở màu tím rồi tới slide câu hỏi.
- Tránh đặt sát một activity khác hoặc sát một slide đã hỏi cùng ý.
- Cả hai slide mất khoảng 2 đến 3 phút. Tính thời lượng này vào buổi học và nói rõ đã bớt phần nào, hoặc chưa bớt.

## Câu hỏi

- Kiểm tra kiến thức, gắn với cách làm việc cùng AI. Không hỏi mức quá cơ bản (ví dụ "đây là vấn đề hay giải pháp?"). Không dùng transcript, bài phỏng vấn hay case study dài.
- Khoảng 5 đáp án. Được trộn dạng: một đáp án, chọn tất cả đáp án đúng, "Chỉ A và B", "Cả A, B và C", "việc nào KHÔNG nên".
- Câu có nhiều đáp án đúng thì speaker notes phải nói rõ. Hỏi Winnie nếu muốn ghi cả lên slide.
- Chỉ hỏi điều deck đã dạy **trước** slide quiz, kể cả các đáp án nhiễu.
- Đáp án nói về cách một công cụ hay chuẩn hoạt động (cái gì được load, cái gì bị chặn) phải đối chiếu tài liệu chính thức trước khi đưa lên slide. Viết đúng phạm vi: nói rõ trường hợp nào đúng, trường hợp nào là ngoại lệ.
- Thuật ngữ tiếng Việt nghe tối nghĩa thì dùng tiếng Anh (ví dụ "load" thay cho "nạp").
- Gửi Winnie duyệt câu hỏi và đáp án trước khi dựng slide.

## Slide

| Slide | Khuôn | Sửa gì |
|---|---|---|
| Mở | `templates/quick-check-opener.html` | `id`, một câu giới thiệu, notes |
| Câu hỏi | `templates/quick-check-question.html` | `id`, câu hỏi, 5 đáp án, đáp án đúng, giải thích, notes |

- Kicker "Quick check" màu đen. Đáp án và giải thích nằm trong một khung, hiện sau một click (`data-build-in="rise 1"`).
- Câu hỏi dài tối đa hai dòng.
- Khuôn dùng cho deck inline. Deck có `deck.css` (v5) thì đổi click reveal sang `class="fragment"`.

## Slide outline và lesson

- Slide mở: `### MILESTONE · Quick check`, không có `Num:` vì đây không phải phase practice.
- Slide câu hỏi: `### NUMBERED · Quick check 1`, On-slide liệt kê 5 đáp án và dòng "Hiện sau một click: Đáp án …".
- Không đưa câu hỏi quiz vào file lesson. Khi quiz làm lộ một chỗ sai trong lý thuyết thì sửa lesson.
