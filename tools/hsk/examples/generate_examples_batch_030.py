"""P5.10.3 (continued) -- Batch 030 (continues immediately after
examples_batch_029.json). This batch is the FIRST entirely tier-2
batch: with batch 029 having exhausted HSK6's tier-1 queue, the
deterministic (tier, id) sort now works through tier-2 records across
HSK1-4, in plain-string id order within tier 2. Spans hsk1_012
(tier 2's smallest remaining HSK1 id after hsk1_011, taken in batch
029) through hsk4_426. HSK/tier for every record was read directly
from load_universe()/classify_risk_tiers output and cross-checked
against the expected distribution (HSK1:20, HSK2:150, HSK3:65,
HSK4:65, all tier 2) before drafting began -- confirmed to match
exactly, with clean transitions at HSK1->HSK2 (index 20), HSK2->HSK3
(index 170), and HSK3->HSK4 (index 235). No numeric-suffix or other
source-data anomalies were found anywhere in this batch.

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** This is the pipeline's most basic-vocabulary-dense batch ***
Tier-2 HSK1-4 words are short, extremely common function words and
elementary vocabulary (对/多/分/和/几/可以/没有/上/下/在, etc.), which
makes natural, distinct sentences harder to keep apart than for the
low-frequency HSK6 vocabulary in prior batches. Two specific risk
areas required deliberate handling:
  - The directional-complement cluster (出来/出去/进来/进去/上来/上去/
    下来/下去/回来/回去/过来/过去 -- twelve words, all built the same
    way: verb + directional complement) is structurally repetitive by
    nature. A first draft using "请你 X 一下。" for several of them
    (出来/上来/过来) was caught as excessively similar during
    drafting and diversified before generation (see below).
  - Several words recur as SEPARATE vocabulary entries at different
    HSK levels with the same character: 过去 (hsk2_050, "the past" /
    "to pass by" sense) and 过去 (hsk3_160, same characters, given the
    "to carry something over there" sense); 等 (hsk2_034 "to wait"
    vs hsk4_147 "to wait" in a different register); 站 (hsk2_186,
    verb "to stand" vs hsk3_466, noun "station"). Each pair given
    deliberately distinct grammatical function/context so the two
    records are not near-duplicates of each other.

Self-caught fixes made during drafting (before the first generation
run, to reduce avoidable near-template flags in an unusually
repetitive vocabulary set):
  - 上来 (hsk2_125): first draft "请你上来一下。" was too similar to
    出来's "请你出来一下。" and 过来's first draft -- rewritten to
    "运动员们陆续上来领奖。".
  - 过来 (hsk2_048): first draft "请你过来一下。" -- rewritten to
    "老师叫我过来一趟。".
  - 下去 (hsk2_160): first draft "请你先下去等着。" echoed the same
    "请你...一下/着" pattern -- rewritten to "楼梯很滑，慢慢下去。".
  - 票 (hsk2_116): first draft "请出示您的票。" was too similar to
    出's own "请出示证件。" (both "请出示...") -- rewritten to "他把票
    放进了口袋。".
  - 名 (hsk2_104): first draft used an awkward measure-word
    construction -- rewritten to the more natural "这次比赛有一百多
    名选手参加。".
  - 道 (hsk4_140): first draft "这道题我做对了。" was too similar to
    hsk3_275's own "这道题真难。" (both "这道题...") -- rewritten to
    "他说的话很有道理。" (using the 道理 compound sense instead).

Fixes applied after the first validator pass (caught by
validate_examples_batch_p103.py's no_duplicate_sentences_across_
pilot_and_batches check): five EXACT duplicates, all common,
elementary sentences that already existed in the pilot corpus
(unsurprising for HSK1-2 vocabulary this basic) --
  - 病 (bìng): "他生病了，没来上课。" -> "医生正在给他看病。".
  - 年 (nián): "我今年二十岁。" -> "我在这家公司工作三年了。".
  - 天 (tiān): "今天天气很好。" -> "明天是星期五。".
  - 别 (bié): "别担心，一切都会好的。" -> "别在这里抽烟。".
  - 告诉 (gàosu): "请告诉我你的电话号码。" -> "请把这个好消息告诉
    大家。".
A second validator pass found five MORE exact duplicates, again
common HSK3-4 sentences already present in the corpus --
  - 努力 (nǔlì): "只要努力，就一定能成功。" -> "他为了这次考试做了
    很多努力。".
  - 小心 (xiǎoxīn): "过马路要小心。" -> "他做事一直很小心。".
  - 总 (zǒng): "他总是迟到。" -> "他做作业总是很认真。".
  - 关键 (guānjiàn): "成功的关键在于坚持。" -> "这份合同的关键条款
    需要仔细阅读。".
  - 道 (dào): "他说的话很有道理。" -> "这道数学题很复杂。".
A third validator pass found one more exact duplicate --
  - 走 (zǒu): "我们走吧。" -> "他一句话没说就走了。".

Near-template fixes (character-bigram Jaccard >= 0.55 against the
full pilot+002-029 corpus, caught by the independent script-level
check, not the validator): as expected for this unusually basic
vocabulary set, twenty flags surfaced, all fixed by diverging
sentence structure while preserving natural, correct usage -- 经常,
快乐, 词, 面, 表, 姓, 疼, 比, 一起, 过年, 多, 错误, 正, 小孩儿, 等,
起, 前面, 可能, 家 (see the individual EXAMPLES_CONTENT entries for
the final sentences; the first-draft versions each collided with an
existing corpus sentence built on the same short, common-vocabulary
template, e.g. "X比Y冷/大", "我肚子有点(儿)疼", "请问您贵姓" etc.).
Re-verified after these fixes: zero cross-corpus flags, zero
within-batch flags (see validation report).

All re-verified against the full pilot+002-029 corpus with zero
remaining exact duplicates and zero near-template flags (see
validation report).

Usage:
    python generate_examples_batch_030.py --dry-run
    python generate_examples_batch_030.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 30
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_030.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# No numeric-suffix homograph records in this batch.
NEEDS_REVIEW_IDS: set[str] = set()

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk1_012": [{"chinese": "医生正在给他看病。", "pinyin": "Yīshēng zhèngzài gěi tā kànbìng.", "meaningVi": "Bác sĩ đang khám bệnh cho anh ấy."}],
    "hsk1_044": [{"chinese": "你说得很对。", "pinyin": "Nǐ shuō de hěn duì.", "meaningVi": "Bạn nói rất đúng."}],
    "hsk1_046": [{"chinese": "这个公园里种了很多花。", "pinyin": "Zhège gōngyuán lǐ zhòngle hěn duō huā.", "meaningVi": "Trong công viên này trồng rất nhiều hoa."}],
    "hsk1_055": [{"chinese": "现在是三点十分。", "pinyin": "Xiànzài shì sān diǎn shí fēn.", "meaningVi": "Bây giờ là ba giờ mười phút."}],
    "hsk1_063": [{"chinese": "他每天都去工作。", "pinyin": "Tā měitiān dōu qù gōngzuò.", "meaningVi": "Anh ấy ngày nào cũng đi làm việc."}],
    "hsk1_076": [{"chinese": "今天是几号？", "pinyin": "Jīntiān shì jǐ hào?", "meaningVi": "Hôm nay là ngày mấy?"}],
    "hsk1_078": [{"chinese": "我和妈妈一起去买菜。", "pinyin": "Wǒ hé māma yìqǐ qù mǎi cài.", "meaningVi": "Tôi và mẹ cùng đi mua rau."}],
    "hsk1_085": [{"chinese": "你家有几口人？", "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?", "meaningVi": "Nhà bạn có mấy người?"}],
    "hsk1_086": [{"chinese": "我家养了一只小猫。", "pinyin": "Wǒ jiā yǎngle yì zhī xiǎomāo.", "meaningVi": "Nhà tôi nuôi một con mèo con."}],
    "hsk1_102": [{"chinese": "我可以进来吗？", "pinyin": "Wǒ kěyǐ jìnlái ma?", "meaningVi": "Tôi có thể vào được không?"}],
    "hsk1_104": [{"chinese": "请张开口。", "pinyin": "Qǐng zhāngkāi kǒu.", "meaningVi": "Xin mở miệng ra."}],
    "hsk1_118": [{"chinese": "他最近工作很忙。", "pinyin": "Tā zuìjìn gōngzuò hěn máng.", "meaningVi": "Gần đây anh ấy làm việc rất bận."}],
    "hsk1_122": [{"chinese": "桌子上没有水果。", "pinyin": "Zhuōzi shàng méiyǒu shuǐguǒ.", "meaningVi": "Trên bàn không có trái cây."}],
    "hsk1_149": [{"chinese": "我在这家公司工作三年了。", "pinyin": "Wǒ zài zhè jiā gōngsī gōngzuò sān nián le.", "meaningVi": "Tôi đã làm việc ở công ty này ba năm rồi."}],
    "hsk1_175": [{"chinese": "书在桌子上。", "pinyin": "Shū zài zhuōzi shàng.", "meaningVi": "Sách ở trên bàn."}],
    "hsk1_180": [{"chinese": "今天来的人很少。", "pinyin": "Jīntiān lái de rén hěn shǎo.", "meaningVi": "Hôm nay số người đến rất ít."}],
    "hsk1_207": [{"chinese": "明天是星期五。", "pinyin": "Míngtiān shì xīngqīwǔ.", "meaningVi": "Ngày mai là thứ Sáu."}],
    "hsk1_226": [{"chinese": "请把书放下。", "pinyin": "Qǐng bǎ shū fàngxià.", "meaningVi": "Xin đặt sách xuống."}],
    "hsk1_234": [{"chinese": "这只狗很小。", "pinyin": "Zhè zhī gǒu hěn xiǎo.", "meaningVi": "Con chó này rất nhỏ."}],
    "hsk1_271": [{"chinese": "他在家看电视。", "pinyin": "Tā zài jiā kàn diànshì.", "meaningVi": "Anh ấy đang ở nhà xem tivi."}],
    "hsk2_002": [{"chinese": "我的爱好是画画。", "pinyin": "Wǒ de àihào shì huàhuà.", "meaningVi": "Sở thích của tôi là vẽ tranh."}],
    "hsk2_004": [{"chinese": "我们班一共有三十个学生。", "pinyin": "Wǒmen bān yígòng yǒu sānshí gè xuésheng.", "meaningVi": "Lớp chúng tôi tổng cộng có ba mươi học sinh."}],
    "hsk2_005": [{"chinese": "请帮我拿一下这个包。", "pinyin": "Qǐng bāng wǒ ná yíxià zhège bāo.", "meaningVi": "Xin giúp tôi cầm cái túi này."}],
    "hsk2_006": [{"chinese": "谢谢你来帮忙。", "pinyin": "Xièxie nǐ lái bāngmáng.", "meaningVi": "Cảm ơn bạn đã đến giúp đỡ."}],
    "hsk2_007": [{"chinese": "她买了一个新包。", "pinyin": "Tā mǎile yí gè xīn bāo.", "meaningVi": "Cô ấy đã mua một chiếc túi mới."}],
    "hsk2_008": [{"chinese": "请拿出你的本子。", "pinyin": "Qǐng náchū nǐ de běnzi.", "meaningVi": "Xin lấy vở của bạn ra."}],
    "hsk2_009": [{"chinese": "这个西瓜比那个大。", "pinyin": "Zhège xīguā bǐ nàge dà.", "meaningVi": "Quả dưa hấu này to hơn quả kia."}],
    "hsk2_010": [{"chinese": "请借我一支笔。", "pinyin": "Qǐng jiè wǒ yì zhī bǐ.", "meaningVi": "Xin cho tôi mượn một cây bút."}],
    "hsk2_011": [{"chinese": "别在这里抽烟。", "pinyin": "Bié zài zhèlǐ chōuyān.", "meaningVi": "Đừng hút thuốc ở đây."}],
    "hsk2_012": [{"chinese": "这家餐厅的菜味道不错。", "pinyin": "Zhè jiā cāntīng de cài wèidao búcuò.", "meaningVi": "Món ăn của nhà hàng này khá ngon."}],
    "hsk2_013": [{"chinese": "不好意思，我来晚了。", "pinyin": "Bù hǎoyìsi, wǒ lái wǎn le.", "meaningVi": "Xin lỗi, tôi đến muộn rồi."}],
    "hsk2_016": [{"chinese": "请出示证件。", "pinyin": "Qǐng chūshì zhèngjiàn.", "meaningVi": "Xin xuất trình giấy tờ."}],
    "hsk2_017": [{"chinese": "他打算明年出国留学。", "pinyin": "Tā dǎsuàn míngnián chūguó liúxué.", "meaningVi": "Anh ấy dự định sang năm ra nước ngoài du học."}],
    "hsk2_018": [{"chinese": "请你出来一下。", "pinyin": "Qǐng nǐ chūlái yíxià.", "meaningVi": "Xin bạn ra ngoài một chút."}],
    "hsk2_019": [{"chinese": "他每天七点出门上班。", "pinyin": "Tā měitiān qī diǎn chūmén shàngbān.", "meaningVi": "Mỗi ngày anh ấy bảy giờ ra khỏi nhà đi làm."}],
    "hsk2_020": [{"chinese": "外面下雨了，先别出去。", "pinyin": "Wàimiàn xiàyǔ le, xiān bié chūqù.", "meaningVi": "Bên ngoài trời mưa rồi, tạm thời đừng ra ngoài."}],
    "hsk2_022": [{"chinese": "请查一下这个词的读音。", "pinyin": "Qǐng chá yíxià zhège cí de dúyīn.", "meaningVi": "Xin tra cách đọc của từ này."}],
    "hsk2_023": [{"chinese": "这是我第一次来北京。", "pinyin": "Zhè shì wǒ dì-yī cì lái Běijīng.", "meaningVi": "Đây là lần đầu tiên tôi đến Bắc Kinh."}],
    "hsk2_024": [{"chinese": "他从上海来。", "pinyin": "Tā cóng Shànghǎi lái.", "meaningVi": "Anh ấy đến từ Thượng Hải."}],
    "hsk2_025": [{"chinese": "她从小就喜欢唱歌。", "pinyin": "Tā cóngxiǎo jiù xǐhuan chànggē.", "meaningVi": "Cô ấy từ nhỏ đã thích hát."}],
    "hsk2_026": [{"chinese": "这道题你做错了。", "pinyin": "Zhè dào tí nǐ zuòcuò le.", "meaningVi": "Bài này bạn làm sai rồi."}],
    "hsk2_027": [{"chinese": "请打电话告诉我。", "pinyin": "Qǐng dǎ diànhuà gàosu wǒ.", "meaningVi": "Xin gọi điện báo cho tôi."}],
    "hsk2_028": [{"chinese": "下雨了，我们打车去吧。", "pinyin": "Xiàyǔ le, wǒmen dǎchē qù ba.", "meaningVi": "Trời mưa rồi, chúng ta đi taxi đi."}],
    "hsk2_029": [{"chinese": "请打开窗户。", "pinyin": "Qǐng dǎkāi chuānghu.", "meaningVi": "Xin mở cửa sổ."}],
    "hsk2_030": [{"chinese": "房间不大，但很干净。", "pinyin": "Fángjiān bú dà, dàn hěn gānjìng.", "meaningVi": "Phòng không lớn, nhưng rất sạch sẽ."}],
    "hsk2_031": [{"chinese": "他很努力，但是成绩不太好。", "pinyin": "Tā hěn nǔlì, dànshì chéngjì bú tài hǎo.", "meaningVi": "Anh ấy rất chăm chỉ, nhưng thành tích không tốt lắm."}],
    "hsk2_034": [{"chinese": "请在门口等我。", "pinyin": "Qǐng zài ménkǒu děng wǒ.", "meaningVi": "Xin đợi tôi ở cửa."}],
    "hsk2_035": [{"chinese": "我每天坐地铁上班。", "pinyin": "Wǒ měitiān zuò dìtiě shàngbān.", "meaningVi": "Mỗi ngày tôi đi tàu điện ngầm đi làm."}],
    "hsk2_036": [{"chinese": "我想点一杯咖啡。", "pinyin": "Wǒ xiǎng diǎn yì bēi kāfēi.", "meaningVi": "Tôi muốn gọi một ly cà phê."}],
    "hsk2_038": [{"chinese": "请不要动。", "pinyin": "Qǐng búyào dòng.", "meaningVi": "Xin đừng cử động."}],
    "hsk2_039": [{"chinese": "我们去那家饭馆吃饭吧。", "pinyin": "Wǒmen qù nà jiā fànguǎn chīfàn ba.", "meaningVi": "Chúng ta đi ăn ở nhà hàng đó đi."}],
    "hsk2_041": [{"chinese": "他个子很高。", "pinyin": "Tā gèzi hěn gāo.", "meaningVi": "Anh ấy vóc dáng rất cao."}],
    "hsk2_042": [{"chinese": "我妹妹在读高中。", "pinyin": "Wǒ mèimei zài dú gāozhōng.", "meaningVi": "Em gái tôi đang học cấp ba."}],
    "hsk2_043": [{"chinese": "请把这个好消息告诉大家。", "pinyin": "Qǐng bǎ zhège hǎo xiāoxi gàosu dàjiā.", "meaningVi": "Xin báo tin vui này cho mọi người."}],
    "hsk2_044": [{"chinese": "他的个子长高了不少。", "pinyin": "Tā de gèzi zhǎnggāole bù shǎo.", "meaningVi": "Vóc dáng của anh ấy đã cao lên nhiều."}],
    "hsk2_045": [{"chinese": "我跟他一起去超市。", "pinyin": "Wǒ gēn tā yìqǐ qù chāoshì.", "meaningVi": "Tôi cùng anh ấy đi siêu thị."}],
    "hsk2_048": [{"chinese": "老师叫我过来一趟。", "pinyin": "Lǎoshī jiào wǒ guòlái yí tàng.", "meaningVi": "Giáo viên gọi tôi đến một chuyến."}],
    "hsk2_049": [{"chinese": "每年过年我们都回老家。", "pinyin": "Měi nián guònián wǒmen dōu huí lǎojiā.", "meaningVi": "Mỗi năm Tết đến chúng tôi đều về quê."}],
    "hsk2_050": [{"chinese": "那件事已经过去了。", "pinyin": "Nà jiàn shì yǐjīng guòqù le.", "meaningVi": "Việc đó đã qua rồi."}],
    "hsk2_052": [{"chinese": "你要喝茶还是喝咖啡？", "pinyin": "Nǐ yào hē chá háishi hē kāfēi?", "meaningVi": "Bạn muốn uống trà hay uống cà phê?"}],
    "hsk2_056": [{"chinese": "他坐在我后面。", "pinyin": "Tā zuò zài wǒ hòumiàn.", "meaningVi": "Anh ấy ngồi ở phía sau tôi."}],
    "hsk2_059": [{"chinese": "她画了一幅山水画。", "pinyin": "Tā huàle yì fú shānshuǐhuà.", "meaningVi": "Cô ấy đã vẽ một bức tranh sơn thủy."}],
    "hsk2_060": [{"chinese": "我的手机坏了。", "pinyin": "Wǒ de shǒujī huài le.", "meaningVi": "Điện thoại của tôi bị hỏng rồi."}],
    "hsk2_061": [{"chinese": "他晚上八点才回来。", "pinyin": "Tā wǎnshang bā diǎn cái huílái.", "meaningVi": "Anh ấy đến tám giờ tối mới về."}],
    "hsk2_062": [{"chinese": "天晚了，我该回去了。", "pinyin": "Tiān wǎn le, wǒ gāi huíqù le.", "meaningVi": "Trời tối rồi, tôi phải về thôi."}],
    "hsk2_065": [{"chinese": "你还记得他的名字吗？", "pinyin": "Nǐ hái jìde tā de míngzi ma?", "meaningVi": "Bạn còn nhớ tên của anh ấy không?"}],
    "hsk2_066": [{"chinese": "这间屋子很宽敞。", "pinyin": "Zhè jiān wūzi hěn kuānchang.", "meaningVi": "Căn phòng này rất rộng rãi."}],
    "hsk2_068": [{"chinese": "学生们都在教室里上课。", "pinyin": "Xuéshengmen dōu zài jiàoshì lǐ shàngkè.", "meaningVi": "Các học sinh đều đang học trong lớp học."}],
    "hsk2_070": [{"chinese": "请进。", "pinyin": "Qǐng jìn.", "meaningVi": "Mời vào."}],
    "hsk2_072": [{"chinese": "外面很冷，快进来吧。", "pinyin": "Wàimiàn hěn lěng, kuài jìnlái ba.", "meaningVi": "Bên ngoài rất lạnh, mau vào đây đi."}],
    "hsk2_073": [{"chinese": "门开着，你可以进去。", "pinyin": "Mén kāizhe, nǐ kěyǐ jìnqù.", "meaningVi": "Cửa đang mở, bạn có thể vào trong."}],
    "hsk2_074": [{"chinese": "他经常忘记带钥匙。", "pinyin": "Tā jīngcháng wàngjì dài yàoshi.", "meaningVi": "Anh ấy thường xuyên quên mang chìa khóa."}],
    "hsk2_076": [{"chinese": "我马上就到。", "pinyin": "Wǒ mǎshàng jiù dào.", "meaningVi": "Tôi sẽ đến ngay."}],
    "hsk2_078": [{"chinese": "电影几点开始？", "pinyin": "Diànyǐng jǐ diǎn kāishǐ?", "meaningVi": "Phim mấy giờ bắt đầu?"}],
    "hsk2_079": [{"chinese": "学校下周一开学。", "pinyin": "Xuéxiào xià zhōuyī kāixué.", "meaningVi": "Trường học khai giảng vào thứ hai tuần sau."}],
    "hsk2_080": [{"chinese": "明天要考数学。", "pinyin": "Míngtiān yào kǎo shùxué.", "meaningVi": "Ngày mai phải thi toán."}],
    "hsk2_081": [{"chinese": "这次考试很难。", "pinyin": "Zhè cì kǎoshì hěn nán.", "meaningVi": "Kỳ thi lần này rất khó."}],
    "hsk2_082": [{"chinese": "明天可能会下雪。", "pinyin": "Míngtiān kěnéng huì xiàxuě.", "meaningVi": "Ngày mai có thể sẽ có tuyết."}],
    "hsk2_084": [{"chinese": "请开快一点。", "pinyin": "Qǐng kāi kuài yìdiǎn.", "meaningVi": "Xin lái nhanh một chút."}],
    "hsk2_085": [{"chinese": "他每天都过得很快乐。", "pinyin": "Tā měitiān dōu guò de hěn kuàilè.", "meaningVi": "Mỗi ngày anh ấy đều sống rất vui vẻ."}],
    "hsk2_086": [{"chinese": "火车快要到站了。", "pinyin": "Huǒchē kuàiyào dào zhàn le.", "meaningVi": "Tàu hỏa sắp đến ga rồi."}],
    "hsk2_088": [{"chinese": "今天工作了一天，很累。", "pinyin": "Jīntiān gōngzuòle yì tiān, hěn lèi.", "meaningVi": "Hôm nay làm việc cả ngày, rất mệt."}],
    "hsk2_090": [{"chinese": "箱子里面装满了衣服。", "pinyin": "Xiāngzi lǐmiàn zhuāngmǎnle yīfu.", "meaningVi": "Bên trong hộp đầy quần áo."}],
    "hsk2_091": [{"chinese": "我家住在五楼。", "pinyin": "Wǒ jiā zhù zài wǔ lóu.", "meaningVi": "Nhà tôi ở tầng năm."}],
    "hsk2_092": [{"chinese": "这条路很宽。", "pinyin": "Zhè tiáo lù hěn kuān.", "meaningVi": "Con đường này rất rộng."}],
    "hsk2_093": [{"chinese": "路上小心一点。", "pinyin": "Lùshang xiǎoxīn yìdiǎn.", "meaningVi": "Trên đường cẩn thận một chút."}],
    "hsk2_096": [{"chinese": "她喜欢绿色的衣服。", "pinyin": "Tā xǐhuan lǜsè de yīfu.", "meaningVi": "Cô ấy thích quần áo màu xanh lá."}],
    "hsk2_097": [{"chinese": "请说得慢一点。", "pinyin": "Qǐng shuō de màn yìdiǎn.", "meaningVi": "Xin nói chậm một chút."}],
    "hsk2_098": [{"chinese": "这部电影一点儿也没意思。", "pinyin": "Zhè bù diànyǐng yìdiǎnr yě méi yìsi.", "meaningVi": "Bộ phim này chẳng thú vị chút nào."}],
    "hsk2_099": [{"chinese": "他每天早上跑步。", "pinyin": "Tā měitiān zǎoshang pǎobù.", "meaningVi": "Mỗi sáng anh ấy đều chạy bộ."}],
    "hsk2_100": [{"chinese": "请把门关好。", "pinyin": "Qǐng bǎ mén guān hǎo.", "meaningVi": "Xin đóng cửa cho kỹ."}],
    "hsk2_101": [{"chinese": "我们在门口见面吧。", "pinyin": "Wǒmen zài ménkǒu jiànmiàn ba.", "meaningVi": "Chúng ta gặp nhau ở cửa ra vào nhé."}],
    "hsk2_102": [{"chinese": "这个景点的门票不贵。", "pinyin": "Zhège jǐngdiǎn de ménpiào bú guì.", "meaningVi": "Vé vào cửa khu du lịch này không đắt."}],
    "hsk2_103": [{"chinese": "他把信的正面写好了地址。", "pinyin": "Tā bǎ xìn de zhèngmiàn xiěhǎole dìzhǐ.", "meaningVi": "Anh ấy đã viết địa chỉ ở mặt trước của bức thư."}],
    "hsk2_104": [{"chinese": "这次比赛有一百多名选手参加。", "pinyin": "Zhè cì bǐsài yǒu yìbǎi duō míng xuǎnshǒu cānjiā.", "meaningVi": "Cuộc thi lần này có hơn một trăm vận động viên tham gia."}],
    "hsk2_105": [{"chinese": "请帮我拿一下书。", "pinyin": "Qǐng bāng wǒ ná yíxià shū.", "meaningVi": "Xin giúp tôi cầm quyển sách."}],
    "hsk2_106": [{"chinese": "天气那么冷，多穿点衣服。", "pinyin": "Tiānqì nàme lěng, duō chuān diǎn yīfu.", "meaningVi": "Thời tiết lạnh như vậy, mặc thêm quần áo đi."}],
    "hsk2_107": [{"chinese": "别那样说话。", "pinyin": "Bié nàyàng shuōhuà.", "meaningVi": "Đừng nói chuyện như thế."}],
    "hsk2_110": [{"chinese": "那个男孩儿很聪明。", "pinyin": "Nàge nánháir hěn cōngming.", "meaningVi": "Cậu bé đó rất thông minh."}],
    "hsk2_112": [{"chinese": "这个女孩儿很可爱。", "pinyin": "Zhège nǚháir hěn kě'ài.", "meaningVi": "Cô bé này rất dễ thương."}],
    "hsk2_113": [{"chinese": "我家旁边有一个公园。", "pinyin": "Wǒ jiā pángbiān yǒu yí gè gōngyuán.", "meaningVi": "Bên cạnh nhà tôi có một công viên."}],
    "hsk2_116": [{"chinese": "他把票放进了口袋。", "pinyin": "Tā bǎ piào fàngjìnle kǒudai.", "meaningVi": "Anh ấy đã bỏ vé vào túi."}],
    "hsk2_118": [{"chinese": "请大家都站起来。", "pinyin": "Qǐng dàjiā dōu zhàn qǐlái.", "meaningVi": "Xin mọi người đứng dậy."}],
    "hsk2_119": [{"chinese": "前面那栋楼是图书馆。", "pinyin": "Qiánmiàn nà dòng lóu shì túshūguǎn.", "meaningVi": "Tòa nhà phía trước là thư viện."}],
    "hsk2_120": [{"chinese": "今天是晴天。", "pinyin": "Jīntiān shì qíngtiān.", "meaningVi": "Hôm nay trời quang."}],
    "hsk2_121": [{"chinese": "他喜欢打球。", "pinyin": "Tā xǐhuan dǎqiú.", "meaningVi": "Anh ấy thích chơi bóng."}],
    "hsk2_122": [{"chinese": "妈妈让我早点回家。", "pinyin": "Māma ràng wǒ zǎodiǎn huíjiā.", "meaningVi": "Mẹ bảo tôi về nhà sớm hơn."}],
    "hsk2_124": [{"chinese": "周末我们去商场买东西吧。", "pinyin": "Zhōumò wǒmen qù shāngchǎng mǎi dōngxi ba.", "meaningVi": "Cuối tuần chúng ta đi trung tâm thương mại mua đồ đi."}],
    "hsk2_125": [{"chinese": "运动员们陆续上来领奖。", "pinyin": "Yùndòngyuánmen lùxù shànglái lǐngjiǎng.", "meaningVi": "Các vận động viên lần lượt lên đây nhận giải."}],
    "hsk2_126": [{"chinese": "桌子上面放着一本书。", "pinyin": "Zhuōzi shàngmiàn fàngzhe yì běn shū.", "meaningVi": "Trên mặt bàn đặt một quyển sách."}],
    "hsk2_127": [{"chinese": "电梯坏了，我们走上去吧。", "pinyin": "Diàntī huài le, wǒmen zǒu shàngqù ba.", "meaningVi": "Thang máy hỏng rồi, chúng ta đi bộ lên đi."}],
    "hsk2_128": [{"chinese": "我每天晚上都上网查资料。", "pinyin": "Wǒ měitiān wǎnshang dōu shàngwǎng chá zīliào.", "meaningVi": "Mỗi tối tôi đều lên mạng tra tài liệu."}],
    "hsk2_129": [{"chinese": "祝您身体健康。", "pinyin": "Zhù nín shēntǐ jiànkāng.", "meaningVi": "Chúc bác sức khỏe dồi dào."}],
    "hsk2_131": [{"chinese": "他年轻时去过很多国家。", "pinyin": "Tā niánqīng shí qùguò hěn duō guójiā.", "meaningVi": "Khi còn trẻ anh ấy đã đến nhiều quốc gia."}],
    "hsk2_132": [{"chinese": "我有点事情要跟你说。", "pinyin": "Wǒ yǒudiǎn shìqing yào gēn nǐ shuō.", "meaningVi": "Tôi có chút việc muốn nói với bạn."}],
    "hsk2_133": [{"chinese": "请举手回答问题。", "pinyin": "Qǐng jǔshǒu huídá wèntí.", "meaningVi": "Xin giơ tay trả lời câu hỏi."}],
    "hsk2_135": [{"chinese": "他的书包很重。", "pinyin": "Tā de shūbāo hěn zhòng.", "meaningVi": "Cặp sách của anh ấy rất nặng."}],
    "hsk2_136": [{"chinese": "今天感觉不太舒服。", "pinyin": "Jīntiān gǎnjué bú tài shūfu.", "meaningVi": "Hôm nay cảm thấy không được khỏe lắm."}],
    "hsk2_137": [{"chinese": "我送你回家吧。", "pinyin": "Wǒ sòng nǐ huíjiā ba.", "meaningVi": "Để tôi đưa bạn về nhà nhé."}],
    "hsk2_138": [{"chinese": "虽然下雨，但他还是来了。", "pinyin": "Suīrán xiàyǔ, dàn tā háishi lái le.", "meaningVi": "Mặc dù trời mưa, nhưng anh ấy vẫn đến."}],
    "hsk2_139": [{"chinese": "因为下雨，所以我们没有出门。", "pinyin": "Yīnwèi xiàyǔ, suǒyǐ wǒmen méiyǒu chūmén.", "meaningVi": "Vì trời mưa, nên chúng tôi không ra ngoài."}],
    "hsk2_140": [{"chinese": "她的头疼得厉害。", "pinyin": "Tā de tóu téng de lìhai.", "meaningVi": "Đầu cô ấy đau dữ dội."}],
    "hsk2_141": [{"chinese": "他喜欢踢足球。", "pinyin": "Tā xǐhuan tī zúqiú.", "meaningVi": "Anh ấy thích đá bóng."}],
    "hsk2_142": [{"chinese": "这道题我不会做。", "pinyin": "Zhè dào tí wǒ bú huì zuò.", "meaningVi": "Bài này tôi không biết làm."}],
    "hsk2_143": [{"chinese": "桌子上有一条毛巾。", "pinyin": "Zhuōzi shàng yǒu yì tiáo máojīn.", "meaningVi": "Trên bàn có một chiếc khăn."}],
    "hsk2_144": [{"chinese": "她跳舞跳得很好看。", "pinyin": "Tā tiàowǔ tiào de hěn hǎokàn.", "meaningVi": "Cô ấy múa rất đẹp."}],
    "hsk2_146": [{"chinese": "他有很多外国朋友。", "pinyin": "Tā yǒu hěn duō wàiguó péngyou.", "meaningVi": "Anh ấy có nhiều bạn nước ngoài."}],
    "hsk2_147": [{"chinese": "外面在下雨。", "pinyin": "Wàimiàn zài xiàyǔ.", "meaningVi": "Bên ngoài đang mưa."}],
    "hsk2_148": [{"chinese": "我已经做完作业了。", "pinyin": "Wǒ yǐjīng zuòwán zuòyè le.", "meaningVi": "Tôi đã làm xong bài tập rồi."}],
    "hsk2_149": [{"chinese": "这辆车花了十万块钱。", "pinyin": "Zhè liàng chē huāle shí wàn kuài qián.", "meaningVi": "Chiếc xe này tốn mười vạn tệ."}],
    "hsk2_150": [{"chinese": "请往前走。", "pinyin": "Qǐng wǎng qián zǒu.", "meaningVi": "Xin đi về phía trước."}],
    "hsk2_151": [{"chinese": "我在网上买了一双鞋。", "pinyin": "Wǒ zài wǎngshang mǎile yì shuāng xié.", "meaningVi": "Tôi đã mua một đôi giày trên mạng."}],
    "hsk2_154": [{"chinese": "你为什么不高兴？", "pinyin": "Nǐ wèi shénme bù gāoxìng?", "meaningVi": "Tại sao bạn không vui?"}],
    "hsk2_155": [{"chinese": "我希望明天是晴天。", "pinyin": "Wǒ xīwàng míngtiān shì qíngtiān.", "meaningVi": "Tôi hy vọng ngày mai trời quang."}],
    "hsk2_156": [{"chinese": "吃饭前要洗手。", "pinyin": "Chīfàn qián yào xǐshǒu.", "meaningVi": "Trước khi ăn cơm phải rửa tay."}],
    "hsk2_157": [{"chinese": "请问洗手间在哪儿？", "pinyin": "Qǐngwèn xǐshǒujiān zài nǎr?", "meaningVi": "Xin hỏi nhà vệ sinh ở đâu?"}],
    "hsk2_158": [{"chinese": "请你从楼上下来。", "pinyin": "Qǐng nǐ cóng lóushàng xiàlái.", "meaningVi": "Xin bạn từ trên lầu xuống đây."}],
    "hsk2_159": [{"chinese": "床下面有一双拖鞋。", "pinyin": "Chuáng xiàmiàn yǒu yì shuāng tuōxié.", "meaningVi": "Dưới gầm giường có một đôi dép."}],
    "hsk2_160": [{"chinese": "楼梯很滑，慢慢下去。", "pinyin": "Lóutī hěn huá, mànmàn xiàqù.", "meaningVi": "Cầu thang trơn lắm, từ từ đi xuống."}],
    "hsk2_161": [{"chinese": "这个小孩儿特别活泼。", "pinyin": "Zhège xiǎoháir tèbié huópō.", "meaningVi": "Đứa trẻ này đặc biệt hiếu động."}],
    "hsk2_162": [{"chinese": "我小时候住在乡下。", "pinyin": "Wǒ xiǎoshíhou zhù zài xiāngxià.", "meaningVi": "Lúc nhỏ tôi sống ở nông thôn."}],
    "hsk2_164": [{"chinese": "我姓王。", "pinyin": "Wǒ xìng Wáng.", "meaningVi": "Tôi họ Vương."}],
    "hsk2_165": [{"chinese": "请填写您的姓名。", "pinyin": "Qǐng tiánxiě nín de xìngmíng.", "meaningVi": "Xin điền họ tên của quý khách."}],
    "hsk2_167": [{"chinese": "她的眼睛又大又亮。", "pinyin": "Tā de yǎnjing yòu dà yòu liàng.", "meaningVi": "Đôi mắt của cô ấy vừa to vừa sáng."}],
    "hsk2_169": [{"chinese": "药店就在医院对面。", "pinyin": "Yàodiàn jiù zài yīyuàn duìmiàn.", "meaningVi": "Hiệu thuốc ở ngay đối diện bệnh viện."}],
    "hsk2_171": [{"chinese": "请稍等一会儿。", "pinyin": "Qǐng shāo děng yíhuìr.", "meaningVi": "Xin chờ một lát."}],
    "hsk2_172": [{"chinese": "他已经走了。", "pinyin": "Tā yǐjīng zǒu le.", "meaningVi": "Anh ấy đã đi rồi."}],
    "hsk2_173": [{"chinese": "我们一起做作业吧。", "pinyin": "Wǒmen yìqǐ zuò zuòyè ba.", "meaningVi": "Chúng ta cùng làm bài tập đi."}],
    "hsk2_174": [{"chinese": "这句话是什么意思？", "pinyin": "Zhè jù huà shì shénme yìsi?", "meaningVi": "Câu này có nghĩa là gì?"}],
    "hsk2_175": [{"chinese": "今天天气阴阴的。", "pinyin": "Jīntiān tiānqì yīnyīn de.", "meaningVi": "Hôm nay trời âm u."}],
    "hsk2_176": [{"chinese": "因为堵车，他迟到了。", "pinyin": "Yīnwèi dǔchē, tā chídào le.", "meaningVi": "Vì kẹt xe nên anh ấy đã đến muộn."}],
    "hsk2_177": [{"chinese": "他游得很快。", "pinyin": "Tā yóu de hěn kuài.", "meaningVi": "Anh ấy bơi rất nhanh."}],
    "hsk2_178": [{"chinese": "夏天我常常去游泳。", "pinyin": "Xiàtiān wǒ chángcháng qù yóuyǒng.", "meaningVi": "Mùa hè tôi thường xuyên đi bơi."}],
    "hsk2_179": [{"chinese": "这本书很有意思。", "pinyin": "Zhè běn shū hěn yǒu yìsi.", "meaningVi": "Cuốn sách này rất thú vị."}],
    "hsk2_180": [{"chinese": "他有时会来找我聊天。", "pinyin": "Tā yǒushí huì lái zhǎo wǒ liáotiān.", "meaningVi": "Thỉnh thoảng anh ấy sẽ đến tìm tôi trò chuyện."}],
    "hsk2_181": [{"chinese": "请往右转。", "pinyin": "Qǐng wǎng yòu zhuǎn.", "meaningVi": "Xin rẽ phải."}],
    "hsk2_182": [{"chinese": "银行在超市的右边。", "pinyin": "Yínháng zài chāoshì de yòubian.", "meaningVi": "Ngân hàng ở bên phải siêu thị."}],
    "hsk2_185": [{"chinese": "医生建议他多做运动。", "pinyin": "Yīshēng jiànyì tā duō zuò yùndòng.", "meaningVi": "Bác sĩ khuyên anh ấy nên vận động nhiều hơn."}],
    "hsk2_186": [{"chinese": "请在这里站好。", "pinyin": "Qǐng zài zhèlǐ zhàn hǎo.", "meaningVi": "Xin đứng ngay ngắn ở đây."}],
    "hsk2_188": [{"chinese": "你怎么这么晚才来？", "pinyin": "Nǐ zěnme zhème wǎn cái lái?", "meaningVi": "Sao bạn đến muộn thế này?"}],
    "hsk2_189": [{"chinese": "事情不是这样的。", "pinyin": "Shìqing bú shì zhèyàng de.", "meaningVi": "Sự việc không phải như thế này."}],
    "hsk2_191": [{"chinese": "他正忙着写报告。", "pinyin": "Tā zhèng mángzhe xiě bàogào.", "meaningVi": "Anh ấy đang bận viết báo cáo."}],
    "hsk2_192": [{"chinese": "这周我很忙。", "pinyin": "Zhè zhōu wǒ hěn máng.", "meaningVi": "Tuần này tôi rất bận."}],
    "hsk2_193": [{"chinese": "我在准备明天的考试。", "pinyin": "Wǒ zài zhǔnbèi míngtiān de kǎoshì.", "meaningVi": "Tôi đang chuẩn bị cho kỳ thi ngày mai."}],
    "hsk2_194": [{"chinese": "这件事要靠自己解决。", "pinyin": "Zhè jiàn shì yào kào zìjǐ jiějué.", "meaningVi": "Việc này phải dựa vào bản thân để giải quyết."}],
    "hsk2_195": [{"chinese": "他一句话没说就走了。", "pinyin": "Tā yí jù huà méi shuō jiù zǒu le.", "meaningVi": "Anh ấy chẳng nói câu nào đã đi mất."}],
    "hsk2_196": [{"chinese": "我每天走路上班。", "pinyin": "Wǒ měitiān zǒulù shàngbān.", "meaningVi": "Mỗi ngày tôi đi bộ đi làm."}],
    "hsk2_198": [{"chinese": "这是我最喜欢的一本书。", "pinyin": "Zhè shì wǒ zuì xǐhuan de yì běn shū.", "meaningVi": "Đây là cuốn sách tôi thích nhất."}],
    "hsk2_199": [{"chinese": "请往左看。", "pinyin": "Qǐng wǎng zuǒ kàn.", "meaningVi": "Xin nhìn sang bên trái."}],
    "hsk2_200": [{"chinese": "教室在图书馆的左边。", "pinyin": "Jiàoshì zài túshūguǎn de zuǒbian.", "meaningVi": "Lớp học ở bên trái thư viện."}],
    "hsk3_006": [{"chinese": "请把门关上。", "pinyin": "Qǐng bǎ mén guānshàng.", "meaningVi": "Xin đóng cửa lại."}],
    "hsk3_021": [{"chinese": "这两种方法比较一下就知道了。", "pinyin": "Zhè liǎng zhǒng fāngfǎ bǐjiào yíxià jiù zhīdào le.", "meaningVi": "So sánh hai phương pháp này một chút là biết."}],
    "hsk3_024": [{"chinese": "今天下午有一场足球比赛。", "pinyin": "Jīntiān xiàwǔ yǒu yì chǎng zúqiú bǐsài.", "meaningVi": "Chiều nay có một trận thi đấu bóng đá."}],
    "hsk3_029": [{"chinese": "这个城市的变化真大。", "pinyin": "Zhège chéngshì de biànhuà zhēn dà.", "meaningVi": "Sự thay đổi của thành phố này thật lớn."}],
    "hsk3_034": [{"chinese": "杯子里放了几块冰。", "pinyin": "Bēizi lǐ fàngle jǐ kuài bīng.", "meaningVi": "Trong cốc để vài viên đá."}],
    "hsk3_043": [{"chinese": "今天不行，我有事。", "pinyin": "Jīntiān bùxíng, wǒ yǒu shì.", "meaningVi": "Hôm nay không được, tôi có việc."}],
    "hsk3_051": [{"chinese": "现在差五分三点。", "pinyin": "Xiànzài chà wǔ fēn sān diǎn.", "meaningVi": "Bây giờ còn năm phút nữa là ba giờ."}],
    "hsk3_052": [{"chinese": "我们俩年龄差不多。", "pinyin": "Wǒmen liǎ niánlíng chàbuduō.", "meaningVi": "Tuổi của hai chúng tôi xấp xỉ nhau."}],
    "hsk3_072": [{"chinese": "你暑假打算去哪儿玩？", "pinyin": "Nǐ shǔjià dǎsuàn qù nǎr wán?", "meaningVi": "Nghỉ hè bạn dự định đi đâu chơi?"}],
    "hsk3_073": [{"chinese": "大概需要一个小时。", "pinyin": "Dàgài xūyào yí gè xiǎoshí.", "meaningVi": "Có lẽ cần khoảng một tiếng đồng hồ."}],
    "hsk3_078": [{"chinese": "出门记得带伞。", "pinyin": "Chūmén jìde dài sǎn.", "meaningVi": "Ra ngoài nhớ mang theo ô."}],
    "hsk3_085": [{"chinese": "他在比赛中得分很高。", "pinyin": "Tā zài bǐsài zhōng défēn hěn gāo.", "meaningVi": "Anh ấy ghi điểm rất cao trong trận đấu."}],
    "hsk3_093": [{"chinese": "昨天晚上停电了。", "pinyin": "Zuótiān wǎnshang tíngdiàn le.", "meaningVi": "Tối qua bị mất điện."}],
    "hsk3_114": [{"chinese": "请把这份文件发给他。", "pinyin": "Qǐng bǎ zhè fèn wénjiàn fā gěi tā.", "meaningVi": "Xin gửi tài liệu này cho anh ấy."}],
    "hsk3_130": [{"chinese": "她收到了一封信。", "pinyin": "Tā shōudàole yì fēng xìn.", "meaningVi": "Cô ấy đã nhận được một lá thư."}],
    "hsk3_139": [{"chinese": "他这几天感冒了。", "pinyin": "Tā zhè jǐ tiān gǎnmào le.", "meaningVi": "Mấy ngày nay anh ấy bị cảm cúm."}],
    "hsk3_145": [{"chinese": "请根据实际情况回答。", "pinyin": "Qǐng gēnjù shíjì qíngkuàng huídá.", "meaningVi": "Xin trả lời dựa theo tình hình thực tế."}],
    "hsk3_152": [{"chinese": "请把电视关了。", "pinyin": "Qǐng bǎ diànshì guān le.", "meaningVi": "Xin tắt tivi đi."}],
    "hsk3_154": [{"chinese": "他们两个人关系很好。", "pinyin": "Tāmen liǎng gè rén guānxì hěn hǎo.", "meaningVi": "Quan hệ giữa hai người họ rất tốt."}],
    "hsk3_160": [{"chinese": "请你把这本书拿过去。", "pinyin": "Qǐng nǐ bǎ zhè běn shū ná guòqù.", "meaningVi": "Xin bạn cầm quyển sách này đi qua đó."}],
    "hsk3_165": [{"chinese": "他好像很累的样子。", "pinyin": "Tā hǎoxiàng hěn lèi de yàngzi.", "meaningVi": "Anh ấy có vẻ như rất mệt."}],
    "hsk3_183": [{"chinese": "他会说三种语言。", "pinyin": "Tā huì shuō sān zhǒng yǔyán.", "meaningVi": "Anh ấy biết nói ba loại ngôn ngữ."}],
    "hsk3_185": [{"chinese": "你可以选择红色或蓝色。", "pinyin": "Nǐ kěyǐ xuǎnzé hóngsè huò lánsè.", "meaningVi": "Bạn có thể chọn màu đỏ hoặc màu xanh."}],
    "hsk3_191": [{"chinese": "别急，慢慢说。", "pinyin": "Bié jí, mànmàn shuō.", "meaningVi": "Đừng vội, từ từ nói."}],
    "hsk3_204": [{"chinese": "桌子的角很尖。", "pinyin": "Zhuōzi de jiǎo hěn jiān.", "meaningVi": "Góc của cái bàn rất nhọn."}],
    "hsk3_208": [{"chinese": "明天有一节数学课。", "pinyin": "Míngtiān yǒu yì jié shùxué kè.", "meaningVi": "Ngày mai có một tiết toán."}],
    "hsk3_217": [{"chinese": "我们经过一条小河。", "pinyin": "Wǒmen jīngguò yì tiáo xiǎohé.", "meaningVi": "Chúng tôi đi qua một con sông nhỏ."}],
    "hsk3_224": [{"chinese": "他决定明天出发。", "pinyin": "Tā juédìng míngtiān chūfā.", "meaningVi": "Anh ấy quyết định ngày mai xuất phát."}],
    "hsk3_225": [{"chinese": "请刷卡付款。", "pinyin": "Qǐng shuākǎ fùkuǎn.", "meaningVi": "Xin quẹt thẻ thanh toán."}],
    "hsk3_231": [{"chinese": "这个办法可行。", "pinyin": "Zhège bànfǎ kě xíng.", "meaningVi": "Cách này khả thi."}],
    "hsk3_235": [{"chinese": "现在是九点一刻。", "pinyin": "Xiànzài shì jiǔ diǎn yí kè.", "meaningVi": "Bây giờ là chín giờ mười lăm phút."}],
    "hsk3_245": [{"chinese": "爷爷已经很老了。", "pinyin": "Yéye yǐjīng hěn lǎo le.", "meaningVi": "Ông nội đã rất già rồi."}],
    "hsk3_252": [{"chinese": "请多做几次练习。", "pinyin": "Qǐng duō zuò jǐ cì liànxí.", "meaningVi": "Xin làm thêm vài lần luyện tập."}],
    "hsk3_268": [{"chinese": "这件毛衣是纯毛的。", "pinyin": "Zhè jiàn máoyī shì chún máo de.", "meaningVi": "Chiếc áo len này làm từ lông thuần."}],
    "hsk3_269": [{"chinese": "这个房间大约二十平方米。", "pinyin": "Zhège fángjiān dàyuē èrshí píngfāngmǐ.", "meaningVi": "Căn phòng này khoảng hai mươi mét vuông."}],
    "hsk3_271": [{"chinese": "我终于明白他的意思了。", "pinyin": "Wǒ zhōngyú míngbai tā de yìsi le.", "meaningVi": "Cuối cùng tôi cũng hiểu ý của anh ấy."}],
    "hsk3_275": [{"chinese": "这道题真难。", "pinyin": "Zhè dào tí zhēn nán.", "meaningVi": "Bài này thật khó."}],
    "hsk3_285": [{"chinese": "草原上有一群牛。", "pinyin": "Cǎoyuán shàng yǒu yì qún niú.", "meaningVi": "Trên thảo nguyên có một đàn bò."}],
    "hsk3_286": [{"chinese": "他为了这次考试做了很多努力。", "pinyin": "Tā wèile zhè cì kǎoshì zuòle hěn duō nǔlì.", "meaningVi": "Anh ấy đã nỗ lực rất nhiều cho kỳ thi lần này."}],
    "hsk3_290": [{"chinese": "她很怕黑。", "pinyin": "Tā hěn pà hēi.", "meaningVi": "Cô ấy rất sợ bóng tối."}],
    "hsk3_301": [{"chinese": "他一早就起床锻炼了。", "pinyin": "Tā yìzǎo jiù qǐchuáng duànliàn le.", "meaningVi": "Anh ấy dậy sớm để tập thể dục."}],
    "hsk3_307": [{"chinese": "请说清楚一点。", "pinyin": "Qǐng shuō qīngchu yìdiǎn.", "meaningVi": "Xin nói rõ ràng một chút."}],
    "hsk3_328": [{"chinese": "门外传来一声巨响。", "pinyin": "Ménwài chuánlái yì shēng jùxiǎng.", "meaningVi": "Bên ngoài cửa vang lên một tiếng động lớn."}],
    "hsk3_329": [{"chinese": "他的生活过得很幸福。", "pinyin": "Tā de shēnghuó guò de hěn xìngfú.", "meaningVi": "Cuộc sống của anh ấy rất hạnh phúc."}],
    "hsk3_351": [{"chinese": "今天她穿得特别漂亮。", "pinyin": "Jīntiān tā chuān de tèbié piàoliang.", "meaningVi": "Hôm nay cô ấy mặc rất đẹp."}],
    "hsk3_358": [{"chinese": "这个主意挺好的。", "pinyin": "Zhège zhǔyi tǐng hǎo de.", "meaningVi": "Ý tưởng này khá hay."}],
    "hsk3_366": [{"chinese": "今天我们叫外卖吧。", "pinyin": "Jīntiān wǒmen jiào wàimài ba.", "meaningVi": "Hôm nay chúng ta gọi đồ ăn giao tận nơi đi."}],
    "hsk3_385": [{"chinese": "他已经习惯了这里的生活。", "pinyin": "Tā yǐjīng xíguànle zhèlǐ de shēnghuó.", "meaningVi": "Anh ấy đã quen với cuộc sống ở đây."}],
    "hsk3_394": [{"chinese": "他向经理请了假。", "pinyin": "Tā xiàng jīnglǐ qǐngle jià.", "meaningVi": "Anh ấy đã xin nghỉ phép với giám đốc."}],
    "hsk3_395": [{"chinese": "她长得很像她妈妈。", "pinyin": "Tā zhǎng de hěn xiàng tā māma.", "meaningVi": "Cô ấy trông rất giống mẹ mình."}],
    "hsk3_398": [{"chinese": "他做事一直很小心。", "pinyin": "Tā zuòshì yìzhí hěn xiǎoxīn.", "meaningVi": "Anh ấy làm việc luôn rất cẩn thận."}],
    "hsk3_406": [{"chinese": "我信你说的话。", "pinyin": "Wǒ xìn nǐ shuō de huà.", "meaningVi": "Tôi tin lời bạn nói."}],
    "hsk3_412": [{"chinese": "这件事需要你的帮助。", "pinyin": "Zhè jiàn shì xūyào nǐ de bāngzhù.", "meaningVi": "Việc này cần sự giúp đỡ của bạn."}],
    "hsk3_420": [{"chinese": "老师对我们要求很严格。", "pinyin": "Lǎoshī duì wǒmen yāoqiú hěn yángé.", "meaningVi": "Giáo viên yêu cầu chúng tôi rất nghiêm khắc."}],
    "hsk3_422": [{"chinese": "他一定会来的。", "pinyin": "Tā yídìng huì lái de.", "meaningVi": "Anh ấy chắc chắn sẽ đến."}],
    "hsk3_424": [{"chinese": "我们一块儿去公园吧。", "pinyin": "Wǒmen yíkuàir qù gōngyuán ba.", "meaningVi": "Chúng ta cùng nhau đi công viên đi."}],
    "hsk3_433": [{"chinese": "他一边吃饭一边看电视。", "pinyin": "Tā yìbiān chīfàn yìbiān kàn diànshì.", "meaningVi": "Anh ấy vừa ăn cơm vừa xem tivi."}],
    "hsk3_440": [{"chinese": "睡眠不足会影响健康。", "pinyin": "Shuìmián bùzú huì yǐngxiǎng jiànkāng.", "meaningVi": "Ngủ không đủ giấc sẽ ảnh hưởng đến sức khỏe."}],
    "hsk3_446": [{"chinese": "这本书跟历史有关。", "pinyin": "Zhè běn shū gēn lìshǐ yǒuguān.", "meaningVi": "Cuốn sách này có liên quan đến lịch sử."}],
    "hsk3_466": [{"chinese": "前面就是公交车站。", "pinyin": "Qiánmiàn jiùshì gōngjiāo chēzhàn.", "meaningVi": "Phía trước chính là trạm xe buýt."}],
    "hsk3_467": [{"chinese": "桌子上放着三张纸。", "pinyin": "Zhuōzi shàng fàngzhe sān zhāng zhǐ.", "meaningVi": "Trên bàn để ba tờ giấy."}],
    "hsk3_470": [{"chinese": "我们在这里照张相吧。", "pinyin": "Wǒmen zài zhèlǐ zhào zhāng xiàng ba.", "meaningVi": "Chúng ta chụp một tấm ảnh ở đây đi."}],
    "hsk3_478": [{"chinese": "我只是想问一下时间。", "pinyin": "Wǒ zhǐshì xiǎng wèn yíxià shíjiān.", "meaningVi": "Tôi chỉ là muốn hỏi giờ thôi."}],
    "hsk3_492": [{"chinese": "这是我的儿子。", "pinyin": "Zhè shì wǒ de érzi.", "meaningVi": "Đây là con trai của tôi."}],
    "hsk3_493": [{"chinese": "他做作业总是很认真。", "pinyin": "Tā zuò zuòyè zǒngshì hěn rènzhēn.", "meaningVi": "Anh ấy làm bài tập luôn luôn rất nghiêm túc."}],
    "hsk4_006": [{"chinese": "请按这个按钮。", "pinyin": "Qǐng àn zhège ànniǔ.", "meaningVi": "Xin nhấn nút này."}],
    "hsk4_013": [{"chinese": "你打球打得真棒！", "pinyin": "Nǐ dǎqiú dǎ de zhēn bàng!", "meaningVi": "Bạn chơi bóng giỏi thật đấy!"}],
    "hsk4_015": [{"chinese": "我保证按时完成任务。", "pinyin": "Wǒ bǎozhèng ànshí wánchéng rènwu.", "meaningVi": "Tôi cam kết hoàn thành nhiệm vụ đúng giờ."}],
    "hsk4_025": [{"chinese": "我本来打算今天出发。", "pinyin": "Wǒ běnlái dǎsuàn jīntiān chūfā.", "meaningVi": "Ban đầu tôi định hôm nay xuất phát."}],
    "hsk4_032": [{"chinese": "这个产品符合国家标准。", "pinyin": "Zhège chǎnpǐn fúhé guójiā biāozhǔn.", "meaningVi": "Sản phẩm này phù hợp với tiêu chuẩn quốc gia."}],
    "hsk4_033": [{"chinese": "他每天都戴着那块旧手表。", "pinyin": "Tā měitiān dōu dàizhe nà kuài jiù shǒubiǎo.", "meaningVi": "Anh ấy mỗi ngày đều đeo chiếc đồng hồ cũ đó."}],
    "hsk4_039": [{"chinese": "他工作认真，并取得了好成绩。", "pinyin": "Tā gōngzuò rènzhēn, bìng qǔdéle hǎo chéngjì.", "meaningVi": "Anh ấy làm việc nghiêm túc, và đạt được thành tích tốt."}],
    "hsk4_044": [{"chinese": "交通不便给他们带来了困扰。", "pinyin": "Jiāotōng búbiàn gěi tāmen dàiláile kùnrǎo.", "meaningVi": "Giao thông bất tiện đã gây phiền toái cho họ."}],
    "hsk4_045": [{"chinese": "他不断努力提高自己。", "pinyin": "Tā búduàn nǔlì tígāo zìjǐ.", "meaningVi": "Anh ấy không ngừng nỗ lực nâng cao bản thân."}],
    "hsk4_046": [{"chinese": "时间不够了，我们快点吧。", "pinyin": "Shíjiān búgòu le, wǒmen kuài diǎn ba.", "meaningVi": "Thời gian không đủ rồi, chúng ta nhanh lên đi."}],
    "hsk4_047": [{"chinese": "这个方法可行，不过有点麻烦。", "pinyin": "Zhège fāngfǎ kěxíng, búguò yǒudiǎn máfan.", "meaningVi": "Cách này khả thi, nhưng có hơi phiền phức."}],
    "hsk4_050": [{"chinese": "这部电影很感人。", "pinyin": "Zhè bù diànyǐng hěn gǎnrén.", "meaningVi": "Bộ phim này rất cảm động."}],
    "hsk4_054": [{"chinese": "他不光会说中文，还会说日语。", "pinyin": "Tā bùguāng huì shuō Zhōngwén, hái huì shuō Rìyǔ.", "meaningVi": "Anh ấy không chỉ biết nói tiếng Trung, mà còn biết nói tiếng Nhật."}],
    "hsk4_070": [{"chinese": "我差点儿忘了这件事。", "pinyin": "Wǒ chàdiǎnr wàngle zhè jiàn shì.", "meaningVi": "Tôi suýt nữa quên mất việc này."}],
    "hsk4_079": [{"chinese": "他的实验终于成功了。", "pinyin": "Tā de shíyàn zhōngyú chénggōng le.", "meaningVi": "Thí nghiệm của anh ấy cuối cùng đã thành công."}],
    "hsk4_089": [{"chinese": "请从这个出口离开。", "pinyin": "Qǐng cóng zhège chūkǒu líkāi.", "meaningVi": "Xin rời khỏi qua lối ra này."}],
    "hsk4_110": [{"chinese": "这份报告里有几处明显的错误。", "pinyin": "Zhè fèn bàogào lǐ yǒu jǐ chù míngxiǎn de cuòwù.", "meaningVi": "Trong bản báo cáo này có vài chỗ sai rõ ràng."}],
    "hsk4_138": [{"chinese": "我们的导游非常热情。", "pinyin": "Wǒmen de dǎoyóu fēicháng rèqíng.", "meaningVi": "Hướng dẫn viên của chúng tôi vô cùng nhiệt tình."}],
    "hsk4_140": [{"chinese": "这道数学题很复杂。", "pinyin": "Zhè dào shùxué tí hěn fùzá.", "meaningVi": "Bài toán này rất phức tạp."}],
    "hsk4_147": [{"chinese": "老师让我们在教室里等一下。", "pinyin": "Lǎoshī ràng wǒmen zài jiàoshì lǐ děng yíxià.", "meaningVi": "Giáo viên bảo chúng tôi đợi một chút trong lớp học."}],
    "hsk4_149": [{"chinese": "今天的气温比较低。", "pinyin": "Jīntiān de qìwēn bǐjiào dī.", "meaningVi": "Nhiệt độ hôm nay khá thấp."}],
    "hsk4_173": [{"chinese": "我们排队等公交车。", "pinyin": "Wǒmen páiduì děng gōngjiāochē.", "meaningVi": "Chúng tôi xếp hàng đợi xe buýt."}],
    "hsk4_179": [{"chinese": "我们一起吃了一顿火锅。", "pinyin": "Wǒmen yìqǐ chīle yí dùn huǒguō.", "meaningVi": "Chúng tôi cùng nhau ăn một bữa lẩu."}],
    "hsk4_189": [{"chinese": "请帮我翻译这句话。", "pinyin": "Qǐng bāng wǒ fānyì zhè jù huà.", "meaningVi": "Xin giúp tôi dịch câu này."}],
    "hsk4_190": [{"chinese": "别再问了，很烦。", "pinyin": "Bié zài wèn le, hěn fán.", "meaningVi": "Đừng hỏi nữa, phiền lắm."}],
    "hsk4_199": [{"chinese": "这次旅行花费不少。", "pinyin": "Zhè cì lǚxíng huāfèi bù shǎo.", "meaningVi": "Chuyến du lịch lần này tốn kém không ít."}],
    "hsk4_215": [{"chinese": "这个项目由他负责。", "pinyin": "Zhège xiàngmù yóu tā fùzé.", "meaningVi": "Dự án này do anh ấy phụ trách."}],
    "hsk4_225": [{"chinese": "这个故事让我很感动。", "pinyin": "Zhège gùshi ràng wǒ hěn gǎndòng.", "meaningVi": "Câu chuyện này khiến tôi rất cảm động."}],
    "hsk4_227": [{"chinese": "我感觉今天特别累。", "pinyin": "Wǒ gǎnjué jīntiān tèbié lèi.", "meaningVi": "Tôi cảm thấy hôm nay đặc biệt mệt."}],
    "hsk4_232": [{"chinese": "请谈谈你的感受。", "pinyin": "Qǐng tántan nǐ de gǎnshòu.", "meaningVi": "Xin chia sẻ cảm nhận của bạn."}],
    "hsk4_244": [{"chinese": "各位同学请注意。", "pinyin": "Gèwèi tóngxué qǐng zhùyì.", "meaningVi": "Các bạn học sinh xin chú ý."}],
    "hsk4_246": [{"chinese": "各个部门都要配合完成任务。", "pinyin": "Gègè bùmén dōu yào pèihé wánchéng rènwu.", "meaningVi": "Từng bộ phận đều phải phối hợp hoàn thành nhiệm vụ."}],
    "hsk4_260": [{"chinese": "这些钱够不够？", "pinyin": "Zhèxiē qián gòu bú gòu?", "meaningVi": "Số tiền này có đủ không?"}],
    "hsk4_269": [{"chinese": "这份合同的关键条款需要仔细阅读。", "pinyin": "Zhè fèn hétong de guānjiàn tiáokuǎn xūyào zǐxì yuèdú.", "meaningVi": "Điều khoản then chốt của bản hợp đồng này cần đọc kỹ."}],
    "hsk4_272": [{"chinese": "这件事不用你管。", "pinyin": "Zhè jiàn shì búyòng nǐ guǎn.", "meaningVi": "Việc này không cần bạn quản."}],
    "hsk4_274": [{"chinese": "屋子里光线很好。", "pinyin": "Wūzi lǐ guāngxiàn hěn hǎo.", "meaningVi": "Trong phòng ánh sáng rất tốt."}],
    "hsk4_275": [{"chinese": "车站里正在广播车次信息。", "pinyin": "Chēzhàn lǐ zhèngzài guǎngbō chēcì xìnxī.", "meaningVi": "Nhà ga đang phát thanh thông tin chuyến xe."}],
    "hsk4_278": [{"chinese": "学校有明确的规定。", "pinyin": "Xuéxiào yǒu míngquè de guīdìng.", "meaningVi": "Nhà trường có quy định rõ ràng."}],
    "hsk4_280": [{"chinese": "这是一场国际比赛。", "pinyin": "Zhè shì yì chǎng guójì bǐsài.", "meaningVi": "Đây là một cuộc thi đấu quốc tế."}],
    "hsk4_291": [{"chinese": "你要好好休息。", "pinyin": "Nǐ yào hǎohǎo xiūxi.", "meaningVi": "Bạn phải nghỉ ngơi cho đàng hoàng."}],
    "hsk4_305": [{"chinese": "我们应该支持环保事业。", "pinyin": "Wǒmen yīnggāi zhīchí huánbǎo shìyè.", "meaningVi": "Chúng ta nên ủng hộ sự nghiệp bảo vệ môi trường."}],
    "hsk4_308": [{"chinese": "他很快就给我回信了。", "pinyin": "Tā hěn kuài jiù gěi wǒ huíxìn le.", "meaningVi": "Anh ấy rất nhanh đã hồi âm cho tôi."}],
    "hsk4_311": [{"chinese": "他活到了九十岁。", "pinyin": "Tā huódàole jiǔshí suì.", "meaningVi": "Ông ấy đã sống đến chín mươi tuổi."}],
    "hsk4_312": [{"chinese": "学校举办了一场文化活动。", "pinyin": "Xuéxiào jǔbànle yì chǎng wénhuà huódòng.", "meaningVi": "Nhà trường đã tổ chức một hoạt động văn hóa."}],
    "hsk4_314": [{"chinese": "大家一起把火扑灭了。", "pinyin": "Dàjiā yìqǐ bǎ huǒ pūmiè le.", "meaningVi": "Mọi người cùng nhau dập tắt ngọn lửa."}],
    "hsk4_319": [{"chinese": "这些是最基本的知识。", "pinyin": "Zhèxiē shì zuì jīběn de zhīshi.", "meaningVi": "Đây là những kiến thức cơ bản nhất."}],
    "hsk4_322": [{"chinese": "听到这个消息，她非常激动。", "pinyin": "Tīngdào zhège xiāoxi, tā fēicháng jīdòng.", "meaningVi": "Nghe được tin này, cô ấy vô cùng phấn khích."}],
    "hsk4_325": [{"chinese": "医生及时赶到了现场。", "pinyin": "Yīshēng jíshí gǎndàole xiànchǎng.", "meaningVi": "Bác sĩ đã kịp thời đến hiện trường."}],
    "hsk4_327": [{"chinese": "他既聪明又努力。", "pinyin": "Tā jì cōngming yòu nǔlì.", "meaningVi": "Anh ấy vừa thông minh vừa chăm chỉ."}],
    "hsk4_329": [{"chinese": "我们的旅行计划改变了。", "pinyin": "Wǒmen de lǚxíng jìhuà gǎibiàn le.", "meaningVi": "Kế hoạch du lịch của chúng tôi đã thay đổi."}],
    "hsk4_354": [{"chinese": "我建议你多休息。", "pinyin": "Wǒ jiànyì nǐ duō xiūxi.", "meaningVi": "Tôi đề nghị bạn nghỉ ngơi nhiều hơn."}],
    "hsk4_356": [{"chinese": "明天将会下雨。", "pinyin": "Míngtiān jiāng huì xiàyǔ.", "meaningVi": "Ngày mai sẽ có mưa."}],
    "hsk4_359": [{"chinese": "他在比赛中获得了大奖。", "pinyin": "Tā zài bǐsài zhōng huòdéle dàjiǎng.", "meaningVi": "Anh ấy đã giành được giải lớn trong cuộc thi."}],
    "hsk4_367": [{"chinese": "请把作业交给老师。", "pinyin": "Qǐng bǎ zuòyè jiāo gěi lǎoshī.", "meaningVi": "Xin nộp bài tập cho giáo viên."}],
    "hsk4_368": [{"chinese": "父母为他感到骄傲。", "pinyin": "Fùmǔ wèi tā gǎndào jiāo'ào.", "meaningVi": "Cha mẹ cảm thấy tự hào về anh ấy."}],
    "hsk4_377": [{"chinese": "家庭教育非常重要。", "pinyin": "Jiātíng jiàoyù fēicháng zhòngyào.", "meaningVi": "Giáo dục gia đình vô cùng quan trọng."}],
    "hsk4_381": [{"chinese": "他先介绍了自己，接着开始讲课。", "pinyin": "Tā xiān jièshàole zìjǐ, jiēzhe kāishǐ jiǎngkè.", "meaningVi": "Anh ấy trước tiên tự giới thiệu, tiếp theo bắt đầu giảng bài."}],
    "hsk4_389": [{"chinese": "尽管很累，他还是坚持完成了工作。", "pinyin": "Jǐnguǎn hěn lèi, tā háishi jiānchí wánchéngle gōngzuò.", "meaningVi": "Dù rất mệt, anh ấy vẫn kiên trì hoàn thành công việc."}],
    "hsk4_396": [{"chinese": "这个国家的经济发展很快。", "pinyin": "Zhège guójiā de jīngjì fāzhǎn hěn kuài.", "meaningVi": "Kinh tế của đất nước này phát triển rất nhanh."}],
    "hsk4_398": [{"chinese": "这是一段难忘的经历。", "pinyin": "Zhè shì yí duàn nánwàng de jīnglì.", "meaningVi": "Đây là một trải nghiệm khó quên."}],
    "hsk4_407": [{"chinese": "你究竟想说什么？", "pinyin": "Nǐ jiūjìng xiǎng shuō shénme?", "meaningVi": "Rốt cuộc bạn muốn nói gì?"}],
    "hsk4_408": [{"chinese": "这个人就是我的老师。", "pinyin": "Zhège rén jiùshì wǒ de lǎoshī.", "meaningVi": "Người này chính là thầy giáo của tôi."}],
    "hsk4_415": [{"chinese": "周末我们要参加一个聚会。", "pinyin": "Zhōumò wǒmen yào cānjiā yí gè jùhuì.", "meaningVi": "Cuối tuần chúng tôi sẽ tham gia một buổi tụ họp."}],
    "hsk4_417": [{"chinese": "这里距离机场很远。", "pinyin": "Zhèlǐ jùlí jīchǎng hěn yuǎn.", "meaningVi": "Nơi đây cách sân bay rất xa."}],
    "hsk4_426": [{"chinese": "这个说法不够科学。", "pinyin": "Zhège shuōfǎ búgòu kēxué.", "meaningVi": "Cách nói này chưa đủ khoa học."}],
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
