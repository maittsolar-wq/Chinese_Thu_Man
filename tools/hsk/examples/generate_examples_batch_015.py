"""P5.10.3 (continued) -- Batch 015 (continues immediately after
examples_batch_014.json; entirely within HSK4). Final batch of the
011-015 five-batch execution requested by the user.

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch -- two same-pinyin-different-
character pairs, neither flagged by the mechanical tier system (it
compares the `word` string, and these are different words):
  - 吸 (xī, "to inhale/suck", as in 吸/吸引/吸烟) vs 西 (xī, "west",
    as in 西部/西红柿): identical pinyin, unrelated characters, each
    demonstrated in its own unambiguous natural compound/sentence.
  - 相 (xiāng, "mutual", as in 相比/相互/相同) vs 香 (xiāng, "fragrant"):
    identical pinyin, unrelated characters; the 香 example was
    deliberately rewritten during drafting (see below) to avoid even
    thematic closeness to the flower-fragrance example already used
    for 闻 (wén, "to smell").

Self-caught near-template revisions made during drafting (before this
batch was finalized -- not found by the validator, caught while
authoring, consistent with prior batches' integrated-QA discipline):
  - 文件 (wénjiàn): first draft "请把文件发给我。" echoed the sentence
    pattern already used for 网址 ("请把网址发给我。") two records
    earlier in this same batch -- rewritten to "这份文件很重要。".
  - 午餐 (wǔcān): first draft echoed both 晚餐's "我们一起吃X吧"
    template and would have reused the exact phrase "免费午餐" from
    提供's own example ("学校为学生提供免费午餐。") -- rewritten to
    "午餐时间到了。".
  - 咸 (xián): first draft "这个汤有点咸。" echoed 味's own example
    sentence structure ("这个汤有点怪味。") immediately above it in
    the batch -- rewritten to "我不喜欢太咸的菜。".
  - 香 (xiāng): first draft "这朵花很香。" was thematically identical
    to 闻's own example (about smelling a flower) -- rewritten to
    "妈妈做的菜很香。".

Other productive-root families kept structurally distinct (no shared
template): 提/提出/提到/提供/提前/提醒 (tí+X); 体检/体温/体重 (tǐ+X);
停/停车/停车场/停止 (tíng+X); 推/推迟/推出 (tuī+X); 网购/网页/网友/
网址 (wǎng+X); 无/无法/无聊/无论 (wú+X); 相比/相互/相同 (xiāng+X);
小吃/小伙子/小说/小组 (xiǎo+X); 修/修理 (xiū, root+derivative).

Cross-batch collision found and fixed during authoring: the first
draft of hsk4_735 (填写) reused "请填写这张表格。" verbatim from
examples_batch_009.json's hsk4_034. Rewritten to "请填写您的姓名和
电话。" before this batch was finalized; re-verified against the
full pilot+002-014 corpus with zero remaining collisions.

Usage:
    python generate_examples_batch_015.py --dry-run
    python generate_examples_batch_015.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 15
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_015.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_725": [{"chinese": "每个人都有自己的特点。", "pinyin": "Měi gè rén dōu yǒu zìjǐ de tèdiǎn.", "meaningVi": "Mỗi người đều có đặc điểm riêng của mình."}],
    "hsk4_726": [{"chinese": "他提着一个箱子。", "pinyin": "Tā tízhe yí gè xiāngzi.", "meaningVi": "Anh ấy xách một cái vali."}],
    "hsk4_727": [{"chinese": "他提出了一个新想法。", "pinyin": "Tā tíchūle yí gè xīn xiǎngfǎ.", "meaningVi": "Anh ấy đã đề xuất một ý tưởng mới."}],
    "hsk4_728": [{"chinese": "他在信里提到了这件事。", "pinyin": "Tā zài xìn lǐ tídàole zhè jiàn shì.", "meaningVi": "Anh ấy đã đề cập đến việc này trong thư."}],
    "hsk4_729": [{"chinese": "学校为学生提供免费午餐。", "pinyin": "Xuéxiào wèi xuésheng tígōng miǎnfèi wǔcān.", "meaningVi": "Nhà trường cung cấp bữa trưa miễn phí cho học sinh."}],
    "hsk4_730": [{"chinese": "我们提前到达了机场。", "pinyin": "Wǒmen tíqián dàodále jīchǎng.", "meaningVi": "Chúng tôi đã đến sân bay sớm hơn dự kiến."}],
    "hsk4_731": [{"chinese": "谢谢你提醒我。", "pinyin": "Xièxie nǐ tíxǐng wǒ.", "meaningVi": "Cảm ơn bạn đã nhắc nhở tôi."}],
    "hsk4_732": [{"chinese": "公司每年组织一次体检。", "pinyin": "Gōngsī měi nián zǔzhī yí cì tǐjiǎn.", "meaningVi": "Công ty mỗi năm tổ chức khám sức khỏe một lần."}],
    "hsk4_733": [{"chinese": "请测量一下体温。", "pinyin": "Qǐng cèliáng yíxià tǐwēn.", "meaningVi": "Xin hãy đo nhiệt độ cơ thể."}],
    "hsk4_734": [{"chinese": "他最近体重增加了。", "pinyin": "Tā zuìjìn tǐzhòng zēngjiā le.", "meaningVi": "Gần đây cân nặng của anh ấy đã tăng lên."}],
    "hsk4_735": [{"chinese": "请填写您的姓名和电话。", "pinyin": "Qǐng tiánxiě nín de xìngmíng hé diànhuà.", "meaningVi": "Xin hãy điền tên và số điện thoại của bạn."}],
    "hsk4_736": [{"chinese": "这里的生活条件不错。", "pinyin": "Zhèlǐ de shēnghuó tiáojiàn búcuò.", "meaningVi": "Điều kiện sống ở đây khá tốt."}],
    "hsk4_737": [{"chinese": "我的听力还需要提高。", "pinyin": "Wǒ de tīnglì hái xūyào tígāo.", "meaningVi": "Kỹ năng nghe của tôi vẫn cần cải thiện."}],
    "hsk4_738": [{"chinese": "电台的听众越来越多。", "pinyin": "Diàntái de tīngzhòng yuèláiyuè duō.", "meaningVi": "Thính giả của đài phát thanh ngày càng nhiều."}],
    "hsk4_739": [{"chinese": "车停在门口。", "pinyin": "Chē tíng zài ménkǒu.", "meaningVi": "Xe dừng ở trước cửa."}],
    "hsk4_740": [{"chinese": "这里不能停车。", "pinyin": "Zhèlǐ bù néng tíngchē.", "meaningVi": "Ở đây không được đỗ xe."}],
    "hsk4_741": [{"chinese": "商场旁边有一个停车场。", "pinyin": "Shāngchǎng pángbiān yǒu yí gè tíngchēchǎng.", "meaningVi": "Bên cạnh trung tâm thương mại có một bãi đỗ xe."}],
    "hsk4_742": [{"chinese": "雨已经停止了。", "pinyin": "Yǔ yǐjīng tíngzhǐ le.", "meaningVi": "Mưa đã tạnh rồi."}],
    "hsk4_746": [{"chinese": "他的童年很快乐。", "pinyin": "Tā de tóngnián hěn kuàilè.", "meaningVi": "Thời thơ ấu của anh ấy rất vui vẻ."}],
    "hsk4_748": [{"chinese": "我们遇到了同样的问题。", "pinyin": "Wǒmen yùdàole tóngyàng de wèntí.", "meaningVi": "Chúng tôi đã gặp phải vấn đề giống nhau."}],
    "hsk4_749": [{"chinese": "他提了一桶水。", "pinyin": "Tā tíle yì tǒng shuǐ.", "meaningVi": "Anh ấy xách một xô nước."}],
    "hsk4_751": [{"chinese": "我今天有点头痛。", "pinyin": "Wǒ jīntiān yǒudiǎn tóutòng.", "meaningVi": "Hôm nay tôi hơi đau đầu."}],
    "hsk4_753": [{"chinese": "请上传一张图片。", "pinyin": "Qǐng shàngchuán yì zhāng túpiàn.", "meaningVi": "Xin hãy tải lên một bức hình."}],
    "hsk4_755": [{"chinese": "请帮我推一下这辆车。", "pinyin": "Qǐng bāng wǒ tuī yíxià zhè liàng chē.", "meaningVi": "Xin giúp tôi đẩy chiếc xe này một chút."}],
    "hsk4_756": [{"chinese": "会议推迟到明天了。", "pinyin": "Huìyì tuīchí dào míngtiān le.", "meaningVi": "Cuộc họp đã hoãn đến ngày mai."}],
    "hsk4_757": [{"chinese": "公司推出了新产品。", "pinyin": "Gōngsī tuīchūle xīn chǎnpǐn.", "meaningVi": "Công ty đã ra mắt sản phẩm mới."}],
    "hsk4_758": [{"chinese": "进门请脱鞋。", "pinyin": "Jìnmén qǐng tuō xié.", "meaningVi": "Vào cửa xin cởi giày."}],
    "hsk4_759": [{"chinese": "他穿了一双白袜子。", "pinyin": "Tā chuānle yì shuāng bái wàzi.", "meaningVi": "Anh ấy đi một đôi tất trắng."}],
    "hsk4_760": [{"chinese": "外出的时候请注意安全。", "pinyin": "Wàichū de shíhou qǐng zhùyì ānquán.", "meaningVi": "Khi ra ngoài xin hãy chú ý an toàn."}],
    "hsk4_761": [{"chinese": "天冷了，穿件外套吧。", "pinyin": "Tiān lěng le, chuān jiàn wàitào ba.", "meaningVi": "Trời lạnh rồi, mặc áo khoác vào đi."}],
    "hsk4_763": [{"chinese": "晚安，做个好梦。", "pinyin": "Wǎn'ān, zuò ge hǎo mèng.", "meaningVi": "Chúc ngủ ngon, mơ giấc mơ đẹp."}],
    "hsk4_764": [{"chinese": "我们一起吃晚餐吧。", "pinyin": "Wǒmen yìqǐ chī wǎncān ba.", "meaningVi": "Chúng ta cùng nhau ăn tối đi."}],
    "hsk4_765": [{"chinese": "现在很多人喜欢网购。", "pinyin": "Xiànzài hěn duō rén xǐhuan wǎnggòu.", "meaningVi": "Bây giờ rất nhiều người thích mua sắm online."}],
    "hsk4_766": [{"chinese": "他往往工作到很晚。", "pinyin": "Tā wǎngwǎng gōngzuò dào hěn wǎn.", "meaningVi": "Anh ấy thường làm việc đến rất muộn."}],
    "hsk4_767": [{"chinese": "这个网页打不开。", "pinyin": "Zhège wǎngyè dǎ bu kāi.", "meaningVi": "Trang web này không mở được."}],
    "hsk4_768": [{"chinese": "我们是在网上认识的网友。", "pinyin": "Wǒmen shì zài wǎngshàng rènshi de wǎngyǒu.", "meaningVi": "Chúng tôi là bạn quen nhau trên mạng."}],
    "hsk4_769": [{"chinese": "请把网址发给我。", "pinyin": "Qǐng bǎ wǎngzhǐ fā gěi wǒ.", "meaningVi": "Xin gửi địa chỉ web cho tôi."}],
    "hsk4_772": [{"chinese": "这个汤有点怪味。", "pinyin": "Zhège tāng yǒudiǎn guài wèi.", "meaningVi": "Món canh này có mùi vị hơi lạ."}],
    "hsk4_773": [{"chinese": "这道菜的味道很好。", "pinyin": "Zhè dào cài de wèidào hěn hǎo.", "meaningVi": "Vị của món ăn này rất ngon."}],
    "hsk4_775": [{"chinese": "请调节一下空调的温度。", "pinyin": "Qǐng tiáojié yíxià kōngtiáo de wēndù.", "meaningVi": "Xin điều chỉnh nhiệt độ điều hòa."}],
    "hsk4_776": [{"chinese": "你闻闻这朵花香不香。", "pinyin": "Nǐ wénwen zhè duǒ huā xiāng bu xiāng.", "meaningVi": "Bạn ngửi thử xem bông hoa này có thơm không."}],
    "hsk4_777": [{"chinese": "这份文件很重要。", "pinyin": "Zhè fèn wénjiàn hěn zhòngyào.", "meaningVi": "Tài liệu này rất quan trọng."}],
    "hsk4_778": [{"chinese": "他写了一篇文章。", "pinyin": "Tā xiěle yì piān wénzhāng.", "meaningVi": "Anh ấy đã viết một bài viết."}],
    "hsk4_779": [{"chinese": "这些文字很难认。", "pinyin": "Zhèxiē wénzì hěn nán rèn.", "meaningVi": "Những chữ viết này rất khó nhận ra."}],
    "hsk4_780": [{"chinese": "我们要减少环境污染。", "pinyin": "Wǒmen yào jiǎnshǎo huánjìng wūrǎn.", "meaningVi": "Chúng ta phải giảm ô nhiễm môi trường."}],
    "hsk4_781": [{"chinese": "他毫无办法。", "pinyin": "Tā háowú bànfǎ.", "meaningVi": "Anh ấy hoàn toàn không có cách nào."}],
    "hsk4_782": [{"chinese": "我无法接受这个结果。", "pinyin": "Wǒ wúfǎ jiēshòu zhège jiéguǒ.", "meaningVi": "Tôi không thể chấp nhận kết quả này."}],
    "hsk4_783": [{"chinese": "一个人在家很无聊。", "pinyin": "Yí gè rén zài jiā hěn wúliáo.", "meaningVi": "Ở nhà một mình rất buồn chán."}],
    "hsk4_784": [{"chinese": "无论发生什么，我都支持你。", "pinyin": "Wúlùn fāshēng shénme, wǒ dōu zhīchí nǐ.", "meaningVi": "Dù có chuyện gì xảy ra, tôi đều ủng hộ bạn."}],
    "hsk4_785": [{"chinese": "午餐时间到了。", "pinyin": "Wǔcān shíjiān dào le.", "meaningVi": "Đến giờ ăn trưa rồi."}],
    "hsk4_787": [{"chinese": "他戒烟了，不再吸烟。", "pinyin": "Tā jièyān le, bú zài xīyān.", "meaningVi": "Anh ấy đã bỏ thuốc, không hút thuốc nữa."}],
    "hsk4_788": [{"chinese": "他们住在城市的西部。", "pinyin": "Tāmen zhù zài chéngshì de xībù.", "meaningVi": "Họ sống ở phía Tây thành phố."}],
    "hsk4_789": [{"chinese": "我买了几个西红柿。", "pinyin": "Wǒ mǎile jǐ gè xīhóngshì.", "meaningVi": "Tôi đã mua vài quả cà chua."}],
    "hsk4_790": [{"chinese": "这个广告吸引了很多顾客。", "pinyin": "Zhège guǎnggào xīyǐnle hěn duō gùkè.", "meaningVi": "Quảng cáo này đã thu hút rất nhiều khách hàng."}],
    "hsk4_791": [{"chinese": "这根线太细了。", "pinyin": "Zhè gēn xiàn tài xì le.", "meaningVi": "Sợi chỉ này quá mảnh."}],
    "hsk4_792": [{"chinese": "她做事很细心。", "pinyin": "Tā zuòshì hěn xìxīn.", "meaningVi": "Cô ấy làm việc rất cẩn thận."}],
    "hsk4_793": [{"chinese": "今年的销量有所下降。", "pinyin": "Jīnnián de xiāoliàng yǒusuǒ xiàjiàng.", "meaningVi": "Doanh số năm nay có phần giảm xuống."}],
    "hsk4_794": [{"chinese": "这条鱼很鲜。", "pinyin": "Zhè tiáo yú hěn xiān.", "meaningVi": "Con cá này rất tươi."}],
    "hsk4_795": [{"chinese": "他送了她一束鲜花。", "pinyin": "Tā sòngle tā yí shù xiānhuā.", "meaningVi": "Anh ấy đã tặng cô ấy một bó hoa tươi."}],
    "hsk4_796": [{"chinese": "我不喜欢太咸的菜。", "pinyin": "Wǒ bù xǐhuan tài xián de cài.", "meaningVi": "Tôi không thích món ăn quá mặn."}],
    "hsk4_797": [{"chinese": "请问可以用现金吗？", "pinyin": "Qǐngwèn kěyǐ yòng xiànjīn ma?", "meaningVi": "Xin hỏi có thể dùng tiền mặt không?"}],
    "hsk4_798": [{"chinese": "我很羡慕他的生活。", "pinyin": "Wǒ hěn xiànmù tā de shēnghuó.", "meaningVi": "Tôi rất ngưỡng mộ cuộc sống của anh ấy."}],
    "hsk4_799": [{"chinese": "这门课是线上教学。", "pinyin": "Zhè mén kè shì xiànshàng jiàoxué.", "meaningVi": "Khóa học này là giảng dạy trực tuyến."}],
    "hsk4_800": [{"chinese": "我们改成线下见面吧。", "pinyin": "Wǒmen gǎichéng xiànxià jiànmiàn ba.", "meaningVi": "Chúng ta đổi sang gặp mặt trực tiếp đi."}],
    "hsk4_802": [{"chinese": "妈妈做的菜很香。", "pinyin": "Māma zuò de cài hěn xiāng.", "meaningVi": "Món ăn mẹ nấu rất thơm."}],
    "hsk4_803": [{"chinese": "跟以前相比，他进步了很多。", "pinyin": "Gēn yǐqián xiāngbǐ, tā jìnbùle hěn duō.", "meaningVi": "So với trước đây, anh ấy đã tiến bộ rất nhiều."}],
    "hsk4_805": [{"chinese": "我们要相互理解。", "pinyin": "Wǒmen yào xiānghù lǐjiě.", "meaningVi": "Chúng ta phải hiểu nhau."}],
    "hsk4_806": [{"chinese": "我们的看法基本相同。", "pinyin": "Wǒmen de kànfǎ jīběn xiāngtóng.", "meaningVi": "Quan điểm của chúng tôi về cơ bản giống nhau."}],
    "hsk4_807": [{"chinese": "请详细说明一下情况。", "pinyin": "Qǐng xiángxì shuōmíng yíxià qíngkuàng.", "meaningVi": "Xin hãy giải thích chi tiết về tình hình."}],
    "hsk4_809": [{"chinese": "我想听听你的想法。", "pinyin": "Wǒ xiǎng tīngting nǐ de xiǎngfǎ.", "meaningVi": "Tôi muốn nghe ý kiến của bạn."}],
    "hsk4_810": [{"chinese": "这项工作很重要。", "pinyin": "Zhè xiàng gōngzuò hěn zhòngyào.", "meaningVi": "Công việc này rất quan trọng."}],
    "hsk4_811": [{"chinese": "我收到了一个好消息。", "pinyin": "Wǒ shōudàole yí gè hǎo xiāoxi.", "meaningVi": "Tôi đã nhận được một tin tốt."}],
    "hsk4_812": [{"chinese": "这条街上有很多小吃。", "pinyin": "Zhè tiáo jiē shàng yǒu hěn duō xiǎochī.", "meaningVi": "Trên con phố này có rất nhiều món ăn vặt."}],
    "hsk4_813": [{"chinese": "这个小伙子很有礼貌。", "pinyin": "Zhège xiǎohuǒzi hěn yǒu lǐmào.", "meaningVi": "Chàng trai trẻ này rất lịch sự."}],
    "hsk4_814": [{"chinese": "我最近在看一本小说。", "pinyin": "Wǒ zuìjìn zài kàn yì běn xiǎoshuō.", "meaningVi": "Gần đây tôi đang đọc một cuốn tiểu thuyết."}],
    "hsk4_815": [{"chinese": "我们被分成了几个小组。", "pinyin": "Wǒmen bèi fēnchéngle jǐ gè xiǎozǔ.", "meaningVi": "Chúng tôi được chia thành mấy nhóm nhỏ."}],
    "hsk4_816": [{"chinese": "这种方法效果很好。", "pinyin": "Zhè zhǒng fāngfǎ xiàoguǒ hěn hǎo.", "meaningVi": "Phương pháp này hiệu quả rất tốt."}],
    "hsk4_818": [{"chinese": "他流了很多血。", "pinyin": "Tā liúle hěn duō xiě.", "meaningVi": "Anh ấy đã chảy rất nhiều máu."}],
    "hsk4_819": [{"chinese": "她的心很善良。", "pinyin": "Tā de xīn hěn shànliáng.", "meaningVi": "Trái tim của cô ấy rất lương thiện."}],
    "hsk4_821": [{"chinese": "今天他的心情不太好。", "pinyin": "Jīntiān tā de xīnqíng bú tài hǎo.", "meaningVi": "Hôm nay tâm trạng của anh ấy không tốt lắm."}],
    "hsk4_822": [{"chinese": "这里手机没有信号。", "pinyin": "Zhèlǐ shǒujī méiyǒu xìnhào.", "meaningVi": "Ở đây điện thoại không có tín hiệu."}],
    "hsk4_823": [{"chinese": "请提供更多的信息。", "pinyin": "Qǐng tígōng gèng duō de xìnxī.", "meaningVi": "Xin cung cấp thêm thông tin."}],
    "hsk4_824": [{"chinese": "他对未来很有信心。", "pinyin": "Tā duì wèilái hěn yǒu xìnxīn.", "meaningVi": "Anh ấy rất tự tin vào tương lai."}],
    "hsk4_826": [{"chinese": "今晚的星星特别亮。", "pinyin": "Jīnwǎn de xīngxing tèbié liàng.", "meaningVi": "Ngôi sao tối nay đặc biệt sáng."}],
    "hsk4_827": [{"chinese": "他早上六点就醒了。", "pinyin": "Tā zǎoshang liù diǎn jiù xǐng le.", "meaningVi": "Sáng nay anh ấy sáu giờ đã tỉnh dậy."}],
    "hsk4_828": [{"chinese": "这个问题带有一定的复杂性。", "pinyin": "Zhège wèntí dàiyǒu yídìng de fùzáxìng.", "meaningVi": "Vấn đề này mang tính phức tạp nhất định."}],
    "hsk4_829": [{"chinese": "报名不限性别。", "pinyin": "Bàomíng bú xiàn xìngbié.", "meaningVi": "Đăng ký không giới hạn giới tính."}],
    "hsk4_831": [{"chinese": "她的性格很开朗。", "pinyin": "Tā de xìnggé hěn kāilǎng.", "meaningVi": "Tính cách của cô ấy rất vui vẻ cởi mở."}],
    "hsk4_832": [{"chinese": "他们是亲兄弟。", "pinyin": "Tāmen shì qīn xiōngdì.", "meaningVi": "Họ là anh em ruột."}],
    "hsk4_833": [{"chinese": "森林里有一只熊。", "pinyin": "Sēnlín lǐ yǒu yì zhī xióng.", "meaningVi": "Trong rừng có một con gấu."}],
    "hsk4_834": [{"chinese": "他会修自行车。", "pinyin": "Tā huì xiū zìxíngchē.", "meaningVi": "Anh ấy biết sửa xe đạp."}],
    "hsk4_835": [{"chinese": "师傅正在修理空调。", "pinyin": "Shīfu zhèngzài xiūlǐ kōngtiáo.", "meaningVi": "Thợ đang sửa chữa điều hòa."}],
    "hsk4_836": [{"chinese": "他去过许多国家。", "pinyin": "Tā qùguo xǔduō guójiā.", "meaningVi": "Anh ấy đã đến nhiều quốc gia."}],
    "hsk4_837": [{"chinese": "这所大学的学费很贵。", "pinyin": "Zhè suǒ dàxué de xuéfèi hěn guì.", "meaningVi": "Học phí của trường đại học này rất đắt."}],
    "hsk4_838": [{"chinese": "他在艺术学院学习。", "pinyin": "Tā zài yìshù xuéyuàn xuéxí.", "meaningVi": "Anh ấy học tại học viện nghệ thuật."}],
    "hsk4_839": [{"chinese": "别把东西压坏了。", "pinyin": "Bié bǎ dōngxi yāhuài le.", "meaningVi": "Đừng đè hỏng đồ vật."}],
    "hsk4_840": [{"chinese": "工作压力太大了。", "pinyin": "Gōngzuò yālì tài dà le.", "meaningVi": "Áp lực công việc quá lớn."}],
    "hsk4_841": [{"chinese": "牙膏用完了。", "pinyin": "Yágāo yòngwán le.", "meaningVi": "Kem đánh răng đã dùng hết."}],
    "hsk4_842": [{"chinese": "中国位于亚洲。", "pinyin": "Zhōngguó wèiyú Yàzhōu.", "meaningVi": "Trung Quốc nằm ở châu Á."}],
    "hsk4_843": [{"chinese": "请不要在这里吸烟。", "pinyin": "Qǐng búyào zài zhèlǐ xīyān.", "meaningVi": "Xin đừng hút thuốc ở đây."}],
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
