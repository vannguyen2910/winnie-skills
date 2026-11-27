---
name: vi-voice
description: "Viết hoặc viết lại tiếng Việt theo giọng Winnie cho lesson, slide, teleprompter, tài liệu mentee. Dùng khi nói 'viết theo giọng của mình', 'chỉnh văn phong', 'dịch sang tiếng Việt'."
---

# vi-voice

Viết hoặc viết lại nội dung tiếng Việt theo đúng văn phong của Winnie.

## Nguồn quy tắc

Đọc toàn bộ file này trước khi viết bất cứ câu nào:

`<03_Mentoring>/_system/rules/vi-voice.md`

`<03_Mentoring>` là thư mục Mentoring trên Google Drive của máy này, tìm bằng:

```bash
ls -d ~/Library/CloudStorage/GoogleDrive-*/"My Drive"/03_Mentoring
```

Nếu làm việc trong thư mục 03_Mentoring, đọc thêm `CLAUDE.md` ở gốc (quy tắc sync lesson và slide outline, không tên tool AI cụ thể, không tên mentee). Nếu cần cấu trúc riêng của khoá AI Prototype Development, đọc `programs/online-course/AI Prototype Development/writing-style-guide.md`. `vi-voice.md` thắng khi có mâu thuẫn về giọng văn và từ vựng.

Ví dụ áp dụng thực tế: `programs/ai-design-workflow/learning/voice-sample-vi.md`.

## Quy trình

1. **Xác định việc cần làm:** viết mới, hay viết lại một file có sẵn (bản dịch, bản nháp). Nếu là file có sẵn, đọc hết trước khi sửa.
2. **Giữ nguyên ý và cấu trúc.** Không thêm nội dung, không mở rộng, không tự tái cấu trúc. Chỉ đổi cách diễn đạt.
3. **Áp dụng quy tắc trong `vi-voice.md`:**
   - Giọng đồng nghiệp: câu ngắn, ví dụ cụ thể trước, khái niệm sau.
   - Bỏ chữ đệm khi nói và các cụm dịch từ tiếng Anh trong hai bảng của file.
   - Tiêu đề, Kicker, nhãn What/Why/When/Where AI helps bằng tiếng Anh; nội dung bằng tiếng Việt.
   - Giữ thuật ngữ nghề bằng tiếng Anh (danh sách trong file).
   - Không ghi thời lượng trên slide.
   - Mục "Giọng mentor, bớt khẩu hiệu" (2026-11-17) thắng mọi chỗ cũ: không slogan, không lặp khuôn "Không phải X, mà là Y" hay "AI làm X, designer làm Y", không dịch thẳng từ tiếng Anh, speaker notes viết như lời đứng lớp có ví dụ và nhận xét nghề. Chỗ nào chỉ cần nói đơn giản thì dừng.
4. **Giữ các thứ phải giữ:** tên field, layout type, front matter, link, code block, tên file, URL.
5. **Đồng bộ file ghép đôi:** lesson và slide outline, slide và method card. Sửa một bên thì kiểm tra và sửa bên còn lại.
6. **Kiểm tra** theo danh sách cuối `vi-voice.md`: tìm chữ đệm, tìm cụm dịch, đọc to vài câu. Thêm ba câu hỏi: câu nào đang cố thành một thông điệp lớn mà chỉ cần nói đơn giản? Có khuôn câu nào lặp quá hai lần trong cùng một slide hay một đoạn notes không? Notes đọc lên có giống một mentor đang nói, hay giống tài liệu hướng dẫn?
7. **Thứ tự khi chạy cùng các skill biên tập khác** (`translationese-cleaner-vi`, `style-guide-vi`, `grammar-checker-vi`, `humanizer-vi`): chạy chúng trước, `vi-voice` sau cùng. Khi hai bên mâu thuẫn về giọng và thuật ngữ thì theo `vi-voice`.

## Khi báo cáo cho Winnie

- Trả lời bằng tiếng Việt.
- Nói ngắn gọn đã sửa những file nào và theo nguyên tắc nào.
- Nêu những chỗ bạn không chắc, để Winnie đọc lại. Đừng khẳng định văn bản đã "tự nhiên" khi chưa có người bản ngữ đọc.
- Khi Winnie sửa một câu, thêm cặp trước và sau vào bảng "Các dòng Winnie sửa trực tiếp" trong `vi-voice.md` để lần sau áp dụng đúng.
