"""P5.10.3 (continued) -- Batch 005 (continues immediately after
examples_batch_004.json; spans the tail of HSK2's eligible pool into
the start of HSK3's).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Usage:
    python generate_examples_batch_005.py --dry-run
    python generate_examples_batch_005.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 5
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_005.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk2_170": [{"chinese": "我爷爷今年七十岁了。", "pinyin": "Wǒ yéye jīnnián qīshí suì le.", "meaningVi": "Ông nội tôi năm nay bảy mươi tuổi rồi."}],
    "hsk2_183": [{"chinese": "河里有很多鱼。", "pinyin": "Hé lǐ yǒu hěn duō yú.", "meaningVi": "Trong sông có rất nhiều cá."}],
    "hsk2_184": [{"chinese": "我家离学校很远。", "pinyin": "Wǒ jiā lí xuéxiào hěn yuǎn.", "meaningVi": "Nhà tôi cách trường rất xa."}],
    "hsk2_187": [{"chinese": "她丈夫是医生。", "pinyin": "Tā zhàngfu shì yīshēng.", "meaningVi": "Chồng cô ấy là bác sĩ."}],
    "hsk2_197": [{"chinese": "他每周都踢足球。", "pinyin": "Tā měi zhōu dōu tī zúqiú.", "meaningVi": "Anh ấy đá bóng mỗi tuần."}],
    "hsk3_011": [{"chinese": "我们得想个办法。", "pinyin": "Wǒmen děi xiǎng gè bànfǎ.", "meaningVi": "Chúng ta phải nghĩ ra cách nào đó."}],
    "hsk3_012": [{"chinese": "他在办公室工作。", "pinyin": "Tā zài bàngōngshì gōngzuò.", "meaningVi": "Anh ấy làm việc trong văn phòng."}],
    "hsk3_013": [{"chinese": "我等了他半天。", "pinyin": "Wǒ děngle tā bàntiān.", "meaningVi": "Tôi đã đợi anh ấy rất lâu."}],
    "hsk3_014": [{"chinese": "他经常帮助别人。", "pinyin": "Tā jīngcháng bāngzhù biérén.", "meaningVi": "Anh ấy thường xuyên giúp đỡ người khác."}],
    "hsk3_015": [{"chinese": "我吃饱了。", "pinyin": "Wǒ chībǎo le.", "meaningVi": "Tôi ăn no rồi."}],
    "hsk3_016": [{"chinese": "爷爷每天看报纸。", "pinyin": "Yéye měitiān kàn bàozhǐ.", "meaningVi": "Ông nội mỗi ngày đọc báo."}],
    "hsk3_017": [{"chinese": "一直往北走就到了。", "pinyin": "Yìzhí wǎng běi zǒu jiù dào le.", "meaningVi": "Cứ đi thẳng về phía bắc là đến."}],
    "hsk3_018": [{"chinese": "北方的冬天很冷。", "pinyin": "Běifāng de dōngtiān hěn lěng.", "meaningVi": "Mùa đông ở phương Bắc rất lạnh."}],
    "hsk3_019": [{"chinese": "我的手机被偷了。", "pinyin": "Wǒ de shǒujī bèi tōu le.", "meaningVi": "Điện thoại của tôi bị mất trộm."}],
    "hsk3_020": [{"chinese": "请借我看看你的笔记。", "pinyin": "Qǐng jiè wǒ kànkan nǐ de bǐjì.", "meaningVi": "Cho tôi mượn xem ghi chép của bạn."}],
    "hsk3_022": [{"chinese": "我买了一个新笔记本电脑。", "pinyin": "Wǒ mǎile yí gè xīn bǐjìběn diànnǎo.", "meaningVi": "Tôi đã mua một chiếc máy tính xách tay mới."}],
    "hsk3_023": [{"chinese": "我喜欢很多运动，比如篮球和足球。", "pinyin": "Wǒ xǐhuan hěn duō yùndòng, bǐrú lánqiú hé zúqiú.", "meaningVi": "Tôi thích nhiều môn thể thao, ví dụ như bóng rổ và bóng đá."}],
    "hsk3_025": [{"chinese": "你必须按时完成作业。", "pinyin": "Nǐ bìxū ànshí wánchéng zuòyè.", "meaningVi": "Bạn phải hoàn thành bài tập đúng giờ."}],
    "hsk3_026": [{"chinese": "天气变冷了。", "pinyin": "Tiānqì biàn lěng le.", "meaningVi": "Thời tiết đã trở lạnh."}],
    "hsk3_027": [{"chinese": "这本书我看了三遍。", "pinyin": "Zhè běn shū wǒ kànle sān biàn.", "meaningVi": "Cuốn sách này tôi đã đọc ba lần."}],
    "hsk3_028": [{"chinese": "冰慢慢变成了水。", "pinyin": "Bīng mànmàn biànchéngle shuǐ.", "meaningVi": "Băng dần dần biến thành nước."}],
    "hsk3_030": [{"chinese": "他们在舞台上表演。", "pinyin": "Tāmen zài wǔtái shàng biǎoyǎn.", "meaningVi": "Họ đang biểu diễn trên sân khấu."}],
    "hsk3_031": [{"chinese": "你还有别的问题吗？", "pinyin": "Nǐ hái yǒu biéde wèntí ma?", "meaningVi": "Bạn còn câu hỏi nào khác không?"}],
    "hsk3_032": [{"chinese": "不要总是麻烦别人。", "pinyin": "Búyào zǒngshì máfan biérén.", "meaningVi": "Đừng luôn làm phiền người khác."}],
    "hsk3_033": [{"chinese": "我们住在这家宾馆。", "pinyin": "Wǒmen zhù zài zhè jiā bīnguǎn.", "meaningVi": "Chúng tôi ở khách sạn này."}],
    "hsk3_035": [{"chinese": "孩子们都爱吃冰激凌。", "pinyin": "Háizimen dōu ài chī bīngjīlíng.", "meaningVi": "Bọn trẻ đều thích ăn kem."}],
    "hsk3_036": [{"chinese": "牛奶放在冰箱里。", "pinyin": "Niúnǎi fàng zài bīngxiāng lǐ.", "meaningVi": "Sữa để trong tủ lạnh."}],
    "hsk3_037": [{"chinese": "医生正在照顾病人。", "pinyin": "Yīshēng zhèngzài zhàogù bìngrén.", "meaningVi": "Bác sĩ đang chăm sóc bệnh nhân."}],
    "hsk3_038": [{"chinese": "他不但聪明，而且很努力。", "pinyin": "Tā búdàn cōngming, érqiě hěn nǔlì.", "meaningVi": "Anh ấy không những thông minh, mà còn rất chăm chỉ."}],
    "hsk3_039": [{"chinese": "我的钥匙不见了。", "pinyin": "Wǒ de yàoshi bújiàn le.", "meaningVi": "Chìa khóa của tôi biến mất rồi."}],
    "hsk3_040": [{"chinese": "不用谢。", "pinyin": "Búyòng xiè.", "meaningVi": "Không cần cảm ơn."}],
    "hsk3_041": [{"chinese": "每个人的想法都不同。", "pinyin": "Měi gè rén de xiǎngfǎ dōu bù tóng.", "meaningVi": "Suy nghĩ của mỗi người đều khác nhau."}],
    "hsk3_042": [{"chinese": "他们结婚不久就有了孩子。", "pinyin": "Tāmen jiéhūn bùjiǔ jiù yǒule háizi.", "meaningVi": "Họ kết hôn chẳng bao lâu thì có con."}],
    "hsk3_044": [{"chinese": "他现在才起床。", "pinyin": "Tā xiànzài cái qǐchuáng.", "meaningVi": "Bây giờ anh ấy mới thức dậy."}],
    "hsk3_045": [{"chinese": "服务员，请给我看看菜单。", "pinyin": "Fúwùyuán, qǐng gěi wǒ kànkan càidān.", "meaningVi": "Phục vụ ơi, cho tôi xem thực đơn."}],
    "hsk3_046": [{"chinese": "我打算参加这次比赛。", "pinyin": "Wǒ dǎsuàn cānjiā zhè cì bǐsài.", "meaningVi": "Tôi định tham gia cuộc thi lần này."}],
    "hsk3_047": [{"chinese": "羊在吃草。", "pinyin": "Yáng zài chī cǎo.", "meaningVi": "Con cừu đang ăn cỏ."}],
    "hsk3_048": [{"chinese": "孩子们在草地上踢球。", "pinyin": "Háizimen zài cǎodì shàng tī qiú.", "meaningVi": "Bọn trẻ đang đá bóng trên bãi cỏ."}],
    "hsk3_049": [{"chinese": "我家住在五层。", "pinyin": "Wǒ jiā zhù zài wǔ céng.", "meaningVi": "Nhà tôi ở tầng năm."}],
    "hsk3_050": [{"chinese": "我在网上查了一下资料。", "pinyin": "Wǒ zài wǎngshàng chále yíxià zīliào.", "meaningVi": "Tôi đã tra cứu tài liệu trên mạng."}],
    "hsk3_053": [{"chinese": "你尝尝这个菜。", "pinyin": "Nǐ chángchang zhège cài.", "meaningVi": "Bạn thử món này xem."}],
    "hsk3_054": [{"chinese": "他常去图书馆看书。", "pinyin": "Tā cháng qù túshūguǎn kàn shū.", "meaningVi": "Anh ấy thường đến thư viện đọc sách."}],
    "hsk3_055": [{"chinese": "感冒是一种常见的病。", "pinyin": "Gǎnmào shì yì zhǒng cháng jiàn de bìng.", "meaningVi": "Cảm lạnh là một loại bệnh thường gặp."}],
    "hsk3_056": [{"chinese": "这是我们常用的方法。", "pinyin": "Zhè shì wǒmen cháng yòng de fāngfǎ.", "meaningVi": "Đây là phương pháp chúng tôi thường dùng."}],
    "hsk3_057": [{"chinese": "我常常和朋友一起吃饭。", "pinyin": "Wǒ chángcháng hé péngyou yìqǐ chīfàn.", "meaningVi": "Tôi thường xuyên ăn cơm cùng bạn bè."}],
    "hsk3_058": [{"chinese": "他穿了一件白衬衫。", "pinyin": "Tā chuānle yí jiàn bái chènshān.", "meaningVi": "Anh ấy mặc một chiếc áo sơ mi trắng."}],
    "hsk3_059": [{"chinese": "她的成绩一直很好。", "pinyin": "Tā de chéngjì yìzhí hěn hǎo.", "meaningVi": "Thành tích của cô ấy luôn luôn tốt."}],
    "hsk3_060": [{"chinese": "上海是一座大城市。", "pinyin": "Shànghǎi shì yí zuò dà chéngshì.", "meaningVi": "Thượng Hải là một thành phố lớn."}],
    "hsk3_061": [{"chinese": "他今天上班迟到了。", "pinyin": "Tā jīntiān shàngbān chídào le.", "meaningVi": "Hôm nay anh ấy đi làm muộn."}],
    "hsk3_062": [{"chinese": "我们明天早上出发。", "pinyin": "Wǒmen míngtiān zǎoshang chūfā.", "meaningVi": "Sáng mai chúng tôi xuất phát."}],
    "hsk3_063": [{"chinese": "他出生在北京。", "pinyin": "Tā chūshēng zài Běijīng.", "meaningVi": "Anh ấy sinh ra ở Bắc Kinh."}],
    "hsk3_064": [{"chinese": "他下周就能出院了。", "pinyin": "Tā xià zhōu jiù néng chūyuàn le.", "meaningVi": "Tuần sau anh ấy có thể xuất viện rồi."}],
    "hsk3_065": [{"chinese": "我弟弟在读初中。", "pinyin": "Wǒ dìdi zài dú chūzhōng.", "meaningVi": "Em trai tôi đang học trung học cơ sở."}],
    "hsk3_066": [{"chinese": "除了他，大家都来了。", "pinyin": "Chúle tā, dàjiā dōu lái le.", "meaningVi": "Trừ anh ấy ra, mọi người đều đến rồi."}],
    "hsk3_067": [{"chinese": "我们坐船去了那个岛。", "pinyin": "Wǒmen zuò chuán qùle nàge dǎo.", "meaningVi": "Chúng tôi đi thuyền đến hòn đảo đó."}],
    "hsk3_068": [{"chinese": "春天来了，花都开了。", "pinyin": "Chūntiān lái le, huā dōu kāi le.", "meaningVi": "Mùa xuân đến rồi, hoa đều nở."}],
    "hsk3_069": [{"chinese": "我用词典查生词。", "pinyin": "Wǒ yòng cídiǎn chá shēngcí.", "meaningVi": "Tôi dùng từ điển để tra từ mới."}],
    "hsk3_070": [{"chinese": "他是一个聪明的学生。", "pinyin": "Tā shì yí gè cōngming de xuéshēng.", "meaningVi": "Anh ấy là một học sinh thông minh."}],
    "hsk3_071": [{"chinese": "我们周末打扫房间。", "pinyin": "Wǒmen zhōumò dǎsǎo fángjiān.", "meaningVi": "Cuối tuần chúng tôi dọn dẹp phòng."}],
    "hsk3_074": [{"chinese": "这个决定要问问大人的意见。", "pinyin": "Zhège juédìng yào wènwen dàren de yìjiàn.", "meaningVi": "Quyết định này cần hỏi ý kiến của người lớn."}],
    "hsk3_075": [{"chinese": "这双鞋的大小正合适。", "pinyin": "Zhè shuāng xié de dàxiǎo zhèng héshì.", "meaningVi": "Kích thước của đôi giày này vừa vặn."}],
    "hsk3_076": [{"chinese": "大熊猫是中国的国宝。", "pinyin": "Dàxióngmāo shì Zhōngguó de guóbǎo.", "meaningVi": "Gấu trúc lớn là quốc bảo của Trung Quốc."}],
    "hsk3_077": [{"chinese": "冬天她常穿一件黑色大衣。", "pinyin": "Dōngtiān tā cháng chuān yí jiàn hēisè dàyī.", "meaningVi": "Mùa đông cô ấy thường mặc một chiếc áo khoác dài màu đen."}],
    "hsk3_079": [{"chinese": "别担心，一切都会好的。", "pinyin": "Bié dānxīn, yíqiè dōu huì hǎo de.", "meaningVi": "Đừng lo, mọi thứ sẽ ổn thôi."}],
    "hsk3_080": [{"chinese": "妈妈给我做了一个生日蛋糕。", "pinyin": "Māma gěi wǒ zuòle yí gè shēngrì dàngāo.", "meaningVi": "Mẹ đã làm cho tôi một chiếc bánh sinh nhật."}],
    "hsk3_081": [{"chinese": "“你会来吗？”“当然会。”", "pinyin": "“Nǐ huì lái ma?” “Dāngrán huì.”", "meaningVi": "'Bạn sẽ đến chứ?' 'Đương nhiên rồi.'"}],
    "hsk3_082": [{"chinese": "春节的时候到处都很热闹。", "pinyin": "Chūnjié de shíhou dàochù dōu hěn rènao.", "meaningVi": "Vào dịp Tết, khắp nơi đều rất náo nhiệt."}],
    "hsk3_084": [{"chinese": "他得到了老师的表扬。", "pinyin": "Tā dédàole lǎoshī de biǎoyáng.", "meaningVi": "Anh ấy nhận được lời khen của giáo viên."}],
    "hsk3_086": [{"chinese": "如果明天下雨的话，我们就不去了。", "pinyin": "Rúguǒ míngtiān xiàyǔ dehuà, wǒmen jiù bú qù le.", "meaningVi": "Nếu ngày mai trời mưa, chúng ta sẽ không đi nữa."}],
    "hsk3_088": [{"chinese": "请把灯关了。", "pinyin": "Qǐng bǎ dēng guān le.", "meaningVi": "Xin tắt đèn."}],
    "hsk3_090": [{"chinese": "会议地点改在三楼了。", "pinyin": "Huìyì dìdiǎn gǎi zài sān lóu le.", "meaningVi": "Địa điểm họp đã đổi sang tầng ba."}],
    "hsk3_092": [{"chinese": "请看一下地图。", "pinyin": "Qǐng kàn yíxià dìtú.", "meaningVi": "Xin xem bản đồ một chút."}],
    "hsk3_094": [{"chinese": "我们坐电梯上去吧。", "pinyin": "Wǒmen zuò diàntī shàngqù ba.", "meaningVi": "Chúng ta đi thang máy lên đi."}],
    "hsk3_095": [{"chinese": "我现在常常看电子书。", "pinyin": "Wǒ xiànzài chángcháng kàn diànzǐshū.", "meaningVi": "Bây giờ tôi thường xuyên đọc sách điện tử."}],
    "hsk3_096": [{"chinese": "他把手机丢了。", "pinyin": "Tā bǎ shǒujī diū le.", "meaningVi": "Anh ấy làm mất điện thoại rồi."}],
    "hsk3_097": [{"chinese": "太阳从东边升起。", "pinyin": "Tàiyáng cóng dōngbiān shēngqǐ.", "meaningVi": "Mặt trời mọc từ phía đông."}],
    "hsk3_098": [{"chinese": "他是中国东北人。", "pinyin": "Tā shì Zhōngguó dōngběi rén.", "meaningVi": "Anh ấy là người đông bắc Trung Quốc."}],
    "hsk3_099": [{"chinese": "这是一座具有东方特色的建筑。", "pinyin": "Zhè shì yí zuò jùyǒu dōngfāng tèsè de jiànzhù.", "meaningVi": "Đây là một công trình mang đặc sắc phương Đông."}],
    "hsk3_100": [{"chinese": "越南在中国的东南方向。", "pinyin": "Yuènán zài Zhōngguó de dōngnán fāngxiàng.", "meaningVi": "Việt Nam ở hướng đông nam của Trung Quốc."}],
    "hsk3_101": [{"chinese": "北方的冬天经常下雪。", "pinyin": "Běifāng de dōngtiān jīngcháng xiàxuě.", "meaningVi": "Mùa đông ở phương Bắc thường có tuyết rơi."}],
    "hsk3_102": [{"chinese": "他懂得怎么照顾自己。", "pinyin": "Tā dǒngde zěnme zhàogù zìjǐ.", "meaningVi": "Anh ấy biết cách chăm sóc bản thân."}],
    "hsk3_103": [{"chinese": "孩子们都喜欢小动物。", "pinyin": "Háizimen dōu xǐhuan xiǎo dòngwù.", "meaningVi": "Bọn trẻ đều thích động vật nhỏ."}],
    "hsk3_104": [{"chinese": "周末我们去动物园吧。", "pinyin": "Zhōumò wǒmen qù dòngwùyuán ba.", "meaningVi": "Cuối tuần chúng ta đi sở thú đi."}],
    "hsk3_105": [{"chinese": "这条路比较短。", "pinyin": "Zhè tiáo lù bǐjiào duǎn.", "meaningVi": "Con đường này khá ngắn."}],
    "hsk3_106": [{"chinese": "夏天他常穿短裤。", "pinyin": "Xiàtiān tā cháng chuān duǎnkù.", "meaningVi": "Mùa hè anh ấy thường mặc quần đùi."}],
    "hsk3_107": [{"chinese": "请读一下这段话。", "pinyin": "Qǐng dú yíxià zhè duàn huà.", "meaningVi": "Xin đọc đoạn văn này."}],
    "hsk3_108": [{"chinese": "每天锻炼身体对健康很好。", "pinyin": "Měitiān duànliàn shēntǐ duì jiànkāng hěn hǎo.", "meaningVi": "Tập thể dục mỗi ngày rất tốt cho sức khỏe."}],
    "hsk3_109": [{"chinese": "请听录音，跟着对话说。", "pinyin": "Qǐng tīng lùyīn, gēnzhe duìhuà shuō.", "meaningVi": "Xin nghe băng, nói theo đoạn hội thoại."}],
    "hsk3_110": [{"chinese": "我肚子饿了。", "pinyin": "Wǒ dùzi è le.", "meaningVi": "Tôi đói bụng rồi."}],
    "hsk3_111": [{"chinese": "这家饭馆便宜而且好吃。", "pinyin": "Zhè jiā fànguǎn piányi érqiě hǎochī.", "meaningVi": "Quán ăn này rẻ mà lại ngon."}],
    "hsk3_112": [{"chinese": "他的耳朵有点儿疼。", "pinyin": "Tā de ěrduo yǒudiǎnr téng.", "meaningVi": "Tai của anh ấy hơi đau."}],
    "hsk3_113": [{"chinese": "我戴上耳机听音乐。", "pinyin": "Wǒ dàishàng ěrjī tīng yīnyuè.", "meaningVi": "Tôi đeo tai nghe nghe nhạc."}],
    "hsk3_115": [{"chinese": "孩子昨晚发烧了。", "pinyin": "Háizi zuówǎn fāshāo le.", "meaningVi": "Tối qua đứa trẻ bị sốt."}],
    "hsk3_116": [{"chinese": "这里发生了一件奇怪的事。", "pinyin": "Zhèlǐ fāshēngle yí jiàn qíguài de shì.", "meaningVi": "Ở đây đã xảy ra một chuyện kỳ lạ."}],
    "hsk3_117": [{"chinese": "我发现了一个有趣的地方。", "pinyin": "Wǒ fāxiànle yí gè yǒuqù de dìfang.", "meaningVi": "Tôi đã phát hiện ra một nơi thú vị."}],
    "hsk3_118": [{"chinese": "这个城市发展得很快。", "pinyin": "Zhège chéngshì fāzhǎn de hěn kuài.", "meaningVi": "Thành phố này phát triển rất nhanh."}],
    "hsk3_119": [{"chinese": "网上购物很方便。", "pinyin": "Wǎngshàng gòuwù hěn fāngbiàn.", "meaningVi": "Mua sắm trực tuyến rất tiện lợi."}],
    "hsk3_120": [{"chinese": "我饿了，先吃碗方便面吧。", "pinyin": "Wǒ è le, xiān chī wǎn fāngbiànmiàn ba.", "meaningVi": "Tôi đói rồi, ăn tạm bát mì ăn liền trước đã."}],
    "hsk3_121": [{"chinese": "这是学习汉语的好方法。", "pinyin": "Zhè shì xuéxí Hànyǔ de hǎo fāngfǎ.", "meaningVi": "Đây là phương pháp tốt để học tiếng Trung."}],
    "hsk3_122": [{"chinese": "我们走错方向了。", "pinyin": "Wǒmen zǒucuò fāngxiàng le.", "meaningVi": "Chúng ta đi sai hướng rồi."}],
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
