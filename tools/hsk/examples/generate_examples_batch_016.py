"""P5.10.3 (continued) -- Batch 016 (continues immediately after
examples_batch_015.json; entirely within HSK4).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch:
  - 要是 (yàoshi, "if") vs 钥匙 (yàoshi, "key"): a genuine full
    homophone pair (identical pinyin syllables AND identical tone
    pattern), not caught by the mechanical tier system (different
    `word` strings) -- given unambiguous, clearly distinct sentences
    (conditional clause vs a lost physical object).
  - 由 (yóu, "by/due to") vs 油 (yóu, "oil/grease"): same pinyin,
    different characters, distinct natural sentences.
  - 友 (yǒu, "friend", in 友好/友情/友谊) vs 有 (yǒu, "to have", in
    有趣/有效/有着): same pinyin, different characters -- six related
    records in this single batch, each kept in its own natural
    compound with no shared template.
  - 夜 (yè, in 夜晚) vs 叶 (yè, in 叶子): same pinyin, different
    characters, distinct sentences.
  - 证 (zhèng, "certificate/proof", in 证/证件) vs 正 (zhèng,
    "correct/formal", in 正常/正确/正式): same pinyin, different
    characters, kept distinct via natural compounds.

Self-caught near-template revisions made during drafting (before this
batch was finalized):
  - 印象 (yìnxiàng): first draft "他给我留下了很好的印象。" echoed the
    exact verb phrase and structure of the existing 留下 example
    (batch 012, hsk4_485: "他给我留下了深刻的印象。") -- rewritten to
    "我对他的第一印象很好。" to remove the shared 留下...印象 template.
  - 证件 (zhèngjiàn): first draft "请出示相关证件。" echoed the "请出示
    您的..." opener already used for 身份证 (batch 014, hsk4_643:
    "请出示您的身份证。") -- rewritten to "出入这里需要证件。".

Cross-batch exact-duplicate collisions found and fixed during
authoring:
  - hsk4_852 (眼镜): first draft "他戴着一副眼镜。" duplicated
    examples_batch_010.json's hsk4_132 (戴) verbatim -- rewritten to
    "我需要配一副新眼镜。".
  - hsk4_926 (者): first draft "这本书的作者是谁？" duplicated
    examples_batch_009.json's hsk4_1000 (作者) verbatim -- since 作者
    already has its own vocabulary record with that exact sentence,
    the bound-suffix demonstration for 者 was moved to a different
    -者 word (消费者, "consumer") instead: "他是一位消费者。". Re-
    verified against the full pilot+002-015 corpus with zero
    remaining exact duplicates.

Near-template (structural, not exact-string) collisions found via an
automated character-bigram Jaccard similarity pass against the full
prior corpus and fixed during authoring:
  - hsk4_859 (要是): first draft "要是明天下雨，我们就不去了。" was a
    near-template match (same "if it rains tomorrow, we won't go"
    skeleton) against 的话's existing example (batch 005, hsk3_086:
    "如果明天下雨的话，我们就不去了。") -- both mean "if", so the
    shared skeleton read as templated; rewritten to "要是你有时间，
    我们聊聊吧。".
  - hsk4_860 (钥匙): first draft "我把钥匙忘在家里了。" was almost a
    verbatim substring of the existing 哎呀 example (pilot, hsk5_002:
    "哎呀，我把钥匙忘在家里了！") -- rewritten to a different scenario,
    "这是打开大门的钥匙。".
  - hsk4_954 (纸巾): first draft "请给我一张纸巾。" was a near-template
    match against 纸's existing example (batch 008, hsk3_476: "请给我
    一张纸。", differing by only the 巾 suffix) -- rewritten to
    "桌上有一盒纸巾。".

Other productive-root families kept structurally distinct (no shared
template): 研究/研究生 (yánjiū+X); 演/演唱/演出/演员 (yǎn+X);
眼镜/眼前 (yǎn+X); 用来/用于 (yòng+X); 增加/增长 (zēng+X);
整/整个/整理 (zhěng+X); 之后/之间/之前/之中 (zhī+X, temporal/spatial
connectives kept in distinct natural contexts); 指/指出 (zhǐ+X).

Usage:
    python generate_examples_batch_016.py --dry-run
    python generate_examples_batch_016.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 16
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_016.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_844": [{"chinese": "请少放点盐。", "pinyin": "Qǐng shǎo fàng diǎn yán.", "meaningVi": "Xin cho ít muối thôi."}],
    "hsk4_846": [{"chinese": "他正在研究这个问题。", "pinyin": "Tā zhèngzài yánjiū zhège wèntí.", "meaningVi": "Anh ấy đang nghiên cứu vấn đề này."}],
    "hsk4_847": [{"chinese": "她是一名研究生。", "pinyin": "Tā shì yì míng yánjiūshēng.", "meaningVi": "Cô ấy là một nghiên cứu sinh."}],
    "hsk4_848": [{"chinese": "这个问题很严重。", "pinyin": "Zhège wèntí hěn yánzhòng.", "meaningVi": "Vấn đề này rất nghiêm trọng."}],
    "hsk4_849": [{"chinese": "他演得很好。", "pinyin": "Tā yǎn de hěn hǎo.", "meaningVi": "Anh ấy diễn rất hay."}],
    "hsk4_850": [{"chinese": "她在晚会上演唱了一首歌。", "pinyin": "Tā zài wǎnhuì shàng yǎnchàngle yì shǒu gē.", "meaningVi": "Cô ấy đã hát một bài hát trong buổi tiệc tối."}],
    "hsk4_851": [{"chinese": "今晚有一场精彩的演出。", "pinyin": "Jīnwǎn yǒu yì chǎng jīngcǎi de yǎnchū.", "meaningVi": "Tối nay có một buổi biểu diễn đặc sắc."}],
    "hsk4_852": [{"chinese": "我需要配一副新眼镜。", "pinyin": "Wǒ xūyào pèi yí fù xīn yǎnjìng.", "meaningVi": "Tôi cần làm một cặp kính mới."}],
    "hsk4_853": [{"chinese": "眼前的困难只是暂时的。", "pinyin": "Yǎnqián de kùnnan zhǐshì zànshí de.", "meaningVi": "Khó khăn trước mắt chỉ là tạm thời."}],
    "hsk4_854": [{"chinese": "她是一位有名的演员。", "pinyin": "Tā shì yí wèi yǒumíng de yǎnyuán.", "meaningVi": "Cô ấy là một diễn viên nổi tiếng."}],
    "hsk4_855": [{"chinese": "今天的阳光很好。", "pinyin": "Jīntiān de yángguāng hěn hǎo.", "meaningVi": "Ánh nắng hôm nay rất đẹp."}],
    "hsk4_856": [{"chinese": "我们要养成好习惯。", "pinyin": "Wǒmen yào yǎngchéng hǎo xíguàn.", "meaningVi": "Chúng ta phải rèn luyện thói quen tốt."}],
    "hsk4_857": [{"chinese": "这个样子看起来不错。", "pinyin": "Zhège yàngzi kàn qǐlai búcuò.", "meaningVi": "Kiểu dáng này trông khá đẹp."}],
    "hsk4_858": [{"chinese": "我邀请他来参加婚礼。", "pinyin": "Wǒ yāoqǐng tā lái cānjiā hūnlǐ.", "meaningVi": "Tôi mời anh ấy đến dự đám cưới."}],
    "hsk4_859": [{"chinese": "要是你有时间，我们聊聊吧。", "pinyin": "Yàoshi nǐ yǒu shíjiān, wǒmen liáoliao ba.", "meaningVi": "Nếu bạn có thời gian, chúng ta nói chuyện một chút nhé."}],
    "hsk4_860": [{"chinese": "这是打开大门的钥匙。", "pinyin": "Zhè shì dǎkāi dàmén de yàoshi.", "meaningVi": "Đây là chìa khóa mở cửa lớn."}],
    "hsk4_861": [{"chinese": "他也许已经知道了。", "pinyin": "Tā yěxǔ yǐjīng zhīdào le.", "meaningVi": "Có lẽ anh ấy đã biết rồi."}],
    "hsk4_863": [{"chinese": "夜晚的城市很安静。", "pinyin": "Yèwǎn de chéngshì hěn ānjìng.", "meaningVi": "Thành phố về đêm rất yên tĩnh."}],
    "hsk4_864": [{"chinese": "秋天树上的叶子都黄了。", "pinyin": "Qiūtiān shù shàng de yèzi dōu huáng le.", "meaningVi": "Mùa thu lá trên cây đều vàng cả."}],
    "hsk4_865": [{"chinese": "一切都会好起来的。", "pinyin": "Yíqiè dōu huì hǎo qǐlai de.", "meaningVi": "Mọi thứ rồi sẽ tốt lên thôi."}],
    "hsk4_866": [{"chinese": "时间已不多了。", "pinyin": "Shíjiān yǐ bù duō le.", "meaningVi": "Thời gian đã không còn nhiều nữa."}],
    "hsk4_867": [{"chinese": "请在一周以内回复。", "pinyin": "Qǐng zài yì zhōu yǐnèi huífù.", "meaningVi": "Xin phản hồi trong vòng một tuần."}],
    "hsk4_868": [{"chinese": "大家对这个计划有不同意见。", "pinyin": "Dàjiā duì zhège jìhuà yǒu bùtóng yìjiàn.", "meaningVi": "Mọi người có ý kiến khác nhau về kế hoạch này."}],
    "hsk4_869": [{"chinese": "他把一生都献给了教育事业。", "pinyin": "Tā bǎ yìshēng dōu xiàn gěile jiàoyù shìyè.", "meaningVi": "Anh ấy đã cống hiến cả đời cho sự nghiệp giáo dục."}],
    "hsk4_870": [{"chinese": "她对艺术很感兴趣。", "pinyin": "Tā duì yìshù hěn gǎn xìngqù.", "meaningVi": "Cô ấy rất hứng thú với nghệ thuật."}],
    "hsk4_871": [{"chinese": "他很努力，因此取得了好成绩。", "pinyin": "Tā hěn nǔlì, yīncǐ qǔdéle hǎo chéngjì.", "meaningVi": "Anh ấy rất chăm chỉ, vì vậy đã đạt được thành tích tốt."}],
    "hsk4_872": [{"chinese": "这个消息引起了大家的注意。", "pinyin": "Zhège xiāoxi yǐnqǐle dàjiā de zhùyì.", "meaningVi": "Tin này đã thu hút sự chú ý của mọi người."}],
    "hsk4_873": [{"chinese": "我对他的第一印象很好。", "pinyin": "Wǒ duì tā de dì-yī yìnxiàng hěn hǎo.", "meaningVi": "Ấn tượng đầu tiên của tôi về anh ấy rất tốt."}],
    "hsk4_874": [{"chinese": "我们队赢了。", "pinyin": "Wǒmen duì yíng le.", "meaningVi": "Đội chúng tôi đã thắng."}],
    "hsk4_875": [{"chinese": "他赢得了大家的尊重。", "pinyin": "Tā yíngdéle dàjiā de zūnzhòng.", "meaningVi": "Anh ấy đã giành được sự tôn trọng của mọi người."}],
    "hsk4_876": [{"chinese": "他去应聘一份新工作。", "pinyin": "Tā qù yìngpìn yí fèn xīn gōngzuò.", "meaningVi": "Anh ấy đi ứng tuyển một công việc mới."}],
    "hsk4_877": [{"chinese": "他是一个勇敢的孩子。", "pinyin": "Tā shì yí gè yǒnggǎn de háizi.", "meaningVi": "Cậu ấy là một đứa trẻ dũng cảm."}],
    "hsk4_879": [{"chinese": "这个工具是用来修车的。", "pinyin": "Zhège gōngjù shì yònglái xiūchē de.", "meaningVi": "Công cụ này được dùng để sửa xe."}],
    "hsk4_880": [{"chinese": "这笔钱将用于教育。", "pinyin": "Zhè bǐ qián jiāng yòngyú jiàoyù.", "meaningVi": "Số tiền này sẽ được dùng cho giáo dục."}],
    "hsk4_881": [{"chinese": "他有很多优点。", "pinyin": "Tā yǒu hěn duō yōudiǎn.", "meaningVi": "Anh ấy có rất nhiều ưu điểm."}],
    "hsk4_882": [{"chinese": "他说话很幽默。", "pinyin": "Tā shuōhuà hěn yōumò.", "meaningVi": "Anh ấy nói chuyện rất hài hước."}],
    "hsk4_883": [{"chinese": "她是一名优秀的学生。", "pinyin": "Tā shì yì míng yōuxiù de xuésheng.", "meaningVi": "Cô ấy là một học sinh xuất sắc."}],
    "hsk4_884": [{"chinese": "这项工作由他负责。", "pinyin": "Zhè xiàng gōngzuò yóu tā fùzé.", "meaningVi": "Công việc này do anh ấy phụ trách."}],
    "hsk4_885": [{"chinese": "妈妈用油炒菜。", "pinyin": "Māma yòng yóu chǎo cài.", "meaningVi": "Mẹ dùng dầu để xào rau."}],
    "hsk4_886": [{"chinese": "我喜欢运动，尤其是游泳。", "pinyin": "Wǒ xǐhuan yùndòng, yóuqí shì yóuyǒng.", "meaningVi": "Tôi thích thể thao, đặc biệt là bơi lội."}],
    "hsk4_887": [{"chinese": "我们打算去海边游玩。", "pinyin": "Wǒmen dǎsuàn qù hǎibiān yóuwán.", "meaningVi": "Chúng tôi định đi biển chơi."}],
    "hsk4_889": [{"chinese": "当地人对我们很友好。", "pinyin": "Dāngdì rén duì wǒmen hěn yǒuhǎo.", "meaningVi": "Người dân địa phương rất thân thiện với chúng tôi."}],
    "hsk4_890": [{"chinese": "他们之间的友情很珍贵。", "pinyin": "Tāmen zhījiān de yǒuqíng hěn zhēnguì.", "meaningVi": "Tình bạn giữa họ rất đáng quý."}],
    "hsk4_891": [{"chinese": "这本书很有趣。", "pinyin": "Zhè běn shū hěn yǒuqù.", "meaningVi": "Cuốn sách này rất thú vị."}],
    "hsk4_892": [{"chinese": "这个方法很有效。", "pinyin": "Zhège fāngfǎ hěn yǒuxiào.", "meaningVi": "Phương pháp này rất hiệu quả."}],
    "hsk4_893": [{"chinese": "我们要珍惜彼此的友谊。", "pinyin": "Wǒmen yào zhēnxī bǐcǐ de yǒuyì.", "meaningVi": "Chúng ta phải trân trọng tình hữu nghị giữa nhau."}],
    "hsk4_894": [{"chinese": "这座城市有着悠久的历史。", "pinyin": "Zhè zuò chéngshì yǒuzhe yōujiǔ de lìshǐ.", "meaningVi": "Thành phố này có lịch sử lâu đời."}],
    "hsk4_895": [{"chinese": "祝你旅途愉快。", "pinyin": "Zhù nǐ lǚtú yúkuài.", "meaningVi": "Chúc bạn có chuyến đi vui vẻ."}],
    "hsk4_896": [{"chinese": "他病了，于是请了假。", "pinyin": "Tā bìng le, yúshì qǐngle jià.", "meaningVi": "Anh ấy bị ốm, vì vậy đã xin nghỉ phép."}],
    "hsk4_898": [{"chinese": "这个语法点比较难。", "pinyin": "Zhège yǔfǎ diǎn bǐjiào nán.", "meaningVi": "Điểm ngữ pháp này khá khó."}],
    "hsk4_899": [{"chinese": "上课前请先预习课文。", "pinyin": "Shàngkè qián qǐng xiān yùxí kèwén.", "meaningVi": "Trước khi lên lớp xin hãy ôn bài trước."}],
    "hsk4_901": [{"chinese": "请原谅我的错误。", "pinyin": "Qǐng yuánliàng wǒ de cuòwù.", "meaningVi": "Xin hãy tha thứ cho lỗi lầm của tôi."}],
    "hsk4_902": [{"chinese": "请说明一下原因。", "pinyin": "Qǐng shuōmíng yíxià yuányīn.", "meaningVi": "Xin hãy giải thích nguyên nhân."}],
    "hsk4_903": [{"chinese": "我们应该远离危险。", "pinyin": "Wǒmen yīnggāi yuǎnlí wēixiǎn.", "meaningVi": "Chúng ta nên tránh xa nguy hiểm."}],
    "hsk4_904": [{"chinese": "他是这所医院的院长。", "pinyin": "Tā shì zhè suǒ yīyuàn de yuànzhǎng.", "meaningVi": "Ông ấy là viện trưởng của bệnh viện này."}],
    "hsk4_905": [{"chinese": "院子里种了很多花。", "pinyin": "Yuànzi lǐ zhòngle hěn duō huā.", "meaningVi": "Trong sân trồng rất nhiều hoa."}],
    "hsk4_908": [{"chinese": "中秋节我们吃月饼。", "pinyin": "Zhōngqiūjié wǒmen chī yuèbing.", "meaningVi": "Tết Trung thu chúng tôi ăn bánh trung thu."}],
    "hsk4_909": [{"chinese": "阅读可以增长知识。", "pinyin": "Yuèdú kěyǐ zēngzhǎng zhīshi.", "meaningVi": "Đọc sách có thể tăng thêm kiến thức."}],
    "hsk4_910": [{"chinese": "你是哪个月份出生的？", "pinyin": "Nǐ shì nǎge yuèfèn chūshēng de?", "meaningVi": "Bạn sinh vào tháng mấy?"}],
    "hsk4_911": [{"chinese": "天上飘着白云。", "pinyin": "Tiān shàng piāozhe bái yún.", "meaningVi": "Trên trời có mây trắng bay."}],
    "hsk4_912": [{"chinese": "这里不允许吸烟。", "pinyin": "Zhèlǐ bù yǔnxǔ xīyān.", "meaningVi": "Ở đây không cho phép hút thuốc."}],
    "hsk4_913": [{"chinese": "她订了一份杂志。", "pinyin": "Tā dìngle yí fèn zázhì.", "meaningVi": "Cô ấy đã đặt mua một tờ tạp chí."}],
    "hsk4_914": [{"chinese": "请再次确认信息。", "pinyin": "Qǐng zàicì quèrèn xìnxī.", "meaningVi": "Xin xác nhận lại thông tin một lần nữa."}],
    "hsk4_916": [{"chinese": "这只是暂时的困难。", "pinyin": "Zhè zhǐshì zànshí de kùnnan.", "meaningVi": "Đây chỉ là khó khăn tạm thời."}],
    "hsk4_917": [{"chinese": "比赛暂停了五分钟。", "pinyin": "Bǐsài zàntíngle wǔ fēnzhōng.", "meaningVi": "Trận đấu đã tạm dừng năm phút."}],
    "hsk4_918": [{"chinese": "早餐要吃好。", "pinyin": "Zǎocān yào chī hǎo.", "meaningVi": "Bữa sáng cần ăn cho tốt."}],
    "hsk4_919": [{"chinese": "他每天早晨都去跑步。", "pinyin": "Tā měitiān zǎochen dōu qù pǎobù.", "meaningVi": "Mỗi sáng anh ấy đều đi chạy bộ."}],
    "hsk4_920": [{"chinese": "这是我的责任。", "pinyin": "Zhè shì wǒ de zérèn.", "meaningVi": "Đây là trách nhiệm của tôi."}],
    "hsk4_921": [{"chinese": "公司决定增加员工工资。", "pinyin": "Gōngsī juédìng zēngjiā yuángōng gōngzī.", "meaningVi": "Công ty quyết định tăng lương cho nhân viên."}],
    "hsk4_922": [{"chinese": "今年的销售额增长了不少。", "pinyin": "Jīnnián de xiāoshòu'é zēngzhǎngle bù shǎo.", "meaningVi": "Doanh số năm nay đã tăng trưởng khá nhiều."}],
    "hsk4_923": [{"chinese": "公司正在招聘新员工。", "pinyin": "Gōngsī zhèngzài zhāopìn xīn yuángōng.", "meaningVi": "Công ty đang tuyển dụng nhân viên mới."}],
    "hsk4_925": [{"chinese": "厨房突然着火了。", "pinyin": "Chúfáng tūrán zháohuǒ le.", "meaningVi": "Nhà bếp đột nhiên bốc cháy."}],
    "hsk4_926": [{"chinese": "他是一位消费者。", "pinyin": "Tā shì yí wèi xiāofèizhě.", "meaningVi": "Anh ấy là một người tiêu dùng."}],
    "hsk4_928": [{"chinese": "他整整等了一个小时。", "pinyin": "Tā zhěngzhěng děngle yí gè xiǎoshí.", "meaningVi": "Anh ấy đã đợi tròn một tiếng đồng hồ."}],
    "hsk4_929": [{"chinese": "整个房间都很干净。", "pinyin": "Zhěnggè fángjiān dōu hěn gānjìng.", "meaningVi": "Cả căn phòng đều rất sạch sẽ."}],
    "hsk4_930": [{"chinese": "他在整理书桌。", "pinyin": "Tā zài zhěnglǐ shūzhuō.", "meaningVi": "Anh ấy đang sắp xếp bàn học."}],
    "hsk4_931": [{"chinese": "请带上你的证。", "pinyin": "Qǐng dài shàng nǐ de zhèng.", "meaningVi": "Xin mang theo giấy tờ của bạn."}],
    "hsk4_932": [{"chinese": "这是正常现象。", "pinyin": "Zhè shì zhèngcháng xiànxiàng.", "meaningVi": "Đây là hiện tượng bình thường."}],
    "hsk4_934": [{"chinese": "出入这里需要证件。", "pinyin": "Chūrù zhèlǐ xūyào zhèngjiàn.", "meaningVi": "Ra vào đây cần giấy tờ tùy thân."}],
    "hsk4_936": [{"chinese": "你的答案是正确的。", "pinyin": "Nǐ de dá'àn shì zhèngquè de.", "meaningVi": "Đáp án của bạn là đúng."}],
    "hsk4_937": [{"chinese": "合同已经正式生效。", "pinyin": "Hétong yǐjīng zhèngshì shēngxiào.", "meaningVi": "Hợp đồng đã chính thức có hiệu lực."}],
    "hsk4_938": [{"chinese": "百分之五十的人同意。", "pinyin": "Bǎifēnzhī wǔshí de rén tóngyì.", "meaningVi": "Năm mươi phần trăm số người đồng ý."}],
    "hsk4_939": [{"chinese": "谢谢大家的支持。", "pinyin": "Xièxie dàjiā de zhīchí.", "meaningVi": "Cảm ơn mọi người đã ủng hộ."}],
    "hsk4_940": [{"chinese": "你可以用手机支付。", "pinyin": "Nǐ kěyǐ yòng shǒujī zhīfù.", "meaningVi": "Bạn có thể thanh toán bằng điện thoại."}],
    "hsk4_941": [{"chinese": "下课之后我们去吃饭。", "pinyin": "Xiàkè zhīhòu wǒmen qù chīfàn.", "meaningVi": "Sau khi tan học chúng ta đi ăn cơm."}],
    "hsk4_942": [{"chinese": "他们之间的关系很好。", "pinyin": "Tāmen zhījiān de guānxi hěn hǎo.", "meaningVi": "Quan hệ giữa họ rất tốt."}],
    "hsk4_943": [{"chinese": "出门之前请关好门窗。", "pinyin": "Chūmén zhīqián qǐng guān hǎo ménchuāng.", "meaningVi": "Trước khi ra ngoài xin đóng cửa cẩn thận."}],
    "hsk4_944": [{"chinese": "他懂得很多知识。", "pinyin": "Tā dǒngde hěn duō zhīshi.", "meaningVi": "Anh ấy hiểu biết rất nhiều kiến thức."}],
    "hsk4_945": [{"chinese": "他生活在忙碌之中。", "pinyin": "Tā shēnghuó zài mánglù zhīzhōng.", "meaningVi": "Anh ấy sống trong sự bận rộn."}],
    "hsk4_947": [{"chinese": "这部电影值得一看。", "pinyin": "Zhè bù diànyǐng zhídé yí kàn.", "meaningVi": "Bộ phim này đáng để xem."}],
    "hsk4_948": [{"chinese": "你可以直接联系我。", "pinyin": "Nǐ kěyǐ zhíjiē liánxì wǒ.", "meaningVi": "Bạn có thể liên hệ trực tiếp với tôi."}],
    "hsk4_949": [{"chinese": "她喜欢种植物。", "pinyin": "Tā xǐhuan zhòng zhíwù.", "meaningVi": "Cô ấy thích trồng cây."}],
    "hsk4_950": [{"chinese": "你的职业是什么？", "pinyin": "Nǐ de zhíyè shì shénme?", "meaningVi": "Nghề nghiệp của bạn là gì?"}],
    "hsk4_951": [{"chinese": "他用手指着地图。", "pinyin": "Tā yòng shǒu zhǐzhe dìtú.", "meaningVi": "Anh ấy dùng tay chỉ vào bản đồ."}],
    "hsk4_952": [{"chinese": "老师指出了我的错误。", "pinyin": "Lǎoshī zhǐchūle wǒ de cuòwù.", "meaningVi": "Giáo viên đã chỉ ra lỗi sai của tôi."}],
    "hsk4_953": [{"chinese": "下雨了，我们只好留在家里。", "pinyin": "Xiàyǔ le, wǒmen zhǐhǎo liú zài jiā lǐ.", "meaningVi": "Trời mưa rồi, chúng tôi đành phải ở lại nhà."}],
    "hsk4_954": [{"chinese": "桌上有一盒纸巾。", "pinyin": "Zhuō shàng yǒu yì hé zhǐjīn.", "meaningVi": "Trên bàn có một hộp khăn giấy."}],
    "hsk4_955": [{"chinese": "这个产品的质量很好。", "pinyin": "Zhège chǎnpǐn de zhìliàng hěn hǎo.", "meaningVi": "Chất lượng của sản phẩm này rất tốt."}],
    "hsk4_956": [{"chinese": "我们至少需要三个人。", "pinyin": "Wǒmen zhìshǎo xūyào sān gè rén.", "meaningVi": "Chúng ta ít nhất cần ba người."}],
    "hsk4_957": [{"chinese": "他更喜欢吃中餐。", "pinyin": "Tā gèng xǐhuan chī zhōngcān.", "meaningVi": "Anh ấy thích ăn món Trung Quốc hơn."}],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ids, universe, tiers = get_next_batch_ids(100)

    if len(ids) != 100:
        print(f"FAIL: queue produced {len(ids)} records, expected 100", file=sys.stderr)
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
            "qaStatus": "pending",
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
