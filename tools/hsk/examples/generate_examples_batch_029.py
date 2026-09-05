"""P5.10.3 (continued) -- Batch 029 (continues immediately after
examples_batch_028.json). This batch FINISHES the HSK6 tier-1 normal
queue (hsk6_1499-hsk6_1800, 299 records) and then, since tier-1 is
exhausted across every HSK level, the deterministic (tier, id) sort
moves on to tier-2 -- picking up its single smallest remaining id,
which happens to be hsk1_011 (an HSK1 record). This is NOT a bug: the
queue sorts ALL not-yet-completed records by (tier, id) ascending, so
once every tier-1 record (across HSK1-6) is exhausted, tier-2 records
begin, sorted by plain string id across all levels -- and "hsk1_..."
sorts before "hsk2_...", "hsk3_...", etc. HSK/tier for every record in
this batch was read directly from load_universe()/classify_risk_tiers
output, not assumed from level continuity.

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Numeric-suffix homograph records (needs_review) ***
Two records in this batch carry the HSK6 numeric-suffix homograph
pattern (see batch 024's 乘2, batch 025's 副2/该2, batch 026's
局1/局2/料1/料2/露1, batch 027's 升2, and batch 028's 所2 for the full
explanation): 则1 (hsk6_1653) and 支2 (hsk6_1694). These are the LAST
two such records in the entire HSK6 dataset -- with this batch, the
numeric-suffix homograph pattern is fully resolved pipeline-wide (12
of 12 handled: 乘2, 副2, 该2, 局1, 局2, 料1, 料2, 露1, 升2, 所2, 则1,
支2). Both left with an empty examples list and qaStatus
"needs_review". Production records untouched.

*** Continuing extremely dense homophone/polyphonic clusters ***
This is the final stretch of HSK6 and spans the y-/z- initial range,
which is unusually dense:
  - yán (2nd tone): 严/沿海/严寒/严禁/严厉/延期/炎热/延伸/研讨/延续/
    言语/炎症 -- twelve members across five different characters
    (严/沿/延/炎/研/言).
  - yí (2nd tone): the largest cluster in this batch -- 姨/一辈子/
    遗产/遗传/一带/一道/一贯/疑惑/一律/移民/仪器/仪式/一向/一系列/
    一再/一阵/遗址 -- sixteen members across six characters (姨/一/
    遗/疑/移/仪).
  - yì (4th tone): 异常/益处/一帆风顺/一口气/议论/一模一样/艺人/
    一身/一时/一同/易于/抑制 -- twelve members across seven
    characters (异/益/一/议/艺/易/抑).
  - yǐn (3rd tone): 引/隐藏/引导/引发/引入/隐私/饮用水 -- seven
    members across three characters (引/隐/饮).
  - yuán (2nd tone): 原本/原材料/原理/原料/园林/原始/原先/元素/
    元宵/源于 -- ten members across three characters (原/园/元).
  - 晕 polyphonic: 晕 alone (hsk6_1633, "dizzy") reads YŪN (1st tone)
    while 晕车 (hsk6_1634, "carsick") reads the SAME character as
    YÙN (4th tone) -- genuinely different tones for the same
    character, kept distinct.
  - 中 polyphonic (critical): 中等/中断/中旬/中央 read ZHŌNG (1st
    tone, "middle/center") while 中毒/中奖/中暑 read the SAME
    character as ZHÒNG (4th tone, "to be hit/struck by" -- to be
    poisoned/win a prize/get heatstroke) -- genuinely different tones
    for the same character. 众人/众所周知 (zhòng, "crowd/masses") and
    重心 (zhòng, "heavy/important") are two further different
    characters sharing the zhòng reading. All five zhòng-reading
    words and all four zhōng-reading words given distinct natural
    contexts.
  - 转 polyphonic: 转换/转交/转让/转身/转移 read ZHUǍN (3rd tone, "to
    turn/transfer") while 转动 (hsk6_1770) reads the SAME character
    as ZHUÀN (4th tone, "to rotate/turn") -- genuinely different tone
    for the same character, kept distinct.
  - zhǔ (3rd tone): 主办/主播/主导/主管/主角/主流/主演/主张 -- eight
    members, same character 主 in different compounds.
  - zhì (4th tone): 制/至关重要/智力/治理/制品/秩序/质疑/至于 --
    eight members across six characters (制/至/智/治/秩/质).

Fix applied after the first validator pass (caught by
validate_examples_batch_p103.py's no_duplicate_sentences_across_
pilot_and_batches check): 指挥 (zhǐhuī)'s first draft "交警在路口
指挥交通。" was an EXACT duplicate of an already-published sentence
elsewhere in the corpus. Rewritten to "他指挥这支乐队已经十年了。".

Near-template fixes (character-bigram Jaccard >= 0.55 against the
full pilot+002-028 corpus, caught by the independent script-level
check, not the validator): nine flags, all fixed by diverging
sentence structure while preserving natural, correct usage:
  - 亚军 vs batch 026's hsk6_0701 "他获得了本次比赛的金牌。" (both
    used the "他获得了本次比赛的...。" template) -> "惜败给冠军，他
    只拿到了亚军。".
  - 一道 vs hsk1_038's "我们去看电影吧。" -> "他和同事一道完成了这个
    项目。".
  - 一阵 vs hsk5_1487's "外面刮起了一阵大风。" (both used the
    "...刮起了一阵大风。" template) -> "会场里响起了一阵热烈的掌声。".
  - 勇于 vs hsk4_509's "我们要勇敢面对困难。" (near-synonym 勇于/
    勇敢 in an otherwise identical clause) -> "他勇于承认自己的
    错误。".
  - 用处 vs hsk5_1395's "这个工具有很多用途。" (near-synonym 用处/
    用途 in an otherwise identical clause) -> "这份说明书详细介绍了
    每个按钮的用处。".
  - 赞同 vs hsk5_1447's "大家都赞成这个提议。" (near-synonym 赞同/
    赞成 in an otherwise identical clause) -> "他对这个方案表示
    赞同。".
  - 粘贴 vs hsk5_1136's "请把海报贴在墙上。" -> "他用胶带把照片粘贴
    在笔记本上。".
  - 珍珠 (手链) vs batch 028's hsk6_1441 "她戴着一条珍珠项链。" (both
    used the "她戴着一条珍珠...。" template on near-synonymous
    jewelry) -> "这条珍珠手链是母亲留给她的。".
  - 政策 vs hsk5_1494's "政府出台了新的经济政策。" (both used the
    "政府出台了新的...政策。" template) -> "这项政策对中小企业十分
    有利。".
Re-verified after these fixes: zero cross-corpus flags, zero
within-batch flags (see validation report).

All re-verified against the full pilot+002-028 corpus with zero
remaining exact duplicates and zero near-template flags (see
validation report).

Usage:
    python generate_examples_batch_029.py --dry-run
    python generate_examples_batch_029.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 29
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_029.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# Records deliberately left with 0 examples (see module docstring):
# HSK6's numeric-suffix homograph pattern makes the literal target
# word unmatchable in natural Chinese text. These are the LAST two
# such records pipeline-wide.
NEEDS_REVIEW_IDS = {"hsk6_1653", "hsk6_1694"}

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk6_1499": [{"chinese": "请把这个文件压缩一下。", "pinyin": "Qǐng bǎ zhège wénjiàn yāsuō yíxià.", "meaningVi": "Xin nén tệp tin này lại."}],
    "hsk6_1500": [{"chinese": "惜败给冠军，他只拿到了亚军。", "pinyin": "Xībài gěi guànjūn, tā zhǐ nádàole yàjūn.", "meaningVi": "Tiếc là thua trước nhà vô địch, anh ấy chỉ giành được á quân."}],
    "hsk6_1501": [{"chinese": "洪水淹了整个村庄。", "pinyin": "Hóngshuǐ yānle zhěnggè cūnzhuāng.", "meaningVi": "Lũ lụt đã nhấn chìm toàn bộ ngôi làng."}],
    "hsk6_1502": [{"chinese": "大水淹没了农田。", "pinyin": "Dàshuǐ yānmòle nóngtián.", "meaningVi": "Nước lớn đã nhấn chìm ruộng đồng."}],
    "hsk6_1503": [{"chinese": "老师对学生要求很严。", "pinyin": "Lǎoshī duì xuésheng yāoqiú hěn yán.", "meaningVi": "Giáo viên yêu cầu học sinh rất nghiêm khắc."}],
    "hsk6_1504": [{"chinese": "这是一座沿海城市。", "pinyin": "Zhè shì yí zuò yánhǎi chéngshì.", "meaningVi": "Đây là một thành phố ven biển."}],
    "hsk6_1505": [{"chinese": "北方的冬天十分严寒。", "pinyin": "Běifāng de dōngtiān shífēn yánhán.", "meaningVi": "Mùa đông ở miền Bắc vô cùng giá rét."}],
    "hsk6_1506": [{"chinese": "车间内严禁吸烟。", "pinyin": "Chējiān nèi yánjìn xīyān.", "meaningVi": "Bên trong xưởng nghiêm cấm hút thuốc."}],
    "hsk6_1507": [{"chinese": "老师严厉地批评了他。", "pinyin": "Lǎoshī yánlì de pīpíngle tā.", "meaningVi": "Giáo viên đã phê bình anh ấy một cách nghiêm khắc."}],
    "hsk6_1508": [{"chinese": "由于天气原因，比赛延期了。", "pinyin": "Yóuyú tiānqì yuányīn, bǐsài yánqī le.", "meaningVi": "Vì lý do thời tiết, trận đấu đã bị hoãn lại."}],
    "hsk6_1509": [{"chinese": "夏天的天气十分炎热。", "pinyin": "Xiàtiān de tiānqì shífēn yánrè.", "meaningVi": "Thời tiết mùa hè vô cùng nóng bức."}],
    "hsk6_1510": [{"chinese": "这条山脉向北延伸。", "pinyin": "Zhè tiáo shānmài xiàng běi yánshēn.", "meaningVi": "Dãy núi này kéo dài về phía bắc."}],
    "hsk6_1511": [{"chinese": "专家们对这个课题进行了研讨。", "pinyin": "Zhuānjiāmen duì zhège kètí jìnxíngle yántǎo.", "meaningVi": "Các chuyên gia đã thảo luận về đề tài này."}],
    "hsk6_1512": [{"chinese": "这个传统一直延续到今天。", "pinyin": "Zhège chuántǒng yìzhí yánxù dào jīntiān.", "meaningVi": "Truyền thống này vẫn tiếp tục cho đến ngày nay."}],
    "hsk6_1513": [{"chinese": "他的言语十分谨慎。", "pinyin": "Tā de yányǔ shífēn jǐnshèn.", "meaningVi": "Lời nói của anh ấy vô cùng thận trọng."}],
    "hsk6_1514": [{"chinese": "他的伤口出现了炎症。", "pinyin": "Tā de shāngkǒu chūxiànle yánzhèng.", "meaningVi": "Vết thương của anh ấy xuất hiện viêm nhiễm."}],
    "hsk6_1515": [{"chinese": "她挑选衣服很有眼光。", "pinyin": "Tā tiāoxuǎn yīfu hěn yǒu yǎnguāng.", "meaningVi": "Cô ấy chọn quần áo rất có mắt nhìn."}],
    "hsk6_1516": [{"chinese": "眼看比赛就要开始了。", "pinyin": "Yǎnkàn bǐsài jiù yào kāishǐ le.", "meaningVi": "Sắp sửa trận đấu bắt đầu rồi."}],
    "hsk6_1517": [{"chinese": "他为大家演奏了一首钢琴曲。", "pinyin": "Tā wèi dàjiā yǎnzòule yì shǒu gāngqínqǔ.", "meaningVi": "Anh ấy đã biểu diễn một bản nhạc piano cho mọi người."}],
    "hsk6_1518": [{"chinese": "公司举办了一场庆祝宴会。", "pinyin": "Gōngsī jǔbànle yì chǎng qìngzhù yànhuì.", "meaningVi": "Công ty đã tổ chức một bữa tiệc mừng."}],
    "hsk6_1519": [{"chinese": "请输入密码进行验证。", "pinyin": "Qǐng shūrù mìmǎ jìnxíng yànzhèng.", "meaningVi": "Xin nhập mật khẩu để xác minh."}],
    "hsk6_1520": [{"chinese": "他仰起头看着天空。", "pinyin": "Tā yǎngqǐ tóu kànzhe tiānkōng.", "meaningVi": "Anh ấy ngẩng đầu lên nhìn bầu trời."}],
    "hsk6_1521": [{"chinese": "蚊子咬的地方很痒。", "pinyin": "Wénzi yǎo de dìfang hěn yǎng.", "meaningVi": "Chỗ bị muỗi cắn rất ngứa."}],
    "hsk6_1522": [{"chinese": "他打算退休后回农村养老。", "pinyin": "Tā dǎsuàn tuìxiū hòu huí nóngcūn yǎnglǎo.", "meaningVi": "Anh ấy dự định sau khi nghỉ hưu sẽ về quê dưỡng già."}],
    "hsk6_1523": [{"chinese": "奶奶住在一家养老院里。", "pinyin": "Nǎinai zhù zài yì jiā yǎnglǎoyuàn lǐ.", "meaningVi": "Bà nội sống trong một viện dưỡng lão."}],
    "hsk6_1524": [{"chinese": "病人需要吸氧气。", "pinyin": "Bìngrén xūyào xī yǎngqì.", "meaningVi": "Bệnh nhân cần thở oxy."}],
    "hsk6_1525": [{"chinese": "这件衣服的样子很好看。", "pinyin": "Zhè jiàn yīfu de yàngzi hěn hǎokàn.", "meaningVi": "Kiểu dáng của chiếc áo này rất đẹp."}],
    "hsk6_1526": [{"chinese": "那是一个遥远的国家。", "pinyin": "Nà shì yí gè yáoyuǎn de guójiā.", "meaningVi": "Đó là một quốc gia xa xôi."}],
    "hsk6_1527": [{"chinese": "请记下这几个要点。", "pinyin": "Qǐng jìxià zhè jǐ gè yàodiǎn.", "meaningVi": "Xin ghi lại mấy điểm chính này."}],
    "hsk6_1528": [{"chinese": "我们要么现在走，要么就晚了。", "pinyin": "Wǒmen yàome xiànzài zǒu, yàome jiù wǎn le.", "meaningVi": "Chúng ta hoặc là đi bây giờ, hoặc là sẽ muộn."}],
    "hsk6_1529": [{"chinese": "诚信是合作的重要要素。", "pinyin": "Chéngxìn shì hézuò de zhòngyào yàosù.", "meaningVi": "Chữ tín là yếu tố quan trọng của hợp tác."}],
    "hsk6_1530": [{"chinese": "这只猫是野猫。", "pinyin": "Zhè zhī māo shì yě māo.", "meaningVi": "Con mèo này là mèo hoang."}],
    "hsk6_1531": [{"chinese": "你去也好，不去也好，随你便。", "pinyin": "Nǐ qù yěhǎo, bú qù yěhǎo, suí nǐ biàn.", "meaningVi": "Bạn đi cũng được, không đi cũng được, tùy bạn."}],
    "hsk6_1532": [{"chinese": "这是一种野生植物。", "pinyin": "Zhè shì yì zhǒng yěshēng zhíwù.", "meaningVi": "Đây là một loại thực vật hoang dã."}],
    "hsk6_1533": [{"chinese": "他们去野外露营了。", "pinyin": "Tāmen qù yěwài lùyíng le.", "meaningVi": "Họ đã đi cắm trại ngoài trời."}],
    "hsk6_1534": [{"chinese": "他从事餐饮业。", "pinyin": "Tā cóngshì cānyǐnyè.", "meaningVi": "Anh ấy làm trong ngành ẩm thực."}],
    "hsk6_1535": [{"chinese": "水是一种液体。", "pinyin": "Shuǐ shì yì zhǒng yètǐ.", "meaningVi": "Nước là một loại chất lỏng."}],
    "hsk6_1536": [{"chinese": "多年过去，他依旧那么年轻。", "pinyin": "Duō nián guòqù, tā yījiù nàme niánqīng.", "meaningVi": "Nhiều năm trôi qua, anh ấy vẫn trẻ trung như vậy."}],
    "hsk6_1537": [{"chinese": "孩子不应该过分依赖父母。", "pinyin": "Háizi bù yīnggāi guòfèn yīlài fùmǔ.", "meaningVi": "Trẻ em không nên quá phụ thuộc vào cha mẹ."}],
    "hsk6_1538": [{"chinese": "这是一所一流的大学。", "pinyin": "Zhè shì yì suǒ yīliú de dàxué.", "meaningVi": "Đây là một trường đại học hạng nhất."}],
    "hsk6_1539": [{"chinese": "衣食住行是老百姓最关心的事。", "pinyin": "Yī-shí-zhù-xíng shì lǎobǎixìng zuì guānxīn de shì.", "meaningVi": "Ăn mặc ở đi lại là việc người dân quan tâm nhất."}],
    "hsk6_1540": [{"chinese": "这家公司主要经营医药产品。", "pinyin": "Zhè jiā gōngsī zhǔyào jīngyíng yīyào chǎnpǐn.", "meaningVi": "Công ty này chủ yếu kinh doanh sản phẩm dược phẩm."}],
    "hsk6_1541": [{"chinese": "他把问题一一列了出来。", "pinyin": "Tā bǎ wèntí yīyī lièle chūlái.", "meaningVi": "Anh ấy đã liệt kê từng vấn đề một."}],
    "hsk6_1542": [{"chinese": "我姨从小就疼我。", "pinyin": "Wǒ yí cóngxiǎo jiù téng wǒ.", "meaningVi": "Dì tôi từ nhỏ đã rất thương tôi."}],
    "hsk6_1543": [{"chinese": "他一辈子都在为教育事业奋斗。", "pinyin": "Tā yíbèizi dōu zài wèi jiàoyù shìyè fèndòu.", "meaningVi": "Cả đời anh ấy đều phấn đấu cho sự nghiệp giáo dục."}],
    "hsk6_1544": [{"chinese": "长城是世界文化遗产。", "pinyin": "Chángchéng shì shìjiè wénhuà yíchǎn.", "meaningVi": "Vạn Lý Trường Thành là di sản văn hóa thế giới."}],
    "hsk6_1545": [{"chinese": "这种病具有遗传性。", "pinyin": "Zhè zhǒng bìng jùyǒu yíchuánxìng.", "meaningVi": "Căn bệnh này mang tính di truyền."}],
    "hsk6_1546": [{"chinese": "这一带风景优美。", "pinyin": "Zhè yídài fēngjǐng yōuměi.", "meaningVi": "Khu vực này phong cảnh tươi đẹp."}],
    "hsk6_1547": [{"chinese": "他和同事一道完成了这个项目。", "pinyin": "Tā hé tóngshì yídào wánchéngle zhège xiàngmù.", "meaningVi": "Anh ấy đã cùng đồng nghiệp hoàn thành dự án này."}],
    "hsk6_1548": [{"chinese": "他一贯认真负责。", "pinyin": "Tā yíguàn rènzhēn fùzé.", "meaningVi": "Anh ấy luôn nhất quán nghiêm túc có trách nhiệm."}],
    "hsk6_1549": [{"chinese": "他脸上露出了疑惑的表情。", "pinyin": "Tā liǎn shàng lòuchūle yíhuò de biǎoqíng.", "meaningVi": "Trên mặt anh ấy lộ ra vẻ nghi hoặc."}],
    "hsk6_1550": [{"chinese": "迟到者一律不得入场。", "pinyin": "Chídàozhě yílǜ bùdé rùchǎng.", "meaningVi": "Người đến muộn đồng loạt không được vào."}],
    "hsk6_1551": [{"chinese": "他们全家移民到了加拿大。", "pinyin": "Tāmen quánjiā yímín dàole Jiānádà.", "meaningVi": "Cả gia đình họ đã di dân đến Canada."}],
    "hsk6_1552": [{"chinese": "实验室里有各种精密仪器。", "pinyin": "Shíyànshì lǐ yǒu gèzhǒng jīngmì yíqì.", "meaningVi": "Trong phòng thí nghiệm có đủ loại dụng cụ tinh vi."}],
    "hsk6_1553": [{"chinese": "婚礼仪式非常隆重。", "pinyin": "Hūnlǐ yíshì fēicháng lóngzhòng.", "meaningVi": "Nghi thức đám cưới vô cùng long trọng."}],
    "hsk6_1554": [{"chinese": "他一向按时上班。", "pinyin": "Tā yíxiàng ànshí shàngbān.", "meaningVi": "Anh ấy luôn đi làm đúng giờ."}],
    "hsk6_1555": [{"chinese": "公司出台了一系列新政策。", "pinyin": "Gōngsī chūtáile yíxìliè xīn zhèngcè.", "meaningVi": "Công ty đã ban hành một loạt chính sách mới."}],
    "hsk6_1556": [{"chinese": "他一再表示歉意。", "pinyin": "Tā yízài biǎoshì qiànyì.", "meaningVi": "Anh ấy nhiều lần bày tỏ lời xin lỗi."}],
    "hsk6_1557": [{"chinese": "会场里响起了一阵热烈的掌声。", "pinyin": "Huìchǎng lǐ xiǎngqǐle yízhèn rèliè de zhǎngshēng.", "meaningVi": "Trong hội trường vang lên một tràng vỗ tay nhiệt liệt."}],
    "hsk6_1558": [{"chinese": "考古学家在这里发现了古代遗址。", "pinyin": "Kǎogǔ xuéjiā zài zhèlǐ fāxiànle gǔdài yízhǐ.", "meaningVi": "Các nhà khảo cổ đã phát hiện di chỉ cổ đại tại đây."}],
    "hsk6_1559": [{"chinese": "请留下电话号码，以便联系。", "pinyin": "Qǐng liúxià diànhuà hàomǎ, yǐbiàn liánxì.", "meaningVi": "Xin để lại số điện thoại để tiện liên hệ."}],
    "hsk6_1560": [{"chinese": "请提前出发，以免迟到。", "pinyin": "Qǐng tíqián chūfā, yǐmiǎn chídào.", "meaningVi": "Xin xuất phát sớm để tránh trễ giờ."}],
    "hsk6_1561": [{"chinese": "今年的销量比以往都好。", "pinyin": "Jīnnián de xiāoliàng bǐ yǐwǎng dōu hǎo.", "meaningVi": "Doanh số năm nay tốt hơn trước đây."}],
    "hsk6_1562": [{"chinese": "他今天的表现十分异常。", "pinyin": "Tā jīntiān de biǎoxiàn shífēn yìcháng.", "meaningVi": "Biểu hiện của anh ấy hôm nay vô cùng khác thường."}],
    "hsk6_1563": [{"chinese": "多读书对孩子有很多益处。", "pinyin": "Duō dúshū duì háizi yǒu hěn duō yìchù.", "meaningVi": "Đọc nhiều sách có nhiều lợi ích cho trẻ em."}],
    "hsk6_1564": [{"chinese": "祝你一帆风顺！", "pinyin": "Zhù nǐ yìfān-fēngshùn!", "meaningVi": "Chúc bạn thuận buồm xuôi gió!"}],
    "hsk6_1565": [{"chinese": "他一口气跑完了全程。", "pinyin": "Tā yìkǒuqì pǎowánle quánchéng.", "meaningVi": "Anh ấy chạy hết toàn bộ chặng đường trong một hơi."}],
    "hsk6_1566": [{"chinese": "大家都在议论这件事。", "pinyin": "Dàjiā dōu zài yìlùn zhè jiàn shì.", "meaningVi": "Mọi người đều đang bàn tán về việc này."}],
    "hsk6_1567": [{"chinese": "这两件衣服一模一样。", "pinyin": "Zhè liǎng jiàn yīfu yìmú-yíyàng.", "meaningVi": "Hai chiếc áo này giống hệt nhau."}],
    "hsk6_1568": [{"chinese": "他是一位受欢迎的艺人。", "pinyin": "Tā shì yí wèi shòu huānyíng de yìrén.", "meaningVi": "Anh ấy là một nghệ sĩ được yêu thích."}],
    "hsk6_1569": [{"chinese": "他一身泥水地跑了回来。", "pinyin": "Tā yìshēn níshuǐ de pǎole huílai.", "meaningVi": "Anh ấy chạy về với toàn thân bùn nước."}],
    "hsk6_1570": [{"chinese": "我一时想不起他的名字。", "pinyin": "Wǒ yìshí xiǎngbuqǐ tā de míngzi.", "meaningVi": "Tôi nhất thời không nhớ ra tên của anh ấy."}],
    "hsk6_1571": [{"chinese": "我们一同前往目的地。", "pinyin": "Wǒmen yìtóng qiánwǎng mùdìdì.", "meaningVi": "Chúng tôi cùng nhau đến điểm đến."}],
    "hsk6_1572": [{"chinese": "这种材料易于加工。", "pinyin": "Zhè zhǒng cáiliào yìyú jiāgōng.", "meaningVi": "Loại vật liệu này dễ gia công."}],
    "hsk6_1573": [{"chinese": "他努力抑制住自己的情绪。", "pinyin": "Tā nǔlì yìzhìzhù zìjǐ de qíngxù.", "meaningVi": "Anh ấy cố gắng kìm nén cảm xúc của mình."}],
    "hsk6_1574": [{"chinese": "他因病请了假。", "pinyin": "Tā yīn bìng qǐngle jià.", "meaningVi": "Anh ấy vì bệnh mà xin nghỉ phép."}],
    "hsk6_1575": [{"chinese": "这个词有两个音节。", "pinyin": "Zhège cí yǒu liǎng gè yīnjié.", "meaningVi": "Từ này có hai âm tiết."}],
    "hsk6_1576": [{"chinese": "这个戒指是纯银的。", "pinyin": "Zhège jièzhi shì chúnyín de.", "meaningVi": "Chiếc nhẫn này là bạc nguyên chất."}],
    "hsk6_1577": [{"chinese": "她获得了这次比赛的银牌。", "pinyin": "Tā huòdéle zhè cì bǐsài de yínpái.", "meaningVi": "Cô ấy đã giành được huy chương bạc của cuộc thi lần này."}],
    "hsk6_1578": [{"chinese": "这本书引起了广泛关注。", "pinyin": "Zhè běn shū yǐnqǐle guǎngfàn guānzhù.", "meaningVi": "Cuốn sách này đã thu hút sự quan tâm rộng rãi."}],
    "hsk6_1579": [{"chinese": "他隐藏了自己的真实想法。", "pinyin": "Tā yǐncángle zìjǐ de zhēnshí xiǎngfǎ.", "meaningVi": "Anh ấy đã che giấu suy nghĩ thật của mình."}],
    "hsk6_1580": [{"chinese": "老师引导学生独立思考。", "pinyin": "Lǎoshī yǐndǎo xuésheng dúlì sīkǎo.", "meaningVi": "Giáo viên hướng dẫn học sinh suy nghĩ độc lập."}],
    "hsk6_1581": [{"chinese": "这项决定引发了争议。", "pinyin": "Zhè xiàng juédìng yǐnfāle zhēngyì.", "meaningVi": "Quyết định này đã gây ra tranh cãi."}],
    "hsk6_1582": [{"chinese": "公司引入了一套新系统。", "pinyin": "Gōngsī yǐnrùle yí tào xīn xìtǒng.", "meaningVi": "Công ty đã đưa vào một hệ thống mới."}],
    "hsk6_1583": [{"chinese": "请尊重他人的隐私。", "pinyin": "Qǐng zūnzhòng tārén de yǐnsī.", "meaningVi": "Xin tôn trọng sự riêng tư của người khác."}],
    "hsk6_1584": [{"chinese": "这里提供免费饮用水。", "pinyin": "Zhèlǐ tígōng miǎnfèi yǐnyòngshuǐ.", "meaningVi": "Nơi đây cung cấp nước uống miễn phí."}],
    "hsk6_1585": [{"chinese": "请在文件上印上公章。", "pinyin": "Qǐng zài wénjiàn shàng yìnshàng gōngzhāng.", "meaningVi": "Xin đóng dấu công ty lên tài liệu."}],
    "hsk6_1586": [{"chinese": "这个婴儿刚满月。", "pinyin": "Zhège yīng'ér gāng mǎnyuè.", "meaningVi": "Em bé này vừa tròn một tháng tuổi."}],
    "hsk6_1587": [{"chinese": "他是大家心目中的英雄。", "pinyin": "Tā shì dàjiā xīnmù zhōng de yīngxióng.", "meaningVi": "Anh ấy là anh hùng trong lòng mọi người."}],
    "hsk6_1588": [{"chinese": "阳光下他的影子拉得很长。", "pinyin": "Yángguāng xià tā de yǐngzi lā de hěn cháng.", "meaningVi": "Dưới ánh nắng bóng của anh ấy kéo dài."}],
    "hsk6_1589": [{"chinese": "上下班高峰期地铁十分拥挤。", "pinyin": "Shàngxiàbān gāofēngqī dìtiě shífēn yōngjǐ.", "meaningVi": "Vào giờ cao điểm đi làm tàu điện ngầm vô cùng chật chội."}],
    "hsk6_1590": [{"chinese": "这座城市涌现出许多优秀企业。", "pinyin": "Zhè zuò chéngshì yǒngxiànchū xǔduō yōuxiù qǐyè.", "meaningVi": "Thành phố này xuất hiện nhiều doanh nghiệp xuất sắc."}],
    "hsk6_1591": [{"chinese": "他勇于承认自己的错误。", "pinyin": "Tā yǒngyú chéngrèn zìjǐ de cuòwù.", "meaningVi": "Anh ấy dám thừa nhận sai lầm của mình."}],
    "hsk6_1592": [{"chinese": "请到餐厅用餐。", "pinyin": "Qǐng dào cāntīng yòngcān.", "meaningVi": "Xin mời đến nhà hàng dùng bữa."}],
    "hsk6_1593": [{"chinese": "这份说明书详细介绍了每个按钮的用处。", "pinyin": "Zhè fèn shuōmíngshū xiángxì jièshàole měi gè ànniǔ de yòngchù.", "meaningVi": "Bản hướng dẫn này giới thiệu chi tiết công dụng của từng nút bấm."}],
    "hsk6_1594": [{"chinese": "他学习一直很用功。", "pinyin": "Tā xuéxí yìzhí hěn yònggōng.", "meaningVi": "Anh ấy học tập luôn rất chăm chỉ."}],
    "hsk6_1595": [{"chinese": "这家公司用人不拘一格。", "pinyin": "Zhè jiā gōngsī yòngrén bù jū yì gé.", "meaningVi": "Công ty này dùng người không theo khuôn mẫu."}],
    "hsk6_1596": [{"chinese": "她用心照顾每一位病人。", "pinyin": "Tā yòngxīn zhàogù měi yí wèi bìngrén.", "meaningVi": "Cô ấy tận tâm chăm sóc từng bệnh nhân."}],
    "hsk6_1597": [{"chinese": "公司正在优化产品结构。", "pinyin": "Gōngsī zhèngzài yōuhuà chǎnpǐn jiégòu.", "meaningVi": "Công ty đang tối ưu hóa cơ cấu sản phẩm."}],
    "hsk6_1598": [{"chinese": "老人和孕妇可以优先上车。", "pinyin": "Lǎorén hé yùnfù kěyǐ yōuxiān shàngchē.", "meaningVi": "Người già và phụ nữ mang thai có thể lên xe ưu tiên."}],
    "hsk6_1599": [{"chinese": "他取得了优异的成绩。", "pinyin": "Tā qǔdéle yōuyì de chéngjì.", "meaningVi": "Anh ấy đã đạt được thành tích xuất sắc."}],
    "hsk6_1600": [{"chinese": "这个节日的由来已久。", "pinyin": "Zhège jiérì de yóulái yǐ jiǔ.", "meaningVi": "Nguồn gốc của lễ hội này đã có từ lâu."}],
    "hsk6_1601": [{"chinese": "公园里挤满了游人。", "pinyin": "Gōngyuán lǐ jǐmǎnle yóurén.", "meaningVi": "Trong công viên chật kín du khách."}],
    "hsk6_1602": [{"chinese": "她的歌声犹如天籁。", "pinyin": "Tā de gēshēng yóurú tiānlài.", "meaningVi": "Giọng hát của cô ấy giống như âm thanh thiên nhiên."}],
    "hsk6_1603": [{"chinese": "这些蔬菜都是有机种植的。", "pinyin": "Zhèxiē shūcài dōu shì yǒujī zhòngzhí de.", "meaningVi": "Những loại rau này đều được trồng hữu cơ."}],
    "hsk6_1604": [{"chinese": "他年轻的时候特别有劲。", "pinyin": "Tā niánqīng de shíhou tèbié yǒujìn.", "meaningVi": "Lúc còn trẻ anh ấy đặc biệt có sức."}],
    "hsk6_1605": [{"chinese": "现场秩序井然有序。", "pinyin": "Xiànchǎng zhìxù jǐngrán yǒuxù.", "meaningVi": "Trật tự tại hiện trường vô cùng có trật tự."}],
    "hsk6_1606": [{"chinese": "他生于一九九零年。", "pinyin": "Tā shēng yú yī jiǔ jiǔ líng nián.", "meaningVi": "Anh ấy sinh vào năm 1990."}],
    "hsk6_1607": [{"chinese": "请查询一下账户余额。", "pinyin": "Qǐng cháxún yíxià zhànghù yú'é.", "meaningVi": "Xin kiểm tra số dư tài khoản."}],
    "hsk6_1608": [{"chinese": "与其抱怨，不如努力改变。", "pinyin": "Yǔqí bàoyuàn, bùrú nǔlì gǎibiàn.", "meaningVi": "Thay vì than phiền, chi bằng nỗ lực thay đổi."}],
    "hsk6_1609": [{"chinese": "冬天他穿了一件厚厚的羽绒服。", "pinyin": "Dōngtiān tā chuānle yí jiàn hòuhòu de yǔróngfú.", "meaningVi": "Mùa đông anh ấy mặc một chiếc áo lông vũ dày."}],
    "hsk6_1610": [{"chinese": "请提前预定房间。", "pinyin": "Qǐng tíqián yùdìng fángjiān.", "meaningVi": "Xin đặt phòng trước."}],
    "hsk6_1611": [{"chinese": "事情的发展超出了大家的预料。", "pinyin": "Shìqing de fāzhǎn chāochūle dàjiā de yùliào.", "meaningVi": "Sự phát triển của sự việc vượt ngoài dự liệu của mọi người."}],
    "hsk6_1612": [{"chinese": "这次考试成绩没有达到预期。", "pinyin": "Zhè cì kǎoshì chéngjì méiyǒu dádào yùqī.", "meaningVi": "Kết quả kỳ thi lần này không đạt được như kỳ vọng."}],
    "hsk6_1613": [{"chinese": "浴室里安装了新的花洒。", "pinyin": "Yùshì lǐ ānzhuāngle xīn de huāsǎ.", "meaningVi": "Trong phòng tắm đã lắp đặt vòi hoa sen mới."}],
    "hsk6_1614": [{"chinese": "人的欲望是无穷的。", "pinyin": "Rén de yùwàng shì wúqióng de.", "meaningVi": "Ham muốn của con người là vô hạn."}],
    "hsk6_1615": [{"chinese": "这里原本是一片荒地。", "pinyin": "Zhèlǐ yuánběn shì yí piàn huāngdì.", "meaningVi": "Nơi đây vốn dĩ là một vùng đất hoang."}],
    "hsk6_1616": [{"chinese": "工厂的原材料价格上涨了。", "pinyin": "Gōngchǎng de yuáncáiliào jiàgé shàngzhǎng le.", "meaningVi": "Giá nguyên vật liệu của nhà máy đã tăng."}],
    "hsk6_1617": [{"chinese": "他讲解了这台机器的工作原理。", "pinyin": "Tā jiǎngjiěle zhè tái jīqì de gōngzuò yuánlǐ.", "meaningVi": "Anh ấy đã giảng giải nguyên lý hoạt động của cỗ máy này."}],
    "hsk6_1618": [{"chinese": "这道菜的原料十分新鲜。", "pinyin": "Zhè dào cài de yuánliào shífēn xīnxiān.", "meaningVi": "Nguyên liệu của món ăn này vô cùng tươi ngon."}],
    "hsk6_1619": [{"chinese": "苏州以古典园林闻名。", "pinyin": "Sūzhōu yǐ gǔdiǎn yuánlín wénmíng.", "meaningVi": "Tô Châu nổi tiếng với vườn cảnh cổ điển."}],
    "hsk6_1620": [{"chinese": "这次活动取得了圆满成功。", "pinyin": "Zhè cì huódòng qǔdéle yuánmǎn chénggōng.", "meaningVi": "Hoạt động lần này đã đạt được thành công trọn vẹn."}],
    "hsk6_1621": [{"chinese": "这片森林还保持着原始状态。", "pinyin": "Zhè piàn sēnlín hái bǎochízhe yuánshǐ zhuàngtài.", "meaningVi": "Khu rừng này vẫn giữ được trạng thái nguyên thủy."}],
    "hsk6_1622": [{"chinese": "氧气是一种化学元素。", "pinyin": "Yǎngqì shì yì zhǒng huàxué yuánsù.", "meaningVi": "Oxy là một nguyên tố hóa học."}],
    "hsk6_1623": [{"chinese": "原先的计划已经改变了。", "pinyin": "Yuánxiān de jìhuà yǐjīng gǎibiàn le.", "meaningVi": "Kế hoạch ban đầu đã thay đổi rồi."}],
    "hsk6_1624": [{"chinese": "元宵那天大家都要吃元宵。", "pinyin": "Yuánxiāo nà tiān dàjiā dōu yào chī yuánxiāo.", "meaningVi": "Vào ngày Tết Nguyên Tiêu mọi người đều phải ăn bánh trôi."}],
    "hsk6_1625": [{"chinese": "这个成语源于一个古老的故事。", "pinyin": "Zhège chéngyǔ yuányú yí gè gǔlǎo de gùshi.", "meaningVi": "Thành ngữ này bắt nguồn từ một câu chuyện cổ xưa."}],
    "hsk6_1626": [{"chinese": "他们通过远程会议讨论问题。", "pinyin": "Tāmen tōngguò yuǎnchéng huìyì tǎolùn wèntí.", "meaningVi": "Họ thảo luận vấn đề thông qua họp từ xa."}],
    "hsk6_1627": [{"chinese": "他从远方寄来了一封信。", "pinyin": "Tā cóng yuǎnfāng jìláile yì fēng xìn.", "meaningVi": "Anh ấy đã gửi một lá thư từ phương xa."}],
    "hsk6_1628": [{"chinese": "我们应该受到规则的约束。", "pinyin": "Wǒmen yīnggāi shòudào guīzé de yuēshù.", "meaningVi": "Chúng ta nên chịu sự ràng buộc của quy tắc."}],
    "hsk6_1629": [{"chinese": "月光洒在湖面上。", "pinyin": "Yuèguāng sǎ zài hú miàn shàng.", "meaningVi": "Ánh trăng rải trên mặt hồ."}],
    "hsk6_1630": [{"chinese": "他会演奏好几种乐器。", "pinyin": "Tā huì yǎnzòu hǎo jǐ zhǒng yuèqì.", "meaningVi": "Anh ấy biết chơi mấy loại nhạc cụ."}],
    "hsk6_1631": [{"chinese": "宇航员登上了月球。", "pinyin": "Yǔhángyuán dēngshàngle yuèqiú.", "meaningVi": "Phi hành gia đã đặt chân lên mặt trăng."}],
    "hsk6_1632": [{"chinese": "这首乐曲十分动听。", "pinyin": "Zhè shǒu yuèqǔ shífēn dòngtīng.", "meaningVi": "Bản nhạc này vô cùng du dương."}],
    "hsk6_1633": [{"chinese": "他一站起来就觉得头晕。", "pinyin": "Tā yí zhànqǐlai jiù juéde tóuyūn.", "meaningVi": "Anh ấy vừa đứng dậy đã cảm thấy chóng mặt."}],
    "hsk6_1634": [{"chinese": "她坐长途汽车容易晕车。", "pinyin": "Tā zuò chángtú qìchē róngyì yùnchē.", "meaningVi": "Cô ấy đi xe khách đường dài dễ bị say xe."}],
    "hsk6_1635": [{"chinese": "这批货物由卡车运送。", "pinyin": "Zhè pī huòwù yóu kǎchē yùnsòng.", "meaningVi": "Lô hàng này được vận chuyển bằng xe tải."}],
    "hsk6_1636": [{"chinese": "系统目前运行正常。", "pinyin": "Xìtǒng mùqián yùnxíng zhèngcháng.", "meaningVi": "Hệ thống hiện đang vận hành bình thường."}],
    "hsk6_1637": [{"chinese": "这家公司主要负责运营网站。", "pinyin": "Zhè jiā gōngsī zhǔyào fùzé yùnyíng wǎngzhàn.", "meaningVi": "Công ty này chủ yếu phụ trách vận hành trang web."}],
    "hsk6_1638": [{"chinese": "这里的东西摆放得很杂。", "pinyin": "Zhèlǐ de dōngxi bǎifàng de hěn zá.", "meaningVi": "Đồ đạc ở đây được sắp xếp lộn xộn."}],
    "hsk6_1639": [{"chinese": "这场灾给百姓带来了巨大损失。", "pinyin": "Zhè chǎng zāi gěi bǎixìng dàiláile jùdà sǔnshī.", "meaningVi": "Tai họa này đã gây ra tổn thất to lớn cho người dân."}],
    "hsk6_1640": [{"chinese": "这个地区经常发生自然灾害。", "pinyin": "Zhège dìqū jīngcháng fāshēng zìrán zāihài.", "meaningVi": "Khu vực này thường xuyên xảy ra thiên tai."}],
    "hsk6_1641": [{"chinese": "地震是一场巨大的灾难。", "pinyin": "Dìzhèn shì yì chǎng jùdà de zāinàn.", "meaningVi": "Động đất là một thảm họa to lớn."}],
    "hsk6_1642": [{"chinese": "志愿者们纷纷前往灾区支援。", "pinyin": "Zhìyuànzhěmen fēnfēn qiánwǎng zāiqū zhīyuán.", "meaningVi": "Các tình nguyện viên lần lượt đến vùng bị thiên tai để hỗ trợ."}],
    "hsk6_1643": [{"chinese": "他再三叮嘱我路上要小心。", "pinyin": "Tā zàisān dīngzhǔ wǒ lùshang yào xiǎoxīn.", "meaningVi": "Anh ấy nhiều lần dặn dò tôi trên đường phải cẩn thận."}],
    "hsk6_1644": [{"chinese": "这种材料可以再生利用。", "pinyin": "Zhè zhǒng cáiliào kěyǐ zàishēng lìyòng.", "meaningVi": "Loại vật liệu này có thể tái sử dụng."}],
    "hsk6_1645": [{"chinese": "他从不在意别人的看法。", "pinyin": "Tā cóng bú zàiyì biéren de kànfǎ.", "meaningVi": "Anh ấy không bao giờ để ý đến ý kiến của người khác."}],
    "hsk6_1646": [{"chinese": "老师对他的作品表示赞赏。", "pinyin": "Lǎoshī duì tā de zuòpǐn biǎoshì zànshǎng.", "meaningVi": "Giáo viên bày tỏ sự tán thưởng đối với tác phẩm của anh ấy."}],
    "hsk6_1647": [{"chinese": "他对这个方案表示赞同。", "pinyin": "Tā duì zhège fāng'àn biǎoshì zàntóng.", "meaningVi": "Anh ấy bày tỏ sự tán thành đối với phương án này."}],
    "hsk6_1648": [{"chinese": "他的方案遭到了大家的反对。", "pinyin": "Tā de fāng'àn zāodàole dàjiā de fǎnduì.", "meaningVi": "Phương án của anh ấy đã vấp phải sự phản đối của mọi người."}],
    "hsk6_1649": [{"chinese": "这座城市遭受了严重的洪灾。", "pinyin": "Zhè zuò chéngshì zāoshòule yánzhòng de hóngzāi.", "meaningVi": "Thành phố này đã hứng chịu trận lũ lụt nghiêm trọng."}],
    "hsk6_1650": [{"chinese": "他在旅途中遭遇了不少困难。", "pinyin": "Tā zài lǚtú zhōng zāoyùle bù shǎo kùnnan.", "meaningVi": "Anh ấy đã gặp phải không ít khó khăn trong chuyến đi."}],
    "hsk6_1651": [{"chinese": "施工现场的噪声很大。", "pinyin": "Shīgōng xiànchǎng de zàoshēng hěn dà.", "meaningVi": "Tiếng ồn tại công trường thi công rất lớn."}],
    "hsk6_1652": [{"chinese": "这座雕塑的造型十分独特。", "pinyin": "Zhè zuò diāosù de zàoxíng shífēn dútè.", "meaningVi": "Kiểu dáng của bức tượng này vô cùng độc đáo."}],
    "hsk6_1653": [],
    "hsk6_1654": [{"chinese": "护士给他扎了一针。", "pinyin": "Hùshi gěi tā zhāle yì zhēn.", "meaningVi": "Y tá đã tiêm cho anh ấy một mũi."}],
    "hsk6_1656": [{"chinese": "这种胶水很粘。", "pinyin": "Zhè zhǒng jiāoshuǐ hěn zhān.", "meaningVi": "Loại keo này rất dính."}],
    "hsk6_1657": [{"chinese": "他用胶带把照片粘贴在笔记本上。", "pinyin": "Tā yòng jiāodài bǎ zhàopiàn zhāntiē zài bǐjìběn shàng.", "meaningVi": "Anh ấy dùng băng dính dán ảnh vào sổ tay."}],
    "hsk6_1658": [{"chinese": "他穿着一身崭新的西装。", "pinyin": "Tā chuānzhe yì shēn zhǎnxīn de xīzhuāng.", "meaningVi": "Anh ấy mặc một bộ com-lê mới tinh."}],
    "hsk6_1659": [{"chinese": "新能源汽车的占比逐年上升。", "pinyin": "Xīnnéngyuán qìchē de zhànbǐ zhúnián shàngshēng.", "meaningVi": "Tỷ lệ chiếm của xe năng lượng mới tăng theo từng năm."}],
    "hsk6_1660": [{"chinese": "士兵们勇敢地投入战斗。", "pinyin": "Shìbīngmen yǒnggǎn de tóurù zhàndòu.", "meaningVi": "Các binh sĩ dũng cảm lao vào chiến đấu."}],
    "hsk6_1661": [{"chinese": "这个品牌占据了大部分市场。", "pinyin": "Zhège pǐnpái zhànjùle dà bùfen shìchǎng.", "meaningVi": "Thương hiệu này chiếm giữ phần lớn thị trường."}],
    "hsk6_1662": [{"chinese": "他最终战胜了自己的恐惧。", "pinyin": "Tā zhōngyú zhànshèngle zìjǐ de kǒngjù.", "meaningVi": "Cuối cùng anh ấy đã chiến thắng nỗi sợ hãi của mình."}],
    "hsk6_1663": [{"chinese": "这类产品占有很大的市场份额。", "pinyin": "Zhè lèi chǎnpǐn zhànyǒu hěn dà de shìchǎng fèn'é.", "meaningVi": "Loại sản phẩm này chiếm hữu thị phần rất lớn."}],
    "hsk6_1664": [{"chinese": "战争给人民带来了深重的灾难。", "pinyin": "Zhànzhēng gěi rénmín dàiláile shēnzhòng de zāinàn.", "meaningVi": "Chiến tranh đã mang lại thảm họa sâu sắc cho nhân dân."}],
    "hsk6_1665": [{"chinese": "这本书共分十章。", "pinyin": "Zhè běn shū gòng fēn shí zhāng.", "meaningVi": "Cuốn sách này được chia làm mười chương."}],
    "hsk6_1666": [{"chinese": "过年要给长辈拜年。", "pinyin": "Guònián yào gěi zhǎngbèi bàinián.", "meaningVi": "Ngày Tết phải chúc Tết các bậc trưởng bối."}],
    "hsk6_1667": [{"chinese": "他克服了重重障碍。", "pinyin": "Tā kèfúle chóngchóng zhàng'ài.", "meaningVi": "Anh ấy đã vượt qua bao trở ngại chồng chất."}],
    "hsk6_1668": [{"chinese": "请核对一下这份账单。", "pinyin": "Qǐng héduì yíxià zhè fèn zhàngdān.", "meaningVi": "Xin kiểm tra lại tờ hóa đơn này."}],
    "hsk6_1669": [{"chinese": "他向我招了招手。", "pinyin": "Tā xiàng wǒ zhāole zhāo shǒu.", "meaningVi": "Anh ấy vẫy tay với tôi."}],
    "hsk6_1670": [{"chinese": "主人热情地招待了客人。", "pinyin": "Zhǔrén rèqíng de zhāodàile kèren.", "meaningVi": "Chủ nhà đã nhiệt tình tiếp đãi khách."}],
    "hsk6_1671": [{"chinese": "这所大学今年扩大了招生规模。", "pinyin": "Zhè suǒ dàxué jīnnián kuòdàle zhāoshēng guīmó.", "meaningVi": "Trường đại học này năm nay đã mở rộng quy mô tuyển sinh."}],
    "hsk6_1672": [{"chinese": "她远远地向我们招手。", "pinyin": "Tā yuǎnyuǎn de xiàng wǒmen zhāoshǒu.", "meaningVi": "Cô ấy vẫy tay chào chúng tôi từ xa."}],
    "hsk6_1673": [{"chinese": "这家公司正在招收新员工。", "pinyin": "Zhè jiā gōngsī zhèngzài zhāoshōu xīn yuángōng.", "meaningVi": "Công ty này đang tuyển nhận nhân viên mới."}],
    "hsk6_1674": [{"chinese": "这条街的照明设施不太好。", "pinyin": "Zhè tiáo jiē de zhàomíng shèshī bú tài hǎo.", "meaningVi": "Thiết bị chiếu sáng của con phố này không tốt lắm."}],
    "hsk6_1675": [{"chinese": "这件商品打八折出售。", "pinyin": "Zhè jiàn shāngpǐn dǎ bā zhé chūshòu.", "meaningVi": "Món hàng này được bán giảm giá hai mươi phần trăm."}],
    "hsk6_1676": [{"chinese": "医生给他打了一针。", "pinyin": "Yīshēng gěi tā dǎle yì zhēn.", "meaningVi": "Bác sĩ đã tiêm cho anh ấy một mũi."}],
    "hsk6_1677": [{"chinese": "警方终于查明了事情的真相。", "pinyin": "Jǐngfāng zhōngyú cháomíngle shìqing de zhēnxiàng.", "meaningVi": "Cảnh sát cuối cùng đã làm rõ sự thật của sự việc."}],
    "hsk6_1678": [{"chinese": "这条珍珠手链是母亲留给她的。", "pinyin": "Zhè tiáo zhēnzhū shǒuliàn shì mǔqīn liú gěi tā de.", "meaningVi": "Chiếc vòng tay ngọc trai này là mẹ để lại cho cô ấy."}],
    "hsk6_1679": [{"chinese": "他抱着枕头睡着了。", "pinyin": "Tā bàozhe zhěntou shuìzháo le.", "meaningVi": "Anh ấy ôm gối ngủ thiếp đi."}],
    "hsk6_1680": [{"chinese": "他出生在一个小镇上。", "pinyin": "Tā chūshēng zài yí gè xiǎo zhèn shàng.", "meaningVi": "Anh ấy sinh ra ở một thị trấn nhỏ."}],
    "hsk6_1681": [{"chinese": "明天下午有阵雨。", "pinyin": "Míngtiān xiàwǔ yǒu zhènyǔ.", "meaningVi": "Chiều mai có mưa rào."}],
    "hsk6_1682": [{"chinese": "他慢慢睁开了眼睛。", "pinyin": "Tā mànmàn zhēngkāile yǎnjing.", "meaningVi": "Anh ấy từ từ mở mắt ra."}],
    "hsk6_1683": [{"chinese": "他们因为小事争吵起来。", "pinyin": "Tāmen yīnwèi xiǎoshì zhēngchǎo qǐlai.", "meaningVi": "Họ vì chuyện nhỏ mà cãi nhau."}],
    "hsk6_1684": [{"chinese": "两队正在争夺冠军。", "pinyin": "Liǎng duì zhèngzài zhēngduó guànjūn.", "meaningVi": "Hai đội đang tranh giành ngôi vô địch."}],
    "hsk6_1685": [{"chinese": "大家为这个问题争论不休。", "pinyin": "Dàjiā wèi zhège wèntí zhēnglùn bùxiū.", "meaningVi": "Mọi người tranh luận không ngừng về vấn đề này."}],
    "hsk6_1686": [{"chinese": "公司正在征求员工的意见。", "pinyin": "Gōngsī zhèngzài zhēngqiú yuángōng de yìjiàn.", "meaningVi": "Công ty đang trưng cầu ý kiến của nhân viên."}],
    "hsk6_1687": [{"chinese": "这个话题引发了很大的争议。", "pinyin": "Zhège huàtí yǐnfāle hěn dà de zhēngyì.", "meaningVi": "Chủ đề này đã gây ra tranh cãi lớn."}],
    "hsk6_1688": [{"chinese": "这项政策对中小企业十分有利。", "pinyin": "Zhè xiàng zhèngcè duì zhōngxiǎo qǐyè shífēn yǒulì.", "meaningVi": "Chính sách này rất có lợi cho các doanh nghiệp vừa và nhỏ."}],
    "hsk6_1689": [{"chinese": "这是一家正规的医院。", "pinyin": "Zhè shì yì jiā zhèngguī de yīyuàn.", "meaningVi": "Đây là một bệnh viện chính quy."}],
    "hsk6_1690": [{"chinese": "请把照片正面朝上放。", "pinyin": "Qǐng bǎ zhàopiàn zhèngmiàn cháo shàng fàng.", "meaningVi": "Xin đặt tấm ảnh với mặt trước hướng lên trên."}],
    "hsk6_1691": [{"chinese": "这个消息还有待证实。", "pinyin": "Zhège xiāoxi hái yǒudài zhèngshí.", "meaningVi": "Tin tức này vẫn cần được xác thực."}],
    "hsk6_1692": [{"chinese": "他一直坚持正义。", "pinyin": "Tā yìzhí jiānchí zhèngyì.", "meaningVi": "Anh ấy luôn kiên trì với công lý."}],
    "hsk6_1693": [{"chinese": "他出现了发烧的症状。", "pinyin": "Tā chūxiànle fāshāo de zhèngzhuàng.", "meaningVi": "Anh ấy xuất hiện triệu chứng sốt."}],
    "hsk6_1694": [],
    "hsk6_1695": [{"chinese": "树上长出了新枝。", "pinyin": "Shù shàng zhǎngchūle xīn zhī.", "meaningVi": "Trên cây mọc ra cành mới."}],
    "hsk6_1696": [{"chinese": "这根柱子支撑着整栋房子。", "pinyin": "Zhè gēn zhùzi zhīchēngzhe zhěng dòng fángzi.", "meaningVi": "Cây cột này chống đỡ toàn bộ ngôi nhà."}],
    "hsk6_1697": [{"chinese": "这个月的支出比较大。", "pinyin": "Zhège yuè de zhīchū bǐjiào dà.", "meaningVi": "Chi tiêu của tháng này khá lớn."}],
    "hsk6_1698": [{"chinese": "这种食物脂肪含量很高。", "pinyin": "Zhè zhǒng shíwù zhīfáng hánliàng hěn gāo.", "meaningVi": "Loại thực phẩm này có hàm lượng chất béo rất cao."}],
    "hsk6_1699": [{"chinese": "他之所以成功，是因为坚持不懈。", "pinyin": "Tā zhīsuǒyǐ chénggōng, shì yīnwèi jiānchí bú xiè.", "meaningVi": "Sở dĩ anh ấy thành công là vì kiên trì không ngừng."}],
    "hsk6_1700": [{"chinese": "今晚由他值班。", "pinyin": "Jīnwǎn yóu tā zhíbān.", "meaningVi": "Tối nay anh ấy trực ban."}],
    "hsk6_1701": [{"chinese": "他升到了更高的职位。", "pinyin": "Tā shēngdàole gèng gāo de zhíwèi.", "meaningVi": "Anh ấy đã thăng lên chức vị cao hơn."}],
    "hsk6_1702": [{"chinese": "他被任命为新的职务。", "pinyin": "Tā bèi rènmìng wéi xīn de zhíwù.", "meaningVi": "Anh ấy được bổ nhiệm vào chức vụ mới."}],
    "hsk6_1703": [{"chinese": "她是这家银行的职员。", "pinyin": "Tā shì zhè jiā yínháng de zhíyuán.", "meaningVi": "Cô ấy là nhân viên của ngân hàng này."}],
    "hsk6_1704": [{"chinese": "保护环境是每个人的职责。", "pinyin": "Bǎohù huánjìng shì měi gè rén de zhízé.", "meaningVi": "Bảo vệ môi trường là trách nhiệm của mỗi người."}],
    "hsk6_1705": [{"chinese": "我侄子今年考上了大学。", "pinyin": "Wǒ zhízi jīnnián kǎoshàngle dàxué.", "meaningVi": "Cháu trai tôi năm nay đã thi đỗ đại học."}],
    "hsk6_1706": [{"chinese": "天下雨了，我们只得取消野餐。", "pinyin": "Tiān xiàyǔ le, wǒmen zhǐdé qǔxiāo yěcān.", "meaningVi": "Trời mưa rồi, chúng tôi đành phải hủy buổi dã ngoại."}],
    "hsk6_1707": [{"chinese": "请在指定地点集合。", "pinyin": "Qǐng zài zhǐdìng dìdiǎn jíhé.", "meaningVi": "Xin tập trung tại địa điểm chỉ định."}],
    "hsk6_1708": [{"chinese": "他只顾玩手机，没听老师讲课。", "pinyin": "Tā zhǐgù wán shǒujī, méi tīng lǎoshī jiǎngkè.", "meaningVi": "Anh ấy chỉ mải chơi điện thoại, không nghe giáo viên giảng bài."}],
    "hsk6_1709": [{"chinese": "他指挥这支乐队已经十年了。", "pinyin": "Tā zhǐhuī zhè zhī yuèduì yǐjīng shí nián le.", "meaningVi": "Anh ấy chỉ huy dàn nhạc này đã mười năm rồi."}],
    "hsk6_1710": [{"chinese": "请按照指示操作。", "pinyin": "Qǐng ànzhào zhǐshì cāozuò.", "meaningVi": "Xin thao tác theo chỉ dẫn."}],
    "hsk6_1711": [{"chinese": "他因为迟到受到了指责。", "pinyin": "Tā yīnwèi chídào shòudàole zhǐzé.", "meaningVi": "Anh ấy bị chỉ trích vì đến muộn."}],
    "hsk6_1712": [{"chinese": "这种药是用中草药制成的。", "pinyin": "Zhè zhǒng yào shì yòng zhōngcǎoyào zhìchéng de.", "meaningVi": "Loại thuốc này được chế từ thảo dược."}],
    "hsk6_1713": [{"chinese": "安全意识至关重要。", "pinyin": "Ānquán yìshí zhìguān-zhòngyào.", "meaningVi": "Ý thức an toàn vô cùng quan trọng."}],
    "hsk6_1714": [{"chinese": "这个游戏可以开发孩子的智力。", "pinyin": "Zhège yóuxì kěyǐ kāifā háizi de zhìlì.", "meaningVi": "Trò chơi này có thể phát triển trí lực của trẻ."}],
    "hsk6_1715": [{"chinese": "政府加强了对河流污染的治理。", "pinyin": "Zhèngfǔ jiāqiángle duì héliú wūrǎn de zhìlǐ.", "meaningVi": "Chính phủ đã tăng cường quản trị ô nhiễm sông ngòi."}],
    "hsk6_1716": [{"chinese": "这是一家皮革制品公司。", "pinyin": "Zhè shì yì jiā pígé zhìpǐn gōngsī.", "meaningVi": "Đây là một công ty sản phẩm da."}],
    "hsk6_1717": [{"chinese": "请大家保持秩序，排队等候。", "pinyin": "Qǐng dàjiā bǎochí zhìxù, páiduì děnghòu.", "meaningVi": "Xin mọi người giữ trật tự, xếp hàng chờ đợi."}],
    "hsk6_1718": [{"chinese": "有人对这项研究结果提出了质疑。", "pinyin": "Yǒu rén duì zhè xiàng yánjiū jiéguǒ tíchūle zhìyí.", "meaningVi": "Có người đã đặt nghi vấn về kết quả nghiên cứu này."}],
    "hsk6_1719": [{"chinese": "至于具体细节，我们再商量。", "pinyin": "Zhìyú jùtǐ xìjié, wǒmen zài shāngliang.", "meaningVi": "Còn về chi tiết cụ thể, chúng ta sẽ bàn sau."}],
    "hsk6_1720": [{"chinese": "他的成绩在班里属于中等水平。", "pinyin": "Tā de chéngjì zài bān lǐ shǔyú zhōngděng shuǐpíng.", "meaningVi": "Thành tích của anh ấy trong lớp thuộc mức trung bình."}],
    "hsk6_1721": [{"chinese": "他第一个冲过了终点。", "pinyin": "Tā dì-yī gè chōngguòle zhōngdiǎn.", "meaningVi": "Anh ấy là người đầu tiên về đích."}],
    "hsk6_1722": [{"chinese": "由于停电，会议中断了。", "pinyin": "Yóuyú tíngdiàn, huìyì zhōngduàn le.", "meaningVi": "Vì mất điện, cuộc họp đã bị gián đoạn."}],
    "hsk6_1723": [{"chinese": "他把这份工作当作终身职业。", "pinyin": "Tā bǎ zhè fèn gōngzuò dàngzuò zhōngshēn zhíyè.", "meaningVi": "Anh ấy coi công việc này là nghề nghiệp suốt đời."}],
    "hsk6_1724": [{"chinese": "我等了整整一个钟头。", "pinyin": "Wǒ děngle zhěngzhěng yí gè zhōngtóu.", "meaningVi": "Tôi đã đợi trọn một tiếng đồng hồ."}],
    "hsk6_1725": [{"chinese": "会议安排在下月中旬。", "pinyin": "Huìyì ānpái zài xiàyuè zhōngxún.", "meaningVi": "Cuộc họp được sắp xếp vào trung tuần tháng sau."}],
    "hsk6_1726": [{"chinese": "广场中央矗立着一座雕像。", "pinyin": "Guǎngchǎng zhōngyāng chùlìzhe yí zuò diāoxiàng.", "meaningVi": "Ở giữa quảng trường sừng sững một bức tượng."}],
    "hsk6_1727": [{"chinese": "他的脚扭伤后肿了起来。", "pinyin": "Tā de jiǎo niǔshāng hòu zhǒngle qǐlai.", "meaningVi": "Chân anh ấy sau khi bị trẹo đã sưng lên."}],
    "hsk6_1729": [{"chinese": "爷爷一辈子都在种地。", "pinyin": "Yéye yíbèizi dōu zài zhòngdì.", "meaningVi": "Ông tôi cả đời đều làm ruộng."}],
    "hsk6_1730": [{"chinese": "他因为吃了变质食物而食物中毒。", "pinyin": "Tā yīnwèi chīle biànzhì shíwù ér shíwù zhòngdú.", "meaningVi": "Anh ấy vì ăn phải thức ăn ôi thiu mà bị ngộ độc thực phẩm."}],
    "hsk6_1731": [{"chinese": "他买彩票中奖了。", "pinyin": "Tā mǎi cǎipiào zhòngjiǎng le.", "meaningVi": "Anh ấy mua vé số trúng thưởng rồi."}],
    "hsk6_1732": [{"chinese": "他的发言得到了众人的认可。", "pinyin": "Tā de fāyán dédàole zhòngrén de rènkě.", "meaningVi": "Bài phát biểu của anh ấy được mọi người công nhận."}],
    "hsk6_1733": [{"chinese": "天太热，他中暑了。", "pinyin": "Tiān tài rè, tā zhòngshǔ le.", "meaningVi": "Trời quá nóng, anh ấy bị say nắng."}],
    "hsk6_1734": [{"chinese": "众所周知，吸烟有害健康。", "pinyin": "Zhòngsuǒzhōuzhī, xīyān yǒuhài jiànkāng.", "meaningVi": "Ai cũng biết, hút thuốc có hại cho sức khỏe."}],
    "hsk6_1735": [{"chinese": "公司把工作重心转移到了海外市场。", "pinyin": "Gōngsī bǎ gōngzuò zhòngxīn zhuǎnyí dàole hǎiwài shìchǎng.", "meaningVi": "Công ty đã chuyển trọng tâm công việc sang thị trường nước ngoài."}],
    "hsk6_1736": [{"chinese": "加利福尼亚是美国的一个州。", "pinyin": "Jiālìfúníyà shì Měiguó de yí gè zhōu.", "meaningVi": "California là một bang của Mỹ."}],
    "hsk6_1737": [{"chinese": "早上我喝了一碗粥。", "pinyin": "Zǎoshang wǒ hēle yì wǎn zhōu.", "meaningVi": "Buổi sáng tôi đã uống một bát cháo."}],
    "hsk6_1738": [{"chinese": "学校周边有很多小吃店。", "pinyin": "Xuéxiào zhōubiān yǒu hěn duō xiǎochīdiàn.", "meaningVi": "Xung quanh trường có nhiều quán ăn vặt."}],
    "hsk6_1739": [{"chinese": "服务员的服务十分周到。", "pinyin": "Fúwùyuán de fúwù shífēn zhōudào.", "meaningVi": "Sự phục vụ của nhân viên vô cùng chu đáo."}],
    "hsk6_1740": [{"chinese": "这种植物的生长周期比较短。", "pinyin": "Zhè zhǒng zhíwù de shēngzhǎng zhōuqī bǐjiào duǎn.", "meaningVi": "Chu kỳ sinh trưởng của loại thực vật này khá ngắn."}],
    "hsk6_1741": [{"chinese": "院子里种了一株桃树。", "pinyin": "Yuànzi lǐ zhòngle yì zhū táoshù.", "meaningVi": "Trong sân trồng một cây đào."}],
    "hsk6_1742": [{"chinese": "她很喜欢收藏珠宝。", "pinyin": "Tā hěn xǐhuan shōucáng zhūbǎo.", "meaningVi": "Cô ấy rất thích sưu tầm châu báu."}],
    "hsk6_1743": [{"chinese": "这个方案还存在诸多问题。", "pinyin": "Zhège fāng'àn hái cúnzài zhūduō wèntí.", "meaningVi": "Phương án này vẫn còn tồn tại nhiều vấn đề."}],
    "hsk6_1744": [{"chinese": "这次比赛由体育局主办。", "pinyin": "Zhè cì bǐsài yóu tǐyùjú zhǔbàn.", "meaningVi": "Cuộc thi lần này do sở thể thao tổ chức."}],
    "hsk6_1745": [{"chinese": "她是一名网络直播主播。", "pinyin": "Tā shì yì míng wǎngluò zhíbō zhǔbō.", "meaningVi": "Cô ấy là một người dẫn chương trình livestream."}],
    "hsk6_1746": [{"chinese": "政府在这个项目中起主导作用。", "pinyin": "Zhèngfǔ zài zhège xiàngmù zhōng qǐ zhǔdǎo zuòyòng.", "meaningVi": "Chính phủ đóng vai trò chủ đạo trong dự án này."}],
    "hsk6_1747": [{"chinese": "他是这个部门的主管。", "pinyin": "Tā shì zhège bùmén de zhǔguǎn.", "meaningVi": "Anh ấy là người phụ trách của bộ phận này."}],
    "hsk6_1748": [{"chinese": "她在这部电影中担任主角。", "pinyin": "Tā zài zhè bù diànyǐng zhōng dānrèn zhǔjué.", "meaningVi": "Cô ấy đảm nhận vai chính trong bộ phim này."}],
    "hsk6_1749": [{"chinese": "环保已经成为社会的主流观念。", "pinyin": "Huánbǎo yǐjīng chéngwéi shèhuì de zhǔliú guānniàn.", "meaningVi": "Bảo vệ môi trường đã trở thành quan niệm chủ đạo của xã hội."}],
    "hsk6_1750": [{"chinese": "这部电影由著名演员主演。", "pinyin": "Zhè bù diànyǐng yóu zhùmíng yǎnyuán zhǔyǎn.", "meaningVi": "Bộ phim này do diễn viên nổi tiếng đóng vai chính."}],
    "hsk6_1751": [{"chinese": "他主张和平解决争端。", "pinyin": "Tā zhǔzhāng hépíng jiějué zhēngduān.", "meaningVi": "Anh ấy chủ trương giải quyết tranh chấp bằng hòa bình."}],
    "hsk6_1752": [{"chinese": "朋友们送上了真诚的祝福。", "pinyin": "Péngyoumen sòngshàngle zhēnchéng de zhùfú.", "meaningVi": "Bạn bè đã gửi lời chúc phúc chân thành."}],
    "hsk6_1753": [{"chinese": "她是经理的助理。", "pinyin": "Tā shì jīnglǐ de zhùlǐ.", "meaningVi": "Cô ấy là trợ lý của giám đốc."}],
    "hsk6_1754": [{"chinese": "他是我工作上的得力助手。", "pinyin": "Tā shì wǒ gōngzuò shàng de délì zhùshǒu.", "meaningVi": "Anh ấy là trợ thủ đắc lực trong công việc của tôi."}],
    "hsk6_1755": [{"chinese": "祝愿大家身体健康。", "pinyin": "Zhùyuàn dàjiā shēntǐ jiànkāng.", "meaningVi": "Chúc mọi người sức khỏe dồi dào."}],
    "hsk6_1756": [{"chinese": "这是一片高档住宅区。", "pinyin": "Zhè shì yí piàn gāodàng zhùzhái qū.", "meaningVi": "Đây là một khu dân cư cao cấp."}],
    "hsk6_1757": [{"chinese": "这是他的代表著作。", "pinyin": "Zhè shì tā de dàibiǎo zhùzuò.", "meaningVi": "Đây là tác phẩm tiêu biểu của ông ấy."}],
    "hsk6_1758": [{"chinese": "工人正在搬砖。", "pinyin": "Gōngrén zhèngzài bān zhuān.", "meaningVi": "Công nhân đang khuân gạch."}],
    "hsk6_1759": [{"chinese": "他毕业于一所专科学校。", "pinyin": "Tā bìyè yú yì suǒ zhuānkē xuéxiào.", "meaningVi": "Anh ấy tốt nghiệp từ một trường cao đẳng chuyên khoa."}],
    "hsk6_1760": [{"chinese": "他为这项发明申请了专利。", "pinyin": "Tā wèi zhè xiàng fāmíng shēnqǐngle zhuānlì.", "meaningVi": "Anh ấy đã xin cấp bằng sáng chế cho phát minh này."}],
    "hsk6_1761": [{"chinese": "电视台制作了一期专题节目。", "pinyin": "Diànshìtái zhìzuòle yì qī zhuāntí jiémù.", "meaningVi": "Đài truyền hình đã sản xuất một tập chương trình chuyên đề."}],
    "hsk6_1762": [{"chinese": "这是残疾人专用通道。", "pinyin": "Zhè shì cánjírén zhuānyòng tōngdào.", "meaningVi": "Đây là lối đi dành riêng cho người khuyết tật."}],
    "hsk6_1763": [{"chinese": "他工作起来非常专注。", "pinyin": "Tā gōngzuò qǐlai fēicháng zhuānzhù.", "meaningVi": "Anh ấy làm việc rất chuyên chú."}],
    "hsk6_1764": [{"chinese": "请把文件转换成PDF格式。", "pinyin": "Qǐng bǎ wénjiàn zhuǎnhuàn chéng PDF géshì.", "meaningVi": "Xin chuyển đổi tài liệu sang định dạng PDF."}],
    "hsk6_1765": [{"chinese": "请把这封信转交给他。", "pinyin": "Qǐng bǎ zhè fēng xìn zhuǎnjiāo gěi tā.", "meaningVi": "Xin chuyển lá thư này cho anh ấy."}],
    "hsk6_1766": [{"chinese": "他打算把店铺转让出去。", "pinyin": "Tā dǎsuàn bǎ diànpù zhuǎnràng chūqù.", "meaningVi": "Anh ấy định chuyển nhượng cửa hàng."}],
    "hsk6_1767": [{"chinese": "她转身离开了房间。", "pinyin": "Tā zhuǎnshēn líkāile fángjiān.", "meaningVi": "Cô ấy quay người rời khỏi phòng."}],
    "hsk6_1768": [{"chinese": "医院把病人转移到了另一间病房。", "pinyin": "Yīyuàn bǎ bìngrén zhuǎnyí dàole lìng yì jiān bìngfáng.", "meaningVi": "Bệnh viện đã chuyển bệnh nhân sang một phòng bệnh khác."}],
    "hsk6_1770": [{"chinese": "请顺时针转动这个把手。", "pinyin": "Qǐng shùnshízhēn zhuàndòng zhège bǎshǒu.", "meaningVi": "Xin xoay tay cầm này theo chiều kim đồng hồ."}],
    "hsk6_1771": [{"chinese": "士兵们配备了先进的装备。", "pinyin": "Shìbīngmen pèibèile xiānjìn de zhuāngbèi.", "meaningVi": "Các binh sĩ được trang bị thiết bị tiên tiến."}],
    "hsk6_1772": [{"chinese": "农民辛勤地照料庄稼。", "pinyin": "Nóngmín xīnqín de zhàoliào zhuāngjia.", "meaningVi": "Nông dân chăm sóc mùa màng một cách cần cù."}],
    "hsk6_1773": [{"chinese": "这件事必须追究责任。", "pinyin": "Zhè jiàn shì bìxū zhuījiū zérèn.", "meaningVi": "Việc này phải truy cứu trách nhiệm."}],
    "hsk6_1774": [{"chinese": "猫在院子里捉老鼠。", "pinyin": "Māo zài yuànzi lǐ zhuō lǎoshǔ.", "meaningVi": "Con mèo bắt chuột trong sân."}],
    "hsk6_1775": [{"chinese": "他用这笔资本开了一家公司。", "pinyin": "Tā yòng zhè bǐ zīběn kāile yì jiā gōngsī.", "meaningVi": "Anh ấy dùng số vốn này để mở một công ty."}],
    "hsk6_1776": [{"chinese": "公司的资产大幅增长。", "pinyin": "Gōngsī de zīchǎn dàfú zēngzhǎng.", "meaningVi": "Tài sản của công ty tăng trưởng mạnh."}],
    "hsk6_1777": [{"chinese": "他为自己的国家感到自豪。", "pinyin": "Tā wèi zìjǐ de guójiā gǎndào zìháo.", "meaningVi": "Anh ấy cảm thấy tự hào về đất nước của mình."}],
    "hsk6_1778": [{"chinese": "这里的自来水可以直接饮用。", "pinyin": "Zhèlǐ de zìláishuǐ kěyǐ zhíjiē yǐnyòng.", "meaningVi": "Nước máy ở đây có thể uống trực tiếp."}],
    "hsk6_1779": [{"chinese": "他是一个非常自律的人。", "pinyin": "Tā shì yí gè fēicháng zìlǜ de rén.", "meaningVi": "Anh ấy là một người rất tự kỷ luật."}],
    "hsk6_1780": [{"chinese": "这部电影配有中文字幕。", "pinyin": "Zhè bù diànyǐng pèiyǒu Zhōngwén zìmù.", "meaningVi": "Bộ phim này có kèm phụ đề tiếng Trung."}],
    "hsk6_1781": [{"chinese": "心理咨询可以帮助预防自杀。", "pinyin": "Xīnlǐ zīxún kěyǐ bāngzhù yùfáng zìshā.", "meaningVi": "Tư vấn tâm lý có thể giúp phòng ngừa tự sát."}],
    "hsk6_1782": [{"chinese": "他不断进行自我反省。", "pinyin": "Tā búduàn jìnxíng zìwǒ fǎnxǐng.", "meaningVi": "Anh ấy không ngừng tự phản tỉnh bản thân."}],
    "hsk6_1783": [{"chinese": "他一个人自言自语。", "pinyin": "Tā yí gè rén zìyán-zìyǔ.", "meaningVi": "Anh ấy một mình tự nói với chính mình."}],
    "hsk6_1784": [{"chinese": "参加这次活动完全出于自愿。", "pinyin": "Cānjiā zhè cì huódòng wánquán chūyú zìyuàn.", "meaningVi": "Tham gia hoạt động lần này hoàn toàn là tự nguyện."}],
    "hsk6_1785": [{"chinese": "这是一家自助餐厅。", "pinyin": "Zhè shì yì jiā zìzhù cāntīng.", "meaningVi": "Đây là một nhà hàng tự phục vụ."}],
    "hsk6_1786": [{"chinese": "她的头发是棕色的。", "pinyin": "Tā de tóufa shì zōngsè de.", "meaningVi": "Tóc của cô ấy màu nâu."}],
    "hsk6_1787": [{"chinese": "他是这家公司的总裁。", "pinyin": "Tā shì zhè jiā gōngsī de zǒngcái.", "meaningVi": "Anh ấy là tổng giám đốc của công ty này."}],
    "hsk6_1788": [{"chinese": "这次募捐总计筹得十万元。", "pinyin": "Zhè cì mùjuān zǒngjì chóudé shí wàn yuán.", "meaningVi": "Đợt quyên góp lần này tổng cộng gây quỹ được một trăm nghìn tệ."}],
    "hsk6_1789": [{"chinese": "他担任本国总理已经五年了。", "pinyin": "Tā dānrèn běnguó zǒnglǐ yǐjīng wǔ nián le.", "meaningVi": "Ông ấy đảm nhiệm chức thủ tướng nước mình đã năm năm."}],
    "hsk6_1790": [{"chinese": "忙了一天，工作总算完成了。", "pinyin": "Mángle yì tiān, gōngzuò zǒngsuàn wánchéng le.", "meaningVi": "Bận rộn cả ngày, công việc cuối cùng cũng hoàn thành."}],
    "hsk6_1791": [{"chinese": "端午节大家都要吃粽子。", "pinyin": "Duānwǔjié dàjiā dōu yào chī zòngzi.", "meaningVi": "Tết Đoan Ngọ mọi người đều phải ăn bánh chưng."}],
    "hsk6_1792": [{"chinese": "他站在走廊里等人。", "pinyin": "Tā zhàn zài zǒuláng lǐ děng rén.", "meaningVi": "Anh ấy đứng ở hành lang chờ người."}],
    "hsk6_1793": [{"chinese": "他睡眠不足。", "pinyin": "Tā shuìmián bùzú.", "meaningVi": "Anh ấy ngủ không đủ giấc."}],
    "hsk6_1794": [{"chinese": "这些证据足以证明他的清白。", "pinyin": "Zhèxiē zhèngjù zúyǐ zhèngmíng tā de qīngbái.", "meaningVi": "Những bằng chứng này đủ để chứng minh sự trong sạch của anh ấy."}],
    "hsk6_1795": [{"chinese": "语言不通阻碍了交流。", "pinyin": "Yǔyán bùtōng zǔ'àile jiāoliú.", "meaningVi": "Bất đồng ngôn ngữ đã cản trở giao tiếp."}],
    "hsk6_1796": [{"chinese": "没有什么能阻挡他前进的脚步。", "pinyin": "Méiyǒu shénme néng zǔdǎng tā qiánjìn de jiǎobù.", "meaningVi": "Không có gì có thể ngăn cản bước tiến của anh ấy."}],
    "hsk6_1797": [{"chinese": "他深深地热爱自己的祖国。", "pinyin": "Tā shēnshēn de rè'ài zìjǐ de zǔguó.", "meaningVi": "Anh ấy yêu sâu sắc tổ quốc của mình."}],
    "hsk6_1798": [{"chinese": "我们应该铭记祖先的历史。", "pinyin": "Wǒmen yīnggāi míngjì zǔxiān de lìshǐ.", "meaningVi": "Chúng ta nên ghi nhớ lịch sử của tổ tiên."}],
    "hsk6_1799": [{"chinese": "他钻进了车底检查。", "pinyin": "Tā zuānjìnle chē dǐ jiǎnchá.", "meaningVi": "Anh ấy chui xuống gầm xe để kiểm tra."}],
    "hsk6_1800": [{"chinese": "他因犯罪而被判刑。", "pinyin": "Tā yīn fànzuì ér bèi pànxíng.", "meaningVi": "Anh ấy vì phạm tội mà bị kết án."}],
    "hsk1_011": [{"chinese": "河边有很多树。", "pinyin": "Hébiān yǒu hěn duō shù.", "meaningVi": "Bên bờ sông có nhiều cây."}],
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
