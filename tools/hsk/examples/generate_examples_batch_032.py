"""P5.10.3 (FINAL) -- Batch 032, the LAST normal-queue batch of the
entire HSK Examples generation pipeline. Continues immediately after
examples_batch_031.json.

*** IMPORTANT: this batch has 112 records, not 300 ***
get_next_batch_ids(300) was called exactly as in every prior batch,
but the deterministic (tier, id) queue had only 112 not-yet-completed
tier-1/2 records remaining across the entire HSK1-6 universe. The
function correctly returned all 112 rather than padding or erroring.
This was independently verified before drafting began (not assumed
from the batch being "planned as final"): direct queries against
load_universe()/classify_risk_tiers()/get_completed_ids() confirm
that after this batch is written, the normal (tier 1+2) queue is
EXACTLY exhausted -- 0 records remain. See the accounting reported
alongside this batch for the full derivation:
  - total universe (all HSK1-6 records): 5400
  - tier distribution across the universe: tier1=4599, tier2=713,
    tier3=80, tier4=8 (tier3+tier4 = 88 = the special-review queue,
    untouched throughout this entire pipeline)
  - normal queue (tier1+tier2) = 4599 + 713 = 5312
  - completed via pilot (100) + batches 002-031 (5100) = 5200
  - remaining before this batch = 5312 - 5200 = 112 (matches exactly)
  - after this batch: 5200 + 112 = 5312 = 100% of the normal queue

HSK/tier for every record was read directly from load_universe()/
classify_risk_tiers output and cross-checked before drafting: level
distribution {5: 112}, all tier 2, entirely HSK5, single contiguous
selection with no level transition (unlike batches 029-031). No
numeric-suffix or other source-data anomalies were found anywhere in
this batch.

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Homophone/polyphonic clusters requiring deliberate handling ***
  - jí (2nd tone): 级 (hsk5_526, "grade/level") and 集 (hsk5_527,
    "episode/collection") -- DIFFERENT characters sharing the same
    pinyin+tone, adjacent in this batch -- kept distinct.
  - qiān (1st tone): 签/签名/签字 -- same character 签 in three
    different compounds, all meaning "to sign", kept to distinct
    natural contexts (签一下名 vs 签名留念 vs 在合同上签字).
  - píng (2nd tone): 平/凭/平衡/评价/平均 -- five members across two
    characters (平/凭), each kept distinct.
  - shēn (1st tone): 深度/深入 -- same character 深, two different
    compounds, kept to distinct contexts.
  - guī (1st tone): 规律/规则 -- same character 规, two different
    compounds, kept distinct.
  - jì (4th tone): 记录/记忆/纪念 -- three different characters (记/
    纪) sharing the same pinyin+tone, kept distinct.
  - Self-caught before finalizing: 静 (jìng, hsk5_626)'s first draft
    "请保持安静。" would have echoed the sentence structure of 安
    (hsk5_005, batch 031, "请大家保持安静。") too closely -- rewritten
    to "深夜的森林格外静。" before generation.
  - Self-caught before finalizing: 较 (jiào, hsk5_593)'s first draft
    used 较为, which had already been used as a near-template
    collision fix in batch 026 (较为合理) -- rewritten to a plain
    comparative use of 较 instead ("他较其他人更有经验。").

Near-template fixes (character-bigram Jaccard >= 0.55 against the
full pilot+002-031 corpus, caught by the independent script-level
check, not the validator; no exact duplicates were found by the
validator itself on the first pass for this batch): five flags, all
fixed by diverging sentence structure while preserving natural,
correct usage:
  - 录音 vs hsk5_738's "请把这段话录下来。" -> "会议全程都有录音。".
  - 居然 vs hsk4_404's "他竟然忘记了我的生日。" (near-synonym 居然/
    竟然 in an otherwise identical clause) -> "他居然一个人完成了
    这项任务。".
  - 烧 vs hsk4_093's "妈妈在厨房做饭。" (near-synonym 烧/做) ->
    "他把开水烧开了。".
  - 架 vs hsk5_1058's "书架上摆满了书。" -> "他做了一个木架子放
    盆栽。".
  - 化 vs hsk3_028's "冰慢慢变成了水。" (near-synonym 化/变) ->
    "石油可以转化为多种产品。".
Re-verified after these fixes: zero cross-corpus flags, zero
within-batch flags (see validation report).

All re-verified against the full pilot+002-031 corpus with zero
remaining exact duplicates and zero near-template flags (see
validation report).

Usage:
    python generate_examples_batch_032.py --dry-run
    python generate_examples_batch_032.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 32
BATCH_SIZE = 300  # requested cap; queue returns fewer (112) -- see module docstring
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_032.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# No numeric-suffix homograph records in this batch.
NEEDS_REVIEW_IDS: set[str] = set()

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk5_437": [{"chinese": "未来是光明的。", "pinyin": "Wèilái shì guāngmíng de.", "meaningVi": "Tương lai là tươi sáng."}],
    "hsk5_442": [{"chinese": "这个话题引起了广泛讨论。", "pinyin": "Zhège huàtí yǐnqǐle guǎngfàn tǎolùn.", "meaningVi": "Chủ đề này đã gây ra cuộc thảo luận rộng rãi."}],
    "hsk5_443": [{"chinese": "生活要有规律。", "pinyin": "Shēnghuó yào yǒu guīlǜ.", "meaningVi": "Cuộc sống phải có quy luật."}],
    "hsk5_445": [{"chinese": "请遵守游戏规则。", "pinyin": "Qǐng zūnshǒu yóuxì guīzé.", "meaningVi": "Xin tuân thủ quy tắc trò chơi."}],
    "hsk5_448": [{"chinese": "球从桌上滚了下来。", "pinyin": "Qiú cóng zhuō shàng gǔnle xiàlai.", "meaningVi": "Quả bóng đã lăn xuống từ trên bàn."}],
    "hsk5_449": [{"chinese": "妈妈在厨房洗锅。", "pinyin": "Māma zài chúfáng xǐ guō.", "meaningVi": "Mẹ đang rửa nồi trong bếp."}],
    "hsk5_456": [{"chinese": "他对花粉过敏。", "pinyin": "Tā duì huāfěn guòmǐn.", "meaningVi": "Anh ấy bị dị ứng với phấn hoa."}],
    "hsk5_459": [{"chinese": "他哈哈大笑起来。", "pinyin": "Tā hāhā dàxiào qǐlai.", "meaningVi": "Anh ấy cười ha hả lớn."}],
    "hsk5_480": [{"chinese": "大家一起合影留念。", "pinyin": "Dàjiā yìqǐ héyǐng liúniàn.", "meaningVi": "Mọi người cùng nhau chụp ảnh chung để lưu niệm."}],
    "hsk5_495": [{"chinese": "地板很滑，小心摔倒。", "pinyin": "Dìbǎn hěn huá, xiǎoxīn shuāidǎo.", "meaningVi": "Sàn nhà rất trơn, cẩn thận ngã."}],
    "hsk5_497": [{"chinese": "石油可以转化为多种产品。", "pinyin": "Shíyóu kěyǐ zhuǎnhuà wéi duō zhǒng chǎnpǐn.", "meaningVi": "Dầu mỏ có thể chuyển hóa thành nhiều loại sản phẩm."}],
    "hsk5_507": [{"chinese": "桌上落了一层灰。", "pinyin": "Zhuō shàng luòle yì céng huī.", "meaningVi": "Trên bàn phủ một lớp bụi."}],
    "hsk5_509": [{"chinese": "他的身体正在恢复。", "pinyin": "Tā de shēntǐ zhèngzài huīfù.", "meaningVi": "Cơ thể anh ấy đang hồi phục."}],
    "hsk5_510": [{"chinese": "他穿了一件灰色的外套。", "pinyin": "Tā chuānle yí jiàn huīsè de wàitào.", "meaningVi": "Anh ấy mặc một chiếc áo khoác màu xám."}],
    "hsk5_517": [{"chinese": "你可以选择坐车或是走路。", "pinyin": "Nǐ kěyǐ xuǎnzé zuòchē huòshì zǒulù.", "meaningVi": "Bạn có thể chọn đi xe hoặc là đi bộ."}],
    "hsk5_524": [{"chinese": "他的肌肉很发达。", "pinyin": "Tā de jīròu hěn fādá.", "meaningVi": "Cơ bắp của anh ấy rất phát triển."}],
    "hsk5_526": [{"chinese": "他在读三年级。", "pinyin": "Tā zài dú sān niánjí.", "meaningVi": "Anh ấy đang học lớp ba."}],
    "hsk5_527": [{"chinese": "这部电视剧一共有三十集。", "pinyin": "Zhè bù diànshìjù yígòng yǒu sānshí jí.", "meaningVi": "Bộ phim truyền hình này tổng cộng có ba mươi tập."}],
    "hsk5_536": [{"chinese": "他半夜去医院看急诊。", "pinyin": "Tā bànyè qù yīyuàn kàn jízhěn.", "meaningVi": "Nửa đêm anh ấy đi bệnh viện cấp cứu."}],
    "hsk5_537": [{"chinese": "请大家集中注意力。", "pinyin": "Qǐng dàjiā jízhōng zhùyìlì.", "meaningVi": "Xin mọi người tập trung chú ý."}],
    "hsk5_538": [{"chinese": "车里太挤了。", "pinyin": "Chē lǐ tài jǐ le.", "meaningVi": "Trong xe quá chật chội."}],
    "hsk5_541": [{"chinese": "请把会议内容记录下来。", "pinyin": "Qǐng bǎ huìyì nèiróng jìlù xiàlai.", "meaningVi": "Xin ghi chép lại nội dung cuộc họp."}],
    "hsk5_545": [{"chinese": "这是他送我的纪念品。", "pinyin": "Zhè shì tā sòng wǒ de jìniànpǐn.", "meaningVi": "Đây là món quà lưu niệm anh ấy tặng tôi."}],
    "hsk5_549": [{"chinese": "这段记忆让他很难忘。", "pinyin": "Zhè duàn jìyì ràng tā hěn nánwàng.", "meaningVi": "Ký ức này khiến anh ấy khó quên."}],
    "hsk5_558": [{"chinese": "他在这次考试中获得了甲等。", "pinyin": "Tā zài zhè cì kǎoshì zhōng huòdéle jiǎděng.", "meaningVi": "Anh ấy đã đạt loại giáp trong kỳ thi lần này."}],
    "hsk5_560": [{"chinese": "他做了一个木架子放盆栽。", "pinyin": "Tā zuòle yí gè mù jiàzi fàng pénzāi.", "meaningVi": "Anh ấy đã làm một cái giá gỗ để đặt cây cảnh."}],
    "hsk5_579": [{"chinese": "这座建筑有上百年历史。", "pinyin": "Zhè zuò jiànzhù yǒu shàng bǎi nián lìshǐ.", "meaningVi": "Công trình kiến trúc này có lịch sử hơn trăm năm."}],
    "hsk5_582": [{"chinese": "他吃饭很讲究。", "pinyin": "Tā chīfàn hěn jiǎngjiu.", "meaningVi": "Anh ấy ăn uống rất cầu kỳ."}],
    "hsk5_590": [{"chinese": "这笔交易金额很大。", "pinyin": "Zhè bǐ jiāoyì jīn'é hěn dà.", "meaningVi": "Số tiền của giao dịch này rất lớn."}],
    "hsk5_593": [{"chinese": "他较其他人更有经验。", "pinyin": "Tā jiào qítārén gèng yǒu jīngyàn.", "meaningVi": "Anh ấy có kinh nghiệm hơn những người khác."}],
    "hsk5_595": [{"chinese": "他很少和外界接触。", "pinyin": "Tā hěn shǎo hé wàijiè jiēchù.", "meaningVi": "Anh ấy rất ít khi tiếp xúc với thế giới bên ngoài."}],
    "hsk5_605": [{"chinese": "这是第十届运动会。", "pinyin": "Zhè shì dì-shí jiè yùndònghuì.", "meaningVi": "Đây là đại hội thể thao khóa thứ mười."}],
    "hsk5_607": [{"chinese": "请把绳子系紧。", "pinyin": "Qǐng bǎ shéngzi jìjǐn.", "meaningVi": "Xin thắt chặt sợi dây."}],
    "hsk5_613": [{"chinese": "他的成绩有了很大进步。", "pinyin": "Tā de chéngjì yǒule hěn dà jìnbù.", "meaningVi": "Thành tích của anh ấy đã có tiến bộ lớn."}],
    "hsk5_621": [{"chinese": "这是一部经典电影。", "pinyin": "Zhè shì yí bù jīngdiǎn diànyǐng.", "meaningVi": "Đây là một bộ phim kinh điển."}],
    "hsk5_623": [{"chinese": "他今天看起来很有精神。", "pinyin": "Tā jīntiān kàn qǐlai hěn yǒu jīngshen.", "meaningVi": "Hôm nay anh ấy trông rất tinh thần."}],
    "hsk5_626": [{"chinese": "深夜的森林格外静。", "pinyin": "Shēnyè de sēnlín géwài jìng.", "meaningVi": "Rừng cây lúc đêm khuya vô cùng tĩnh lặng."}],
    "hsk5_633": [{"chinese": "他居然一个人完成了这项任务。", "pinyin": "Tā jūrán yí gè rén wánchéngle zhè xiàng rènwu.", "meaningVi": "Không ngờ anh ấy đã một mình hoàn thành nhiệm vụ này."}],
    "hsk5_642": [{"chinese": "请说得具体一点。", "pinyin": "Qǐng shuō de jùtǐ yìdiǎn.", "meaningVi": "Xin nói cụ thể hơn một chút."}],
    "hsk5_645": [{"chinese": "这是绝对不可能的事。", "pinyin": "Zhè shì juéduì bù kěnéng de shì.", "meaningVi": "Đây là việc tuyệt đối không thể xảy ra."}],
    "hsk5_646": [{"chinese": "他们晋级了决赛。", "pinyin": "Tāmen jìnjíle juésài.", "meaningVi": "Họ đã lọt vào vòng chung kết."}],
    "hsk5_648": [{"chinese": "他下定决心要戒烟。", "pinyin": "Tā xiàdìng juéxīn yào jièyān.", "meaningVi": "Anh ấy đã hạ quyết tâm bỏ thuốc lá."}],
    "hsk5_650": [{"chinese": "这个公园全天开放。", "pinyin": "Zhège gōngyuán quántiān kāifàng.", "meaningVi": "Công viên này mở cửa cả ngày."}],
    "hsk5_652": [{"chinese": "奥运会开幕式非常精彩。", "pinyin": "Àoyùnhuì kāimùshì fēicháng jīngcǎi.", "meaningVi": "Lễ khai mạc Olympic vô cùng đặc sắc."}],
    "hsk5_662": [{"chinese": "天上有一颗星星。", "pinyin": "Tiānshàng yǒu yì kē xīngxing.", "meaningVi": "Trên trời có một ngôi sao."}],
    "hsk5_672": [{"chinese": "一只鸟在空中飞翔。", "pinyin": "Yì zhī niǎo zài kōngzhōng fēixiáng.", "meaningVi": "Một con chim đang bay lượn trên không trung."}],
    "hsk5_673": [{"chinese": "他很难控制自己的情绪。", "pinyin": "Tā hěn nán kòngzhì zìjǐ de qíngxù.", "meaningVi": "Anh ấy rất khó kiểm soát cảm xúc của mình."}],
    "hsk5_677": [{"chinese": "这条街很宽。", "pinyin": "Zhè tiáo jiē hěn kuān.", "meaningVi": "Con phố này rất rộng."}],
    "hsk5_682": [{"chinese": "这笔资金的来源不明。", "pinyin": "Zhè bǐ zījīn de láiyuán bùmíng.", "meaningVi": "Nguồn gốc của khoản tiền này không rõ ràng."}],
    "hsk5_683": [{"chinese": "农民辛勤劳动。", "pinyin": "Nóngmín xīnqín láodòng.", "meaningVi": "Nông dân lao động chăm chỉ."}],
    "hsk5_693": [{"chinese": "这类问题很常见。", "pinyin": "Zhè lèi wèntí hěn chángjiàn.", "meaningVi": "Loại vấn đề này rất thường gặp."}],
    "hsk5_697": [{"chinese": "他买了几个梨。", "pinyin": "Tā mǎile jǐ gè lí.", "meaningVi": "Anh ấy đã mua vài quả lê."}],
    "hsk5_701": [{"chinese": "这个理论还需要验证。", "pinyin": "Zhège lǐlùn hái xūyào yànzhèng.", "meaningVi": "Lý luận này vẫn cần được kiểm chứng."}],
    "hsk5_704": [{"chinese": "他用尽全力搬起了箱子。", "pinyin": "Tā yòngjìn quánlì bānqǐle xiāngzi.", "meaningVi": "Anh ấy dùng hết sức lực để nhấc chiếc hộp lên."}],
    "hsk5_708": [{"chinese": "这笔生意的利润很高。", "pinyin": "Zhè bǐ shēngyì de lìrùn hěn gāo.", "meaningVi": "Lợi nhuận của thương vụ này rất cao."}],
    "hsk5_711": [{"chinese": "两家公司决定联合经营。", "pinyin": "Liǎng jiā gōngsī juédìng liánhé jīngyíng.", "meaningVi": "Hai công ty quyết định liên kết kinh doanh."}],
    "hsk5_716": [{"chinese": "他们正在谈恋爱。", "pinyin": "Tāmen zhèngzài tán liàn'ài.", "meaningVi": "Họ đang yêu nhau."}],
    "hsk5_722": [{"chinese": "会议临时改到了下午。", "pinyin": "Huìyì línshí gǎidàole xiàwǔ.", "meaningVi": "Cuộc họp tạm thời đổi sang buổi chiều."}],
    "hsk5_723": [{"chinese": "上课铃响了。", "pinyin": "Shàngkè líng xiǎng le.", "meaningVi": "Chuông vào lớp đã reo."}],
    "hsk5_725": [{"chinese": "他去银行领取工资。", "pinyin": "Tā qù yínháng lǐngqǔ gōngzī.", "meaningVi": "Anh ấy đến ngân hàng lãnh lương."}],
    "hsk5_727": [{"chinese": "这位领导很受尊敬。", "pinyin": "Zhè wèi lǐngdǎo hěn shòu zūnjìng.", "meaningVi": "Vị lãnh đạo này rất được kính trọng."}],
    "hsk5_731": [{"chinese": "这个好消息令大家很兴奋。", "pinyin": "Zhège hǎo xiāoxi lìng dàjiā hěn xīngfèn.", "meaningVi": "Tin tốt này khiến mọi người rất phấn khích."}],
    "hsk5_735": [{"chinese": "请在这里留言。", "pinyin": "Qǐng zài zhèlǐ liúyán.", "meaningVi": "Xin để lại lời nhắn ở đây."}],
    "hsk5_737": [{"chinese": "屋顶漏雨了。", "pinyin": "Wūdǐng lòu yǔ le.", "meaningVi": "Mái nhà bị dột mưa."}],
    "hsk5_744": [{"chinese": "会议全程都有录音。", "pinyin": "Huìyì quánchéng dōu yǒu lùyīn.", "meaningVi": "Toàn bộ cuộc họp đều có ghi âm."}],
    "hsk5_748": [{"chinese": "他被老板骂了一顿。", "pinyin": "Tā bèi lǎobǎn màle yí dùn.", "meaningVi": "Anh ấy đã bị ông chủ mắng một trận."}],
    "hsk5_754": [{"chinese": "他们之间存在矛盾。", "pinyin": "Tāmen zhījiān cúnzài máodùn.", "meaningVi": "Giữa họ tồn tại mâu thuẫn."}],
    "hsk5_764": [{"chinese": "这是我们两个人的秘密。", "pinyin": "Zhè shì wǒmen liǎng gè rén de mìmì.", "meaningVi": "Đây là bí mật của hai chúng tôi."}],
    "hsk5_765": [{"chinese": "他们合作十分密切。", "pinyin": "Tāmen hézuò shífēn mìqiè.", "meaningVi": "Sự hợp tác của họ vô cùng mật thiết."}],
    "hsk5_772": [{"chinese": "这是一个敏感的话题。", "pinyin": "Zhè shì yí gè mǐngǎn de huàtí.", "meaningVi": "Đây là một chủ đề nhạy cảm."}],
    "hsk5_776": [{"chinese": "请给出一个明确的答案。", "pinyin": "Qǐng gěichū yí gè míngquè de dá'àn.", "meaningVi": "Xin đưa ra một câu trả lời rõ ràng."}],
    "hsk5_782": [{"chinese": "照片有点模糊。", "pinyin": "Zhàopiàn yǒudiǎn móhu.", "meaningVi": "Bức ảnh hơi mờ."}],
    "hsk5_793": [{"chinese": "孩子们在楼下闹得很厉害。", "pinyin": "Háizimen zài lóuxià nào de hěn lìhai.", "meaningVi": "Bọn trẻ dưới lầu làm ồn dữ dội."}],
    "hsk5_802": [{"chinese": "他穿着一条牛仔裤。", "pinyin": "Tā chuānzhe yì tiáo niúzǎikù.", "meaningVi": "Anh ấy mặc một chiếc quần bò."}],
    "hsk5_812": [{"chinese": "公司派他去国外出差。", "pinyin": "Gōngsī pài tā qù guówài chūchāi.", "meaningVi": "Công ty cử anh ấy đi công tác nước ngoài."}],
    "hsk5_819": [{"chinese": "这条领带跟这件衬衫很配。", "pinyin": "Zhè tiáo lǐngdài gēn zhè jiàn chènshān hěn pèi.", "meaningVi": "Chiếc cà vạt này rất hợp với chiếc áo sơ mi này."}],
    "hsk5_822": [{"chinese": "请拿一个盆来洗菜。", "pinyin": "Qǐng ná yí gè pén lái xǐ cài.", "meaningVi": "Xin lấy một cái chậu để rửa rau."}],
    "hsk5_828": [{"chinese": "草原上有几匹马。", "pinyin": "Cǎoyuán shàng yǒu jǐ pǐ mǎ.", "meaningVi": "Trên thảo nguyên có vài con ngựa."}],
    "hsk5_832": [{"chinese": "这是一件艺术品。", "pinyin": "Zhè shì yí jiàn yìshùpǐn.", "meaningVi": "Đây là một tác phẩm nghệ thuật."}],
    "hsk5_837": [{"chinese": "请把桌子放平。", "pinyin": "Qǐng bǎ zhuōzi fàngpíng.", "meaningVi": "Xin đặt cái bàn cho bằng phẳng."}],
    "hsk5_839": [{"chinese": "请凭票入场。", "pinyin": "Qǐng píng piào rùchǎng.", "meaningVi": "Xin dựa vào vé để vào cửa."}],
    "hsk5_841": [{"chinese": "请注意保持身体平衡。", "pinyin": "Qǐng zhùyì bǎochí shēntǐ pínghéng.", "meaningVi": "Xin chú ý giữ thăng bằng cơ thể."}],
    "hsk5_842": [{"chinese": "大家对这部电影评价很高。", "pinyin": "Dàjiā duì zhè bù diànyǐng píngjià hěn gāo.", "meaningVi": "Mọi người đánh giá rất cao bộ phim này."}],
    "hsk5_845": [{"chinese": "全班平均分是八十五。", "pinyin": "Quán bān píngjūn fēn shì bāshíwǔ.", "meaningVi": "Điểm trung bình của cả lớp là tám mươi lăm."}],
    "hsk5_852": [{"chinese": "大家的动作很整齐。", "pinyin": "Dàjiā de dòngzuò hěn zhěngqí.", "meaningVi": "Động tác của mọi người rất đều đặn."}],
    "hsk5_859": [{"chinese": "请在这里签一下名。", "pinyin": "Qǐng zài zhèlǐ qiān yíxià míng.", "meaningVi": "Xin ký tên ở đây."}],
    "hsk5_861": [{"chinese": "请给我签名留念。", "pinyin": "Qǐng gěi wǒ qiānmíng liúniàn.", "meaningVi": "Xin ký tên lưu niệm cho tôi."}],
    "hsk5_862": [{"chinese": "请在合同上签字。", "pinyin": "Qǐng zài hétong shàng qiānzì.", "meaningVi": "Xin ký tên vào hợp đồng."}],
    "hsk5_868": [{"chinese": "他还欠我一百块钱。", "pinyin": "Tā hái qiàn wǒ yìbǎi kuài qián.", "meaningVi": "Anh ấy vẫn nợ tôi một trăm tệ."}],
    "hsk5_874": [{"chinese": "有人抢了她的包。", "pinyin": "Yǒu rén qiǎngle tā de bāo.", "meaningVi": "Có người đã cướp túi của cô ấy."}],
    "hsk5_876": [{"chinese": "他悄悄地走了出去。", "pinyin": "Tā qiāoqiāo de zǒule chūqù.", "meaningVi": "Anh ấy lặng lẽ đi ra ngoài."}],
    "hsk5_878": [{"chinese": "妈妈亲了亲孩子的脸。", "pinyin": "Māma qīnle qīn háizi de liǎn.", "meaningVi": "Mẹ đã hôn lên má của đứa trẻ."}],
    "hsk5_887": [{"chinese": "不要轻易放弃。", "pinyin": "Búyào qīngyì fàngqì.", "meaningVi": "Đừng dễ dàng từ bỏ."}],
    "hsk5_893": [{"chinese": "他向老师提出了请求。", "pinyin": "Tā xiàng lǎoshī tíchūle qǐngqiú.", "meaningVi": "Anh ấy đã đưa ra thỉnh cầu với giáo viên."}],
    "hsk5_898": [{"chinese": "这件事你没有决定权。", "pinyin": "Zhè jiàn shì nǐ méiyǒu juédìngquán.", "meaningVi": "Việc này bạn không có quyền quyết định."}],
    "hsk5_900": [{"chinese": "我们会全力以赴。", "pinyin": "Wǒmen huì quánlì yǐfù.", "meaningVi": "Chúng tôi sẽ dốc toàn lực."}],
    "hsk5_904": [{"chinese": "我劝你别去了。", "pinyin": "Wǒ quàn nǐ bié qù le.", "meaningVi": "Tôi khuyên bạn đừng đi nữa."}],
    "hsk5_905": [{"chinese": "他缺乏工作经验。", "pinyin": "Tā quēfá gōngzuò jīngyàn.", "meaningVi": "Anh ấy thiếu kinh nghiệm làm việc."}],
    "hsk5_907": [{"chinese": "请确定一下会议时间。", "pinyin": "Qǐng quèdìng yíxià huìyì shíjiān.", "meaningVi": "Xin xác định thời gian cuộc họp."}],
    "hsk5_909": [{"chinese": "天上飞过一群大雁。", "pinyin": "Tiānshàng fēiguò yì qún dàyàn.", "meaningVi": "Trên trời bay qua một đàn nhạn."}],
    "hsk5_918": [{"chinese": "这些花是人工种植的。", "pinyin": "Zhèxiē huā shì réngōng zhòngzhí de.", "meaningVi": "Những bông hoa này được trồng nhân tạo."}],
    "hsk5_927": [{"chinese": "他是历史上的重要人物。", "pinyin": "Tā shì lìshǐ shàng de zhòngyào rénwù.", "meaningVi": "Anh ấy là nhân vật quan trọng trong lịch sử."}],
    "hsk5_932": [{"chinese": "他为人正直，如他父亲一样。", "pinyin": "Tā wéirén zhèngzhí, rú tā fùqīn yíyàng.", "meaningVi": "Anh ấy là người chính trực, giống như cha anh ấy vậy."}],
    "hsk5_938": [{"chinese": "这张沙发很软。", "pinyin": "Zhè zhāng shāfā hěn ruǎn.", "meaningVi": "Chiếc ghế sofa này rất mềm."}],
    "hsk5_939": [{"chinese": "他开发了一款新软件。", "pinyin": "Tā kāifāle yì kuǎn xīn ruǎnjiàn.", "meaningVi": "Anh ấy đã phát triển một phần mềm mới."}],
    "hsk5_941": [{"chinese": "她把水洒了一地。", "pinyin": "Tā bǎ shuǐ sǎle yí dì.", "meaningVi": "Cô ấy đã làm đổ nước vãi khắp đất."}],
    "hsk5_956": [{"chinese": "他的伤已经好了。", "pinyin": "Tā de shāng yǐjīng hǎo le.", "meaningVi": "Vết thương của anh ấy đã lành rồi."}],
    "hsk5_967": [{"chinese": "他把开水烧开了。", "pinyin": "Tā bǎ kāishuǐ shāokāi le.", "meaningVi": "Anh ấy đã đun sôi nước."}],
    "hsk5_970": [{"chinese": "她舍不得离开这里。", "pinyin": "Tā shěbude líkāi zhèlǐ.", "meaningVi": "Cô ấy không nỡ rời khỏi nơi đây."}],
    "hsk5_973": [{"chinese": "这座建筑的设计很独特。", "pinyin": "Zhè zuò jiànzhù de shèjì hěn dútè.", "meaningVi": "Thiết kế của công trình này rất độc đáo."}],
    "hsk5_981": [{"chinese": "这个湖的深度超过十米。", "pinyin": "Zhège hú de shēndù chāoguò shí mǐ.", "meaningVi": "Độ sâu của hồ này vượt quá mười mét."}],
    "hsk5_985": [{"chinese": "我们需要深入了解这个问题。", "pinyin": "Wǒmen xūyào shēnrù liǎojiě zhège wèntí.", "meaningVi": "Chúng ta cần tìm hiểu sâu vấn đề này."}],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ids, universe, tiers = get_next_batch_ids(BATCH_SIZE)

    if len(ids) != len(EXAMPLES_CONTENT):
        print(f"FAIL: queue produced {len(ids)} records, expected {len(EXAMPLES_CONTENT)}", file=sys.stderr)
        sys.exit(1)
    if ids != sorted(EXAMPLES_CONTENT.keys(), key=lambda rid: (tiers[rid], rid)):
        print("FAIL: queue-computed ID set does not match this script's embedded EXAMPLES_CONTENT "
              "-- refusing to proceed", file=sys.stderr)
        sys.exit(1)

    print(f"=== batch {BATCH_NUMBER:03d} selection ===")
    print(f"records: {len(ids)} (final batch -- normal queue exhausted after this)")

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
