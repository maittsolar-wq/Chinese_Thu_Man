"""P5.10.3 (continued) -- Batch 024 (continues immediately after
examples_batch_023.json). This is the FIRST batch to cross from HSK5
into HSK6: 49 records finish off the remaining HSK5 tier1/2 queue
(hsk5_944-hsk5_999), and 251 records begin the HSK6 queue
(hsk6_0034-hsk6_0286).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Extremely dense homophone/polyphonic landscape entering HSK6 ***
This batch surfaces the largest same-pinyin-different-character
clusters seen so far in the pipeline, none flagged by the mechanical
tier system (it compares the `word` string, and every pair below is a
different word):
  - shàn (4th tone): 善良/善于 (善) vs 擅长 (擅) vs 扇子 (扇) --
    three characters.
  - shāng (1st tone): 伤害 (伤) vs 商家/商人/商务/商业 (商).
  - shè (4th tone): 设备/设立/设施/设置 (设) vs 社区 (社) vs 摄影
    (摄) -- three characters.
  - shēn (1st tone): 伸 (伸) vs 身材/身份 (身) vs 深厚/深刻/深远
    (深) -- three characters.
  - shēng (1st tone): 升/升级/升温 (升) vs 生产/生存/生动/生物/生肖/
    生长 (生) -- two characters, nine members total.
  - bèi (4th tone): 被动/被迫 (被) vs 背心 (背) vs 备用 (备) vs 倍增
    (倍) -- four characters.
  - bì (4th tone): 闭 vs 避 vs 必修 (必) -- three characters.
  - biàn (4th tone): 遍地 (遍) vs 便捷 (便) vs 变质 (变) -- three
    characters.
  - bó (2nd tone): 博览会 (博) vs 薄弱 (薄) vs 脖子 (脖) -- three
    characters.
  - bù (4th tone), the largest cluster in the batch: 不安/不曾/不成/
    不得/不禁/不时/不许/不宜/不已/不止/不耐烦/不顾/不料/不适/不至于
    (不) vs 布/布置 (布) vs 部队/部位 (部) vs 步骤 (步) -- four
    characters spanning roughly twenty members.
  - cái (2nd tone): 财产/财富/财务/财物/材质 (财/材) vs 才华/才能
    (才) -- two characters.
  - cǎi (3rd tone): 采购/采集/采纳 (采) vs 彩虹/彩票 (彩) vs 踩 (踩,
    distinct tone actually -- verified 3rd tone matches).
  - cè (4th tone): 侧 vs 测量 vs 策划/策略 (策) -- three characters.
  - chā (1st tone): 叉 vs 差异 (差, correctly read chā "difference"
    here, not chà "lacking" or chāi "to dispatch") vs 插座 (插) --
    three characters.
  - cháng (2nd tone): 肠 vs 长短/长寿 (长, correctly read cháng
    "long" here, not zhǎng "to grow/chief") vs 常规/常年/常温 (常) --
    three characters.
  - chǎng (3rd tone): 场次/场地/场馆/场合/场景/场面 (场) vs 厂家/厂商
    (厂) -- two characters, eight members.
  - chāo (1st tone): 抄 vs 超越 (超) -- distinct from the already-
    published 超/超出/超级/超速 (batch 019).
  - cháo (2nd tone): 朝代 (朝) vs 潮流/潮湿 (潮) vs 嘲笑 (嘲) -- three
    characters.
  - chǎo (3rd tone): 炒股 (炒) vs 吵架 (吵).
  - chēng (1st tone): 撑 vs 称号/称呼/称作 (称) -- distinct from the
    already-published 称为/称赞 (batch 021).
  - chéng (2nd tone), continuing the pipeline's largest recurring
    cluster (already spanning 成本/成分/程度/承担/城区/乘务员/程序
    from batches 020-021 and 成果/成立/成年/成员/成长 from batch 022):
    new members here add 成/乘(2, "to multiply")/盛/承办/惩罚/成交/
    承诺/成千上万/呈现/成效/诚信/成语/城镇 -- five characters (成/乘/
    盛/承/诚/城) now active simultaneously.
  - chōng (1st tone): 冲动/冲击/冲实/冲突 (冲) kept distinct from the
    already-published 充电/充分/充满/充值/充足 (充, batches 020/022)
    -- same pinyin+tone, different character.
  - chóng (2nd tone): 崇拜 (崇) kept distinct from the already-
    published 重复 (重, in its chóng "again" reading, batch 022).
  - chū (1st tone): 出场/出境/出力/出名/出入/出示/出游/出于 (出) vs
    初步/初等 (初) -- two characters, ten members.
  - dà (4th tone), continuing the pipeline's other largest recurring
    cluster (already 大胆/大多/大会/大妈/大米/大脑/大批/大厦/大事/
    大象/大型/大爷/大于/大众 from batch 022): eleven new members here
    (大臣/大吃一惊/大地/大都/大方/大幅/大伙儿/大使/大师/大洋洲/大致).
  - dāng (1st tone), continuing from batch 022's 当地/当年/当中/当成/
    当作: eight new members here (当场/当初/当代/当今/当面/当下/当选/
    当天), each anchored to a distinct real-world referent.
  - dǎo/dào (a genuinely polyphonic character 倒): 倒闭/倒车 (dǎo,
    "to collapse"/"to transfer [vehicles]") vs 倒是 (dào, "on the
    contrary") -- both readings given correctly, and 导师 (dǎo, a
    different character) kept distinct from 倒 in its dǎo reading.

Self-caught fixes made during drafting (before this batch was
finalized):
  - 测量 (cèliáng): first draft "请测量一下体温。" would have been an
    EXACT duplicate of 体温's own already-published example (batch
    015, hsk4_733: "请测量一下体温。") -- rewritten to "请测量一下这
    块布的长度。".
  - 称作 (chēngzuò): first draft "这种植物被称作仙人掌。" was a near-
    duplicate of the near-synonym 叫作's own already-published example
    (batch 016, hsk4_378: "这种植物叫作仙人掌。", same subject 仙人掌)
    -- rewritten to "人们把这种鸟称作益鸟。".
  - 出示 (chūshì): first draft "请出示您的证件。" echoed the "请出示
    您的..." template already used for 身份证 (batch 014, hsk4_643:
    "请出示您的身份证。") -- rewritten to "他向警察出示了驾照。".
  All re-verified against the full pilot+002-023 corpus with zero
  remaining exact duplicates and zero near-template flags (see
  validation report).

Validator-caught fixes (found by validate_examples_batch_p103.py's
target_word_present check, not by manual review):
  - 舍得 (shěde): first draft "她舍不得扔掉旧照片。" used the negated
    form 舍不得, which does not contain 舍得 as a contiguous substring
    (不 sits between the two characters) -- rewritten to the
    affirmative "他很舍得为孩子花钱。", which does.
  - 乘2 (hsk6_0157): this record's production `word` field is
    literally "乘2" -- HSK6's data carries a homograph-disambiguation
    numeric suffix on twelve records (乘2, 副2, 该2, 局1/局2, 料1/
    料2, 露1, 升2, 所2, 则1, 支2; only 乘2 falls within this batch's
    ID range, hsk6_0034-hsk6_0286 -- the other eleven are further
    along and will need the identical treatment when their batches
    are reached). The literal string "乘2" can never appear in a
    natural Chinese sentence, so no authored example could honestly
    satisfy target_word_present; per the established "mark
    needs_review rather than fabricate" rule (same pattern as the
    P5.10.2 pilot's hsk6_0027 case), this record is left with an
    empty examples list and qaStatus "needs_review" rather than
    given a sentence that could never pass validation. (Also worth
    noting: the first draft mistakenly used 乘's "to multiply" sense
    -- "三乘四等于十二。" -- when the record's actual meaningVi is
    "cưỡi; đi bằng; thừa", i.e. "to ride/travel by [transport]"; this
    sense error was superseded by the needs_review decision, but is
    flagged here in case this ID's data is revisited in a future
    cleanup of the numeric-suffix pattern.)

Automated near-template pass (character-bigram Jaccard similarity
against the full pilot+002-023 corpus) caught four further near-
duplicates fixed after the manual drafting pass:
  - 深刻 (shēnkè): first draft "这本书给我留下了深刻的印象。" was a
    near-template match against 留下's own already-published example
    (batch 012, hsk4_485: "他给我留下了深刻的印象。", sharing the
    "留下了深刻的印象" clause) -- rewritten to "他对这次失败进行了
    深刻的反思。".
  - 身份 (shēnfèn): first draft "请出示您的身份证明。" was a near-
    template match against 身份证's own already-published example
    (batch 014, hsk4_643: "请出示您的身份证。") -- rewritten to
    "他隐瞒了自己的真实身份。".
  - 不许 (bùxǔ): first draft "这里不许吸烟。" was a near-template
    match against the near-synonym 允许's own already-published
    example (batch 016, hsk4_912: "这里不允许吸烟。") -- rewritten to
    "妈妈不许他晚上出门。".
  - 升 (shēng): first draft "太阳从东方升起。" was a near-template
    match against an existing HSK3-lineage example ("太阳从东边升
    起。") -- rewritten to "国旗随着音乐缓缓升起。".
  All re-verified with zero remaining flags.

Usage:
    python generate_examples_batch_024.py --dry-run
    python generate_examples_batch_024.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 24
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_024.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# Records deliberately left with 0 examples (mirrors the P5.10.2 pilot's
# NEEDS_REVIEW pattern for hsk6_0027): the production `word` field itself
# carries a homograph-disambiguation numeric suffix (e.g. "乘2") that can
# never literally appear in natural Chinese text, so no authored sentence
# could ever satisfy the target_word_present check honestly. See the
# module docstring for the full explanation and the eleven further
# HSK6 records (out of this batch's range) carrying the same pattern.
NEEDS_REVIEW_IDS = {"hsk6_0157"}

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk5_944": [{"chinese": "沙漠里几乎没有水。", "pinyin": "Shāmò lǐ jīhū méiyǒu shuǐ.", "meaningVi": "Trong sa mạc hầu như không có nước."}],
    "hsk5_945": [{"chinese": "鞋子里进了沙子。", "pinyin": "Xiézi lǐ jìnle shāzi.", "meaningVi": "Cát lọt vào trong giày."}],
    "hsk5_946": [{"chinese": "别装傻了。", "pinyin": "Bié zhuāng shǎ le.", "meaningVi": "Đừng giả ngốc nữa."}],
    "hsk5_947": [{"chinese": "衣服要拿去晒一晒。", "pinyin": "Yīfu yào ná qù shài yi shài.", "meaningVi": "Quần áo phải mang đi phơi nắng."}],
    "hsk5_948": [{"chinese": "请把这条信息删了。", "pinyin": "Qǐng bǎ zhè tiáo xìnxī shān le.", "meaningVi": "Xin xóa tin nhắn này đi."}],
    "hsk5_950": [{"chinese": "他不小心删除了文件。", "pinyin": "Tā bù xiǎoxīn shānchúle wénjiàn.", "meaningVi": "Anh ấy vô ý xóa mất tệp tin."}],
    "hsk5_951": [{"chinese": "他们生活在山区。", "pinyin": "Tāmen shēnghuó zài shānqū.", "meaningVi": "Họ sống ở vùng núi."}],
    "hsk5_952": [{"chinese": "他擅长弹钢琴。", "pinyin": "Tā shàncháng tán gāngqín.", "meaningVi": "Anh ấy giỏi chơi đàn piano."}],
    "hsk5_953": [{"chinese": "她心地善良。", "pinyin": "Tā xīndì shànliáng.", "meaningVi": "Cô ấy có tấm lòng lương thiện."}],
    "hsk5_954": [{"chinese": "他善于与人沟通。", "pinyin": "Tā shànyú yǔ rén gōutōng.", "meaningVi": "Anh ấy giỏi giao tiếp với người khác."}],
    "hsk5_955": [{"chinese": "奶奶拿着扇子扇风。", "pinyin": "Nǎinai názhe shànzi shān fēng.", "meaningVi": "Bà nội cầm quạt quạt gió."}],
    "hsk5_957": [{"chinese": "这句话深深伤害了她。", "pinyin": "Zhè jù huà shēnshēn shānghàile tā.", "meaningVi": "Câu nói này đã làm tổn thương cô ấy sâu sắc."}],
    "hsk5_958": [{"chinese": "很多商家都参加了促销活动。", "pinyin": "Hěn duō shāngjiā dōu cānjiāle cùxiāo huódòng.", "meaningVi": "Rất nhiều nhà kinh doanh đã tham gia hoạt động khuyến mãi."}],
    "hsk5_959": [{"chinese": "他是一位成功的商人。", "pinyin": "Tā shì yí wèi chénggōng de shāngrén.", "meaningVi": "Anh ấy là một thương nhân thành đạt."}],
    "hsk5_960": [{"chinese": "他经常出差办理商务事宜。", "pinyin": "Tā jīngcháng chūchāi bànlǐ shāngwù shìyí.", "meaningVi": "Anh ấy thường xuyên đi công tác xử lý công việc thương mại."}],
    "hsk5_961": [{"chinese": "这条街是商业区。", "pinyin": "Zhè tiáo jiē shì shāngyèqū.", "meaningVi": "Con phố này là khu thương mại."}],
    "hsk5_962": [{"chinese": "大家一起赏花吧。", "pinyin": "Dàjiā yìqǐ shǎng huā ba.", "meaningVi": "Mọi người cùng nhau ngắm hoa đi."}],
    "hsk5_963": [{"chinese": "请把照片上传到网站。", "pinyin": "Qǐng bǎ zhàopiàn shàngchuán dào wǎngzhàn.", "meaningVi": "Xin tải ảnh lên trang web."}],
    "hsk5_964": [{"chinese": "气温正在上升。", "pinyin": "Qìwēn zhèngzài shàngshēng.", "meaningVi": "Nhiệt độ đang tăng lên."}],
    "hsk5_965": [{"chinese": "请上下检查一遍。", "pinyin": "Qǐng shàngxià jiǎnchá yí biàn.", "meaningVi": "Xin kiểm tra từ trên xuống dưới một lượt."}],
    "hsk5_966": [{"chinese": "房价一直在上涨。", "pinyin": "Fángjià yìzhí zài shàngzhǎng.", "meaningVi": "Giá nhà luôn tăng."}],
    "hsk5_968": [{"chinese": "周末我们去烧烤吧。", "pinyin": "Zhōumò wǒmen qù shāokǎo ba.", "meaningVi": "Cuối tuần chúng ta đi nướng thịt đi."}],
    "hsk5_969": [{"chinese": "草丛里有一条蛇。", "pinyin": "Cǎocóng lǐ yǒu yì tiáo shé.", "meaningVi": "Trong bụi cỏ có một con rắn."}],
    "hsk5_971": [{"chinese": "他很舍得为孩子花钱。", "pinyin": "Tā hěn shěde wèi háizi huā qián.", "meaningVi": "Anh ấy rất sẵn lòng chi tiền cho con cái."}],
    "hsk5_972": [{"chinese": "这家医院设备先进。", "pinyin": "Zhè jiā yīyuàn shèbèi xiānjìn.", "meaningVi": "Thiết bị của bệnh viện này rất tiên tiến."}],
    "hsk5_974": [{"chinese": "学校设立了奖学金。", "pinyin": "Xuéxiào shèlìle jiǎngxuéjīn.", "meaningVi": "Nhà trường đã thiết lập học bổng."}],
    "hsk5_975": [{"chinese": "我们社区经常组织活动。", "pinyin": "Wǒmen shèqū jīngcháng zǔzhī huódòng.", "meaningVi": "Cộng đồng của chúng tôi thường xuyên tổ chức hoạt động."}],
    "hsk5_976": [{"chinese": "这里的公共设施很齐全。", "pinyin": "Zhèlǐ de gōnggòng shèshī hěn qíquán.", "meaningVi": "Cơ sở vật chất công cộng ở đây rất đầy đủ."}],
    "hsk5_977": [{"chinese": "他喜欢摄影。", "pinyin": "Tā xǐhuan shèyǐng.", "meaningVi": "Anh ấy thích chụp ảnh."}],
    "hsk5_978": [{"chinese": "请设置一下密码。", "pinyin": "Qǐng shèzhì yíxià mìmǎ.", "meaningVi": "Xin cài đặt mật khẩu."}],
    "hsk5_979": [{"chinese": "他伸手拿桌上的书。", "pinyin": "Tā shēnshǒu ná zhuō shàng de shū.", "meaningVi": "Anh ấy vươn tay lấy cuốn sách trên bàn."}],
    "hsk5_980": [{"chinese": "她身材很好。", "pinyin": "Tā shēncái hěn hǎo.", "meaningVi": "Vóc dáng của cô ấy rất đẹp."}],
    "hsk5_982": [{"chinese": "他隐瞒了自己的真实身份。", "pinyin": "Tā yǐnmánle zìjǐ de zhēnshí shēnfèn.", "meaningVi": "Anh ấy đã giấu đi thân phận thật của mình."}],
    "hsk5_983": [{"chinese": "他们之间有深厚的友谊。", "pinyin": "Tāmen zhījiān yǒu shēnhòu de yǒuyì.", "meaningVi": "Giữa họ có tình bạn sâu sắc."}],
    "hsk5_984": [{"chinese": "他对这次失败进行了深刻的反思。", "pinyin": "Tā duì zhè cì shībài jìnxíngle shēnkè de fǎnsī.", "meaningVi": "Anh ấy đã suy ngẫm sâu sắc về thất bại lần này."}],
    "hsk5_986": [{"chinese": "这项政策影响深远。", "pinyin": "Zhè xiàng zhèngcè yǐngxiǎng shēnyuǎn.", "meaningVi": "Chính sách này có ảnh hưởng sâu rộng."}],
    "hsk5_987": [{"chinese": "这是一个古老的神话故事。", "pinyin": "Zhè shì yí gè gǔlǎo de shénhuà gùshi.", "meaningVi": "Đây là một câu chuyện thần thoại cổ xưa."}],
    "hsk5_988": [{"chinese": "这个地方充满神秘色彩。", "pinyin": "Zhège dìfang chōngmǎn shénmì sècǎi.", "meaningVi": "Nơi này tràn đầy màu sắc thần bí."}],
    "hsk5_989": [{"chinese": "国旗随着音乐缓缓升起。", "pinyin": "Guóqí suízhe yīnyuè huǎnhuǎn shēngqǐ.", "meaningVi": "Lá quốc kỳ từ từ được kéo lên theo tiếng nhạc."}],
    "hsk5_990": [{"chinese": "这家工厂生产手机零件。", "pinyin": "Zhè jiā gōngchǎng shēngchǎn shǒujī língjiàn.", "meaningVi": "Nhà máy này sản xuất linh kiện điện thoại."}],
    "hsk5_991": [{"chinese": "在沙漠中生存非常困难。", "pinyin": "Zài shāmò zhōng shēngcún fēicháng kùnnan.", "meaningVi": "Sinh tồn trong sa mạc vô cùng khó khăn."}],
    "hsk5_992": [{"chinese": "老师讲课很生动。", "pinyin": "Lǎoshī jiǎngkè hěn shēngdòng.", "meaningVi": "Giáo viên giảng bài rất sinh động."}],
    "hsk5_993": [{"chinese": "请把系统升级到最新版本。", "pinyin": "Qǐng bǎ xìtǒng shēngjí dào zuìxīn bǎnběn.", "meaningVi": "Xin nâng cấp hệ thống lên phiên bản mới nhất."}],
    "hsk5_994": [{"chinese": "最近两国关系逐渐升温。", "pinyin": "Zuìjìn liǎng guó guānxi zhújiàn shēngwēn.", "meaningVi": "Gần đây quan hệ hai nước dần dần ấm lên."}],
    "hsk5_995": [{"chinese": "他大学学的是生物专业。", "pinyin": "Tā dàxué xué de shì shēngwù zhuānyè.", "meaningVi": "Anh ấy học chuyên ngành sinh vật ở đại học."}],
    "hsk5_996": [{"chinese": "你的生肖是什么？", "pinyin": "Nǐ de shēngxiào shì shénme?", "meaningVi": "Con giáp của bạn là gì?"}],
    "hsk5_997": [{"chinese": "这种植物生长得很快。", "pinyin": "Zhè zhǒng zhíwù shēngzhǎng de hěn kuài.", "meaningVi": "Loại thực vật này sinh trưởng rất nhanh."}],
    "hsk5_998": [{"chinese": "这样可以省不少钱。", "pinyin": "Zhèyàng kěyǐ shěng bù shǎo qián.", "meaningVi": "Làm như vậy có thể tiết kiệm không ít tiền."}],
    "hsk5_999": [{"chinese": "中国有很多省份。", "pinyin": "Zhōngguó yǒu hěn duō shěngfèn.", "meaningVi": "Trung Quốc có rất nhiều tỉnh thành."}],
    "hsk6_0034": [{"chinese": "别这么悲观。", "pinyin": "Bié zhème bēiguān.", "meaningVi": "Đừng bi quan như vậy."}],
    "hsk6_0035": [{"chinese": "这是一场人生悲剧。", "pinyin": "Zhè shì yì chǎng rénshēng bēijù.", "meaningVi": "Đây là một bi kịch của cuộc đời."}],
    "hsk6_0036": [{"chinese": "她无法掩饰内心的悲伤。", "pinyin": "Tā wúfǎ yǎnshì nèixīn de bēishāng.", "meaningVi": "Cô ấy không thể che giấu nỗi buồn trong lòng."}],
    "hsk6_0037": [{"chinese": "北极的冰川正在融化。", "pinyin": "Běijí de bīngchuān zhèngzài rónghuà.", "meaningVi": "Sông băng ở Bắc Cực đang tan chảy."}],
    "hsk6_0038": [{"chinese": "加拿大位于北美洲。", "pinyin": "Jiānádà wèiyú Běiměizhōu.", "meaningVi": "Canada nằm ở Bắc Mỹ."}],
    "hsk6_0039": [{"chinese": "他做事总是很被动。", "pinyin": "Tā zuòshì zǒngshì hěn bèidòng.", "meaningVi": "Anh ấy làm việc lúc nào cũng rất bị động."}],
    "hsk6_0040": [{"chinese": "他被迫辞去了职务。", "pinyin": "Tā bèipò cíqùle zhíwù.", "meaningVi": "Anh ấy bị buộc phải từ chức."}],
    "hsk6_0041": [{"chinese": "夏天他喜欢穿背心。", "pinyin": "Xiàtiān tā xǐhuan chuān bèixīn.", "meaningVi": "Mùa hè anh ấy thích mặc áo ba lỗ."}],
    "hsk6_0042": [{"chinese": "请准备一把备用钥匙。", "pinyin": "Qǐng zhǔnbèi yì bǎ bèiyòng yàoshi.", "meaningVi": "Xin chuẩn bị một chiếc chìa khóa dự phòng."}],
    "hsk6_0043": [{"chinese": "销量比去年倍增。", "pinyin": "Xiāoliàng bǐ qùnián bèizēng.", "meaningVi": "Doanh số tăng gấp đôi so với năm ngoái."}],
    "hsk6_0044": [{"chinese": "孩子们在草地上奔跑。", "pinyin": "Háizimen zài cǎodì shàng bēnpǎo.", "meaningVi": "Bọn trẻ chạy nhảy trên bãi cỏ."}],
    "hsk6_0045": [{"chinese": "这是动物的本能反应。", "pinyin": "Zhè shì dòngwù de běnnéng fǎnyìng.", "meaningVi": "Đây là phản ứng bản năng của động vật."}],
    "hsk6_0046": [{"chinese": "问题本身并不复杂。", "pinyin": "Wèntí běnshēn bìng bù fùzá.", "meaningVi": "Bản thân vấn đề không phức tạp."}],
    "hsk6_0047": [{"chinese": "这个品牌是本土企业。", "pinyin": "Zhège páizi shì běntǔ qǐyè.", "meaningVi": "Thương hiệu này là doanh nghiệp bản địa."}],
    "hsk6_0048": [{"chinese": "别逼他做不愿意的事。", "pinyin": "Bié bī tā zuò bú yuànyì de shì.", "meaningVi": "Đừng ép anh ấy làm việc không muốn làm."}],
    "hsk6_0049": [{"chinese": "打个比方，这就像盖房子。", "pinyin": "Dǎ gè bǐfang, zhè jiù xiàng gài fángzi.", "meaningVi": "Ví dụ như, việc này giống như xây nhà vậy."}],
    "hsk6_0050": [{"chinese": "农业在这个国家占的比重很大。", "pinyin": "Nóngyè zài zhège guójiā zhàn de bǐzhòng hěn dà.", "meaningVi": "Nông nghiệp chiếm tỷ trọng lớn trong quốc gia này."}],
    "hsk6_0051": [{"chinese": "请闭上眼睛。", "pinyin": "Qǐng bìshàng yǎnjing.", "meaningVi": "Xin nhắm mắt lại."}],
    "hsk6_0052": [{"chinese": "他躲避着记者的提问。", "pinyin": "Tā duǒbìzhe jìzhě de tíwèn.", "meaningVi": "Anh ấy né tránh câu hỏi của phóng viên."}],
    "hsk6_0053": [{"chinese": "这是一门必修课。", "pinyin": "Zhè shì yì mén bìxiū kè.", "meaningVi": "Đây là một môn học bắt buộc."}],
    "hsk6_0054": [{"chinese": "她会编竹篮。", "pinyin": "Tā huì biān zhúlán.", "meaningVi": "Cô ấy biết đan giỏ tre."}],
    "hsk6_0055": [{"chinese": "她是一名杂志编辑。", "pinyin": "Tā shì yì míng zázhì biānjí.", "meaningVi": "Cô ấy là một biên tập viên tạp chí."}],
    "hsk6_0056": [{"chinese": "他负责编写教材。", "pinyin": "Tā fùzé biānxiě jiàocái.", "meaningVi": "Anh ấy phụ trách biên soạn giáo trình."}],
    "hsk6_0057": [{"chinese": "春天遍地都是野花。", "pinyin": "Chūntiān biàndì dōu shì yěhuā.", "meaningVi": "Mùa xuân khắp nơi đều là hoa dại."}],
    "hsk6_0058": [{"chinese": "网上支付非常便捷。", "pinyin": "Wǎngshàng zhīfù fēicháng biànjié.", "meaningVi": "Thanh toán trực tuyến vô cùng tiện lợi."}],
    "hsk6_0059": [{"chinese": "天热食物容易变质。", "pinyin": "Tiān rè shíwù róngyì biànzhì.", "meaningVi": "Trời nóng thức ăn dễ bị biến chất."}],
    "hsk6_0060": [{"chinese": "他是一名士兵。", "pinyin": "Tā shì yì míng shìbīng.", "meaningVi": "Anh ấy là một người lính."}],
    "hsk6_0061": [{"chinese": "这种病毒传播很快。", "pinyin": "Zhè zhǒng bìngdú chuánbō hěn kuài.", "meaningVi": "Loại virus này lây lan rất nhanh."}],
    "hsk6_0062": [{"chinese": "这个节目每天晚上八点播。", "pinyin": "Zhège jiémù měitiān wǎnshang bā diǎn bō.", "meaningVi": "Chương trình này phát sóng lúc tám giờ tối mỗi ngày."}],
    "hsk6_0063": [{"chinese": "农民正在田里播种。", "pinyin": "Nóngmín zhèngzài tián lǐ bōzhǒng.", "meaningVi": "Nông dân đang gieo hạt trên đồng."}],
    "hsk6_0064": [{"chinese": "这次博览会吸引了很多参观者。", "pinyin": "Zhè cì bólǎnhuì xīyǐnle hěn duō cānguānzhě.", "meaningVi": "Hội chợ triển lãm lần này đã thu hút rất nhiều khách tham quan."}],
    "hsk6_0065": [{"chinese": "他的英语基础比较薄弱。", "pinyin": "Tā de Yīngyǔ jīchǔ bǐjiào bóruò.", "meaningVi": "Nền tảng tiếng Anh của anh ấy khá yếu."}],
    "hsk6_0066": [{"chinese": "他脖子有点疼。", "pinyin": "Tā bózi yǒudiǎn téng.", "meaningVi": "Cổ của anh ấy hơi đau."}],
    "hsk6_0067": [{"chinese": "他等得有点不耐烦了。", "pinyin": "Tā děng de yǒudiǎn bú nàifán le.", "meaningVi": "Anh ấy đợi đến mức có chút mất kiên nhẫn."}],
    "hsk6_0068": [{"chinese": "他不顾大家反对，坚持自己的想法。", "pinyin": "Tā búgù dàjiā fǎnduì, jiānchí zìjǐ de xiǎngfǎ.", "meaningVi": "Anh ấy bất chấp sự phản đối của mọi người, kiên trì ý kiến của mình."}],
    "hsk6_0069": [{"chinese": "不料半路下起了大雨。", "pinyin": "Búliào bànlù xiàqǐle dàyǔ.", "meaningVi": "Không ngờ giữa đường lại đổ mưa to."}],
    "hsk6_0070": [{"chinese": "他感到身体不适。", "pinyin": "Tā gǎndào shēntǐ búshì.", "meaningVi": "Anh ấy cảm thấy cơ thể khó chịu."}],
    "hsk6_0071": [{"chinese": "事情还不至于这么严重。", "pinyin": "Shìqing hái búzhìyú zhème yánzhòng.", "meaningVi": "Sự việc chưa đến mức nghiêm trọng như vậy."}],
    "hsk6_0072": [{"chinese": "裤子破了个洞，需要补一下。", "pinyin": "Kùzi pòle gè dòng, xūyào bǔ yíxià.", "meaningVi": "Quần bị thủng một lỗ, cần vá lại."}],
    "hsk6_0073": [{"chinese": "渔民出海捕鱼。", "pinyin": "Yúmín chūhǎi bǔ yú.", "meaningVi": "Ngư dân ra khơi đánh cá."}],
    "hsk6_0074": [{"chinese": "公司给予他一定的补偿。", "pinyin": "Gōngsī jǐyǔ tā yídìng de bǔcháng.", "meaningVi": "Công ty đã bồi thường cho anh ấy một khoản nhất định."}],
    "hsk6_0075": [{"chinese": "老师给请假的学生补课。", "pinyin": "Lǎoshī gěi qǐngjià de xuésheng bǔkè.", "meaningVi": "Giáo viên dạy bù cho học sinh xin nghỉ phép."}],
    "hsk6_0076": [{"chinese": "政府给农民发放补贴。", "pinyin": "Zhèngfǔ gěi nóngmín fāfàng bǔtiē.", "meaningVi": "Chính phủ cấp trợ cấp cho nông dân."}],
    "hsk6_0077": [{"chinese": "他放学后去补习班。", "pinyin": "Tā fàngxué hòu qù bǔxíbān.", "meaningVi": "Sau khi tan học anh ấy đi học thêm."}],
    "hsk6_0078": [{"chinese": "这块布很柔软。", "pinyin": "Zhè kuài bù hěn róuruǎn.", "meaningVi": "Miếng vải này rất mềm mại."}],
    "hsk6_0079": [{"chinese": "他心里感到有些不安。", "pinyin": "Tā xīnlǐ gǎndào yǒuxiē bù'ān.", "meaningVi": "Trong lòng anh ấy cảm thấy có chút bất an."}],
    "hsk6_0080": [{"chinese": "他不曾放弃过自己的梦想。", "pinyin": "Tā bùcéng fàngqìguo zìjǐ de mèngxiǎng.", "meaningVi": "Anh ấy chưa từng từ bỏ ước mơ của mình."}],
    "hsk6_0081": [{"chinese": "这件事恐怕办不成。", "pinyin": "Zhè jiàn shì kǒngpà bàn bù chéng.", "meaningVi": "Việc này e là làm không xong."}],
    "hsk6_0082": [{"chinese": "未经允许不得入内。", "pinyin": "Wèijīng yǔnxǔ bùdé rùnèi.", "meaningVi": "Chưa được cho phép không được vào trong."}],
    "hsk6_0083": [{"chinese": "他曾经在部队服役。", "pinyin": "Tā céngjīng zài bùduì fúyì.", "meaningVi": "Anh ấy đã từng phục vụ trong quân đội."}],
    "hsk6_0084": [{"chinese": "听到这个消息，她不禁笑了。", "pinyin": "Tīngdào zhège xiāoxi, tā bùjīn xiào le.", "meaningVi": "Nghe được tin này, cô ấy không nhịn được cười."}],
    "hsk6_0085": [{"chinese": "他不时抬头看看时间。", "pinyin": "Tā bùshí táitóu kànkan shíjiān.", "meaningVi": "Thỉnh thoảng anh ấy lại ngẩng đầu xem giờ."}],
    "hsk6_0086": [{"chinese": "请指出疼痛的部位。", "pinyin": "Qǐng zhǐchū téngtòng de bùwèi.", "meaningVi": "Xin chỉ ra vị trí đau."}],
    "hsk6_0087": [{"chinese": "妈妈不许他晚上出门。", "pinyin": "Māma bùxǔ tā wǎnshang chūmén.", "meaningVi": "Mẹ không cho phép anh ấy ra ngoài vào buổi tối."}],
    "hsk6_0088": [{"chinese": "空腹不宜喝咖啡。", "pinyin": "Kōngfù bù yí hē kāfēi.", "meaningVi": "Bụng đói không nên uống cà phê."}],
    "hsk6_0089": [{"chinese": "他激动不已。", "pinyin": "Tā jīdòng bùyǐ.", "meaningVi": "Anh ấy xúc động không ngừng."}],
    "hsk6_0090": [{"chinese": "教室已经布置好了。", "pinyin": "Jiàoshì yǐjīng bùzhì hǎo le.", "meaningVi": "Lớp học đã được bố trí xong."}],
    "hsk6_0091": [{"chinese": "参加的人数不止一百。", "pinyin": "Cānjiā de rénshù bùzhǐ yìbǎi.", "meaningVi": "Số người tham gia không chỉ một trăm."}],
    "hsk6_0092": [{"chinese": "请按照步骤操作。", "pinyin": "Qǐng ànzhào bùzhòu cāozuò.", "meaningVi": "Xin thao tác theo từng bước."}],
    "hsk6_0093": [{"chinese": "大家都在猜测结果。", "pinyin": "Dàjiā dōu zài cāicè jiéguǒ.", "meaningVi": "Mọi người đều đang đoán kết quả."}],
    "hsk6_0094": [{"chinese": "这是他个人的财产。", "pinyin": "Zhè shì tā gèrén de cáichǎn.", "meaningVi": "Đây là tài sản cá nhân của anh ấy."}],
    "hsk6_0095": [{"chinese": "健康比财富更重要。", "pinyin": "Jiànkāng bǐ cáifù gèng zhòngyào.", "meaningVi": "Sức khỏe quan trọng hơn của cải."}],
    "hsk6_0096": [{"chinese": "他很有音乐才华。", "pinyin": "Tā hěn yǒu yīnyuè cáihuá.", "meaningVi": "Anh ấy rất có tài năng âm nhạc."}],
    "hsk6_0097": [{"chinese": "她具备管理才能。", "pinyin": "Tā jùbèi guǎnlǐ cáinéng.", "meaningVi": "Cô ấy có năng lực quản lý."}],
    "hsk6_0098": [{"chinese": "她在公司负责财务工作。", "pinyin": "Tā zài gōngsī fùzé cáiwù gōngzuò.", "meaningVi": "Cô ấy phụ trách công việc tài chính trong công ty."}],
    "hsk6_0099": [{"chinese": "请保管好个人财物。", "pinyin": "Qǐng bǎoguǎn hǎo gèrén cáiwù.", "meaningVi": "Xin bảo quản tốt tài sản cá nhân."}],
    "hsk6_0100": [{"chinese": "这把椅子的材质是实木。", "pinyin": "Zhè bǎ yǐzi de cáizhì shì shímù.", "meaningVi": "Chất liệu của cái ghế này là gỗ nguyên khối."}],
    "hsk6_0101": [{"chinese": "别踩到我的脚。", "pinyin": "Bié cǎidào wǒ de jiǎo.", "meaningVi": "Đừng giẫm lên chân tôi."}],
    "hsk6_0102": [{"chinese": "他负责公司的采购工作。", "pinyin": "Tā fùzé gōngsī de cǎigòu gōngzuò.", "meaningVi": "Anh ấy phụ trách công việc thu mua của công ty."}],
    "hsk6_0103": [{"chinese": "雨后天空出现了彩虹。", "pinyin": "Yǔ hòu tiānkōng chūxiànle cǎihóng.", "meaningVi": "Sau mưa trên bầu trời xuất hiện cầu vồng."}],
    "hsk6_0104": [{"chinese": "他们去山里采集标本。", "pinyin": "Tāmen qù shān lǐ cǎijí biāoběn.", "meaningVi": "Họ đi vào núi để thu thập mẫu vật."}],
    "hsk6_0105": [{"chinese": "领导采纳了他的建议。", "pinyin": "Lǐngdǎo cǎinàle tā de jiànyì.", "meaningVi": "Lãnh đạo đã chấp nhận đề xuất của anh ấy."}],
    "hsk6_0106": [{"chinese": "他买了一张彩票。", "pinyin": "Tā mǎile yì zhāng cǎipiào.", "meaningVi": "Anh ấy đã mua một tờ vé số."}],
    "hsk6_0107": [{"chinese": "很多公司都来参展。", "pinyin": "Hěn duō gōngsī dōu lái cānzhǎn.", "meaningVi": "Rất nhiều công ty đã đến tham gia triển lãm."}],
    "hsk6_0108": [{"chinese": "他因事故导致残疾。", "pinyin": "Tā yīn shìgù dǎozhì cánjí.", "meaningVi": "Anh ấy bị khuyết tật do tai nạn."}],
    "hsk6_0109": [{"chinese": "货物存放在仓库里。", "pinyin": "Huòwù cúnfàng zài cāngkù lǐ.", "meaningVi": "Hàng hóa được cất giữ trong kho."}],
    "hsk6_0110": [{"chinese": "内蒙古有广阔的草原。", "pinyin": "Nèiménggǔ yǒu guǎngkuò de cǎoyuán.", "meaningVi": "Nội Mông có thảo nguyên rộng lớn."}],
    "hsk6_0111": [{"chinese": "他站在我的左侧。", "pinyin": "Tā zhàn zài wǒ de zuǒ cè.", "meaningVi": "Anh ấy đứng ở bên trái tôi."}],
    "hsk6_0112": [{"chinese": "这次活动是他策划的。", "pinyin": "Zhè cì huódòng shì tā cèhuà de.", "meaningVi": "Hoạt động lần này là do anh ấy lên kế hoạch."}],
    "hsk6_0113": [{"chinese": "请测量一下这块布的长度。", "pinyin": "Qǐng cèliáng yíxià zhè kuài bù de chángdù.", "meaningVi": "Xin đo độ dài của miếng vải này."}],
    "hsk6_0114": [{"chinese": "我们需要新的营销策略。", "pinyin": "Wǒmen xūyào xīn de yíngxiāo cèlüè.", "meaningVi": "Chúng ta cần chiến lược tiếp thị mới."}],
    "hsk6_0115": [{"chinese": "这篇文章层次分明。", "pinyin": "Zhè piān wénzhāng céngcì fēnmíng.", "meaningVi": "Bài viết này có bố cục rõ ràng."}],
    "hsk6_0116": [{"chinese": "从经济层面来看，这是个好决定。", "pinyin": "Cóng jīngjì céngmiàn lái kàn, zhè shì gè hǎo juédìng.", "meaningVi": "Xét về mặt kinh tế, đây là một quyết định tốt."}],
    "hsk6_0117": [{"chinese": "请用叉子吃牛排。", "pinyin": "Qǐng yòng chāzi chī niúpái.", "meaningVi": "Xin dùng nĩa để ăn bít tết."}],
    "hsk6_0118": [{"chinese": "两国文化存在很大差异。", "pinyin": "Liǎng guó wénhuà cúnzài hěn dà chāyì.", "meaningVi": "Văn hóa của hai nước có sự khác biệt rất lớn."}],
    "hsk6_0119": [{"chinese": "请把插头插进插座。", "pinyin": "Qǐng bǎ chātóu chā jìn chāzuò.", "meaningVi": "Xin cắm phích cắm vào ổ điện."}],
    "hsk6_0120": [{"chinese": "您可以在网上查询订单状态。", "pinyin": "Nín kěyǐ zài wǎngshàng cháxún dìngdān zhuàngtài.", "meaningVi": "Bạn có thể tra cứu trạng thái đơn hàng trên mạng."}],
    "hsk6_0121": [{"chinese": "这栋旧楼即将被拆除。", "pinyin": "Zhè dòng jiù lóu jíjiāng bèi chāichú.", "meaningVi": "Tòa nhà cũ này sắp bị phá dỡ."}],
    "hsk6_0122": [{"chinese": "这台机器产出效率很高。", "pinyin": "Zhè tái jīqì chǎnchū xiàolǜ hěn gāo.", "meaningVi": "Hiệu suất sản xuất của cái máy này rất cao."}],
    "hsk6_0123": [{"chinese": "这种茶叶的产地是福建。", "pinyin": "Zhè zhǒng cháyè de chǎndì shì Fújiàn.", "meaningVi": "Nơi sản xuất loại trà này là Phúc Kiến."}],
    "hsk6_0124": [{"chinese": "他肠胃不太好。", "pinyin": "Tā chángwèi bú tài hǎo.", "meaningVi": "Đường ruột của anh ấy không tốt lắm."}],
    "hsk6_0125": [{"chinese": "请裁剪合适的长短。", "pinyin": "Qǐng cáijiǎn héshì de chángduǎn.", "meaningVi": "Xin cắt độ dài phù hợp."}],
    "hsk6_0126": [{"chinese": "这是常规检查。", "pinyin": "Zhè shì chángguī jiǎnchá.", "meaningVi": "Đây là kiểm tra định kỳ."}],
    "hsk6_0127": [{"chinese": "他常年在外地工作。", "pinyin": "Tā chángnián zài wàidì gōngzuò.", "meaningVi": "Anh ấy quanh năm làm việc ở nơi khác."}],
    "hsk6_0128": [{"chinese": "老人希望健康长寿。", "pinyin": "Lǎorén xīwàng jiànkāng chángshòu.", "meaningVi": "Người già mong muốn khỏe mạnh trường thọ."}],
    "hsk6_0129": [{"chinese": "这瓶饮料要常温保存。", "pinyin": "Zhè píng yǐnliào yào chángwēn bǎocún.", "meaningVi": "Chai đồ uống này cần bảo quản ở nhiệt độ thường."}],
    "hsk6_0130": [{"chinese": "今天的电影场次已经排满了。", "pinyin": "Jīntiān de diànyǐng chǎngcì yǐjīng páimǎn le.", "meaningVi": "Các suất chiếu phim hôm nay đã kín chỗ."}],
    "hsk6_0131": [{"chinese": "比赛场地已经准备好了。", "pinyin": "Bǐsài chǎngdì yǐjīng zhǔnbèi hǎo le.", "meaningVi": "Địa điểm thi đấu đã chuẩn bị xong."}],
    "hsk6_0132": [{"chinese": "这座体育场馆能容纳五万人。", "pinyin": "Zhè zuò tǐyù chǎngguǎn néng róngnà wǔ wàn rén.", "meaningVi": "Nhà thi đấu này có thể chứa năm mươi nghìn người."}],
    "hsk6_0133": [{"chinese": "在正式场合要穿正装。", "pinyin": "Zài zhèngshì chǎnghé yào chuān zhèngzhuāng.", "meaningVi": "Trong dịp trang trọng phải mặc trang phục chính thức."}],
    "hsk6_0134": [{"chinese": "请联系厂家维修。", "pinyin": "Qǐng liánxì chǎngjiā wéixiū.", "meaningVi": "Xin liên hệ nhà sản xuất để sửa chữa."}],
    "hsk6_0135": [{"chinese": "这个场景令人难忘。", "pinyin": "Zhège chǎngjǐng lìng rén nánwàng.", "meaningVi": "Cảnh tượng này khiến người ta khó quên."}],
    "hsk6_0136": [{"chinese": "婚礼现场场面很热闹。", "pinyin": "Hūnlǐ xiànchǎng chǎngmiàn hěn rènao.", "meaningVi": "Không khí tại đám cưới rất náo nhiệt."}],
    "hsk6_0137": [{"chinese": "我们和多家厂商合作。", "pinyin": "Wǒmen hé duō jiā chǎngshāng hézuò.", "meaningVi": "Chúng tôi hợp tác với nhiều nhà sản xuất."}],
    "hsk6_0138": [{"chinese": "请保持道路畅通。", "pinyin": "Qǐng bǎochí dàolù chàngtōng.", "meaningVi": "Xin giữ cho con đường thông suốt."}],
    "hsk6_0139": [{"chinese": "这本书是畅销书。", "pinyin": "Zhè běn shū shì chàngxiāo shū.", "meaningVi": "Cuốn sách này là sách bán chạy."}],
    "hsk6_0140": [{"chinese": "他抄了同学的作业。", "pinyin": "Tā chāole tóngxué de zuòyè.", "meaningVi": "Anh ấy đã chép bài tập của bạn học."}],
    "hsk6_0141": [{"chinese": "他超越了自己的极限。", "pinyin": "Tā chāoyuèle zìjǐ de jíxiàn.", "meaningVi": "Anh ấy đã vượt qua giới hạn của bản thân."}],
    "hsk6_0142": [{"chinese": "唐朝是一个繁荣的朝代。", "pinyin": "Tángcháo shì yí gè fánróng de cháodài.", "meaningVi": "Nhà Đường là một triều đại phồn vinh."}],
    "hsk6_0143": [{"chinese": "这种穿衣风格很符合潮流。", "pinyin": "Zhè zhǒng chuānyī fēnggé hěn fúhé cháoliú.", "meaningVi": "Kiểu ăn mặc này rất hợp xu hướng."}],
    "hsk6_0144": [{"chinese": "南方的气候比较潮湿。", "pinyin": "Nánfāng de qìhòu bǐjiào cháoshī.", "meaningVi": "Khí hậu miền Nam khá ẩm ướt."}],
    "hsk6_0145": [{"chinese": "请不要嘲笑别人的缺点。", "pinyin": "Qǐng búyào cháoxiào biéren de quēdiǎn.", "meaningVi": "Xin đừng chế giễu khuyết điểm của người khác."}],
    "hsk6_0146": [{"chinese": "他最近迷上了炒股。", "pinyin": "Tā zuìjìn míshàngle chǎogǔ.", "meaningVi": "Gần đây anh ấy mê chơi cổ phiếu."}],
    "hsk6_0147": [{"chinese": "他们俩又吵架了。", "pinyin": "Tāmen liǎ yòu chǎojià le.", "meaningVi": "Hai người họ lại cãi nhau rồi."}],
    "hsk6_0148": [{"chinese": "他撤回了自己的意见。", "pinyin": "Tā chèhuíle zìjǐ de yìjiàn.", "meaningVi": "Anh ấy đã rút lại ý kiến của mình."}],
    "hsk6_0149": [{"chinese": "这项决定已被撤销。", "pinyin": "Zhè xiàng juédìng yǐ bèi chèxiāo.", "meaningVi": "Quyết định này đã bị hủy bỏ."}],
    "hsk6_0150": [{"chinese": "他心情沉重。", "pinyin": "Tā xīnqíng chénzhòng.", "meaningVi": "Tâm trạng của anh ấy nặng nề."}],
    "hsk6_0151": [{"chinese": "趁天还没黑，我们赶紧走吧。", "pinyin": "Chèn tiān hái méi hēi, wǒmen gǎnjǐn zǒu ba.", "meaningVi": "Nhân lúc trời chưa tối, chúng ta mau đi thôi."}],
    "hsk6_0152": [{"chinese": "他用手撑着桌子。", "pinyin": "Tā yòng shǒu chēngzhe zhuōzi.", "meaningVi": "Anh ấy dùng tay chống lên bàn."}],
    "hsk6_0153": [{"chinese": "他获得了优秀员工的称号。", "pinyin": "Tā huòdéle yōuxiù yuángōng de chēnghào.", "meaningVi": "Anh ấy đã nhận được danh hiệu nhân viên xuất sắc."}],
    "hsk6_0154": [{"chinese": "我该怎么称呼您？", "pinyin": "Wǒ gāi zěnme chēnghu nín?", "meaningVi": "Tôi nên xưng hô với ngài như thế nào?"}],
    "hsk6_0155": [{"chinese": "人们把这种鸟称作益鸟。", "pinyin": "Rénmen bǎ zhè zhǒng niǎo chēngzuò yìniǎo.", "meaningVi": "Người ta gọi loại chim này là chim có ích."}],
    "hsk6_0156": [{"chinese": "他终于学有所成。", "pinyin": "Tā zhōngyú xué yǒu suǒ chéng.", "meaningVi": "Cuối cùng anh ấy đã học có thành tựu."}],
    "hsk6_0157": [],
    "hsk6_0158": [{"chinese": "请帮我盛一碗饭。", "pinyin": "Qǐng bāng wǒ chéng yì wǎn fàn.", "meaningVi": "Xin giúp tôi múc một bát cơm."}],
    "hsk6_0159": [{"chinese": "这座城市承办了这次运动会。", "pinyin": "Zhè zuò chéngshì chéngbànle zhè cì yùndònghuì.", "meaningVi": "Thành phố này đã đăng cai đại hội thể thao lần này."}],
    "hsk6_0160": [{"chinese": "犯错就要接受惩罚。", "pinyin": "Fàncuò jiù yào jiēshòu chéngfá.", "meaningVi": "Phạm lỗi thì phải chịu sự trừng phạt."}],
    "hsk6_0161": [{"chinese": "这笔生意终于成交了。", "pinyin": "Zhè bǐ shēngyì zhōngyú chéngjiāo le.", "meaningVi": "Phi vụ làm ăn này cuối cùng đã thành công."}],
    "hsk6_0162": [{"chinese": "他承诺会准时到达。", "pinyin": "Tā chéngnuò huì zhǔnshí dàodá.", "meaningVi": "Anh ấy cam kết sẽ đến đúng giờ."}],
    "hsk6_0163": [{"chinese": "成千上万的人参加了这次游行。", "pinyin": "Chéngqiān-shàngwàn de rén cānjiāle zhè cì yóuxíng.", "meaningVi": "Hàng nghìn hàng vạn người đã tham gia cuộc diễu hành lần này."}],
    "hsk6_0164": [{"chinese": "数据呈现出上升趋势。", "pinyin": "Shùjù chéngxiàn chū shàngshēng qūshì.", "meaningVi": "Số liệu thể hiện xu hướng tăng lên."}],
    "hsk6_0165": [{"chinese": "这项改革已经取得了明显成效。", "pinyin": "Zhè xiàng gǎigé yǐjīng qǔdéle míngxiǎn chéngxiào.", "meaningVi": "Cuộc cải cách này đã đạt được hiệu quả rõ rệt."}],
    "hsk6_0166": [{"chinese": "做生意要讲诚信。", "pinyin": "Zuò shēngyì yào jiǎng chéngxìn.", "meaningVi": "Làm ăn kinh doanh phải giữ chữ tín."}],
    "hsk6_0167": [{"chinese": "他能说出很多成语。", "pinyin": "Tā néng shuōchū hěn duō chéngyǔ.", "meaningVi": "Anh ấy có thể nói ra rất nhiều thành ngữ."}],
    "hsk6_0168": [{"chinese": "越来越多的农民搬到城镇生活。", "pinyin": "Yuèláiyuè duō de nóngmín bāndào chéngzhèn shēnghuó.", "meaningVi": "Ngày càng nhiều nông dân chuyển đến thị trấn sinh sống."}],
    "hsk6_0169": [{"chinese": "这种香水味道很持久。", "pinyin": "Zhè zhǒng xiāngshuǐ wèidào hěn chíjiǔ.", "meaningVi": "Mùi hương của loại nước hoa này rất bền lâu."}],
    "hsk6_0170": [{"chinese": "他持有该公司百分之十的股份。", "pinyin": "Tā chíyǒu gāi gōngsī bǎifēnzhī shí de gǔfèn.", "meaningVi": "Anh ấy nắm giữ mười phần trăm cổ phần của công ty này."}],
    "hsk6_0171": [{"chinese": "一尺大约是三十三厘米。", "pinyin": "Yì chǐ dàyuē shì sānshísān límǐ.", "meaningVi": "Một thước xấp xỉ ba mươi ba centimet."}],
    "hsk6_0172": [{"chinese": "请告诉我你的尺寸。", "pinyin": "Qǐng gàosu wǒ nǐ de chǐcùn.", "meaningVi": "Xin cho tôi biết kích cỡ của bạn."}],
    "hsk6_0173": [{"chinese": "别冲动，先冷静想想。", "pinyin": "Bié chōngdòng, xiān lěngjìng xiǎngxiang.", "meaningVi": "Đừng bốc đồng, hãy bình tĩnh suy nghĩ trước đã."}],
    "hsk6_0174": [{"chinese": "这次事件对市场造成了冲击。", "pinyin": "Zhè cì shìjiàn duì shìchǎng zàochéngle chōngjī.", "meaningVi": "Sự kiện này đã gây ra tác động đối với thị trường."}],
    "hsk6_0175": [{"chinese": "他的生活过得很充实。", "pinyin": "Tā de shēnghuó guò de hěn chōngshí.", "meaningVi": "Cuộc sống của anh ấy rất đầy đủ, phong phú."}],
    "hsk6_0176": [{"chinese": "双方发生了冲突。", "pinyin": "Shuāngfāng fāshēngle chōngtū.", "meaningVi": "Hai bên đã xảy ra xung đột."}],
    "hsk6_0177": [{"chinese": "很多孩子崇拜自己的父母。", "pinyin": "Hěn duō háizi chóngbài zìjǐ de fùmǔ.", "meaningVi": "Rất nhiều đứa trẻ tôn thờ cha mẹ của mình."}],
    "hsk6_0178": [{"chinese": "地震后，政府帮助居民重建家园。", "pinyin": "Dìzhèn hòu, zhèngfǔ bāngzhù jūmín chóngjiàn jiāyuán.", "meaningVi": "Sau động đất, chính phủ giúp cư dân xây dựng lại nhà cửa."}],
    "hsk6_0180": [{"chinese": "今天商场有抽奖活动。", "pinyin": "Jīntiān shāngchǎng yǒu chōujiǎng huódòng.", "meaningVi": "Hôm nay trung tâm thương mại có hoạt động bốc thăm trúng thưởng."}],
    "hsk6_0181": [{"chinese": "这幅画风格很抽象。", "pinyin": "Zhè fú huà fēnggé hěn chōuxiàng.", "meaningVi": "Phong cách của bức tranh này rất trừu tượng."}],
    "hsk6_0182": [{"chinese": "别发愁，办法总会有的。", "pinyin": "Bié fāchóu, bànfǎ zǒng huì yǒu de.", "meaningVi": "Đừng lo lắng, thế nào cũng sẽ có cách."}],
    "hsk6_0183": [{"chinese": "婚礼正在紧张筹备中。", "pinyin": "Hūnlǐ zhèngzài jǐnzhāng chóubèi zhōng.", "meaningVi": "Đám cưới đang được chuẩn bị khẩn trương."}],
    "hsk6_0184": [{"chinese": "我们已经取得了初步成果。", "pinyin": "Wǒmen yǐjīng qǔdéle chūbù chéngguǒ.", "meaningVi": "Chúng tôi đã đạt được thành quả bước đầu."}],
    "hsk6_0185": [{"chinese": "主角终于出场了。", "pinyin": "Zhǔjué zhōngyú chūchǎng le.", "meaningVi": "Nhân vật chính cuối cùng cũng xuất hiện trên sân khấu."}],
    "hsk6_0186": [{"chinese": "这是初等数学的内容。", "pinyin": "Zhè shì chūděng shùxué de nèiróng.", "meaningVi": "Đây là nội dung toán học sơ cấp."}],
    "hsk6_0187": [{"chinese": "请出示护照办理出境手续。", "pinyin": "Qǐng chūshì hùzhào bànlǐ chūjìng shǒuxù.", "meaningVi": "Xin xuất trình hộ chiếu để làm thủ tục xuất cảnh."}],
    "hsk6_0188": [{"chinese": "大家都在为这次活动出力。", "pinyin": "Dàjiā dōu zài wèi zhè cì huódòng chūlì.", "meaningVi": "Mọi người đều đang góp sức cho hoạt động lần này."}],
    "hsk6_0189": [{"chinese": "他因为这部电影出名了。", "pinyin": "Tā yīnwèi zhè bù diànyǐng chūmíng le.", "meaningVi": "Anh ấy nổi tiếng nhờ bộ phim này."}],
    "hsk6_0190": [{"chinese": "这两份数据出入很大。", "pinyin": "Zhè liǎng fèn shùjù chūrù hěn dà.", "meaningVi": "Hai bộ số liệu này có sự chênh lệch rất lớn."}],
    "hsk6_0191": [{"chinese": "他向警察出示了驾照。", "pinyin": "Tā xiàng jǐngchá chūshìle jiàzhào.", "meaningVi": "Anh ấy đã xuất trình bằng lái xe cho cảnh sát."}],
    "hsk6_0192": [{"chinese": "五一假期很多人选择出游。", "pinyin": "Wǔyī jiàqī hěn duō rén xuǎnzé chūyóu.", "meaningVi": "Vào kỳ nghỉ mùng một tháng năm rất nhiều người chọn đi du lịch."}],
    "hsk6_0193": [{"chinese": "他这么做是出于好意。", "pinyin": "Tā zhème zuò shì chūyú hǎoyì.", "meaningVi": "Anh ấy làm như vậy là xuất phát từ thiện ý."}],
    "hsk6_0194": [{"chinese": "请把这个选项除去。", "pinyin": "Qǐng bǎ zhège xuǎnxiàng chúqù.", "meaningVi": "Xin loại bỏ lựa chọn này đi."}],
    "hsk6_0195": [{"chinese": "除非下雨，否则比赛照常进行。", "pinyin": "Chúfēi xiàyǔ, fǒuzé bǐsài zhàocháng jìnxíng.", "meaningVi": "Trừ khi trời mưa, nếu không trận đấu vẫn diễn ra như thường."}],
    "hsk6_0196": [{"chinese": "这些食物需要冷藏储存。", "pinyin": "Zhèxiē shíwù xūyào lěngcáng chǔcún.", "meaningVi": "Những thực phẩm này cần được bảo quản lạnh."}],
    "hsk6_0197": [{"chinese": "违反规定会受到处罚。", "pinyin": "Wéifǎn guīdìng huì shòudào chǔfá.", "meaningVi": "Vi phạm quy định sẽ bị xử phạt."}],
    "hsk6_0198": [{"chinese": "他每个月都有储蓄的习惯。", "pinyin": "Tā měi gè yuè dōu yǒu chǔxù de xíguàn.", "meaningVi": "Mỗi tháng anh ấy đều có thói quen tiết kiệm."}],
    "hsk6_0199": [{"chinese": "他处处为别人着想。", "pinyin": "Tā chùchù wèi biéren zhuóxiǎng.", "meaningVi": "Anh ấy luôn nghĩ cho người khác ở mọi nơi."}],
    "hsk6_0200": [{"chinese": "我们穿过一条小巷。", "pinyin": "Wǒmen chuānguò yì tiáo xiǎo xiàng.", "meaningVi": "Chúng tôi đi xuyên qua một con ngõ nhỏ."}],
    "hsk6_0201": [{"chinese": "这项技艺已经传承了几代人。", "pinyin": "Zhè xiàng jìyì yǐjīng chuánchéngle jǐ dài rén.", "meaningVi": "Kỹ nghệ này đã được truyền thừa qua mấy thế hệ."}],
    "hsk6_0202": [{"chinese": "请把这个消息传达给大家。", "pinyin": "Qǐng bǎ zhège xiāoxi chuándá gěi dàjiā.", "meaningVi": "Xin truyền đạt tin này cho mọi người."}],
    "hsk6_0203": [{"chinese": "感冒很容易传染。", "pinyin": "Gǎnmào hěn róngyì chuánrǎn.", "meaningVi": "Cảm cúm rất dễ lây."}],
    "hsk6_0204": [{"chinese": "学校采取措施预防传染病。", "pinyin": "Xuéxiào cǎiqǔ cuòshī yùfáng chuánrǎnbìng.", "meaningVi": "Nhà trường áp dụng biện pháp phòng ngừa bệnh truyền nhiễm."}],
    "hsk6_0205": [{"chinese": "老师傅向徒弟传授技术。", "pinyin": "Lǎo shīfu xiàng túdì chuánshòu jìshù.", "meaningVi": "Người thợ cả truyền dạy kỹ thuật cho học trò."}],
    "hsk6_0206": [{"chinese": "数据传输速度很快。", "pinyin": "Shùjù chuánshū sùdù hěn kuài.", "meaningVi": "Tốc độ truyền dữ liệu rất nhanh."}],
    "hsk6_0207": [{"chinese": "请把文件用传真发过来。", "pinyin": "Qǐng bǎ wénjiàn yòng chuánzhēn fā guòlái.", "meaningVi": "Xin gửi tài liệu bằng fax qua đây."}],
    "hsk6_0208": [{"chinese": "港口停靠着很多船只。", "pinyin": "Gǎngkǒu tíngkàozhe hěn duō chuánzhī.", "meaningVi": "Ở cảng đang đậu rất nhiều tàu thuyền."}],
    "hsk6_0209": [{"chinese": "她戴着一串项链。", "pinyin": "Tā dàizhe yí chuàn xiàngliàn.", "meaningVi": "Cô ấy đeo một chuỗi dây chuyền."}],
    "hsk6_0210": [{"chinese": "请到三号窗口办理业务。", "pinyin": "Qǐng dào sān hào chuāngkǒu bànlǐ yèwù.", "meaningVi": "Xin đến quầy số ba để làm thủ tục."}],
    "hsk6_0211": [{"chinese": "他一个人出去闯荡。", "pinyin": "Tā yí gè rén chūqù chuǎngdàng.", "meaningVi": "Anh ấy một mình ra ngoài lập nghiệp."}],
    "hsk6_0212": [{"chinese": "他创办了这家公司。", "pinyin": "Tā chuàngbànle zhè jiā gōngsī.", "meaningVi": "Anh ấy đã sáng lập công ty này."}],
    "hsk6_0213": [{"chinese": "他们共同创建了这个组织。", "pinyin": "Tāmen gòngtóng chuàngjiànle zhège zǔzhī.", "meaningVi": "Họ đã cùng nhau sáng lập tổ chức này."}],
    "hsk6_0214": [{"chinese": "这家公司是他创立的。", "pinyin": "Zhè jiā gōngsī shì tā chuànglì de.", "meaningVi": "Công ty này là do anh ấy sáng lập."}],
    "hsk6_0215": [{"chinese": "这个广告很有创意。", "pinyin": "Zhège guǎnggào hěn yǒu chuàngyì.", "meaningVi": "Quảng cáo này rất sáng tạo."}],
    "hsk6_0216": [{"chinese": "这两条线互相垂直。", "pinyin": "Zhè liǎng tiáo xiàn hùxiāng chuízhí.", "meaningVi": "Hai đường thẳng này vuông góc với nhau."}],
    "hsk6_0217": [{"chinese": "这是纯棉的衣服。", "pinyin": "Zhè shì chún mián de yīfu.", "meaningVi": "Đây là quần áo cotton nguyên chất."}],
    "hsk6_0218": [{"chinese": "中国瓷器历史悠久。", "pinyin": "Zhōngguó cíqì lìshǐ yōujiǔ.", "meaningVi": "Đồ sứ Trung Quốc có lịch sử lâu đời."}],
    "hsk6_0219": [{"chinese": "此刻他正在赶往机场。", "pinyin": "Cǐkè tā zhèngzài gǎnwǎng jīchǎng.", "meaningVi": "Lúc này anh ấy đang trên đường đến sân bay."}],
    "hsk6_0220": [{"chinese": "玫瑰花有刺。", "pinyin": "Méigui huā yǒu cì.", "meaningVi": "Hoa hồng có gai."}],
    "hsk6_0221": [{"chinese": "他参加比赛的次数不多。", "pinyin": "Tā cānjiā bǐsài de cìshù bù duō.", "meaningVi": "Số lần anh ấy tham gia thi đấu không nhiều."}],
    "hsk6_0222": [{"chinese": "他匆匆离开了。", "pinyin": "Tā cōngcōng líkāi le.", "meaningVi": "Anh ấy vội vàng rời đi."}],
    "hsk6_0223": [{"chinese": "他匆忙收拾行李出门了。", "pinyin": "Tā cōngmáng shōushi xíngli chūmén le.", "meaningVi": "Anh ấy vội vàng thu dọn hành lý ra ngoài."}],
    "hsk6_0224": [{"chinese": "他从未去过国外。", "pinyin": "Tā cóngwèi qùguo guówài.", "meaningVi": "Anh ấy chưa từng ra nước ngoài."}],
    "hsk6_0225": [{"chinese": "他有十年的从业经验。", "pinyin": "Tā yǒu shí nián de cóngyè jīngyàn.", "meaningVi": "Anh ấy có mười năm kinh nghiệm làm nghề."}],
    "hsk6_0226": [{"chinese": "这道菜要加点醋。", "pinyin": "Zhè dào cài yào jiā diǎn cù.", "meaningVi": "Món ăn này cần cho thêm chút giấm."}],
    "hsk6_0227": [{"chinese": "这个饼干很脆。", "pinyin": "Zhège bǐnggān hěn cuì.", "meaningVi": "Cái bánh quy này rất giòn."}],
    "hsk6_0228": [{"chinese": "她的心理其实很脆弱。", "pinyin": "Tā de xīnlǐ qíshí hěn cuìruò.", "meaningVi": "Tâm lý của cô ấy thực ra rất mong manh."}],
    "hsk6_0229": [{"chinese": "这是一个安静的村庄。", "pinyin": "Zhè shì yí gè ānjìng de cūnzhuāng.", "meaningVi": "Đây là một ngôi làng yên tĩnh."}],
    "hsk6_0230": [{"chinese": "这个设备可以存储大量数据。", "pinyin": "Zhège shèbèi kěyǐ cúnchǔ dàliàng shùjù.", "meaningVi": "Thiết bị này có thể lưu trữ lượng lớn dữ liệu."}],
    "hsk6_0231": [{"chinese": "一寸光阴一寸金。", "pinyin": "Yí cùn guāngyīn yí cùn jīn.", "meaningVi": "Một tấc thời gian một tấc vàng."}],
    "hsk6_0232": [{"chinese": "人生难免会遇到挫折。", "pinyin": "Rénshēng nánmiǎn huì yùdào cuòzhé.", "meaningVi": "Đời người khó tránh khỏi gặp phải thất bại."}],
    "hsk6_0233": [{"chinese": "他帮我搭了个帐篷。", "pinyin": "Tā bāng wǒ dāle gè zhàngpeng.", "meaningVi": "Anh ấy đã giúp tôi dựng một cái lều."}],
    "hsk6_0234": [{"chinese": "这件衣服和裤子很搭配。", "pinyin": "Zhè jiàn yīfu hé kùzi hěn dāpèi.", "meaningVi": "Chiếc áo này và quần rất hợp nhau."}],
    "hsk6_0235": [{"chinese": "请尽快给我答复。", "pinyin": "Qǐng jǐnkuài gěi wǒ dáfù.", "meaningVi": "Xin trả lời tôi sớm nhất có thể."}],
    "hsk6_0236": [{"chinese": "他经常和外国人打交道。", "pinyin": "Tā jīngcháng hé wàiguó rén dǎ jiāodao.", "meaningVi": "Anh ấy thường xuyên giao tiếp với người nước ngoài."}],
    "hsk6_0237": [{"chinese": "她的演讲打动了在场所有人。", "pinyin": "Tā de yǎnjiǎng dǎdòngle zàichǎng suǒyǒu rén.", "meaningVi": "Bài diễn thuyết của cô ấy đã làm rung động tất cả mọi người có mặt."}],
    "hsk6_0238": [{"chinese": "这次失败对他打击很大。", "pinyin": "Zhè cì shībài duì tā dǎjī hěn dà.", "meaningVi": "Thất bại lần này đã gây đả kích lớn cho anh ấy."}],
    "hsk6_0239": [{"chinese": "两个孩子因为玩具打架了。", "pinyin": "Liǎng gè háizi yīnwèi wánjù dǎjià le.", "meaningVi": "Hai đứa trẻ đánh nhau vì đồ chơi."}],
    "hsk6_0240": [{"chinese": "请上班时记得打卡。", "pinyin": "Qǐng shàngbān shí jìde dǎkǎ.", "meaningVi": "Xin nhớ chấm công khi đi làm."}],
    "hsk6_0241": [{"chinese": "外面打雷了。", "pinyin": "Wàimiàn dǎléi le.", "meaningVi": "Bên ngoài có sấm rồi."}],
    "hsk6_0242": [{"chinese": "公司致力于打造知名品牌。", "pinyin": "Gōngsī zhìlì yú dǎzào zhīmíng pǐnpái.", "meaningVi": "Công ty nỗ lực xây dựng thương hiệu nổi tiếng."}],
    "hsk6_0243": [{"chinese": "古时候两国经常打仗。", "pinyin": "Gǔ shíhou liǎng guó jīngcháng dǎzhàng.", "meaningVi": "Thời xưa hai nước thường xuyên đánh nhau."}],
    "hsk6_0244": [{"chinese": "皇帝召见了大臣。", "pinyin": "Huángdì zhàojiànle dàchén.", "meaningVi": "Hoàng đế đã triệu kiến đại thần."}],
    "hsk6_0245": [{"chinese": "听到这个消息，他大吃一惊。", "pinyin": "Tīngdào zhège xiāoxi, tā dàchī-yìjīng.", "meaningVi": "Nghe được tin này, anh ấy vô cùng kinh ngạc."}],
    "hsk6_0246": [{"chinese": "春天大地一片绿色。", "pinyin": "Chūntiān dàdì yí piàn lǜsè.", "meaningVi": "Mùa xuân đại địa một màu xanh."}],
    "hsk6_0247": [{"chinese": "参加聚会的大都是老同学。", "pinyin": "Cānjiā jùhuì de dàdū shì lǎo tóngxué.", "meaningVi": "Phần lớn người tham gia buổi họp mặt là bạn học cũ."}],
    "hsk6_0248": [{"chinese": "她待人很大方。", "pinyin": "Tā dàirén hěn dàfang.", "meaningVi": "Cô ấy đối xử với người khác rất hào phóng."}],
    "hsk6_0249": [{"chinese": "今年销量大幅增长。", "pinyin": "Jīnnián xiāoliàng dàfú zēngzhǎng.", "meaningVi": "Doanh số năm nay tăng trưởng đáng kể."}],
    "hsk6_0250": [{"chinese": "大伙儿都同意这个方案。", "pinyin": "Dàhuǒr dōu tóngyì zhège fāng'àn.", "meaningVi": "Mọi người đều đồng ý với phương án này."}],
    "hsk6_0251": [{"chinese": "他被任命为驻华大使。", "pinyin": "Tā bèi rènmìng wéi zhù Huá dàshǐ.", "meaningVi": "Anh ấy được bổ nhiệm làm đại sứ tại Trung Quốc."}],
    "hsk6_0252": [{"chinese": "他是这个领域公认的大师。", "pinyin": "Tā shì zhège lǐngyù gōngrèn de dàshī.", "meaningVi": "Anh ấy là bậc thầy được công nhận trong lĩnh vực này."}],
    "hsk6_0253": [{"chinese": "澳大利亚属于大洋洲。", "pinyin": "Àodàlìyà shǔyú Dàyángzhōu.", "meaningVi": "Úc thuộc châu Đại Dương."}],
    "hsk6_0254": [{"chinese": "我大致了解了情况。", "pinyin": "Wǒ dàzhì liǎojiěle qíngkuàng.", "meaningVi": "Tôi đã hiểu sơ bộ về tình hình."}],
    "hsk6_0255": [{"chinese": "他呆呆地站在那里。", "pinyin": "Tā dāidāi de zhàn zài nàlǐ.", "meaningVi": "Anh ấy đứng ngẩn ngơ ở đó."}],
    "hsk6_0257": [{"chinese": "他为此付出了巨大的代价。", "pinyin": "Tā wèi cǐ fùchūle jùdà de dàijià.", "meaningVi": "Anh ấy đã trả giá đắt vì điều này."}],
    "hsk6_0258": [{"chinese": "他向银行申请了贷款。", "pinyin": "Tā xiàng yínháng shēnqǐngle dàikuǎn.", "meaningVi": "Anh ấy đã xin vay vốn ngân hàng."}],
    "hsk6_0259": [{"chinese": "他是这个品牌的代理商。", "pinyin": "Tā shì zhège páizi de dàilǐshāng.", "meaningVi": "Anh ấy là đại lý của thương hiệu này."}],
    "hsk6_0260": [{"chinese": "教练带领球队获得了冠军。", "pinyin": "Jiàoliàn dàilǐng qiúduì huòdéle guànjūn.", "meaningVi": "Huấn luyện viên đã dẫn dắt đội bóng giành chức vô địch."}],
    "hsk6_0261": [{"chinese": "他的想法很单纯。", "pinyin": "Tā de xiǎngfǎ hěn dānchún.", "meaningVi": "Suy nghĩ của anh ấy rất đơn thuần."}],
    "hsk6_0262": [{"chinese": "这份工作有点单调。", "pinyin": "Zhè fèn gōngzuò yǒudiǎn dāndiào.", "meaningVi": "Công việc này hơi đơn điệu."}],
    "hsk6_0263": [{"chinese": "别耽误大家的时间。", "pinyin": "Bié dānwu dàjiā de shíjiān.", "meaningVi": "Đừng làm mất thời gian của mọi người."}],
    "hsk6_0264": [{"chinese": "家长很担忧孩子的安全。", "pinyin": "Jiāzhǎng hěn dānyōu háizi de ānquán.", "meaningVi": "Phụ huynh rất lo lắng về sự an toàn của con cái."}],
    "hsk6_0265": [{"chinese": "鸡蛋含有丰富的蛋白质。", "pinyin": "Jīdàn hányǒu fēngfù de dànbáizhì.", "meaningVi": "Trứng gà chứa nhiều protein."}],
    "hsk6_0266": [{"chinese": "一个新的生命诞生了。", "pinyin": "Yí gè xīn de shēngmìng dànshēng le.", "meaningVi": "Một sinh mệnh mới đã ra đời."}],
    "hsk6_0267": [{"chinese": "他当场就答应了。", "pinyin": "Tā dāngchǎng jiù dāyìng le.", "meaningVi": "Anh ấy đã đồng ý ngay tại chỗ."}],
    "hsk6_0268": [{"chinese": "当初我们都不看好这个项目。", "pinyin": "Dāngchū wǒmen dōu bú kànhǎo zhège xiàngmù.", "meaningVi": "Ban đầu chúng tôi đều không đánh giá cao dự án này."}],
    "hsk6_0269": [{"chinese": "他是当代著名的画家。", "pinyin": "Tā shì dāngdài zhùmíng de huàjiā.", "meaningVi": "Anh ấy là họa sĩ nổi tiếng đương đại."}],
    "hsk6_0270": [{"chinese": "当今社会科技发展迅速。", "pinyin": "Dāngjīn shèhuì kējì fāzhǎn xùnsù.", "meaningVi": "Xã hội ngày nay khoa học kỹ thuật phát triển nhanh chóng."}],
    "hsk6_0271": [{"chinese": "有话请当面说清楚。", "pinyin": "Yǒu huà qǐng dāngmiàn shuō qīngchu.", "meaningVi": "Có gì muốn nói xin nói rõ trực tiếp."}],
    "hsk6_0272": [{"chinese": "我们要珍惜当下。", "pinyin": "Wǒmen yào zhēnxī dāngxià.", "meaningVi": "Chúng ta phải trân trọng hiện tại."}],
    "hsk6_0273": [{"chinese": "他顺利当选为班长。", "pinyin": "Tā shùnlì dāngxuǎn wéi bānzhǎng.", "meaningVi": "Anh ấy đã được bầu làm lớp trưởng một cách thuận lợi."}],
    "hsk6_0274": [{"chinese": "请把这份文件归入档案。", "pinyin": "Qǐng bǎ zhè fèn wénjiàn guīrù dàng'àn.", "meaningVi": "Xin đưa tài liệu này vào hồ sơ lưu trữ."}],
    "hsk6_0275": [{"chinese": "货物当天就能送到。", "pinyin": "Huòwù dàngtiān jiù néng sòngdào.", "meaningVi": "Hàng hóa có thể giao đến ngay trong ngày."}],
    "hsk6_0276": [{"chinese": "这附近有一座小岛。", "pinyin": "Zhè fùjìn yǒu yí zuò xiǎo dǎo.", "meaningVi": "Gần đây có một hòn đảo nhỏ."}],
    "hsk6_0277": [{"chinese": "这家公司去年倒闭了。", "pinyin": "Zhè jiā gōngsī qùnián dǎobì le.", "meaningVi": "Công ty này đã phá sản vào năm ngoái."}],
    "hsk6_0278": [{"chinese": "请在下一站倒车。", "pinyin": "Qǐng zài xià yí zhàn dǎochē.", "meaningVi": "Xin chuyển tàu ở trạm tiếp theo."}],
    "hsk6_0279": [{"chinese": "他是我的大学导师。", "pinyin": "Tā shì wǒ de dàxué dǎoshī.", "meaningVi": "Anh ấy là người hướng dẫn đại học của tôi."}],
    "hsk6_0280": [{"chinese": "我们要遵守社会道德。", "pinyin": "Wǒmen yào zūnshǒu shèhuì dàodé.", "meaningVi": "Chúng ta phải tuân thủ đạo đức xã hội."}],
    "hsk6_0281": [{"chinese": "这个办法倒是挺不错的。", "pinyin": "Zhège bànfǎ dàoshì tǐng búcuò de.", "meaningVi": "Cách này thì lại khá là hay đấy."}],
    "hsk6_0282": [{"chinese": "得了，别再说了。", "pinyin": "Déle, bié zài shuō le.", "meaningVi": "Thôi được rồi, đừng nói nữa."}],
    "hsk6_0283": [{"chinese": "多亏大家帮忙，问题得以解决。", "pinyin": "Duōkuī dàjiā bāngmáng, wèntí déyǐ jiějué.", "meaningVi": "May nhờ mọi người giúp đỡ, vấn đề mới được giải quyết."}],
    "hsk6_0284": [{"chinese": "我是昨天才得知这个消息的。", "pinyin": "Wǒ shì zuótiān cái dézhī zhège xiāoxi de.", "meaningVi": "Tôi đến hôm qua mới biết được tin này."}],
    "hsk6_0285": [{"chinese": "春节期间到处挂着红灯笼。", "pinyin": "Chūnjié qījiān dàochù guàzhe hóng dēnglong.", "meaningVi": "Trong dịp Tết khắp nơi treo đèn lồng đỏ."}],
    "hsk6_0286": [{"chinese": "这些产品分为不同等级。", "pinyin": "Zhèxiē chǎnpǐn fēnwéi bùtóng děngjí.", "meaningVi": "Những sản phẩm này được chia thành các cấp độ khác nhau."}],
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
