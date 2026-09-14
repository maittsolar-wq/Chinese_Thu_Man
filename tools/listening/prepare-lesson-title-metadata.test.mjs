import assert from "node:assert/strict";
import { parseLessonFilename } from "./prepare-lesson-title-metadata.mjs";

for (const [filename, id, vietnameseTitle] of [
  ["001-502.mp4", "001", "502"],
  ["002-ban-be-den-giup-do.mp4", "002", "Bạn bè đến giúp đỡ"],
  ["003-ban-cua-ly-huyen.mp4", "003", "Bạn của Lý Huyền"],
  ["004-ban-gai-se-tuc-gian.mp4", "004", "Bạn gái sẽ tức giận"],
  ["022-o-sieu-thi.mp4", "022", "Ở siêu thị"],
]) {
  assert.deepEqual(parseLessonFilename(filename), { id, vietnameseTitle, vietnameseTitleSource: "filename", chineseTitle: null, chineseTitleSource: null, needsReview: true });
}
assert.equal(parseLessonFilename("not-a-lesson.mp4"), null);
console.log("Listening filename metadata parser: OK");
