"""P5.10.3 (continued) -- Batch 012 (continues immediately after
examples_batch_011.json; entirely within HSK4).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch:
  - 流 (liú, "to flow") vs 留 (liú, "to stay/keep behind"): identical
    pinyin, different characters, not caught by the mechanical tier
    system (it compares the `word` string, and these are different
    words) -- hand-verified and given clearly distinct natural
    sentences (河水...流 vs 决定留在...).
  - 降/降低/降价/降落/降温 (jiàng+X family): each given its own
    natural, non-templated context (price / temperature / aircraft /
    volume).
  - 举/举办/举例/举行 (jǔ+X family) and 景点/景区/景色 (jǐng+X
    family): kept structurally distinct, no shared template.
  - 零下/零花钱/零钱/零食 (líng+X family): four unrelated compounds,
    each with its own natural context.
  - 仅 vs 仅仅 (jǐn / jǐnjǐn, near-synonyms "only"): distinct
    constructions.
  - 来不及 vs 来得及 (láibují / láidejí, antonym pair "won't make it
    in time" / "still in time"): distinct, complementary contexts.
  - 两 (liǎng, classifier-required "two") vs 俩 (liǎ, bound "the two
    of [us/them]", pinyin differs -- liǎ not liǎng): distinct
    constructions.
  - 流利 (liúlì) appears as a compound inside 口语's example sentence
    text (Vietnamese explanation only, not verbatim duplicated); the
    standalone 流利 record's own example uses different sentence text
    ("她法语说得很流利。") -- verified no duplicate Chinese sentence
    string exists across the batch.

Cross-batch collision found and fixed during authoring: the first
draft of hsk4_424 (棵) reused "院子里有一棵大树。" verbatim from
examples_batch_007.json's hsk3_342. Rewritten to "路边种着几棵柳树。"
before this batch was finalized; re-verified against the full
pilot+002-011 corpus with zero remaining collisions.

Usage:
    python generate_examples_batch_012.py --dry-run
    python generate_examples_batch_012.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 12
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_012.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_358": [{"chinese": "他将要出国留学。", "pinyin": "Tā jiāngyào chūguó liúxué.", "meaningVi": "Anh ấy sắp đi du học nước ngoài."}],
    "hsk4_360": [{"chinese": "公司发了奖金。", "pinyin": "Gōngsī fāle jiǎngjīn.", "meaningVi": "Công ty đã phát tiền thưởng."}],
    "hsk4_361": [{"chinese": "她获得了奖学金。", "pinyin": "Tā huòdéle jiǎngxuéjīn.", "meaningVi": "Cô ấy đã nhận được học bổng."}],
    "hsk4_362": [{"chinese": "价格降了不少。", "pinyin": "Jiàgé jiàngle bù shǎo.", "meaningVi": "Giá đã giảm đi khá nhiều."}],
    "hsk4_363": [{"chinese": "请降低音量。", "pinyin": "Qǐng jiàngdī yīnliàng.", "meaningVi": "Xin hãy giảm âm lượng."}],
    "hsk4_364": [{"chinese": "这款手机降价了。", "pinyin": "Zhè kuǎn shǒujī jiàngjià le.", "meaningVi": "Mẫu điện thoại này đã giảm giá."}],
    "hsk4_365": [{"chinese": "飞机马上就要降落了。", "pinyin": "Fēijī mǎshàng jiù yào jiàngluò le.", "meaningVi": "Máy bay sắp hạ cánh rồi."}],
    "hsk4_366": [{"chinese": "明天开始降温。", "pinyin": "Míngtiān kāishǐ jiàngwēn.", "meaningVi": "Bắt đầu từ ngày mai nhiệt độ sẽ giảm."}],
    "hsk4_369": [{"chinese": "交警在路口指挥交通。", "pinyin": "Jiāojǐng zài lùkǒu zhǐhuī jiāotōng.", "meaningVi": "Cảnh sát giao thông đang chỉ huy giao thông ở ngã tư."}],
    "hsk4_370": [{"chinese": "我们经常用中文交流。", "pinyin": "Wǒmen jīngcháng yòng Zhōngwén jiāoliú.", "meaningVi": "Chúng tôi thường giao lưu bằng tiếng Trung."}],
    "hsk4_371": [{"chinese": "他们住在郊区。", "pinyin": "Tāmen zhù zài jiāoqū.", "meaningVi": "Họ sống ở ngoại ô."}],
    "hsk4_372": [{"chinese": "这个城市的交通很方便。", "pinyin": "Zhège chéngshì de jiāotōng hěn fāngbiàn.", "meaningVi": "Giao thông của thành phố này rất thuận tiện."}],
    "hsk4_373": [{"chinese": "他是我们的篮球教练。", "pinyin": "Tā shì wǒmen de lánqiú jiàoliàn.", "meaningVi": "Anh ấy là huấn luyện viên bóng rổ của chúng tôi."}],
    "hsk4_374": [{"chinese": "她的理想是当一名教师。", "pinyin": "Tā de lǐxiǎng shì dāng yì míng jiàoshī.", "meaningVi": "Ước mơ của cô ấy là trở thành giáo viên."}],
    "hsk4_375": [{"chinese": "这位教授很有名。", "pinyin": "Zhè wèi jiàoshòu hěn yǒumíng.", "meaningVi": "Vị giáo sư này rất nổi tiếng."}],
    "hsk4_376": [{"chinese": "他的教学方法很有效。", "pinyin": "Tā de jiàoxué fāngfǎ hěn yǒuxiào.", "meaningVi": "Phương pháp giảng dạy của anh ấy rất hiệu quả."}],
    "hsk4_378": [{"chinese": "这种植物叫作仙人掌。", "pinyin": "Zhè zhǒng zhíwù jiàozuò xiānrénzhǎng.", "meaningVi": "Loại thực vật này được gọi là xương rồng."}],
    "hsk4_379": [{"chinese": "街道两旁都是商店。", "pinyin": "Jiēdào liǎngpáng dōu shì shāngdiàn.", "meaningVi": "Hai bên đường phố đều là cửa hàng."}],
    "hsk4_380": [{"chinese": "他接受了我的建议。", "pinyin": "Tā jiēshòule wǒ de jiànyì.", "meaningVi": "Anh ấy đã chấp nhận đề nghị của tôi."}],
    "hsk4_383": [{"chinese": "节假日期间火车票很难买。", "pinyin": "Jiéjiàrì qījiān huǒchēpiào hěn nán mǎi.", "meaningVi": "Trong dịp lễ Tết vé tàu rất khó mua."}],
    "hsk4_384": [{"chinese": "我们要节约用水。", "pinyin": "Wǒmen yào jiéyuē yòng shuǐ.", "meaningVi": "Chúng ta phải tiết kiệm nước."}],
    "hsk4_385": [{"chinese": "服务员，请结账。", "pinyin": "Fúwùyuán, qǐng jiézhàng.", "meaningVi": "Phục vụ ơi, xin thanh toán."}],
    "hsk4_386": [{"chinese": "他向我解释了原因。", "pinyin": "Tā xiàng wǒ jiěshìle yuányīn.", "meaningVi": "Anh ấy đã giải thích lý do cho tôi."}],
    "hsk4_387": [{"chinese": "今后我会更加努力。", "pinyin": "Jīnhòu wǒ huì gèngjiā nǔlì.", "meaningVi": "Từ nay về sau tôi sẽ càng nỗ lực hơn."}],
    "hsk4_388": [{"chinese": "参加考试的仅十人。", "pinyin": "Cānjiā kǎoshì de jǐn shí rén.", "meaningVi": "Người tham gia kỳ thi chỉ có mười người."}],
    "hsk4_390": [{"chinese": "这仅仅是个开始。", "pinyin": "Zhè jǐnjǐn shì gè kāishǐ.", "meaningVi": "Đây chỉ mới là bắt đầu."}],
    "hsk4_391": [{"chinese": "考试前他很紧张。", "pinyin": "Kǎoshì qián tā hěn jǐnzhāng.", "meaningVi": "Trước kỳ thi anh ấy rất căng thẳng."}],
    "hsk4_392": [{"chinese": "请大家有序进入会场。", "pinyin": "Qǐng dàjiā yǒuxù jìnrù huìchǎng.", "meaningVi": "Mời mọi người vào hội trường một cách trật tự."}],
    "hsk4_393": [{"chinese": "会议正在进行。", "pinyin": "Huìyì zhèngzài jìnxíng.", "meaningVi": "Cuộc họp đang được tiến hành."}],
    "hsk4_394": [{"chinese": "此处禁止停车。", "pinyin": "Cǐchù jìnzhǐ tíngchē.", "meaningVi": "Nơi đây cấm đỗ xe."}],
    "hsk4_395": [{"chinese": "这场比赛非常精彩。", "pinyin": "Zhè chǎng bǐsài fēicháng jīngcǎi.", "meaningVi": "Trận đấu này vô cùng hấp dẫn."}],
    "hsk4_397": [{"chinese": "他喜欢看京剧。", "pinyin": "Tā xǐhuan kàn jīngjù.", "meaningVi": "Anh ấy thích xem kinh kịch."}],
    "hsk4_399": [{"chinese": "他有丰富的工作经验。", "pinyin": "Tā yǒu fēngfù de gōngzuò jīngyàn.", "meaningVi": "Anh ấy có kinh nghiệm làm việc phong phú."}],
    "hsk4_400": [{"chinese": "警察正在调查这起事故。", "pinyin": "Jǐngchá zhèngzài diàochá zhè qǐ shìgù.", "meaningVi": "Cảnh sát đang điều tra vụ tai nạn này."}],
    "hsk4_401": [{"chinese": "这是一个著名的景点。", "pinyin": "Zhè shì yí gè zhùmíng de jǐngdiǎn.", "meaningVi": "Đây là một điểm du lịch nổi tiếng."}],
    "hsk4_402": [{"chinese": "这个景区门票很贵。", "pinyin": "Zhège jǐngqū ménpiào hěn guì.", "meaningVi": "Vé vào khu du lịch này rất đắt."}],
    "hsk4_403": [{"chinese": "山上的景色很美。", "pinyin": "Shān shàng de jǐngsè hěn měi.", "meaningVi": "Phong cảnh trên núi rất đẹp."}],
    "hsk4_404": [{"chinese": "他竟然忘记了我的生日。", "pinyin": "Tā jìngrán wàngjìle wǒ de shēngrì.", "meaningVi": "Anh ấy không ngờ lại quên mất sinh nhật của tôi."}],
    "hsk4_405": [{"chinese": "这个行业竞争很激烈。", "pinyin": "Zhège hángyè jìngzhēng hěn jīliè.", "meaningVi": "Ngành này cạnh tranh rất khốc liệt."}],
    "hsk4_406": [{"chinese": "她照了照镜子。", "pinyin": "Tā zhàole zhào jìngzi.", "meaningVi": "Cô ấy soi gương một chút."}],
    "hsk4_409": [{"chinese": "请大家举手。", "pinyin": "Qǐng dàjiā jǔshǒu.", "meaningVi": "Mời mọi người giơ tay."}],
    "hsk4_410": [{"chinese": "学校举办了运动会。", "pinyin": "Xuéxiào jǔbànle yùndònghuì.", "meaningVi": "Nhà trường đã tổ chức đại hội thể thao."}],
    "hsk4_411": [{"chinese": "老师举例说明这个语法。", "pinyin": "Lǎoshī jǔlì shuōmíng zhège yǔfǎ.", "meaningVi": "Giáo viên đưa ví dụ để giải thích ngữ pháp này."}],
    "hsk4_412": [{"chinese": "婚礼将在下周举行。", "pinyin": "Hūnlǐ jiāng zài xiàzhōu jǔxíng.", "meaningVi": "Đám cưới sẽ được tổ chức vào tuần sau."}],
    "hsk4_413": [{"chinese": "我们周末聚一聚吧。", "pinyin": "Wǒmen zhōumò jù yi jù ba.", "meaningVi": "Cuối tuần chúng ta tụ họp một chút đi."}],
    "hsk4_414": [{"chinese": "公司组织了一次聚餐。", "pinyin": "Gōngsī zǔzhīle yí cì jùcān.", "meaningVi": "Công ty đã tổ chức một buổi liên hoan."}],
    "hsk4_416": [{"chinese": "他拒绝了我的邀请。", "pinyin": "Tā jùjuéle wǒ de yāoqǐng.", "meaningVi": "Anh ấy đã từ chối lời mời của tôi."}],
    "hsk4_418": [{"chinese": "我们去剧院看戏。", "pinyin": "Wǒmen qù jùyuàn kàn xì.", "meaningVi": "Chúng tôi đi nhà hát xem kịch."}],
    "hsk4_419": [{"chinese": "别生气，我只是开玩笑。", "pinyin": "Bié shēngqì, wǒ zhǐshì kāi wánxiào.", "meaningVi": "Đừng giận, tôi chỉ đùa thôi."}],
    "hsk4_420": [{"chinese": "你对这件事有什么看法？", "pinyin": "Nǐ duì zhè jiàn shì yǒu shénme kànfǎ?", "meaningVi": "Bạn có quan điểm gì về việc này?"}],
    "hsk4_421": [{"chinese": "我们今晚烤肉吃。", "pinyin": "Wǒmen jīnwǎn kǎoròu chī.", "meaningVi": "Tối nay chúng ta nướng thịt ăn."}],
    "hsk4_422": [{"chinese": "我需要考虑一下。", "pinyin": "Wǒ xūyào kǎolǜ yíxià.", "meaningVi": "Tôi cần suy nghĩ một chút."}],
    "hsk4_423": [{"chinese": "今年的考生人数增加了。", "pinyin": "Jīnnián de kǎoshēng rénshù zēngjiā le.", "meaningVi": "Số lượng thí sinh năm nay đã tăng lên."}],
    "hsk4_424": [{"chinese": "路边种着几棵柳树。", "pinyin": "Lù biān zhòngzhe jǐ kē liǔshù.", "meaningVi": "Bên đường trồng vài cây liễu."}],
    "hsk4_425": [{"chinese": "现代科技发展很快。", "pinyin": "Xiàndài kējì fāzhǎn hěn kuài.", "meaningVi": "Khoa học kỹ thuật hiện đại phát triển rất nhanh."}],
    "hsk4_427": [{"chinese": "他咳了几声。", "pinyin": "Tā kéle jǐ shēng.", "meaningVi": "Anh ấy ho vài tiếng."}],
    "hsk4_428": [{"chinese": "我最近老是咳嗽。", "pinyin": "Wǒ zuìjìn lǎoshì késou.", "meaningVi": "Gần đây tôi cứ ho mãi."}],
    "hsk4_429": [{"chinese": "没能参加，真可惜。", "pinyin": "Méi néng cānjiā, zhēn kěxī.", "meaningVi": "Không thể tham gia được, thật đáng tiếc."}],
    "hsk4_430": [{"chinese": "这袋盐重五百克。", "pinyin": "Zhè dài yán zhòng wǔbǎi kè.", "meaningVi": "Túi muối này nặng năm trăm gam."}],
    "hsk4_431": [{"chinese": "这门课程很有意思。", "pinyin": "Zhè mén kèchéng hěn yǒu yìsi.", "meaningVi": "Khóa học này rất thú vị."}],
    "hsk4_433": [{"chinese": "课堂上大家都很认真。", "pinyin": "Kètáng shàng dàjiā dōu hěn rènzhēn.", "meaningVi": "Trong lớp học mọi người đều rất nghiêm túc."}],
    "hsk4_434": [{"chinese": "客厅里放着一张沙发。", "pinyin": "Kètīng lǐ fàngzhe yì zhāng shāfā.", "meaningVi": "Trong phòng khách đặt một chiếc sofa."}],
    "hsk4_437": [{"chinese": "这里的空气很新鲜。", "pinyin": "Zhèlǐ de kōngqì hěn xīnxiān.", "meaningVi": "Không khí ở đây rất trong lành."}],
    "hsk4_440": [{"chinese": "他的口语说得很流利。", "pinyin": "Tā de kǒuyǔ shuō de hěn liúlì.", "meaningVi": "Khẩu ngữ của anh ấy nói rất trôi chảy."}],
    "hsk4_441": [{"chinese": "这个药很苦。", "pinyin": "Zhège yào hěn kǔ.", "meaningVi": "Loại thuốc này rất đắng."}],
    "hsk4_442": [{"chinese": "他经常吃快餐。", "pinyin": "Tā jīngcháng chī kuàicān.", "meaningVi": "Anh ấy thường ăn đồ ăn nhanh."}],
    "hsk4_443": [{"chinese": "我的快递到了吗？", "pinyin": "Wǒ de kuàidì dào le ma?", "meaningVi": "Bưu kiện chuyển phát nhanh của tôi đến chưa?"}],
    "hsk4_444": [{"chinese": "他快速地跑了过去。", "pinyin": "Tā kuàisù de pǎole guòqù.", "meaningVi": "Anh ấy nhanh chóng chạy qua."}],
    "hsk4_447": [{"chinese": "请帮我拉一下门。", "pinyin": "Qǐng bāng wǒ lā yíxià mén.", "meaningVi": "Xin giúp tôi kéo cửa một chút."}],
    "hsk4_448": [{"chinese": "请把垃圾扔进垃圾桶。", "pinyin": "Qǐng bǎ lājī rēng jìn lājītǒng.", "meaningVi": "Xin hãy vứt rác vào thùng rác."}],
    "hsk4_449": [{"chinese": "这道菜太辣了。", "pinyin": "Zhè dào cài tài là le.", "meaningVi": "Món ăn này quá cay."}],
    "hsk4_450": [{"chinese": "快点，不然就来不及了。", "pinyin": "Kuài diǎn, bùrán jiù láibují le.", "meaningVi": "Nhanh lên, nếu không thì sẽ không kịp đâu."}],
    "hsk4_451": [{"chinese": "现在出发还来得及。", "pinyin": "Xiànzài chūfā hái láidejí.", "meaningVi": "Bây giờ xuất phát vẫn còn kịp."}],
    "hsk4_452": [{"chinese": "他今天有点懒，不想出门。", "pinyin": "Tā jīntiān yǒudiǎn lǎn, bù xiǎng chūmén.", "meaningVi": "Hôm nay anh ấy hơi lười, không muốn ra ngoài."}],
    "hsk4_453": [{"chinese": "不要浪费时间。", "pinyin": "Búyào làngfèi shíjiān.", "meaningVi": "Đừng lãng phí thời gian."}],
    "hsk4_454": [{"chinese": "这是一个浪漫的城市。", "pinyin": "Zhè shì yí gè làngmàn de chéngshì.", "meaningVi": "Đây là một thành phố lãng mạn."}],
    "hsk4_455": [{"chinese": "动物园里有一只老虎。", "pinyin": "Dòngwùyuán lǐ yǒu yì zhī lǎohǔ.", "meaningVi": "Trong sở thú có một con hổ."}],
    "hsk4_456": [{"chinese": "我打算回老家过年。", "pinyin": "Wǒ dǎsuàn huí lǎojiā guònián.", "meaningVi": "Tôi định về quê ăn Tết."}],
    "hsk4_457": [{"chinese": "政府很关心老年人的生活。", "pinyin": "Zhèngfǔ hěn guānxīn lǎonián rén de shēnghuó.", "meaningVi": "Chính phủ rất quan tâm đến cuộc sống của người cao tuổi."}],
    "hsk4_458": [{"chinese": "他老是迟到。", "pinyin": "Tā lǎoshì chídào.", "meaningVi": "Anh ấy luôn luôn đến muộn."}],
    "hsk4_459": [{"chinese": "遇到问题要冷静。", "pinyin": "Yùdào wèntí yào lěngjìng.", "meaningVi": "Gặp vấn đề phải bình tĩnh."}],
    "hsk4_460": [{"chinese": "我明天要去理发。", "pinyin": "Wǒ míngtiān yào qù lǐfà.", "meaningVi": "Ngày mai tôi phải đi cắt tóc."}],
    "hsk4_461": [{"chinese": "我完全理解你的意思。", "pinyin": "Wǒ wánquán lǐjiě nǐ de yìsi.", "meaningVi": "Tôi hoàn toàn hiểu ý của bạn."}],
    "hsk4_464": [{"chinese": "他打篮球打得很厉害。", "pinyin": "Tā dǎ lánqiú dǎ de hěn lìhai.", "meaningVi": "Anh ấy chơi bóng rổ rất giỏi."}],
    "hsk4_465": [{"chinese": "搬这张桌子需要点力气。", "pinyin": "Bān zhè zhāng zhuōzi xūyào diǎn lìqi.", "meaningVi": "Khiêng cái bàn này cần chút sức lực."}],
    "hsk4_466": [{"chinese": "我喜欢很多运动，例如游泳和跑步。", "pinyin": "Wǒ xǐhuan hěn duō yùndòng, lìrú yóuyǒng hé pǎobù.", "meaningVi": "Tôi thích nhiều môn thể thao, ví dụ như bơi lội và chạy bộ."}],
    "hsk4_467": [{"chinese": "请举一个例子。", "pinyin": "Qǐng jǔ yí gè lìzi.", "meaningVi": "Xin hãy đưa ra một ví dụ."}],
    "hsk4_468": [{"chinese": "我们俩是好朋友。", "pinyin": "Wǒmen liǎ shì hǎo péngyou.", "meaningVi": "Hai chúng tôi là bạn tốt."}],
    "hsk4_470": [{"chinese": "有事请随时联系我。", "pinyin": "Yǒu shì qǐng suíshí liánxì wǒ.", "meaningVi": "Có việc gì xin liên lạc với tôi bất cứ lúc nào."}],
    "hsk4_471": [{"chinese": "今天天气有点凉。", "pinyin": "Jīntiān tiānqì yǒudiǎn liáng.", "meaningVi": "Hôm nay thời tiết hơi mát."}],
    "hsk4_473": [{"chinese": "我买了两本书。", "pinyin": "Wǒ mǎile liǎng běn shū.", "meaningVi": "Tôi đã mua hai cuốn sách."}],
    "hsk4_476": [{"chinese": "今天气温零下五度。", "pinyin": "Jīntiān qìwēn líng xià wǔ dù.", "meaningVi": "Hôm nay nhiệt độ dưới không năm độ."}],
    "hsk4_477": [{"chinese": "妈妈每周给我零花钱。", "pinyin": "Māma měi zhōu gěi wǒ línghuāqián.", "meaningVi": "Mỗi tuần mẹ cho tôi tiền tiêu vặt."}],
    "hsk4_478": [{"chinese": "你有零钱吗？", "pinyin": "Nǐ yǒu língqián ma?", "meaningVi": "Bạn có tiền lẻ không?"}],
    "hsk4_479": [{"chinese": "小孩子都喜欢吃零食。", "pinyin": "Xiǎo háizi dōu xǐhuan chī língshí.", "meaningVi": "Trẻ con đều thích ăn đồ ăn vặt."}],
    "hsk4_482": [{"chinese": "他决定留在北京工作。", "pinyin": "Tā juédìng liú zài Běijīng gōngzuò.", "meaningVi": "Anh ấy quyết định ở lại Bắc Kinh làm việc."}],
    "hsk4_483": [{"chinese": "河水慢慢地流着。", "pinyin": "Héshuǐ mànmàn de liúzhe.", "meaningVi": "Nước sông chảy chầm chậm."}],
    "hsk4_484": [{"chinese": "她法语说得很流利。", "pinyin": "Tā Fǎyǔ shuō de hěn liúlì.", "meaningVi": "Cô ấy nói tiếng Pháp rất trôi chảy."}],
    "hsk4_485": [{"chinese": "他给我留下了深刻的印象。", "pinyin": "Tā gěi wǒ liúxiàle shēnkè de yìnxiàng.", "meaningVi": "Anh ấy để lại cho tôi ấn tượng sâu sắc."}],
    "hsk4_486": [{"chinese": "这种发型现在很流行。", "pinyin": "Zhè zhǒng fàxíng xiànzài hěn liúxíng.", "meaningVi": "Kiểu tóc này bây giờ rất thịnh hành."}],
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
