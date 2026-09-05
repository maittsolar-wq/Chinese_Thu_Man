"""P5.10.3 (continued) -- Batch 026 (continues immediately after
examples_batch_025.json; entirely within HSK6, hsk6_0589-hsk6_0893).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Numeric-suffix homograph records (needs_review) ***
Five records in this batch carry the HSK6 numeric-suffix homograph
pattern (see batch 024's 乘2 and batch 025's 副2/该2 for the full
explanation): 局1/局2 (hsk6_0741/hsk6_0742) and 料1/料2
(hsk6_0850/hsk6_0851), plus 露1 (hsk6_0863). None of these literal
strings can appear in natural Chinese text, so all five are left with
an empty examples list and qaStatus "needs_review", per the
established rule. Production records untouched. Five further such
records remain later in HSK6 (升2, 所2, 则1, 支2) and will need
identical treatment when reached.

*** Continuing extremely dense homophone/polyphonic clusters ***
This batch substantially extends the pipeline's largest recurring
families, none flagged by the mechanical tier system (it compares the
`word` string, and every pair below is a different word):
  - jiā (1st tone): ten new members (夹/加倍/家常/家家户户/加剧/家居/
    家属/加以/家园/加重) added to the already-huge 加+X family
    (batch 011) and 家庭/家乡/家长/家具 (batch 011).
  - jiān (1st tone): eleven new members (尖/肩膀/监测/坚定/监督/坚固/
    坚决/艰难/艰辛/坚硬/兼职) added to the already-published 艰苦/
    坚强 (batch 023).
  - jiǎn (3rd tone): six new members (检测/简化/简介/减弱/减压/检验)
    added to the already-large 捡/剪/减/简 cluster (batch 023).
  - jiàn (4th tone): eight new members (剑/箭/鉴定/间隔/间接/健全/
    建筑物, plus 将军 same reading) added to the already-large 建/键/
    渐 cluster (batch 023).
  - jiāo (1st tone): seven new members (胶带/焦点/交际/焦虑/胶水/
    交谈/郊外) added to the already-published 浇/交换/交往 (batch
    023).
  - jiè (4th tone) and jiē (1st tone) clusters continuing from 接待/
    阶段/接近/接收 and 结构/结合/结论/节省 (batch 023): six and seven
    new members respectively (接连/结实/街头 vs 杰出/节能/结尾/截至/
    截止/节奏; 解/解答/解读/解放/解说 vs 借鉴/戒指/借助).
  - jìn (4th tone): seven new members (尽/进而/进度/进化/近来/近视/
    进展) added to the already-large 近代/进口/尽力/近年来/近期/近日/
    进一步 cluster (batch 023) -- 尽 here (jìn, "to exhaust/use up")
    kept distinct from the jǐn-reading 尽快/尽量 (batch 023).
  - jīng (1st tone): nine new members (精美/精确/惊人/经商/精通/精心/
    惊讶/精致/精准) added to the already-published 精力/惊喜/经营
    (batch 023).
  - jiù (4th tone): seven new members (就读/舅舅/救命/就算/救援/救灾/
    救助) added to the already-large 酒吧/久远/救/救护车/就业 cluster
    (batch 023).
  - jù (4th tone): six new members (剧本/聚集/俱乐部/剧烈, plus 决策
    same reading via 决) added to the already-large 据/距/具备/剧场/
    巨大/据说/具有 cluster (batch 023).
  - kāi (1st tone): five new members (开创/开关/开启/开设/开头) added
    to the already-large 开发/开幕/开水/开通/开业/开展 cluster (batch
    023).
  - kàn (4th tone): seven new members (看不起/看待/看得起/看好/看似/
    看中/看重) added to the already-published 看望/看作 (batch 023).
  - lǎo (3rd tone): three new members (老实/老鼠/老太太) added to the
    already-large 老百姓/老板/老公/姥姥/老婆/姥爷 cluster (batch 023).
  - lì (4th tone): ten new members (立/粒/立场/力度/历经/历年/例外/
    利息, plus 联合国 as a compound) added to the already-large
    立即/立刻/力量/利益/利用 cluster (batch 023).
  - liú (2nd tone): six new members (流程/流动/浏览器/流量/流入/流通)
    added to the already-large 流传/流感/浏览/流/留/留下/流利/流行
    cluster (batches 016/023).
  - lù (4th tone): six new members (路程/路况/路面/录像/录用/录制)
    added to the already-large 录/陆地/录取/路人/路线/陆续 cluster
    (batch 023).
  - Genuine same-pinyin-different-character pairs newly introduced:
    尖/监/坚/艰/兼 (jiān, five characters); 酱/降 (jiàng, distinct
    from the already-published 降 family); 局/菊 (jú); 井/警/景/颈
    (jǐng, four characters); 课/客/口/扣/酷 (kè/kǒu/kòu/kù, tone-
    distinguished cluster); 拦/栏/兰 (lán); 牢/劳 (láo); 会计's 会
    (kuài reading, distinct from the everyday huì reading used in
    汇报/绘画/会见/汇款/会见 elsewhere in this same batch); 空地/
    空闲 (kòng, distinct from the everyday kōng "air/empty" reading
    used in 空气/空间, batches 023/024).

Self-caught exact-duplicate revision made during drafting (before
this batch was finalized): 老鼠 (lǎoshǔ)'s first draft "猫抓到了一只
老鼠。" would have been an EXACT duplicate of 抓's own already-
published example (batch 022, hsk5_1554: "猫抓到了一只老鼠。") --
rewritten to "家里最近出现了老鼠。".

Fix applied after the first --dry-run/validator pass (caught by
validate_examples_batch_p103.py itself, not self-caught before
writing): hsk6_0861 (露, lòu, "to show/reveal/appear") had been
drafted with the WRONG character -- its first draft accidentally
reused hsk6_0862's own sentence ("这个系统存在安全漏洞。", which
targets 漏洞/漏 lòudòng/lòu, a different character sharing the same
pinyin+tone as 露). This produced both a target_word_present failure
(the literal character 露 never appeared) and an exact cross-record
duplicate. Rewritten to "他很久没有在公开场合露面了。" (using the
natural compound 露面 lòumiàn, "to show up/make an appearance",
matching hsk6_0861's meaningVi "xuất hiện, hiển thị"). Re-validated
clean: zero target_word_present failures, zero exact duplicates.

Near-template fixes (character-bigram Jaccard >= 0.55 against the
full pilot+002-025 corpus, caught by the independent script-level
check, not the validator): five flags, all fixed by diverging
sentence structure while preserving natural, correct usage:
  - 集团 vs hsk5_856's "这是一家大型企业。" (both used the "这是一家
    大型企业..." template) -> "这家跨国集团在多个国家设有分公司。"
  - 净 vs hsk4_059's "请把桌子擦干净。" (both used 擦(干)净 on 桌子)
    -> "他把碗里的饭吃净了。" (different verb+object, same resultative
    使用 of 净).
  - 啦 vs hsk3_330's "别生气了。" (my first draft literally reused
    that clause) -> "走啦，我们要迟到了。".
  - 俱乐部 vs hsk4_310's "他是这家健身房的会员。" (both used the
    "他是这家...的会员" template) -> "这家俱乐部每月组织一次聚会。".
  - 极为 vs hsk5_533's "这件事极其重要。" (near-synonym 极为/极其 in
    an otherwise identical clause) -> "这次谈判的结果极为关键。".

All re-verified against the full pilot+002-025 corpus with zero
remaining exact duplicates and zero near-template flags (see
validation report).

Usage:
    python generate_examples_batch_026.py --dry-run
    python generate_examples_batch_026.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 26
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_026.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# Records deliberately left with 0 examples (see module docstring):
# HSK6's numeric-suffix homograph pattern makes the literal target
# word unmatchable in natural Chinese text.
NEEDS_REVIEW_IDS = {"hsk6_0741", "hsk6_0742", "hsk6_0850", "hsk6_0851", "hsk6_0863"}

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk6_0589": [{"chinese": "请把工作进度向领导汇报。", "pinyin": "Qǐng bǎ gōngzuò jìndù xiàng lǐngdǎo huìbào.", "meaningVi": "Xin báo cáo tiến độ công việc cho lãnh đạo."}],
    "hsk6_0590": [{"chinese": "她喜欢绘画。", "pinyin": "Tā xǐhuan huìhuà.", "meaningVi": "Cô ấy thích vẽ tranh."}],
    "hsk6_0591": [{"chinese": "两国领导人举行了会见。", "pinyin": "Liǎng guó lǐngdǎorén jǔxíngle huìjiàn.", "meaningVi": "Lãnh đạo hai nước đã tiến hành cuộc gặp gỡ."}],
    "hsk6_0592": [{"chinese": "请通过银行汇款。", "pinyin": "Qǐng tōngguò yínháng huìkuǎn.", "meaningVi": "Xin chuyển tiền qua ngân hàng."}],
    "hsk6_0593": [{"chinese": "婚姻需要双方共同经营。", "pinyin": "Hūnyīn xūyào shuāngfāng gòngtóng jīngyíng.", "meaningVi": "Hôn nhân cần cả hai bên cùng nhau vun đắp."}],
    "hsk6_0594": [{"chinese": "别把两种液体混在一起。", "pinyin": "Bié bǎ liǎng zhǒng yètǐ hùn zài yìqǐ.", "meaningVi": "Đừng trộn hai loại chất lỏng vào với nhau."}],
    "hsk6_0595": [{"chinese": "请把面粉和水混合均匀。", "pinyin": "Qǐng bǎ miànfěn hé shuǐ hùnhé jūnyún.", "meaningVi": "Xin trộn đều bột mì với nước."}],
    "hsk6_0596": [{"chinese": "现场秩序一片混乱。", "pinyin": "Xiànchǎng zhìxù yí piàn hùnluàn.", "meaningVi": "Trật tự tại hiện trường vô cùng hỗn loạn."}],
    "hsk6_0597": [{"chinese": "这个城市充满活力。", "pinyin": "Zhège chéngshì chōngmǎn huólì.", "meaningVi": "Thành phố này tràn đầy sức sống."}],
    "hsk6_0598": [{"chinese": "她在班里表现得很活跃。", "pinyin": "Tā zài bān lǐ biǎoxiàn de hěn huóyuè.", "meaningVi": "Cô ấy thể hiện rất năng động trong lớp."}],
    "hsk6_0599": [{"chinese": "请用火柴点燃蜡烛。", "pinyin": "Qǐng yòng huǒchái diǎnrán làzhú.", "meaningVi": "Xin dùng diêm để thắp nến."}],
    "hsk6_0600": [{"chinese": "这场火灾造成了巨大损失。", "pinyin": "Zhè chǎng huǒzāi zàochéngle jùdà sǔnshī.", "meaningVi": "Vụ hỏa hoạn này đã gây ra thiệt hại to lớn."}],
    "hsk6_0601": [{"chinese": "人民币是中国的法定货币。", "pinyin": "Rénmínbì shì Zhōngguó de fǎdìng huòbì.", "meaningVi": "Nhân dân tệ là đồng tiền pháp định của Trung Quốc."}],
    "hsk6_0602": [{"chinese": "一辆货车停在路边。", "pinyin": "Yí liàng huòchē tíng zài lùbiān.", "meaningVi": "Một chiếc xe tải đỗ bên đường."}],
    "hsk6_0603": [{"chinese": "他们最终击败了对手。", "pinyin": "Tāmen zhōngyú jībàile duìshǒu.", "meaningVi": "Cuối cùng họ đã đánh bại đối thủ."}],
    "hsk6_0604": [{"chinese": "这里是一个训练基地。", "pinyin": "Zhèlǐ shì yí gè xùnliàn jīdì.", "meaningVi": "Đây là một căn cứ huấn luyện."}],
    "hsk6_0605": [{"chinese": "请为机动车让路。", "pinyin": "Qǐng wèi jīdòngchē rànglù.", "meaningVi": "Xin nhường đường cho xe cơ giới."}],
    "hsk6_0606": [{"chinese": "战争年代很多人忍受饥饿。", "pinyin": "Zhànzhēng niándài hěn duō rén rěnshòu jī'è.", "meaningVi": "Trong thời chiến tranh nhiều người phải chịu đói."}],
    "hsk6_0607": [{"chinese": "老师善于激发学生的兴趣。", "pinyin": "Lǎoshī shànyú jīfā xuésheng de xìngqù.", "meaningVi": "Giáo viên giỏi khơi dậy hứng thú của học sinh."}],
    "hsk6_0608": [{"chinese": "他投资了一支基金。", "pinyin": "Tā tóuzīle yì zhī jījīn.", "meaningVi": "Anh ấy đã đầu tư vào một quỹ."}],
    "hsk6_0609": [{"chinese": "老师的话激励了他。", "pinyin": "Lǎoshī de huà jīlìle tā.", "meaningVi": "Lời của giáo viên đã khích lệ anh ấy."}],
    "hsk6_0610": [{"chinese": "他工作充满激情。", "pinyin": "Tā gōngzuò chōngmǎn jīqíng.", "meaningVi": "Anh ấy làm việc tràn đầy nhiệt huyết."}],
    "hsk6_0611": [{"chinese": "他学的是机械专业。", "pinyin": "Tā xué de shì jīxiè zhuānyè.", "meaningVi": "Anh ấy học chuyên ngành cơ khí."}],
    "hsk6_0612": [{"chinese": "这种性状是基因决定的。", "pinyin": "Zhè zhǒng xìngzhuàng shì jīyīn juédìng de.", "meaningVi": "Đặc tính này được quyết định bởi gen."}],
    "hsk6_0613": [{"chinese": "这是一个难得的机遇。", "pinyin": "Zhè shì yí gè nándé de jīyù.", "meaningVi": "Đây là một cơ hội hiếm có."}],
    "hsk6_0614": [{"chinese": "我们需要建立一个有效的机制。", "pinyin": "Wǒmen xūyào jiànlì yí gè yǒuxiào de jīzhì.", "meaningVi": "Chúng ta cần xây dựng một cơ chế hiệu quả."}],
    "hsk6_0615": [{"chinese": "即便下雨，我们也要去。", "pinyin": "Jíbiàn xiàyǔ, wǒmen yě yào qù.", "meaningVi": "Ngay cả khi trời mưa, chúng tôi cũng phải đi."}],
    "hsk6_0616": [{"chinese": "请不要采取极端的做法。", "pinyin": "Qǐng búyào cǎiqǔ jíduān de zuòfǎ.", "meaningVi": "Xin đừng áp dụng cách làm cực đoan."}],
    "hsk6_0617": [{"chinese": "医生对伤员进行了急救。", "pinyin": "Yīshēng duì shāngyuán jìnxíngle jíjiù.", "meaningVi": "Bác sĩ đã cấp cứu cho người bị thương."}],
    "hsk6_0618": [{"chinese": "他急切地想知道结果。", "pinyin": "Tā jíqiè de xiǎng zhīdào jiéguǒ.", "meaningVi": "Anh ấy nôn nóng muốn biết kết quả."}],
    "hsk6_0619": [{"chinese": "这家跨国集团在多个国家设有分公司。", "pinyin": "Zhè jiā kuàguó jítuán zài duō gè guójiā shèyǒu fēngōngsī.", "meaningVi": "Tập đoàn đa quốc gia này có chi nhánh tại nhiều quốc gia."}],
    "hsk6_0620": [{"chinese": "这次谈判的结果极为关键。", "pinyin": "Zhè cì tánpàn de jiéguǒ jíwéi guānjiàn.", "meaningVi": "Kết quả của cuộc đàm phán lần này cực kỳ quan trọng."}],
    "hsk6_0621": [{"chinese": "红色在中国代表吉祥。", "pinyin": "Hóngsè zài Zhōngguó dàibiǎo jíxiáng.", "meaningVi": "Màu đỏ ở Trung Quốc tượng trưng cho sự may mắn."}],
    "hsk6_0622": [{"chinese": "他继承了父亲的事业。", "pinyin": "Tā jìchéngle fùqīn de shìyè.", "meaningVi": "Anh ấy đã kế thừa sự nghiệp của cha."}],
    "hsk6_0623": [{"chinese": "他获得了这次比赛的季军。", "pinyin": "Tā huòdéle zhè cì bǐsài de jìjūn.", "meaningVi": "Anh ấy đã giành được hạng ba trong cuộc thi lần này."}],
    "hsk6_0624": [{"chinese": "部队的纪律非常严格。", "pinyin": "Bùduì de jìlǜ fēicháng yángé.", "meaningVi": "Kỷ luật của bộ đội vô cùng nghiêm khắc."}],
    "hsk6_0625": [{"chinese": "一个人在外地生活很寂寞。", "pinyin": "Yí gè rén zài wàidì shēnghuó hěn jìmò.", "meaningVi": "Sống một mình ở nơi xa lạ rất cô đơn."}],
    "hsk6_0626": [{"chinese": "这需要一定的技巧。", "pinyin": "Zhè xūyào yídìng de jìqiǎo.", "meaningVi": "Việc này cần có kỹ xảo nhất định."}],
    "hsk6_0627": [{"chinese": "他的技艺十分精湛。", "pinyin": "Tā de jìyì shífēn jīngzhàn.", "meaningVi": "Tay nghề của anh ấy vô cùng tinh xảo."}],
    "hsk6_0628": [{"chinese": "请把文件夹好。", "pinyin": "Qǐng bǎ wénjiàn jiā hǎo.", "meaningVi": "Xin kẹp tài liệu lại cho gọn."}],
    "hsk6_0629": [{"chinese": "他加倍努力工作。", "pinyin": "Tā jiābèi nǔlì gōngzuò.", "meaningVi": "Anh ấy làm việc nỗ lực gấp đôi."}],
    "hsk6_0630": [{"chinese": "我们聊了聊家常。", "pinyin": "Wǒmen liáole liáo jiācháng.", "meaningVi": "Chúng tôi đã nói chuyện phiếm về đời thường."}],
    "hsk6_0631": [{"chinese": "春节期间，家家户户都很热闹。", "pinyin": "Chūnjié qījiān, jiājiāhùhù dōu hěn rènao.", "meaningVi": "Trong dịp Tết, nhà nhà đều nhộn nhịp."}],
    "hsk6_0632": [{"chinese": "争吵使矛盾进一步加剧。", "pinyin": "Zhēngchǎo shǐ máodùn jìnyíbù jiājù.", "meaningVi": "Cãi vã khiến mâu thuẫn thêm trầm trọng."}],
    "hsk6_0633": [{"chinese": "这是一家家居用品店。", "pinyin": "Zhè shì yì jiā jiājū yòngpǐn diàn.", "meaningVi": "Đây là một cửa hàng đồ dùng gia đình."}],
    "hsk6_0634": [{"chinese": "医院通知了病人的家属。", "pinyin": "Yīyuàn tōngzhīle bìngrén de jiāshǔ.", "meaningVi": "Bệnh viện đã thông báo cho gia đình bệnh nhân."}],
    "hsk6_0635": [{"chinese": "这个问题需要加以重视。", "pinyin": "Zhège wèntí xūyào jiāyǐ zhòngshì.", "meaningVi": "Vấn đề này cần được coi trọng."}],
    "hsk6_0636": [{"chinese": "他们重建了自己的家园。", "pinyin": "Tāmen chóngjiànle zìjǐ de jiāyuán.", "meaningVi": "Họ đã xây dựng lại quê hương của mình."}],
    "hsk6_0637": [{"chinese": "他的病情有所加重。", "pinyin": "Tā de bìngqíng yǒusuǒ jiāzhòng.", "meaningVi": "Bệnh tình của anh ấy có phần trở nặng."}],
    "hsk6_0638": [{"chinese": "让我们假设一种情况。", "pinyin": "Ràng wǒmen jiǎshè yì zhǒng qíngkuàng.", "meaningVi": "Hãy để chúng ta giả định một tình huống."}],
    "hsk6_0639": [{"chinese": "她嫁给了一位医生。", "pinyin": "Tā jià gěile yí wèi yīshēng.", "meaningVi": "Cô ấy đã lấy chồng là một bác sĩ."}],
    "hsk6_0640": [{"chinese": "这支铅笔很尖。", "pinyin": "Zhè zhī qiānbǐ hěn jiān.", "meaningVi": "Cây bút chì này rất nhọn."}],
    "hsk6_0641": [{"chinese": "他拍了拍我的肩膀。", "pinyin": "Tā pāile pāi wǒ de jiānbǎng.", "meaningVi": "Anh ấy vỗ vỗ vai tôi."}],
    "hsk6_0642": [{"chinese": "这里对空气质量进行实时监测。", "pinyin": "Zhèlǐ duì kōngqì zhìliàng jìnxíng shíshí jiāncè.", "meaningVi": "Nơi đây giám sát chất lượng không khí theo thời gian thực."}],
    "hsk6_0643": [{"chinese": "他态度十分坚定。", "pinyin": "Tā tàidù shífēn jiāndìng.", "meaningVi": "Thái độ của anh ấy vô cùng kiên định."}],
    "hsk6_0644": [{"chinese": "我们需要相互监督。", "pinyin": "Wǒmen xūyào xiānghù jiāndū.", "meaningVi": "Chúng ta cần giám sát lẫn nhau."}],
    "hsk6_0645": [{"chinese": "这座桥梁十分坚固。", "pinyin": "Zhè zuò qiáoliáng shífēn jiāngù.", "meaningVi": "Cây cầu này vô cùng kiên cố."}],
    "hsk6_0646": [{"chinese": "他坚决反对这个方案。", "pinyin": "Tā jiānjué fǎnduì zhège fāng'àn.", "meaningVi": "Anh ấy kiên quyết phản đối phương án này."}],
    "hsk6_0647": [{"chinese": "他度过了一段艰难的时期。", "pinyin": "Tā dùguòle yí duàn jiānnán de shíqī.", "meaningVi": "Anh ấy đã trải qua một giai đoạn khó khăn."}],
    "hsk6_0648": [{"chinese": "创业的过程充满艰辛。", "pinyin": "Chuàngyè de guòchéng chōngmǎn jiānxīn.", "meaningVi": "Quá trình khởi nghiệp tràn đầy gian khổ."}],
    "hsk6_0649": [{"chinese": "这块石头非常坚硬。", "pinyin": "Zhè kuài shítou fēicháng jiānyìng.", "meaningVi": "Tảng đá này vô cùng cứng rắn."}],
    "hsk6_0650": [{"chinese": "他一边上学一边兼职工作。", "pinyin": "Tā yìbiān shàngxué yìbiān jiānzhí gōngzuò.", "meaningVi": "Anh ấy vừa đi học vừa làm thêm."}],
    "hsk6_0651": [{"chinese": "请检测一下产品质量。", "pinyin": "Qǐng jiǎncè yíxià chǎnpǐn zhìliàng.", "meaningVi": "Xin kiểm tra chất lượng sản phẩm."}],
    "hsk6_0652": [{"chinese": "这个流程可以简化。", "pinyin": "Zhège liúchéng kěyǐ jiǎnhuà.", "meaningVi": "Quy trình này có thể được đơn giản hóa."}],
    "hsk6_0653": [{"chinese": "请写一份个人简介。", "pinyin": "Qǐng xiě yí fèn gèrén jiǎnjiè.", "meaningVi": "Xin viết một bản giới thiệu bản thân."}],
    "hsk6_0654": [{"chinese": "台风的威力正在减弱。", "pinyin": "Táifēng de wēilì zhèngzài jiǎnruò.", "meaningVi": "Sức mạnh của cơn bão đang suy yếu."}],
    "hsk6_0655": [{"chinese": "运动是一种有效的减压方式。", "pinyin": "Yùndòng shì yì zhǒng yǒuxiào de jiǎnyā fāngshì.", "meaningVi": "Vận động là một cách giảm áp lực hiệu quả."}],
    "hsk6_0656": [{"chinese": "实践是检验真理的唯一标准。", "pinyin": "Shíjiàn shì jiǎnyàn zhēnlǐ de wéiyī biāozhǔn.", "meaningVi": "Thực tiễn là tiêu chuẩn duy nhất để kiểm nghiệm chân lý."}],
    "hsk6_0657": [{"chinese": "古代武士随身佩剑。", "pinyin": "Gǔdài wǔshì suíshēn pèi jiàn.", "meaningVi": "Võ sĩ thời cổ đại luôn đeo kiếm bên mình."}],
    "hsk6_0658": [{"chinese": "他一箭射中了靶心。", "pinyin": "Tā yí jiàn shèzhòngle bǎxīn.", "meaningVi": "Anh ấy bắn một mũi tên trúng hồng tâm."}],
    "hsk6_0659": [{"chinese": "专家对这幅画进行了鉴定。", "pinyin": "Zhuānjiā duì zhè fú huà jìnxíngle jiàndìng.", "meaningVi": "Chuyên gia đã tiến hành giám định bức tranh này."}],
    "hsk6_0660": [{"chinese": "两次演出间隔一个小时。", "pinyin": "Liǎng cì yǎnchū jiàngé yí gè xiǎoshí.", "meaningVi": "Hai buổi biểu diễn cách nhau một tiếng đồng hồ."}],
    "hsk6_0661": [{"chinese": "这是一种间接的方式。", "pinyin": "Zhè shì yì zhǒng jiànjiē de fāngshì.", "meaningVi": "Đây là một cách thức gián tiếp."}],
    "hsk6_0662": [{"chinese": "我们要建立健全的制度。", "pinyin": "Wǒmen yào jiànlì jiànquán de zhìdù.", "meaningVi": "Chúng ta phải xây dựng chế độ hoàn thiện."}],
    "hsk6_0663": [{"chinese": "这座建筑物有一百年历史了。", "pinyin": "Zhè zuò jiànzhùwù yǒu yìbǎi nián lìshǐ le.", "meaningVi": "Công trình kiến trúc này đã có lịch sử một trăm năm."}],
    "hsk6_0664": [{"chinese": "这位将军带兵打了很多胜仗。", "pinyin": "Zhè wèi jiāngjūn dài bīng dǎle hěn duō shèngzhàng.", "meaningVi": "Vị tướng quân này đã dẫn quân đánh thắng rất nhiều trận."}],
    "hsk6_0665": [{"chinese": "导游详细讲解了这段历史。", "pinyin": "Dǎoyóu xiángxì jiǎngjiěle zhè duàn lìshǐ.", "meaningVi": "Hướng dẫn viên đã giảng giải chi tiết về giai đoạn lịch sử này."}],
    "hsk6_0666": [{"chinese": "他获得了一枚奖牌。", "pinyin": "Tā huòdéle yì méi jiǎngpái.", "meaningVi": "Anh ấy đã giành được một tấm huy chương."}],
    "hsk6_0667": [{"chinese": "获胜者可以领取奖品。", "pinyin": "Huòshèngzhě kěyǐ lǐngqǔ jiǎngpǐn.", "meaningVi": "Người chiến thắng có thể nhận giải thưởng."}],
    "hsk6_0668": [{"chinese": "这盘菜配的酱很好吃。", "pinyin": "Zhè pán cài pèi de jiàng hěn hǎochī.", "meaningVi": "Nước xốt kèm theo món ăn này rất ngon."}],
    "hsk6_0669": [{"chinese": "请加一点酱油。", "pinyin": "Qǐng jiā yìdiǎn jiàngyóu.", "meaningVi": "Xin cho thêm một chút xì dầu."}],
    "hsk6_0670": [{"chinese": "请用胶带把箱子封好。", "pinyin": "Qǐng yòng jiāodài bǎ xiāngzi fēng hǎo.", "meaningVi": "Xin dùng băng dính dán kín thùng lại."}],
    "hsk6_0671": [{"chinese": "这个话题成了大家关注的焦点。", "pinyin": "Zhège huàtí chéngle dàjiā guānzhù de jiāodiǎn.", "meaningVi": "Chủ đề này đã trở thành tiêu điểm được mọi người quan tâm."}],
    "hsk6_0672": [{"chinese": "他不太擅长交际。", "pinyin": "Tā bú tài shàncháng jiāojì.", "meaningVi": "Anh ấy không giỏi giao tiếp xã hội lắm."}],
    "hsk6_0673": [{"chinese": "考试前他感到很焦虑。", "pinyin": "Kǎoshì qián tā gǎndào hěn jiāolǜ.", "meaningVi": "Trước kỳ thi anh ấy cảm thấy rất lo âu."}],
    "hsk6_0674": [{"chinese": "请用胶水把纸粘好。", "pinyin": "Qǐng yòng jiāoshuǐ bǎ zhǐ zhān hǎo.", "meaningVi": "Xin dùng keo dán tờ giấy lại."}],
    "hsk6_0675": [{"chinese": "他们愉快地交谈起来。", "pinyin": "Tāmen yúkuài de jiāotán qǐlai.", "meaningVi": "Họ vui vẻ trò chuyện với nhau."}],
    "hsk6_0676": [{"chinese": "周末我们去郊外野餐吧。", "pinyin": "Zhōumò wǒmen qù jiāowài yěcān ba.", "meaningVi": "Cuối tuần chúng ta đi ngoại ô picnic đi."}],
    "hsk6_0677": [{"chinese": "猫躲在房间的角落里。", "pinyin": "Māo duǒ zài fángjiān de jiǎoluò lǐ.", "meaningVi": "Con mèo trốn trong góc phòng."}],
    "hsk6_0678": [{"chinese": "雪地上留下了一串脚印。", "pinyin": "Xuědì shàng liúxiàle yí chuàn jiǎoyìn.", "meaningVi": "Trên nền tuyết để lại một chuỗi dấu chân."}],
    "hsk6_0679": [{"chinese": "这个方案较为合理。", "pinyin": "Zhège fāng'àn jiàowéi hélǐ.", "meaningVi": "Phương án này tương đối hợp lý."}],
    "hsk6_0680": [{"chinese": "这次失败给了他一个深刻的教训。", "pinyin": "Zhè cì shībài gěile tā yí gè shēnkè de jiàoxùn.", "meaningVi": "Thất bại lần này đã cho anh ấy một bài học sâu sắc."}],
    "hsk6_0683": [{"chinese": "他接连获得了几个奖项。", "pinyin": "Tā jiēlián huòdéle jǐ gè jiǎngxiàng.", "meaningVi": "Anh ấy liên tiếp giành được vài giải thưởng."}],
    "hsk6_0684": [{"chinese": "这个箱子做得很结实。", "pinyin": "Zhège xiāngzi zuò de hěn jiēshi.", "meaningVi": "Cái hộp này làm rất chắc chắn."}],
    "hsk6_0685": [{"chinese": "街头艺人在表演。", "pinyin": "Jiētóu yìrén zài biǎoyǎn.", "meaningVi": "Nghệ nhân đường phố đang biểu diễn."}],
    "hsk6_0686": [{"chinese": "他是一位杰出的科学家。", "pinyin": "Tā shì yí wèi jiéchū de kēxuéjiā.", "meaningVi": "Anh ấy là một nhà khoa học kiệt xuất."}],
    "hsk6_0687": [{"chinese": "这款空调节能又环保。", "pinyin": "Zhè kuǎn kōngtiáo jiénéng yòu huánbǎo.", "meaningVi": "Chiếc điều hòa này tiết kiệm năng lượng lại thân thiện với môi trường."}],
    "hsk6_0688": [{"chinese": "这部小说的结尾出人意料。", "pinyin": "Zhè bù xiǎoshuō de jiéwěi chūrén-yìliào.", "meaningVi": "Đoạn kết của cuốn tiểu thuyết này nằm ngoài dự đoán."}],
    "hsk6_0689": [{"chinese": "截至目前，报名人数已超过一千。", "pinyin": "Jiézhì mùqián, bàomíng rénshù yǐ chāoguò yìqiān.", "meaningVi": "Tính đến hiện tại, số người đăng ký đã vượt quá một nghìn."}],
    "hsk6_0690": [{"chinese": "报名将于本周五截止。", "pinyin": "Bàomíng jiāng yú běn zhōu wǔ jiézhǐ.", "meaningVi": "Việc đăng ký sẽ kết thúc vào thứ sáu tuần này."}],
    "hsk6_0691": [{"chinese": "这首歌的节奏很欢快。", "pinyin": "Zhè shǒu gē de jiézòu hěn huānkuài.", "meaningVi": "Nhịp điệu của bài hát này rất vui tươi."}],
    "hsk6_0692": [{"chinese": "请解开这个绳结。", "pinyin": "Qǐng jiěkāi zhège shéngjié.", "meaningVi": "Xin cởi nút thắt của sợi dây này."}],
    "hsk6_0693": [{"chinese": "老师帮我解答了这道题。", "pinyin": "Lǎoshī bāng wǒ jiědále zhè dào tí.", "meaningVi": "Giáo viên đã giúp tôi giải đáp bài toán này."}],
    "hsk6_0694": [{"chinese": "专家对这项政策进行了解读。", "pinyin": "Zhuānjiā duì zhè xiàng zhèngcè jìnxíngle jiědú.", "meaningVi": "Chuyên gia đã giải thích chính sách này."}],
    "hsk6_0695": [{"chinese": "科技解放了人类的双手。", "pinyin": "Kējì jiěfàngle rénlèi de shuāngshǒu.", "meaningVi": "Khoa học công nghệ đã giải phóng đôi tay con người."}],
    "hsk6_0696": [{"chinese": "他为大家解说了比赛规则。", "pinyin": "Tā wèi dàjiā jiěshuōle bǐsài guīzé.", "meaningVi": "Anh ấy đã giải thích luật thi đấu cho mọi người."}],
    "hsk6_0697": [{"chinese": "我们可以借鉴他国的经验。", "pinyin": "Wǒmen kěyǐ jièjiàn tāguó de jīngyàn.", "meaningVi": "Chúng ta có thể học hỏi kinh nghiệm của nước khác."}],
    "hsk6_0698": [{"chinese": "他送给她一枚戒指。", "pinyin": "Tā sòng gěi tā yì méi jièzhi.", "meaningVi": "Anh ấy đã tặng cô ấy một chiếc nhẫn."}],
    "hsk6_0699": [{"chinese": "他借助工具完成了任务。", "pinyin": "Tā jièzhù gōngjù wánchéngle rènwu.", "meaningVi": "Anh ấy đã hoàn thành nhiệm vụ nhờ vào công cụ."}],
    "hsk6_0700": [{"chinese": "请核对一下转账金额。", "pinyin": "Qǐng héduì yíxià zhuǎnzhàng jīn'é.", "meaningVi": "Xin kiểm tra lại số tiền chuyển khoản."}],
    "hsk6_0701": [{"chinese": "他获得了本次比赛的金牌。", "pinyin": "Tā huòdéle běn cì bǐsài de jīnpái.", "meaningVi": "Anh ấy đã giành được huy chương vàng của cuộc thi lần này."}],
    "hsk6_0702": [{"chinese": "健康比金钱更重要。", "pinyin": "Jiànkāng bǐ jīnqián gèng zhòngyào.", "meaningVi": "Sức khỏe quan trọng hơn tiền bạc."}],
    "hsk6_0703": [{"chinese": "他在金融行业工作。", "pinyin": "Tā zài jīnróng hángyè gōngzuò.", "meaningVi": "Anh ấy làm việc trong ngành tài chính."}],
    "hsk6_0704": [{"chinese": "这个零件是用金属做的。", "pinyin": "Zhège língjiàn shì yòng jīnshǔ zuò de.", "meaningVi": "Linh kiện này được làm bằng kim loại."}],
    "hsk6_0705": [{"chinese": "这枚戒指是纯金子做的。", "pinyin": "Zhè méi jièzhi shì chún jīnzi zuò de.", "meaningVi": "Chiếc nhẫn này được làm bằng vàng nguyên chất."}],
    "hsk6_0706": [{"chinese": "他把杯里的水喝尽了。", "pinyin": "Tā bǎ bēi lǐ de shuǐ hējìn le.", "meaningVi": "Anh ấy đã uống cạn nước trong cốc."}],
    "hsk6_0707": [{"chinese": "他先分析问题，进而提出解决方案。", "pinyin": "Tā xiān fēnxī wèntí, jìn'ér tíchū jiějué fāng'àn.", "meaningVi": "Anh ấy phân tích vấn đề trước, sau đó đưa ra phương án giải quyết."}],
    "hsk6_0708": [{"chinese": "请汇报一下工程进度。", "pinyin": "Qǐng huìbào yíxià gōngchéng jìndù.", "meaningVi": "Xin báo cáo tiến độ công trình."}],
    "hsk6_0709": [{"chinese": "人类是从猿类进化而来的。", "pinyin": "Rénlèi shì cóng yuánlèi jìnhuà ér lái de.", "meaningVi": "Loài người tiến hóa từ loài vượn."}],
    "hsk6_0710": [{"chinese": "近来他工作很忙。", "pinyin": "Jìnlái tā gōngzuò hěn máng.", "meaningVi": "Gần đây anh ấy làm việc rất bận."}],
    "hsk6_0711": [{"chinese": "他有点近视，需要戴眼镜。", "pinyin": "Tā yǒudiǎn jìnshì, xūyào dài yǎnjìng.", "meaningVi": "Anh ấy hơi cận thị, cần đeo kính."}],
    "hsk6_0712": [{"chinese": "项目进展顺利。", "pinyin": "Xiàngmù jìnzhǎn shùnlì.", "meaningVi": "Dự án tiến triển thuận lợi."}],
    "hsk6_0713": [{"chinese": "这份礼物包装得非常精美。", "pinyin": "Zhè fèn lǐwù bāozhuāng de fēicháng jīngměi.", "meaningVi": "Món quà này được đóng gói vô cùng tinh tế."}],
    "hsk6_0714": [{"chinese": "请给出精确的数字。", "pinyin": "Qǐng gěichū jīngquè de shùzì.", "meaningVi": "Xin đưa ra con số chính xác."}],
    "hsk6_0715": [{"chinese": "他的进步速度惊人。", "pinyin": "Tā de jìnbù sùdù jīngrén.", "meaningVi": "Tốc độ tiến bộ của anh ấy đáng kinh ngạc."}],
    "hsk6_0716": [{"chinese": "他辞职去经商了。", "pinyin": "Tā cízhí qù jīngshāng le.", "meaningVi": "Anh ấy đã nghỉ việc đi kinh doanh."}],
    "hsk6_0717": [{"chinese": "他精通好几门外语。", "pinyin": "Tā jīngtōng hǎo jǐ mén wàiyǔ.", "meaningVi": "Anh ấy thông thạo mấy ngoại ngữ."}],
    "hsk6_0718": [{"chinese": "这道菜是她精心准备的。", "pinyin": "Zhè dào cài shì tā jīngxīn zhǔnbèi de.", "meaningVi": "Món ăn này là cô ấy chuẩn bị tỉ mỉ."}],
    "hsk6_0719": [{"chinese": "大家都对这个结果感到惊讶。", "pinyin": "Dàjiā dōu duì zhège jiéguǒ gǎndào jīngyà.", "meaningVi": "Mọi người đều cảm thấy ngạc nhiên trước kết quả này."}],
    "hsk6_0720": [{"chinese": "这件工艺品十分精致。", "pinyin": "Zhè jiàn gōngyìpǐn shífēn jīngzhì.", "meaningVi": "Sản phẩm thủ công này vô cùng tinh xảo."}],
    "hsk6_0721": [{"chinese": "这台仪器测量非常精准。", "pinyin": "Zhè tái yíqì cèliáng fēicháng jīngzhǔn.", "meaningVi": "Thiết bị này đo lường rất chính xác."}],
    "hsk6_0722": [{"chinese": "村子里有一口老井。", "pinyin": "Cūnzi lǐ yǒu yì kǒu lǎo jǐng.", "meaningVi": "Trong làng có một cái giếng cũ."}],
    "hsk6_0723": [{"chinese": "老师警告他不要迟到。", "pinyin": "Lǎoshī jǐnggào tā búyào chídào.", "meaningVi": "Giáo viên cảnh cáo anh ấy đừng đến muộn."}],
    "hsk6_0724": [{"chinese": "这里的自然景观十分独特。", "pinyin": "Zhèlǐ de zìrán jǐngguān shífēn dútè.", "meaningVi": "Cảnh quan thiên nhiên nơi đây vô cùng độc đáo."}],
    "hsk6_0725": [{"chinese": "眼前是一片繁荣的景象。", "pinyin": "Yǎnqián shì yí piàn fánróng de jǐngxiàng.", "meaningVi": "Trước mắt là một cảnh tượng phồn vinh."}],
    "hsk6_0726": [{"chinese": "长期低头会伤害颈椎。", "pinyin": "Chángqī dītóu huì shānghài jǐngzhuī.", "meaningVi": "Cúi đầu lâu dài sẽ gây hại cho đốt sống cổ."}],
    "hsk6_0727": [{"chinese": "他把碗里的饭吃净了。", "pinyin": "Tā bǎ wǎn lǐ de fàn chī jìng le.", "meaningVi": "Anh ấy đã ăn hết sạch cơm trong bát."}],
    "hsk6_0728": [{"chinese": "他参加了数学竞赛。", "pinyin": "Tā cānjiāle shùxué jìngsài.", "meaningVi": "Anh ấy đã tham gia cuộc thi toán học."}],
    "hsk6_0729": [{"chinese": "请对准镜头微笑。", "pinyin": "Qǐng duìzhǔn jìngtóu wēixiào.", "meaningVi": "Xin nhìn vào ống kính và mỉm cười."}],
    "hsk6_0730": [{"chinese": "双方因土地问题发生了纠纷。", "pinyin": "Shuāngfāng yīn tǔdì wèntí fāshēngle jiūfēn.", "meaningVi": "Hai bên đã xảy ra tranh chấp vì vấn đề đất đai."}],
    "hsk6_0731": [{"chinese": "老师及时纠正了他的发音。", "pinyin": "Lǎoshī jíshí jiūzhèngle tā de fāyīn.", "meaningVi": "Giáo viên đã kịp thời sửa chữa cách phát âm của anh ấy."}],
    "hsk6_0732": [{"chinese": "请用酒精消毒。", "pinyin": "Qǐng yòng jiǔjīng xiāodú.", "meaningVi": "Xin dùng cồn để khử trùng."}],
    "hsk6_0733": [{"chinese": "婚礼上准备了各种酒水。", "pinyin": "Hūnlǐ shàng zhǔnbèile gèzhǒng jiǔshuǐ.", "meaningVi": "Trong đám cưới đã chuẩn bị đủ các loại đồ uống."}],
    "hsk6_0734": [{"chinese": "他在这所大学就读。", "pinyin": "Tā zài zhè suǒ dàxué jiùdú.", "meaningVi": "Anh ấy theo học tại trường đại học này."}],
    "hsk6_0735": [{"chinese": "我舅舅是一名医生。", "pinyin": "Wǒ jiùjiu shì yì míng yīshēng.", "meaningVi": "Cậu tôi là một bác sĩ."}],
    "hsk6_0736": [{"chinese": "救命啊！有人落水了！", "pinyin": "Jiùmìng a! Yǒu rén luòshuǐ le!", "meaningVi": "Cứu với! Có người rơi xuống nước rồi!"}],
    "hsk6_0737": [{"chinese": "就算失败了，我也不后悔。", "pinyin": "Jiùsuàn shībài le, wǒ yě bú hòuhuǐ.", "meaningVi": "Cho dù có thất bại, tôi cũng không hối hận."}],
    "hsk6_0738": [{"chinese": "救援队正在赶往现场。", "pinyin": "Jiùyuánduì zhèngzài gǎnwǎng xiànchǎng.", "meaningVi": "Đội cứu hộ đang trên đường đến hiện trường."}],
    "hsk6_0739": [{"chinese": "政府派出军队救灾。", "pinyin": "Zhèngfǔ pàichū jūnduì jiùzāi.", "meaningVi": "Chính phủ đã cử quân đội đi cứu trợ thiên tai."}],
    "hsk6_0740": [{"chinese": "他们向受困人员提供救助。", "pinyin": "Tāmen xiàng shòukùn rényuán tígōng jiùzhù.", "meaningVi": "Họ đã cung cấp sự cứu trợ cho những người bị mắc kẹt."}],
    "hsk6_0741": [],
    "hsk6_0742": [],
    "hsk6_0743": [{"chinese": "秋天菊花盛开。", "pinyin": "Qiūtiān júhuā shèngkāi.", "meaningVi": "Mùa thu hoa cúc nở rộ."}],
    "hsk6_0744": [{"chinese": "目前的局面比较复杂。", "pinyin": "Mùqián de júmiàn bǐjiào fùzá.", "meaningVi": "Cục diện hiện tại khá phức tạp."}],
    "hsk6_0745": [{"chinese": "他的想法有一定的局限性。", "pinyin": "Tā de xiǎngfǎ yǒu yídìng de júxiànxìng.", "meaningVi": "Suy nghĩ của anh ấy có tính hạn chế nhất định."}],
    "hsk6_0746": [{"chinese": "他的举动引起了大家的注意。", "pinyin": "Tā de jǔdòng yǐnqǐle dàjiā de zhùyì.", "meaningVi": "Hành động của anh ấy đã thu hút sự chú ý của mọi người."}],
    "hsk6_0747": [{"chinese": "这部电影的剧本写得很好。", "pinyin": "Zhè bù diànyǐng de jùběn xiě de hěn hǎo.", "meaningVi": "Kịch bản của bộ phim này viết rất hay."}],
    "hsk6_0748": [{"chinese": "人群渐渐聚集起来。", "pinyin": "Rénqún jiànjiàn jùjí qǐlai.", "meaningVi": "Đám đông dần dần tụ tập lại."}],
    "hsk6_0749": [{"chinese": "这家俱乐部每月组织一次聚会。", "pinyin": "Zhè jiā jùlèbù měi yuè zǔzhī yí cì jùhuì.", "meaningVi": "Câu lạc bộ này mỗi tháng tổ chức một buổi họp mặt."}],
    "hsk6_0750": [{"chinese": "他运动后心跳剧烈。", "pinyin": "Tā yùndòng hòu xīntiào jùliè.", "meaningVi": "Sau khi vận động tim anh ấy đập rất mạnh."}],
    "hsk6_0751": [{"chinese": "大家纷纷为灾区捐款。", "pinyin": "Dàjiā fēnfēn wèi zāiqū juānkuǎn.", "meaningVi": "Mọi người lần lượt quyên góp tiền cho vùng bị thiên tai."}],
    "hsk6_0752": [{"chinese": "他向图书馆捐赠了一批图书。", "pinyin": "Tā xiàng túshūguǎn juānzèngle yì pī túshū.", "meaningVi": "Anh ấy đã quyên tặng một lô sách cho thư viện."}],
    "hsk6_0755": [{"chinese": "这是一个重要的决策。", "pinyin": "Zhè shì yí gè zhòngyào de juécè.", "meaningVi": "Đây là một quyết sách quan trọng."}],
    "hsk6_0756": [{"chinese": "他没有绝望，继续努力。", "pinyin": "Tā méiyǒu juéwàng, jìxù nǔlì.", "meaningVi": "Anh ấy không tuyệt vọng, vẫn tiếp tục cố gắng."}],
    "hsk6_0757": [{"chinese": "军队保卫着国家的安全。", "pinyin": "Jūnduì bǎowèizhe guójiā de ānquán.", "meaningVi": "Quân đội bảo vệ an toàn của đất nước."}],
    "hsk6_0758": [{"chinese": "他从小就想成为一名军人。", "pinyin": "Tā cóngxiǎo jiù xiǎng chéngwéi yì míng jūnrén.", "meaningVi": "Anh ấy từ nhỏ đã muốn trở thành một quân nhân."}],
    "hsk6_0759": [{"chinese": "请把颜料涂抹均匀。", "pinyin": "Qǐng bǎ yánliào túmǒ jūnyún.", "meaningVi": "Xin bôi màu đều tay."}],
    "hsk6_0760": [{"chinese": "他给朋友寄了一张生日卡片。", "pinyin": "Tā gěi péngyou jìle yì zhāng shēngrì kǎpiàn.", "meaningVi": "Anh ấy đã gửi cho bạn một tấm thiệp sinh nhật."}],
    "hsk6_0761": [{"chinese": "他开创了一个新的时代。", "pinyin": "Tā kāichuàngle yí gè xīn de shídài.", "meaningVi": "Anh ấy đã mở ra một thời đại mới."}],
    "hsk6_0762": [{"chinese": "请打开电灯开关。", "pinyin": "Qǐng dǎkāi diàndēng kāiguān.", "meaningVi": "Xin bật công tắc đèn."}],
    "hsk6_0763": [{"chinese": "这次旅行开启了他人生的新篇章。", "pinyin": "Zhè cì lǚxíng kāiqǐle tā rénshēng de xīn piānzhāng.", "meaningVi": "Chuyến du lịch này đã mở ra một chương mới trong cuộc đời anh ấy."}],
    "hsk6_0764": [{"chinese": "学校开设了很多选修课。", "pinyin": "Xuéxiào kāishèle hěn duō xuǎnxiūkè.", "meaningVi": "Nhà trường đã mở nhiều môn học tự chọn."}],
    "hsk6_0765": [{"chinese": "这篇文章的开头很吸引人。", "pinyin": "Zhè piān wénzhāng de kāitóu hěn xīyǐn rén.", "meaningVi": "Phần mở đầu của bài viết này rất thu hút."}],
    "hsk6_0766": [{"chinese": "请不要随意砍伐树木。", "pinyin": "Qǐng búyào suíyì kǎnfá shùmù.", "meaningVi": "Xin đừng chặt cây một cách tùy tiện."}],
    "hsk6_0767": [{"chinese": "请不要看不起任何人。", "pinyin": "Qǐng búyào kànbuqǐ rènhé rén.", "meaningVi": "Xin đừng coi thường bất kỳ ai."}],
    "hsk6_0768": [{"chinese": "我们要客观地看待这个问题。", "pinyin": "Wǒmen yào kèguān de kàndài zhège wèntí.", "meaningVi": "Chúng ta phải nhìn nhận vấn đề này một cách khách quan."}],
    "hsk6_0769": [{"chinese": "谢谢你这么看得起我。", "pinyin": "Xièxie nǐ zhème kàndeqǐ wǒ.", "meaningVi": "Cảm ơn bạn đã coi trọng tôi như vậy."}],
    "hsk6_0770": [{"chinese": "大家都很看好这个项目。", "pinyin": "Dàjiā dōu hěn kànhǎo zhège xiàngmù.", "meaningVi": "Mọi người đều rất kỳ vọng vào dự án này."}],
    "hsk6_0771": [{"chinese": "这道题看似简单，其实很难。", "pinyin": "Zhè dào tí kànsì jiǎndān, qíshí hěn nán.", "meaningVi": "Bài toán này trông có vẻ đơn giản, nhưng thực ra rất khó."}],
    "hsk6_0772": [{"chinese": "她看中了一条裙子。", "pinyin": "Tā kànzhòngle yì tiáo qúnzi.", "meaningVi": "Cô ấy đã ưng ý một chiếc váy."}],
    "hsk6_0773": [{"chinese": "公司很看重员工的经验。", "pinyin": "Gōngsī hěn kànzhòng yuángōng de jīngyàn.", "meaningVi": "Công ty rất coi trọng kinh nghiệm của nhân viên."}],
    "hsk6_0774": [{"chinese": "祝你早日康复。", "pinyin": "Zhù nǐ zǎorì kāngfù.", "meaningVi": "Chúc bạn sớm bình phục."}],
    "hsk6_0775": [{"chinese": "他们去外地进行实地考察。", "pinyin": "Tāmen qù wàidì jìnxíng shídì kǎochá.", "meaningVi": "Họ đã đến nơi khác để khảo sát thực địa."}],
    "hsk6_0776": [{"chinese": "他是一名考古学家。", "pinyin": "Tā shì yì míng kǎogǔ xuéjiā.", "meaningVi": "Anh ấy là một nhà khảo cổ học."}],
    "hsk6_0777": [{"chinese": "公司每年对员工进行考核。", "pinyin": "Gōngsī měi nián duì yuángōng jìnxíng kǎohé.", "meaningVi": "Công ty hàng năm đều tiến hành đánh giá nhân viên."}],
    "hsk6_0778": [{"chinese": "这是对我们意志的考验。", "pinyin": "Zhè shì duì wǒmen yìzhì de kǎoyàn.", "meaningVi": "Đây là sự thử thách đối với ý chí của chúng ta."}],
    "hsk6_0779": [{"chinese": "他去医院看了内科。", "pinyin": "Tā qù yīyuàn kànle nèikē.", "meaningVi": "Anh ấy đã đến bệnh viện khám khoa nội."}],
    "hsk6_0780": [{"chinese": "他喜欢看科幻电影。", "pinyin": "Tā xǐhuan kàn kēhuàn diànyǐng.", "meaningVi": "Anh ấy thích xem phim khoa học viễn tưởng."}],
    "hsk6_0781": [{"chinese": "数学是我最喜欢的科目。", "pinyin": "Shùxué shì wǒ zuì xǐhuan de kēmù.", "meaningVi": "Toán học là môn học tôi thích nhất."}],
    "hsk6_0782": [{"chinese": "这本书是一本科普读物。", "pinyin": "Zhè běn shū shì yì běn kēpǔ dúwù.", "meaningVi": "Cuốn sách này là một cuốn sách phổ cập khoa học."}],
    "hsk6_0783": [{"chinese": "这道菜非常可口。", "pinyin": "Zhè dào cài fēicháng kěkǒu.", "meaningVi": "Món ăn này vô cùng ngon miệng."}],
    "hsk6_0784": [{"chinese": "那只流浪狗看起来很可怜。", "pinyin": "Nà zhī liúlànggǒu kàn qǐlai hěn kělián.", "meaningVi": "Con chó hoang đó trông rất đáng thương."}],
    "hsk6_0785": [{"chinese": "他渴望有一天能实现梦想。", "pinyin": "Tā kěwàng yǒu yì tiān néng shíxiàn mèngxiǎng.", "meaningVi": "Anh ấy khao khát một ngày nào đó có thể thực hiện được ước mơ."}],
    "hsk6_0786": [{"chinese": "这个计划切实可行。", "pinyin": "Zhège jìhuà qièshí kěxíng.", "meaningVi": "Kế hoạch này thực sự khả thi."}],
    "hsk6_0787": [{"chinese": "他坐客车去了外地。", "pinyin": "Tā zuò kèchē qùle wàidì.", "meaningVi": "Anh ấy đi xe khách đến nơi khác."}],
    "hsk6_0788": [{"chinese": "这是一个值得研究的课题。", "pinyin": "Zhè shì yí gè zhídé yánjiū de kètí.", "meaningVi": "Đây là một đề tài đáng để nghiên cứu."}],
    "hsk6_0789": [{"chinese": "他肯帮助别人。", "pinyin": "Tā kěn bāngzhù biéren.", "meaningVi": "Anh ấy sẵn lòng giúp đỡ người khác."}],
    "hsk6_0790": [{"chinese": "她克服了对黑暗的恐惧。", "pinyin": "Tā kèfúle duì hēi'àn de kǒngjù.", "meaningVi": "Cô ấy đã vượt qua nỗi sợ bóng tối."}],
    "hsk6_0791": [{"chinese": "这里有一块空地。", "pinyin": "Zhèlǐ yǒu yí kuài kòngdì.", "meaningVi": "Nơi đây có một khoảng đất trống."}],
    "hsk6_0792": [{"chinese": "有空闲时间我喜欢看书。", "pinyin": "Yǒu kòngxián shíjiān wǒ xǐhuan kànshū.", "meaningVi": "Khi có thời gian rảnh rỗi tôi thích đọc sách."}],
    "hsk6_0793": [{"chinese": "这种面包口感松软。", "pinyin": "Zhè zhǒng miànbāo kǒugǎn sōngruǎn.", "meaningVi": "Cảm giác khi ăn loại bánh mì này rất mềm xốp."}],
    "hsk6_0794": [{"chinese": "大家喊着口号前进。", "pinyin": "Dàjiā hǎnzhe kǒuhào qiánjìn.", "meaningVi": "Mọi người vừa hô khẩu hiệu vừa tiến lên."}],
    "hsk6_0795": [{"chinese": "请保持口腔卫生。", "pinyin": "Qǐng bǎochí kǒuqiāng wèishēng.", "meaningVi": "Xin giữ vệ sinh khoang miệng."}],
    "hsk6_0796": [{"chinese": "这只是口头约定。", "pinyin": "Zhè zhǐshì kǒutóu yuēdìng.", "meaningVi": "Đây chỉ là thỏa thuận bằng miệng."}],
    "hsk6_0797": [{"chinese": "请把扣子扣好。", "pinyin": "Qǐng bǎ kòuzi kòu hǎo.", "meaningVi": "Xin cài cúc áo cho gọn."}],
    "hsk6_0798": [{"chinese": "这份工作有点枯燥。", "pinyin": "Zhè fèn gōngzuò yǒudiǎn kūzào.", "meaningVi": "Công việc này hơi khô khan."}],
    "hsk6_0799": [{"chinese": "他穿着一身很酷的衣服。", "pinyin": "Tā chuānzhe yì shēn hěn kù de yīfu.", "meaningVi": "Anh ấy mặc một bộ quần áo rất ngầu."}],
    "hsk6_0800": [{"chinese": "大家都夸这道菜做得好。", "pinyin": "Dàjiā dōu kuā zhè dào cài zuò de hǎo.", "meaningVi": "Mọi người đều khen món ăn này làm ngon."}],
    "hsk6_0801": [{"chinese": "老师夸奖了他的进步。", "pinyin": "Lǎoshī kuājiǎngle tā de jìnbù.", "meaningVi": "Giáo viên đã khen ngợi sự tiến bộ của anh ấy."}],
    "hsk6_0802": [{"chinese": "他说话有点夸张。", "pinyin": "Tā shuōhuà yǒudiǎn kuāzhāng.", "meaningVi": "Anh ấy nói chuyện hơi phóng đại."}],
    "hsk6_0803": [{"chinese": "她是公司的会计。", "pinyin": "Tā shì gōngsī de kuàijì.", "meaningVi": "Cô ấy là kế toán của công ty."}],
    "hsk6_0804": [{"chinese": "这种支付方式非常快捷。", "pinyin": "Zhè zhǒng zhīfù fāngshì fēicháng kuàijié.", "meaningVi": "Phương thức thanh toán này vô cùng nhanh chóng."}],
    "hsk6_0805": [{"chinese": "请把余款付清。", "pinyin": "Qǐng bǎ yúkuǎn fùqīng.", "meaningVi": "Xin thanh toán hết số tiền còn lại."}],
    "hsk6_0806": [{"chinese": "这件衣服的款式很新颖。", "pinyin": "Zhè jiàn yīfu de kuǎnshì hěn xīnyǐng.", "meaningVi": "Kiểu dáng của chiếc áo này rất mới lạ."}],
    "hsk6_0807": [{"chinese": "公司这个季度出现亏损。", "pinyin": "Gōngsī zhège jìdù chūxiàn kuīsǔn.", "meaningVi": "Công ty quý này xuất hiện lỗ vốn."}],
    "hsk6_0808": [{"chinese": "这个问题一直困扰着他。", "pinyin": "Zhège wèntí yìzhí kùnrǎozhe tā.", "meaningVi": "Vấn đề này luôn làm phiền anh ấy."}],
    "hsk6_0809": [{"chinese": "公司正在扩展海外市场。", "pinyin": "Gōngsī zhèngzài kuòzhǎn hǎiwài shìchǎng.", "meaningVi": "Công ty đang mở rộng thị trường nước ngoài."}],
    "hsk6_0811": [{"chinese": "他不能吃辣椒。", "pinyin": "Tā bù néng chī làjiāo.", "meaningVi": "Anh ấy không thể ăn ớt."}],
    "hsk6_0812": [{"chinese": "走啦，我们要迟到了。", "pinyin": "Zǒu la, wǒmen yào chídào le.", "meaningVi": "Đi thôi, chúng ta sắp trễ rồi."}],
    "hsk6_0813": [{"chinese": "春天即将来临。", "pinyin": "Chūntiān jíjiāng láilín.", "meaningVi": "Mùa xuân sắp đến rồi."}],
    "hsk6_0814": [{"chinese": "他们两家一直有来往。", "pinyin": "Tāmen liǎng jiā yìzhí yǒu láiwǎng.", "meaningVi": "Hai gia đình họ luôn có qua lại."}],
    "hsk6_0815": [{"chinese": "他把责任都赖在别人身上。", "pinyin": "Tā bǎ zérèn dōu lài zài biéren shēnshang.", "meaningVi": "Anh ấy đổ hết trách nhiệm lên người khác."}],
    "hsk6_0816": [{"chinese": "请不要拦着我。", "pinyin": "Qǐng búyào lánzhe wǒ.", "meaningVi": "Xin đừng cản tôi."}],
    "hsk6_0817": [{"chinese": "请靠在栏杆上小心一点。", "pinyin": "Qǐng kào zài lángān shàng xiǎoxīn yìdiǎn.", "meaningVi": "Xin cẩn thận khi dựa vào lan can."}],
    "hsk6_0818": [{"chinese": "他家里养了几盆兰花。", "pinyin": "Tā jiālǐ yǎngle jǐ pén lánhuā.", "meaningVi": "Nhà anh ấy trồng vài chậu hoa lan."}],
    "hsk6_0819": [{"chinese": "这个苹果已经烂了。", "pinyin": "Zhège píngguǒ yǐjīng làn le.", "meaningVi": "Quả táo này đã bị thối rồi."}],
    "hsk6_0820": [{"chinese": "森林里有一群狼。", "pinyin": "Sēnlín lǐ yǒu yì qún láng.", "meaningVi": "Trong rừng có một đàn sói."}],
    "hsk6_0821": [{"chinese": "请大声朗读这篇课文。", "pinyin": "Qǐng dàshēng lǎngdú zhè piān kèwén.", "meaningVi": "Xin đọc to bài văn này."}],
    "hsk6_0822": [{"chinese": "请把绳子系牢。", "pinyin": "Qǐng bǎ shéngzi jì láo.", "meaningVi": "Xin buộc chặt sợi dây."}],
    "hsk6_0823": [{"chinese": "这个行业需要大量劳动力。", "pinyin": "Zhège hángyè xūyào dàliàng láodònglì.", "meaningVi": "Ngành này cần một lượng lớn nhân lực lao động."}],
    "hsk6_0824": [{"chinese": "他是个老实人。", "pinyin": "Tā shì gè lǎoshi rén.", "meaningVi": "Anh ấy là một người thật thà."}],
    "hsk6_0825": [{"chinese": "家里最近出现了老鼠。", "pinyin": "Jiā lǐ zuìjìn chūxiànle lǎoshǔ.", "meaningVi": "Gần đây trong nhà xuất hiện chuột."}],
    "hsk6_0826": [{"chinese": "一位老太太在公园散步。", "pinyin": "Yí wèi lǎotàitai zài gōngyuán sànbù.", "meaningVi": "Một bà cụ đang đi dạo trong công viên."}],
    "hsk6_0827": [{"chinese": "他乐于助人。", "pinyin": "Tā lèyú zhùrén.", "meaningVi": "Anh ấy sẵn lòng giúp đỡ người khác."}],
    "hsk6_0828": [{"chinese": "打雷了，快回家吧。", "pinyin": "Dǎléi le, kuài huí jiā ba.", "meaningVi": "Có sấm rồi, mau về nhà đi."}],
    "hsk6_0829": [{"chinese": "请按类别整理这些文件。", "pinyin": "Qǐng àn lèibié zhěnglǐ zhèxiē wénjiàn.", "meaningVi": "Xin sắp xếp những tài liệu này theo loại."}],
    "hsk6_0830": [{"chinese": "别理他，他在开玩笑。", "pinyin": "Bié lǐ tā, tā zài kāi wánxiào.", "meaningVi": "Đừng để ý anh ấy, anh ấy đang đùa thôi."}],
    "hsk6_0831": [{"chinese": "她很会理财。", "pinyin": "Tā hěn huì lǐcái.", "meaningVi": "Cô ấy rất giỏi quản lý tài chính."}],
    "hsk6_0832": [{"chinese": "他高中选择了理科。", "pinyin": "Tā gāozhōng xuǎnzéle lǐkē.", "meaningVi": "Anh ấy đã chọn ban khoa học tự nhiên ở trung học."}],
    "hsk6_0833": [{"chinese": "这家公司的经营理念很先进。", "pinyin": "Zhè jiā gōngsī de jīngyíng lǐniàn hěn xiānjìn.", "meaningVi": "Lý niệm kinh doanh của công ty này rất tiên tiến."}],
    "hsk6_0834": [{"chinese": "遇事要理性思考。", "pinyin": "Yùshì yào lǐxìng sīkǎo.", "meaningVi": "Gặp việc phải suy nghĩ lý trí."}],
    "hsk6_0835": [{"chinese": "他从小立志要当医生。", "pinyin": "Tā cóngxiǎo lìzhì yào dāng yīshēng.", "meaningVi": "Anh ấy từ nhỏ đã lập chí muốn làm bác sĩ."}],
    "hsk6_0836": [{"chinese": "桌上掉了几粒米。", "pinyin": "Zhuō shàng diàole jǐ lì mǐ.", "meaningVi": "Trên bàn rơi vài hạt gạo."}],
    "hsk6_0837": [{"chinese": "请说明你的立场。", "pinyin": "Qǐng shuōmíng nǐ de lìchǎng.", "meaningVi": "Xin nói rõ lập trường của bạn."}],
    "hsk6_0838": [{"chinese": "这项政策的执行力度很大。", "pinyin": "Zhè xiàng zhèngcè de zhíxíng lìdù hěn dà.", "meaningVi": "Cường độ thực thi của chính sách này rất lớn."}],
    "hsk6_0839": [{"chinese": "他历经千辛万苦才成功。", "pinyin": "Tā lìjīng qiānxīn-wànkǔ cái chénggōng.", "meaningVi": "Anh ấy đã trải qua muôn vàn khó khăn mới thành công."}],
    "hsk6_0840": [{"chinese": "历年的销售数据都保存在这里。", "pinyin": "Lìnián de xiāoshòu shùjù dōu bǎocún zài zhèlǐ.", "meaningVi": "Số liệu bán hàng của các năm đều được lưu trữ ở đây."}],
    "hsk6_0841": [{"chinese": "没有人可以例外。", "pinyin": "Méiyǒu rén kěyǐ lìwài.", "meaningVi": "Không ai có thể là ngoại lệ."}],
    "hsk6_0842": [{"chinese": "这笔存款的利息不高。", "pinyin": "Zhè bǐ cúnkuǎn de lìxī bù gāo.", "meaningVi": "Lãi suất của khoản tiền gửi này không cao."}],
    "hsk6_0843": [{"chinese": "联合国总部设在纽约。", "pinyin": "Liánhéguó zǒngbù shè zài Niǔyuē.", "meaningVi": "Trụ sở Liên Hợp Quốc đặt tại New York."}],
    "hsk6_0844": [{"chinese": "请确保设备已联网。", "pinyin": "Qǐng quèbǎo shèbèi yǐ liánwǎng.", "meaningVi": "Xin đảm bảo thiết bị đã kết nối mạng."}],
    "hsk6_0845": [{"chinese": "看到这张照片，我联想到了童年。", "pinyin": "Kàndào zhè zhāng zhàopiàn, wǒ liánxiǎng dàole tóngnián.", "meaningVi": "Nhìn thấy bức ảnh này, tôi liên tưởng đến thời thơ ấu."}],
    "hsk6_0846": [{"chinese": "请点击下面的链接。", "pinyin": "Qǐng diǎnjī xiàmiàn de liànjiē.", "meaningVi": "Xin nhấp vào liên kết bên dưới."}],
    "hsk6_0847": [{"chinese": "这座大桥连接了河的两岸。", "pinyin": "Zhè zuò dàqiáo liánjiēle hé de liǎng'àn.", "meaningVi": "Cây cầu lớn này kết nối hai bờ sông."}],
    "hsk6_0848": [{"chinese": "意见出现了两极分化。", "pinyin": "Yìjiàn chūxiànle liǎngjí fēnhuà.", "meaningVi": "Ý kiến đã xuất hiện sự phân hóa hai cực."}],
    "hsk6_0849": [{"chinese": "请把衣服晾在阳台上。", "pinyin": "Qǐng bǎ yīfu liàng zài yángtái shàng.", "meaningVi": "Xin phơi quần áo trên ban công."}],
    "hsk6_0850": [],
    "hsk6_0851": [],
    "hsk6_0852": [{"chinese": "他被雨淋湿了。", "pinyin": "Tā bèi yǔ línshī le.", "meaningVi": "Anh ấy bị mưa làm ướt."}],
    "hsk6_0853": [{"chinese": "他凌晨三点才睡觉。", "pinyin": "Tā língchén sān diǎn cái shuìjiào.", "meaningVi": "Anh ấy đến ba giờ sáng mới đi ngủ."}],
    "hsk6_0854": [{"chinese": "请按照流程办理手续。", "pinyin": "Qǐng ànzhào liúchéng bànlǐ shǒuxù.", "meaningVi": "Xin làm thủ tục theo quy trình."}],
    "hsk6_0855": [{"chinese": "空气在房间里流动。", "pinyin": "Kōngqì zài fángjiān lǐ liúdòng.", "meaningVi": "Không khí lưu thông trong phòng."}],
    "hsk6_0856": [{"chinese": "请打开浏览器搜索。", "pinyin": "Qǐng dǎkāi liúlǎnqì sōusuǒ.", "meaningVi": "Xin mở trình duyệt để tìm kiếm."}],
    "hsk6_0857": [{"chinese": "这个月的手机流量用完了。", "pinyin": "Zhège yuè de shǒujī liúliàng yòngwán le.", "meaningVi": "Dung lượng mạng di động tháng này đã dùng hết."}],
    "hsk6_0858": [{"chinese": "大量资金流入了这个市场。", "pinyin": "Dàliàng zījīn liúrùle zhège shìchǎng.", "meaningVi": "Một lượng lớn vốn đã đổ vào thị trường này."}],
    "hsk6_0859": [{"chinese": "这种货币在国际上广泛流通。", "pinyin": "Zhè zhǒng huòbì zài guójì shàng guǎngfàn liútōng.", "meaningVi": "Loại tiền tệ này được lưu thông rộng rãi trên quốc tế."}],
    "hsk6_0860": [{"chinese": "楼道里堆满了杂物。", "pinyin": "Lóudào lǐ duīmǎnle záwù.", "meaningVi": "Trong hành lang chất đầy đồ đạc linh tinh."}],
    "hsk6_0861": [{"chinese": "他很久没有在公开场合露面了。", "pinyin": "Tā hěn jiǔ méiyǒu zài gōngkāi chǎnghé lòumiàn le.", "meaningVi": "Đã lâu rồi anh ấy không xuất hiện ở nơi công cộng."}],
    "hsk6_0862": [{"chinese": "这个系统存在安全漏洞。", "pinyin": "Zhège xìtǒng cúnzài ānquán lòudòng.", "meaningVi": "Hệ thống này tồn tại lỗ hổng an ninh."}],
    "hsk6_0863": [],
    "hsk6_0864": [{"chinese": "剩下的路程不远了。", "pinyin": "Shèngxià de lùchéng bù yuǎn le.", "meaningVi": "Quãng đường còn lại không xa nữa."}],
    "hsk6_0865": [{"chinese": "今天的路况不太好。", "pinyin": "Jīntiān de lùkuàng bú tài hǎo.", "meaningVi": "Tình hình giao thông hôm nay không tốt lắm."}],
    "hsk6_0866": [{"chinese": "下雨后路面很滑。", "pinyin": "Xiàyǔ hòu lùmiàn hěn huá.", "meaningVi": "Sau khi mưa mặt đường rất trơn."}],
    "hsk6_0867": [{"chinese": "请打开监控录像。", "pinyin": "Qǐng dǎkāi jiānkòng lùxiàng.", "meaningVi": "Xin mở đoạn ghi hình camera giám sát."}],
    "hsk6_0868": [{"chinese": "他被公司正式录用了。", "pinyin": "Tā bèi gōngsī zhèngshì lùyòng le.", "meaningVi": "Anh ấy đã chính thức được công ty tuyển dụng."}],
    "hsk6_0869": [{"chinese": "这期节目已经录制完成。", "pinyin": "Zhè qī jiémù yǐjīng lùzhì wánchéng.", "meaningVi": "Tập chương trình này đã ghi hình xong."}],
    "hsk6_0870": [{"chinese": "祝你旅程愉快。", "pinyin": "Zhù nǐ lǚchéng yúkuài.", "meaningVi": "Chúc bạn có một hành trình vui vẻ."}],
    "hsk6_0871": [{"chinese": "这段旅途十分辛苦。", "pinyin": "Zhè duàn lǚtú shífēn xīnkǔ.", "meaningVi": "Chuyến đi này vô cùng vất vả."}],
    "hsk6_0872": [{"chinese": "双方都应该履行合同。", "pinyin": "Shuāngfāng dōu yīnggāi lǚxíng hétong.", "meaningVi": "Cả hai bên đều phải thực hiện hợp đồng."}],
    "hsk6_0873": [{"chinese": "这个班的及格率很高。", "pinyin": "Zhège bān de jígélǜ hěn gāo.", "meaningVi": "Tỷ lệ đạt yêu cầu của lớp này rất cao."}],
    "hsk6_0874": [{"chinese": "政府在城市里大力推行绿化。", "pinyin": "Zhèngfǔ zài chéngshì lǐ dàlì tuīxíng lǜhuà.", "meaningVi": "Chính phủ đang tích cực thực hiện phủ xanh trong thành phố."}],
    "hsk6_0875": [{"chinese": "比赛已经进行到第三轮。", "pinyin": "Bǐsài yǐjīng jìnxíng dào dì-sān lún.", "meaningVi": "Trận đấu đã diễn ra đến vòng thứ ba."}],
    "hsk6_0876": [{"chinese": "他们坐轮船去了那座岛。", "pinyin": "Tāmen zuò lúnchuán qùle nà zuò dǎo.", "meaningVi": "Họ đi tàu thủy đến hòn đảo đó."}],
    "hsk6_0877": [{"chinese": "大家轮流值班。", "pinyin": "Dàjiā lúnliú zhíbān.", "meaningVi": "Mọi người thay phiên nhau trực."}],
    "hsk6_0878": [{"chinese": "他因为受伤只能坐轮椅。", "pinyin": "Tā yīnwèi shòushāng zhǐ néng zuò lúnyǐ.", "meaningVi": "Anh ấy vì bị thương nên chỉ có thể ngồi xe lăn."}],
    "hsk6_0879": [{"chinese": "这辆自行车的轮子坏了。", "pinyin": "Zhè liàng zìxíngchē de lúnzi huài le.", "meaningVi": "Bánh xe của chiếc xe đạp này bị hỏng."}],
    "hsk6_0880": [{"chinese": "他经常在网络论坛上发言。", "pinyin": "Tā jīngcháng zài wǎngluò lùntán shàng fāyán.", "meaningVi": "Anh ấy thường xuyên phát biểu trên diễn đàn mạng."}],
    "hsk6_0881": [{"chinese": "飞机安全落地了。", "pinyin": "Fēijī ānquán luòdì le.", "meaningVi": "Máy bay đã hạ cánh an toàn."}],
    "hsk6_0882": [{"chinese": "这个地区经济比较落后。", "pinyin": "Zhège dìqū jīngjì bǐjiào luòhòu.", "meaningVi": "Kinh tế của khu vực này khá lạc hậu."}],
    "hsk6_0883": [{"chinese": "做事不能马虎。", "pinyin": "Zuòshì bù néng mǎhu.", "meaningVi": "Làm việc không được qua loa."}],
    "hsk6_0884": [{"chinese": "船已经靠近码头了。", "pinyin": "Chuán yǐjīng kàojìn mǎtou le.", "meaningVi": "Con thuyền đã gần cập bến."}],
    "hsk6_0885": [{"chinese": "地上有一群蚂蚁。", "pinyin": "Dìshang yǒu yì qún mǎyǐ.", "meaningVi": "Trên đất có một đàn kiến."}],
    "hsk6_0886": [{"chinese": "有话就直说嘛。", "pinyin": "Yǒu huà jiù zhí shuō ma.", "meaningVi": "Có gì thì cứ nói thẳng ra đi."}],
    "hsk6_0887": [{"chinese": "他把宝藏埋在了树下。", "pinyin": "Tā bǎ bǎozàng máizài le shù xià.", "meaningVi": "Anh ấy đã chôn kho báu dưới gốc cây."}],
    "hsk6_0888": [{"chinese": "他迈着大步向前走。", "pinyin": "Tā màizhe dà bù xiàng qián zǒu.", "meaningVi": "Anh ấy sải những bước dài tiến về phía trước."}],
    "hsk6_0889": [{"chinese": "请对着麦克风说话。", "pinyin": "Qǐng duìzhe màikèfēng shuōhuà.", "meaningVi": "Xin nói vào micro."}],
    "hsk6_0890": [{"chinese": "这是一段漫长的等待。", "pinyin": "Zhè shì yí duàn màncháng de děngdài.", "meaningVi": "Đây là một khoảng thời gian chờ đợi dài dằng dặc."}],
    "hsk6_0891": [{"chinese": "他从小就喜欢看漫画。", "pinyin": "Tā cóngxiǎo jiù xǐhuan kàn mànhuà.", "meaningVi": "Anh ấy từ nhỏ đã thích xem truyện tranh."}],
    "hsk6_0892": [{"chinese": "这条路专为盲人设计。", "pinyin": "Zhè tiáo lù zhuān wèi mángrén shèjì.", "meaningVi": "Con đường này được thiết kế dành riêng cho người mù."}],
    "hsk6_0893": [{"chinese": "他冒着大雨赶去上班。", "pinyin": "Tā màozhe dà yǔ gǎnqù shàngbān.", "meaningVi": "Anh ấy đội mưa lớn vội vàng đi làm."}],
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
