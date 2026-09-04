"""P5.10.3 (continued) -- Batch 008 (continues immediately after
examples_batch_007.json; entirely within HSK3).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch:
  - 园 (yuán, "garden/park") vs 员 (yuán, "member/staff-suffix"): same
    pinyin, genuinely different characters and bound morphemes. Each is
    used in its own natural compound (植物园 / 售票员) so the two
    cannot be confused despite sharing a reading.
  - 遇到 (yùdào) vs 遇见 (yùjiàn), both "to encounter/meet": kept as
    distinct genuine near-synonyms with their own natural sentences
    (neither forced into an artificial contrast).
  - 以为 (yǐwéi, "mistakenly believed") vs 认为 (rènwéi, "to think/
    believe", already covered in an earlier batch): 以为's example is
    deliberately written to carry the "turned out to be wrong" nuance
    that distinguishes it from neutral 认为.
  - 怎么办 (zěnme bàn, "what to do") vs 怎样 (zěnyàng, "how"): kept in
    their respective natural constructions (worried rhetorical question
    vs. neutral manner question) rather than interchangeable phrasing.

Usage:
    python generate_examples_batch_008.py --dry-run
    python generate_examples_batch_008.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 8
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_008.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk3_356": [{"chinese": "他从椅子上跳了下来。", "pinyin": "Tā cóng yǐzi shàng tiàole xiàlái.", "meaningVi": "Anh ấy nhảy xuống từ chiếc ghế."}],
    "hsk3_357": [{"chinese": "听说他要出国了。", "pinyin": "Tīngshuō tā yào chūguó le.", "meaningVi": "Nghe nói anh ấy sắp ra nước ngoài."}],
    "hsk3_359": [{"chinese": "他是我的同事。", "pinyin": "Tā shì wǒ de tóngshì.", "meaningVi": "Anh ấy là đồng nghiệp của tôi."}],
    "hsk3_360": [{"chinese": "我同意你的意见。", "pinyin": "Wǒ tóngyì nǐ de yìjiàn.", "meaningVi": "Tôi đồng ý với ý kiến của bạn."}],
    "hsk3_361": [{"chinese": "她的头发很长。", "pinyin": "Tā de tóufa hěn cháng.", "meaningVi": "Tóc của cô ấy rất dài."}],
    "hsk3_362": [{"chinese": "天突然下起雨来。", "pinyin": "Tiān tūrán xiàqǐ yǔ lái.", "meaningVi": "Trời đột nhiên đổ mưa."}],
    "hsk3_363": [{"chinese": "我经常去图书馆看书。", "pinyin": "Wǒ jīngcháng qù túshūguǎn kàn shū.", "meaningVi": "Tôi thường xuyên đến thư viện đọc sách."}],
    "hsk3_364": [{"chinese": "他跑步的时候摔伤了腿。", "pinyin": "Tā pǎobù de shíhou shuāishāngle tuǐ.", "meaningVi": "Anh ấy bị thương chân khi chạy bộ."}],
    "hsk3_365": [{"chinese": "他是从外地来的。", "pinyin": "Tā shì cóng wàidì lái de.", "meaningVi": "Anh ấy đến từ nơi khác."}],
    "hsk3_367": [{"chinese": "学好一门外语不容易。", "pinyin": "Xuéhǎo yì mén wàiyǔ bù róngyì.", "meaningVi": "Học tốt một ngoại ngữ không dễ."}],
    "hsk3_368": [{"chinese": "他已经完成了作业。", "pinyin": "Tā yǐjīng wánchéngle zuòyè.", "meaningVi": "Anh ấy đã hoàn thành bài tập rồi."}],
    "hsk3_369": [{"chinese": "请再给我一碗米饭。", "pinyin": "Qǐng zài gěi wǒ yì wǎn mǐfàn.", "meaningVi": "Xin cho tôi thêm một bát cơm."}],
    "hsk3_370": [{"chinese": "我们的航班晚点了。", "pinyin": "Wǒmen de hángbān wǎndiǎn le.", "meaningVi": "Chuyến bay của chúng tôi bị trễ."}],
    "hsk3_371": [{"chinese": "学校举办了一场晚会。", "pinyin": "Xuéxiào jǔbànle yì chǎng wǎnhuì.", "meaningVi": "Trường đã tổ chức một buổi dạ hội."}],
    "hsk3_372": [{"chinese": "他每周打两次网球。", "pinyin": "Tā měi zhōu dǎ liǎng cì wǎngqiú.", "meaningVi": "Anh ấy chơi tennis hai lần mỗi tuần."}],
    "hsk3_373": [{"chinese": "这个网站的信息很有用。", "pinyin": "Zhège wǎngzhàn de xìnxī hěn yǒuyòng.", "meaningVi": "Thông tin trên trang web này rất hữu ích."}],
    "hsk3_374": [{"chinese": "我忘记带钥匙了。", "pinyin": "Wǒ wàngjì dài yàoshi le.", "meaningVi": "Tôi quên mang chìa khóa rồi."}],
    "hsk3_376": [{"chinese": "为了健康，他每天锻炼。", "pinyin": "Wèile jiànkāng, tā měitiān duànliàn.", "meaningVi": "Vì sức khỏe, anh ấy tập thể dục mỗi ngày."}],
    "hsk3_377": [{"chinese": "请问卫生间在哪儿？", "pinyin": "Qǐngwèn wèishēngjiān zài nǎr?", "meaningVi": "Xin hỏi nhà vệ sinh ở đâu?"}],
    "hsk3_378": [{"chinese": "我对中国文化很感兴趣。", "pinyin": "Wǒ duì Zhōngguó wénhuà hěn gǎn xìngqù.", "meaningVi": "Tôi rất hứng thú với văn hóa Trung Quốc."}],
    "hsk3_379": [{"chinese": "这间屋子很暖和。", "pinyin": "Zhè jiān wūzi hěn nuǎnhuo.", "meaningVi": "Căn phòng này rất ấm."}],
    "hsk3_380": [{"chinese": "太阳从西边落下。", "pinyin": "Tàiyáng cóng xībiān luòxià.", "meaningVi": "Mặt trời lặn về phía tây."}],
    "hsk3_381": [{"chinese": "甘肃在中国的西北部。", "pinyin": "Gānsù zài Zhōngguó de xīběibù.", "meaningVi": "Cam Túc nằm ở phía tây bắc Trung Quốc."}],
    "hsk3_382": [{"chinese": "这是一部西方电影。", "pinyin": "Zhè shì yí bù xīfāng diànyǐng.", "meaningVi": "Đây là một bộ phim phương Tây."}],
    "hsk3_383": [{"chinese": "夏天吃西瓜很解暑。", "pinyin": "Xiàtiān chī xīguā hěn jiěshǔ.", "meaningVi": "Mùa hè ăn dưa hấu rất giải nhiệt."}],
    "hsk3_384": [{"chinese": "云南在中国的西南部。", "pinyin": "Yúnnán zài Zhōngguó de xīnánbù.", "meaningVi": "Vân Nam nằm ở phía tây nam Trung Quốc."}],
    "hsk3_386": [{"chinese": "孩子们都很喜爱这个游戏。", "pinyin": "Háizimen dōu hěn xǐ'ài zhège yóuxì.", "meaningVi": "Bọn trẻ đều rất yêu thích trò chơi này."}],
    "hsk3_387": [{"chinese": "我用洗衣机洗衣服。", "pinyin": "Wǒ yòng xǐyījī xǐ yīfu.", "meaningVi": "Tôi dùng máy giặt để giặt quần áo."}],
    "hsk3_388": [{"chinese": "我每天晚上洗澡。", "pinyin": "Wǒ měitiān wǎnshang xǐzǎo.", "meaningVi": "Tôi tắm mỗi tối."}],
    "hsk3_389": [{"chinese": "夏天这里很热。", "pinyin": "Xiàtiān zhèlǐ hěn rè.", "meaningVi": "Mùa hè ở đây rất nóng."}],
    "hsk3_390": [{"chinese": "你先走吧，我马上就来。", "pinyin": "Nǐ xiān zǒu ba, wǒ mǎshàng jiù lái.", "meaningVi": "Bạn đi trước đi, tôi đến ngay."}],
    "hsk3_391": [{"chinese": "我早上吃了一根香蕉。", "pinyin": "Wǒ zǎoshang chīle yì gēn xiāngjiāo.", "meaningVi": "Buổi sáng tôi đã ăn một quả chuối."}],
    "hsk3_392": [{"chinese": "我相信你能做到。", "pinyin": "Wǒ xiāngxìn nǐ néng zuòdào.", "meaningVi": "Tôi tin bạn có thể làm được."}],
    "hsk3_393": [{"chinese": "请把箱子放在这里。", "pinyin": "Qǐng bǎ xiāngzi fàng zài zhèlǐ.", "meaningVi": "Xin đặt va li ở đây."}],
    "hsk3_396": [{"chinese": "他买了一台新相机。", "pinyin": "Tā mǎile yì tái xīn xiàngjī.", "meaningVi": "Anh ấy đã mua một chiếc máy ảnh mới."}],
    "hsk3_397": [{"chinese": "我们住在同一个小区。", "pinyin": "Wǒmen zhù zài tóng yí gè xiǎoqū.", "meaningVi": "Chúng tôi sống trong cùng một khu dân cư."}],
    "hsk3_399": [{"chinese": "校园里种了很多树。", "pinyin": "Xiàoyuán lǐ zhòngle hěn duō shù.", "meaningVi": "Trong khuôn viên trường trồng rất nhiều cây."}],
    "hsk3_400": [{"chinese": "校长在开学典礼上讲话。", "pinyin": "Xiàozhǎng zài kāixué diǎnlǐ shàng jiǎnghuà.", "meaningVi": "Hiệu trưởng phát biểu trong lễ khai giảng."}],
    "hsk3_401": [{"chinese": "这双鞋很好看。", "pinyin": "Zhè shuāng xié hěn hǎokàn.", "meaningVi": "Đôi giày này rất đẹp."}],
    "hsk3_402": [{"chinese": "我心里很不安。", "pinyin": "Wǒ xīnlǐ hěn bù'ān.", "meaningVi": "Trong lòng tôi rất bất an."}],
    "hsk3_403": [{"chinese": "祝你新年快乐！", "pinyin": "Zhù nǐ xīnnián kuàilè!", "meaningVi": "Chúc bạn năm mới vui vẻ!"}],
    "hsk3_404": [{"chinese": "我每天早上看新闻。", "pinyin": "Wǒ měitiān zǎoshang kàn xīnwén.", "meaningVi": "Tôi xem tin tức mỗi sáng."}],
    "hsk3_405": [{"chinese": "这些蔬菜很新鲜。", "pinyin": "Zhèxiē shūcài hěn xīnxiān.", "meaningVi": "Những loại rau này rất tươi."}],
    "hsk3_407": [{"chinese": "我用信用卡付款。", "pinyin": "Wǒ yòng xìnyòngkǎ fùkuǎn.", "meaningVi": "Tôi thanh toán bằng thẻ tín dụng."}],
    "hsk3_409": [{"chinese": "请帮我拿一下行李。", "pinyin": "Qǐng bāng wǒ ná yíxià xíngli.", "meaningVi": "Xin giúp tôi cầm hành lý một chút."}],
    "hsk3_410": [{"chinese": "他对音乐没有兴趣。", "pinyin": "Tā duì yīnyuè méiyǒu xìngqù.", "meaningVi": "Anh ấy không có hứng thú với âm nhạc."}],
    "hsk3_411": [{"chinese": "他这个月在休假。", "pinyin": "Tā zhège yuè zài xiūjià.", "meaningVi": "Tháng này anh ấy đang nghỉ phép."}],
    "hsk3_413": [{"chinese": "你选哪一个？", "pinyin": "Nǐ xuǎn nǎ yí gè?", "meaningVi": "Bạn chọn cái nào?"}],
    "hsk3_414": [{"chinese": "这是一个很难的选择。", "pinyin": "Zhè shì yí gè hěn nán de xuǎnzé.", "meaningVi": "Đây là một sự lựa chọn khó khăn."}],
    "hsk3_415": [{"chinese": "这个学期我们学了很多汉字。", "pinyin": "Zhège xuéqī wǒmen xuéle hěn duō Hànzì.", "meaningVi": "Học kỳ này chúng tôi đã học rất nhiều chữ Hán."}],
    "hsk3_416": [{"chinese": "他的牙很白。", "pinyin": "Tā de yá hěn bái.", "meaningVi": "Răng của anh ấy rất trắng."}],
    "hsk3_417": [{"chinese": "我买了一把新牙刷。", "pinyin": "Wǒ mǎile yì bǎ xīn yáshuā.", "meaningVi": "Tôi đã mua một bàn chải đánh răng mới."}],
    "hsk3_418": [{"chinese": "山上有很多羊。", "pinyin": "Shān shàng yǒu hěn duō yáng.", "meaningVi": "Trên núi có rất nhiều dê."}],
    "hsk3_419": [{"chinese": "他家养了一只小狗。", "pinyin": "Tā jiā yǎngle yì zhī xiǎo gǒu.", "meaningVi": "Nhà anh ấy nuôi một con chó nhỏ."}],
    "hsk3_421": [{"chinese": "这本书一共三百页。", "pinyin": "Zhè běn shū yígòng sānbǎi yè.", "meaningVi": "Cuốn sách này tổng cộng có ba trăm trang."}],
    "hsk3_423": [{"chinese": "这些东西一共多少钱？", "pinyin": "Zhèxiē dōngxi yígòng duōshao qián?", "meaningVi": "Những thứ này tổng cộng bao nhiêu tiền?"}],
    "hsk3_425": [{"chinese": "我和他的想法不一样。", "pinyin": "Wǒ hé tā de xiǎngfǎ bù yíyàng.", "meaningVi": "Suy nghĩ của tôi và anh ấy không giống nhau."}],
    "hsk3_426": [{"chinese": "以后有时间再聊吧。", "pinyin": "Yǐhòu yǒu shíjiān zài liáo ba.", "meaningVi": "Sau này có thời gian rồi nói chuyện tiếp nhé."}],
    "hsk3_427": [{"chinese": "我以前不喜欢喝咖啡。", "pinyin": "Wǒ yǐqián bù xǐhuan hē kāfēi.", "meaningVi": "Trước đây tôi không thích uống cà phê."}],
    "hsk3_428": [{"chinese": "十八岁以上才能开车。", "pinyin": "Shíbā suì yǐshàng cái néng kāichē.", "meaningVi": "Từ mười tám tuổi trở lên mới được lái xe."}],
    "hsk3_429": [{"chinese": "除了他以外，大家都到了。", "pinyin": "Chúle tā yǐwài, dàjiā dōu dào le.", "meaningVi": "Ngoài anh ấy ra, mọi người đều đến rồi."}],
    "hsk3_430": [{"chinese": "我以为你不会来了。", "pinyin": "Wǒ yǐwéi nǐ bú huì lái le.", "meaningVi": "Tôi tưởng bạn sẽ không đến nữa."}],
    "hsk3_431": [{"chinese": "请看以下内容。", "pinyin": "Qǐng kàn yǐxià nèiróng.", "meaningVi": "Xin xem nội dung dưới đây."}],
    "hsk3_432": [{"chinese": "我一般八点起床。", "pinyin": "Wǒ yìbān bā diǎn qǐchuáng.", "meaningVi": "Tôi thường thức dậy lúc tám giờ."}],
    "hsk3_434": [{"chinese": "他一直很努力。", "pinyin": "Tā yìzhí hěn nǔlì.", "meaningVi": "Anh ấy luôn luôn chăm chỉ."}],
    "hsk3_435": [{"chinese": "她喜欢听古典音乐。", "pinyin": "Tā xǐhuan tīng gǔdiǎn yīnyuè.", "meaningVi": "Cô ấy thích nghe nhạc cổ điển."}],
    "hsk3_436": [{"chinese": "我去银行取钱。", "pinyin": "Wǒ qù yínháng qǔ qián.", "meaningVi": "Tôi đi ngân hàng rút tiền."}],
    "hsk3_437": [{"chinese": "我把银行卡忘在家里了。", "pinyin": "Wǒ bǎ yínhángkǎ wàng zài jiā lǐ le.", "meaningVi": "Tôi quên thẻ ngân hàng ở nhà rồi."}],
    "hsk3_438": [{"chinese": "你想喝什么饮料？", "pinyin": "Nǐ xiǎng hē shénme yǐnliào?", "meaningVi": "Bạn muốn uống loại đồ uống gì?"}],
    "hsk3_439": [{"chinese": "你应该多休息。", "pinyin": "Nǐ yīnggāi duō xiūxi.", "meaningVi": "Bạn nên nghỉ ngơi nhiều hơn."}],
    "hsk3_441": [{"chinese": "我用手机拍照。", "pinyin": "Wǒ yòng shǒujī pāizhào.", "meaningVi": "Tôi dùng điện thoại để chụp ảnh."}],
    "hsk3_442": [{"chinese": "请检查一下你的邮件。", "pinyin": "Qǐng jiǎnchá yíxià nǐ de yóujiàn.", "meaningVi": "Xin kiểm tra email của bạn."}],
    "hsk3_443": [{"chinese": "这个地方吸引了很多游客。", "pinyin": "Zhège dìfang xīyǐnle hěn duō yóukè.", "meaningVi": "Nơi này thu hút rất nhiều du khách."}],
    "hsk3_444": [{"chinese": "孩子们喜欢玩这个游戏。", "pinyin": "Háizimen xǐhuan wán zhège yóuxì.", "meaningVi": "Bọn trẻ thích chơi trò chơi này."}],
    "hsk3_445": [{"chinese": "请把文件发到我的邮箱。", "pinyin": "Qǐng bǎ wénjiàn fā dào wǒ de yóuxiāng.", "meaningVi": "Xin gửi tài liệu vào email của tôi."}],
    "hsk3_447": [{"chinese": "这家饭馆很有名。", "pinyin": "Zhè jiā fànguǎn hěn yǒumíng.", "meaningVi": "Nhà hàng này rất nổi tiếng."}],
    "hsk3_448": [{"chinese": "这本书对我很有用。", "pinyin": "Zhè běn shū duì wǒ hěn yǒuyòng.", "meaningVi": "Cuốn sách này rất hữu ích với tôi."}],
    "hsk3_449": [{"chinese": "他今天又迟到了。", "pinyin": "Tā jīntiān yòu chídào le.", "meaningVi": "Hôm nay anh ấy lại đến muộn."}],
    "hsk3_450": [{"chinese": "我们放学后去打羽毛球。", "pinyin": "Wǒmen fàngxué hòu qù dǎ yǔmáoqiú.", "meaningVi": "Sau khi tan học chúng tôi đi đánh cầu lông."}],
    "hsk3_451": [{"chinese": "汉语是一种很美的语言。", "pinyin": "Hànyǔ shì yì zhǒng hěn měi de yǔyán.", "meaningVi": "Tiếng Trung là một ngôn ngữ rất đẹp."}],
    "hsk3_452": [{"chinese": "下雨了，快穿上雨衣。", "pinyin": "Xiàyǔ le, kuài chuānshàng yǔyī.", "meaningVi": "Trời mưa rồi, mau mặc áo mưa vào."}],
    "hsk3_453": [{"chinese": "我在路上遇到了一个老朋友。", "pinyin": "Wǒ zài lùshang yùdàole yí gè lǎo péngyou.", "meaningVi": "Tôi đã gặp một người bạn cũ trên đường."}],
    "hsk3_454": [{"chinese": "很高兴在这里遇见你。", "pinyin": "Hěn gāoxìng zài zhèlǐ yùjiàn nǐ.", "meaningVi": "Rất vui được gặp bạn ở đây."}],
    "hsk3_455": [{"chinese": "这是一个植物园。", "pinyin": "Zhè shì yí gè zhíwùyuán.", "meaningVi": "Đây là một vườn thực vật."}],
    "hsk3_456": [{"chinese": "他是一名售票员。", "pinyin": "Tā shì yì míng shòupiàoyuán.", "meaningVi": "Anh ấy là một nhân viên bán vé."}],
    "hsk3_457": [{"chinese": "我愿意帮助你。", "pinyin": "Wǒ yuànyì bāngzhù nǐ.", "meaningVi": "Tôi sẵn lòng giúp đỡ bạn."}],
    "hsk3_458": [{"chinese": "天气越来越冷了。", "pinyin": "Tiānqì yuè lái yuè lěng le.", "meaningVi": "Thời tiết ngày càng lạnh hơn."}],
    "hsk3_459": [{"chinese": "今晚的月亮很圆。", "pinyin": "Jīnwǎn de yuèliang hěn yuán.", "meaningVi": "Trăng đêm nay rất tròn."}],
    "hsk3_460": [{"chinese": "学校下个月举行运动会。", "pinyin": "Xuéxiào xià gè yuè jǔxíng yùndònghuì.", "meaningVi": "Trường sẽ tổ chức hội thao vào tháng sau."}],
    "hsk3_461": [{"chinese": "他是一名优秀的运动员。", "pinyin": "Tā shì yì míng yōuxiù de yùndòngyuán.", "meaningVi": "Anh ấy là một vận động viên xuất sắc."}],
    "hsk3_462": [{"chinese": "咱们一起去吧。", "pinyin": "Zánmen yìqǐ qù ba.", "meaningVi": "Chúng ta cùng đi đi."}],
    "hsk3_463": [{"chinese": "你的鞋子太脏了。", "pinyin": "Nǐ de xiézi tài zāng le.", "meaningVi": "Giày của bạn bẩn quá."}],
    "hsk3_464": [{"chinese": "要是他不同意，怎么办？", "pinyin": "Yàoshi tā bù tóngyì, zěnme bàn?", "meaningVi": "Nếu anh ấy không đồng ý thì phải làm sao?"}],
    "hsk3_465": [{"chinese": "你觉得这个办法怎样？", "pinyin": "Nǐ juéde zhège bànfǎ zěnyàng?", "meaningVi": "Bạn thấy cách này thế nào?"}],
    "hsk3_469": [{"chinese": "别着急，慢慢来。", "pinyin": "Bié zháojí, mànman lái.", "meaningVi": "Đừng sốt ruột, từ từ thôi."}],
    "hsk3_471": [{"chinese": "谢谢你一直照顾我。", "pinyin": "Xièxie nǐ yìzhí zhàogù wǒ.", "meaningVi": "Cảm ơn bạn đã luôn chăm sóc tôi."}],
    "hsk3_472": [{"chinese": "这张照片拍得很漂亮。", "pinyin": "Zhè zhāng zhàopiàn pāi de hěn piàoliang.", "meaningVi": "Bức ảnh này chụp rất đẹp."}],
    "hsk3_473": [{"chinese": "我们在长城照相留念。", "pinyin": "Wǒmen zài Chángchéng zhàoxiàng liúniàn.", "meaningVi": "Chúng tôi chụp ảnh lưu niệm ở Vạn Lý Trường Thành."}],
    "hsk3_474": [{"chinese": "他工作到很晚，直到深夜才回家。", "pinyin": "Tā gōngzuò dào hěn wǎn, zhídào shēnyè cái huí jiā.", "meaningVi": "Anh ấy làm việc đến rất khuya, mãi đến đêm khuya mới về nhà."}],
    "hsk3_476": [{"chinese": "请给我一张纸。", "pinyin": "Qǐng gěi wǒ yì zhāng zhǐ.", "meaningVi": "Xin cho tôi một tờ giấy."}],
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
