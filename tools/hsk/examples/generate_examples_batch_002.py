"""P5.10.3 -- Batch 002 (records 101-200 of the 5300 remaining after the
P5.10.2 pilot).

Same honesty note as generate_hsk_examples_p102.py: record SELECTION
(via queue_lib_p103.get_next_batch_ids) is deterministic; example
CONTENT below was authored directly by this assistant (LLM), not by a
separate reproducible algorithm.

Usage:
    python generate_examples_batch_002.py --dry-run
    python generate_examples_batch_002.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 2
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_002.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk1_007": [
        {"chinese": "现在是三点半。", "pinyin": "Xiànzài shì sān diǎn bàn.", "meaningVi": "Bây giờ là ba giờ rưỡi."},
        {"chinese": "我只吃了半个苹果。", "pinyin": "Wǒ zhǐ chīle bàn gè píngguǒ.", "meaningVi": "Tôi chỉ ăn nửa quả táo."},
    ],
    "hsk1_008": [
        {"chinese": "妈妈买了很多包子。", "pinyin": "Māma mǎile hěn duō bāozi.", "meaningVi": "Mẹ mua rất nhiều bánh bao."},
        {"chinese": "这家店的包子很好吃。", "pinyin": "Zhè jiā diàn de bāozi hěn hǎochī.", "meaningVi": "Bánh bao của cửa hàng này rất ngon."},
    ],
    "hsk1_009": [
        {"chinese": "请把杯子放在桌子上。", "pinyin": "Qǐng bǎ bēizi fàng zài zhuōzi shàng.", "meaningVi": "Xin đặt cốc lên bàn."},
        {"chinese": "这个杯子是我的。", "pinyin": "Zhège bēizi shì wǒ de.", "meaningVi": "Cái cốc này là của tôi."},
    ],
    "hsk1_010": [
        {"chinese": "我买了三本书。", "pinyin": "Wǒ mǎile sān běn shū.", "meaningVi": "Tôi đã mua ba cuốn sách."},
    ],
    "hsk1_013": [
        {"chinese": "我不喜欢喝咖啡。", "pinyin": "Wǒ bù xǐhuan hē kāfēi.", "meaningVi": "Tôi không thích uống cà phê."},
        {"chinese": "他今天不来了。", "pinyin": "Tā jīntiān bù lái le.", "meaningVi": "Hôm nay anh ấy không đến nữa."},
    ],
    "hsk1_014": [
        {"chinese": "“谢谢你。”“不客气。”", "pinyin": "“Xièxie nǐ.” “Bú kèqi.”", "meaningVi": "'Cảm ơn bạn.' 'Không có gì.'"},
    ],
    "hsk1_015": [
        {"chinese": "不要迟到。", "pinyin": "Búyào chídào.", "meaningVi": "Đừng đến muộn."},
        {"chinese": "我不要这个，我要那个。", "pinyin": "Wǒ búyào zhège, wǒ yào nàge.", "meaningVi": "Tôi không muốn cái này, tôi muốn cái kia."},
    ],
    "hsk1_016": [
        {"chinese": "这个菜很好吃。", "pinyin": "Zhège cài hěn hǎochī.", "meaningVi": "Món ăn này rất ngon."},
        {"chinese": "妈妈在厨房做菜。", "pinyin": "Māma zài chúfáng zuò cài.", "meaningVi": "Mẹ đang nấu ăn trong bếp."},
    ],
    "hsk1_017": [
        {"chinese": "我喜欢喝茶。", "pinyin": "Wǒ xǐhuan hē chá.", "meaningVi": "Tôi thích uống trà."},
    ],
    "hsk1_018": [
        {"chinese": "她唱歌唱得很好。", "pinyin": "Tā chàng gē chàng de hěn hǎo.", "meaningVi": "Cô ấy hát rất hay."},
        {"chinese": "我们一起唱这首歌吧。", "pinyin": "Wǒmen yìqǐ chàng zhè shǒu gē ba.", "meaningVi": "Chúng ta cùng hát bài này đi."},
    ],
    "hsk1_019": [
        {"chinese": "我要去超市买东西。", "pinyin": "Wǒ yào qù chāoshì mǎi dōngxi.", "meaningVi": "Tôi muốn đi siêu thị mua đồ."},
    ],
    "hsk1_020": [
        {"chinese": "这辆车是新的。", "pinyin": "Zhè liàng chē shì xīn de.", "meaningVi": "Chiếc xe này là mới."},
    ],
    "hsk1_021": [
        {"chinese": "我们一起吃饭吧。", "pinyin": "Wǒmen yìqǐ chīfàn ba.", "meaningVi": "Chúng ta cùng ăn cơm đi."},
        {"chinese": "他喜欢吃水果。", "pinyin": "Tā xǐhuan chī shuǐguǒ.", "meaningVi": "Anh ấy thích ăn hoa quả."},
    ],
    "hsk1_022": [
        {"chinese": "我们坐出租车去机场吧。", "pinyin": "Wǒmen zuò chūzūchē qù jīchǎng ba.", "meaningVi": "Chúng ta đi taxi ra sân bay đi."},
    ],
    "hsk1_023": [
        {"chinese": "今天很冷，多穿点衣服。", "pinyin": "Jīntiān hěn lěng, duō chuān diǎn yīfu.", "meaningVi": "Hôm nay rất lạnh, mặc thêm quần áo đi."},
        {"chinese": "她穿了一条红色的裙子。", "pinyin": "Tā chuānle yì tiáo hóngsè de qúnzi.", "meaningVi": "Cô ấy mặc một chiếc váy màu đỏ."},
    ],
    "hsk1_024": [
        {"chinese": "我给妈妈打电话。", "pinyin": "Wǒ gěi māma dǎ diànhuà.", "meaningVi": "Tôi gọi điện thoại cho mẹ."},
    ],
    "hsk1_025": [
        {"chinese": "这个房间很大。", "pinyin": "Zhège fángjiān hěn dà.", "meaningVi": "Căn phòng này rất rộng."},
        {"chinese": "他比我大两岁。", "pinyin": "Tā bǐ wǒ dà liǎng suì.", "meaningVi": "Anh ấy lớn hơn tôi hai tuổi."},
    ],
    "hsk1_026": [
        {"chinese": "大家好！", "pinyin": "Dàjiā hǎo!", "meaningVi": "Xin chào mọi người!"},
        {"chinese": "大家都很喜欢这个电影。", "pinyin": "Dàjiā dōu hěn xǐhuan zhège diànyǐng.", "meaningVi": "Mọi người đều rất thích bộ phim này."},
    ],
    "hsk1_027": [
        {"chinese": "他是北京大学的学生。", "pinyin": "Tā shì Běijīng Dàxué de xuéshēng.", "meaningVi": "Anh ấy là sinh viên của Đại học Bắc Kinh."},
    ],
    "hsk1_028": [
        {"chinese": "我姐姐是大学生。", "pinyin": "Wǒ jiějie shì dàxuéshēng.", "meaningVi": "Chị tôi là sinh viên đại học."},
    ],
    "hsk1_029": [
        {"chinese": "我们到北京了。", "pinyin": "Wǒmen dào Běijīng le.", "meaningVi": "Chúng tôi đã đến Bắc Kinh."},
        {"chinese": "从这儿到学校要走十分钟。", "pinyin": "Cóng zhèr dào xuéxiào yào zǒu shí fēnzhōng.", "meaningVi": "Từ đây đến trường phải đi mười phút."},
    ],
    "hsk1_030": [
        {"chinese": "这是我的书。", "pinyin": "Zhè shì wǒ de shū.", "meaningVi": "Đây là sách của tôi."},
    ],
    "hsk1_031": [
        {"chinese": "今天是我第一次来中国。", "pinyin": "Jīntiān shì wǒ dì-yī cì lái Zhōngguó.", "meaningVi": "Hôm nay là lần đầu tiên tôi đến Trung Quốc."},
    ],
    "hsk1_032": [
        {"chinese": "我弟弟今年八岁。", "pinyin": "Wǒ dìdi jīnnián bā suì.", "meaningVi": "Em trai tôi năm nay tám tuổi."},
    ],
    "hsk1_033": [
        {"chinese": "现在几点了？", "pinyin": "Xiànzài jǐ diǎn le?", "meaningVi": "Bây giờ là mấy giờ?"},
        {"chinese": "请给我一点水。", "pinyin": "Qǐng gěi wǒ yìdiǎn shuǐ.", "meaningVi": "Xin cho tôi một chút nước."},
    ],
    "hsk1_034": [
        {"chinese": "这家店卖衣服。", "pinyin": "Zhè jiā diàn mài yīfu.", "meaningVi": "Cửa hàng này bán quần áo."},
    ],
    "hsk1_035": [
        {"chinese": "我的电话号码是一二三。", "pinyin": "Wǒ de diànhuà hàomǎ shì yī èr sān.", "meaningVi": "Số điện thoại của tôi là một hai ba."},
        {"chinese": "他正在打电话。", "pinyin": "Tā zhèngzài dǎ diànhuà.", "meaningVi": "Anh ấy đang gọi điện thoại."},
    ],
    "hsk1_036": [
        {"chinese": "我的电脑坏了。", "pinyin": "Wǒ de diànnǎo huài le.", "meaningVi": "Máy tính của tôi bị hỏng rồi."},
    ],
    "hsk1_037": [
        {"chinese": "我们晚上看电视吧。", "pinyin": "Wǒmen wǎnshang kàn diànshì ba.", "meaningVi": "Tối nay chúng ta xem tivi đi."},
    ],
    "hsk1_038": [
        {"chinese": "我们去看电影吧。", "pinyin": "Wǒmen qù kàn diànyǐng ba.", "meaningVi": "Chúng ta đi xem phim đi."},
    ],
    "hsk1_039": [
        {"chinese": "电影院离我家很近。", "pinyin": "Diànyǐngyuàn lí wǒ jiā hěn jìn.", "meaningVi": "Rạp chiếu phim rất gần nhà tôi."},
    ],
    "hsk1_040": [
        {"chinese": "你买了什么东西？", "pinyin": "Nǐ mǎile shénme dōngxi?", "meaningVi": "Bạn đã mua gì vậy?"},
    ],
    "hsk1_041": [
        {"chinese": "我们都是学生。", "pinyin": "Wǒmen dōu shì xuéshēng.", "meaningVi": "Chúng tôi đều là học sinh."},
    ],
    "hsk1_042": [
        {"chinese": "他每天读英语。", "pinyin": "Tā měitiān dú Yīngyǔ.", "meaningVi": "Mỗi ngày anh ấy đọc tiếng Anh."},
    ],
    "hsk1_043": [
        {"chinese": "他在图书馆读书。", "pinyin": "Tā zài túshūguǎn dúshū.", "meaningVi": "Anh ấy đang đọc sách trong thư viện."},
    ],
    "hsk1_045": [
        {"chinese": "对不起，我来晚了。", "pinyin": "Duìbuqǐ, wǒ lái wǎn le.", "meaningVi": "Xin lỗi, tôi đến muộn."},
    ],
    "hsk1_047": [
        {"chinese": "这个多少钱？", "pinyin": "Zhège duōshao qián?", "meaningVi": "Cái này bao nhiêu tiền?"},
    ],
    "hsk1_048": [
        {"chinese": "他们的儿子在上大学。", "pinyin": "Tāmen de érzi zài shàng dàxué.", "meaningVi": "Con trai của họ đang học đại học."},
    ],
    "hsk1_049": [
        {"chinese": "一加一等于二。", "pinyin": "Yī jiā yī děngyú èr.", "meaningVi": "Một cộng một bằng hai."},
    ],
    "hsk1_050": [
        {"chinese": "妈妈做的饭很好吃。", "pinyin": "Māma zuò de fàn hěn hǎochī.", "meaningVi": "Cơm mẹ nấu rất ngon."},
    ],
    "hsk1_051": [
        {"chinese": "我们在饭店吃晚饭。", "pinyin": "Wǒmen zài fàndiàn chī wǎnfàn.", "meaningVi": "Chúng tôi ăn tối ở nhà hàng."},
    ],
    "hsk1_052": [
        {"chinese": "我的房间很干净。", "pinyin": "Wǒ de fángjiān hěn gānjìng.", "meaningVi": "Phòng của tôi rất sạch sẽ."},
    ],
    "hsk1_053": [
        {"chinese": "这本书非常有意思。", "pinyin": "Zhè běn shū fēicháng yǒu yìsi.", "meaningVi": "Cuốn sách này rất thú vị."},
    ],
    "hsk1_054": [
        {"chinese": "我们坐飞机去上海。", "pinyin": "Wǒmen zuò fēijī qù Shànghǎi.", "meaningVi": "Chúng tôi đi máy bay đến Thượng Hải."},
    ],
    "hsk1_056": [
        {"chinese": "请等五分钟。", "pinyin": "Qǐng děng wǔ fēnzhōng.", "meaningVi": "Xin đợi năm phút."},
    ],
    "hsk1_057": [
        {"chinese": "认识你很高兴。", "pinyin": "Rènshi nǐ hěn gāoxìng.", "meaningVi": "Rất vui được quen biết bạn."},
        {"chinese": "他今天很高兴。", "pinyin": "Tā jīntiān hěn gāoxìng.", "meaningVi": "Hôm nay anh ấy rất vui."},
    ],
    "hsk1_058": [
        {"chinese": "这是一首很好听的歌。", "pinyin": "Zhè shì yì shǒu hěn hǎotīng de gē.", "meaningVi": "Đây là một bài hát rất hay."},
    ],
    "hsk1_059": [
        {"chinese": "我哥哥在银行工作。", "pinyin": "Wǒ gēge zài yínháng gōngzuò.", "meaningVi": "Anh trai tôi làm việc ở ngân hàng."},
    ],
    "hsk1_060": [
        {"chinese": "我有一个问题。", "pinyin": "Wǒ yǒu yí gè wèntí.", "meaningVi": "Tôi có một câu hỏi."},
    ],
    "hsk1_061": [
        {"chinese": "他给了我一本书。", "pinyin": "Tā gěile wǒ yì běn shū.", "meaningVi": "Anh ấy đưa cho tôi một cuốn sách."},
    ],
    "hsk1_062": [
        {"chinese": "我在一家公司工作。", "pinyin": "Wǒ zài yì jiā gōngsī gōngzuò.", "meaningVi": "Tôi làm việc ở một công ty."},
    ],
    "hsk1_064": [
        {"chinese": "我家有一只狗。", "pinyin": "Wǒ jiā yǒu yì zhī gǒu.", "meaningVi": "Nhà tôi có một con chó."},
    ],
    "hsk1_065": [
        {"chinese": "这件衣服太贵了。", "pinyin": "Zhè jiàn yīfu tài guì le.", "meaningVi": "Chiếc áo này quá đắt."},
    ],
    "hsk1_066": [
        {"chinese": "你是哪国人？", "pinyin": "Nǐ shì nǎ guó rén?", "meaningVi": "Bạn là người nước nào?"},
    ],
    "hsk1_068": [
        {"chinese": "这个孩子很可爱。", "pinyin": "Zhège háizi hěn kě'ài.", "meaningVi": "Đứa trẻ này rất đáng yêu."},
    ],
    "hsk1_069": [
        {"chinese": "我在学习汉语。", "pinyin": "Wǒ zài xuéxí Hànyǔ.", "meaningVi": "Tôi đang học tiếng Trung."},
    ],
    "hsk1_070": [
        {"chinese": "这个汉字怎么写？", "pinyin": "Zhège Hànzì zěnme xiě?", "meaningVi": "Chữ Hán này viết thế nào?"},
    ],
    "hsk1_072": [
        {"chinese": "妈妈做的饺子很好吃。", "pinyin": "Māma zuò de jiǎozi hěn hǎochī.", "meaningVi": "Bánh chẻo mẹ làm rất ngon."},
    ],
    "hsk1_073": [
        {"chinese": "这条裙子很好看。", "pinyin": "Zhè tiáo qúnzi hěn hǎokàn.", "meaningVi": "Chiếc váy này rất đẹp."},
    ],
    "hsk1_074": [
        {"chinese": "这首歌很好听。", "pinyin": "Zhè shǒu gē hěn hǎotīng.", "meaningVi": "Bài hát này rất hay."},
    ],
    "hsk1_075": [
        {"chinese": "这个游戏很好玩儿。", "pinyin": "Zhège yóuxì hěn hǎowánr.", "meaningVi": "Trò chơi này rất thú vị."},
    ],
    "hsk1_077": [
        {"chinese": "你想喝什么？", "pinyin": "Nǐ xiǎng hē shénme?", "meaningVi": "Bạn muốn uống gì?"},
    ],
    "hsk1_079": [
        {"chinese": "今天天气很好。", "pinyin": "Jīntiān tiānqì hěn hǎo.", "meaningVi": "Hôm nay thời tiết rất đẹp."},
    ],
    "hsk1_080": [
        {"chinese": "三天后我们再见面。", "pinyin": "Sān tiān hòu wǒmen zài jiànmiàn.", "meaningVi": "Ba ngày sau chúng ta gặp lại."},
    ],
    "hsk1_081": [
        {"chinese": "我要回家了。", "pinyin": "Wǒ yào huí jiā le.", "meaningVi": "Tôi phải về nhà rồi."},
    ],
    "hsk1_082": [
        {"chinese": "我会说一点儿汉语。", "pinyin": "Wǒ huì shuō yìdiǎnr Hànyǔ.", "meaningVi": "Tôi biết nói một chút tiếng Trung."},
    ],
    "hsk1_083": [
        {"chinese": "我们坐火车去北京。", "pinyin": "Wǒmen zuò huǒchē qù Běijīng.", "meaningVi": "Chúng tôi đi tàu hỏa đến Bắc Kinh."},
    ],
    "hsk1_084": [
        {"chinese": "早上我吃了一个鸡蛋。", "pinyin": "Zǎoshang wǒ chīle yí gè jīdàn.", "meaningVi": "Buổi sáng tôi ăn một quả trứng gà."},
    ],
    "hsk1_087": [
        {"chinese": "我很想念我的家人。", "pinyin": "Wǒ hěn xiǎngniàn wǒ de jiārén.", "meaningVi": "Tôi rất nhớ gia đình mình."},
    ],
    "hsk1_088": [
        {"chinese": "我们下午三点见。", "pinyin": "Wǒmen xiàwǔ sān diǎn jiàn.", "meaningVi": "Chúng ta gặp nhau lúc ba giờ chiều."},
    ],
    "hsk1_089": [
        {"chinese": "她买了一件新衣服。", "pinyin": "Tā mǎile yí jiàn xīn yīfu.", "meaningVi": "Cô ấy đã mua một chiếc áo mới."},
    ],
    "hsk1_090": [
        {"chinese": "我们一起包饺子吧。", "pinyin": "Wǒmen yìqǐ bāo jiǎozi ba.", "meaningVi": "Chúng ta cùng gói bánh chẻo đi."},
    ],
    "hsk1_091": [
        {"chinese": "我叫王明。", "pinyin": "Wǒ jiào Wáng Míng.", "meaningVi": "Tôi tên là Vương Minh."},
    ],
    "hsk1_092": [
        {"chinese": "我姐姐是医生。", "pinyin": "Wǒ jiějie shì yīshēng.", "meaningVi": "Chị tôi là bác sĩ."},
    ],
    "hsk1_093": [
        {"chinese": "我今年二十岁。", "pinyin": "Wǒ jīnnián èrshí suì.", "meaningVi": "Năm nay tôi hai mươi tuổi."},
    ],
    "hsk1_094": [
        {"chinese": "今天是星期一。", "pinyin": "Jīntiān shì xīngqīyī.", "meaningVi": "Hôm nay là thứ Hai."},
    ],
    "hsk1_095": [
        {"chinese": "我家有九本书。", "pinyin": "Wǒ jiā yǒu jiǔ běn shū.", "meaningVi": "Nhà tôi có chín cuốn sách."},
    ],
    "hsk1_096": [
        {"chinese": "我觉得这个电影很好看。", "pinyin": "Wǒ juéde zhège diànyǐng hěn hǎokàn.", "meaningVi": "Tôi thấy bộ phim này rất hay."},
    ],
    "hsk1_097": [
        {"chinese": "请开门。", "pinyin": "Qǐng kāimén.", "meaningVi": "Xin mở cửa."},
        {"chinese": "会议九点开始。", "pinyin": "Huìyì jiǔ diǎn kāishǐ.", "meaningVi": "Cuộc họp bắt đầu lúc chín giờ."},
    ],
    "hsk1_098": [
        {"chinese": "他每天开车上班。", "pinyin": "Tā měitiān kāichē shàngbān.", "meaningVi": "Anh ấy lái xe đi làm mỗi ngày."},
    ],
    "hsk1_100": [
        {"chinese": "我要去医院看病。", "pinyin": "Wǒ yào qù yīyuàn kànbìng.", "meaningVi": "Tôi phải đi bệnh viện khám bệnh."},
    ],
    "hsk1_101": [
        {"chinese": "我看见他了。", "pinyin": "Wǒ kànjiàn tā le.", "meaningVi": "Tôi đã nhìn thấy anh ấy."},
    ],
    "hsk1_103": [
        {"chinese": "我们今天有汉语课。", "pinyin": "Wǒmen jīntiān yǒu Hànyǔ kè.", "meaningVi": "Hôm nay chúng tôi có tiết học tiếng Trung."},
    ],
    "hsk1_105": [
        {"chinese": "这个苹果三块钱。", "pinyin": "Zhège píngguǒ sān kuài qián.", "meaningVi": "Quả táo này ba đồng."},
    ],
    "hsk1_106": [
        {"chinese": "你什么时候来？", "pinyin": "Nǐ shénme shíhou lái?", "meaningVi": "Khi nào bạn đến?"},
    ],
    "hsk1_107": [
        {"chinese": "我的老师很好。", "pinyin": "Wǒ de lǎoshī hěn hǎo.", "meaningVi": "Giáo viên của tôi rất tốt."},
    ],
    "hsk1_108": [
        {"chinese": "我吃饭了。", "pinyin": "Wǒ chīfàn le.", "meaningVi": "Tôi đã ăn cơm rồi."},
    ],
    "hsk1_109": [
        {"chinese": "今天很冷。", "pinyin": "Jīntiān hěn lěng.", "meaningVi": "Hôm nay rất lạnh."},
    ],
    "hsk1_110": [
        {"chinese": "书在包里。", "pinyin": "Shū zài bāo lǐ.", "meaningVi": "Sách ở trong túi."},
    ],
    "hsk1_111": [
        {"chinese": "我要两杯咖啡。", "pinyin": "Wǒ yào liǎng bēi kāfēi.", "meaningVi": "Tôi muốn hai cốc cà phê."},
    ],
    "hsk1_112": [
        {"chinese": "我的电话号码有一个零。", "pinyin": "Wǒ de diànhuà hàomǎ yǒu yí gè líng.", "meaningVi": "Số điện thoại của tôi có một số không."},
    ],
    "hsk1_113": [
        {"chinese": "我们班有六个女生。", "pinyin": "Wǒmen bān yǒu liù gè nǚshēng.", "meaningVi": "Lớp chúng tôi có sáu nữ sinh."},
    ],
    "hsk1_114": [
        {"chinese": "我妈妈是护士。", "pinyin": "Wǒ māma shì hùshi.", "meaningVi": "Mẹ tôi là y tá."},
    ],
    "hsk1_115": [
        {"chinese": "你喜欢喝茶吗？", "pinyin": "Nǐ xǐhuan hē chá ma?", "meaningVi": "Bạn có thích uống trà không?"},
    ],
    "hsk1_116": [
        {"chinese": "我想买一件衣服。", "pinyin": "Wǒ xiǎng mǎi yí jiàn yīfu.", "meaningVi": "Tôi muốn mua một chiếc áo."},
    ],
    "hsk1_117": [
        {"chinese": "这家商店卖水果。", "pinyin": "Zhè jiā shāngdiàn mài shuǐguǒ.", "meaningVi": "Cửa hàng này bán hoa quả."},
    ],
    "hsk1_119": [
        {"chinese": "我家的猫很可爱。", "pinyin": "Wǒ jiā de māo hěn kě'ài.", "meaningVi": "Con mèo nhà tôi rất đáng yêu."},
    ],
    "hsk1_120": [
        {"chinese": "“对不起。”“没关系。”", "pinyin": "“Duìbuqǐ.” “Méi guānxi.”", "meaningVi": "'Xin lỗi.' 'Không sao.'"},
    ],
    "hsk1_121": [
        {"chinese": "你没事吧？", "pinyin": "Nǐ méishì ba?", "meaningVi": "Bạn không sao chứ?"},
    ],
    "hsk1_123": [
        {"chinese": "我妹妹在上小学。", "pinyin": "Wǒ mèimei zài shàng xiǎoxué.", "meaningVi": "Em gái tôi đang học tiểu học."},
    ],
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
              "(another batch may have already consumed some of these IDs, or the queue has drifted "
              "since this script was written) -- refusing to proceed", file=sys.stderr)
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
