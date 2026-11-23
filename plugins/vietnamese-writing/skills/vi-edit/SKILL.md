---
name: vi-edit
description: Biên tập nội dung tiếng Việt cho khoá học của Winnie bằng đúng chuỗi skill và kiểm tra bằng script. Dùng NGAY khi Winnie nói tiếng Việt "kỳ", "gượng", "nghe như dịch", "nghe như AI", "chỉnh văn phong", "sửa tiếng Việt", "viết lại cho tự nhiên", "improve content", "polish", hoặc khi tạo/sửa chữ tiếng Việt trên slide, speaker notes, lesson, slide outline, practice, teleprompter, method card, tin gửi mentee. Điều phối translationese-cleaner-vi, style-guide-vi, grammar-checker-vi, humanizer-vi, rồi vi-voice cuối cùng, chạy lint_vi.py sau khi sửa, và đồng bộ file ghép đôi. KHÔNG dùng vietnamese-copy-polish cho nội dung dạy học (skill đó chỉ cho copy marketing và bài đăng mạng xã hội).
---

# vi-edit

Một điểm vào duy nhất cho mọi việc viết hoặc sửa tiếng Việt trong khoá học. Mục tiêu: Winnie không phải nhắc từng skill và không phải gửi folder skill nữa.

## Quy tắc cứng

1. **Luôn chạy cả chuỗi, đúng thứ tự.** Không tự chọn một vài skill cho "nhanh".
2. **Không dùng `vietnamese-copy-polish`** cho slide, notes, lesson, outline, practice. Skill đó dành cho marketing.
3. **Luôn chạy lint sau khi sửa** và sửa hết ERROR trước khi báo xong.
4. **Dùng đúng bản skill trong plugin `vietnamese-writing`** (tên đầy đủ có tiền tố `vietnamese-writing:`). Bỏ qua các bản trùng tên ở `anthropic-skills:` hay `userSettings:`.
5. **Không tự điền chỗ chưa xác nhận.** Giữ `[to confirm]`, nguồn, số liệu, ID, tên file, mức chắc chắn của evidence. Chỉ đổi cách diễn đạt.

## Quy trình

### 1. Xác định phạm vi
- Loại nội dung: chữ trên slide, speaker notes, lesson, outline, practice, tin nhắn.
- File ghép đôi cần sửa theo (lesson với slide outline, deck với outline, slide với method card).
- Xưng hô của dự án. Deck và notes của khoá AI Design Workflow dùng **"chúng ta"** cho cả nhóm và "bạn" khi nói trực tiếp với học viên; không trộn "mình" cho cả nhóm. Nếu dự án có CLAUDE.md quy định khác thì theo CLAUDE.md.

### 2. Đọc quy tắc
Đọc `../vi-voice/references/vi-voice-rules.md` (bản sao ngay trong plugin). Nếu máy có file gốc trên Drive và file gốc mới hơn, dùng file gốc: `~/Library/CloudStorage/GoogleDrive-*/My Drive/03_Mentoring/_system/rules/vi-voice.md`.

### 3. Chạy chuỗi skill, theo thứ tự này
Gọi từng skill bằng công cụ Skill, đúng tên có tiền tố:
1. `vietnamese-writing:translationese-cleaner-vi`: bỏ câu dịch sát từ tiếng Anh.
2. `vietnamese-writing:style-guide-vi`: xưng hô, thuật ngữ, viết hoa, số, định dạng nhất quán.
3. `vietnamese-writing:grammar-checker-vi`: chính tả, dấu câu, tham chiếu đại từ.
4. `vietnamese-writing:humanizer-vi`: nhịp câu, khuôn lặp, giọng quá trơn.
5. `vietnamese-writing:vi-voice`: **cuối cùng**; khi hai skill mâu thuẫn về giọng và thuật ngữ thì `vi-voice` thắng.

Nội dung nhỏ (một vài câu) vẫn chạy đủ chuỗi, nhưng có thể gộp phần báo cáo.

### 4. Sửa
- Slide Artifact: đọc lại đúng file trước khi sửa, sửa bằng thay thế chính xác, không viết lại cả file. Nếu trang có người đang chỉnh, đọc bản mới nhất ngay trước khi lưu và giữ chỉnh sửa của Winnie.
- Speaker notes: lời nói đủ chủ vị, ví dụ trước khái niệm, mỗi bullet một ý, câu hỏi cho lớp phải là câu hỏi.
- Chữ trên slide: mỗi dòng một thông điệp, đọc được trong một cái nhìn, không ghi thời lượng.

### 5. Lint (bắt buộc)
```bash
python3 "<thư mục skill này>/scripts/lint_vi.py" <file hoặc thư mục> [--notes-only] [--slide-only]
```
Script nhận `.md`, slide `.html` (tách chữ trên slide và `<aside>` notes) hoặc thư mục. Nó bắt: cụm dịch cần tránh, chữ đệm, dấu gạch dài, tên công cụ AI, thời lượng trên slide, "Câu hỏi cho lớp" thiếu dấu hỏi, khuôn câu bị hạn chế, chuỗi câu cụt, trộn "chúng ta" với "mình". ERROR phải sửa hết; WARN đọc lại và quyết, nếu giữ thì nói lý do trong báo cáo.

### 6. Đồng bộ
Sửa deck thì sửa outline và lesson cho khớp (và ngược lại). Chạy lint cả các file ghép đôi.

### 7. Báo cáo cho Winnie (tiếng Việt, ngắn)
- Đã chạy những skill nào, theo thứ tự nào, và kết quả lint (số ERROR, WARN còn lại).
- Đã sửa những file nào, và nhóm lỗi chính.
- Chỗ chưa chắc để Winnie đọc lại. Không khẳng định văn bản "đã tự nhiên".
- Khi Winnie sửa trực tiếp một câu, thêm cặp trước và sau vào bảng "Các dòng Winnie sửa trực tiếp" trong `../vi-voice/references/vi-voice-rules.md` rồi chạy `scripts/sync_rules.sh --to-drive` để bản gốc không bị lệch.

## Cập nhật quy tắc
`scripts/sync_rules.sh` đồng bộ bản sao trong plugin với file gốc trên Drive:
- `sync_rules.sh` (mặc định) chép Drive vào plugin.
- `sync_rules.sh --to-drive` chép plugin ra Drive.
- Thêm cụm mới cần tránh vào danh sách `TRANSLATED` và `FILLER` trong `lint_vi.py` mỗi khi `vi-voice-rules.md` thêm cụm.
