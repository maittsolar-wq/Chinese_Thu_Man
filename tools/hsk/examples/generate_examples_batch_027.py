"""P5.10.3 (continued) -- Batch 027 (continues immediately after
examples_batch_026.json; entirely within HSK6, hsk6_0894-hsk6_1196).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Numeric-suffix homograph records (needs_review) ***
One record in this batch carries the HSK6 numeric-suffix homograph
pattern (see batch 024's 乘2, batch 025's 副2/该2, and batch 026's
局1/局2/料1/料2/露1 for the full explanation): 升2 (hsk6_1169). The
literal string "升2" can never appear in natural Chinese text, so it
is left with an empty examples list and qaStatus "needs_review", per
the established rule. Production record untouched. Three further such
records remain later in HSK6 (所2, 则1, 支2) and will need identical
treatment when reached.

*** Continuing extremely dense homophone/polyphonic clusters ***
This batch is unusually dense even by this pipeline's standards.
None of the pairs below are flagged by the mechanical tier system (it
compares the `word` string, and every pair is a different word), but
all required deliberate disambiguation:
  - miǎn (3rd tone): 免/勉强/免税/免疫/难免 -- five members, same
    tone, three different characters (免/勉/难 is nán not miǎn --
    难免 uses 难(nán)+免(miǎn) as a compound).
  - mó/mú polyphonic 模: 模仿/模拟/模特儿/模型 all read mó ("to
    imitate/a model"), but 模样 reads MÚ ("appearance/shape") --
    genuinely different tone for the same character. Kept distinct.
  - qǐ (3rd tone): 起初/起点/启动/启发/启示/启事/起源 -- seven
    members. 启示 and 启事 are BOTH qǐshì (identical pinyin+tone,
    different characters: 启示 "revelation/insight" vs 启事 "notice/
    announcement") -- given deliberately distinct natural contexts
    (一个深刻的启示 vs 一则寻人启事).
  - qiáng/qiǎng polyphonic 强: 强化/强壮 read qiáng (2nd tone,
    "strong/to strengthen") while 强迫 reads QIǍNG (3rd tone, "to
    force/compel") -- genuinely different tone for the same
    character. Kept distinct.
  - qīng/qíng (1st/2nd tone) mega-cluster: 清/清晨/清淡/清洁/清理/
    清扫/倾听/清洗/清晰/倾向/清醒 (qīng, eleven members) plus 青春/
    青春期 (qīng, two more) and 情节/晴朗/情形 (qíng, three members)
    -- fourteen total in one batch. All given distinct natural
    compounds/contexts.
  - qiú (2nd tone): 求/求婚/求救/求职/求助 -- five members, all the
    same character 求 in different compounds.
  - qǔ (3rd tone): 曲(qǔ, "melody/tune")/娶(qǔ, "to marry a wife")/
    取(qǔ, in 取代) -- three different characters, identical
    pinyin+tone. Kept distinct.
  - rén (2nd tone): 人工智能/人家/人均/人山人海/人行道 -- five
    members, plus 人士 and 人事, which are BOTH rénshì (identical
    pinyin+tone, different characters: 人士 "person of standing" vs
    人事 "personnel/human-resources affairs") -- given deliberately
    distinct natural contexts.
  - rèn (4th tone): 认错/认定/认可/认同/认知 -- five members, same
    character 认 in different compounds.
  - shè (4th tone): 社/射/涉及/射击/摄像/设想/摄像头 -- seven
    members, five different characters (社/射/涉/摄/设) sharing the
    same pinyin+tone.
  - shí (2nd tone): the largest cluster in this batch -- 识/拾/时光/
    实话/实惠/时机/时尚/实时/时速/石油/食欲/实质/十足/识别 --
    fourteen members across SEVEN different characters (识/拾/时/实/
    石/食/十). Each kept to its own natural, unambiguous compound.
  - pō (1st tone): 坡/泼 -- two different characters, identical
    pinyin+tone. Kept distinct (坡 "slope" vs 泼 "to splash/spill").
  - pū (1st tone): 扑/铺 -- two different characters, identical
    pinyin+tone. Kept distinct (扑 "to pounce/rush at" vs 铺 "to
    spread out/lay").
  - piāo (1st tone) polyphonic pair: 飘 ("to float/flutter in air")
    and 漂 ("to float/drift on water") share the SAME pinyin AND tone
    here (production data gives 漂 as piāo, not the more familiar
    piào of 漂亮) -- two different characters, deliberately given
    air-vs-water contexts to keep them distinct.
  - shàng (4th tone): 上当/上级/上进/上市/上述/上台/上旬 -- seven
    members, same character 上 in different compounds.
  - shān/shǎn: 山顶/山峰/山坡 (shān, 1st tone) vs 闪/闪电 (shǎn, 3rd
    tone) -- distinct tones, distinct characters.

Fix applied after the first validator pass (caught by
validate_examples_batch_p103.py's no_duplicate_sentences_across_
pilot_and_batches check): 扫描 (sǎomiáo)'s first draft "请扫描这个
二维码。" was an EXACT duplicate of an already-published sentence in
batch 022. Rewritten to "机场安检会扫描每一件行李。".

Near-template fixes (character-bigram Jaccard >= 0.55 against the
full pilot+002-026 corpus, caught by the independent script-level
check, not the validator): four flags, all fixed by diverging
sentence structure while preserving natural, correct usage:
  - 入境 vs hsk6_0187's "请出示护照办理出境手续。" (both used the
    "请出示护照办理...手续。" template) -> "外国游客需要办理入境
    手续。".
  - 弱点 vs hsk4_725's "每个人都有自己的特点。" (both used the "每个
    人都有自己的...。" template) -> "认清自己的弱点才能不断进步。".
  - 墙壁 vs hsk4_207's "墙上挂着一幅画。" (near-identical clause on
    the near-synonym 墙/墙壁) -> "工人正在粉刷墙壁。".
  - 深夜 vs hsk3_474's "他工作到很晚，直到深夜才回家。" (my first
    draft reused essentially the same clause) -> "深夜的街道格外
    安静。".
Re-verified after these fixes: zero cross-corpus flags, zero
within-batch flags (see validation report).

All re-verified against the full pilot+002-026 corpus with zero
remaining exact duplicates and zero near-template flags (see
validation report).

Usage:
    python generate_examples_batch_027.py --dry-run
    python generate_examples_batch_027.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 27
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_027.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# Records deliberately left with 0 examples (see module docstring):
# HSK6's numeric-suffix homograph pattern makes the literal target
# word unmatchable in natural Chinese text.
NEEDS_REVIEW_IDS = {"hsk6_1169"}

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk6_0894": [{"chinese": "他喜欢冒险的运动。", "pinyin": "Tā xǐhuan màoxiǎn de yùndòng.", "meaningVi": "Anh ấy thích các môn thể thao mạo hiểm."}],
    "hsk6_0895": [{"chinese": "两国之间的贸易日益频繁。", "pinyin": "Liǎng guó zhījiān de màoyì rìyì pínfán.", "meaningVi": "Thương mại giữa hai nước ngày càng thường xuyên."}],
    "hsk6_0896": [{"chinese": "这个地区盛产煤。", "pinyin": "Zhège dìqū shèngchǎn méi.", "meaningVi": "Khu vực này sản xuất nhiều than đá."}],
    "hsk6_0897": [{"chinese": "冬天梅花在雪中绽放。", "pinyin": "Dōngtiān méihuā zài xuě zhōng zhànfàng.", "meaningVi": "Mùa đông hoa mai nở trong tuyết."}],
    "hsk6_0898": [{"chinese": "她的眉毛又细又长。", "pinyin": "Tā de méimao yòu xì yòu cháng.", "meaningVi": "Lông mày của cô ấy vừa mảnh vừa dài."}],
    "hsk6_0899": [{"chinese": "这座建筑设计得十分美观。", "pinyin": "Zhè zuò jiànzhù shèjì de shífēn měiguān.", "meaningVi": "Công trình này được thiết kế vô cùng đẹp mắt."}],
    "hsk6_0900": [{"chinese": "他努力弥补自己的过失。", "pinyin": "Tā nǔlì míbǔ zìjǐ de guòshī.", "meaningVi": "Anh ấy cố gắng bù đắp lỗi lầm của mình."}],
    "hsk6_0901": [{"chinese": "这里的风景十分迷人。", "pinyin": "Zhèlǐ de fēngjǐng shífēn mírén.", "meaningVi": "Phong cảnh nơi đây vô cùng quyến rũ."}],
    "hsk6_0902": [{"chinese": "树林长得很密。", "pinyin": "Shùlín zhǎng de hěn mì.", "meaningVi": "Rừng cây mọc rất rậm rạp."}],
    "hsk6_0903": [{"chinese": "这个城市的人口密度很高。", "pinyin": "Zhège chéngshì de rénkǒu mìdù hěn gāo.", "meaningVi": "Mật độ dân số của thành phố này rất cao."}],
    "hsk6_0904": [{"chinese": "蜜蜂在花丛中飞来飞去。", "pinyin": "Mìfēng zài huācóng zhōng fēilái-fēiqù.", "meaningVi": "Ong mật bay qua bay lại trong bụi hoa."}],
    "hsk6_0905": [{"chinese": "这一带工厂十分密集。", "pinyin": "Zhè yídài gōngchǎng shífēn mìjí.", "meaningVi": "Khu vực này nhà máy dày đặc."}],
    "hsk6_0906": [{"chinese": "这件衣服是纯棉做的。", "pinyin": "Zhè jiàn yīfu shì chún mián zuò de.", "meaningVi": "Chiếc áo này được làm từ vải cotton nguyên chất."}],
    "hsk6_0907": [{"chinese": "会员可以免运费。", "pinyin": "Huìyuán kěyǐ miǎn yùnfèi.", "meaningVi": "Hội viên có thể được miễn phí vận chuyển."}],
    "hsk6_0908": [{"chinese": "他勉强答应了这个请求。", "pinyin": "Tā miǎnqiǎng dāyingle zhège qǐngqiú.", "meaningVi": "Anh ấy miễn cưỡng đồng ý yêu cầu này."}],
    "hsk6_0909": [{"chinese": "这里是免税购物区。", "pinyin": "Zhèlǐ shì miǎnshuì gòuwù qū.", "meaningVi": "Đây là khu mua sắm miễn thuế."}],
    "hsk6_0910": [{"chinese": "疫苗可以增强人体免疫力。", "pinyin": "Yìmiáo kěyǐ zēngqiáng réntǐ miǎnyìlì.", "meaningVi": "Vắc-xin có thể tăng cường khả năng miễn dịch của cơ thể."}],
    "hsk6_0911": [{"chinese": "医生检查了他的面部表情。", "pinyin": "Yīshēng jiǎnchále tā de miànbù biǎoqíng.", "meaningVi": "Bác sĩ đã kiểm tra biểu cảm trên mặt anh ấy."}],
    "hsk6_0912": [{"chinese": "她用面粉做了一个蛋糕。", "pinyin": "Tā yòng miànfěn zuòle yí gè dàngāo.", "meaningVi": "Cô ấy đã dùng bột mì làm một chiếc bánh."}],
    "hsk6_0913": [{"chinese": "他很爱面子。", "pinyin": "Tā hěn ài miànzi.", "meaningVi": "Anh ấy rất coi trọng thể diện."}],
    "hsk6_0914": [{"chinese": "作家生动地描绘了这座城市。", "pinyin": "Zuòjiā shēngdòng de miáohuìle zhè zuò chéngshì.", "meaningVi": "Nhà văn đã miêu tả sinh động thành phố này."}],
    "hsk6_0915": [{"chinese": "这段文字描写了主人公的心理活动。", "pinyin": "Zhè duàn wénzì miáoxiěle zhǔréngōng de xīnlǐ huódòng.", "meaningVi": "Đoạn văn này miêu tả hoạt động tâm lý của nhân vật chính."}],
    "hsk6_0916": [{"chinese": "这个主意真妙。", "pinyin": "Zhège zhǔyi zhēn miào.", "meaningVi": "Ý tưởng này thật tuyệt vời."}],
    "hsk6_0917": [{"chinese": "火已经灭了。", "pinyin": "Huǒ yǐjīng miè le.", "meaningVi": "Lửa đã tắt rồi."}],
    "hsk6_0918": [{"chinese": "这首民歌流传了几百年。", "pinyin": "Zhè shǒu míngē liúchuánle jǐ bǎi nián.", "meaningVi": "Bài dân ca này đã lưu truyền mấy trăm năm."}],
    "hsk6_0919": [{"chinese": "这是一个民间传说。", "pinyin": "Zhè shì yí gè mínjiān chuánshuō.", "meaningVi": "Đây là một truyền thuyết dân gian."}],
    "hsk6_0920": [{"chinese": "这个地方保留着独特的民俗。", "pinyin": "Zhège dìfang bǎoliúzhe dútè de mínsú.", "meaningVi": "Nơi này vẫn giữ được phong tục dân gian độc đáo."}],
    "hsk6_0921": [{"chinese": "我们预订了一家民宿。", "pinyin": "Wǒmen yùdìngle yì jiā mínsù.", "meaningVi": "Chúng tôi đã đặt một homestay."}],
    "hsk6_0922": [{"chinese": "政府呼吁民众节约用水。", "pinyin": "Zhèngfǔ hūyù mínzhòng jiéyuē yòngshuǐ.", "meaningVi": "Chính phủ kêu gọi người dân tiết kiệm nước."}],
    "hsk6_0923": [{"chinese": "这是一个民主国家。", "pinyin": "Zhè shì yí gè mínzhǔ guójiā.", "meaningVi": "Đây là một quốc gia dân chủ."}],
    "hsk6_0924": [{"chinese": "这次招聘的名额有限。", "pinyin": "Zhè cì zhāopìn de míng'é yǒuxiàn.", "meaningVi": "Chỉ tiêu tuyển dụng lần này có hạn."}],
    "hsk6_0925": [{"chinese": "教室里灯光明亮。", "pinyin": "Jiàoshì lǐ dēngguāng míngliàng.", "meaningVi": "Trong lớp học ánh đèn sáng sủa."}],
    "hsk6_0926": [{"chinese": "他明明知道答案，却不说。", "pinyin": "Tā míngmíng zhīdào dá'àn, què bù shuō.", "meaningVi": "Rõ ràng anh ấy biết đáp án, nhưng lại không nói."}],
    "hsk6_0927": [{"chinese": "这家餐厅很有名气。", "pinyin": "Zhè jiā cāntīng hěn yǒu míngqi.", "meaningVi": "Nhà hàng này rất có danh tiếng."}],
    "hsk6_0928": [{"chinese": "这里有许多名胜古迹。", "pinyin": "Zhèlǐ yǒu xǔduō míngshèng gǔjì.", "meaningVi": "Nơi đây có nhiều danh lam thắng cảnh."}],
    "hsk6_0929": [{"chinese": "将军下达了命令。", "pinyin": "Jiāngjūn xiàdále mìnglìng.", "meaningVi": "Tướng quân đã ban hành mệnh lệnh."}],
    "hsk6_0930": [{"chinese": "这座桥以他的名字命名。", "pinyin": "Zhè zuò qiáo yǐ tā de míngzi mìngmíng.", "meaningVi": "Cây cầu này được đặt tên theo tên của ông ấy."}],
    "hsk6_0931": [{"chinese": "孩子喜欢模仿大人的动作。", "pinyin": "Háizi xǐhuan mófǎng dàren de dòngzuò.", "meaningVi": "Trẻ em thích bắt chước hành động của người lớn."}],
    "hsk6_0932": [{"chinese": "这是一次模拟考试。", "pinyin": "Zhè shì yí cì mónǐ kǎoshì.", "meaningVi": "Đây là một kỳ thi mô phỏng."}],
    "hsk6_0933": [{"chinese": "她是一名时装模特儿。", "pinyin": "Tā shì yì míng shízhuāng mótèr.", "meaningVi": "Cô ấy là một người mẫu thời trang."}],
    "hsk6_0934": [{"chinese": "他骑摩托车上班。", "pinyin": "Tā qí mótuōchē shàngbān.", "meaningVi": "Anh ấy đi làm bằng xe máy."}],
    "hsk6_0935": [{"chinese": "他做了一个飞机模型。", "pinyin": "Tā zuòle yí gè fēijī móxíng.", "meaningVi": "Anh ấy đã làm một mô hình máy bay."}],
    "hsk6_0936": [{"chinese": "她默默地流下了眼泪。", "pinyin": "Tā mòmò de liúxiàle yǎnlèi.", "meaningVi": "Cô ấy lặng lẽ rơi nước mắt."}],
    "hsk6_0937": [{"chinese": "他现在的模样和以前完全不同。", "pinyin": "Tā xiànzài de múyàng hé yǐqián wánquán bùtóng.", "meaningVi": "Dáng vẻ hiện tại của anh ấy hoàn toàn khác trước."}],
    "hsk6_0938": [{"chinese": "这是一只母鸡。", "pinyin": "Zhè shì yì zhī mǔjī.", "meaningVi": "Đây là một con gà mái."}],
    "hsk6_0939": [{"chinese": "汉语是他的母语。", "pinyin": "Hànyǔ shì tā de mǔyǔ.", "meaningVi": "Tiếng Trung là tiếng mẹ đẻ của anh ấy."}],
    "hsk6_0940": [{"chinese": "这座房子是用木材建造的。", "pinyin": "Zhè zuò fángzi shì yòng mùcái jiànzào de.", "meaningVi": "Ngôi nhà này được xây bằng gỗ."}],
    "hsk6_0941": [{"chinese": "请查看书的目录。", "pinyin": "Qǐng chákàn shū de mùlù.", "meaningVi": "Xin xem mục lục của cuốn sách."}],
    "hsk6_0942": [{"chinese": "这是婴儿专用奶粉。", "pinyin": "Zhè shì yīng'ér zhuānyòng nǎifěn.", "meaningVi": "Đây là sữa bột dành riêng cho trẻ sơ sinh."}],
    "hsk6_0943": [{"chinese": "这道题的难点在于计算。", "pinyin": "Zhè dào tí de nándiǎn zàiyú jìsuàn.", "meaningVi": "Điểm khó của bài toán này nằm ở việc tính toán."}],
    "hsk6_0944": [{"chinese": "南极洲常年被冰雪覆盖。", "pinyin": "Nánjízhōu chángnián bèi bīngxuě fùgài.", "meaningVi": "Châu Nam Cực quanh năm được băng tuyết bao phủ."}],
    "hsk6_0945": [{"chinese": "巴西位于南美洲。", "pinyin": "Bāxī wèiyú Nánměizhōu.", "meaningVi": "Brazil nằm ở Nam Mỹ."}],
    "hsk6_0946": [{"chinese": "刚开始学难免会犯错误。", "pinyin": "Gāng kāishǐ xué nánmiǎn huì fàn cuòwù.", "meaningVi": "Mới bắt đầu học khó tránh khỏi mắc lỗi."}],
    "hsk6_0947": [{"chinese": "他挠了挠脑袋。", "pinyin": "Tā náole náo nǎodai.", "meaningVi": "Anh ấy gãi gãi đầu."}],
    "hsk6_0948": [{"chinese": "他脑子转得很快。", "pinyin": "Tā nǎozi zhuàn de hěn kuài.", "meaningVi": "Đầu óc anh ấy suy nghĩ rất nhanh."}],
    "hsk6_0949": [{"chinese": "这幅画的内涵很丰富。", "pinyin": "Zhè fú huà de nèihán hěn fēngfù.", "meaningVi": "Nội hàm của bức tranh này rất phong phú."}],
    "hsk6_0950": [{"chinese": "他患的是内科疾病。", "pinyin": "Tā huàn de shì nèikē jíbìng.", "meaningVi": "Anh ấy mắc bệnh thuộc khoa nội."}],
    "hsk6_0951": [{"chinese": "房子内外都打扫得很干净。", "pinyin": "Fángzi nèiwài dōu dǎsǎo de hěn gānjìng.", "meaningVi": "Trong ngoài nhà đều được quét dọn sạch sẽ."}],
    "hsk6_0952": [{"chinese": "请选择合适的内衣尺码。", "pinyin": "Qǐng xuǎnzé héshì de nèiyī chǐmǎ.", "meaningVi": "Xin chọn size đồ lót phù hợp."}],
    "hsk6_0953": [{"chinese": "这种食物能提供大量能量。", "pinyin": "Zhè zhǒng shíwù néng tígōng dàliàng néngliàng.", "meaningVi": "Loại thực phẩm này có thể cung cấp nhiều năng lượng."}],
    "hsk6_0954": [{"chinese": "我们应该开发可再生能源。", "pinyin": "Wǒmen yīnggāi kāifā kě zàishēng néngyuán.", "meaningVi": "Chúng ta nên phát triển năng lượng tái tạo."}],
    "hsk6_0955": [{"chinese": "他的鞋上沾满了泥。", "pinyin": "Tā de xié shàng zhānmǎnle ní.", "meaningVi": "Giày của anh ấy dính đầy bùn."}],
    "hsk6_0956": [{"chinese": "这是本年度最佳影片。", "pinyin": "Zhè shì běn niándù zuìjiā yǐngpiàn.", "meaningVi": "Đây là bộ phim hay nhất trong năm."}],
    "hsk6_0957": [{"chinese": "公司在年终举行了聚餐。", "pinyin": "Gōngsī zài niánzhōng jǔxíngle jùcān.", "meaningVi": "Công ty đã tổ chức tiệc vào cuối năm."}],
    "hsk6_0958": [{"chinese": "他从小就喜欢念书。", "pinyin": "Tā cóngxiǎo jiù xǐhuan niànshū.", "meaningVi": "Anh ấy từ nhỏ đã thích đọc sách."}],
    "hsk6_0959": [{"chinese": "他不小心扭伤了脚踝。", "pinyin": "Tā bù xiǎoxīn niǔshāngle jiǎohuái.", "meaningVi": "Anh ấy vô tình bị trẹo mắt cá chân."}],
    "hsk6_0960": [{"chinese": "这个市场专门卖农产品。", "pinyin": "Zhège shìchǎng zhuānmén mài nóngchǎnpǐn.", "meaningVi": "Chợ này chuyên bán nông sản."}],
    "hsk6_0961": [{"chinese": "他对音乐有浓厚的兴趣。", "pinyin": "Tā duì yīnyuè yǒu nónghòu de xìngqù.", "meaningVi": "Anh ấy có hứng thú sâu đậm với âm nhạc."}],
    "hsk6_0962": [{"chinese": "农民在农田里劳作。", "pinyin": "Nóngmín zài nóngtián lǐ láozuò.", "meaningVi": "Nông dân đang lao động trên đồng ruộng."}],
    "hsk6_0963": [{"chinese": "今天天气很暖。", "pinyin": "Jīntiān tiānqì hěn nuǎn.", "meaningVi": "Hôm nay thời tiết rất ấm."}],
    "hsk6_0964": [{"chinese": "冬天家里开着暖气。", "pinyin": "Dōngtiān jiālǐ kāizhe nuǎnqì.", "meaningVi": "Mùa đông trong nhà bật hệ thống sưởi."}],
    "hsk6_0965": [{"chinese": "他从小就把这位歌手当作偶像。", "pinyin": "Tā cóngxiǎo jiù bǎ zhè wèi gēshǒu dàngzuò ǒuxiàng.", "meaningVi": "Anh ấy từ nhỏ đã coi ca sĩ này là thần tượng."}],
    "hsk6_0966": [{"chinese": "医生排除了严重疾病的可能。", "pinyin": "Yīshēng páichúle yánzhòng jíbìng de kěnéng.", "meaningVi": "Bác sĩ đã loại trừ khả năng mắc bệnh nghiêm trọng."}],
    "hsk6_0967": [{"chinese": "工厂减少了污水排放。", "pinyin": "Gōngchǎng jiǎnshǎole wūshuǐ páifàng.", "meaningVi": "Nhà máy đã giảm lượng xả nước thải."}],
    "hsk6_0968": [{"chinese": "演员们正在排练新剧。", "pinyin": "Yǎnyuánmen zhèngzài páiliàn xīn jù.", "meaningVi": "Các diễn viên đang tập luyện vở kịch mới."}],
    "hsk6_0969": [{"chinese": "他在班里的排名靠前。", "pinyin": "Tā zài bān lǐ de páimíng kàoqián.", "meaningVi": "Thứ hạng của anh ấy trong lớp khá cao."}],
    "hsk6_0970": [{"chinese": "桌上放着一个盘子。", "pinyin": "Zhuō shàng fàngzhe yí gè pánzi.", "meaningVi": "Trên bàn để một cái đĩa."}],
    "hsk6_0971": [{"chinese": "孩子们盼望着假期的到来。", "pinyin": "Háizimen pànwàngzhe jiàqī de dàolái.", "meaningVi": "Bọn trẻ mong chờ kỳ nghỉ đến."}],
    "hsk6_0972": [{"chinese": "这是一个庞大的工程。", "pinyin": "Zhè shì yí gè pángdà de gōngchéng.", "meaningVi": "Đây là một công trình khổng lồ."}],
    "hsk6_0973": [{"chinese": "他把球抛向空中。", "pinyin": "Tā bǎ qiú pāo xiàng kōngzhōng.", "meaningVi": "Anh ấy ném quả bóng lên không trung."}],
    "hsk6_0974": [{"chinese": "他的脚上起了一个水泡。", "pinyin": "Tā de jiǎo shàng qǐle yí gè shuǐpào.", "meaningVi": "Chân anh ấy nổi một mụn nước."}],
    "hsk6_0975": [{"chinese": "公司同意赔偿他的损失。", "pinyin": "Gōngsī tóngyì péicháng tā de sǔnshī.", "meaningVi": "Công ty đồng ý bồi thường thiệt hại cho anh ấy."}],
    "hsk6_0976": [{"chinese": "导游全程陪同游客。", "pinyin": "Dǎoyóu quánchéng péitóng yóukè.", "meaningVi": "Hướng dẫn viên đi cùng du khách suốt hành trình."}],
    "hsk6_0977": [{"chinese": "农场培育出了新品种。", "pinyin": "Nóngchǎng péiyùchūle xīn pǐnzhǒng.", "meaningVi": "Nông trại đã nuôi dưỡng thành công giống mới."}],
    "hsk6_0978": [{"chinese": "每间教室都配备了投影仪。", "pinyin": "Měi jiān jiàoshì dōu pèibèile tóuyǐngyí.", "meaningVi": "Mỗi phòng học đều được trang bị máy chiếu."}],
    "hsk6_0979": [{"chinese": "大家都很佩服他的勇气。", "pinyin": "Dàjiā dōu hěn pèifú tā de yǒngqì.", "meaningVi": "Mọi người đều rất khâm phục lòng dũng cảm của anh ấy."}],
    "hsk6_0980": [{"chinese": "小区配套设施十分齐全。", "pinyin": "Xiǎoqū pèitào shèshī shífēn qíquán.", "meaningVi": "Cơ sở hạ tầng đồng bộ của khu dân cư rất đầy đủ."}],
    "hsk6_0981": [{"chinese": "她往花上喷了些水。", "pinyin": "Tā wǎng huā shàng pēnle xiē shuǐ.", "meaningVi": "Cô ấy phun một ít nước lên hoa."}],
    "hsk6_0982": [{"chinese": "她双手捧着一束花。", "pinyin": "Tā shuāngshǒu pěngzhe yí shù huā.", "meaningVi": "Cô ấy hai tay bưng một bó hoa."}],
    "hsk6_0983": [{"chinese": "两辆车发生了碰撞。", "pinyin": "Liǎng liàng chē fāshēngle pèngzhuàng.", "meaningVi": "Hai chiếc xe đã va chạm với nhau."}],
    "hsk6_0984": [{"chinese": "她披着一件外套。", "pinyin": "Tā pīzhe yí jiàn wàitào.", "meaningVi": "Cô ấy khoác một chiếc áo khoác."}],
    "hsk6_0985": [{"chinese": "苹果皮不要扔掉。", "pinyin": "Píngguǒ pí búyào rēngdiào.", "meaningVi": "Vỏ táo đừng vứt đi."}],
    "hsk6_0986": [{"chinese": "长时间开车容易疲劳。", "pinyin": "Cháng shíjiān kāichē róngyì píláo.", "meaningVi": "Lái xe thời gian dài dễ bị mệt mỏi."}],
    "hsk6_0987": [{"chinese": "请稍等片刻。", "pinyin": "Qǐng shāo děng piànkè.", "meaningVi": "Xin vui lòng chờ một lát."}],
    "hsk6_0988": [{"chinese": "他的看法有些片面。", "pinyin": "Tā de kànfǎ yǒuxiē piànmiàn.", "meaningVi": "Quan điểm của anh ấy có phần phiến diện."}],
    "hsk6_0989": [{"chinese": "千万不要相信骗子的话。", "pinyin": "Qiānwàn búyào xiāngxìn piànzi de huà.", "meaningVi": "Ngàn vạn lần đừng tin lời của kẻ lừa đảo."}],
    "hsk6_0990": [{"chinese": "树叶随风飘落。", "pinyin": "Shùyè suí fēng piāoluò.", "meaningVi": "Lá cây theo gió bay rơi."}],
    "hsk6_0991": [{"chinese": "一片树叶在水面上漂着。", "pinyin": "Yí piàn shùyè zài shuǐmiàn shàng piāozhe.", "meaningVi": "Một chiếc lá cây trôi nổi trên mặt nước."}],
    "hsk6_0992": [{"chinese": "请换到体育频道。", "pinyin": "Qǐng huàndào tǐyù píndào.", "meaningVi": "Xin chuyển sang kênh thể thao."}],
    "hsk6_0993": [{"chinese": "最近他出差十分频繁。", "pinyin": "Zuìjìn tā chūchāi shífēn pínfán.", "meaningVi": "Gần đây anh ấy đi công tác rất thường xuyên."}],
    "hsk6_0994": [{"chinese": "政府大力帮助贫困地区。", "pinyin": "Zhèngfǔ dàlì bāngzhù pínkùn dìqū.", "meaningVi": "Chính phủ tích cực giúp đỡ các khu vực nghèo khó."}],
    "hsk6_0995": [{"chinese": "他锻炼的频率提高了。", "pinyin": "Tā duànliàn de pínlǜ tígāo le.", "meaningVi": "Tần suất tập luyện của anh ấy đã tăng lên."}],
    "hsk6_0996": [{"chinese": "游客可以品尝当地美食。", "pinyin": "Yóukè kěyǐ pǐncháng dāngdì měishí.", "meaningVi": "Du khách có thể thưởng thức món ăn địa phương."}],
    "hsk6_0997": [{"chinese": "法律面前人人平等。", "pinyin": "Fǎlǜ miànqián rénrén píngděng.", "meaningVi": "Trước pháp luật mọi người đều bình đẳng."}],
    "hsk6_0998": [{"chinese": "他过着平凡而幸福的生活。", "pinyin": "Tā guòzhe píngfán ér xìngfú de shēnghuó.", "meaningVi": "Anh ấy sống một cuộc sống bình thường mà hạnh phúc."}],
    "hsk6_0999": [{"chinese": "五的平方是二十五。", "pinyin": "Wǔ de píngfāng shì èrshíwǔ.", "meaningVi": "Bình phương của năm là hai mươi lăm."}],
    "hsk6_1000": [{"chinese": "这套房子有一百平方米。", "pinyin": "Zhè tào fángzi yǒu yìbǎi píngfāngmǐ.", "meaningVi": "Căn nhà này có một trăm mét vuông."}],
    "hsk6_1001": [{"chinese": "专家对项目进行了评估。", "pinyin": "Zhuānjiā duì xiàngmù jìnxíngle pínggū.", "meaningVi": "Chuyên gia đã tiến hành đánh giá dự án."}],
    "hsk6_1002": [{"chinese": "网友们对这条新闻发表了评论。", "pinyin": "Wǎngyǒumen duì zhè tiáo xīnwén fābiǎole pínglùn.", "meaningVi": "Cư dân mạng đã bình luận về tin tức này."}],
    "hsk6_1003": [{"chinese": "他被评选为年度最佳员工。", "pinyin": "Tā bèi píngxuǎn wéi niándù zuìjiā yuángōng.", "meaningVi": "Anh ấy được bình chọn là nhân viên xuất sắc nhất năm."}],
    "hsk6_1004": [{"chinese": "这条路是一段上坡。", "pinyin": "Zhè tiáo lù shì yí duàn shàngpō.", "meaningVi": "Con đường này là một đoạn dốc lên."}],
    "hsk6_1005": [{"chinese": "别把水泼到地上。", "pinyin": "Bié bǎ shuǐ pō dào dìshang.", "meaningVi": "Đừng làm đổ nước xuống đất."}],
    "hsk6_1006": [{"chinese": "这家公司最终破产了。", "pinyin": "Zhè jiā gōngsī zhōngyú pòchǎn le.", "meaningVi": "Công ty này cuối cùng đã phá sản."}],
    "hsk6_1007": [{"chinese": "他有迫切的求学愿望。", "pinyin": "Tā yǒu pòqiè de qiúxué yuànwàng.", "meaningVi": "Anh ấy có nguyện vọng cấp bách muốn đi học."}],
    "hsk6_1008": [{"chinese": "小猫扑向了那只蝴蝶。", "pinyin": "Xiǎomāo pū xiàngle nà zhī húdié.", "meaningVi": "Con mèo con lao về phía con bướm đó."}],
    "hsk6_1009": [{"chinese": "请把床单铺好。", "pinyin": "Qǐng bǎ chuángdān pū hǎo.", "meaningVi": "Xin trải chăn giường cho phẳng."}],
    "hsk6_1010": [{"chinese": "消防员迅速扑灭了大火。", "pinyin": "Xiāofángyuán xùnsù pūmièle dàhuǒ.", "meaningVi": "Lính cứu hỏa đã nhanh chóng dập tắt đám cháy lớn."}],
    "hsk6_1011": [{"chinese": "她穿着十分朴素。", "pinyin": "Tā chuānzhuó shífēn pǔsù.", "meaningVi": "Cách ăn mặc của cô ấy rất giản dị."}],
    "hsk6_1012": [{"chinese": "他欺骗了大家的信任。", "pinyin": "Tā qīpiànle dàjiā de xìnrèn.", "meaningVi": "Anh ấy đã lừa gạt niềm tin của mọi người."}],
    "hsk6_1013": [{"chinese": "父母对他寄予很大期望。", "pinyin": "Fùmǔ duì tā jìyǔ hěn dà qīwàng.", "meaningVi": "Cha mẹ đặt kỳ vọng rất lớn vào anh ấy."}],
    "hsk6_1014": [{"chinese": "请在期限内完成任务。", "pinyin": "Qǐng zài qīxiàn nèi wánchéng rènwu.", "meaningVi": "Xin hoàn thành nhiệm vụ trong thời hạn."}],
    "hsk6_1015": [{"chinese": "他在国外留学多年，其间很少回国。", "pinyin": "Tā zài guówài liúxué duō nián, qíjiān hěn shǎo huíguó.", "meaningVi": "Anh ấy du học nước ngoài nhiều năm, trong khoảng thời gian đó rất ít khi về nước."}],
    "hsk6_1016": [{"chinese": "这家超市商品十分齐全。", "pinyin": "Zhè jiā chāoshì shāngpǐn shífēn qíquán.", "meaningVi": "Siêu thị này hàng hóa vô cùng đầy đủ."}],
    "hsk6_1017": [{"chinese": "他小心地移动着棋子。", "pinyin": "Tā xiǎoxīn de yídòngzhe qízǐ.", "meaningVi": "Anh ấy cẩn thận di chuyển quân cờ."}],
    "hsk6_1018": [{"chinese": "起初大家都不相信这个消息。", "pinyin": "Qǐchū dàjiā dōu bù xiāngxìn zhège xiāoxi.", "meaningVi": "Ban đầu mọi người đều không tin tin tức này."}],
    "hsk6_1019": [{"chinese": "这里就是马拉松的起点。", "pinyin": "Zhèlǐ jiùshì mǎlāsōng de qǐdiǎn.", "meaningVi": "Đây chính là điểm khởi đầu của cuộc thi marathon."}],
    "hsk6_1020": [{"chinese": "他按下按钮启动了机器。", "pinyin": "Tā ànxià ànniǔ qǐdòngle jīqì.", "meaningVi": "Anh ấy nhấn nút để khởi động máy móc."}],
    "hsk6_1021": [{"chinese": "这本书给了他很大的启发。", "pinyin": "Zhè běn shū gěile tā hěn dà de qǐfā.", "meaningVi": "Cuốn sách này đã cho anh ấy sự gợi mở rất lớn."}],
    "hsk6_1022": [{"chinese": "这个故事给我们带来了深刻的启示。", "pinyin": "Zhège gùshi gěi wǒmen dàiláile shēnkè de qǐshì.", "meaningVi": "Câu chuyện này đã mang lại cho chúng ta bài học sâu sắc."}],
    "hsk6_1023": [{"chinese": "他在报纸上刊登了一则寻人启事。", "pinyin": "Tā zài bàozhǐ shàng kāndēngle yì zé xúnrén qǐshì.", "meaningVi": "Anh ấy đã đăng một thông báo tìm người trên báo."}],
    "hsk6_1024": [{"chinese": "这项传统起源于唐代。", "pinyin": "Zhè xiàng chuántǒng qǐyuán yú Tángdài.", "meaningVi": "Truyền thống này bắt nguồn từ thời nhà Đường."}],
    "hsk6_1025": [{"chinese": "派对现场气氛十分热烈。", "pinyin": "Pàiduì xiànchǎng qìfēn shífēn rèliè.", "meaningVi": "Không khí tại buổi tiệc vô cùng sôi động."}],
    "hsk6_1026": [{"chinese": "这种气体没有颜色。", "pinyin": "Zhè zhǒng qìtǐ méiyǒu yánsè.", "meaningVi": "Loại khí này không có màu."}],
    "hsk6_1027": [{"chinese": "厨房里飘出一股香甜的气味。", "pinyin": "Chúfáng lǐ piāochū yì gǔ xiāngtián de qìwèi.", "meaningVi": "Trong bếp tỏa ra một mùi thơm ngọt."}],
    "hsk6_1028": [{"chinese": "她举止优雅，很有气质。", "pinyin": "Tā jǔzhǐ yōuyǎ, hěn yǒu qìzhì.", "meaningVi": "Cử chỉ của cô ấy thanh lịch, rất có khí chất."}],
    "hsk6_1029": [{"chinese": "请用词恰当一些。", "pinyin": "Qǐng yòngcí qiàdàng yìxiē.", "meaningVi": "Xin dùng từ cho thích hợp hơn."}],
    "hsk6_1030": [{"chinese": "我出门时恰好遇见了他。", "pinyin": "Wǒ chūmén shí qiàhǎo yùjiànle tā.", "meaningVi": "Lúc tôi ra cửa thì vừa vặn gặp anh ấy."}],
    "hsk6_1031": [{"chinese": "事实恰恰相反。", "pinyin": "Shìshí qiàqià xiāngfǎn.", "meaningVi": "Sự thật lại chính xác ngược lại."}],
    "hsk6_1032": [{"chinese": "妈妈牵着孩子的手过马路。", "pinyin": "Māma qiānzhe háizi de shǒu guò mǎlù.", "meaningVi": "Mẹ dắt tay con qua đường."}],
    "hsk6_1033": [{"chinese": "春联给千家万户带来了喜庆的气氛。", "pinyin": "Chūnlián gěi qiānjiā-wànhù dàiláile xǐqìng de qìfēn.", "meaningVi": "Câu đối Tết mang lại không khí vui mừng cho muôn vàn gia đình."}],
    "hsk6_1034": [{"chinese": "他为人谦虚，从不炫耀。", "pinyin": "Tā wéirén qiānxū, cóng bú xuànyào.", "meaningVi": "Anh ấy là người khiêm tốn, không bao giờ khoe khoang."}],
    "hsk6_1035": [{"chinese": "这个行业的前景十分广阔。", "pinyin": "Zhège hángyè de qiánjǐng shífēn guǎngkuò.", "meaningVi": "Triển vọng của ngành này vô cùng rộng mở."}],
    "hsk6_1036": [{"chinese": "这个孩子很有潜力。", "pinyin": "Zhège háizi hěn yǒu qiánlì.", "meaningVi": "Đứa trẻ này rất có tiềm năng."}],
    "hsk6_1037": [{"chinese": "项目前期需要做大量调研。", "pinyin": "Xiàngmù qiánqī xūyào zuò dàliàng diàoyán.", "meaningVi": "Giai đoạn trước của dự án cần thực hiện nhiều khảo sát."}],
    "hsk6_1038": [{"chinese": "诚实是合作的前提。", "pinyin": "Chéngshí shì hézuò de qiántí.", "meaningVi": "Trung thực là tiền đề của hợp tác."}],
    "hsk6_1039": [{"chinese": "这两种方案中，我更倾向于前者。", "pinyin": "Zhè liǎng zhǒng fāng'àn zhōng, wǒ gèng qīngxiàng yú qiánzhě.", "meaningVi": "Trong hai phương án này, tôi thiên về phương án trước hơn."}],
    "hsk6_1040": [{"chinese": "警察配备了枪支。", "pinyin": "Jǐngchá pèibèile qiāngzhī.", "meaningVi": "Cảnh sát được trang bị súng."}],
    "hsk6_1041": [{"chinese": "工人正在粉刷墙壁。", "pinyin": "Gōngrén zhèngzài fěnshuā qiángbì.", "meaningVi": "Công nhân đang sơn quét tường."}],
    "hsk6_1042": [{"chinese": "学校强化了安全管理。", "pinyin": "Xuéxiào qiánghuàle ānquán guǎnlǐ.", "meaningVi": "Nhà trường đã tăng cường quản lý an toàn."}],
    "hsk6_1043": [{"chinese": "他身体十分强壮。", "pinyin": "Tā shēntǐ shífēn qiángzhuàng.", "meaningVi": "Cơ thể anh ấy vô cùng khỏe mạnh."}],
    "hsk6_1044": [{"chinese": "请不要强迫孩子学习。", "pinyin": "Qǐng búyào qiǎngpò háizi xuéxí.", "meaningVi": "Xin đừng ép buộc trẻ em học tập."}],
    "hsk6_1045": [{"chinese": "你瞧，那边有一只小鸟。", "pinyin": "Nǐ qiáo, nàbiān yǒu yì zhī xiǎoniǎo.", "meaningVi": "Nhìn kìa, đằng kia có một con chim nhỏ."}],
    "hsk6_1046": [{"chinese": "这座桥梁连接了两座城市。", "pinyin": "Zhè zuò qiáoliáng liánjiēle liǎng zuò chéngshì.", "meaningVi": "Cây cầu này kết nối hai thành phố."}],
    "hsk6_1047": [{"chinese": "他巧妙地解决了这个难题。", "pinyin": "Tā qiǎomiào de jiějuéle zhège nántí.", "meaningVi": "Anh ấy đã khéo léo giải quyết vấn đề khó này."}],
    "hsk6_1048": [{"chinese": "请拿出切实可行的方案。", "pinyin": "Qǐng náchū qièshí kěxíng de fāng'àn.", "meaningVi": "Xin đưa ra phương án thiết thực khả thi."}],
    "hsk6_1049": [{"chinese": "他们两个是十分亲密的朋友。", "pinyin": "Tāmen liǎng gè shì shífēn qīnmì de péngyou.", "meaningVi": "Hai người họ là những người bạn vô cùng thân thiết."}],
    "hsk6_1050": [{"chinese": "请填写你的紧急联系亲属。", "pinyin": "Qǐng tiánxiě nǐ de jǐnjí liánxì qīnshǔ.", "meaningVi": "Xin điền thông tin người thân liên hệ khẩn cấp."}],
    "hsk6_1051": [{"chinese": "他是一个勤劳的农民。", "pinyin": "Tā shì yí gè qínláo de nóngmín.", "meaningVi": "Anh ấy là một người nông dân chăm chỉ."}],
    "hsk6_1052": [{"chinese": "湖水清得能看到水底。", "pinyin": "Húshuǐ qīng de néng kàndào shuǐdǐ.", "meaningVi": "Nước hồ trong đến mức có thể nhìn thấy đáy."}],
    "hsk6_1053": [{"chinese": "清晨的空气特别清新。", "pinyin": "Qīngchén de kōngqì tèbié qīngxīn.", "meaningVi": "Không khí buổi sáng sớm đặc biệt trong lành."}],
    "hsk6_1054": [{"chinese": "青春是人生中最美好的时光。", "pinyin": "Qīngchūn shì rénshēng zhōng zuì měihǎo de shíguāng.", "meaningVi": "Tuổi trẻ là quãng thời gian đẹp nhất trong đời người."}],
    "hsk6_1055": [{"chinese": "他正处于青春期。", "pinyin": "Tā zhèng chǔyú qīngchūnqī.", "meaningVi": "Anh ấy đang trong giai đoạn tuổi dậy thì."}],
    "hsk6_1056": [{"chinese": "他最近饮食比较清淡。", "pinyin": "Tā zuìjìn yǐnshí bǐjiào qīngdàn.", "meaningVi": "Gần đây ăn uống của anh ấy khá thanh đạm."}],
    "hsk6_1057": [{"chinese": "阿姨每天负责清洁楼道。", "pinyin": "Āyí měitiān fùzé qīngjié lóudào.", "meaningVi": "Cô lao công mỗi ngày phụ trách dọn vệ sinh hành lang."}],
    "hsk6_1058": [{"chinese": "请清理一下桌面。", "pinyin": "Qǐng qīnglǐ yíxià zhuōmiàn.", "meaningVi": "Xin dọn dẹp mặt bàn."}],
    "hsk6_1059": [{"chinese": "工人正在清扫街道。", "pinyin": "Gōngrén zhèngzài qīngsǎo jiēdào.", "meaningVi": "Công nhân đang quét dọn đường phố."}],
    "hsk6_1060": [{"chinese": "老师耐心倾听学生的意见。", "pinyin": "Lǎoshī nàixīn qīngtīng xuésheng de yìjiàn.", "meaningVi": "Giáo viên kiên nhẫn lắng nghe ý kiến của học sinh."}],
    "hsk6_1061": [{"chinese": "请把水果清洗干净再吃。", "pinyin": "Qǐng bǎ shuǐguǒ qīngxǐ gānjìng zài chī.", "meaningVi": "Xin rửa sạch trái cây trước khi ăn."}],
    "hsk6_1062": [{"chinese": "这张照片非常清晰。", "pinyin": "Zhè zhāng zhàopiàn fēicháng qīngxī.", "meaningVi": "Bức ảnh này vô cùng rõ nét."}],
    "hsk6_1063": [{"chinese": "他的意见倾向于支持这个方案。", "pinyin": "Tā de yìjiàn qīngxiàng yú zhīchí zhège fāng'àn.", "meaningVi": "Ý kiến của anh ấy nghiêng về việc ủng hộ phương án này."}],
    "hsk6_1064": [{"chinese": "他喝了咖啡后头脑清醒多了。", "pinyin": "Tā hēle kāfēi hòu tóunǎo qīngxǐng duō le.", "meaningVi": "Sau khi uống cà phê đầu óc anh ấy tỉnh táo hơn nhiều."}],
    "hsk6_1065": [{"chinese": "这部电影的情节十分紧张。", "pinyin": "Zhè bù diànyǐng de qíngjié shífēn jǐnzhāng.", "meaningVi": "Tình tiết của bộ phim này vô cùng căng thẳng."}],
    "hsk6_1066": [{"chinese": "今天天气晴朗。", "pinyin": "Jīntiān tiānqì qínglǎng.", "meaningVi": "Hôm nay thời tiết trong sáng."}],
    "hsk6_1067": [{"chinese": "请说明一下当时的情形。", "pinyin": "Qǐng shuōmíng yíxià dāngshí de qíngxing.", "meaningVi": "Xin giải thích tình hình lúc đó."}],
    "hsk6_1068": [{"chinese": "他求老师给他多一点时间。", "pinyin": "Tā qiú lǎoshī gěi tā duō yìdiǎn shíjiān.", "meaningVi": "Anh ấy xin thầy giáo cho thêm chút thời gian."}],
    "hsk6_1069": [{"chinese": "他在海边向女友求婚了。", "pinyin": "Tā zài hǎibiān xiàng nǚyǒu qiúhūn le.", "meaningVi": "Anh ấy đã cầu hôn bạn gái bên bờ biển."}],
    "hsk6_1070": [{"chinese": "他向路人大声求救。", "pinyin": "Tā xiàng lùrén dàshēng qiújiù.", "meaningVi": "Anh ấy hét lớn cầu cứu người đi đường."}],
    "hsk6_1071": [{"chinese": "他正在网上求职。", "pinyin": "Tā zhèngzài wǎngshàng qiúzhí.", "meaningVi": "Anh ấy đang tìm việc trên mạng."}],
    "hsk6_1072": [{"chinese": "遇到困难可以向老师求助。", "pinyin": "Yùdào kùnnan kěyǐ xiàng lǎoshī qiúzhù.", "meaningVi": "Gặp khó khăn có thể nhờ giáo viên giúp đỡ."}],
    "hsk6_1073": [{"chinese": "请区分这两个概念。", "pinyin": "Qǐng qūfēn zhè liǎng gè gàiniàn.", "meaningVi": "Xin phân biệt hai khái niệm này."}],
    "hsk6_1074": [{"chinese": "我们需要开辟新的销售渠道。", "pinyin": "Wǒmen xūyào kāipì xīn de xiāoshòu qúdào.", "meaningVi": "Chúng ta cần mở ra kênh bán hàng mới."}],
    "hsk6_1075": [{"chinese": "他为这首诗谱了曲。", "pinyin": "Tā wèi zhè shǒu shī pǔle qǔ.", "meaningVi": "Anh ấy đã phổ nhạc cho bài thơ này."}],
    "hsk6_1076": [{"chinese": "他娶了一位善良的姑娘。", "pinyin": "Tā qǔle yí wèi shànliáng de gūniang.", "meaningVi": "Anh ấy đã cưới một cô gái hiền lành."}],
    "hsk6_1077": [{"chinese": "机器人正在逐渐取代人工。", "pinyin": "Jīqìrén zhèngzài zhújiàn qǔdài réngōng.", "meaningVi": "Robot đang dần thay thế nhân công."}],
    "hsk6_1078": [{"chinese": "这本书写得很有趣味。", "pinyin": "Zhè běn shū xiě de hěn yǒu qùwèi.", "meaningVi": "Cuốn sách này viết rất thú vị."}],
    "hsk6_1079": [{"chinese": "他在纸上画了一个圈。", "pinyin": "Tā zài zhǐ shàng huàle yí gè quān.", "meaningVi": "Anh ấy vẽ một vòng tròn trên giấy."}],
    "hsk6_1080": [{"chinese": "老师全程陪伴学生完成比赛。", "pinyin": "Lǎoshī quánchéng péibàn xuésheng wánchéng bǐsài.", "meaningVi": "Giáo viên đồng hành toàn bộ hành trình cùng học sinh hoàn thành cuộc thi."}],
    "hsk6_1081": [{"chinese": "总统拥有很大的权力。", "pinyin": "Zǒngtǒng yōngyǒu hěn dà de quánlì.", "meaningVi": "Tổng thống nắm giữ quyền lực rất lớn."}],
    "hsk6_1082": [{"chinese": "他用优惠券买了这件衣服。", "pinyin": "Tā yòng yōuhuìquàn mǎile zhè jiàn yīfu.", "meaningVi": "Anh ấy dùng phiếu giảm giá mua chiếc áo này."}],
    "hsk6_1083": [{"chinese": "这款产品存在设计缺陷。", "pinyin": "Zhè kuǎn chǎnpǐn cúnzài shèjì quēxiàn.", "meaningVi": "Sản phẩm này tồn tại khiếm khuyết về thiết kế."}],
    "hsk6_1084": [{"chinese": "公司确立了新的发展目标。", "pinyin": "Gōngsī quèlìle xīn de fāzhǎn mùbiāo.", "meaningVi": "Công ty đã xác lập mục tiêu phát triển mới."}],
    "hsk6_1085": [{"chinese": "干部要联系群众。", "pinyin": "Gànbù yào liánxì qúnzhòng.", "meaningVi": "Cán bộ phải liên hệ với quần chúng."}],
    "hsk6_1086": [{"chinese": "这辆汽车使用清洁燃料。", "pinyin": "Zhè liàng qìchē shǐyòng qīngjié ránliào.", "meaningVi": "Chiếc ô tô này sử dụng nhiên liệu sạch."}],
    "hsk6_1087": [{"chinese": "她把头发染成了棕色。", "pinyin": "Tā bǎ tóufa rǎnchéngle zōngsè.", "meaningVi": "Cô ấy đã nhuộm tóc thành màu nâu."}],
    "hsk6_1088": [{"chinese": "这个话题成了网络热点。", "pinyin": "Zhège huàtí chéngle wǎngluò rèdiǎn.", "meaningVi": "Chủ đề này đã trở thành điểm nóng trên mạng."}],
    "hsk6_1089": [{"chinese": "这部电视剧的热度持续上升。", "pinyin": "Zhè bù diànshìjù de rèdù chíxù shàngshēng.", "meaningVi": "Độ hot của bộ phim truyền hình này liên tục tăng lên."}],
    "hsk6_1090": [{"chinese": "这是今年最热门的专业。", "pinyin": "Zhè shì jīnnián zuì rèmén de zhuānyè.", "meaningVi": "Đây là ngành học hot nhất năm nay."}],
    "hsk6_1091": [{"chinese": "浴室里装了一台热水器。", "pinyin": "Yùshì lǐ zhuāngle yì tái rèshuǐqì.", "meaningVi": "Trong phòng tắm đã lắp một máy nước nóng."}],
    "hsk6_1092": [{"chinese": "请拨打客服热线。", "pinyin": "Qǐng bōdǎ kèfú rèxiàn.", "meaningVi": "Xin gọi đường dây nóng chăm sóc khách hàng."}],
    "hsk6_1093": [{"chinese": "这项政策引发了社会热议。", "pinyin": "Zhè xiàng zhèngcè yǐnfāle shèhuì rèyì.", "meaningVi": "Chính sách này đã gây ra cuộc bàn luận sôi nổi trong xã hội."}],
    "hsk6_1094": [{"chinese": "人工智能正在改变我们的生活。", "pinyin": "Réngōng zhìnéng zhèngzài gǎibiàn wǒmen de shēnghuó.", "meaningVi": "Trí tuệ nhân tạo đang thay đổi cuộc sống của chúng ta."}],
    "hsk6_1095": [{"chinese": "人家早就告诉过你了。", "pinyin": "Rénjia zǎo jiù gàosuguo nǐ le.", "meaningVi": "Người ta đã sớm nói cho bạn biết rồi."}],
    "hsk6_1096": [{"chinese": "这个城市的人均收入较高。", "pinyin": "Zhège chéngshì de rénjūn shōurù jiào gāo.", "meaningVi": "Thu nhập bình quân đầu người của thành phố này khá cao."}],
    "hsk6_1097": [{"chinese": "节日期间景区人山人海。", "pinyin": "Jiérì qījiān jǐngqū rénshān-rénhǎi.", "meaningVi": "Trong dịp lễ khu du lịch đông như biển người."}],
    "hsk6_1098": [{"chinese": "许多社会人士参加了这次活动。", "pinyin": "Xǔduō shèhuì rénshì cānjiāle zhè cì huódòng.", "meaningVi": "Nhiều nhân sĩ trong xã hội đã tham gia hoạt động này."}],
    "hsk6_1099": [{"chinese": "她在公司负责人事工作。", "pinyin": "Tā zài gōngsī fùzé rénshì gōngzuò.", "meaningVi": "Cô ấy phụ trách công tác nhân sự trong công ty."}],
    "hsk6_1100": [{"chinese": "这场事故是人为造成的。", "pinyin": "Zhè chǎng shìgù shì rénwéi zàochéng de.", "meaningVi": "Tai nạn này là do con người gây ra."}],
    "hsk6_1101": [{"chinese": "请在人行道上行走。", "pinyin": "Qǐng zài rénxíngdào shàng xíngzǒu.", "meaningVi": "Xin đi bộ trên vỉa hè."}],
    "hsk6_1102": [{"chinese": "他默默忍受着痛苦。", "pinyin": "Tā mòmò rěnshòuzhe tòngkǔ.", "meaningVi": "Anh ấy lặng lẽ chịu đựng nỗi đau."}],
    "hsk6_1103": [{"chinese": "他勇敢地向老师认错。", "pinyin": "Tā yǒnggǎn de xiàng lǎoshī rèncuò.", "meaningVi": "Anh ấy dũng cảm nhận lỗi với giáo viên."}],
    "hsk6_1104": [{"chinese": "法院认定他没有责任。", "pinyin": "Fǎyuàn rèndìng tā méiyǒu zérèn.", "meaningVi": "Tòa án xác định anh ấy không có trách nhiệm."}],
    "hsk6_1105": [{"chinese": "他的努力得到了大家的认可。", "pinyin": "Tā de nǔlì dédàole dàjiā de rènkě.", "meaningVi": "Nỗ lực của anh ấy đã được mọi người thừa nhận."}],
    "hsk6_1106": [{"chinese": "大家都认同这个观点。", "pinyin": "Dàjiā dōu rèntóng zhège guāndiǎn.", "meaningVi": "Mọi người đều đồng tình với quan điểm này."}],
    "hsk6_1107": [{"chinese": "这项研究提高了人们对疾病的认知。", "pinyin": "Zhè xiàng yánjiū tígāole rénmen duì jíbìng de rènzhī.", "meaningVi": "Nghiên cứu này đã nâng cao nhận thức của mọi người về căn bệnh."}],
    "hsk6_1108": [{"chinese": "他退休后仍旧关心公司发展。", "pinyin": "Tā tuìxiū hòu réngjiù guānxīn gōngsī fāzhǎn.", "meaningVi": "Sau khi nghỉ hưu anh ấy vẫn quan tâm đến sự phát triển của công ty."}],
    "hsk6_1109": [{"chinese": "日后有机会再见面吧。", "pinyin": "Rìhòu yǒu jīhuì zài jiànmiàn ba.", "meaningVi": "Sau này có dịp gặp lại nhau nhé."}],
    "hsk6_1110": [{"chinese": "日前，该地区发生了一场地震。", "pinyin": "Rìqián, gāi dìqū fāshēngle yì chǎng dìzhèn.", "meaningVi": "Gần đây, khu vực đó đã xảy ra một trận động đất."}],
    "hsk6_1111": [{"chinese": "医护人员日夜守护病人。", "pinyin": "Yīhù rényuán rìyè shǒuhù bìngrén.", "meaningVi": "Nhân viên y tế ngày đêm chăm sóc bệnh nhân."}],
    "hsk6_1112": [{"chinese": "城市交通日益拥挤。", "pinyin": "Chéngshì jiāotōng rìyì yōngjǐ.", "meaningVi": "Giao thông thành phố ngày càng đông đúc."}],
    "hsk6_1113": [{"chinese": "这道菜融合了中西方口味。", "pinyin": "Zhè dào cài rónghéle Zhōng-Xīfāng kǒuwèi.", "meaningVi": "Món ăn này kết hợp hương vị Trung và phương Tây."}],
    "hsk6_1114": [{"chinese": "冰块很快就融化了。", "pinyin": "Bīngkuài hěn kuài jiù rónghuà le.", "meaningVi": "Đá viên nhanh chóng tan chảy."}],
    "hsk6_1115": [{"chinese": "这个硬盘的容量很大。", "pinyin": "Zhège yìngpán de róngliàng hěn dà.", "meaningVi": "Dung lượng của ổ cứng này rất lớn."}],
    "hsk6_1116": [{"chinese": "他很快融入了新的集体。", "pinyin": "Tā hěn kuài róngrùle xīn de jítǐ.", "meaningVi": "Anh ấy nhanh chóng hòa nhập vào tập thể mới."}],
    "hsk6_1117": [{"chinese": "这是一份莫大的荣誉。", "pinyin": "Zhè shì yí fèn mòdà de róngyù.", "meaningVi": "Đây là một vinh dự vô cùng to lớn."}],
    "hsk6_1118": [{"chinese": "这块布料十分柔软。", "pinyin": "Zhè kuài bùliào shífēn róuruǎn.", "meaningVi": "Tấm vải này vô cùng mềm mại."}],
    "hsk6_1119": [{"chinese": "外国游客需要办理入境手续。", "pinyin": "Wàiguó yóukè xūyào bànlǐ rùjìng shǒuxù.", "meaningVi": "Du khách nước ngoài cần làm thủ tục nhập cảnh."}],
    "hsk6_1120": [{"chinese": "这本书适合初学者入门。", "pinyin": "Zhè běn shū shìhé chūxuézhě rùmén.", "meaningVi": "Cuốn sách này phù hợp cho người mới bắt đầu nhập môn."}],
    "hsk6_1121": [{"chinese": "他成功入选了国家队。", "pinyin": "Tā chénggōng rùxuǎnle guójiāduì.", "meaningVi": "Anh ấy đã được tuyển chọn thành công vào đội tuyển quốc gia."}],
    "hsk6_1122": [{"chinese": "认清自己的弱点才能不断进步。", "pinyin": "Rènqīng zìjǐ de ruòdiǎn cáinéng búduàn jìnbù.", "meaningVi": "Nhận rõ điểm yếu của bản thân mới có thể không ngừng tiến bộ."}],
    "hsk6_1123": [{"chinese": "他往地上撒了一些种子。", "pinyin": "Tā wǎng dìshang sǎle yìxiē zhǒngzi.", "meaningVi": "Anh ấy rắc một ít hạt giống xuống đất."}],
    "hsk6_1124": [{"chinese": "他把信塞进了信箱。", "pinyin": "Tā bǎ xìn sāijìnle xìnxiāng.", "meaningVi": "Anh ấy nhét lá thư vào hộp thư."}],
    "hsk6_1125": [{"chinese": "本届赛事吸引了众多观众。", "pinyin": "Běn jiè sàishì xīyǐnle zhòngduō guānzhòng.", "meaningVi": "Sự kiện thi đấu lần này đã thu hút đông đảo khán giả."}],
    "hsk6_1127": [{"chinese": "他喜欢写散文。", "pinyin": "Tā xǐhuan xiě sǎnwén.", "meaningVi": "Anh ấy thích viết văn xuôi."}],
    "hsk6_1129": [{"chinese": "花园里散发着阵阵花香。", "pinyin": "Huāyuán lǐ sànfāzhe zhènzhèn huāxiāng.", "meaningVi": "Trong vườn hoa tỏa ra từng đợt hương thơm."}],
    "hsk6_1130": [{"chinese": "他喊得嗓子都哑了。", "pinyin": "Tā hǎn de sǎngzi dōu yǎ le.", "meaningVi": "Anh ấy hét đến khản cả giọng."}],
    "hsk6_1131": [{"chinese": "事故使他丧失了工作能力。", "pinyin": "Shìgù shǐ tā sàngshīle gōngzuò nénglì.", "meaningVi": "Tai nạn đã khiến anh ấy mất khả năng lao động."}],
    "hsk6_1132": [{"chinese": "机场安检会扫描每一件行李。", "pinyin": "Jīchǎng ānjiǎn huì sǎomiáo měi yí jiàn xíngli.", "meaningVi": "An ninh sân bay sẽ quét từng kiện hành lý."}],
    "hsk6_1133": [{"chinese": "他从不杀害任何动物。", "pinyin": "Tā cóng bù shāhài rènhé dòngwù.", "meaningVi": "Anh ấy không bao giờ giết hại bất kỳ con vật nào."}],
    "hsk6_1134": [{"chinese": "司机紧急刹车了。", "pinyin": "Sījī jǐnjí shāchē le.", "meaningVi": "Tài xế đã phanh gấp."}],
    "hsk6_1135": [{"chinese": "海里有一条鲨鱼。", "pinyin": "Hǎi lǐ yǒu yì tiáo shāyú.", "meaningVi": "Trong biển có một con cá mập."}],
    "hsk6_1136": [{"chinese": "我们对候选人进行了筛选。", "pinyin": "Wǒmen duì hòuxuǎnrén jìnxíngle shāixuǎn.", "meaningVi": "Chúng tôi đã tiến hành sàng lọc các ứng viên."}],
    "hsk6_1137": [{"chinese": "他们终于到达了山顶。", "pinyin": "Tāmen zhōngyú dàodále shāndǐng.", "meaningVi": "Cuối cùng họ cũng đã lên đến đỉnh núi."}],
    "hsk6_1138": [{"chinese": "远处的山峰被云雾笼罩。", "pinyin": "Yuǎnchù de shānfēng bèi yúnwù lǒngzhào.", "meaningVi": "Đỉnh núi ở xa bị mây mù bao phủ."}],
    "hsk6_1139": [{"chinese": "羊群在山坡上吃草。", "pinyin": "Yángqún zài shānpō shàng chī cǎo.", "meaningVi": "Đàn cừu đang ăn cỏ trên sườn núi."}],
    "hsk6_1140": [{"chinese": "远处闪了一下光。", "pinyin": "Yuǎnchù shǎnle yíxià guāng.", "meaningVi": "Ở xa lóe lên một tia sáng."}],
    "hsk6_1141": [{"chinese": "天空中划过一道闪电。", "pinyin": "Tiānkōng zhōng huàguò yí dào shǎndiàn.", "meaningVi": "Trên bầu trời lóe lên một tia chớp."}],
    "hsk6_1143": [{"chinese": "这个商标已经注册了。", "pinyin": "Zhège shāngbiāo yǐjīng zhùcè le.", "meaningVi": "Nhãn hiệu này đã được đăng ký."}],
    "hsk6_1144": [{"chinese": "医生给他的伤口消毒。", "pinyin": "Yīshēng gěi tā de shāngkǒu xiāodú.", "meaningVi": "Bác sĩ khử trùng vết thương cho anh ấy."}],
    "hsk6_1145": [{"chinese": "这场事故造成了严重的伤亡。", "pinyin": "Zhè chǎng shìgù zàochéngle yánzhòng de shāngwáng.", "meaningVi": "Tai nạn này đã gây ra thương vong nghiêm trọng."}],
    "hsk6_1146": [{"chinese": "医院正在全力救治伤员。", "pinyin": "Yīyuàn zhèngzài quánlì jiùzhì shāngyuán.", "meaningVi": "Bệnh viện đang nỗ lực hết sức cứu chữa người bị thương."}],
    "hsk6_1147": [{"chinese": "他因为轻信而上当了。", "pinyin": "Tā yīnwèi qīngxìn ér shàngdàng le.", "meaningVi": "Anh ấy vì nhẹ dạ tin người mà bị lừa."}],
    "hsk6_1148": [{"chinese": "他把情况汇报给了上级。", "pinyin": "Tā bǎ qíngkuàng huìbào gěile shàngjí.", "meaningVi": "Anh ấy đã báo cáo tình hình lên cấp trên."}],
    "hsk6_1149": [{"chinese": "他是一个很上进的年轻人。", "pinyin": "Tā shì yí gè hěn shàngjìn de niánqīngrén.", "meaningVi": "Anh ấy là một thanh niên rất cầu tiến."}],
    "hsk6_1150": [{"chinese": "这款新手机即将上市。", "pinyin": "Zhè kuǎn xīn shǒujī jíjiāng shàngshì.", "meaningVi": "Chiếc điện thoại mới này sắp được ra mắt thị trường."}],
    "hsk6_1151": [{"chinese": "以上述内容仅供参考。", "pinyin": "Yǐ shàngshù nèiróng jǐn gōng cānkǎo.", "meaningVi": "Nội dung nêu trên chỉ để tham khảo."}],
    "hsk6_1152": [{"chinese": "演员们陆续上台表演。", "pinyin": "Yǎnyuánmen lùxù shàngtái biǎoyǎn.", "meaningVi": "Các diễn viên lần lượt lên sân khấu biểu diễn."}],
    "hsk6_1153": [{"chinese": "会议定在下月上旬举行。", "pinyin": "Huìyì dìng zài xiàyuè shàngxún jǔxíng.", "meaningVi": "Cuộc họp được ấn định tổ chức vào thượng tuần tháng sau."}],
    "hsk6_1154": [{"chinese": "这是一档少儿节目。", "pinyin": "Zhè shì yí dàng shào'ér jiémù.", "meaningVi": "Đây là một chương trình dành cho thiếu nhi."}],
    "hsk6_1155": [{"chinese": "他不小心咬到了舌头。", "pinyin": "Tā bù xiǎoxīn yǎodàole shétou.", "meaningVi": "Anh ấy vô tình cắn phải lưỡi."}],
    "hsk6_1156": [{"chinese": "这家出版社出版了很多好书。", "pinyin": "Zhè jiā chūbǎnshè chūbǎnle hěn duō hǎo shū.", "meaningVi": "Nhà xuất bản này đã xuất bản rất nhiều cuốn sách hay."}],
    "hsk6_1157": [{"chinese": "阳光射进了房间。", "pinyin": "Yángguāng shèjìnle fángjiān.", "meaningVi": "Ánh nắng chiếu vào trong phòng."}],
    "hsk6_1158": [{"chinese": "这个问题涉及很多方面。", "pinyin": "Zhège wèntí shèjí hěn duō fāngmiàn.", "meaningVi": "Vấn đề này liên quan đến nhiều mặt."}],
    "hsk6_1159": [{"chinese": "他参加了射击比赛。", "pinyin": "Tā cānjiāle shèjī bǐsài.", "meaningVi": "Anh ấy đã tham gia cuộc thi bắn súng."}],
    "hsk6_1160": [{"chinese": "婚礼现场安排了专业摄像。", "pinyin": "Hūnlǐ xiànchǎng ānpáile zhuānyè shèxiàng.", "meaningVi": "Hiện trường đám cưới đã sắp xếp quay phim chuyên nghiệp."}],
    "hsk6_1161": [{"chinese": "他设想了一个大胆的计划。", "pinyin": "Tā shèxiǎngle yí gè dàdǎn de jìhuà.", "meaningVi": "Anh ấy đã hình dung ra một kế hoạch táo bạo."}],
    "hsk6_1162": [{"chinese": "门口安装了一个摄像头。", "pinyin": "Ménkǒu ānzhuāngle yí gè shèxiàngtóu.", "meaningVi": "Trước cửa đã lắp một chiếc camera."}],
    "hsk6_1163": [{"chinese": "运动有益于身心健康。", "pinyin": "Yùndòng yǒuyì yú shēnxīn jiànkāng.", "meaningVi": "Vận động có lợi cho sức khỏe thân và tâm."}],
    "hsk6_1164": [{"chinese": "深夜的街道格外安静。", "pinyin": "Shēnyè de jiēdào géwài ānjìng.", "meaningVi": "Đường phố lúc đêm khuya vô cùng yên tĩnh."}],
    "hsk6_1165": [{"chinese": "古人相信神的存在。", "pinyin": "Gǔrén xiāngxìn shén de cúnzài.", "meaningVi": "Người xưa tin vào sự tồn tại của thần linh."}],
    "hsk6_1166": [{"chinese": "这根神经控制着手指的运动。", "pinyin": "Zhè gēn shénjīng kòngzhìzhe shǒuzhǐ de yùndòng.", "meaningVi": "Dây thần kinh này điều khiển chuyển động của ngón tay."}],
    "hsk6_1167": [{"chinese": "大自然充满了神奇的力量。", "pinyin": "Dàzìrán chōngmǎnle shénqí de lìliang.", "meaningVi": "Thiên nhiên tràn đầy sức mạnh thần kỳ."}],
    "hsk6_1168": [{"chinese": "每个人的审美观点都不一样。", "pinyin": "Měi gè rén de shěnměi guāndiǎn dōu bù yíyàng.", "meaningVi": "Quan điểm thẩm mỹ của mỗi người đều không giống nhau."}],
    "hsk6_1169": [],
    "hsk6_1170": [{"chinese": "这个软件可以自动生成报告。", "pinyin": "Zhège ruǎnjiàn kěyǐ zìdòng shēngchéng bàogào.", "meaningVi": "Phần mềm này có thể tự động tạo ra báo cáo."}],
    "hsk6_1171": [{"chinese": "汉语的声调很难掌握。", "pinyin": "Hànyǔ de shēngdiào hěn nán zhǎngwò.", "meaningVi": "Thanh điệu tiếng Trung rất khó nắm vững."}],
    "hsk6_1172": [{"chinese": "这种植物生命力很强。", "pinyin": "Zhè zhǒng zhíwù shēngmìnglì hěn qiáng.", "meaningVi": "Loại thực vật này có sức sống rất mạnh mẽ."}],
    "hsk6_1173": [{"chinese": "我们应该保护生态环境。", "pinyin": "Wǒmen yīnggāi bǎohù shēngtài huánjìng.", "meaningVi": "Chúng ta nên bảo vệ môi trường sinh thái."}],
    "hsk6_1174": [{"chinese": "他为升学付出了很多努力。", "pinyin": "Tā wèi shēngxué fùchūle hěn duō nǔlì.", "meaningVi": "Anh ấy đã bỏ ra rất nhiều nỗ lực để lên bậc học cao hơn."}],
    "hsk6_1175": [{"chinese": "请把剩余的食物放进冰箱。", "pinyin": "Qǐng bǎ shèngyú de shíwù fàngjìn bīngxiāng.", "meaningVi": "Xin cho thức ăn còn thừa vào tủ lạnh."}],
    "hsk6_1176": [{"chinese": "他从小背诵了很多古代诗词。", "pinyin": "Tā cóngxiǎo bèisòngle hěn duō gǔdài shīcí.", "meaningVi": "Anh ấy từ nhỏ đã học thuộc rất nhiều thơ từ cổ đại."}],
    "hsk6_1177": [{"chinese": "这个房间的湿度比较高。", "pinyin": "Zhège fángjiān de shīdù bǐjiào gāo.", "meaningVi": "Độ ẩm của căn phòng này khá cao."}],
    "hsk6_1178": [{"chinese": "他拜了一位武术师父。", "pinyin": "Tā bàile yí wèi wǔshù shīfu.", "meaningVi": "Anh ấy đã bái một vị sư phụ võ thuật."}],
    "hsk6_1179": [{"chinese": "她喜欢朗诵诗歌。", "pinyin": "Tā xǐhuan lǎngsòng shīgē.", "meaningVi": "Cô ấy thích ngâm thơ ca."}],
    "hsk6_1180": [{"chinese": "狮子被称为百兽之王。", "pinyin": "Shīzi bèi chēngwéi bǎishòu zhī wáng.", "meaningVi": "Sư tử được gọi là chúa tể muôn loài."}],
    "hsk6_1181": [{"chinese": "这个字他不识。", "pinyin": "Zhège zì tā bù shí.", "meaningVi": "Chữ này anh ấy không biết."}],
    "hsk6_1182": [{"chinese": "她弯腰拾起了地上的钱包。", "pinyin": "Tā wānyāo shíqǐle dìshang de qiánbāo.", "meaningVi": "Cô ấy cúi người nhặt lên chiếc ví trên đất."}],
    "hsk6_1183": [{"chinese": "这个系统可以识别人脸。", "pinyin": "Zhège xìtǒng kěyǐ shíbié rénliǎn.", "meaningVi": "Hệ thống này có thể nhận diện khuôn mặt."}],
    "hsk6_1184": [{"chinese": "那段时光让人怀念。", "pinyin": "Nà duàn shíguāng ràng rén huáiniàn.", "meaningVi": "Khoảng thời gian đó khiến người ta lưu luyến."}],
    "hsk6_1185": [{"chinese": "我跟你说实话吧。", "pinyin": "Wǒ gēn nǐ shuō shíhuà ba.", "meaningVi": "Tôi nói thật với bạn nhé."}],
    "hsk6_1186": [{"chinese": "这家店的商品价格实惠。", "pinyin": "Zhè jiā diàn de shāngpǐn jiàgé shíhuì.", "meaningVi": "Giá cả hàng hóa của cửa hàng này thiết thực."}],
    "hsk6_1187": [{"chinese": "现在还不是最好的时机。", "pinyin": "Xiànzài hái bú shì zuì hǎo de shíjī.", "meaningVi": "Bây giờ vẫn chưa phải là thời cơ tốt nhất."}],
    "hsk6_1188": [{"chinese": "她一直走在时尚的前沿。", "pinyin": "Tā yìzhí zǒu zài shíshàng de qiányán.", "meaningVi": "Cô ấy luôn đi đầu trong lĩnh vực thời trang."}],
    "hsk6_1189": [{"chinese": "这个平台可以实时更新数据。", "pinyin": "Zhège píngtái kěyǐ shíshí gēngxīn shùjù.", "meaningVi": "Nền tảng này có thể cập nhật dữ liệu theo thời gian thực."}],
    "hsk6_1190": [{"chinese": "这辆车的时速可达两百公里。", "pinyin": "Zhè liàng chē de shísù kě dá liǎngbǎi gōnglǐ.", "meaningVi": "Tốc độ của chiếc xe này có thể đạt hai trăm km một giờ."}],
    "hsk6_1191": [{"chinese": "这个国家石油资源丰富。", "pinyin": "Zhège guójiā shíyóu zīyuán fēngfù.", "meaningVi": "Quốc gia này tài nguyên dầu mỏ phong phú."}],
    "hsk6_1192": [{"chinese": "天气太热，他没有食欲。", "pinyin": "Tiānqì tài rè, tā méiyǒu shíyù.", "meaningVi": "Thời tiết quá nóng, anh ấy không có cảm giác thèm ăn."}],
    "hsk6_1193": [{"chinese": "这个问题的实质在于沟通不足。", "pinyin": "Zhège wèntí de shízhì zàiyú gōutōng bùzú.", "meaningVi": "Bản chất của vấn đề này nằm ở việc thiếu giao tiếp."}],
    "hsk6_1194": [{"chinese": "他信心十足地走上了讲台。", "pinyin": "Tā xìnxīn shízú de zǒushàngle jiǎngtái.", "meaningVi": "Anh ấy tự tin đầy đủ bước lên bục giảng."}],
    "hsk6_1195": [{"chinese": "请大家使劲往前推。", "pinyin": "Qǐng dàjiā shǐjìn wǎng qián tuī.", "meaningVi": "Xin mọi người dùng sức đẩy về phía trước."}],
    "hsk6_1196": [{"chinese": "士兵们坚守在边境。", "pinyin": "Shìbīngmen jiānshǒu zài biānjìng.", "meaningVi": "Các binh sĩ kiên trì bám trụ ở biên giới."}],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ids, universe, tiers = get_next_batch_ids(BATCH_SIZE)

    if len(ids) != BATCH_SIZE:
        print(f"FAIL: queue produced {len(ids)} records, expected {BATCH_SIZE}", file=sys.stderr)
        sys.exit(1)
    if ids != sorted(EXAMPLES_CONTENT.keys(), key=lambda rid: (tiers[rid], rid)):
        print("FAIL: queue-computed ID set does not match this script's embedded EXAMPLES_CONTENT "
              "-- refusing to proceed", file=sys.stderr)
        sys.exit(1)

    print(f"=== batch {BATCH_NUMBER:03d} selection ===")
    print(f"records: {len(ids)}")

    if args.dry_run:
        print("=== DRY RUN: no files written ===")
        return

    if OUTPUT_PATH.exists():
        print(f"FAIL: {OUTPUT_PATH} already exists -- refusing to overwrite.", file=sys.stderr)
        sys.exit(1)

    level_counts: dict[int, int] = {}
    for rid in ids:
        level_counts[universe[rid]["_level"]] = level_counts.get(universe[rid]["_level"], 0) + 1

    source_hashes = {}
    for n in sorted(level_counts.keys()):
        path = REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
        source_hashes[f"hsk{n}"] = hashlib.sha256(load_json_text(path).encode("utf-8")).hexdigest()

    generated_at = datetime.now(timezone.utc).isoformat()

    records_out = []
    total_examples = 0
    for rid in ids:
        r = universe[rid]
        examples = EXAMPLES_CONTENT[rid]
        total_examples += len(examples)
        records_out.append({
            "sourceId": rid,
            "sourceWord": r["word"],
            "hskLevel": r["_level"],
            "riskTier": tiers[rid],
            "qaStatus": "needs_review" if rid in NEEDS_REVIEW_IDS else "pending",
            "reviewerStatus": "unreviewed",
            "integrationStatus": "not_integrated",
            "examples": examples,
        })

    artifact = {
        "batchId": f"batch-{BATCH_NUMBER:03d}",
        "batchNumber": BATCH_NUMBER,
        "generatedAt": generated_at,
        "generationMethod": GENERATION_METHOD,
        "generatorScript": f"tools/hsk/examples/generate_examples_batch_{BATCH_NUMBER:03d}.py",
        "sourceProductionHashes": source_hashes,
        "batchSize": len(records_out),
        "totalExamples": total_examples,
        "records": records_out,
    }

    text = json.dumps(artifact, indent=2, ensure_ascii=False) + "\n"
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    print(f"Wrote {OUTPUT_PATH}")
    print(f"records={len(records_out)} total_examples={total_examples}")


if __name__ == "__main__":
    main()
