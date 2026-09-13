import type {
  ListeningLevel,
  ListeningLevelId,
  ListeningLesson,
  ListeningDialogueLine,
  ListeningVocabularyItem,
} from "./types";
import type { HskLevel } from "@/lib/data/types";

/**
 * Mock Listening catalog — the current, active data source behind
 * `listeningRepository.ts` (see that file for the seam that lets a real
 * B2-backed source replace this one later without touching any
 * page/component). Nothing here reads from or duplicates data/hsk/**.
 *
 * Dialogue lines use the exact same `id`/`start`/`end` field names as
 * transcript.json's `sentences[]` (see types.ts's comment) purely so a
 * human reading this file can see the real-data shape it's standing in
 * for — mock lines never set `end` (nothing here needs it), and their
 * ids ("s01".."s04") are scoped per-lesson, not globally unique, matching
 * how a real per-lesson transcript.json would number its own sentences.
 */

export const LISTENING_LEVELS: ListeningLevel[] = [
  {
    id: "hsk1",
    hskLevel: 1,
    name: "HSK 1",
    lessonCount: 30,
    description: "Hội thoại cơ bản, gần gũi cuộc sống.",
    listDescription: "30 bài nghe với những tình huống giao tiếp cơ bản, gần gũi trong cuộc sống.",
  },
  {
    id: "hsk2",
    hskLevel: 2,
    name: "HSK 2",
    lessonCount: 108,
    description: "Mở rộng vốn từ, nhiều tình huống thực tế hơn.",
    listDescription: "108 bài nghe mở rộng vốn từ với nhiều tình huống giao tiếp thực tế hơn.",
  },
  {
    id: "hsk3",
    hskLevel: 3,
    name: "HSK 3",
    lessonCount: 16,
    description: "Hội thoại phong phú, nâng cao khả năng nghe hiểu.",
    listDescription: "16 bài nghe phong phú giúp nâng cao khả năng nghe hiểu của bạn.",
  },
];

export function getListeningLevel(id: string): ListeningLevel | null {
  return LISTENING_LEVELS.find((level) => level.id === id) ?? null;
}

interface LessonTemplate {
  slug: string;
  label: string;
  chineseTitle: string;
  vietnameseTitle: string;
  durationSeconds: number;
  dialogue: ListeningDialogueLine[];
  vocabulary: ListeningVocabularyItem[];
}

function line(id: string, chinese: string, pinyin: string, vietnamese: string, start: number): ListeningDialogueLine {
  return { id, chinese, pinyin, vietnamese, start };
}

function vocab(chinese: string, pinyin: string, meaningVi: string): ListeningVocabularyItem {
  return { chinese, pinyin, meaningVi };
}

/** 8 curated scenario templates — cycled to fill each level's lesson count.
 *  Content is representative HSK1-level mock dialogue, not a real catalog. */
