"""P5.10.3 (continued) -- Batch 023 (continues immediately after
examples_batch_022.json; entirely within HSK5). Second 300-record
batch in this phase.

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Dense same-pinyin-different-character clusters in this batch, none
flagged by the mechanical tier system (it compares the `word` string,
and every pair below is a different word):
  - 艰(jiān)苦 vs 坚(jiān)强.
  - 捡/剪/剪刀/减肥/简历/简直: FOUR characters (捡/剪/减/简) all
    jiǎn (3rd tone).
  - 建/键/渐渐/建立/键盘/建设/建造: THREE characters (建/键/渐) all
    jiàn (4th tone).
  - 讲话/奖励/讲述/讲座 vs 将近: 讲/奖 both jiǎng (3rd tone), distinct
    from 将 (jiāng, 1st tone).
  - 脚步 vs 角度: 脚/角 both jiǎo (3rd tone) -- note 角 is itself
    polyphonic (jiǎo in 角度 "angle", jué in 角色 "role", both
    appearing in this same batch and given the correct reading per
    sense).
  - 接待/阶段/接近/接收 vs (the unrelated, already-published 结构/
    结合/结论 lineage): 接/阶 both jiē (1st tone).
  - 结构/结合/结论 vs 节省: 结/节 both jié (2nd tone).
  - 紧急/尽快/尽量/紧密/谨慎: 紧/尽/谨 all jǐn (3rd tone) -- and 尽
    is itself polyphonic: jǐn in 尽快/尽量 ("as much as possible") vs
    jìn in 尽力 ("to the utmost") -- both readings appear in this
    batch and are given their correct sense.
  - 近代/进口/尽力/近年来/近期/近日/进一步: 近/进 both jìn (4th tone).
  - 精力/惊喜/经营: 精/惊/经 all jīng (1st tone).
  - 酒吧/久远 (jiǔ) vs 救/救护车/就业 (jiù): two pairs of homophones.
  - 橘子 (jú) vs 据/距/具备/剧场/巨大/据说/具有 (jù, five characters).
  - 开发/开幕/开水/开通/开业/开展: six kāi+X members.
  - 克服 vs 客服: a full exact homophone pair (both kèfú), anchored to
    unrelated referents (overcoming difficulty vs. customer support)
    to keep them unambiguous.
  - 老百姓/老板/老公/老婆 (老) vs 姥姥/姥爷 (姥): both lǎo (3rd tone).
  - 泪/泪水 (lèi) vs 类似/类型 (lèi): same pinyin+tone, different
    characters.
  - 离婚/离职 vs 厘米: 离/厘 both lí (2nd tone).
  - 立即/立刻/利益/利用 (lì) vs 力量 (lì): same pinyin+tone.
  - 良好 vs 粮食: 良/粮 both liáng (2nd tone).
  - 录/录取 vs 陆地/陆续 vs 路人/路线: 录/陆/路 all lù (4th tone),
    three characters.
  - 目光 vs 木头: 目/木 both mù (4th tone).
  - 赔 vs 陪伴 vs 培训/培养: 赔/陪/培 all péi (2nd tone), three
    characters.
  - 其/奇迹 vs 其余: 其/奇 both qí (2nd tone).
  - 墙 vs 强大/强调/强度/强烈: 墙/强 both qiáng (2nd tone).
  - 青 vs 轻重: 青/轻 both qīng (1st tone).

Sense-alignment note: 角色 (juésè)'s pinyin correctly uses the jué
reading of the polyphonic character 角 (a role/character), kept
distinct from 角度 (jiǎodù, "angle"), which uses the jiǎo reading of
the same character.

Self-caught near-duplicate revision made during drafting (before this
batch was finalized): 可见 (kějiàn)'s first draft "由此可见，这个问题
很重要。" echoed the "由此可见..." opener already used, within this
same batch, for 由此 (hsk5_1402, batch 021 lineage continuing here --
actually the same batch: "由此可见，努力是成功的关键。") -- rewritten
to "这份报告可见他做了大量调查。" to avoid the internal near-template.

Near-synonym pairs kept in genuinely distinct constructions (not
templated): 立即/立刻 (lìjí/lìkè, both "immediately"); 平安 kept
distinct from the already-published near-synonym 一路顺风 (batch 021).

Validator-caught fix (found by validate_examples_batch_p103.py's
no_duplicate_sentences_across_pilot_and_batches check): 墙 (qiáng)'s
first draft "墙上挂着一幅画。" was an EXACT duplicate of 幅's own
already-published example (batch 010, hsk4_207: "墙上挂着一幅画。").
A second draft ("他把海报贴在了墙上。") was then found, before
finalizing, to be a near-template match against 贴's own already-
published example (batch 018, hsk5_1136: "请把海报贴在墙上。") --
rewritten a second time to "这堵墙已经有几十年历史了。", which is
unrelated to both.

Automated near-template pass (character-bigram Jaccard similarity
against the full pilot+002-022 corpus) caught two further near-
duplicates fixed after the manual drafting pass:
  - 坚强 (jiānqiáng): first draft "她是一个坚强的女孩。" was a near-
    template match against 女人's own already-published example
    (batch 007, hsk3_287: "她是一个坚强的女人。", which happens to use
    坚强 as its descriptive adjective, differing from the draft by
    only 女孩/女人) -- rewritten to "无论遇到什么困难，他都很坚强。".
  - 空间 (kōngjiān): first draft "这个房间的空间很大。" was a near-
    template match against an existing HSK1-lineage example ("这个
    房间很大。") -- rewritten to "设计师充分利用了每一寸空间。".
  Both re-verified with zero remaining flags.

Usage:
    python generate_examples_batch_023.py --dry-run
    python generate_examples_batch_023.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 23
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_023.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk5_557": [{"chinese": "他每天帮妈妈做家务。", "pinyin": "Tā měitiān bāng māma zuò jiāwù.", "meaningVi": "Anh ấy mỗi ngày đều giúp mẹ làm việc nhà."}],
    "hsk5_559": [{"chinese": "假如明天不下雨，我们就去爬山。", "pinyin": "Jiǎrú míngtiān bú xiàyǔ, wǒmen jiù qù páshān.", "meaningVi": "Giả sử ngày mai không mưa, chúng ta sẽ đi leo núi."}],
    "hsk5_561": [{"chinese": "请系好安全带再驾驶。", "pinyin": "Qǐng jì hǎo ānquándài zài jiàshǐ.", "meaningVi": "Xin thắt dây an toàn trước khi lái xe."}],
    "hsk5_562": [{"chinese": "他刚拿到驾照。", "pinyin": "Tā gāng nádào jiàzhào.", "meaningVi": "Anh ấy vừa mới lấy được bằng lái xe."}],
    "hsk5_563": [{"chinese": "这幅画很有价值。", "pinyin": "Zhè fú huà hěn yǒu jiàzhí.", "meaningVi": "Bức tranh này rất có giá trị."}],
    "hsk5_564": [{"chinese": "他经历了艰苦的岁月。", "pinyin": "Tā jīnglìle jiānkǔ de suìyuè.", "meaningVi": "Anh ấy đã trải qua những năm tháng gian khổ."}],
    "hsk5_565": [{"chinese": "无论遇到什么困难，他都很坚强。", "pinyin": "Wúlùn yùdào shénme kùnnan, tā dōu hěn jiānqiáng.", "meaningVi": "Dù gặp phải khó khăn gì, anh ấy cũng đều rất kiên cường."}],
    "hsk5_566": [{"chinese": "他在路上捡到一个钱包。", "pinyin": "Tā zài lù shàng jiǎndào yí gè qiánbāo.", "meaningVi": "Anh ấy nhặt được một cái ví trên đường."}],
    "hsk5_567": [{"chinese": "请帮我剪一下头发。", "pinyin": "Qǐng bāng wǒ jiǎn yíxià tóufa.", "meaningVi": "Xin giúp tôi cắt tóc một chút."}],
    "hsk5_568": [{"chinese": "请把剪刀递给我。", "pinyin": "Qǐng bǎ jiǎndāo dì gěi wǒ.", "meaningVi": "Xin đưa cây kéo cho tôi."}],
    "hsk5_569": [{"chinese": "她最近在减肥。", "pinyin": "Tā zuìjìn zài jiǎnféi.", "meaningVi": "Gần đây cô ấy đang giảm cân."}],
    "hsk5_570": [{"chinese": "请把你的简历发给我。", "pinyin": "Qǐng bǎ nǐ de jiǎnlì fā gěi wǒ.", "meaningVi": "Xin gửi sơ yếu lý lịch của bạn cho tôi."}],
    "hsk5_571": [{"chinese": "这个价格简直太贵了。", "pinyin": "Zhège jiàgé jiǎnzhí tài guì le.", "meaningVi": "Giá này thật quá đắt."}],
    "hsk5_572": [{"chinese": "这里要建一座桥。", "pinyin": "Zhèlǐ yào jiàn yí zuò qiáo.", "meaningVi": "Ở đây sẽ xây một cây cầu."}],
    "hsk5_573": [{"chinese": "请按下这个键。", "pinyin": "Qǐng ànxià zhège jiàn.", "meaningVi": "Xin bấm phím này."}],
    "hsk5_574": [{"chinese": "天渐渐黑了。", "pinyin": "Tiān jiànjiàn hēi le.", "meaningVi": "Trời dần dần tối lại."}],
    "hsk5_575": [{"chinese": "我们建立了长期合作关系。", "pinyin": "Wǒmen jiànlìle chángqī hézuò guānxi.", "meaningVi": "Chúng tôi đã thiết lập mối quan hệ hợp tác lâu dài."}],
    "hsk5_576": [{"chinese": "他的键盘坏了。", "pinyin": "Tā de jiànpán huài le.", "meaningVi": "Bàn phím của anh ấy bị hỏng."}],
    "hsk5_577": [{"chinese": "这个城市正在大力建设。", "pinyin": "Zhège chéngshì zhèngzài dàlì jiànshè.", "meaningVi": "Thành phố này đang được xây dựng mạnh mẽ."}],
    "hsk5_578": [{"chinese": "这座宫殿建造于明朝。", "pinyin": "Zhè zuò gōngdiàn jiànzào yú Míngcháo.", "meaningVi": "Cung điện này được xây dựng vào thời nhà Minh."}],
    "hsk5_580": [{"chinese": "他工作将近十年了。", "pinyin": "Tā gōngzuò jiāngjìn shí nián le.", "meaningVi": "Anh ấy đã làm việc gần mười năm rồi."}],
    "hsk5_581": [{"chinese": "校长在会上讲话。", "pinyin": "Xiàozhǎng zài huì shàng jiǎnghuà.", "meaningVi": "Hiệu trưởng phát biểu trong cuộc họp."}],
    "hsk5_583": [{"chinese": "学校奖励了表现优秀的学生。", "pinyin": "Xuéxiào jiǎnglìle biǎoxiàn yōuxiù de xuésheng.", "meaningVi": "Nhà trường đã khen thưởng những học sinh có thành tích xuất sắc."}],
    "hsk5_584": [{"chinese": "他向我们讲述了这段历史。", "pinyin": "Tā xiàng wǒmen jiǎngshùle zhè duàn lìshǐ.", "meaningVi": "Anh ấy đã kể cho chúng tôi nghe về giai đoạn lịch sử này."}],
    "hsk5_585": [{"chinese": "今天下午有一场讲座。", "pinyin": "Jīntiān xiàwǔ yǒu yì chǎng jiǎngzuò.", "meaningVi": "Chiều nay có một buổi diễn thuyết."}],
    "hsk5_586": [{"chinese": "今年夏天降水量偏多。", "pinyin": "Jīnnián xiàtiān jiàngshuǐliàng piān duō.", "meaningVi": "Mùa hè năm nay lượng mưa hơi nhiều."}],
    "hsk5_587": [{"chinese": "别忘了给花浇水。", "pinyin": "Bié wàngle gěi huā jiāo shuǐ.", "meaningVi": "Đừng quên tưới nước cho hoa."}],
    "hsk5_588": [{"chinese": "我们交换了联系方式。", "pinyin": "Wǒmen jiāohuànle liánxì fāngshì.", "meaningVi": "Chúng tôi đã trao đổi cách liên lạc."}],
    "hsk5_589": [{"chinese": "他们已经交往三年了。", "pinyin": "Tāmen yǐjīng jiāowǎng sān nián le.", "meaningVi": "Họ đã hẹn hò được ba năm rồi."}],
    "hsk5_591": [{"chinese": "他放慢了脚步。", "pinyin": "Tā fàngmànle jiǎobù.", "meaningVi": "Anh ấy chậm bước chân lại."}],
    "hsk5_592": [{"chinese": "请换个角度想问题。", "pinyin": "Qǐng huàn gè jiǎodù xiǎng wèntí.", "meaningVi": "Xin hãy suy nghĩ vấn đề theo góc độ khác."}],
    "hsk5_594": [{"chinese": "这本教材内容很丰富。", "pinyin": "Zhè běn jiàocái nèiróng hěn fēngfù.", "meaningVi": "Nội dung của giáo trình này rất phong phú."}],
    "hsk5_596": [{"chinese": "公司热情接待了客人。", "pinyin": "Gōngsī rèqíng jiēdàile kèren.", "meaningVi": "Công ty đã tiếp đón khách nhiệt tình."}],
    "hsk5_597": [{"chinese": "项目进入了新阶段。", "pinyin": "Xiàngmù jìnrùle xīn jiēduàn.", "meaningVi": "Dự án đã bước vào giai đoạn mới."}],
    "hsk5_598": [{"chinese": "天气逐渐接近夏天。", "pinyin": "Tiānqì zhújiàn jiējìn xiàtiān.", "meaningVi": "Thời tiết dần dần tiến gần đến mùa hè."}],
    "hsk5_599": [{"chinese": "我没有接收到你的信息。", "pinyin": "Wǒ méiyǒu jiēshōu dào nǐ de xìnxī.", "meaningVi": "Tôi đã không nhận được tin nhắn của bạn."}],
    "hsk5_601": [{"chinese": "这个句子的结构很复杂。", "pinyin": "Zhège jùzi de jiégòu hěn fùzá.", "meaningVi": "Cấu trúc của câu này rất phức tạp."}],
    "hsk5_602": [{"chinese": "理论要与实践相结合。", "pinyin": "Lǐlùn yào yǔ shíjiàn xiāng jiéhé.", "meaningVi": "Lý thuyết phải kết hợp với thực tiễn."}],
    "hsk5_603": [{"chinese": "我们得出了相同的结论。", "pinyin": "Wǒmen déchūle xiāngtóng de jiélùn.", "meaningVi": "Chúng tôi đã rút ra kết luận giống nhau."}],
    "hsk5_604": [{"chinese": "这种方法可以节省时间。", "pinyin": "Zhè zhǒng fāngfǎ kěyǐ jiéshěng shíjiān.", "meaningVi": "Phương pháp này có thể tiết kiệm thời gian."}],
    "hsk5_606": [{"chinese": "今日新闻有哪些？", "pinyin": "Jīnrì xīnwén yǒu nǎxiē?", "meaningVi": "Tin tức hôm nay có những gì?"}],
    "hsk5_608": [{"chinese": "这是一个紧急情况。", "pinyin": "Zhè shì yí gè jǐnjí qíngkuàng.", "meaningVi": "Đây là một tình huống khẩn cấp."}],
    "hsk5_609": [{"chinese": "请尽快回复我。", "pinyin": "Qǐng jǐnkuài huífù wǒ.", "meaningVi": "Xin phản hồi cho tôi càng sớm càng tốt."}],
    "hsk5_610": [{"chinese": "请尽量早点到。", "pinyin": "Qǐng jǐnliàng zǎo diǎn dào.", "meaningVi": "Xin cố gắng đến sớm hơn."}],
    "hsk5_611": [{"chinese": "这两个问题紧密相关。", "pinyin": "Zhè liǎng gè wèntí jǐnmì xiāngguān.", "meaningVi": "Hai vấn đề này có liên quan mật thiết với nhau."}],
    "hsk5_612": [{"chinese": "做决定时要谨慎。", "pinyin": "Zuò juédìng shí yào jǐnshèn.", "meaningVi": "Khi đưa ra quyết định phải thận trọng."}],
    "hsk5_614": [{"chinese": "这是近代历史上的重要事件。", "pinyin": "Zhè shì jìndài lìshǐ shàng de zhòngyào shìjiàn.", "meaningVi": "Đây là sự kiện quan trọng trong lịch sử cận đại."}],
    "hsk5_615": [{"chinese": "这些水果都是进口的。", "pinyin": "Zhèxiē shuǐguǒ dōu shì jìnkǒu de.", "meaningVi": "Những loại trái cây này đều là hàng nhập khẩu."}],
    "hsk5_616": [{"chinese": "我会尽力帮助你。", "pinyin": "Wǒ huì jìnlì bāngzhù nǐ.", "meaningVi": "Tôi sẽ cố hết sức giúp bạn."}],
    "hsk5_617": [{"chinese": "近年来这个城市变化很大。", "pinyin": "Jìnnián lái zhège chéngshì biànhuà hěn dà.", "meaningVi": "Những năm gần đây thành phố này thay đổi rất nhiều."}],
    "hsk5_618": [{"chinese": "近期不宜出行。", "pinyin": "Jìnqī bù yí chūxíng.", "meaningVi": "Thời gian gần đây không thích hợp để đi lại."}],
    "hsk5_619": [{"chinese": "近日天气比较凉爽。", "pinyin": "Jìnrì tiānqì bǐjiào liángshuǎng.", "meaningVi": "Mấy ngày gần đây thời tiết khá mát mẻ."}],
    "hsk5_620": [{"chinese": "我们需要进一步讨论。", "pinyin": "Wǒmen xūyào jìnyíbù tǎolùn.", "meaningVi": "Chúng ta cần thảo luận thêm một bước nữa."}],
    "hsk5_622": [{"chinese": "他把精力都放在工作上。", "pinyin": "Tā bǎ jīnglì dōu fàng zài gōngzuò shàng.", "meaningVi": "Anh ấy dồn hết tâm sức vào công việc."}],
    "hsk5_624": [{"chinese": "这真是一个惊喜。", "pinyin": "Zhè zhēnshi yí gè jīngxǐ.", "meaningVi": "Đây thực sự là một điều bất ngờ vui mừng."}],
    "hsk5_625": [{"chinese": "他经营着一家小店。", "pinyin": "Tā jīngyíngzhe yì jiā xiǎo diàn.", "meaningVi": "Anh ấy đang kinh doanh một cửa hàng nhỏ."}],
    "hsk5_627": [{"chinese": "周末他们喜欢去酒吧。", "pinyin": "Zhōumò tāmen xǐhuan qù jiǔbā.", "meaningVi": "Cuối tuần họ thích đi quán bar."}],
    "hsk5_628": [{"chinese": "这个传统年代久远。", "pinyin": "Zhège chuántǒng niándài jiǔyuǎn.", "meaningVi": "Truyền thống này có từ rất lâu đời."}],
    "hsk5_629": [{"chinese": "消防员救出了被困的孩子。", "pinyin": "Xiāofángyuán jiùchūle bèi kùn de háizi.", "meaningVi": "Lính cứu hỏa đã cứu được đứa trẻ bị mắc kẹt."}],
    "hsk5_630": [{"chinese": "救护车很快就到了。", "pinyin": "Jiùhùchē hěn kuài jiù dào le.", "meaningVi": "Xe cứu thương đã đến rất nhanh."}],
    "hsk5_631": [{"chinese": "大学生就业压力很大。", "pinyin": "Dàxuéshēng jiùyè yālì hěn dà.", "meaningVi": "Áp lực tìm việc của sinh viên đại học rất lớn."}],
    "hsk5_632": [{"chinese": "小区居民都很友好。", "pinyin": "Xiǎoqū jūmín dōu hěn yǒuhǎo.", "meaningVi": "Cư dân trong khu dân cư đều rất thân thiện."}],
    "hsk5_634": [{"chinese": "他一直居住在这座城市。", "pinyin": "Tā yìzhí jūzhù zài zhè zuò chéngshì.", "meaningVi": "Anh ấy luôn cư trú tại thành phố này."}],
    "hsk5_635": [{"chinese": "我买了一袋橘子。", "pinyin": "Wǒ mǎile yí dài júzi.", "meaningVi": "Tôi đã mua một túi quýt."}],
    "hsk5_636": [{"chinese": "据报道，明天会下雪。", "pinyin": "Jù bàodào, míngtiān huì xiàxuě.", "meaningVi": "Theo báo cáo, ngày mai sẽ có tuyết."}],
    "hsk5_637": [{"chinese": "学校距我家不远。", "pinyin": "Xuéxiào jù wǒ jiā bù yuǎn.", "meaningVi": "Trường học cách nhà tôi không xa."}],
    "hsk5_638": [{"chinese": "他具备了应聘的条件。", "pinyin": "Tā jùbèile yìngpìn de tiáojiàn.", "meaningVi": "Anh ấy đã có đủ điều kiện để ứng tuyển."}],
    "hsk5_639": [{"chinese": "这座剧场能容纳上千人。", "pinyin": "Zhè zuò jùchǎng néng róngnà shàng qiān rén.", "meaningVi": "Nhà hát này có thể chứa hàng nghìn người."}],
    "hsk5_640": [{"chinese": "这项发现具有巨大意义。", "pinyin": "Zhè xiàng fāxiàn jùyǒu jùdà yìyì.", "meaningVi": "Phát hiện này có ý nghĩa to lớn."}],
    "hsk5_641": [{"chinese": "据说这家店的菜很好吃。", "pinyin": "Jùshuō zhè jiā diàn de cài hěn hǎochī.", "meaningVi": "Nghe nói món ăn của quán này rất ngon."}],
    "hsk5_643": [{"chinese": "这件文物具有很高的历史价值。", "pinyin": "Zhè jiàn wénwù jùyǒu hěn gāo de lìshǐ jiàzhí.", "meaningVi": "Món cổ vật này có giá trị lịch sử rất cao."}],
    "hsk5_644": [{"chinese": "他捐了一笔钱给灾区。", "pinyin": "Tā juānle yì bǐ qián gěi zāiqū.", "meaningVi": "Anh ấy đã quyên góp một khoản tiền cho vùng bị thiên tai."}],
    "hsk5_647": [{"chinese": "她在这部电影里演一个重要角色。", "pinyin": "Tā zài zhè bù diànyǐng lǐ yǎn yí gè zhòngyào juésè.", "meaningVi": "Cô ấy đóng một vai quan trọng trong bộ phim này."}],
    "hsk5_649": [{"chinese": "公司正在开发新产品。", "pinyin": "Gōngsī zhèngzài kāifā xīn chǎnpǐn.", "meaningVi": "Công ty đang phát triển sản phẩm mới."}],
    "hsk5_651": [{"chinese": "运动会明天开幕。", "pinyin": "Yùndònghuì míngtiān kāimù.", "meaningVi": "Đại hội thể thao sẽ khai mạc vào ngày mai."}],
    "hsk5_653": [{"chinese": "请喝点开水。", "pinyin": "Qǐng hē diǎn kāishuǐ.", "meaningVi": "Xin uống chút nước sôi để nguội."}],
    "hsk5_654": [{"chinese": "这条地铁线路刚开通。", "pinyin": "Zhè tiáo dìtiě xiànlù gāng kāitōng.", "meaningVi": "Tuyến tàu điện ngầm này vừa mới thông xe."}],
    "hsk5_655": [{"chinese": "这家餐厅下周开业。", "pinyin": "Zhè jiā cāntīng xiàzhōu kāiyè.", "meaningVi": "Nhà hàng này khai trương vào tuần sau."}],
    "hsk5_656": [{"chinese": "学校开展了各种活动。", "pinyin": "Xuéxiào kāizhǎnle gèzhǒng huódòng.", "meaningVi": "Nhà trường đã triển khai nhiều hoạt động khác nhau."}],
    "hsk5_658": [{"chinese": "他去医院看望病人。", "pinyin": "Tā qù yīyuàn kànwàng bìngrén.", "meaningVi": "Anh ấy đến bệnh viện thăm bệnh nhân."}],
    "hsk5_659": [{"chinese": "大家把他看作榜样。", "pinyin": "Dàjiā bǎ tā kànzuò bǎngyàng.", "meaningVi": "Mọi người coi anh ấy như tấm gương."}],
    "hsk5_660": [{"chinese": "请不要靠着门站。", "pinyin": "Qǐng búyào kàozhe mén zhàn.", "meaningVi": "Xin đừng dựa vào cửa mà đứng."}],
    "hsk5_661": [{"chinese": "请不要靠近施工区域。", "pinyin": "Qǐng búyào kàojìn shīgōng qūyù.", "meaningVi": "Xin đừng đến gần khu vực đang thi công."}],
    "hsk5_663": [{"chinese": "他一直从事科研工作。", "pinyin": "Tā yìzhí cóngshì kēyán gōngzuò.", "meaningVi": "Anh ấy luôn làm công tác nghiên cứu khoa học."}],
    "hsk5_664": [{"chinese": "这份报告可见他做了大量调查。", "pinyin": "Zhè fèn bàogào kějiàn tā zuòle dàliàng diàochá.", "meaningVi": "Từ bản báo cáo này có thể thấy anh ấy đã làm rất nhiều điều tra."}],
    "hsk5_665": [{"chinese": "这个消息来源可靠吗？", "pinyin": "Zhège xiāoxi láiyuán kěkào ma?", "meaningVi": "Nguồn tin này có đáng tin cậy không?"}],
    "hsk5_666": [{"chinese": "那只是一场可怕的梦。", "pinyin": "Nà zhǐshì yì chǎng kěpà de mèng.", "meaningVi": "Đó chỉ là một giấc mơ đáng sợ."}],
    "hsk5_667": [{"chinese": "我们一定能克服困难。", "pinyin": "Wǒmen yídìng néng kèfú kùnnan.", "meaningVi": "Chúng ta nhất định có thể khắc phục khó khăn."}],
    "hsk5_668": [{"chinese": "有问题可以联系客服。", "pinyin": "Yǒu wèntí kěyǐ liánxì kèfú.", "meaningVi": "Có vấn đề gì có thể liên hệ bộ phận chăm sóc khách hàng."}],
    "hsk5_669": [{"chinese": "请客观地评价这件事。", "pinyin": "Qǐng kèguān de píngjià zhè jiàn shì.", "meaningVi": "Xin đánh giá việc này một cách khách quan."}],
    "hsk5_670": [{"chinese": "他正在和客户谈生意。", "pinyin": "Tā zhèngzài hé kèhù tán shēngyì.", "meaningVi": "Anh ấy đang bàn công việc kinh doanh với khách hàng."}],
    "hsk5_671": [{"chinese": "设计师充分利用了每一寸空间。", "pinyin": "Shèjìshī chōngfèn lìyòngle měi yí cùn kōngjiān.", "meaningVi": "Nhà thiết kế đã tận dụng triệt để từng tấc không gian."}],
    "hsk5_674": [{"chinese": "他把手放进口袋里。", "pinyin": "Tā bǎ shǒu fàng jìn kǒudai lǐ.", "meaningVi": "Anh ấy cho tay vào túi."}],
    "hsk5_675": [{"chinese": "每个人的口味不一样。", "pinyin": "Měi gè rén de kǒuwèi bù yíyàng.", "meaningVi": "Khẩu vị của mỗi người đều không giống nhau."}],
    "hsk5_676": [{"chinese": "这批货放在仓库里。", "pinyin": "Zhè pī huò fàng zài cāngkù lǐ.", "meaningVi": "Lô hàng này được để trong kho."}],
    "hsk5_678": [{"chinese": "请测量一下门的宽度。", "pinyin": "Qǐng cèliáng yíxià mén de kuāndù.", "meaningVi": "Xin đo chiều rộng của cánh cửa."}],
    "hsk5_679": [{"chinese": "亏你提醒我，不然就忘了。", "pinyin": "Kuī nǐ tíxǐng wǒ, bùrán jiù wàng le.", "meaningVi": "May mà bạn nhắc tôi, nếu không thì đã quên mất."}],
    "hsk5_680": [{"chinese": "他对昆虫很感兴趣。", "pinyin": "Tā duì kūnchóng hěn gǎn xìngqù.", "meaningVi": "Anh ấy rất hứng thú với côn trùng."}],
    "hsk5_681": [{"chinese": "公司决定扩大规模。", "pinyin": "Gōngsī juédìng kuòdà guīmó.", "meaningVi": "Công ty quyết định mở rộng quy mô."}],
    "hsk5_684": [{"chinese": "这项政策关系到老百姓的利益。", "pinyin": "Zhè xiàng zhèngcè guānxi dào lǎobǎixìng de lìyì.", "meaningVi": "Chính sách này liên quan đến lợi ích của dân chúng."}],
    "hsk5_685": [{"chinese": "他是这家店的老板。", "pinyin": "Tā shì zhè jiā diàn de lǎobǎn.", "meaningVi": "Anh ấy là ông chủ của cửa hàng này."}],
    "hsk5_686": [{"chinese": "她的老公在外地工作。", "pinyin": "Tā de lǎogōng zài wàidì gōngzuò.", "meaningVi": "Chồng của cô ấy làm việc ở nơi khác."}],
    "hsk5_687": [{"chinese": "我从小跟姥姥一起长大。", "pinyin": "Wǒ cóngxiǎo gēn lǎolao yìqǐ zhǎngdà.", "meaningVi": "Tôi lớn lên cùng bà ngoại từ nhỏ."}],
    "hsk5_688": [{"chinese": "他很疼爱自己的老婆。", "pinyin": "Tā hěn téng'ài zìjǐ de lǎopo.", "meaningVi": "Anh ấy rất yêu thương vợ của mình."}],
    "hsk5_689": [{"chinese": "姥爷喜欢下棋。", "pinyin": "Lǎoye xǐhuan xiàqí.", "meaningVi": "Ông ngoại thích chơi cờ."}],
    "hsk5_690": [{"chinese": "他是个乐观的人。", "pinyin": "Tā shì gè lèguān de rén.", "meaningVi": "Anh ấy là một người lạc quan."}],
    "hsk5_691": [{"chinese": "学习也能找到乐趣。", "pinyin": "Xuéxí yě néng zhǎodào lèqù.", "meaningVi": "Học tập cũng có thể tìm thấy niềm vui."}],
    "hsk5_692": [{"chinese": "她眼里含着泪。", "pinyin": "Tā yǎn lǐ hánzhe lèi.", "meaningVi": "Trong mắt cô ấy chứa đầy nước mắt."}],
    "hsk5_694": [{"chinese": "泪水从她脸上滑落。", "pinyin": "Lèishuǐ cóng tā liǎn shàng huáluò.", "meaningVi": "Nước mắt lăn dài trên má cô ấy."}],
    "hsk5_695": [{"chinese": "我遇到过类似的情况。", "pinyin": "Wǒ yùdàoguo lèisì de qíngkuàng.", "meaningVi": "Tôi đã từng gặp tình huống tương tự."}],
    "hsk5_696": [{"chinese": "这是一种新的产品类型。", "pinyin": "Zhè shì yì zhǒng xīn de chǎnpǐn lèixíng.", "meaningVi": "Đây là một loại hình sản phẩm mới."}],
    "hsk5_698": [{"chinese": "他们已经离婚了。", "pinyin": "Tāmen yǐjīng líhūn le.", "meaningVi": "Họ đã ly hôn rồi."}],
    "hsk5_699": [{"chinese": "这张桌子长八十厘米。", "pinyin": "Zhè zhāng zhuōzi cháng bāshí límǐ.", "meaningVi": "Cái bàn này dài tám mươi centimet."}],
    "hsk5_700": [{"chinese": "他上个月离职了。", "pinyin": "Tā shàng gè yuè lízhí le.", "meaningVi": "Tháng trước anh ấy đã nghỉ việc."}],
    "hsk5_702": [{"chinese": "箱子里头是什么？", "pinyin": "Xiāngzi lǐtou shì shénme?", "meaningVi": "Bên trong hộp là gì?"}],
    "hsk5_703": [{"chinese": "他没有给出理由。", "pinyin": "Tā méiyǒu gěichū lǐyóu.", "meaningVi": "Anh ấy đã không đưa ra lý do."}],
    "hsk5_705": [{"chinese": "请立即处理这件事。", "pinyin": "Qǐng lìjí chǔlǐ zhè jiàn shì.", "meaningVi": "Xin xử lý việc này ngay lập tức."}],
    "hsk5_706": [{"chinese": "他听到消息立刻赶了过去。", "pinyin": "Tā tīngdào xiāoxi lìkè gǎnle guòqù.", "meaningVi": "Anh ấy nghe tin liền chạy đến ngay."}],
    "hsk5_707": [{"chinese": "团结就是力量。", "pinyin": "Tuánjié jiù shì lìliàng.", "meaningVi": "Đoàn kết chính là sức mạnh."}],
    "hsk5_709": [{"chinese": "这样做符合大家的利益。", "pinyin": "Zhèyàng zuò fúhé dàjiā de lìyì.", "meaningVi": "Làm như vậy phù hợp với lợi ích của mọi người."}],
    "hsk5_710": [{"chinese": "请充分利用这次机会。", "pinyin": "Qǐng chōngfèn lìyòng zhè cì jīhuì.", "meaningVi": "Xin tận dụng triệt để cơ hội lần này."}],
    "hsk5_712": [{"chinese": "这座桥连接两个岛屿。", "pinyin": "Zhè zuò qiáo liánjiē liǎng gè dǎoyǔ.", "meaningVi": "Cây cầu này kết nối hai hòn đảo."}],
    "hsk5_713": [{"chinese": "他连忙道歉。", "pinyin": "Tā liánmáng dàoqiàn.", "meaningVi": "Anh ấy vội vàng xin lỗi."}],
    "hsk5_714": [{"chinese": "他连续三年获奖。", "pinyin": "Tā liánxù sān nián huòjiǎng.", "meaningVi": "Anh ấy liên tục ba năm đoạt giải."}],
    "hsk5_715": [{"chinese": "他今天脸色不太好。", "pinyin": "Tā jīntiān liǎnsè bú tài hǎo.", "meaningVi": "Hôm nay sắc mặt của anh ấy không tốt lắm."}],
    "hsk5_717": [{"chinese": "他养成了良好的习惯。", "pinyin": "Tā yǎngchéngle liánghǎo de xíguàn.", "meaningVi": "Anh ấy đã hình thành thói quen tốt."}],
    "hsk5_718": [{"chinese": "这里盛产粮食。", "pinyin": "Zhèlǐ shèngchǎn liángshi.", "meaningVi": "Nơi đây sản xuất nhiều lương thực."}],
    "hsk5_720": [{"chinese": "他真是个了不起的人。", "pinyin": "Tā zhēnshi gè liǎobuqǐ de rén.", "meaningVi": "Anh ấy thật sự là một người giỏi giang."}],
    "hsk5_721": [{"chinese": "这趟列车马上就要出发了。", "pinyin": "Zhè tàng lièchē mǎshàng jiù yào chūfā le.", "meaningVi": "Chuyến tàu này sắp xuất phát rồi."}],
    "hsk5_724": [{"chinese": "他处理问题很灵活。", "pinyin": "Tā chǔlǐ wèntí hěn línghuó.", "meaningVi": "Anh ấy xử lý vấn đề rất linh hoạt."}],
    "hsk5_726": [{"chinese": "他今天打了一条领带。", "pinyin": "Tā jīntiān dǎle yì tiáo lǐngdài.", "meaningVi": "Hôm nay anh ấy thắt một chiếc cà vạt."}],
    "hsk5_728": [{"chinese": "请到前台领取奖品。", "pinyin": "Qǐng dào qiántái lǐngqǔ jiǎngpǐn.", "meaningVi": "Xin đến quầy lễ tân nhận giải thưởng."}],
    "hsk5_729": [{"chinese": "目前他们队领先两分。", "pinyin": "Mùqián tāmen duì lǐngxiān liǎng fēn.", "meaningVi": "Hiện tại đội của họ đang dẫn trước hai điểm."}],
    "hsk5_730": [{"chinese": "他在这个领域很有名气。", "pinyin": "Tā zài zhège lǐngyù hěn yǒu míngqì.", "meaningVi": "Anh ấy rất có tiếng tăm trong lĩnh vực này."}],
    "hsk5_732": [{"chinese": "这个故事一直流传至今。", "pinyin": "Zhège gùshi yìzhí liúchuán zhìjīn.", "meaningVi": "Câu chuyện này được lưu truyền đến tận bây giờ."}],
    "hsk5_733": [{"chinese": "最近流感很流行。", "pinyin": "Zuìjìn liúgǎn hěn liúxíng.", "meaningVi": "Gần đây bệnh cúm rất phổ biến."}],
    "hsk5_734": [{"chinese": "我随便浏览了一下网页。", "pinyin": "Wǒ suíbiàn liúlǎnle yíxià wǎngyè.", "meaningVi": "Tôi lướt qua trang web một chút."}],
    "hsk5_736": [{"chinese": "龙是中国传统文化的象征。", "pinyin": "Lóng shì Zhōngguó chuántǒng wénhuà de xiàngzhēng.", "meaningVi": "Rồng là biểu tượng văn hóa truyền thống của Trung Quốc."}],
    "hsk5_738": [{"chinese": "请把这段话录下来。", "pinyin": "Qǐng bǎ zhè duàn huà lù xiàlai.", "meaningVi": "Xin ghi âm lại đoạn nói này."}],
    "hsk5_739": [{"chinese": "鲸鱼是水生动物，不是陆地动物。", "pinyin": "Jīngyú shì shuǐshēng dòngwù, bú shì lùdì dòngwù.", "meaningVi": "Cá voi là động vật sống dưới nước, không phải động vật trên cạn."}],
    "hsk5_740": [{"chinese": "他被这所大学录取了。", "pinyin": "Tā bèi zhè suǒ dàxué lùqǔ le.", "meaningVi": "Anh ấy đã được trường đại học này tuyển chọn."}],
    "hsk5_741": [{"chinese": "一位路人帮她捡起了钱包。", "pinyin": "Yí wèi lùrén bāng tā jiǎnqǐle qiánbāo.", "meaningVi": "Một người qua đường đã giúp cô ấy nhặt lại ví."}],
    "hsk5_742": [{"chinese": "请选择最短的路线。", "pinyin": "Qǐng xuǎnzé zuì duǎn de lùxiàn.", "meaningVi": "Xin chọn tuyến đường ngắn nhất."}],
    "hsk5_743": [{"chinese": "客人们陆续到达了。", "pinyin": "Kèrénmen lùxù dàodá le.", "meaningVi": "Khách khứa lần lượt đến nơi."}],
    "hsk5_745": [{"chinese": "他们通过旅行社预订了机票。", "pinyin": "Tāmen tōngguò lǚxíngshè yùdìngle jīpiào.", "meaningVi": "Họ đã đặt vé máy bay thông qua công ty du lịch."}],
    "hsk5_746": [{"chinese": "他正在写毕业论文。", "pinyin": "Tā zhèngzài xiě bìyè lùnwén.", "meaningVi": "Anh ấy đang viết luận văn tốt nghiệp."}],
    "hsk5_747": [{"chinese": "他的话很有逻辑。", "pinyin": "Tā de huà hěn yǒu luójí.", "meaningVi": "Lời nói của anh ấy rất có logic."}],
    "hsk5_749": [{"chinese": "这笔买卖很划算。", "pinyin": "Zhè bǐ mǎimai hěn huásuàn.", "meaningVi": "Phi vụ mua bán này rất hời."}],
    "hsk5_750": [{"chinese": "这个方案不能满足所有人的需求。", "pinyin": "Zhège fāng'àn bù néng mǎnzú suǒyǒu rén de xūqiú.", "meaningVi": "Phương án này không thể đáp ứng nhu cầu của tất cả mọi người."}],
    "hsk5_751": [{"chinese": "他每天的生活都很忙碌。", "pinyin": "Tā měitiān de shēnghuó dōu hěn mánglù.", "meaningVi": "Cuộc sống hàng ngày của anh ấy rất bận rộn."}],
    "hsk5_752": [{"chinese": "他用毛笔写字。", "pinyin": "Tā yòng máobǐ xiězì.", "meaningVi": "Anh ấy viết chữ bằng bút lông."}],
    "hsk5_753": [{"chinese": "这台机器出毛病了。", "pinyin": "Zhè tái jīqì chū máobìng le.", "meaningVi": "Cái máy này bị hỏng rồi."}],
    "hsk5_755": [{"chinese": "这事儿我真没法儿解决。", "pinyin": "Zhè shìr wǒ zhēn méifǎr jiějué.", "meaningVi": "Việc này tôi thực sự không có cách nào giải quyết."}],
    "hsk5_756": [{"chinese": "他送了她一束玫瑰。", "pinyin": "Tā sòngle tā yí shù méigui.", "meaningVi": "Anh ấy đã tặng cô ấy một bó hoa hồng."}],
    "hsk5_757": [{"chinese": "这件事引起了媒体的关注。", "pinyin": "Zhè jiàn shì yǐnqǐle méitǐ de guānzhù.", "meaningVi": "Việc này đã thu hút sự chú ý của truyền thông."}],
    "hsk5_758": [{"chinese": "她从小学习美术。", "pinyin": "Tā cóngxiǎo xuéxí měishù.", "meaningVi": "Cô ấy học mỹ thuật từ nhỏ."}],
    "hsk5_759": [{"chinese": "这道菜非常美味。", "pinyin": "Zhè dào cài fēicháng měiwèi.", "meaningVi": "Món ăn này vô cùng ngon miệng."}],
    "hsk5_760": [{"chinese": "她很有个人魅力。", "pinyin": "Tā hěn yǒu gèrén mèilì.", "meaningVi": "Cô ấy có sức hút cá nhân rất lớn."}],
    "hsk5_761": [{"chinese": "医院今天不开门诊。", "pinyin": "Yīyuàn jīntiān bù kāi ménzhěn.", "meaningVi": "Hôm nay bệnh viện không có khám ngoại trú."}],
    "hsk5_762": [{"chinese": "他是个足球迷。", "pinyin": "Tā shì gè zúqiú mí.", "meaningVi": "Anh ấy là một fan bóng đá."}],
    "hsk5_763": [{"chinese": "我们在山里迷路了。", "pinyin": "Wǒmen zài shān lǐ mílù le.", "meaningVi": "Chúng tôi bị lạc đường trong núi."}],
    "hsk5_766": [{"chinese": "她是经理的秘书。", "pinyin": "Tā shì jīnglǐ de mìshū.", "meaningVi": "Cô ấy là thư ký của giám đốc."}],
    "hsk5_767": [{"chinese": "事情有很多面。", "pinyin": "Shìqing yǒu hěn duō miàn.", "meaningVi": "Sự việc có nhiều mặt."}],
    "hsk5_768": [{"chinese": "这套房子的面积是九十平米。", "pinyin": "Zhè tào fángzi de miànjī shì jiǔshí píngmǐ.", "meaningVi": "Diện tích của căn nhà này là chín mươi mét vuông."}],
    "hsk5_769": [{"chinese": "公司目前面临一些困难。", "pinyin": "Gōngsī mùqián miànlín yìxiē kùnnan.", "meaningVi": "Công ty hiện đang đối mặt với một số khó khăn."}],
    "hsk5_770": [{"chinese": "这个产品面向年轻消费者。", "pinyin": "Zhège chǎnpǐn miànxiàng niánqīng xiāofèizhě.", "meaningVi": "Sản phẩm này hướng tới người tiêu dùng trẻ tuổi."}],
    "hsk5_771": [{"chinese": "请描述一下当时的情况。", "pinyin": "Qǐng miáoshù yíxià dāngshí de qíngkuàng.", "meaningVi": "Xin miêu tả lại tình hình lúc đó."}],
    "hsk5_773": [{"chinese": "这家公司的名称改变了。", "pinyin": "Zhè jiā gōngsī de míngchēng gǎibiàn le.", "meaningVi": "Tên gọi của công ty này đã thay đổi."}],
    "hsk5_774": [{"chinese": "她喜欢买名牌包。", "pinyin": "Tā xǐhuan mǎi míngpái bāo.", "meaningVi": "Cô ấy thích mua túi xách thương hiệu nổi tiếng."}],
    "hsk5_775": [{"chinese": "请给我一张名片。", "pinyin": "Qǐng gěi wǒ yì zhāng míngpiàn.", "meaningVi": "Xin cho tôi một tấm danh thiếp."}],
    "hsk5_777": [{"chinese": "他的进步很明显。", "pinyin": "Tā de jìnbù hěn míngxiǎn.", "meaningVi": "Sự tiến bộ của anh ấy rất rõ ràng."}],
    "hsk5_778": [{"chinese": "她是一位当红明星。", "pinyin": "Tā shì yí wèi dāng hóng míngxīng.", "meaningVi": "Cô ấy là một ngôi sao đang nổi tiếng."}],
    "hsk5_779": [{"chinese": "这是命中注定的。", "pinyin": "Zhè shì mìngzhōng zhùdìng de.", "meaningVi": "Đây là do số phận đã định."}],
    "hsk5_780": [{"chinese": "他改变了自己的命运。", "pinyin": "Tā gǎibiànle zìjǐ de mìngyùn.", "meaningVi": "Anh ấy đã thay đổi vận mệnh của chính mình."}],
    "hsk5_781": [{"chinese": "小心，别摸那个东西。", "pinyin": "Xiǎoxīn, bié mō nàge dōngxi.", "meaningVi": "Cẩn thận, đừng sờ vào thứ đó."}],
    "hsk5_783": [{"chinese": "这是一种新的商业模式。", "pinyin": "Zhè shì yì zhǒng xīn de shāngyè móshì.", "meaningVi": "Đây là một mô hình kinh doanh mới."}],
    "hsk5_784": [{"chinese": "这个地方对我很陌生。", "pinyin": "Zhège dìfang duì wǒ hěn mòshēng.", "meaningVi": "Nơi này rất xa lạ đối với tôi."}],
    "hsk5_785": [{"chinese": "某天他突然出现了。", "pinyin": "Mǒu tiān tā tūrán chūxiàn le.", "meaningVi": "Một ngày nào đó anh ấy đột nhiên xuất hiện."}],
    "hsk5_786": [{"chinese": "大家的目光都集中在他身上。", "pinyin": "Dàjiā de mùguāng dōu jízhōng zài tā shēnshang.", "meaningVi": "Ánh mắt của mọi người đều tập trung vào anh ấy."}],
    "hsk5_787": [{"chinese": "这张桌子是木头做的。", "pinyin": "Zhè zhāng zhuōzi shì mùtou zuò de.", "meaningVi": "Cái bàn này được làm bằng gỗ."}],
    "hsk5_788": [{"chinese": "哪怕再苦再累，他也不放弃。", "pinyin": "Nǎpà zài kǔ zài lèi, tā yě bú fàngqì.", "meaningVi": "Dù có khổ có mệt đến đâu, anh ấy cũng không từ bỏ."}],
    "hsk5_789": [{"chinese": "这是一次难得的机会。", "pinyin": "Zhè shì yí cì nándé de jīhuì.", "meaningVi": "Đây là một cơ hội hiếm có."}],
    "hsk5_790": [{"chinese": "这道题的难度很大。", "pinyin": "Zhè dào tí de nándù hěn dà.", "meaningVi": "Độ khó của bài toán này rất lớn."}],
    "hsk5_791": [{"chinese": "他的心情难以形容。", "pinyin": "Tā de xīnqíng nányǐ xíngróng.", "meaningVi": "Tâm trạng của anh ấy khó mà miêu tả được."}],
    "hsk5_792": [{"chinese": "那位男子看起来很年轻。", "pinyin": "Nà wèi nánzǐ kàn qǐlai hěn niánqīng.", "meaningVi": "Người đàn ông đó trông rất trẻ."}],
    "hsk5_794": [{"chinese": "我把闹钟定在七点。", "pinyin": "Wǒ bǎ nàozhōng dìng zài qī diǎn.", "meaningVi": "Tôi đặt đồng hồ báo thức lúc bảy giờ."}],
    "hsk5_795": [{"chinese": "这是公司内部的消息。", "pinyin": "Zhè shì gōngsī nèibù de xiāoxi.", "meaningVi": "Đây là tin tức nội bộ của công ty."}],
    "hsk5_796": [{"chinese": "她是个很能干的女人。", "pinyin": "Tā shì gè hěn nénggàn de nǚrén.", "meaningVi": "Cô ấy là một người phụ nữ rất giỏi giang."}],
    "hsk5_797": [{"chinese": "这是年初制定的计划。", "pinyin": "Zhè shì niánchū zhìdìng de jìhuà.", "meaningVi": "Đây là kế hoạch được lập ra vào đầu năm."}],
    "hsk5_798": [{"chinese": "那是一个特殊的年代。", "pinyin": "Nà shì yí gè tèshū de niándài.", "meaningVi": "Đó là một thời đại đặc biệt."}],
    "hsk5_799": [{"chinese": "他的年纪比我大。", "pinyin": "Tā de niánjì bǐ wǒ dà.", "meaningVi": "Tuổi tác của anh ấy lớn hơn tôi."}],
    "hsk5_800": [{"chinese": "全家人一起吃年夜饭。", "pinyin": "Quánjiā rén yìqǐ chī niányèfàn.", "meaningVi": "Cả nhà cùng nhau ăn bữa cơm tất niên."}],
    "hsk5_801": [{"chinese": "请把这段课文念一遍。", "pinyin": "Qǐng bǎ zhè duàn kèwén niàn yí biàn.", "meaningVi": "Xin đọc lại đoạn bài văn này một lần."}],
    "hsk5_803": [{"chinese": "这杯咖啡太浓了。", "pinyin": "Zhè bēi kāfēi tài nóng le.", "meaningVi": "Cốc cà phê này quá đậm."}],
    "hsk5_804": [{"chinese": "农民正在地里劳作。", "pinyin": "Nóngmín zhèngzài dì lǐ láozuò.", "meaningVi": "Nông dân đang lao động trên đồng ruộng."}],
    "hsk5_805": [{"chinese": "这个国家以农业为主。", "pinyin": "Zhège guójiā yǐ nóngyè wéi zhǔ.", "meaningVi": "Quốc gia này chủ yếu phát triển nông nghiệp."}],
    "hsk5_806": [{"chinese": "那位女子非常优雅。", "pinyin": "Nà wèi nǚzǐ fēicháng yōuyǎ.", "meaningVi": "Người phụ nữ đó vô cùng thanh lịch."}],
    "hsk5_807": [{"chinese": "哦，原来是这样。", "pinyin": "Ò, yuánlái shì zhèyàng.", "meaningVi": "Ồ, hóa ra là như vậy."}],
    "hsk5_808": [{"chinese": "他打算去欧洲旅行。", "pinyin": "Tā dǎsuàn qù Ōuzhōu lǚxíng.", "meaningVi": "Anh ấy định đi du lịch châu Âu."}],
    "hsk5_809": [{"chinese": "这次相遇纯属偶然。", "pinyin": "Zhè cì xiāngyù chúnshǔ ǒurán.", "meaningVi": "Cuộc gặp gỡ lần này hoàn toàn là ngẫu nhiên."}],
    "hsk5_810": [{"chinese": "这部电影是在云南拍摄的。", "pinyin": "Zhè bù diànyǐng shì zài Yúnnán pāishè de.", "meaningVi": "Bộ phim này được quay tại Vân Nam."}],
    "hsk5_811": [{"chinese": "请按顺序排列这些数字。", "pinyin": "Qǐng àn shùnxù páiliè zhèxiē shùzì.", "meaningVi": "Xin sắp xếp những con số này theo thứ tự."}],
    "hsk5_813": [{"chinese": "他去派出所报了案。", "pinyin": "Tā qù pàichūsuǒ bàole àn.", "meaningVi": "Anh ấy đã đến đồn công an trình báo."}],
    "hsk5_814": [{"chinese": "飞机正在跑道上滑行。", "pinyin": "Fēijī zhèngzài pǎodào shàng huáxíng.", "meaningVi": "Máy bay đang di chuyển trên đường băng."}],
    "hsk5_815": [{"chinese": "他把弄坏的东西赔给了对方。", "pinyin": "Tā bǎ nònghuài de dōngxi péi gěile duìfāng.", "meaningVi": "Anh ấy đã đền cho bên kia món đồ đã làm hỏng."}],
    "hsk5_816": [{"chinese": "谢谢你一直陪伴着我。", "pinyin": "Xièxie nǐ yìzhí péibànzhe wǒ.", "meaningVi": "Cảm ơn bạn đã luôn ở bên đồng hành cùng tôi."}],
    "hsk5_817": [{"chinese": "新员工需要参加培训。", "pinyin": "Xīn yuángōng xūyào cānjiā péixùn.", "meaningVi": "Nhân viên mới cần tham gia đào tạo."}],
    "hsk5_818": [{"chinese": "学校很重视培养学生的能力。", "pinyin": "Xuéxiào hěn zhòngshì péiyǎng xuésheng de nénglì.", "meaningVi": "Nhà trường rất coi trọng việc bồi dưỡng năng lực của học sinh."}],
    "hsk5_820": [{"chinese": "谢谢大家的配合。", "pinyin": "Xièxie dàjiā de pèihé.", "meaningVi": "Cảm ơn sự phối hợp của mọi người."}],
    "hsk5_821": [{"chinese": "这家超市提供免费配送服务。", "pinyin": "Zhè jiā chāoshì tígōng miǎnfèi pèisòng fúwù.", "meaningVi": "Siêu thị này cung cấp dịch vụ giao hàng miễn phí."}],
    "hsk5_823": [{"chinese": "小心别碰到桌角。", "pinyin": "Xiǎoxīn bié pèngdào zhuōjiǎo.", "meaningVi": "Cẩn thận đừng va vào góc bàn."}],
    "hsk5_824": [{"chinese": "我在路上碰见了老朋友。", "pinyin": "Wǒ zài lù shàng pèngjiànle lǎo péngyou.", "meaningVi": "Tôi đã tình cờ gặp bạn cũ trên đường."}],
    "hsk5_827": [{"chinese": "他的申请被批准了。", "pinyin": "Tā de shēnqǐng bèi pīzhǔn le.", "meaningVi": "Đơn xin của anh ấy đã được phê duyệt."}],
    "hsk5_829": [{"chinese": "他被骗走了不少钱。", "pinyin": "Tā bèi piànzǒule bù shǎo qián.", "meaningVi": "Anh ấy đã bị lừa mất không ít tiền."}],
    "hsk5_830": [{"chinese": "请把这些碎片拼在一起。", "pinyin": "Qǐng bǎ zhèxiē suìpiàn pīn zài yìqǐ.", "meaningVi": "Xin ghép những mảnh vỡ này lại với nhau."}],
    "hsk5_831": [{"chinese": "学汉字要先学拼音。", "pinyin": "Xué Hànzì yào xiān xué pīnyīn.", "meaningVi": "Học chữ Hán phải học phiên âm trước."}],
    "hsk5_833": [{"chinese": "这是一个国际知名品牌。", "pinyin": "Zhè shì yí gè guójì zhīmíng pǐnpái.", "meaningVi": "Đây là một thương hiệu nổi tiếng quốc tế."}],
    "hsk5_834": [{"chinese": "这款产品的品质很好。", "pinyin": "Zhè kuǎn chǎnpǐn de pǐnzhì hěn hǎo.", "meaningVi": "Chất lượng của sản phẩm này rất tốt."}],
    "hsk5_835": [{"chinese": "这种苹果是新品种。", "pinyin": "Zhè zhǒng píngguǒ shì xīn pǐnzhǒng.", "meaningVi": "Loại táo này là giống mới."}],
    "hsk5_836": [{"chinese": "公司聘请了一位专家。", "pinyin": "Gōngsī pìnqǐngle yí wèi zhuānjiā.", "meaningVi": "Công ty đã thuê một chuyên gia."}],
    "hsk5_838": [{"chinese": "请给这篇文章评个分。", "pinyin": "Qǐng gěi zhè piān wénzhāng píng gè fēn.", "meaningVi": "Xin chấm điểm cho bài viết này."}],
    "hsk5_840": [{"chinese": "祝你一路平安。", "pinyin": "Zhù nǐ yílù píng'ān.", "meaningVi": "Chúc bạn thượng lộ bình an."}],
    "hsk5_843": [{"chinese": "他凭借努力获得了成功。", "pinyin": "Tā píngjiè nǔlì huòdéle chénggōng.", "meaningVi": "Anh ấy đã đạt được thành công nhờ vào sự nỗ lực."}],
    "hsk5_844": [{"chinese": "湖面十分平静。", "pinyin": "Húmiàn shífēn píngjìng.", "meaningVi": "Mặt hồ vô cùng yên tĩnh."}],
    "hsk5_846": [{"chinese": "手机屏幕碎了。", "pinyin": "Shǒujī píngmù suì le.", "meaningVi": "Màn hình điện thoại đã bị vỡ."}],
    "hsk5_847": [{"chinese": "这是一个网络购物平台。", "pinyin": "Zhè shì yí gè wǎngluò gòuwù píngtái.", "meaningVi": "Đây là một nền tảng mua sắm trực tuyến."}],
    "hsk5_848": [{"chinese": "请不要破坏公共设施。", "pinyin": "Qǐng búyào pòhuài gōnggòng shèshī.", "meaningVi": "Xin đừng phá hoại cơ sở vật chất công cộng."}],
    "hsk5_849": [{"chinese": "智能手机已经普及了。", "pinyin": "Zhìnéng shǒujī yǐjīng pǔjí le.", "meaningVi": "Điện thoại thông minh đã được phổ cập rồi."}],
    "hsk5_850": [{"chinese": "我很期待这次旅行。", "pinyin": "Wǒ hěn qīdài zhè cì lǚxíng.", "meaningVi": "Tôi rất mong đợi chuyến du lịch lần này."}],
    "hsk5_851": [{"chinese": "假期期间他在家休息。", "pinyin": "Jiàqī qījiān tā zài jiā xiūxi.", "meaningVi": "Trong kỳ nghỉ anh ấy nghỉ ngơi ở nhà."}],
    "hsk5_853": [{"chinese": "他有两个孩子，其一在上大学。", "pinyin": "Tā yǒu liǎng gè háizi, qí yī zài shàng dàxué.", "meaningVi": "Anh ấy có hai đứa con, một trong số đó đang học đại học."}],
    "hsk5_854": [{"chinese": "医生创造了一个奇迹。", "pinyin": "Yīshēng chuàngzàole yí gè qíjì.", "meaningVi": "Bác sĩ đã tạo ra một kỳ tích."}],
    "hsk5_855": [{"chinese": "其余的问题以后再说。", "pinyin": "Qíyú de wèntí yǐhòu zài shuō.", "meaningVi": "Những vấn đề còn lại để sau nói."}],
    "hsk5_856": [{"chinese": "这是一家大型企业。", "pinyin": "Zhè shì yì jiā dàxíng qǐyè.", "meaningVi": "Đây là một doanh nghiệp quy mô lớn."}],
    "hsk5_857": [{"chinese": "孩子们拿着气球玩耍。", "pinyin": "Háizimen názhe qìqiú wánshuǎ.", "meaningVi": "Bọn trẻ cầm bóng bay chơi đùa."}],
    "hsk5_858": [{"chinese": "汽油价格又涨了。", "pinyin": "Qìyóu jiàgé yòu zhǎng le.", "meaningVi": "Giá xăng lại tăng rồi."}],
    "hsk5_860": [{"chinese": "双方正式签订了合同。", "pinyin": "Shuāngfāng zhèngshì qiāndìngle hétong.", "meaningVi": "Hai bên đã chính thức ký kết hợp đồng."}],
    "hsk5_863": [{"chinese": "队伍继续向前进。", "pinyin": "Duìwu jìxù xiàng qián jìn.", "meaningVi": "Đội ngũ tiếp tục tiến về phía trước."}],
    "hsk5_864": [{"chinese": "请大家准时前来参加。", "pinyin": "Qǐng dàjiā zhǔnshí qiánlái cānjiā.", "meaningVi": "Xin mọi người đến đúng giờ tham gia."}],
    "hsk5_865": [{"chinese": "他对自己的前途很有信心。", "pinyin": "Tā duì zìjǐ de qiántú hěn yǒu xìnxīn.", "meaningVi": "Anh ấy rất tự tin vào tiền đồ của mình."}],
    "hsk5_866": [{"chinese": "他明天前往上海出差。", "pinyin": "Tā míngtiān qiánwǎng Shànghǎi chūchāi.", "meaningVi": "Ngày mai anh ấy đi công tác đến Thượng Hải."}],
    "hsk5_867": [{"chinese": "这条河很浅。", "pinyin": "Zhè tiáo hé hěn qiǎn.", "meaningVi": "Con sông này rất nông."}],
    "hsk5_869": [{"chinese": "这堵墙已经有几十年历史了。", "pinyin": "Zhè dǔ qiáng yǐjīng yǒu jǐshí nián lìshǐ le.", "meaningVi": "Bức tường này đã có lịch sử mấy chục năm rồi."}],
    "hsk5_870": [{"chinese": "这个国家的经济十分强大。", "pinyin": "Zhège guójiā de jīngjì shífēn qiángdà.", "meaningVi": "Kinh tế của quốc gia này vô cùng hùng mạnh."}],
    "hsk5_871": [{"chinese": "老师反复强调这个知识点。", "pinyin": "Lǎoshī fǎnfù qiángdiào zhège zhīshidiǎn.", "meaningVi": "Giáo viên nhiều lần nhấn mạnh điểm kiến thức này."}],
    "hsk5_872": [{"chinese": "这项工作强度很大。", "pinyin": "Zhè xiàng gōngzuò qiángdù hěn dà.", "meaningVi": "Cường độ của công việc này rất lớn."}],
    "hsk5_873": [{"chinese": "大家强烈反对这个决定。", "pinyin": "Dàjiā qiángliè fǎnduì zhège juédìng.", "meaningVi": "Mọi người kịch liệt phản đối quyết định này."}],
    "hsk5_875": [{"chinese": "医生正在抢救伤员。", "pinyin": "Yīshēng zhèngzài qiǎngjiù shāngyuán.", "meaningVi": "Bác sĩ đang cấp cứu người bị thương."}],
    "hsk5_877": [{"chinese": "请把西瓜切成小块。", "pinyin": "Qǐng bǎ xīguā qiē chéng xiǎo kuài.", "meaningVi": "Xin cắt dưa hấu thành từng miếng nhỏ."}],
    "hsk5_879": [{"chinese": "亲爱的朋友们，大家好。", "pinyin": "Qīn'ài de péngyoumen, dàjiā hǎo.", "meaningVi": "Các bạn thân mến, xin chào mọi người."}],
    "hsk5_880": [{"chinese": "婚礼上来了很多亲朋好友。", "pinyin": "Hūnlǐ shàng láile hěn duō qīnpéng-hǎoyǒu.", "meaningVi": "Trong đám cưới có rất nhiều bạn bè và người thân đến."}],
    "hsk5_881": [{"chinese": "她说话的语气很亲切。", "pinyin": "Tā shuōhuà de yǔqì hěn qīnqiè.", "meaningVi": "Giọng điệu nói chuyện của cô ấy rất thân thiết."}],
    "hsk5_882": [{"chinese": "亲情是最珍贵的感情。", "pinyin": "Qīnqíng shì zuì zhēnguì de gǎnqíng.", "meaningVi": "Tình thân là tình cảm quý giá nhất."}],
    "hsk5_883": [{"chinese": "过年了，大家都想和亲人团聚。", "pinyin": "Guònián le, dàjiā dōu xiǎng hé qīnrén tuánjù.", "meaningVi": "Tết đến rồi, mọi người đều muốn đoàn tụ với người thân."}],
    "hsk5_884": [{"chinese": "经理亲自接待了客户。", "pinyin": "Jīnglǐ qīnzì jiēdàile kèhù.", "meaningVi": "Giám đốc đã đích thân tiếp đón khách hàng."}],
    "hsk5_885": [{"chinese": "他学习很勤奋。", "pinyin": "Tā xuéxí hěn qínfèn.", "meaningVi": "Anh ấy học tập rất cần cù."}],
    "hsk5_886": [{"chinese": "春天山上一片青绿。", "pinyin": "Chūntiān shān shàng yí piàn qīnglǜ.", "meaningVi": "Mùa xuân trên núi một màu xanh biếc."}],
    "hsk5_888": [{"chinese": "他做事分不清轻重。", "pinyin": "Tā zuòshì fēn bù qīng qīngzhòng.", "meaningVi": "Anh ấy làm việc không phân biệt được cái nào quan trọng hơn."}],
    "hsk5_889": [{"chinese": "这首诗表达了作者的情感。", "pinyin": "Zhè shǒu shī biǎodále zuòzhě de qínggǎn.", "meaningVi": "Bài thơ này thể hiện tình cảm của tác giả."}],
    "hsk5_890": [{"chinese": "那个情景我至今难忘。", "pinyin": "Nàge qíngjǐng wǒ zhìjīn nánwàng.", "meaningVi": "Cảnh tượng đó đến nay tôi vẫn không quên được."}],
    "hsk5_891": [{"chinese": "请注意控制自己的情绪。", "pinyin": "Qǐng zhùyì kòngzhì zìjǐ de qíngxù.", "meaningVi": "Xin chú ý kiểm soát tâm trạng của bản thân."}],
    "hsk5_892": [{"chinese": "我想向您请教一个问题。", "pinyin": "Wǒ xiǎng xiàng nín qǐngjiào yí gè wèntí.", "meaningVi": "Tôi muốn thỉnh giáo ngài một vấn đề."}],
    "hsk5_894": [{"chinese": "他小时候家里很穷。", "pinyin": "Tā xiǎoshíhou jiā lǐ hěn qióng.", "meaningVi": "Lúc nhỏ nhà anh ấy rất nghèo."}],
    "hsk5_895": [{"chinese": "这是未来发展的趋势。", "pinyin": "Zhè shì wèilái fāzhǎn de qūshì.", "meaningVi": "Đây là xu hướng phát triển trong tương lai."}],
    "hsk5_896": [{"chinese": "这个区域禁止停车。", "pinyin": "Zhège qūyù jìnzhǐ tíngchē.", "meaningVi": "Khu vực này cấm đỗ xe."}],
    "hsk5_897": [{"chinese": "他的祖父去年去世了。", "pinyin": "Tā de zǔfù qùnián qùshì le.", "meaningVi": "Ông nội của anh ấy đã qua đời năm ngoái."}],
    "hsk5_899": [{"chinese": "每个人都有受教育的权利。", "pinyin": "Měi gè rén dōu yǒu shòu jiàoyù de quánlì.", "meaningVi": "Mỗi người đều có quyền được giáo dục."}],
    "hsk5_901": [{"chinese": "请全面分析这个问题。", "pinyin": "Qǐng quánmiàn fēnxī zhège wèntí.", "meaningVi": "Xin phân tích toàn diện vấn đề này."}],
    "hsk5_902": [{"chinese": "全体员工都参加了会议。", "pinyin": "Quántǐ yuángōng dōu cānjiāle huìyì.", "meaningVi": "Toàn thể nhân viên đều đã tham gia cuộc họp."}],
    "hsk5_903": [{"chinese": "这是一款全新的手机。", "pinyin": "Zhè shì yì kuǎn quánxīn de shǒujī.", "meaningVi": "Đây là một mẫu điện thoại hoàn toàn mới."}],
    "hsk5_906": [{"chinese": "我们要确保产品质量。", "pinyin": "Wǒmen yào quèbǎo chǎnpǐn zhìliàng.", "meaningVi": "Chúng ta phải đảm bảo chất lượng sản phẩm."}],
    "hsk5_908": [{"chinese": "请确认一下您的地址。", "pinyin": "Qǐng quèrèn yíxià nín de dìzhǐ.", "meaningVi": "Xin xác nhận địa chỉ của bạn."}],
    "hsk5_910": [{"chinese": "老年人是一个需要关注的群体。", "pinyin": "Lǎonián rén shì yí gè xūyào guānzhù de qúntǐ.", "meaningVi": "Người cao tuổi là một nhóm cần được quan tâm."}],
    "hsk5_911": [{"chinese": "木柴正在燃烧。", "pinyin": "Mùchái zhèngzài ránshāo.", "meaningVi": "Củi đang cháy."}],
    "hsk5_912": [{"chinese": "前面堵车，我们绕道走吧。", "pinyin": "Qiánmiàn dǔchē, wǒmen ràodào zǒu ba.", "meaningVi": "Phía trước tắc đường, chúng ta đi đường vòng đi."}],
    "hsk5_913": [{"chinese": "他热爱自己的工作。", "pinyin": "Tā rè'ài zìjǐ de gōngzuò.", "meaningVi": "Anh ấy yêu thích công việc của mình."}],
    "hsk5_914": [{"chinese": "运动可以消耗热量。", "pinyin": "Yùndòng kěyǐ xiāohào rèliàng.", "meaningVi": "Vận động có thể tiêu hao nhiệt lượng."}],
    "hsk5_915": [{"chinese": "大家热烈鼓掌欢迎他。", "pinyin": "Dàjiā rèliè gǔzhǎng huānyíng tā.", "meaningVi": "Mọi người vỗ tay nhiệt liệt chào đón anh ấy."}],
    "hsk5_916": [{"chinese": "他是个热心肠的人。", "pinyin": "Tā shì gè rèxīncháng de rén.", "meaningVi": "Anh ấy là một người nhiệt tình."}],
    "hsk5_917": [{"chinese": "公司急需招募人才。", "pinyin": "Gōngsī jíxū zhāomù réncái.", "meaningVi": "Công ty đang rất cần tuyển mộ nhân tài."}],
    "hsk5_919": [{"chinese": "良好的人际关系很重要。", "pinyin": "Liánghǎo de rénjì guānxi hěn zhòngyào.", "meaningVi": "Mối quan hệ giữa người với người tốt đẹp rất quan trọng."}],
    "hsk5_920": [{"chinese": "这个城市的人口超过一千万。", "pinyin": "Zhège chéngshì de rénkǒu chāoguò yìqiān wàn.", "meaningVi": "Dân số của thành phố này vượt quá mười triệu."}],
    "hsk5_921": [{"chinese": "保护环境关系到人类的未来。", "pinyin": "Bǎohù huánjìng guānxi dào rénlèi de wèilái.", "meaningVi": "Bảo vệ môi trường liên quan đến tương lai của nhân loại."}],
    "hsk5_922": [{"chinese": "这个项目需要大量人力。", "pinyin": "Zhège xiàngmù xūyào dàliàng rénlì.", "meaningVi": "Dự án này cần một lượng lớn nhân lực."}],
    "hsk5_923": [{"chinese": "政府要为人民服务。", "pinyin": "Zhèngfǔ yào wèi rénmín fúwù.", "meaningVi": "Chính phủ phải phục vụ nhân dân."}],
    "hsk5_924": [{"chinese": "请问一美元能换多少人民币？", "pinyin": "Qǐngwèn yì měiyuán néng huàn duōshao rénmínbì?", "meaningVi": "Xin hỏi một đô la Mỹ có thể đổi được bao nhiêu nhân dân tệ?"}],
    "hsk5_925": [{"chinese": "广场上聚集了很多人群。", "pinyin": "Guǎngchǎng shàng jùjíle hěn duō rénqún.", "meaningVi": "Trên quảng trường tụ tập rất nhiều đám đông."}],
    "hsk5_926": [{"chinese": "水对人体非常重要。", "pinyin": "Shuǐ duì réntǐ fēicháng zhòngyào.", "meaningVi": "Nước vô cùng quan trọng đối với cơ thể con người."}],
    "hsk5_928": [{"chinese": "他忍住了没有哭出来。", "pinyin": "Tā rěnzhùle méiyǒu kū chūlai.", "meaningVi": "Anh ấy nhịn được không khóc ra."}],
    "hsk5_929": [{"chinese": "我几乎认不出他了。", "pinyin": "Wǒ jīhū rèn bu chū tā le.", "meaningVi": "Tôi gần như không nhận ra anh ấy nữa."}],
    "hsk5_930": [{"chinese": "墙上挂着一本日历。", "pinyin": "Qiáng shàng guàzhe yì běn rìlì.", "meaningVi": "Trên tường treo một quyển lịch."}],
    "hsk5_931": [{"chinese": "这家超市专卖日用品。", "pinyin": "Zhè jiā chāoshì zhuānmài rìyòngpǐn.", "meaningVi": "Siêu thị này chuyên bán đồ dùng hàng ngày."}],
    "hsk5_933": [{"chinese": "事情竟然如此发展。", "pinyin": "Shìqing jìngrán rúcǐ fāzhǎn.", "meaningVi": "Sự việc lại phát triển như thế này."}],
    "hsk5_934": [{"chinese": "你打算如何解决这个问题？", "pinyin": "Nǐ dǎsuàn rúhé jiějué zhège wèntí?", "meaningVi": "Bạn định giải quyết vấn đề này như thế nào?"}],
    "hsk5_935": [{"chinese": "如今生活水平提高了很多。", "pinyin": "Rújīn shēnghuó shuǐpíng tígāole hěn duō.", "meaningVi": "Ngày nay mức sống đã được nâng cao rất nhiều."}],
    "hsk5_936": [{"chinese": "他对我如同亲兄弟一样。", "pinyin": "Tā duì wǒ rútóng qīn xiōngdì yíyàng.", "meaningVi": "Anh ấy đối với tôi giống như anh em ruột vậy."}],
    "hsk5_937": [{"chinese": "具体安排如下。", "pinyin": "Jùtǐ ānpái rúxià.", "meaningVi": "Sắp xếp cụ thể như sau."}],
    "hsk5_940": [{"chinese": "他身体比较虚弱。", "pinyin": "Tā shēntǐ bǐjiào xūruò.", "meaningVi": "Cơ thể của anh ấy khá yếu."}],
    "hsk5_942": [{"chinese": "运动员们走进了赛场。", "pinyin": "Yùndòngyuánmen zǒujìnle sàichǎng.", "meaningVi": "Các vận động viên đã bước vào sân thi đấu."}],
    "hsk5_943": [{"chinese": "这幅画色彩鲜艳。", "pinyin": "Zhè fú huà sècǎi xiānyàn.", "meaningVi": "Bức tranh này màu sắc rực rỡ."}],
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
