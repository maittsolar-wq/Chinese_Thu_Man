"""P5.10.3 (continued) -- Batch 031 (continues immediately after
examples_batch_030.json). Spans the remaining HSK4 tier-2 queue
(91 records, hsk4_432-hsk4_999, COMPLETING HSK4's tier-2 queue) plus
the start of HSK5's tier-2 queue (209 records, hsk5_005-hsk5_430).
HSK/tier for every record was read directly from load_universe()/
classify_risk_tiers output and cross-checked before drafting --
level distribution {4: 91, 5: 209}, all tier 2, confirmed exactly,
with a single clean transition at index 91 (hsk4_999 -> hsk5_005).

*** Non-sequential ID ordering within HSK5 (expected, not a bug) ***
Unlike prior batches, the HSK5 portion of this batch does NOT appear
in ascending numeric order: e.g. hsk5_099 is followed by hsk5_1008,
then hsk5_101, then hsk5_1014, etc. This is the established
deterministic (tier, id) PLAIN-STRING sort behavior (documented since
the pilot phase): "hsk5_1008" sorts before "hsk5_101" because string
comparison hits "100" vs "101" at the third character before length
matters. Every id was verified individually against load_universe()
before drafting; none of the "jumps" are missing or duplicated
records -- they are exactly what the deterministic sort produces.

*** Sparse per-level id gaps within this batch (expected) ***
Both the HSK4 and HSK5 portions of this batch have many non-
consecutive ids within their own level's numeric range (e.g. HSK4
jumps 432->435->438->445->446->462...). This is NOT a queue error:
it reflects that most ids in that numeric range were already
completed as TIER-1 records in earlier batches (002-021 for HSK4,
021-025 for HSK5) or belong to the special-review queue (tier 3/4);
only the tier-2 remainder shows up now. Confirmed via direct
comparison against get_completed_ids() and classify_risk_tiers().

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

No numeric-suffix homograph or other source-data anomalies were
found anywhere in this batch.

*** Homophone/polyphonic clusters requiring deliberate handling ***
  - shēn (1st tone): 身 (hsk4_641, "body") and 深 (hsk4_642, "deep")
    are DIFFERENT characters sharing the same pinyin+tone, adjacent
    in this batch -- kept to clearly distinct natural contexts.
  - zuò (4th tone): 座 (hsk4_991, "measure word for large solid
    objects"), 作为 (hsk4_996), 作文 (hsk4_998), and 作用 (hsk4_999)
    -- two different characters (座/作) across four records, all
    given distinct natural compounds.
  - tōng (1st tone): 通/通过/通知 (hsk4_743/744/745) -- same
    character 通 in three different compounds, kept distinct.
  - suǒ (3rd tone): 所 (hsk5_1098, measure word for institutions)
    and 锁 (hsk5_1099, "lock") -- DIFFERENT characters sharing the
    same pinyin+tone, adjacent in this batch -- kept distinct.
  - yǐ (3rd tone): 乙 (hsk5_1361, the second of the ten Heavenly
    Stems, used in 甲方/乙方 "Party A/Party B") and 以 (hsk5_1362,
    "by means of/according to") -- DIFFERENT characters sharing the
    same pinyin+tone, adjacent in this batch -- kept distinct.
  - gēn (1st tone): 根 (hsk5_403, "root") and 根本 (hsk5_404,
    "fundamentally") -- same character 根, given distinct contexts
    (literal "tree root" vs the abstract adverb sense).
  - zhí: 值 (hsk4_946, "to be worth", 2nd tone) vs 直 (hsk5_1501,
    "straight", 2nd tone) vs 执行 (hsk5_1505, zhíxíng, "to execute")
    -- three different characters/readings sharing the same
    pinyin+tone across the batch, each kept to a distinct natural
    context.

Fixes applied after the first validator pass (caught by
validate_examples_batch_p103.py's no_duplicate_sentences_across_
pilot_and_batches check): five exact duplicates --
  - 本 (běn): "我买了两本书。" -> "这套丛书一共十本。".
  - 白 (bái): "她的皮肤很白。" -> "他吓得脸色发白。".
  - 篇 (piān): "他写了一篇文章。" -> "这篇报道引起了广泛关注。".
  - 损失 (sǔnshī): "这次事故造成了很大的损失。" -> "公司这个季度
    损失惨重。".
  - 传说 (chuánshuō): "这是一个古老的传说。" -> "这个地方流传着一个
    美丽的传说。".
A second validator pass found one more exact duplicate --
  - 一路 (yílù): "祝你一路平安。" (a common idiom) -> "他们一路上
    说说笑笑，很快就到了。".

Near-template fixes (character-bigram Jaccard >= 0.55 against the
full pilot+002-030 corpus, caught by the independent script-level
check, not the validator): ten flags, all fixed by diverging sentence
structure while preserving natural, correct usage:
  - 同 vs hsk5_1299's "这两件事的性质不同。" -> "他俩的想法完全
    不同。".
  - 套 vs hsk3_123's "他们买了一套新房子。" -> "她带了一套换洗
    衣服。".
  - 座 vs hsk3_323's "这座山很高。" -> "那座桥修得很漂亮。".
  - 签证 vs hsk4_667's "他去使馆办签证。" -> "他的签证还没有批
    下来。".
  - 自由 vs batch028's hsk6_1444 "她一直向往自由的生活。" -> "他更
    喜欢自由自在地工作。".
  - 暖和 vs batch027's hsk6_0963 "今天天气很暖。" -> "穿上这件外套
    会暖和很多。".
  - 罚款 vs hsk5_324's "违反规定会被罚款。" (near-identical near-
    synonym clause) -> "他因为违章停车被罚款了。".
  - 顺 vs hsk3_126's "你放心，一切都很顺利。" -> "这次考试他考得
    很顺。".
  - 气 vs hsk3_330's "别生气了。" -> "屋里的气味有点怪。".
  - 发达 vs hsk5_870's "这个国家的经济十分强大。" -> "这个地区的
    交通十分发达。".
Re-verified after these fixes: zero cross-corpus flags, zero
within-batch flags (see validation report).

All re-verified against the full pilot+002-030 corpus with zero
remaining exact duplicates and zero near-template flags (see
validation report).

Usage:
    python generate_examples_batch_031.py --dry-run
    python generate_examples_batch_031.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 31
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_031.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# No numeric-suffix homograph records in this batch.
NEEDS_REVIEW_IDS: set[str] = set()

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_432": [{"chinese": "你太客气了。", "pinyin": "Nǐ tài kèqi le.", "meaningVi": "Bạn khách sáo quá."}],
    "hsk4_435": [{"chinese": "他肯定会来的。", "pinyin": "Tā kěndìng huì lái de.", "meaningVi": "Anh ấy chắc chắn sẽ đến."}],
    "hsk4_438": [{"chinese": "恐怕明天会下雨。", "pinyin": "Kǒngpà míngtiān huì xiàyǔ.", "meaningVi": "E rằng ngày mai sẽ mưa."}],
    "hsk4_445": [{"chinese": "他觉得很困，想睡觉。", "pinyin": "Tā juéde hěn kùn, xiǎng shuìjiào.", "meaningVi": "Anh ấy cảm thấy buồn ngủ, muốn đi ngủ."}],
    "hsk4_446": [{"chinese": "他遇到了很大的困难。", "pinyin": "Tā yùdàole hěn dà de kùnnan.", "meaningVi": "Anh ấy đã gặp phải khó khăn rất lớn."}],
    "hsk4_462": [{"chinese": "他说话很有礼貌。", "pinyin": "Tā shuōhuà hěn yǒu lǐmào.", "meaningVi": "Anh ấy nói chuyện rất lịch sự."}],
    "hsk4_463": [{"chinese": "他的理想是当医生。", "pinyin": "Tā de lǐxiǎng shì dāng yīshēng.", "meaningVi": "Lý tưởng của anh ấy là làm bác sĩ."}],
    "hsk4_469": [{"chinese": "他连饭都没吃就走了。", "pinyin": "Tā lián fàn dōu méi chī jiù zǒu le.", "meaningVi": "Anh ấy đến cả cơm cũng chưa ăn đã đi rồi."}],
    "hsk4_474": [{"chinese": "屋里灯很亮。", "pinyin": "Wū lǐ dēng hěn liàng.", "meaningVi": "Trong phòng đèn rất sáng."}],
    "hsk4_475": [{"chinese": "请把名单列出来。", "pinyin": "Qǐng bǎ míngdān lièchūlai.", "meaningVi": "Xin liệt kê danh sách ra."}],
    "hsk4_480": [{"chinese": "这是另一个问题。", "pinyin": "Zhè shì lìng yí gè wèntí.", "meaningVi": "Đây là một vấn đề khác."}],
    "hsk4_481": [{"chinese": "另外，我还有一件事要说。", "pinyin": "Lìngwài, wǒ hái yǒu yí jiàn shì yào shuō.", "meaningVi": "Ngoài ra, tôi còn có một việc muốn nói."}],
    "hsk4_492": [{"chinese": "房间里很乱。", "pinyin": "Fángjiān lǐ hěn luàn.", "meaningVi": "Trong phòng rất lộn xộn."}],
    "hsk4_494": [{"chinese": "麻烦你帮我一个忙。", "pinyin": "Máfan nǐ bāng wǒ yí gè máng.", "meaningVi": "Phiền bạn giúp tôi một việc."}],
    "hsk4_496": [{"chinese": "杯子里装满了水。", "pinyin": "Bēizi lǐ zhuāngmǎnle shuǐ.", "meaningVi": "Trong cốc đầy nước."}],
    "hsk4_505": [{"chinese": "我昨晚做了一个梦。", "pinyin": "Wǒ zuówǎn zuòle yí gè mèng.", "meaningVi": "Tối qua tôi đã mơ một giấc mơ."}],
    "hsk4_506": [{"chinese": "他的梦想终于实现了。", "pinyin": "Tā de mèngxiǎng zhōngyú shíxiàn le.", "meaningVi": "Ước mơ của anh ấy cuối cùng đã thành hiện thực."}],
    "hsk4_521": [{"chinese": "老师对学生很有耐心。", "pinyin": "Lǎoshī duì xuésheng hěn yǒu nàixīn.", "meaningVi": "Giáo viên rất kiên nhẫn với học sinh."}],
    "hsk4_540": [{"chinese": "穿上这件外套会暖和很多。", "pinyin": "Chuānshàng zhè jiàn wàitào huì nuǎnhuo hěn duō.", "meaningVi": "Mặc chiếc áo khoác này vào sẽ ấm hơn nhiều."}],
    "hsk4_541": [{"chinese": "他偶尔会来看我。", "pinyin": "Tā ǒu'ěr huì lái kàn wǒ.", "meaningVi": "Thỉnh thoảng anh ấy đến thăm tôi."}],
    "hsk4_542": [{"chinese": "他给我拍了一张照片。", "pinyin": "Tā gěi wǒ pāile yì zhāng zhàopiàn.", "meaningVi": "Anh ấy đã chụp cho tôi một tấm ảnh."}],
    "hsk4_543": [{"chinese": "请大家排好队。", "pinyin": "Qǐng dàjiā pái hǎo duì.", "meaningVi": "Xin mọi người xếp hàng ngay ngắn."}],
    "hsk4_554": [{"chinese": "这篇报道引起了广泛关注。", "pinyin": "Zhè piān bàodào yǐnqǐle guǎngfàn guānzhù.", "meaningVi": "Bài báo này đã thu hút sự quan tâm rộng rãi."}],
    "hsk4_555": [{"chinese": "他吃了一片药。", "pinyin": "Tā chīle yí piàn yào.", "meaningVi": "Anh ấy đã uống một viên thuốc."}],
    "hsk4_557": [{"chinese": "他平常都很早起床。", "pinyin": "Tā píngcháng dōu hěn zǎo qǐchuáng.", "meaningVi": "Bình thường anh ấy đều dậy rất sớm."}],
    "hsk4_558": [{"chinese": "他的衣服破了一个洞。", "pinyin": "Tā de yīfu pòle yí gè dòng.", "meaningVi": "Áo của anh ấy bị rách một lỗ."}],
    "hsk4_570": [{"chinese": "屋里的气味有点怪。", "pinyin": "Wū lǐ de qìwèi yǒudiǎn guài.", "meaningVi": "Mùi trong phòng hơi lạ."}],
    "hsk4_576": [{"chinese": "他的签证还没有批下来。", "pinyin": "Tā de qiānzhèng hái méiyǒu pī xiàlai.", "meaningVi": "Visa của anh ấy vẫn chưa được phê duyệt."}],
    "hsk4_594": [{"chinese": "这两个词有什么区别？", "pinyin": "Zhè liǎng gè cí yǒu shénme qūbié?", "meaningVi": "Hai từ này có gì khác biệt?"}],
    "hsk4_598": [{"chinese": "全家人都很开心。", "pinyin": "Quán jiā rén dōu hěn kāixīn.", "meaningVi": "Cả nhà đều rất vui."}],
    "hsk4_609": [{"chinese": "春节的时候街上很热闹。", "pinyin": "Chūnjié de shíhou jiē shàng hěn rènao.", "meaningVi": "Vào dịp Tết trên phố rất nhộn nhịp."}],
    "hsk4_641": [{"chinese": "他浑身都湿透了。", "pinyin": "Tā húnshēn dōu shītòu le.", "meaningVi": "Toàn thân anh ấy đều ướt sũng."}],
    "hsk4_642": [{"chinese": "这条河很深。", "pinyin": "Zhè tiáo hé hěn shēn.", "meaningVi": "Con sông này rất sâu."}],
    "hsk4_652": [{"chinese": "这次实验失败了。", "pinyin": "Zhè cì shíyàn shībài le.", "meaningVi": "Thí nghiệm lần này đã thất bại."}],
    "hsk4_656": [{"chinese": "听到这个消息，他很失望。", "pinyin": "Tīngdào zhège xiāoxi, tā hěn shīwàng.", "meaningVi": "Nghe được tin này, anh ấy rất thất vọng."}],
    "hsk4_658": [{"chinese": "我们要从实际出发。", "pinyin": "Wǒmen yào cóng shíjì chūfā.", "meaningVi": "Chúng ta phải xuất phát từ thực tế."}],
    "hsk4_664": [{"chinese": "这道题实在太难了。", "pinyin": "Zhè dào tí shízài tài nán le.", "meaningVi": "Bài này thật là quá khó."}],
    "hsk4_678": [{"chinese": "他的收入不高。", "pinyin": "Tā de shōurù bù gāo.", "meaningVi": "Thu nhập của anh ấy không cao."}],
    "hsk4_683": [{"chinese": "首先，我们要确定目标。", "pinyin": "Shǒuxiān, wǒmen yào quèdìng mùbiāo.", "meaningVi": "Trước tiên, chúng ta phải xác định mục tiêu."}],
    "hsk4_700": [{"chinese": "请你说明一下情况。", "pinyin": "Qǐng nǐ shuōmíng yíxià qíngkuàng.", "meaningVi": "Xin bạn giải thích tình hình."}],
    "hsk4_703": [{"chinese": "那盆花已经死了。", "pinyin": "Nà pén huā yǐjīng sǐ le.", "meaningVi": "Chậu hoa đó đã chết rồi."}],
    "hsk4_708": [{"chinese": "这笔账我还没算清楚。", "pinyin": "Zhè bǐ zhàng wǒ hái méi suàn qīngchu.", "meaningVi": "Khoản tiền này tôi vẫn chưa tính rõ."}],
    "hsk4_709": [{"chinese": "你随便坐。", "pinyin": "Nǐ suíbiàn zuò.", "meaningVi": "Bạn cứ ngồi tùy ý."}],
    "hsk4_713": [{"chinese": "所有的学生都到齐了。", "pinyin": "Suǒyǒu de xuésheng dōu dàoqí le.", "meaningVi": "Tất cả học sinh đều đã đến đông đủ."}],
    "hsk4_714": [{"chinese": "教室里有一台电脑。", "pinyin": "Jiàoshì lǐ yǒu yì tái diànnǎo.", "meaningVi": "Trong lớp học có một chiếc máy tính."}],
    "hsk4_724": [{"chinese": "我最讨厌下雨天。", "pinyin": "Wǒ zuì tǎoyàn xiàyǔ tiān.", "meaningVi": "Tôi ghét nhất ngày trời mưa."}],
    "hsk4_743": [{"chinese": "这条路不通。", "pinyin": "Zhè tiáo lù bù tōng.", "meaningVi": "Con đường này không thông."}],
    "hsk4_744": [{"chinese": "他顺利通过了考试。", "pinyin": "Tā shùnlì tōngguòle kǎoshì.", "meaningVi": "Anh ấy đã thuận lợi vượt qua kỳ thi."}],
    "hsk4_745": [{"chinese": "学校发了一个通知。", "pinyin": "Xuéxiào fāle yí gè tōngzhī.", "meaningVi": "Nhà trường đã gửi một thông báo."}],
    "hsk4_747": [{"chinese": "他一边工作，同时一边学习。", "pinyin": "Tā yìbiān gōngzuò, tóngshí yìbiān xuéxí.", "meaningVi": "Anh ấy vừa làm việc, đồng thời vừa học tập."}],
    "hsk4_750": [{"chinese": "他的伤口很痛。", "pinyin": "Tā de shāngkǒu hěn tòng.", "meaningVi": "Vết thương của anh ấy rất đau."}],
    "hsk4_752": [{"chinese": "请看这张图。", "pinyin": "Qǐng kàn zhè zhāng tú.", "meaningVi": "Xin xem bức hình này."}],
    "hsk4_754": [{"chinese": "花盆里装的是土。", "pinyin": "Huāpén lǐ zhuāng de shì tǔ.", "meaningVi": "Trong chậu hoa đựng là đất."}],
    "hsk4_762": [{"chinese": "我完全同意你的看法。", "pinyin": "Wǒ wánquán tóngyì nǐ de kànfǎ.", "meaningVi": "Tôi hoàn toàn đồng ý với quan điểm của bạn."}],
    "hsk4_770": [{"chinese": "这里很危险，别靠近。", "pinyin": "Zhèlǐ hěn wēixiǎn, bié kàojìn.", "meaningVi": "Ở đây rất nguy hiểm, đừng lại gần."}],
    "hsk4_774": [{"chinese": "请注意个人卫生。", "pinyin": "Qǐng zhùyì gèrén wèishēng.", "meaningVi": "Xin chú ý vệ sinh cá nhân."}],
    "hsk4_786": [{"chinese": "这完全是一个误会。", "pinyin": "Zhè wánquán shì yí gè wùhuì.", "meaningVi": "Đây hoàn toàn là một sự hiểu lầm."}],
    "hsk4_801": [{"chinese": "我们要充分利用现有资源。", "pinyin": "Wǒmen yào chōngfèn lìyòng xiànyǒu zīyuán.", "meaningVi": "Chúng ta phải tận dụng đầy đủ nguồn lực hiện có."}],
    "hsk4_804": [{"chinese": "结果和我想的相反。", "pinyin": "Jiéguǒ hé wǒ xiǎng de xiāngfǎn.", "meaningVi": "Kết quả trái ngược với những gì tôi nghĩ."}],
    "hsk4_808": [{"chinese": "电话响了。", "pinyin": "Diànhuà xiǎng le.", "meaningVi": "Điện thoại reo rồi."}],
    "hsk4_817": [{"chinese": "他给大家讲了一个笑话。", "pinyin": "Tā gěi dàjiā jiǎngle yí gè xiàohua.", "meaningVi": "Anh ấy đã kể cho mọi người một câu chuyện cười."}],
    "hsk4_820": [{"chinese": "这份工作很辛苦。", "pinyin": "Zhè fèn gōngzuò hěn xīnkǔ.", "meaningVi": "Công việc này rất vất vả."}],
    "hsk4_825": [{"chinese": "听到这个好消息，他非常兴奋。", "pinyin": "Tīngdào zhège hǎo xiāoxi, tā fēicháng xīngfèn.", "meaningVi": "Nghe được tin tốt này, anh ấy vô cùng phấn khích."}],
    "hsk4_830": [{"chinese": "他们一家过得很幸福。", "pinyin": "Tāmen yì jiā guò de hěn xìngfú.", "meaningVi": "Gia đình họ sống rất hạnh phúc."}],
    "hsk4_845": [{"chinese": "他对自己要求很严格。", "pinyin": "Tā duì zìjǐ yāoqiú hěn yángé.", "meaningVi": "Anh ấy yêu cầu bản thân rất nghiêm khắc."}],
    "hsk4_862": [{"chinese": "昨天夜里下了一场雪。", "pinyin": "Zuótiān yè lǐ xiàle yì chǎng xuě.", "meaningVi": "Tối qua đã có một trận tuyết rơi."}],
    "hsk4_878": [{"chinese": "我永远不会忘记你。", "pinyin": "Wǒ yǒngyuǎn bú huì wàngjì nǐ.", "meaningVi": "Tôi sẽ mãi mãi không quên bạn."}],
    "hsk4_888": [{"chinese": "由于天气原因，航班取消了。", "pinyin": "Yóuyú tiānqì yuányīn, hángbān qǔxiāo le.", "meaningVi": "Do lý do thời tiết, chuyến bay đã bị hủy."}],
    "hsk4_897": [{"chinese": "这与他没有关系。", "pinyin": "Zhè yǔ tā méiyǒu guānxì.", "meaningVi": "Việc này không liên quan gì đến anh ấy."}],
    "hsk4_900": [{"chinese": "原来是你啊！", "pinyin": "Yuánlái shì nǐ a!", "meaningVi": "Hóa ra là bạn à!"}],
    "hsk4_906": [{"chinese": "明天大概约五点到。", "pinyin": "Míngtiān dàgài yuē wǔ diǎn dào.", "meaningVi": "Ngày mai khoảng năm giờ sẽ đến."}],
    "hsk4_907": [{"chinese": "他和女朋友有个约会。", "pinyin": "Tā hé nǚpéngyou yǒu gè yuēhuì.", "meaningVi": "Anh ấy có một cuộc hẹn với bạn gái."}],
    "hsk4_915": [{"chinese": "这件事以后再说吧。", "pinyin": "Zhè jiàn shì yǐhòu zàishuō ba.", "meaningVi": "Việc này để sau rồi nói."}],
    "hsk4_927": [{"chinese": "他是一个真正的朋友。", "pinyin": "Tā shì yí gè zhēnzhèng de péngyou.", "meaningVi": "Anh ấy là một người bạn thực sự."}],
    "hsk4_933": [{"chinese": "这件衣服正好合适。", "pinyin": "Zhè jiàn yīfu zhènghǎo héshì.", "meaningVi": "Chiếc áo này vừa vặn đúng lúc."}],
    "hsk4_935": [{"chinese": "请出示身份证明。", "pinyin": "Qǐng chūshì shēnfèn zhèngmíng.", "meaningVi": "Xin xuất trình giấy tờ chứng minh."}],
    "hsk4_946": [{"chinese": "这本书很值得一读。", "pinyin": "Zhè běn shū hěn zhídé yì dú.", "meaningVi": "Cuốn sách này rất đáng đọc."}],
    "hsk4_961": [{"chinese": "请把重点画出来。", "pinyin": "Qǐng bǎ zhòngdiǎn huàchūlai.", "meaningVi": "Xin đánh dấu trọng điểm ra."}],
    "hsk4_968": [{"chinese": "这是专门为儿童设计的产品。", "pinyin": "Zhè shì zhuānmén wèi értóng shèjì de chǎnpǐn.", "meaningVi": "Đây là sản phẩm được thiết kế chuyên biệt cho trẻ em."}],
    "hsk4_969": [{"chinese": "你学的是什么专业？", "pinyin": "Nǐ xué de shì shénme zhuānyè?", "meaningVi": "Bạn học ngành gì?"}],
    "hsk4_975": [{"chinese": "他说得很准。", "pinyin": "Tā shuō de hěn zhǔn.", "meaningVi": "Anh ấy nói rất chuẩn xác."}],
    "hsk4_981": [{"chinese": "我们要保护自然环境。", "pinyin": "Wǒmen yào bǎohù zìrán huánjìng.", "meaningVi": "Chúng ta phải bảo vệ môi trường tự nhiên."}],
    "hsk4_983": [{"chinese": "他说话很自信。", "pinyin": "Tā shuōhuà hěn zìxìn.", "meaningVi": "Anh ấy nói chuyện rất tự tin."}],
    "hsk4_985": [{"chinese": "请对这次会议做个总结。", "pinyin": "Qǐng duì zhè cì huìyì zuò gè zǒngjié.", "meaningVi": "Xin tổng kết lại cuộc họp lần này."}],
    "hsk4_987": [{"chinese": "请大家分成三个组。", "pinyin": "Qǐng dàjiā fēnchéng sān gè zǔ.", "meaningVi": "Xin mọi người chia thành ba nhóm."}],
    "hsk4_989": [{"chinese": "我们应该互相尊重。", "pinyin": "Wǒmen yīnggāi hùxiāng zūnzhòng.", "meaningVi": "Chúng ta nên tôn trọng lẫn nhau."}],
    "hsk4_990": [{"chinese": "他大概三十岁左右。", "pinyin": "Tā dàgài sānshí suì zuǒyòu.", "meaningVi": "Anh ấy khoảng ba mươi tuổi."}],
    "hsk4_991": [{"chinese": "那座桥修得很漂亮。", "pinyin": "Nà zuò qiáo xiū de hěn piàoliang.", "meaningVi": "Cây cầu đó xây rất đẹp."}],
    "hsk4_996": [{"chinese": "作为老师，他非常负责。", "pinyin": "Zuòwéi lǎoshī, tā fēicháng fùzé.", "meaningVi": "Với tư cách là giáo viên, anh ấy vô cùng có trách nhiệm."}],
    "hsk4_998": [{"chinese": "他的作文写得很好。", "pinyin": "Tā de zuòwén xiě de hěn hǎo.", "meaningVi": "Bài văn của anh ấy viết rất hay."}],
    "hsk4_999": [{"chinese": "这种药有什么作用？", "pinyin": "Zhè zhǒng yào yǒu shénme zuòyòng?", "meaningVi": "Loại thuốc này có tác dụng gì?"}],
    "hsk5_005": [{"chinese": "请大家保持安静。", "pinyin": "Qǐng dàjiā bǎochí ānjìng.", "meaningVi": "Xin mọi người giữ yên tĩnh."}],
    "hsk5_007": [{"chinese": "朋友们都来安慰她。", "pinyin": "Péngyoumen dōu lái ānwèi tā.", "meaningVi": "Bạn bè đều đến an ủi cô ấy."}],
    "hsk5_011": [{"chinese": "他对这次比赛很有把握。", "pinyin": "Tā duì zhè cì bǐsài hěn yǒu bǎwò.", "meaningVi": "Anh ấy rất có nắm chắc về cuộc thi lần này."}],
    "hsk5_012": [{"chinese": "他吓得脸色发白。", "pinyin": "Tā xià de liǎnsè fābái.", "meaningVi": "Anh ấy sợ đến mức sắc mặt tái nhợt."}],
    "hsk5_013": [{"chinese": "他半夜才睡觉。", "pinyin": "Tā bànyè cái shuìjiào.", "meaningVi": "Anh ấy đến nửa đêm mới đi ngủ."}],
    "hsk5_015": [{"chinese": "他收到了一个包裹。", "pinyin": "Tā shōudàole yí gè bāoguǒ.", "meaningVi": "Anh ấy đã nhận được một bưu kiện."}],
    "hsk5_018": [{"chinese": "这个礼物包装得很精美。", "pinyin": "Zhège lǐwù bāozhuāng de hěn jīngměi.", "meaningVi": "Món quà này được đóng gói vô cùng tinh tế."}],
    "hsk5_021": [{"chinese": "请保管好自己的物品。", "pinyin": "Qǐng bǎoguǎn hǎo zìjǐ de wùpǐn.", "meaningVi": "Xin bảo quản tốt đồ đạc của mình."}],
    "hsk5_022": [{"chinese": "大楼门口有保安。", "pinyin": "Dàlóu ménkǒu yǒu bǎo'ān.", "meaningVi": "Trước cửa tòa nhà có bảo vệ."}],
    "hsk5_028": [{"chinese": "他给自己买了一份保险。", "pinyin": "Tā gěi zìjǐ mǎile yí fèn bǎoxiǎn.", "meaningVi": "Anh ấy đã mua cho mình một gói bảo hiểm."}],
    "hsk5_031": [{"chinese": "这条新闻报道很详细。", "pinyin": "Zhè tiáo xīnwén bàodào hěn xiángxì.", "meaningVi": "Bản tin này đưa tin rất chi tiết."}],
    "hsk5_032": [{"chinese": "请把这份报告交给经理。", "pinyin": "Qǐng bǎ zhè fèn bàogào jiāo gěi jīnglǐ.", "meaningVi": "Xin nộp bản báo cáo này cho giám đốc."}],
    "hsk5_033": [{"chinese": "发生了抢劫，他立刻报警。", "pinyin": "Fāshēngle qiǎngjié, tā lìkè bàojǐng.", "meaningVi": "Xảy ra cướp giật, anh ấy lập tức báo cảnh sát."}],
    "hsk5_035": [{"chinese": "别整天抱怨了。", "pinyin": "Bié zhěngtiān bàoyuàn le.", "meaningVi": "Đừng suốt ngày than phiền nữa."}],
    "hsk5_040": [{"chinese": "这套丛书一共十本。", "pinyin": "Zhè tào cóngshū yígòng shí běn.", "meaningVi": "Bộ sách này tổng cộng mười quyển."}],
    "hsk5_043": [{"chinese": "我本人不同意这个方案。", "pinyin": "Wǒ běnrén bù tóngyì zhège fāng'àn.", "meaningVi": "Bản thân tôi không đồng ý với phương án này."}],
    "hsk5_045": [{"chinese": "我们彼此都很了解。", "pinyin": "Wǒmen bǐcǐ dōu hěn liǎojiě.", "meaningVi": "Chúng tôi hiểu nhau rất rõ."}],
    "hsk5_048": [{"chinese": "他用了一个生动的比喻。", "pinyin": "Tā yòngle yí gè shēngdòng de bǐyù.", "meaningVi": "Anh ấy đã dùng một phép ẩn dụ sinh động."}],
    "hsk5_049": [{"chinese": "这件事必须尽快解决。", "pinyin": "Zhè jiàn shì bìxū jǐnkuài jiějué.", "meaningVi": "Việc này phải giải quyết càng sớm càng tốt."}],
    "hsk5_050": [{"chinese": "他毕竟是个孩子。", "pinyin": "Tā bìjìng shì gè háizi.", "meaningVi": "Xét cho cùng nó vẫn chỉ là một đứa trẻ."}],
    "hsk5_053": [{"chinese": "这是历史发展的必然趋势。", "pinyin": "Zhè shì lìshǐ fāzhǎn de bìrán qūshì.", "meaningVi": "Đây là xu thế tất yếu của sự phát triển lịch sử."}],
    "hsk5_057": [{"chinese": "公司人事最近有变动。", "pinyin": "Gōngsī rénshì zuìjìn yǒu biàndòng.", "meaningVi": "Nhân sự công ty gần đây có biến động."}],
    "hsk5_058": [{"chinese": "网购给生活带来了便利。", "pinyin": "Wǎnggòu gěi shēnghuó dàiláile biànlì.", "meaningVi": "Mua sắm trực tuyến mang lại sự tiện lợi cho cuộc sống."}],
    "hsk5_061": [{"chinese": "这个标志代表什么意思？", "pinyin": "Zhège biāozhì dàibiǎo shénme yìsi?", "meaningVi": "Ký hiệu này đại diện cho ý nghĩa gì?"}],
    "hsk5_067": [{"chinese": "妈妈烙了几张饼。", "pinyin": "Māma làole jǐ zhāng bǐng.", "meaningVi": "Mẹ đã làm mấy chiếc bánh."}],
    "hsk5_071": [{"chinese": "玻璃杯碎了。", "pinyin": "Bōli bēi suì le.", "meaningVi": "Cốc thủy tinh đã vỡ."}],
    "hsk5_072": [{"chinese": "周末我们去博物馆参观吧。", "pinyin": "Zhōumò wǒmen qù bówùguǎn cānguān ba.", "meaningVi": "Cuối tuần chúng ta đi tham quan bảo tàng đi."}],
    "hsk5_074": [{"chinese": "这是一场不幸的事故。", "pinyin": "Zhè shì yì chǎng búxìng de shìgù.", "meaningVi": "Đây là một tai nạn bất hạnh."}],
    "hsk5_077": [{"chinese": "今天热得不得了。", "pinyin": "Jīntiān rè de bùdéliǎo.", "meaningVi": "Hôm nay nóng kinh khủng."}],
    "hsk5_079": [{"chinese": "熬夜对身体有不良影响。", "pinyin": "Áoyè duì shēntǐ yǒu bùliáng yǐngxiǎng.", "meaningVi": "Thức khuya có ảnh hưởng xấu đến cơ thể."}],
    "hsk5_080": [{"chinese": "快点走，不然要迟到了。", "pinyin": "Kuài diǎn zǒu, bùrán yào chídào le.", "meaningVi": "Đi nhanh lên, nếu không sẽ muộn đấy."}],
    "hsk5_082": [{"chinese": "这个方案还存在不足之处。", "pinyin": "Zhège fāng'àn hái cúnzài bùzú zhī chù.", "meaningVi": "Phương án này vẫn còn tồn tại điểm thiếu sót."}],
    "hsk5_084": [{"chinese": "裁判吹响了哨子。", "pinyin": "Cáipàn chuīxiǎngle shàozi.", "meaningVi": "Trọng tài đã thổi còi."}],
    "hsk5_090": [{"chinese": "他在餐饮行业工作。", "pinyin": "Tā zài cānyǐn hángyè gōngzuò.", "meaningVi": "Anh ấy làm việc trong ngành ẩm thực."}],
    "hsk5_094": [{"chinese": "这套书一共有五册。", "pinyin": "Zhè tào shū yígòng yǒu wǔ cè.", "meaningVi": "Bộ sách này tổng cộng có năm cuốn."}],
    "hsk5_099": [{"chinese": "请把插头插好。", "pinyin": "Qǐng bǎ chātóu chāhǎo.", "meaningVi": "Xin cắm phích điện cho chắc."}],
    "hsk5_1008": [{"chinese": "这次比赛他出现了失误。", "pinyin": "Zhè cì bǐsài tā chūxiànle shīwù.", "meaningVi": "Trận đấu lần này anh ấy đã mắc sai sót."}],
    "hsk5_101": [{"chinese": "两队实力有差距。", "pinyin": "Liǎng duì shílì yǒu chājù.", "meaningVi": "Sức mạnh của hai đội có sự chênh lệch."}],
    "hsk5_1014": [{"chinese": "这是最关键的时刻。", "pinyin": "Zhè shì zuì guānjiàn de shíkè.", "meaningVi": "Đây là khoảnh khắc then chốt nhất."}],
    "hsk5_1022": [{"chinese": "他们在实验室做实验。", "pinyin": "Tāmen zài shíyànshì zuò shíyàn.", "meaningVi": "Họ đang làm thí nghiệm trong phòng thí nghiệm."}],
    "hsk5_1027": [{"chinese": "他始终没有放弃。", "pinyin": "Tā shǐzhōng méiyǒu fàngqì.", "meaningVi": "Anh ấy từ đầu đến cuối không hề từ bỏ."}],
    "hsk5_103": [{"chinese": "工人正在拆房子。", "pinyin": "Gōngrén zhèngzài chāi fángzi.", "meaningVi": "Công nhân đang phá dỡ căn nhà."}],
    "hsk5_1043": [{"chinese": "这次旅行让我收获很多。", "pinyin": "Zhè cì lǚxíng ràng wǒ shōuhuò hěn duō.", "meaningVi": "Chuyến du lịch này khiến tôi thu hoạch được rất nhiều."}],
    "hsk5_1050": [{"chinese": "他明天要做手术。", "pinyin": "Tā míngtiān yào zuò shǒushù.", "meaningVi": "Ngày mai anh ấy phải phẫu thuật."}],
    "hsk5_1064": [{"chinese": "我的鼠标坏了。", "pinyin": "Wǒ de shǔbiāo huài le.", "meaningVi": "Chuột máy tính của tôi bị hỏng."}],
    "hsk5_1074": [{"chinese": "这次考试他考得很顺。", "pinyin": "Zhè cì kǎoshì tā kǎo de hěn shùn.", "meaningVi": "Kỳ thi lần này anh ấy làm rất suôn sẻ."}],
    "hsk5_1075": [{"chinese": "说不定他明天就来了。", "pinyin": "Shuōbudìng tā míngtiān jiù lái le.", "meaningVi": "Chưa biết chừng ngày mai anh ấy sẽ đến."}],
    "hsk5_1078": [{"chinese": "这是我的私人物品。", "pinyin": "Zhè shì wǒ de sīrén wùpǐn.", "meaningVi": "Đây là đồ dùng cá nhân của tôi."}],
    "hsk5_1079": [{"chinese": "他的思维方式很独特。", "pinyin": "Tā de sīwéi fāngshì hěn dútè.", "meaningVi": "Cách tư duy của anh ấy rất độc đáo."}],
    "hsk5_1086": [{"chinese": "我住在学校宿舍。", "pinyin": "Wǒ zhù zài xuéxiào sùshè.", "meaningVi": "Tôi ở trong ký túc xá của trường."}],
    "hsk5_1093": [{"chinese": "花瓶摔碎了。", "pinyin": "Huāpíng shuāisuì le.", "meaningVi": "Bình hoa đã rơi vỡ."}],
    "hsk5_1095": [{"chinese": "公司这个季度损失惨重。", "pinyin": "Gōngsī zhège jìdù sǔnshī cǎnzhòng.", "meaningVi": "Công ty quý này chịu tổn thất nặng nề."}],
    "hsk5_1098": [{"chinese": "学校附近有一所医院。", "pinyin": "Xuéxiào fùjìn yǒu yì suǒ yīyuàn.", "meaningVi": "Gần trường có một bệnh viện."}],
    "hsk5_1099": [{"chinese": "请把门锁好。", "pinyin": "Qǐng bǎ mén suǒ hǎo.", "meaningVi": "Xin khóa cửa cho kỹ."}],
    "hsk5_1105": [{"chinese": "树上结满了桃子。", "pinyin": "Shù shàng jiémǎnle táozi.", "meaningVi": "Trên cây kết đầy quả đào."}],
    "hsk5_1106": [{"chinese": "她带了一套换洗衣服。", "pinyin": "Tā dàile yí tào huànxǐ yīfu.", "meaningVi": "Cô ấy mang theo một bộ quần áo để thay."}],
    "hsk5_111": [{"chinese": "这是一个长期计划。", "pinyin": "Zhè shì yí gè chángqī jìhuà.", "meaningVi": "Đây là một kế hoạch dài hạn."}],
    "hsk5_1113": [{"chinese": "政府提倡绿色出行。", "pinyin": "Zhèngfǔ tíchàng lǜsè chūxíng.", "meaningVi": "Chính phủ đề xướng đi lại xanh."}],
    "hsk5_1119": [{"chinese": "我深深体会到了他的辛苦。", "pinyin": "Wǒ shēnshēn tǐhuìdàole tā de xīnkǔ.", "meaningVi": "Tôi đã cảm nhận sâu sắc sự vất vả của anh ấy."}],
    "hsk5_1123": [{"chinese": "我替你去开会吧。", "pinyin": "Wǒ tì nǐ qù kāihuì ba.", "meaningVi": "Để tôi đi họp thay bạn."}],
    "hsk5_113": [{"chinese": "他勇于尝试新事物。", "pinyin": "Tā yǒngyú chángshì xīn shìwù.", "meaningVi": "Anh ấy dám thử những điều mới."}],
    "hsk5_1133": [{"chinese": "这是一次巨大的挑战。", "pinyin": "Zhè shì yí cì jùdà de tiǎozhàn.", "meaningVi": "Đây là một thử thách to lớn."}],
    "hsk5_1139": [{"chinese": "他通常六点起床。", "pinyin": "Tā tōngcháng liù diǎn qǐchuáng.", "meaningVi": "Anh ấy thông thường dậy lúc sáu giờ."}],
    "hsk5_1141": [{"chinese": "他俩的想法完全不同。", "pinyin": "Tā liǎ de xiǎngfǎ wánquán bù tóng.", "meaningVi": "Suy nghĩ của hai người họ hoàn toàn khác nhau."}],
    "hsk5_1145": [{"chinese": "请大家统一穿校服。", "pinyin": "Qǐng dàjiā tǒngyī chuān xiàofú.", "meaningVi": "Xin mọi người thống nhất mặc đồng phục."}],
    "hsk5_1148": [{"chinese": "公司投入了大量资金。", "pinyin": "Gōngsī tóurùle dàliàng zījīn.", "meaningVi": "Công ty đã đầu tư một lượng lớn vốn."}],
    "hsk5_1150": [{"chinese": "他在这次比赛中表现突出。", "pinyin": "Tā zài zhè cì bǐsài zhōng biǎoxiàn tūchū.", "meaningVi": "Anh ấy thể hiện nổi bật trong cuộc thi lần này."}],
    "hsk5_1156": [{"chinese": "他把纸揉成了一团。", "pinyin": "Tā bǎ zhǐ róuchéngle yì tuán.", "meaningVi": "Anh ấy vò tờ giấy thành một cục."}],
    "hsk5_1172": [{"chinese": "这条路有点弯。", "pinyin": "Zhè tiáo lù yǒudiǎn wān.", "meaningVi": "Con đường này hơi cong."}],
    "hsk5_1175": [{"chinese": "这个制度还需要不断完善。", "pinyin": "Zhège zhìdù hái xūyào búduàn wánshàn.", "meaningVi": "Chế độ này vẫn cần không ngừng hoàn thiện."}],
    "hsk5_1177": [{"chinese": "万一下雨怎么办？", "pinyin": "Wànyī xiàyǔ zěnme bàn?", "meaningVi": "Nhỡ trời mưa thì làm sao?"}],
    "hsk5_1181": [{"chinese": "她对我微笑了一下。", "pinyin": "Tā duì wǒ wēixiàole yíxià.", "meaningVi": "Cô ấy đã mỉm cười với tôi một cái."}],
    "hsk5_1194": [{"chinese": "他的胃不太好。", "pinyin": "Tā de wèi bú tài hǎo.", "meaningVi": "Dạ dày của anh ấy không tốt lắm."}],
    "hsk5_1196": [{"chinese": "我们要为未来做打算。", "pinyin": "Wǒmen yào wèi wèilái zuò dǎsuàn.", "meaningVi": "Chúng ta phải lên kế hoạch cho tương lai."}],
    "hsk5_1199": [{"chinese": "家是最温暖的地方。", "pinyin": "Jiā shì zuì wēnnuǎn de dìfang.", "meaningVi": "Nhà là nơi ấm áp nhất."}],
    "hsk5_1201": [{"chinese": "他现在有一份稳定的工作。", "pinyin": "Tā xiànzài yǒu yí fèn wěndìng de gōngzuò.", "meaningVi": "Bây giờ anh ấy có một công việc ổn định."}],
    "hsk5_1207": [{"chinese": "他很无奈地摇了摇头。", "pinyin": "Tā hěn wúnài de yáole yáo tóu.", "meaningVi": "Anh ấy lắc đầu một cách bất lực."}],
    "hsk5_121": [{"chinese": "他朝我笑了笑。", "pinyin": "Tā cháo wǒ xiàole xiào.", "meaningVi": "Anh ấy cười với tôi."}],
    "hsk5_122": [{"chinese": "隔壁太吵了。", "pinyin": "Gébì tài chǎo le.", "meaningVi": "Bên cạnh ồn ào quá."}],
    "hsk5_1220": [{"chinese": "现在人们的物质生活水平提高了。", "pinyin": "Xiànzài rénmen de wùzhì shēnghuó shuǐpíng tígāo le.", "meaningVi": "Hiện nay mức sống vật chất của con người đã được nâng cao."}],
    "hsk5_1228": [{"chinese": "他很喜欢看戏剧。", "pinyin": "Tā hěn xǐhuan kàn xìjù.", "meaningVi": "Anh ấy rất thích xem kịch."}],
    "hsk5_1229": [{"chinese": "学校建立了新的管理系统。", "pinyin": "Xuéxiào jiànlìle xīn de guǎnlǐ xìtǒng.", "meaningVi": "Nhà trường đã xây dựng hệ thống quản lý mới."}],
    "hsk5_1231": [{"chinese": "客人们先后到达了。", "pinyin": "Kèrénmen xiānhòu dàodá le.", "meaningVi": "Các vị khách lần lượt đến."}],
    "hsk5_1232": [{"chinese": "这是一套先进的设备。", "pinyin": "Zhè shì yí tào xiānjìn de shèbèi.", "meaningVi": "Đây là một bộ thiết bị tiên tiến."}],
    "hsk5_1239": [{"chinese": "这是一座现代化的城市。", "pinyin": "Zhè shì yí zuò xiàndàihuà de chéngshì.", "meaningVi": "Đây là một thành phố hiện đại hóa."}],
    "hsk5_1242": [{"chinese": "我们要面对现实。", "pinyin": "Wǒmen yào miànduì xiànshí.", "meaningVi": "Chúng ta phải đối mặt với hiện thực."}],
    "hsk5_1244": [{"chinese": "每人限制购买两件。", "pinyin": "Měi rén xiànzhì gòumǎi liǎng jiàn.", "meaningVi": "Mỗi người bị hạn chế mua hai món."}],
    "hsk5_1249": [{"chinese": "他的水平相当不错。", "pinyin": "Tā de shuǐpíng xiāngdāng búcuò.", "meaningVi": "Trình độ của anh ấy khá là tốt."}],
    "hsk5_1250": [{"chinese": "这个地区相对比较贫穷。", "pinyin": "Zhège dìqū xiāngduì bǐjiào pínqióng.", "meaningVi": "Khu vực này tương đối nghèo."}],
    "hsk5_1255": [{"chinese": "他很享受这样的生活。", "pinyin": "Tā hěn xiǎngshòu zhèyàng de shēnghuó.", "meaningVi": "Anh ấy rất tận hưởng cuộc sống như vậy."}],
    "hsk5_1261": [{"chinese": "鸽子象征着和平。", "pinyin": "Gēzi xiàngzhēngzhe hépíng.", "meaningVi": "Chim bồ câu tượng trưng cho hòa bình."}],
    "hsk5_1265": [{"chinese": "请不要用消极的态度面对困难。", "pinyin": "Qǐng búyào yòng xiāojí de tàidù miànduì kùnnan.", "meaningVi": "Xin đừng dùng thái độ tiêu cực để đối mặt với khó khăn."}],
    "hsk5_1273": [{"chinese": "那幅画挂得有点斜。", "pinyin": "Nà fú huà guà de yǒudiǎn xié.", "meaningVi": "Bức tranh đó treo hơi lệch."}],
    "hsk5_1274": [{"chinese": "双方签订了一份协议。", "pinyin": "Shuāngfāng qiāndìngle yí fèn xiéyì.", "meaningVi": "Hai bên đã ký kết một bản thỏa thuận."}],
    "hsk5_128": [{"chinese": "请车主把车挪一下。", "pinyin": "Qǐng chēzhǔ bǎ chē nuó yíxià.", "meaningVi": "Xin chủ xe di chuyển xe một chút."}],
    "hsk5_1280": [{"chinese": "我很欣赏他的才华。", "pinyin": "Wǒ hěn xīnshǎng tā de cáihuá.", "meaningVi": "Tôi rất ngưỡng mộ tài năng của anh ấy."}],
    "hsk5_1288": [{"chinese": "说了就要行动。", "pinyin": "Shuōle jiù yào xíngdòng.", "meaningVi": "Đã nói thì phải hành động."}],
    "hsk5_1295": [{"chinese": "他很注重自己的形象。", "pinyin": "Tā hěn zhùzhòng zìjǐ de xíngxiàng.", "meaningVi": "Anh ấy rất chú trọng hình ảnh của bản thân."}],
    "hsk5_1298": [{"chinese": "我觉得自己很幸运。", "pinyin": "Wǒ juéde zìjǐ hěn xìngyùn.", "meaningVi": "Tôi cảm thấy bản thân mình rất may mắn."}],
    "hsk5_130": [{"chinese": "石头沉到了水底。", "pinyin": "Shítou chéndàole shuǐdǐ.", "meaningVi": "Hòn đá đã chìm xuống đáy nước."}],
    "hsk5_1305": [{"chinese": "他虚心接受了大家的建议。", "pinyin": "Tā xūxīn jiēshòule dàjiā de jiànyì.", "meaningVi": "Anh ấy khiêm tốn tiếp nhận ý kiến của mọi người."}],
    "hsk5_1316": [{"chinese": "他向工作人员询问了情况。", "pinyin": "Tā xiàng gōngzuò rényuán xúnwènle qíngkuàng.", "meaningVi": "Anh ấy đã hỏi thăm tình hình với nhân viên."}],
    "hsk5_1321": [{"chinese": "租房需要交押金。", "pinyin": "Zūfáng xūyào jiāo yājīn.", "meaningVi": "Thuê nhà cần phải nộp tiền cọc."}],
    "hsk5_1325": [{"chinese": "我们沿着河边散步。", "pinyin": "Wǒmen yánzhe hébiān sànbù.", "meaningVi": "Chúng tôi đi dạo dọc theo bờ sông."}],
    "hsk5_1328": [{"chinese": "他表情很严肃。", "pinyin": "Tā biǎoqíng hěn yánsù.", "meaningVi": "Vẻ mặt của anh ấy rất nghiêm túc."}],
    "hsk5_1330": [{"chinese": "他闭上了眼。", "pinyin": "Tā bìshàngle yǎn.", "meaningVi": "Anh ấy đã nhắm mắt lại."}],
    "hsk5_1337": [{"chinese": "小心，那只狗会咬人。", "pinyin": "Xiǎoxīn, nà zhī gǒu huì yǎo rén.", "meaningVi": "Cẩn thận, con chó đó sẽ cắn người."}],
    "hsk5_1344": [{"chinese": "他对公司业务很熟悉。", "pinyin": "Tā duì gōngsī yèwù hěn shúxī.", "meaningVi": "Anh ấy rất quen thuộc với nghiệp vụ của công ty."}],
    "hsk5_1346": [{"chinese": "请依据事实说话。", "pinyin": "Qǐng yījù shìshí shuōhuà.", "meaningVi": "Xin nói dựa theo sự thật."}],
    "hsk5_1347": [{"chinese": "孩子不能一直依靠父母。", "pinyin": "Háizi bù néng yìzhí yīkào fùmǔ.", "meaningVi": "Trẻ con không thể mãi dựa dẫm vào cha mẹ."}],
    "hsk5_1356": [{"chinese": "没能参加婚礼，我感到很遗憾。", "pinyin": "Méi néng cānjiā hūnlǐ, wǒ gǎndào hěn yíhàn.", "meaningVi": "Không thể tham dự đám cưới, tôi cảm thấy rất tiếc."}],
    "hsk5_1357": [{"chinese": "他们一路上说说笑笑，很快就到了。", "pinyin": "Tāmen yílù shàng shuōshuo-xiàoxiào, hěn kuài jiù dào le.", "meaningVi": "Họ vừa nói vừa cười suốt dọc đường, chẳng mấy chốc đã đến nơi."}],
    "hsk5_1360": [{"chinese": "大家的意见比较一致。", "pinyin": "Dàjiā de yìjiàn bǐjiào yízhì.", "meaningVi": "Ý kiến của mọi người khá thống nhất."}],
    "hsk5_1361": [{"chinese": "甲方和乙方签订了合同。", "pinyin": "Jiǎfāng hé yǐfāng qiāndìngle hétong.", "meaningVi": "Bên A và bên B đã ký kết hợp đồng."}],
    "hsk5_1362": [{"chinese": "他以优异的成绩毕业了。", "pinyin": "Tā yǐ yōuyì de chéngjì bìyè le.", "meaningVi": "Anh ấy đã tốt nghiệp với thành tích xuất sắc."}],
    "hsk5_1366": [{"chinese": "他终于意识到了自己的错误。", "pinyin": "Tā zhōngyú yìshídàole zìjǐ de cuòwù.", "meaningVi": "Cuối cùng anh ấy đã nhận thức được lỗi lầm của mình."}],
    "hsk5_1367": [{"chinese": "路上发生了一起意外。", "pinyin": "Lùshang fāshēngle yì qǐ yìwài.", "meaningVi": "Trên đường đã xảy ra một sự cố bất ngờ."}],
    "hsk5_1369": [{"chinese": "纳税是每个公民的义务。", "pinyin": "Nàshuì shì měi gè gōngmín de yìwù.", "meaningVi": "Nộp thuế là nghĩa vụ của mỗi công dân."}],
    "hsk5_1384": [{"chinese": "这张床太硬了。", "pinyin": "Zhè zhāng chuáng tài yìng le.", "meaningVi": "Chiếc giường này quá cứng."}],
    "hsk5_1386": [{"chinese": "电脑硬件需要升级了。", "pinyin": "Diànnǎo yìngjiàn xūyào shēngjí le.", "meaningVi": "Phần cứng máy tính cần được nâng cấp."}],
    "hsk5_1387": [{"chinese": "这项技术已经广泛应用。", "pinyin": "Zhè xiàng jìshù yǐjīng guǎngfàn yìngyòng.", "meaningVi": "Công nghệ này đã được ứng dụng rộng rãi."}],
    "hsk5_1396": [{"chinese": "这个月有购物优惠活动。", "pinyin": "Zhège yuè yǒu gòuwù yōuhuì huódòng.", "meaningVi": "Tháng này có hoạt động ưu đãi mua sắm."}],
    "hsk5_141": [{"chinese": "他在事业上取得了很大成就。", "pinyin": "Tā zài shìyè shàng qǔdéle hěn dà chéngjiù.", "meaningVi": "Anh ấy đã đạt được thành tựu lớn trong sự nghiệp."}],
    "hsk5_1416": [{"chinese": "周末大家喜欢娱乐一下。", "pinyin": "Zhōumò dàjiā xǐhuan yúlè yíxià.", "meaningVi": "Cuối tuần mọi người thích giải trí một chút."}],
    "hsk5_1421": [{"chinese": "天气预报说明天有雨。", "pinyin": "Tiānqì yùbào shuō míngtiān yǒu yǔ.", "meaningVi": "Dự báo thời tiết nói ngày mai có mưa."}],
    "hsk5_1429": [{"chinese": "月亮是圆的。", "pinyin": "Yuèliang shì yuán de.", "meaningVi": "Mặt trăng có hình tròn."}],
    "hsk5_145": [{"chinese": "这部电影只适合成人观看。", "pinyin": "Zhè bù diànyǐng zhǐ shìhé chéngrén guānkàn.", "meaningVi": "Bộ phim này chỉ phù hợp cho người lớn xem."}],
    "hsk5_1451": [{"chinese": "他早晚会明白的。", "pinyin": "Tā zǎowǎn huì míngbai de.", "meaningVi": "Sớm muộn gì anh ấy cũng sẽ hiểu ra."}],
    "hsk5_1461": [{"chinese": "她在果园里摘苹果。", "pinyin": "Tā zài guǒyuán lǐ zhāi píngguǒ.", "meaningVi": "Cô ấy hái táo trong vườn cây ăn quả."}],
    "hsk5_1465": [{"chinese": "这次展览吸引了很多人。", "pinyin": "Zhè cì zhǎnlǎn xīyǐnle hěn duō rén.", "meaningVi": "Buổi triển lãm lần này đã thu hút rất nhiều người."}],
    "hsk5_1471": [{"chinese": "最近房价涨了很多。", "pinyin": "Zuìjìn fángjià zhǎngle hěn duō.", "meaningVi": "Gần đây giá nhà đã tăng lên nhiều."}],
    "hsk5_1474": [{"chinese": "他已经掌握了这门技术。", "pinyin": "Tā yǐjīng zhǎngwòle zhè mén jìshù.", "meaningVi": "Anh ấy đã nắm vững kỹ thuật này."}],
    "hsk5_148": [{"chinese": "这个西瓜已经成熟了。", "pinyin": "Zhège xīguā yǐjīng chéngshú le.", "meaningVi": "Quả dưa hấu này đã chín rồi."}],
    "hsk5_1486": [{"chinese": "医生对他的病情做出了诊断。", "pinyin": "Yīshēng duì tā de bìngqíng zuòchūle zhěnduàn.", "meaningVi": "Bác sĩ đã đưa ra chẩn đoán về bệnh tình của anh ấy."}],
    "hsk5_1501": [{"chinese": "请沿着这条路一直走。", "pinyin": "Qǐng yánzhe zhè tiáo lù yìzhí zǒu.", "meaningVi": "Xin đi thẳng theo con đường này."}],
    "hsk5_1505": [{"chinese": "这项命令必须立刻执行。", "pinyin": "Zhè xiàng mìnglìng bìxū lìkè zhíxíng.", "meaningVi": "Mệnh lệnh này phải thực hiện ngay lập tức."}],
    "hsk5_1516": [{"chinese": "这是一款智能手机。", "pinyin": "Zhè shì yì kuǎn zhìnéng shǒujī.", "meaningVi": "Đây là một chiếc điện thoại thông minh."}],
    "hsk5_1539": [{"chinese": "熊猫喜欢吃竹子。", "pinyin": "Xióngmāo xǐhuan chī zhúzi.", "meaningVi": "Gấu trúc thích ăn tre."}],
    "hsk5_1543": [{"chinese": "这只是他的主观看法。", "pinyin": "Zhè zhǐshì tā de zhǔguān kànfǎ.", "meaningVi": "Đây chỉ là quan điểm chủ quan của anh ấy."}],
    "hsk5_1549": [{"chinese": "他刚注册了一个新账号。", "pinyin": "Tā gāng zhùcèle yí gè xīn zhànghào.", "meaningVi": "Anh ấy vừa đăng ký một tài khoản mới."}],
    "hsk5_1560": [{"chinese": "这个房间的装饰很简单。", "pinyin": "Zhège fángjiān de zhuāngshì hěn jiǎndān.", "meaningVi": "Trang trí của căn phòng này rất đơn giản."}],
    "hsk5_1575": [{"chinese": "这扇门是自动开关的。", "pinyin": "Zhè shàn mén shì zìdòng kāiguān de.", "meaningVi": "Cánh cửa này đóng mở tự động."}],
    "hsk5_1576": [{"chinese": "他学习很自觉。", "pinyin": "Tā xuéxí hěn zìjué.", "meaningVi": "Anh ấy học tập rất tự giác."}],
    "hsk5_1579": [{"chinese": "他更喜欢自由自在地工作。", "pinyin": "Tā gèng xǐhuan zìyóu-zìzài de gōngzuò.", "meaningVi": "Anh ấy thích làm việc một cách tự do thoải mái hơn."}],
    "hsk5_1591": [{"chinese": "这两种颜色组合得很好看。", "pinyin": "Zhè liǎng zhǒng yánsè zǔhé de hěn hǎokàn.", "meaningVi": "Hai màu sắc này kết hợp trông rất đẹp."}],
    "hsk5_1593": [{"chinese": "学校组织了一次春游。", "pinyin": "Xuéxiào zǔzhīle yí cì chūnyóu.", "meaningVi": "Nhà trường đã tổ chức một chuyến dã ngoại mùa xuân."}],
    "hsk5_1598": [{"chinese": "我们都很尊敬这位老师。", "pinyin": "Wǒmen dōu hěn zūnjìng zhè wèi lǎoshī.", "meaningVi": "Chúng tôi đều rất tôn kính vị giáo viên này."}],
    "hsk5_168": [{"chinese": "这只小狗长得很丑，但很可爱。", "pinyin": "Zhè zhī xiǎogǒu zhǎng de hěn chǒu, dàn hěn kě'ài.", "meaningVi": "Con chó con này trông xấu xí, nhưng rất đáng yêu."}],
    "hsk5_169": [{"chinese": "这双鞋很臭。", "pinyin": "Zhè shuāng xié hěn chòu.", "meaningVi": "Đôi giày này rất hôi."}],
    "hsk5_170": [{"chinese": "我们是初次见面。", "pinyin": "Wǒmen shì chūcì jiànmiàn.", "meaningVi": "Chúng ta là lần đầu gặp mặt."}],
    "hsk5_171": [{"chinese": "这本书明年就要出版了。", "pinyin": "Zhè běn shū míngnián jiù yào chūbǎn le.", "meaningVi": "Cuốn sách này sang năm sẽ được xuất bản."}],
    "hsk5_186": [{"chinese": "这个地方流传着一个美丽的传说。", "pinyin": "Zhège dìfang liúchuánzhe yí gè měilì de chuánshuō.", "meaningVi": "Nơi này lưu truyền một truyền thuyết đẹp."}],
    "hsk5_187": [{"chinese": "春节是中国的传统节日。", "pinyin": "Chūnjié shì Zhōngguó de chuántǒng jiérì.", "meaningVi": "Tết Nguyên Đán là lễ hội truyền thống của Trung Quốc."}],
    "hsk5_190": [{"chinese": "公司很鼓励员工创新。", "pinyin": "Gōngsī hěn gǔlì yuángōng chuàngxīn.", "meaningVi": "Công ty rất khuyến khích nhân viên đổi mới sáng tạo."}],
    "hsk5_193": [{"chinese": "他正在创作一部新小说。", "pinyin": "Tā zhèngzài chuàngzuò yí bù xīn xiǎoshuō.", "meaningVi": "Anh ấy đang sáng tác một cuốn tiểu thuyết mới."}],
    "hsk5_195": [{"chinese": "他决定辞职去创业。", "pinyin": "Tā juédìng cízhí qù chuàngyè.", "meaningVi": "Anh ấy quyết định từ chức để khởi nghiệp."}],
    "hsk5_199": [{"chinese": "这部电影情节很刺激。", "pinyin": "Zhè bù diànyǐng qíngjié hěn cìjī.", "meaningVi": "Tình tiết của bộ phim này rất kích thích."}],
    "hsk5_209": [{"chinese": "他有一笔存款。", "pinyin": "Tā yǒu yì bǐ cúnkuǎn.", "meaningVi": "Anh ấy có một khoản tiền gửi."}],
    "hsk5_221": [{"chinese": "政府大力支持这个项目。", "pinyin": "Zhèngfǔ dàlì zhīchí zhège xiàngmù.", "meaningVi": "Chính phủ ra sức hỗ trợ dự án này."}],
    "hsk5_233": [{"chinese": "这个手艺已经传了三代了。", "pinyin": "Zhège shǒuyì yǐjīng chuánle sān dài le.", "meaningVi": "Tay nghề này đã truyền được ba đời rồi."}],
    "hsk5_234": [{"chinese": "他是我们班的代表。", "pinyin": "Tā shì wǒmen bān de dàibiǎo.", "meaningVi": "Anh ấy là đại diện của lớp chúng tôi."}],
    "hsk5_238": [{"chinese": "请填一张申请单。", "pinyin": "Qǐng tián yì zhāng shēnqǐngdān.", "meaningVi": "Xin điền một tờ đơn xin."}],
    "hsk5_247": [{"chinese": "当前的任务是提高效率。", "pinyin": "Dāngqián de rènwu shì tígāo xiàolǜ.", "meaningVi": "Nhiệm vụ hiện tại là nâng cao hiệu suất."}],
    "hsk5_249": [{"chinese": "请不要挡住我的视线。", "pinyin": "Qǐng búyào dǎngzhù wǒ de shìxiàn.", "meaningVi": "Xin đừng che tầm nhìn của tôi."}],
    "hsk5_254": [{"chinese": "他是一位有名的导演。", "pinyin": "Tā shì yí wèi yǒumíng de dǎoyǎn.", "meaningVi": "Anh ấy là một đạo diễn nổi tiếng."}],
    "hsk5_274": [{"chinese": "他们在地下修建了一条隧道。", "pinyin": "Tāmen zài dìxià xiūjiànle yì tiáo suìdào.", "meaningVi": "Họ đã xây dựng một đường hầm dưới lòng đất."}],
    "hsk5_275": [{"chinese": "昨晚发生了一次地震。", "pinyin": "Zuówǎn fāshēngle yí cì dìzhèn.", "meaningVi": "Tối qua đã xảy ra một trận động đất."}],
    "hsk5_278": [{"chinese": "遥控器需要换电池了。", "pinyin": "Yáokòngqì xūyào huàn diànchí le.", "meaningVi": "Điều khiển từ xa cần thay pin rồi."}],
    "hsk5_286": [{"chinese": "他定期去医院检查身体。", "pinyin": "Tā dìngqī qù yīyuàn jiǎnchá shēntǐ.", "meaningVi": "Anh ấy định kỳ đi bệnh viện kiểm tra sức khỏe."}],
    "hsk5_288": [{"chinese": "外面太冷了，水都冻上了。", "pinyin": "Wàimiàn tài lěng le, shuǐ dōu dòngshàng le.", "meaningVi": "Bên ngoài quá lạnh, nước đều đóng băng rồi."}],
    "hsk5_295": [{"chinese": "孩子应该学会独立生活。", "pinyin": "Háizi yīnggāi xuéhuì dúlì shēnghuó.", "meaningVi": "Trẻ em nên học cách sống độc lập."}],
    "hsk5_299": [{"chinese": "前面堵车了。", "pinyin": "Qiánmiàn dǔchē le.", "meaningVi": "Phía trước bị kẹt xe rồi."}],
    "hsk5_300": [{"chinese": "今天气温三十度。", "pinyin": "Jīntiān qìwēn sānshí dù.", "meaningVi": "Nhiệt độ hôm nay ba mươi độ."}],
    "hsk5_302": [{"chinese": "这是一个短期项目。", "pinyin": "Zhè shì yí gè duǎnqī xiàngmù.", "meaningVi": "Đây là một dự án ngắn hạn."}],
    "hsk5_304": [{"chinese": "门口堆着一堆纸箱。", "pinyin": "Ménkǒu duīzhe yì duī zhǐxiāng.", "meaningVi": "Trước cửa chất một đống thùng giấy."}],
    "hsk5_305": [{"chinese": "我们来对比一下这两份数据。", "pinyin": "Wǒmen lái duìbǐ yíxià zhè liǎng fèn shùjù.", "meaningVi": "Chúng ta hãy đối chiếu hai bộ dữ liệu này."}],
    "hsk5_310": [{"chinese": "这辆卡车能装十吨货物。", "pinyin": "Zhè liàng kǎchē néng zhuāng shí dūn huòwù.", "meaningVi": "Chiếc xe tải này có thể chở mười tấn hàng."}],
    "hsk5_311": [{"chinese": "花园里开了几朵花。", "pinyin": "Huāyuán lǐ kāile jǐ duǒ huā.", "meaningVi": "Trong vườn hoa nở mấy bông."}],
    "hsk5_318": [{"chinese": "这个地区的交通十分发达。", "pinyin": "Zhège dìqū de jiāotōng shífēn fādá.", "meaningVi": "Giao thông của khu vực này vô cùng phát triển."}],
    "hsk5_320": [{"chinese": "电灯是谁发明的？", "pinyin": "Diàndēng shì shéi fāmíng de?", "meaningVi": "Đèn điện do ai phát minh ra?"}],
    "hsk5_322": [{"chinese": "请大家踊跃发言。", "pinyin": "Qǐng dàjiā yǒngyuè fāyán.", "meaningVi": "Xin mọi người tích cực phát biểu."}],
    "hsk5_323": [{"chinese": "他的发音很标准。", "pinyin": "Tā de fāyīn hěn biāozhǔn.", "meaningVi": "Phát âm của anh ấy rất chuẩn."}],
    "hsk5_325": [{"chinese": "他因为违章停车被罚款了。", "pinyin": "Tā yīnwèi wéizhāng tíngchē bèi fákuǎn le.", "meaningVi": "Anh ấy vì đỗ xe sai quy định mà bị phạt tiền."}],
    "hsk5_329": [{"chinese": "这座城市十分繁荣。", "pinyin": "Zhè zuò chéngshì shífēn fánróng.", "meaningVi": "Thành phố này vô cùng phồn vinh."}],
    "hsk5_330": [{"chinese": "请把衣服反过来晾。", "pinyin": "Qǐng bǎ yīfu fǎn guòlai liàng.", "meaningVi": "Xin lộn ngược áo lại để phơi."}],
    "hsk5_332": [{"chinese": "这个问题我们反复讨论过了。", "pinyin": "Zhège wèntí wǒmen fǎnfù tǎolùnguò le.", "meaningVi": "Vấn đề này chúng tôi đã thảo luận đi thảo luận lại."}],
    "hsk5_334": [{"chinese": "他的反应很快。", "pinyin": "Tā de fǎnyìng hěn kuài.", "meaningVi": "Phản ứng của anh ấy rất nhanh."}],
    "hsk5_338": [{"chinese": "这块地是正方形的。", "pinyin": "Zhè kuài dì shì zhèngfāngxíng de.", "meaningVi": "Mảnh đất này có hình vuông."}],
    "hsk5_348": [{"chinese": "他们毕业后就分别了。", "pinyin": "Tāmen bìyè hòu jiù fēnbié le.", "meaningVi": "Sau khi tốt nghiệp họ đã chia tay nhau."}],
    "hsk5_350": [{"chinese": "大家纷纷发表了自己的看法。", "pinyin": "Dàjiā fēnfēn fābiǎole zìjǐ de kànfǎ.", "meaningVi": "Mọi người lần lượt bày tỏ quan điểm của mình."}],
    "hsk5_355": [{"chinese": "请你分析一下原因。", "pinyin": "Qǐng nǐ fēnxī yíxià yuányīn.", "meaningVi": "Xin bạn phân tích nguyên nhân."}],
    "hsk5_360": [{"chinese": "粉丝们疯狂地追星。", "pinyin": "Fěnsīmen fēngkuáng de zhuīxīng.", "meaningVi": "Người hâm mộ điên cuồng đuổi theo thần tượng."}],
    "hsk5_363": [{"chinese": "不能完全否定他的努力。", "pinyin": "Bù néng wánquán fǒudìng tā de nǔlì.", "meaningVi": "Không thể hoàn toàn phủ định nỗ lực của anh ấy."}],
    "hsk5_366": [{"chinese": "他扶着老人过马路。", "pinyin": "Tā fúzhe lǎorén guò mǎlù.", "meaningVi": "Anh ấy đỡ cụ già qua đường."}],
    "hsk5_372": [{"chinese": "学费给家里带来了不小的负担。", "pinyin": "Xuéfèi gěi jiālǐ dàiláile bù xiǎo de fùdān.", "meaningVi": "Học phí đã mang lại gánh nặng không nhỏ cho gia đình."}],
    "hsk5_374": [{"chinese": "这个国家资源十分富有。", "pinyin": "Zhège guójiā zīyuán shífēn fùyǒu.", "meaningVi": "Tài nguyên của quốc gia này vô cùng giàu có."}],
    "hsk5_376": [{"chinese": "教育改革一直在推进。", "pinyin": "Jiàoyù gǎigé yìzhí zài tuījìn.", "meaningVi": "Cải cách giáo dục vẫn đang được thúc đẩy."}],
    "hsk5_381": [{"chinese": "请把锅盖盖上。", "pinyin": "Qǐng bǎ guōgài gàishàng.", "meaningVi": "Xin đậy nắp nồi lại."}],
    "hsk5_382": [{"chinese": "请概括一下文章的主要内容。", "pinyin": "Qǐng gàikuò yíxià wénzhāng de zhǔyào nèiróng.", "meaningVi": "Xin tóm tắt nội dung chính của bài viết."}],
    "hsk5_385": [{"chinese": "我到的时候刚好下雨。", "pinyin": "Wǒ dào de shíhou gānghǎo xiàyǔ.", "meaningVi": "Lúc tôi đến vừa hay trời mưa."}],
    "hsk5_388": [{"chinese": "这座塔的高度是一百米。", "pinyin": "Zhè zuò tǎ de gāodù shì yìbǎi mǐ.", "meaningVi": "Chiều cao của tòa tháp này là một trăm mét."}],
    "hsk5_392": [{"chinese": "他把事情搞砸了。", "pinyin": "Tā bǎ shìqing gǎozá le.", "meaningVi": "Anh ấy đã làm hỏng việc."}],
    "hsk5_398": [{"chinese": "只有个别学生没交作业。", "pinyin": "Zhǐyǒu gèbié xuésheng méi jiāo zuòyè.", "meaningVi": "Chỉ có một số ít học sinh chưa nộp bài tập."}],
    "hsk5_403": [{"chinese": "树根扎得很深。", "pinyin": "Shùgēn zhā de hěn shēn.", "meaningVi": "Rễ cây cắm rất sâu."}],
    "hsk5_404": [{"chinese": "这根本不是问题。", "pinyin": "Zhè gēnběn bú shì wèntí.", "meaningVi": "Cái này căn bản không phải là vấn đề."}],
    "hsk5_418": [{"chinese": "他为国家做出了巨大贡献。", "pinyin": "Tā wèi guójiā zuòchūle jùdà gòngxiàn.", "meaningVi": "Anh ấy đã cống hiến to lớn cho đất nước."}],
    "hsk5_421": [{"chinese": "这些因素构成了成功的关键。", "pinyin": "Zhèxiē yīnsù gòuchéngle chénggōng de guānjiàn.", "meaningVi": "Những nhân tố này tạo thành chìa khóa của thành công."}],
    "hsk5_423": [{"chinese": "他会打鼓。", "pinyin": "Tā huì dǎgǔ.", "meaningVi": "Anh ấy biết đánh trống."}],
    "hsk5_430": [{"chinese": "别怪他，这不是他的错。", "pinyin": "Bié guài tā, zhè bú shì tā de cuò.", "meaningVi": "Đừng trách anh ấy, đây không phải lỗi của anh ấy."}],
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
