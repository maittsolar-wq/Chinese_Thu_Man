"""P5.10.3 (continued) -- Batch 021 (continues immediately after
examples_batch_020.json; entirely within HSK5). First 200-record
batch in this phase (batches 002-020 were each 100 records).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Dense homophone landscape in this 200-record batch ***
  - zhì (4th tone) mega-cluster, nine members across six characters,
    none flagged by the mechanical tier system (different `word`
    strings): 至/至今 (至); 治/治疗 (治); 制订/制定/制度/制造/制作
    (制); 智慧 (智); 志愿者 (志). Two of these are a full exact
    homophone PAIR with near-identical meaning: 制订 (zhìdìng, "to
    draft/map out") vs 制定 (zhìdìng, "to enact/formulate") --
    deliberately anchored to different registers/referents (a
    personal travel plan vs. government legislation) so the two stay
    unambiguous despite being genuine near-synonyms.
  - zhèng (4th tone) cluster, four characters: 政府/政治 (政);
    证据/证书 (证); 正如 (正); 挣 (挣, in its "to earn" reading,
    distinct from the unrelated zhēng-1st-tone 争/争取 also in this
    batch).
  - chéng (2nd tone) cluster continuing from batch 020's 成本/成分/
    程度/承担: 成果/成立/成年/成员/成长 (成); 城区 (城); 承认/承受
    (承); 乘务员 (乘); 程序 (程) -- nine new members, all kept
    distinct from each other and from the already-published batch
    020 chéng words.
  - 有力 (yǒulì, "forceful/strong") vs 有利 (yǒulì, "advantageous"):
    a full exact homophone pair, anchored to a speech's persuasiveness
    vs. a weather condition's favorability, respectively.
  - zhōng (1st tone, 中+X) eight-member family: 中华/中华民族/中级/
    中介/中期/中外/中心/中药/中医 -- each in its own well-established,
    unambiguous compound.
  - zhǔ/zhù cluster: 煮 (zhǔ, "to boil/cook") vs the seven-member 主+X
    family (主持/主动/主人/主任/主食/主题/主席, all zhǔ) vs the
    zhù-tone family 住房/住宿/住址/注重 (all zhù).
  - zī cluster: 资格/资金/资源 (资) vs 姿势 (姿) vs 咨询 (咨).
  - zhǎn cluster: 展出/展开/展示/展现 (four members, one root).
  - zhàn cluster: 占/占线 (占, "to occupy/be busy") vs 站台 (站,
    "platform") -- same pinyin+tone, different character.
  - zhǒng/zhòng/zhòng cluster: 种类/种子 (种, zhǒng reading) vs
    种植 (种, zhòng reading -- same character, different tone) vs
    重大/重量 (重, zhòng) vs 众多 (众, zhòng) -- three different
    characters sharing the zhòng(4th tone) reading, plus 种's own
    polyphony.
  - zǔ/zú cluster: 族/足够 (zú) vs 组成/阻止 (zǔ).
  - zì/zǐ cluster: 紫/子女 (zǐ) vs 自从/自身/字母 (zì).
  - zuì cluster: 醉/最初/最佳 (all zuì, 4th tone).

Self-caught near-duplicate/near-template revisions made during
drafting (before this batch was finalized -- not found by the
validator, caught while authoring, consistent with prior batches):
  - 邮票 (yóupiào): first draft "他喜欢收集邮票。" would have been an
    EXACT duplicate of 收集's own already-published example (batch
    018, hsk5_1044: "他喜欢收集邮票。") -- rewritten to "这张邮票很
    珍贵。".
  - 愿望 (yuànwàng): first draft "他终于实现了自己的愿望。" was a
    near-template match against 实现's own already-published example
    (batch 017, hsk5_1020: "他终于实现了自己的梦想。") -- rewritten to
    "她的愿望是当一名医生。".
  - 糟糕 (zāogāo): first draft risked reusing the "把钥匙忘在家里"
    scenario already used for 哎呀 (pilot) -- rewritten to an
    unrelated missed-flight scenario.
  - 整整 (zhěngzhěng): first draft "他整整等了一天。" was a near-
    template match against 整's own already-published example (batch
    016, hsk4_928: "他整整等了一个小时。") -- rewritten to "这个项目
    整整用了三年时间。".
  - 知名 (zhīmíng): first draft "他是一位知名的作家。" would have been
    the third occurrence of the "他/她是一位X的Y" template already
    used for 著名 (batch 017) and 作家 (batch 017) -- rewritten to
    "这个牌子在业内很知名。".
  - 职工 (zhígōng): first draft echoed the "X为Y提供免费午餐" template
    already used for 提供 (batch 015, hsk4_729) -- rewritten to
    "工厂里有上百名职工。".
  - 住宿 (zhùsù): first draft would have reused that same "学校为
    学生提供..." template a second time in this batch -- rewritten to
    "这家旅馆的住宿条件不错。".
  - 注重 (zhùzhòng): first draft "这家公司很注重员工培训。" was a
    near-duplicate of the near-synonym 重视's own already-published
    example (batch 017, hsk4_962: "公司很重视员工培训。") -- rewritten
    to "她很注重生活细节。".
  - 尺子 (chǐzi): first draft echoed the "用尺子...一下" template
    already used for 测 (batch 017, hsk5_095: "用尺子测一下长度。")
    -- rewritten to "他忘记带尺子了。".
  - 总统 (zǒngtǒng): first draft echoed the "他当选为..." template
    used earlier in this same batch for 主席 -- rewritten to "这个
    国家的总统即将访问中国。".
  - 遵守 (zūnshǒu): first draft "每个人都应该遵守交通规则。" was a
    near-duplicate of 应当's own draft earlier in this same batch
    ("我们应当遵守交通规则。") -- rewritten to "请遵守考场纪律。".
  All re-verified against the full pilot+002-020 corpus with zero
  remaining exact duplicates and zero near-template flags (see
  validation report).

Validator-caught fix (found by validate_examples_batch_p103.py's
target_word_present check, not by manual review): 作出 (zuòchū)'s
first draft "他做出了一个艰难的决定。" used the near-synonym variant
做出 instead of the literal target word 作出 -- rewritten to "他作出
了明智的选择。".

Automated near-template pass (character-bigram Jaccard similarity
against the full pilot+002-020 corpus) caught two further near-
synonym near-duplicates fixed after the manual drafting pass:
  - 总共 (zǒnggòng): first draft "这些东西总共多少钱？" was a near-
    template match against the near-synonym 一共's own already-
    published example (batch 005, hsk3_423: "这些东西一共多少钱？",
    differing by only 总共/一共) -- rewritten to "这次旅行总共花了
    三千元。".
  - 总之 (zǒngzhī): first draft "总之，这是一次难忘的旅行。" was a
    near-template match against 难忘's own already-published example
    (batch 013, hsk4_526: "那是一次难忘的旅行。") -- rewritten to
    "总之，我们必须尽快解决这个问题。".
  Both re-verified with zero remaining flags.

Usage:
    python generate_examples_batch_021.py --dry-run
    python generate_examples_batch_021.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 21
BATCH_SIZE = 200
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_021.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk5_1395": [{"chinese": "这个工具有很多用途。", "pinyin": "Zhège gōngjù yǒu hěn duō yòngtú.", "meaningVi": "Công cụ này có rất nhiều công dụng."}],
    "hsk5_1397": [{"chinese": "中国有悠久的历史。", "pinyin": "Zhōngguó yǒu yōujiǔ de lìshǐ.", "meaningVi": "Trung Quốc có lịch sử lâu đời."}],
    "hsk5_1398": [{"chinese": "这批种子的品质优良。", "pinyin": "Zhè pī zhǒngzi de pǐnzhì yōuliáng.", "meaningVi": "Chất lượng của lô hạt giống này rất tốt."}],
    "hsk5_1399": [{"chinese": "这里的风景十分优美。", "pinyin": "Zhèlǐ de fēngjǐng shífēn yōuměi.", "meaningVi": "Phong cảnh ở đây vô cùng tươi đẹp."}],
    "hsk5_140": [{"chinese": "这是他多年努力的成果。", "pinyin": "Zhè shì tā duō nián nǔlì de chéngguǒ.", "meaningVi": "Đây là thành quả nỗ lực nhiều năm của anh ấy."}],
    "hsk5_1400": [{"chinese": "他在比赛中占据优势。", "pinyin": "Tā zài bǐsài zhōng zhànjù yōushì.", "meaningVi": "Anh ấy chiếm ưu thế trong cuộc thi."}],
    "hsk5_1401": [{"chinese": "这家企业以优质服务著称。", "pinyin": "Zhè jiā qǐyè yǐ yōuzhì fúwù zhùchēng.", "meaningVi": "Doanh nghiệp này nổi tiếng với dịch vụ chất lượng cao."}],
    "hsk5_1402": [{"chinese": "由此可见，努力是成功的关键。", "pinyin": "Yóucǐ kějiàn, nǔlì shì chénggōng de guānjiàn.", "meaningVi": "Từ đó có thể thấy, nỗ lực là chìa khóa của thành công."}],
    "hsk5_1403": [{"chinese": "我把包裹邮寄给了朋友。", "pinyin": "Wǒ bǎ bāoguǒ yóujì gěile péngyou.", "meaningVi": "Tôi đã gửi bưu kiện cho bạn qua đường bưu điện."}],
    "hsk5_1404": [{"chinese": "邮局就在前面。", "pinyin": "Yóujú jiù zài qiánmiàn.", "meaningVi": "Bưu điện ở ngay phía trước."}],
    "hsk5_1405": [{"chinese": "我们游览了故宫。", "pinyin": "Wǒmen yóulǎnle Gùgōng.", "meaningVi": "Chúng tôi đã tham quan Cố Cung."}],
    "hsk5_1406": [{"chinese": "这张邮票很珍贵。", "pinyin": "Zhè zhāng yóupiào hěn zhēnguì.", "meaningVi": "Con tem này rất quý giá."}],
    "hsk5_1407": [{"chinese": "早餐我喜欢吃油条。", "pinyin": "Zǎocān wǒ xǐhuan chī yóutiáo.", "meaningVi": "Bữa sáng tôi thích ăn quẩy."}],
    "hsk5_1408": [{"chinese": "别犹豫了，赶快决定吧。", "pinyin": "Bié yóuyù le, gǎnkuài juédìng ba.", "meaningVi": "Đừng do dự nữa, mau quyết định đi."}],
    "hsk5_1409": [{"chinese": "吸烟对健康有害。", "pinyin": "Xīyān duì jiànkāng yǒuhài.", "meaningVi": "Hút thuốc có hại cho sức khỏe."}],
    "hsk5_1410": [{"chinese": "他的发言很有力。", "pinyin": "Tā de fāyán hěn yǒulì.", "meaningVi": "Bài phát biểu của anh ấy rất mạnh mẽ, đầy sức thuyết phục."}],
    "hsk5_1411": [{"chinese": "这个天气条件对比赛有利。", "pinyin": "Zhège tiānqì tiáojiàn duì bǐsài yǒulì.", "meaningVi": "Điều kiện thời tiết này có lợi cho trận đấu."}],
    "hsk5_1412": [{"chinese": "我们的时间有限，请抓紧。", "pinyin": "Wǒmen de shíjiān yǒuxiàn, qǐng zhuājǐn.", "meaningVi": "Thời gian của chúng ta có hạn, xin hãy khẩn trương."}],
    "hsk5_1413": [{"chinese": "多读书对孩子有益。", "pinyin": "Duō dúshū duì háizi yǒuyì.", "meaningVi": "Đọc nhiều sách có ích cho trẻ em."}],
    "hsk5_1414": [{"chinese": "早睡早起有助于健康。", "pinyin": "Zǎo shuì zǎo qǐ yǒuzhùyú jiànkāng.", "meaningVi": "Ngủ sớm dậy sớm có ích cho sức khỏe."}],
    "hsk5_1415": [{"chinese": "她的孩子在幼儿园上学。", "pinyin": "Tā de háizi zài yòu'éryuán shàngxué.", "meaningVi": "Con của cô ấy đang học ở trường mầm non."}],
    "hsk5_1417": [{"chinese": "他说话的语气很温和。", "pinyin": "Tā shuōhuà de yǔqì hěn wēnhé.", "meaningVi": "Giọng điệu nói chuyện của anh ấy rất ôn hòa."}],
    "hsk5_1418": [{"chinese": "今年的雨水比较多。", "pinyin": "Jīnnián de yǔshuǐ bǐjiào duō.", "meaningVi": "Năm nay lượng mưa khá nhiều."}],
    "hsk5_1419": [{"chinese": "他的语文成绩很好。", "pinyin": "Tā de yǔwén chéngjì hěn hǎo.", "meaningVi": "Điểm môn ngữ văn của anh ấy rất tốt."}],
    "hsk5_142": [{"chinese": "这家公司成立于两千年。", "pinyin": "Zhè jiā gōngsī chénglì yú liǎngqiān nián.", "meaningVi": "Công ty này được thành lập vào năm hai nghìn."}],
    "hsk5_1420": [{"chinese": "请发一条语音消息给我。", "pinyin": "Qǐng fā yì tiáo yǔyīn xiāoxi gěi wǒ.", "meaningVi": "Xin gửi cho tôi một tin nhắn thoại."}],
    "hsk5_1422": [{"chinese": "天气预测明天会下雨。", "pinyin": "Tiānqì yùcè míngtiān huì xiàyǔ.", "meaningVi": "Dự báo thời tiết cho biết ngày mai sẽ mưa."}],
    "hsk5_1423": [{"chinese": "我已经预订了房间。", "pinyin": "Wǒ yǐjīng yùdìngle fángjiān.", "meaningVi": "Tôi đã đặt phòng trước rồi."}],
    "hsk5_1424": [{"chinese": "我们要做好预防措施。", "pinyin": "Wǒmen yào zuò hǎo yùfáng cuòshī.", "meaningVi": "Chúng ta phải làm tốt các biện pháp phòng ngừa."}],
    "hsk5_1425": [{"chinese": "预计明天到达。", "pinyin": "Yùjì míngtiān dàodá.", "meaningVi": "Dự kiến ngày mai sẽ đến nơi."}],
    "hsk5_1426": [{"chinese": "妈妈煮了玉米。", "pinyin": "Māma zhǔle yùmǐ.", "meaningVi": "Mẹ đã luộc ngô."}],
    "hsk5_1427": [{"chinese": "看病需要提前预约。", "pinyin": "Kànbìng xūyào tíqián yùyuē.", "meaningVi": "Khám bệnh cần đặt lịch trước."}],
    "hsk5_1428": [{"chinese": "这是原价，没有打折。", "pinyin": "Zhè shì yuán jià, méiyǒu dǎzhé.", "meaningVi": "Đây là giá gốc, không có giảm giá."}],
    "hsk5_143": [{"chinese": "他已经成年了。", "pinyin": "Tā yǐjīng chéngnián le.", "meaningVi": "Anh ấy đã trưởng thành rồi (đến tuổi thành niên)."}],
    "hsk5_1430": [{"chinese": "请保持原有的顺序。", "pinyin": "Qǐng bǎochí yuányǒu de shùnxù.", "meaningVi": "Xin giữ nguyên thứ tự ban đầu."}],
    "hsk5_1431": [{"chinese": "元旦快到了。", "pinyin": "Yuándàn kuài dào le.", "meaningVi": "Tết Dương lịch sắp đến rồi."}],
    "hsk5_1432": [{"chinese": "公司很关心员工的福利。", "pinyin": "Gōngsī hěn guānxīn yuángōng de fúlì.", "meaningVi": "Công ty rất quan tâm đến phúc lợi của nhân viên."}],
    "hsk5_1433": [{"chinese": "做人要有自己的原则。", "pinyin": "Zuòrén yào yǒu zìjǐ de yuánzé.", "meaningVi": "Làm người phải có nguyên tắc riêng."}],
    "hsk5_1434": [{"chinese": "我愿为此付出努力。", "pinyin": "Wǒ yuàn wèi cǐ fùchū nǔlì.", "meaningVi": "Tôi nguyện nỗ lực vì điều này."}],
    "hsk5_1435": [{"chinese": "她的愿望是当一名医生。", "pinyin": "Tā de yuànwàng shì dāng yì míng yīshēng.", "meaningVi": "Nguyện vọng của cô ấy là trở thành bác sĩ."}],
    "hsk5_1436": [{"chinese": "我们约定明天见面。", "pinyin": "Wǒmen yuēdìng míngtiān jiànmiàn.", "meaningVi": "Chúng tôi hẹn gặp nhau vào ngày mai."}],
    "hsk5_1437": [{"chinese": "这些货物要运到北京。", "pinyin": "Zhèxiē huòwù yào yùn dào Běijīng.", "meaningVi": "Những hàng hóa này phải vận chuyển đến Bắc Kinh."}],
    "hsk5_1438": [{"chinese": "网上购物通常需要付运费。", "pinyin": "Wǎngshàng gòuwù tōngcháng xūyào fù yùnfèi.", "meaningVi": "Mua sắm trực tuyến thường cần trả phí vận chuyển."}],
    "hsk5_1439": [{"chinese": "他今天运气不错。", "pinyin": "Tā jīntiān yùnqi búcuò.", "meaningVi": "Hôm nay anh ấy vận may khá tốt."}],
    "hsk5_144": [{"chinese": "他们住在城区。", "pinyin": "Tāmen zhù zài chéngqū.", "meaningVi": "Họ sống ở khu nội thành."}],
    "hsk5_1440": [{"chinese": "这条铁路主要用于货物运输。", "pinyin": "Zhè tiáo tiělù zhǔyào yòngyú huòwù yùnshū.", "meaningVi": "Tuyến đường sắt này chủ yếu dùng để vận chuyển hàng hóa."}],
    "hsk5_1441": [{"chinese": "他能灵活运用所学的知识。", "pinyin": "Tā néng línghuó yùnyòng suǒ xué de zhīshi.", "meaningVi": "Anh ấy có thể vận dụng linh hoạt kiến thức đã học."}],
    "hsk5_1442": [{"chinese": "事故发生时他也在场。", "pinyin": "Shìgù fāshēng shí tā yě zàichǎng.", "meaningVi": "Khi vụ tai nạn xảy ra anh ấy cũng có mặt."}],
    "hsk5_1443": [{"chinese": "他根本不在乎别人怎么想。", "pinyin": "Tā gēnběn bú zàihu biéren zěnme xiǎng.", "meaningVi": "Anh ấy hoàn toàn không để ý người khác nghĩ gì."}],
    "hsk5_1444": [{"chinese": "全班同学，包括我在内，都参加了。", "pinyin": "Quán bān tóngxué, bāokuò wǒ zàinèi, dōu cānjiā le.", "meaningVi": "Cả lớp, kể cả tôi, đều đã tham gia."}],
    "hsk5_1445": [{"chinese": "客服现在在线。", "pinyin": "Kèfú xiànzài zàixiàn.", "meaningVi": "Nhân viên chăm sóc khách hàng hiện đang trực tuyến."}],
    "hsk5_1446": [{"chinese": "成功的关键在于坚持。", "pinyin": "Chénggōng de guānjiàn zàiyú jiānchí.", "meaningVi": "Chìa khóa của thành công nằm ở sự kiên trì."}],
    "hsk5_1447": [{"chinese": "大家都赞成这个提议。", "pinyin": "Dàjiā dōu zànchéng zhège tíyì.", "meaningVi": "Mọi người đều tán thành đề xuất này."}],
    "hsk5_1448": [{"chinese": "这件事办得太糟了。", "pinyin": "Zhè jiàn shì bàn de tài zāo le.", "meaningVi": "Việc này làm quá tệ rồi."}],
    "hsk5_1449": [{"chinese": "天啊，太糟糕了，我没赶上飞机。", "pinyin": "Tiān a, tài zāogāo le, wǒ méi gǎnshàng fēijī.", "meaningVi": "Trời ơi, tệ quá, tôi đã lỡ chuyến bay."}],
    "hsk5_1450": [{"chinese": "这是他早期的作品。", "pinyin": "Zhè shì tā zǎoqī de zuòpǐn.", "meaningVi": "Đây là tác phẩm thời kỳ đầu của anh ấy."}],
    "hsk5_1452": [{"chinese": "他早已忘记了这件事。", "pinyin": "Tā zǎoyǐ wàngjìle zhè jiàn shì.", "meaningVi": "Anh ấy đã quên chuyện này từ lâu rồi."}],
    "hsk5_1453": [{"chinese": "这座桥是用石头造的。", "pinyin": "Zhè zuò qiáo shì yòng shítou zào de.", "meaningVi": "Cây cầu này được xây bằng đá."}],
    "hsk5_1454": [{"chinese": "这次事故造成了很大的损失。", "pinyin": "Zhè cì shìgù zàochéngle hěn dà de sǔnshī.", "meaningVi": "Vụ tai nạn lần này đã gây ra thiệt hại rất lớn."}],
    "hsk5_1455": [{"chinese": "公司员工人数逐年递增。", "pinyin": "Gōngsī yuángōng rénshù zhúnián dìzēng.", "meaningVi": "Số lượng nhân viên công ty tăng dần theo từng năm."}],
    "hsk5_1456": [{"chinese": "一起运动可以增进感情。", "pinyin": "Yìqǐ yùndòng kěyǐ zēngjìn gǎnqíng.", "meaningVi": "Cùng nhau tập thể dục có thể tăng cường tình cảm."}],
    "hsk5_1457": [{"chinese": "锻炼可以增强体质。", "pinyin": "Duànliàn kěyǐ zēngqiáng tǐzhì.", "meaningVi": "Rèn luyện có thể tăng cường thể chất."}],
    "hsk5_1458": [{"chinese": "买一赠一。", "pinyin": "Mǎi yī zèng yī.", "meaningVi": "Mua một tặng một."}],
    "hsk5_1459": [{"chinese": "商场赠送了顾客一份小礼物。", "pinyin": "Shāngchǎng zèngsòngle gùkè yí fèn xiǎo lǐwù.", "meaningVi": "Trung tâm thương mại đã tặng khách hàng một món quà nhỏ."}],
    "hsk5_146": [{"chinese": "他承认了自己的错误。", "pinyin": "Tā chéngrènle zìjǐ de cuòwù.", "meaningVi": "Anh ấy đã thừa nhận lỗi lầm của mình."}],
    "hsk5_1462": [{"chinese": "这条街很窄。", "pinyin": "Zhè tiáo jiē hěn zhǎi.", "meaningVi": "Con phố này rất hẹp."}],
    "hsk5_1463": [{"chinese": "这些作品正在博物馆展出。", "pinyin": "Zhèxiē zuòpǐn zhèngzài bówùguǎn zhǎnchū.", "meaningVi": "Những tác phẩm này đang được trưng bày tại bảo tàng."}],
    "hsk5_1464": [{"chinese": "双方就这个问题展开了讨论。", "pinyin": "Shuāngfāng jiù zhège wèntí zhǎnkāile tǎolùn.", "meaningVi": "Hai bên đã tiến hành thảo luận về vấn đề này."}],
    "hsk5_1466": [{"chinese": "他在比赛中展示了自己的实力。", "pinyin": "Tā zài bǐsài zhōng zhǎnshìle zìjǐ de shílì.", "meaningVi": "Anh ấy đã thể hiện thực lực của mình trong cuộc thi."}],
    "hsk5_1467": [{"chinese": "这幅画展现了大自然的美。", "pinyin": "Zhè fú huà zhǎnxiànle dàzìrán de měi.", "meaningVi": "Bức tranh này thể hiện vẻ đẹp của thiên nhiên."}],
    "hsk5_1468": [{"chinese": "女性在这个行业占大多数。", "pinyin": "Nǚxìng zài zhège hángyè zhàn dàduōshù.", "meaningVi": "Nữ giới chiếm đa số trong ngành này."}],
    "hsk5_1469": [{"chinese": "火车已经进站台了。", "pinyin": "Huǒchē yǐjīng jìn zhàntái le.", "meaningVi": "Tàu hỏa đã vào sân ga rồi."}],
    "hsk5_147": [{"chinese": "他承受着很大的压力。", "pinyin": "Tā chéngshòuzhe hěn dà de yālì.", "meaningVi": "Anh ấy đang chịu đựng áp lực rất lớn."}],
    "hsk5_1470": [{"chinese": "电话一直占线。", "pinyin": "Diànhuà yìzhí zhànxiàn.", "meaningVi": "Điện thoại cứ báo bận suốt."}],
    "hsk5_1472": [{"chinese": "最近汽油涨价了。", "pinyin": "Zuìjìn qìyóu zhǎngjià le.", "meaningVi": "Gần đây xăng dầu đã tăng giá."}],
    "hsk5_1473": [{"chinese": "台下响起了热烈的掌声。", "pinyin": "Táixià xiǎngqǐle rèliè de zhǎngshēng.", "meaningVi": "Bên dưới sân khấu vang lên tiếng vỗ tay nhiệt liệt."}],
    "hsk5_1475": [{"chinese": "请输入你的账号和密码。", "pinyin": "Qǐng shūrù nǐ de zhànghào hé mìmǎ.", "meaningVi": "Xin nhập tài khoản và mật khẩu của bạn."}],
    "hsk5_1476": [{"chinese": "请把钱转到我的账户。", "pinyin": "Qǐng bǎ qián zhuǎn dào wǒ de zhànghù.", "meaningVi": "Xin chuyển tiền vào tài khoản của tôi."}],
    "hsk5_1477": [{"chinese": "天冷了，小心着凉。", "pinyin": "Tiān lěng le, xiǎoxīn zháoliáng.", "meaningVi": "Trời lạnh rồi, cẩn thận bị cảm lạnh."}],
    "hsk5_1478": [{"chinese": "公司下周将召开年会。", "pinyin": "Gōngsī xiàzhōu jiāng zhàokāi niánhuì.", "meaningVi": "Công ty tuần sau sẽ tổ chức đại hội thường niên."}],
    "hsk5_1479": [{"chinese": "现在购物有折扣。", "pinyin": "Xiànzài gòuwù yǒu zhékòu.", "meaningVi": "Bây giờ mua sắm có chiết khấu."}],
    "hsk5_1480": [{"chinese": "他大学主修哲学。", "pinyin": "Tā dàxué zhǔxiū zhéxué.", "meaningVi": "Anh ấy học chuyên ngành triết học ở đại học."}],
    "hsk5_1481": [{"chinese": "他的道歉很真诚。", "pinyin": "Tā de dàoqiàn hěn zhēnchéng.", "meaningVi": "Lời xin lỗi của anh ấy rất chân thành."}],
    "hsk5_1482": [{"chinese": "这项政策是针对年轻人制定的。", "pinyin": "Zhè xiàng zhèngcè shì zhēnduì niánqīng rén zhìdìng de.", "meaningVi": "Chính sách này được đưa ra nhằm vào giới trẻ."}],
    "hsk5_1483": [{"chinese": "这是一份珍贵的礼物。", "pinyin": "Zhè shì yí fèn zhēnguì de lǐwù.", "meaningVi": "Đây là một món quà quý giá."}],
    "hsk5_1484": [{"chinese": "这是根据真实事件改编的电影。", "pinyin": "Zhè shì gēnjù zhēnshí shìjiàn gǎibiān de diànyǐng.", "meaningVi": "Đây là bộ phim được chuyển thể từ sự kiện có thật."}],
    "hsk5_1485": [{"chinese": "我们要珍惜眼前的幸福。", "pinyin": "Wǒmen yào zhēnxī yǎnqián de xìngfú.", "meaningVi": "Chúng ta phải trân trọng hạnh phúc trước mắt."}],
    "hsk5_1487": [{"chinese": "外面刮起了一阵大风。", "pinyin": "Wàimiàn guāqǐle yí zhèn dà fēng.", "meaningVi": "Bên ngoài nổi lên một trận gió lớn."}],
    "hsk5_1488": [{"chinese": "别再争了，冷静一下。", "pinyin": "Bié zài zhēng le, lěngjìng yíxià.", "meaningVi": "Đừng tranh cãi nữa, bình tĩnh lại một chút."}],
    "hsk5_1489": [{"chinese": "我们要争取更多的机会。", "pinyin": "Wǒmen yào zhēngqǔ gèng duō de jīhuì.", "meaningVi": "Chúng ta phải tranh thủ nhiều cơ hội hơn."}],
    "hsk5_149": [{"chinese": "乘务员热情地为乘客服务。", "pinyin": "Chéngwùyuán rèqíng de wèi chéngkè fúwù.", "meaningVi": "Tiếp viên nhiệt tình phục vụ hành khách."}],
    "hsk5_1490": [{"chinese": "他把书桌收拾得很整齐。", "pinyin": "Tā bǎ shūzhuō shōushi de hěn zhěngqí.", "meaningVi": "Anh ấy dọn bàn học gọn gàng ngăn nắp."}],
    "hsk5_1491": [{"chinese": "从整体来看，这个方案是可行的。", "pinyin": "Cóng zhěngtǐ lái kàn, zhège fāng'àn shì kěxíng de.", "meaningVi": "Nhìn tổng thể, phương án này khả thi."}],
    "hsk5_1492": [{"chinese": "这个项目整整用了三年时间。", "pinyin": "Zhège xiàngmù zhěngzhěng yòngle sān nián shíjiān.", "meaningVi": "Dự án này đã mất trọn ba năm."}],
    "hsk5_1493": [{"chinese": "他每天辛苦挣钱养家。", "pinyin": "Tā měitiān xīnkǔ zhèng qián yǎng jiā.", "meaningVi": "Anh ấy mỗi ngày vất vả kiếm tiền nuôi gia đình."}],
    "hsk5_1494": [{"chinese": "政府出台了新的经济政策。", "pinyin": "Zhèngfǔ chūtáile xīn de jīngjì zhèngcè.", "meaningVi": "Chính phủ đã ban hành chính sách kinh tế mới."}],
    "hsk5_1495": [{"chinese": "警方找到了关键证据。", "pinyin": "Jǐngfāng zhǎodàole guānjiàn zhèngjù.", "meaningVi": "Cảnh sát đã tìm thấy chứng cứ then chốt."}],
    "hsk5_1496": [{"chinese": "正如大家所说，这确实是个好机会。", "pinyin": "Zhèngrú dàjiā suǒ shuō, zhè quèshí shì gè hǎo jīhuì.", "meaningVi": "Đúng như mọi người đã nói, đây thực sự là một cơ hội tốt."}],
    "hsk5_1497": [{"chinese": "他获得了汉语水平证书。", "pinyin": "Tā huòdéle Hànyǔ shuǐpíng zhèngshū.", "meaningVi": "Anh ấy đã nhận được chứng chỉ trình độ tiếng Hán."}],
    "hsk5_1498": [{"chinese": "他对政治不太感兴趣。", "pinyin": "Tā duì zhèngzhì bú tài gǎn xìngqù.", "meaningVi": "Anh ấy không hứng thú lắm với chính trị."}],
    "hsk5_1499": [{"chinese": "请给我一支笔。", "pinyin": "Qǐng gěi wǒ yì zhī bǐ.", "meaningVi": "Xin cho tôi một cây bút."}],
    "hsk5_150": [{"chinese": "请按照正确的程序操作。", "pinyin": "Qǐng ànzhào zhèngquè de chéngxù cāozuò.", "meaningVi": "Xin thao tác theo đúng trình tự."}],
    "hsk5_1500": [{"chinese": "这个牌子在业内很知名。", "pinyin": "Zhège páizi zài yènèi hěn zhīmíng.", "meaningVi": "Thương hiệu này rất nổi tiếng trong ngành."}],
    "hsk5_1502": [{"chinese": "他正在做直播。", "pinyin": "Tā zhèngzài zuò zhíbō.", "meaningVi": "Anh ấy đang livestream."}],
    "hsk5_1503": [{"chinese": "职场新人要多学习。", "pinyin": "Zhíchǎng xīnrén yào duō xuéxí.", "meaningVi": "Người mới đi làm cần học hỏi nhiều."}],
    "hsk5_1504": [{"chinese": "工厂里有上百名职工。", "pinyin": "Gōngchǎng lǐ yǒu shàng bǎi míng zhígōng.", "meaningVi": "Trong nhà máy có hơn một trăm công nhân."}],
    "hsk5_1506": [{"chinese": "血止住了。", "pinyin": "Xiě zhǐzhùle.", "meaningVi": "Máu đã cầm được rồi."}],
    "hsk5_1507": [{"chinese": "老师耐心地指导我们写作业。", "pinyin": "Lǎoshī nàixīn de zhǐdǎo wǒmen xiě zuòyè.", "meaningVi": "Giáo viên kiên nhẫn chỉ dẫn chúng tôi làm bài tập."}],
    "hsk5_1508": [{"chinese": "营业时间为上午九点至晚上九点。", "pinyin": "Yíngyè shíjiān wéi shàngwǔ jiǔ diǎn zhì wǎnshang jiǔ diǎn.", "meaningVi": "Giờ mở cửa là từ chín giờ sáng đến chín giờ tối."}],
    "hsk5_1509": [{"chinese": "这种病可以治好。", "pinyin": "Zhè zhǒng bìng kěyǐ zhì hǎo.", "meaningVi": "Bệnh này có thể chữa khỏi."}],
    "hsk5_151": [{"chinese": "他是我们团队的新成员。", "pinyin": "Tā shì wǒmen tuánduì de xīn chéngyuán.", "meaningVi": "Anh ấy là thành viên mới của đội chúng tôi."}],
    "hsk5_1510": [{"chinese": "他们制订了详细的旅行计划。", "pinyin": "Tāmen zhìdìngle xiángxì de lǚxíng jìhuà.", "meaningVi": "Họ đã lập ra một kế hoạch du lịch chi tiết."}],
    "hsk5_1511": [{"chinese": "政府制定了新的法律。", "pinyin": "Zhèngfǔ zhìdìngle xīn de fǎlǜ.", "meaningVi": "Chính phủ đã ban hành luật mới."}],
    "hsk5_1512": [{"chinese": "公司的管理制度很严格。", "pinyin": "Gōngsī de guǎnlǐ zhìdù hěn yángé.", "meaningVi": "Chế độ quản lý của công ty rất nghiêm ngặt."}],
    "hsk5_1513": [{"chinese": "这是古人智慧的结晶。", "pinyin": "Zhè shì gǔrén zhìhuì de jiéjīng.", "meaningVi": "Đây là tinh hoa trí tuệ của người xưa."}],
    "hsk5_1514": [{"chinese": "这个传统至今仍然保留着。", "pinyin": "Zhège chuántǒng zhìjīn réngrán bǎoliúzhe.", "meaningVi": "Truyền thống này đến nay vẫn còn được giữ gìn."}],
    "hsk5_1515": [{"chinese": "医生正在为他治疗。", "pinyin": "Yīshēng zhèngzài wèi tā zhìliáo.", "meaningVi": "Bác sĩ đang điều trị cho anh ấy."}],
    "hsk5_1517": [{"chinese": "很多志愿者参加了这次救灾活动。", "pinyin": "Hěn duō zhìyuànzhě cānjiāle zhè cì jiùzāi huódòng.", "meaningVi": "Rất nhiều tình nguyện viên đã tham gia hoạt động cứu trợ thiên tai lần này."}],
    "hsk5_1518": [{"chinese": "这些零件是在中国制造的。", "pinyin": "Zhèxiē língjiàn shì zài Zhōngguó zhìzào de.", "meaningVi": "Những linh kiện này được sản xuất tại Trung Quốc."}],
    "hsk5_1519": [{"chinese": "这道菜制作起来很简单。", "pinyin": "Zhè dào cài zhìzuò qǐlai hěn jiǎndān.", "meaningVi": "Món ăn này làm khá đơn giản."}],
    "hsk5_152": [{"chinese": "孩子在爱中健康成长。", "pinyin": "Háizi zài ài zhōng jiànkāng chéngzhǎng.", "meaningVi": "Trẻ em lớn lên khỏe mạnh trong tình yêu thương."}],
    "hsk5_1520": [{"chinese": "中华文化源远流长。", "pinyin": "Zhōnghuá wénhuà yuányuǎn-liúcháng.", "meaningVi": "Văn hóa Trung Hoa có nguồn gốc lâu đời."}],
    "hsk5_1521": [{"chinese": "中华民族有着优秀的传统美德。", "pinyin": "Zhōnghuá Mínzú yǒuzhe yōuxiù de chuántǒng měidé.", "meaningVi": "Dân tộc Trung Hoa có những đức tính truyền thống tốt đẹp."}],
    "hsk5_1522": [{"chinese": "他通过了汉语中级考试。", "pinyin": "Tā tōngguòle Hànyǔ zhōngjí kǎoshì.", "meaningVi": "Anh ấy đã vượt qua kỳ thi tiếng Hán trình độ trung cấp."}],
    "hsk5_1523": [{"chinese": "他通过中介租到了房子。", "pinyin": "Tā tōngguò zhōngjiè zūdàole fángzi.", "meaningVi": "Anh ấy đã thuê được nhà thông qua môi giới."}],
    "hsk5_1524": [{"chinese": "这是一个中期发展目标。", "pinyin": "Zhè shì yí gè zhōngqī fāzhǎn mùbiāo.", "meaningVi": "Đây là một mục tiêu phát triển trung hạn."}],
    "hsk5_1525": [{"chinese": "这个展览吸引了中外游客。", "pinyin": "Zhège zhǎnlǎn xīyǐnle zhōngwài yóukè.", "meaningVi": "Triển lãm này đã thu hút du khách trong và ngoài nước."}],
    "hsk5_1526": [{"chinese": "这栋楼是市中心最高的建筑。", "pinyin": "Zhè dòng lóu shì shì zhōngxīn zuì gāo de jiànzhù.", "meaningVi": "Tòa nhà này là công trình cao nhất ở trung tâm thành phố."}],
    "hsk5_1527": [{"chinese": "他每天都喝中药。", "pinyin": "Tā měitiān dōu hē zhōngyào.", "meaningVi": "Anh ấy mỗi ngày đều uống thuốc Đông y."}],
    "hsk5_1528": [{"chinese": "他相信中医的疗效。", "pinyin": "Tā xiāngxìn zhōngyī de liáoxiào.", "meaningVi": "Anh ấy tin vào hiệu quả điều trị của Đông y."}],
    "hsk5_1529": [{"chinese": "这家商店的商品种类很齐全。", "pinyin": "Zhè jiā shāngdiàn de shāngpǐn zhǒnglèi hěn qíquán.", "meaningVi": "Chủng loại hàng hóa của cửa hàng này rất đầy đủ."}],
    "hsk5_153": [{"chinese": "她买了几个橙子。", "pinyin": "Tā mǎile jǐ gè chéngzi.", "meaningVi": "Cô ấy đã mua vài quả cam."}],
    "hsk5_1530": [{"chinese": "农民在地里播下了种子。", "pinyin": "Nóngmín zài dì lǐ bōxiàle zhǒngzi.", "meaningVi": "Nông dân đã gieo hạt giống xuống đất."}],
    "hsk5_1531": [{"chinese": "这是一个重大的决定。", "pinyin": "Zhè shì yí gè zhòngdà de juédìng.", "meaningVi": "Đây là một quyết định trọng đại."}],
    "hsk5_1532": [{"chinese": "这座城市拥有众多的历史古迹。", "pinyin": "Zhè zuò chéngshì yōngyǒu zhòngduō de lìshǐ gǔjì.", "meaningVi": "Thành phố này sở hữu rất nhiều di tích lịch sử."}],
    "hsk5_1533": [{"chinese": "请检查一下包裹的重量。", "pinyin": "Qǐng jiǎnchá yíxià bāoguǒ de zhòngliàng.", "meaningVi": "Xin kiểm tra trọng lượng của bưu kiện."}],
    "hsk5_1534": [{"chinese": "这里适合种植水稻。", "pinyin": "Zhèlǐ shìhé zhòngzhí shuǐdào.", "meaningVi": "Nơi đây thích hợp để trồng lúa nước."}],
    "hsk5_1535": [{"chinese": "今年是公司成立十周年。", "pinyin": "Jīnnián shì gōngsī chénglì shí zhōunián.", "meaningVi": "Năm nay là kỷ niệm mười năm thành lập công ty."}],
    "hsk5_1536": [{"chinese": "农场里养了很多猪。", "pinyin": "Nóngchǎng lǐ yǎngle hěn duō zhū.", "meaningVi": "Trong nông trại nuôi rất nhiều lợn."}],
    "hsk5_1537": [{"chinese": "情况正在逐步好转。", "pinyin": "Qíngkuàng zhèngzài zhúbù hǎozhuǎn.", "meaningVi": "Tình hình đang dần dần chuyển biến tốt."}],
    "hsk5_1538": [{"chinese": "天气逐渐变冷了。", "pinyin": "Tiānqì zhújiàn biàn lěng le.", "meaningVi": "Thời tiết dần dần trở lạnh."}],
    "hsk5_154": [{"chinese": "院子里有一个小水池。", "pinyin": "Yuànzi lǐ yǒu yí gè xiǎo shuǐchí.", "meaningVi": "Trong sân có một cái ao nhỏ."}],
    "hsk5_1540": [{"chinese": "她正在煮面条。", "pinyin": "Tā zhèngzài zhǔ miàntiáo.", "meaningVi": "Cô ấy đang nấu mì."}],
    "hsk5_1541": [{"chinese": "她主持过很多节目。", "pinyin": "Tā zhǔchíguo hěn duō jiémù.", "meaningVi": "Cô ấy đã từng dẫn rất nhiều chương trình."}],
    "hsk5_1542": [{"chinese": "他主动帮我提行李。", "pinyin": "Tā zhǔdòng bāng wǒ tí xíngli.", "meaningVi": "Anh ấy chủ động giúp tôi xách hành lý."}],
    "hsk5_1544": [{"chinese": "这只狗很听主人的话。", "pinyin": "Zhè zhī gǒu hěn tīng zhǔrén de huà.", "meaningVi": "Chú chó này rất nghe lời chủ nhân."}],
    "hsk5_1545": [{"chinese": "他是我们部门的主任。", "pinyin": "Tā shì wǒmen bùmén de zhǔrèn.", "meaningVi": "Anh ấy là chủ nhiệm của bộ phận chúng tôi."}],
    "hsk5_1546": [{"chinese": "米饭是中国人的主食。", "pinyin": "Mǐfàn shì Zhōngguórén de zhǔshí.", "meaningVi": "Cơm là món ăn chính của người Trung Quốc."}],
    "hsk5_1547": [{"chinese": "这次会议的主题是环保。", "pinyin": "Zhè cì huìyì de zhǔtí shì huánbǎo.", "meaningVi": "Chủ đề của cuộc họp lần này là bảo vệ môi trường."}],
    "hsk5_1548": [{"chinese": "他当选为学生会主席。", "pinyin": "Tā dāngxuǎn wéi xuéshēnghuì zhǔxí.", "meaningVi": "Anh ấy được bầu làm chủ tịch hội học sinh."}],
    "hsk5_155": [{"chinese": "这场雨持续了三天。", "pinyin": "Zhè chǎng yǔ chíxùle sān tiān.", "meaningVi": "Trận mưa này đã kéo dài ba ngày."}],
    "hsk5_1550": [{"chinese": "政府正在解决年轻人的住房问题。", "pinyin": "Zhèngfǔ zhèngzài jiějué niánqīng rén de zhùfáng wèntí.", "meaningVi": "Chính phủ đang giải quyết vấn đề nhà ở cho người trẻ."}],
    "hsk5_1551": [{"chinese": "这家旅馆的住宿条件不错。", "pinyin": "Zhè jiā lǚguǎn de zhùsù tiáojiàn búcuò.", "meaningVi": "Điều kiện lưu trú của khách sạn này khá tốt."}],
    "hsk5_1552": [{"chinese": "请填写您的住址。", "pinyin": "Qǐng tiánxiě nín de zhùzhǐ.", "meaningVi": "Xin điền địa chỉ cư trú của bạn."}],
    "hsk5_1553": [{"chinese": "她很注重生活细节。", "pinyin": "Tā hěn zhùzhòng shēnghuó xìjié.", "meaningVi": "Cô ấy rất chú trọng đến các chi tiết trong cuộc sống."}],
    "hsk5_1554": [{"chinese": "猫抓到了一只老鼠。", "pinyin": "Māo zhuādàole yì zhī lǎoshǔ.", "meaningVi": "Con mèo đã bắt được một con chuột."}],
    "hsk5_1555": [{"chinese": "大家要抓紧时间。", "pinyin": "Dàjiā yào zhuājǐn shíjiān.", "meaningVi": "Mọi người phải tranh thủ thời gian."}],
    "hsk5_1556": [{"chinese": "他是这方面的专家。", "pinyin": "Tā shì zhè fāngmiàn de zhuānjiā.", "meaningVi": "Anh ấy là chuyên gia trong lĩnh vực này."}],
    "hsk5_1557": [{"chinese": "请大家专心听讲。", "pinyin": "Qǐng dàjiā zhuānxīn tīngjiǎng.", "meaningVi": "Xin mọi người chuyên tâm nghe giảng."}],
    "hsk5_1558": [{"chinese": "他的态度发生了很大的转变。", "pinyin": "Tā de tàidù fāshēngle hěn dà de zhuǎnbiàn.", "meaningVi": "Thái độ của anh ấy đã có sự chuyển biến rất lớn."}],
    "hsk5_1559": [{"chinese": "请帮我转告他这个消息。", "pinyin": "Qǐng bāng wǒ zhuǎngào tā zhège xiāoxi.", "meaningVi": "Xin giúp tôi chuyển lời cho anh ấy tin này."}],
    "hsk5_156": [{"chinese": "他忘记带尺子了。", "pinyin": "Tā wàngjì dài chǐzi le.", "meaningVi": "Anh ấy quên mang thước rồi."}],
    "hsk5_1561": [{"chinese": "他们家正在装修。", "pinyin": "Tāmen jiā zhèngzài zhuāngxiū.", "meaningVi": "Nhà họ đang sửa sang nội thất."}],
    "hsk5_1562": [{"chinese": "他不小心撞到了桌子。", "pinyin": "Tā bù xiǎoxīn zhuàngdàole zhuōzi.", "meaningVi": "Anh ấy vô ý va vào cái bàn."}],
    "hsk5_1563": [{"chinese": "他的身体状况良好。", "pinyin": "Tā de shēntǐ zhuàngkuàng liánghǎo.", "meaningVi": "Tình trạng sức khỏe của anh ấy tốt."}],
    "hsk5_1564": [{"chinese": "他最近的工作状态很好。", "pinyin": "Tā zuìjìn de gōngzuò zhuàngtài hěn hǎo.", "meaningVi": "Trạng thái làm việc gần đây của anh ấy rất tốt."}],
    "hsk5_1565": [{"chinese": "他在后面追那辆公交车。", "pinyin": "Tā zài hòumiàn zhuī nà liàng gōngjiāochē.", "meaningVi": "Anh ấy chạy đuổi theo chiếc xe buýt đó ở phía sau."}],
    "hsk5_1566": [{"chinese": "每个人都有权追求自己的幸福。", "pinyin": "Měi gè rén dōu yǒu quán zhuīqiú zìjǐ de xìngfú.", "meaningVi": "Mỗi người đều có quyền theo đuổi hạnh phúc của riêng mình."}],
    "hsk5_1567": [{"chinese": "他已经获得了参赛资格。", "pinyin": "Tā yǐjīng huòdéle cānsài zīgé.", "meaningVi": "Anh ấy đã có được tư cách tham gia thi đấu."}],
    "hsk5_1568": [{"chinese": "这个项目缺乏资金支持。", "pinyin": "Zhège xiàngmù quēfá zījīn zhīchí.", "meaningVi": "Dự án này thiếu vốn hỗ trợ."}],
    "hsk5_1569": [{"chinese": "他睡觉的姿势很奇怪。", "pinyin": "Tā shuìjiào de zīshì hěn qíguài.", "meaningVi": "Tư thế ngủ của anh ấy rất kỳ lạ."}],
    "hsk5_157": [{"chinese": "小鸟展开了翅膀。", "pinyin": "Xiǎoniǎo zhǎnkāile chìbǎng.", "meaningVi": "Chú chim nhỏ xòe đôi cánh ra."}],
    "hsk5_1570": [{"chinese": "有问题请咨询客服。", "pinyin": "Yǒu wèntí qǐng zīxún kèfú.", "meaningVi": "Có vấn đề gì xin tư vấn với bộ phận chăm sóc khách hàng."}],
    "hsk5_1571": [{"chinese": "我们要合理利用自然资源。", "pinyin": "Wǒmen yào hélǐ lìyòng zìrán zīyuán.", "meaningVi": "Chúng ta phải sử dụng hợp lý tài nguyên thiên nhiên."}],
    "hsk5_1572": [{"chinese": "她穿了一件紫色的裙子。", "pinyin": "Tā chuānle yí jiàn zǐsè de qúnzi.", "meaningVi": "Cô ấy mặc một chiếc váy màu tím."}],
    "hsk5_1573": [{"chinese": "父母都希望子女幸福。", "pinyin": "Fùmǔ dōu xīwàng zǐnǚ xìngfú.", "meaningVi": "Cha mẹ đều mong con cái hạnh phúc."}],
    "hsk5_1574": [{"chinese": "自从搬家以后，他很少回老家。", "pinyin": "Zìcóng bānjiā yǐhòu, tā hěn shǎo huí lǎojiā.", "meaningVi": "Từ khi chuyển nhà, anh ấy ít khi về quê."}],
    "hsk5_1577": [{"chinese": "英语有二十六个字母。", "pinyin": "Yīngyǔ yǒu èrshíliù gè zìmǔ.", "meaningVi": "Tiếng Anh có hai mươi sáu chữ cái."}],
    "hsk5_1578": [{"chinese": "每个人都要提高自身素质。", "pinyin": "Měi gè rén dōu yào tígāo zìshēn sùzhì.", "meaningVi": "Mỗi người đều phải nâng cao tố chất của bản thân."}],
    "hsk5_1580": [{"chinese": "这是一所综合性大学。", "pinyin": "Zhè shì yì suǒ zōnghéxìng dàxué.", "meaningVi": "Đây là một trường đại học tổng hợp."}],
    "hsk5_1581": [{"chinese": "公司总部设在上海。", "pinyin": "Gōngsī zǒngbù shè zài Shànghǎi.", "meaningVi": "Trụ sở chính của công ty đặt tại Thượng Hải."}],
    "hsk5_1582": [{"chinese": "这次旅行总共花了三千元。", "pinyin": "Zhè cì lǚxíng zǒnggòng huāle sānqiān yuán.", "meaningVi": "Chuyến du lịch lần này tổng cộng đã tiêu hết ba nghìn đồng."}],
    "hsk5_1583": [{"chinese": "参赛人员总数超过了一百人。", "pinyin": "Cānsài rényuán zǒngshù chāoguòle yìbǎi rén.", "meaningVi": "Tổng số người tham gia thi đấu đã vượt quá một trăm người."}],
    "hsk5_1584": [{"chinese": "总体来说，这次活动很成功。", "pinyin": "Zǒngtǐ láishuō, zhè cì huódòng hěn chénggōng.", "meaningVi": "Nhìn chung, hoạt động lần này rất thành công."}],
    "hsk5_1585": [{"chinese": "这个国家的总统即将访问中国。", "pinyin": "Zhège guójiā de zǒngtǒng jíjiāng fǎngwèn Zhōngguó.", "meaningVi": "Tổng thống nước này sắp thăm Trung Quốc."}],
    "hsk5_1586": [{"chinese": "总之，我们必须尽快解决这个问题。", "pinyin": "Zǒngzhī, wǒmen bìxū jǐnkuài jiějué zhège wèntí.", "meaningVi": "Tóm lại, chúng ta phải giải quyết vấn đề này càng sớm càng tốt."}],
    "hsk5_1587": [{"chinese": "这里的租金比较便宜。", "pinyin": "Zhèlǐ de zūjīn bǐjiào piányi.", "meaningVi": "Tiền thuê nhà ở đây khá rẻ."}],
    "hsk5_1588": [{"chinese": "他来自一个大家族。", "pinyin": "Tā láizì yí gè dà jiāzú.", "meaningVi": "Anh ấy đến từ một đại gia tộc."}],
    "hsk5_1589": [{"chinese": "我们准备的食物足够大家吃。", "pinyin": "Wǒmen zhǔnbèi de shíwù zúgòu dàjiā chī.", "meaningVi": "Thức ăn chúng tôi chuẩn bị đủ cho mọi người ăn."}],
    "hsk5_159": [{"chinese": "手机没电了，需要充电。", "pinyin": "Shǒujī méi diàn le, xūyào chōngdiàn.", "meaningVi": "Điện thoại hết pin rồi, cần sạc điện."}],
    "hsk5_1590": [{"chinese": "这个小组由五个人组成。", "pinyin": "Zhège xiǎozǔ yóu wǔ gè rén zǔchéng.", "meaningVi": "Nhóm này gồm năm người."}],
    "hsk5_1592": [{"chinese": "警察及时阻止了这场冲突。", "pinyin": "Jǐngchá jíshí zǔzhǐle zhè chǎng chōngtū.", "meaningVi": "Cảnh sát đã kịp thời ngăn chặn cuộc xung đột này."}],
    "hsk5_1594": [{"chinese": "他张开嘴巴打了个哈欠。", "pinyin": "Tā zhāngkāi zuǐba dǎle gè hāqian.", "meaningVi": "Anh ấy há miệng ngáp một cái."}],
    "hsk5_1595": [{"chinese": "他喝醉了。", "pinyin": "Tā hē zuì le.", "meaningVi": "Anh ấy đã say rượu rồi."}],
    "hsk5_1596": [{"chinese": "最初我并不喜欢这份工作。", "pinyin": "Zuìchū wǒ bìng bù xǐhuan zhè fèn gōngzuò.", "meaningVi": "Ban đầu tôi không thích công việc này lắm."}],
    "hsk5_1597": [{"chinese": "他获得了本届比赛的最佳选手奖。", "pinyin": "Tā huòdéle běn jiè bǐsài de zuìjiā xuǎnshǒu jiǎng.", "meaningVi": "Anh ấy đã giành giải vận động viên xuất sắc nhất của kỳ thi đấu này."}],
    "hsk5_1599": [{"chinese": "请遵守考场纪律。", "pinyin": "Qǐng zūnshǒu kǎochǎng jìlǜ.", "meaningVi": "Xin tuân thủ kỷ luật phòng thi."}],
    "hsk5_160": [{"chinese": "请做好充分的准备。", "pinyin": "Qǐng zuò hǎo chōngfèn de zhǔnbèi.", "meaningVi": "Xin chuẩn bị đầy đủ."}],
    "hsk5_1600": [{"chinese": "他作出了明智的选择。", "pinyin": "Tā zuòchūle míngzhì de xuǎnzé.", "meaningVi": "Anh ấy đã đưa ra một lựa chọn sáng suốt."}],
    "hsk5_161": [{"chinese": "教室里充满了欢声笑语。", "pinyin": "Jiàoshì lǐ chōngmǎnle huānshēng-xiàoyǔ.", "meaningVi": "Trong lớp học tràn đầy tiếng cười nói vui vẻ."}],
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