const LESSON_TEMPLATES: LessonTemplate[] = [
  {
    slug: "502",
    label: "502",
    chineseTitle: "初次见面",
    vietnameseTitle: "Bữa tối công bằng",
    durationSeconds: 54,
    dialogue: [
      line("s01", "你好，我是小明。", "Nǐ hǎo, wǒ shì Xiǎomíng.", "Xin chào, mình là Tiểu Minh.", 0),
      line("s02", "你好，我是小红。", "Nǐ hǎo, wǒ shì Xiǎohóng.", "Xin chào, mình là Tiểu Hồng.", 5),
      line("s03", "很高兴认识你。", "Hěn gāoxìng rènshi nǐ.", "Rất vui được làm quen với bạn.", 9),
      line("s04", "我也是。", "Wǒ yě shì.", "Mình cũng vậy.", 13),
    ],
    vocabulary: [
      vocab("你好", "nǐ hǎo", "xin chào"),
      vocab("是", "shì", "là"),
      vocab("高兴", "gāoxìng", "vui"),
      vocab("认识", "rènshi", "quen biết"),
    ],
  },
  {
    slug: "ban-be",
    label: "朋友",
    chineseTitle: "好朋友",
    vietnameseTitle: "Bạn bè thân thiết",
    durationSeconds: 72,
    dialogue: [
      line("s01", "你好，你叫什么名字？", "Nǐ hǎo, nǐ jiào shénme míngzi?", "Chào bạn, bạn tên gì?", 0),
      line("s02", "我叫小华，你呢？", "Wǒ jiào Xiǎohuá, nǐ ne?", "Mình tên là Tiểu Hoa, còn bạn?", 4),
      line("s03", "我们是好朋友吗？", "Wǒmen shì hǎo péngyou ma?", "Chúng ta là bạn tốt phải không?", 9),
      line("s04", "对，我们是好朋友。", "Duì, wǒmen shì hǎo péngyou.", "Đúng vậy, chúng ta là bạn tốt.", 13),
    ],
    vocabulary: [
      vocab("朋友", "péngyou", "bạn bè"),
      vocab("名字", "míngzi", "tên"),
      vocab("好", "hǎo", "tốt"),
      vocab("叫", "jiào", "gọi là"),
    ],
  },
  {
    slug: "mua-do",
    label: "东西",
    chineseTitle: "买东西",
    vietnameseTitle: "Đi mua đồ",
    durationSeconds: 65,
    dialogue: [
      line("s01", "你要买什么？", "Nǐ yào mǎi shénme?", "Bạn muốn mua gì?", 0),
      line("s02", "我要买一本书。", "Wǒ yào mǎi yì běn shū.", "Mình muốn mua một quyển sách.", 4),
      line("s03", "这本书多少钱？", "Zhè běn shū duōshao qián?", "Quyển sách này bao nhiêu tiền?", 9),
      line("s04", "二十块钱。", "Èrshí kuài qián.", "Hai mươi tệ.", 13),
    ],
    vocabulary: [
      vocab("买", "mǎi", "mua"),
      vocab("书", "shū", "sách"),
      vocab("钱", "qián", "tiền"),
      vocab("多少", "duōshao", "bao nhiêu"),
    ],
  },
  {
    slug: "dat-mon",
    label: "点餐",
    chineseTitle: "在餐厅",
    vietnameseTitle: "Gọi món trong nhà hàng",
    durationSeconds: 80,
    dialogue: [
      line("s01", "欢迎光临，请问几位？", "Huānyíng guānglín, qǐngwèn jǐ wèi?", "Chào mừng quý khách, xin hỏi mấy người ạ?", 0),
      line("s02", "两位，谢谢。", "Liǎng wèi, xièxie.", "Hai người, cảm ơn.", 4),
      line("s03", "你们想吃点什么？", "Nǐmen xiǎng chī diǎn shénme?", "Các bạn muốn ăn gì?", 9),
      line("s04", "我要一碗米饭。", "Wǒ yào yì wǎn mǐfàn.", "Mình muốn một bát cơm.", 14),
    ],
    vocabulary: [
      vocab("吃", "chī", "ăn"),
      vocab("米饭", "mǐfàn", "cơm"),
      vocab("位", "wèi", "vị (lượng từ chỉ người)"),
      vocab("想", "xiǎng", "muốn"),
    ],
  },
  {
    slug: "hoi-duong",
    label: "路线",
    chineseTitle: "问路",
    vietnameseTitle: "Hỏi đường",
    durationSeconds: 48,
    dialogue: [
      line("s01", "请问，火车站怎么走？", "Qǐngwèn, huǒchēzhàn zěnme zǒu?", "Xin hỏi, ga tàu đi thế nào?", 0),
      line("s02", "一直走，然后右转。", "Yìzhí zǒu, ránhòu yòu zhuǎn.", "Đi thẳng, sau đó rẽ phải.", 4),
      line("s03", "远不远？", "Yuǎn bu yuǎn?", "Có xa không?", 9),
      line("s04", "不远，五分钟。", "Bù yuǎn, wǔ fēnzhōng.", "Không xa, năm phút.", 12),
    ],
    vocabulary: [
      vocab("走", "zǒu", "đi"),
      vocab("右", "yòu", "phải"),
      vocab("远", "yuǎn", "xa"),
      vocab("分钟", "fēnzhōng", "phút"),
    ],
  },
  {
    slug: "sieu-thi",
    label: "超市",
    chineseTitle: "在超市",
    vietnameseTitle: "Ở siêu thị",
    durationSeconds: 76,
    dialogue: [
      line("s01", "这里有牛奶吗？", "Zhèlǐ yǒu niúnǎi ma?", "Ở đây có sữa không?", 0),
      line("s02", "有，在那边。", "Yǒu, zài nàbiān.", "Có, ở đằng kia.", 4),
      line("s03", "谢谢你。", "Xièxie nǐ.", "Cảm ơn bạn.", 8),
      line("s04", "不客气。", "Bú kèqi.", "Không có gì.", 11),
    ],
    vocabulary: [
      vocab("牛奶", "niúnǎi", "sữa"),
      vocab("那边", "nàbiān", "đằng kia"),
      vocab("谢谢", "xièxie", "cảm ơn"),
      vocab("有", "yǒu", "có"),
    ],
  },
  {
    slug: "gia-dinh",
    label: "家庭",
    chineseTitle: "我的家人",
    vietnameseTitle: "Gia đình của tôi",
    durationSeconds: 63,
    dialogue: [
      line("s01", "你家有几口人？", "Nǐ jiā yǒu jǐ kǒu rén?", "Nhà bạn có mấy người?", 0),
      line("s02", "我家有四口人。", "Wǒ jiā yǒu sì kǒu rén.", "Nhà mình có bốn người.", 4),
      line("s03", "你爸爸做什么工作？", "Nǐ bàba zuò shénme gōngzuò?", "Bố bạn làm nghề gì?", 9),
      line("s04", "他是老师。", "Tā shì lǎoshī.", "Bố mình là giáo viên.", 13),
    ],
    vocabulary: [
      vocab("家", "jiā", "nhà, gia đình"),
      vocab("爸爸", "bàba", "bố"),
      vocab("老师", "lǎoshī", "giáo viên"),
      vocab("口", "kǒu", "lượng từ chỉ người trong nhà"),
    ],
  },
  {
    slug: "cong-viec",
    label: "工作",
    chineseTitle: "工作和职业",
    vietnameseTitle: "Công việc và nghề nghiệp",
    durationSeconds: 87,
    dialogue: [
      line("s01", "你做什么工作？", "Nǐ zuò shénme gōngzuò?", "Bạn làm công việc gì?", 0),
      line("s02", "我是医生。", "Wǒ shì yīshēng.", "Mình là bác sĩ.", 4),
      line("s03", "你喜欢你的工作吗？", "Nǐ xǐhuan nǐ de gōngzuò ma?", "Bạn có thích công việc của mình không?", 9),
      line("s04", "我很喜欢。", "Wǒ hěn xǐhuan.", "Mình rất thích.", 14),
    ],
    vocabulary: [
      vocab("工作", "gōngzuò", "công việc"),
      vocab("医生", "yīshēng", "bác sĩ"),
      vocab("喜欢", "xǐhuan", "thích"),
      vocab("做", "zuò", "làm"),
    ],
  },
];

function buildLessons(id: ListeningLevelId, hskLevel: HskLevel, count: number): ListeningLesson[] {
  return Array.from({ length: count }, (_, index) => {
    const code = String(index + 1).padStart(3, "0");
    const template = LESSON_TEMPLATES[index % LESSON_TEMPLATES.length]!;
    return {
      id: `${code}-${template.slug}`,
      level: id,
      hskLevel,
      code,
      label: template.label,
      chineseTitle: template.chineseTitle,
      vietnameseTitle: template.vietnameseTitle,
      durationSeconds: template.durationSeconds,
      dialogue: template.dialogue,
      vocabulary: template.vocabulary,
      // No real video/thumbnail exists for any mock lesson — every
      // consumer falls back to its placeholder rendering.
      videoUrl: null,
      thumbnailUrl: null,
    };
  });
}

const LESSONS_BY_LEVEL: Record<ListeningLevelId, ListeningLesson[]> = {
  hsk1: buildLessons("hsk1", 1, 30),
  hsk2: buildLessons("hsk2", 2, 108),
  hsk3: buildLessons("hsk3", 3, 16),
};

export function getListeningLessons(level: ListeningLevelId): ListeningLesson[] {
  return LESSONS_BY_LEVEL[level] ?? [];
}

export function getListeningLesson(level: ListeningLevelId, id: string): ListeningLesson | null {
  return LESSONS_BY_LEVEL[level]?.find((lesson) => lesson.id === id) ?? null;
}

/** Previous/next within the same level's lesson list, in catalog order —
 *  wraps neither direction (null at the first/last lesson). */
export function getAdjacentLessons(
  level: ListeningLevelId,
  id: string
): { previous: ListeningLesson | null; next: ListeningLesson | null } {
  const lessons = LESSONS_BY_LEVEL[level] ?? [];
  const index = lessons.findIndex((lesson) => lesson.id === id);
  if (index === -1) return { previous: null, next: null };
  return {
    previous: index > 0 ? lessons[index - 1] ?? null : null,
    next: index < lessons.length - 1 ? lessons[index + 1] ?? null : null,
  };
}
