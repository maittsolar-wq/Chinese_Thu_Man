"""P5.10.3 (continued) -- Batch 007 (continues immediately after
examples_batch_006.json; entirely within HSK3).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch to bound-morpheme and near-synonym-pair
risks the mechanical tier system does not catch on its own:
  - 市/试/室 (all bare single-character bound morphemes, rarely used
    standalone in modern speech): each example uses the morpheme in its
    most natural minimal real usage (本市, 试一下, 室内) rather than
    forcing an unnatural fully-bare sentence.
  - 收 (shōu, "to collect/receive") vs 收到 (shōudào, "to have
    received") -- kept structurally distinct: 收 example shows the
    ongoing/habitual collecting action, 收到 example shows the
    completed-receipt sense, matching each word's real usage pattern.
  - 受 (shòu, "to suffer/undergo" -- bound, mostly in compounds like
    受伤) vs 受到 (shòudào, "to receive/be subjected to" -- the freer,
    more common modern form): kept in separate natural compounds/
    constructions so neither example could be mistaken for the other.

Usage:
    python generate_examples_batch_007.py --dry-run
    python generate_examples_batch_007.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 7
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_007.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk3_242": [{"chinese": "请给我一瓶矿泉水。", "pinyin": "Qǐng gěi wǒ yì píng kuàngquánshuǐ.", "meaningVi": "Xin cho tôi một chai nước khoáng."}],
    "hsk3_243": [{"chinese": "他来自越南。", "pinyin": "Tā láizì Yuènán.", "meaningVi": "Anh ấy đến từ Việt Nam."}],
    "hsk3_244": [{"chinese": "今天天空很蓝。", "pinyin": "Jīntiān tiānkōng hěn lán.", "meaningVi": "Hôm nay bầu trời rất xanh."}],
    "hsk3_246": [{"chinese": "我们应该尊重老人。", "pinyin": "Wǒmen yīnggāi zūnzhòng lǎorén.", "meaningVi": "Chúng ta nên tôn trọng người già."}],
    "hsk3_247": [{"chinese": "他明天要离开这座城市。", "pinyin": "Tā míngtiān yào líkāi zhè zuò chéngshì.", "meaningVi": "Ngày mai anh ấy sẽ rời khỏi thành phố này."}],
    "hsk3_248": [{"chinese": "这是我送给你的礼物。", "pinyin": "Zhè shì wǒ sòng gěi nǐ de lǐwù.", "meaningVi": "Đây là món quà tôi tặng bạn."}],
    "hsk3_249": [{"chinese": "我对中国历史很感兴趣。", "pinyin": "Wǒ duì Zhōngguó lìshǐ hěn gǎn xìngqù.", "meaningVi": "Tôi rất có hứng thú với lịch sử Trung Quốc."}],
    "hsk3_250": [{"chinese": "她的脸红了。", "pinyin": "Tā de liǎn hóng le.", "meaningVi": "Mặt cô ấy đỏ lên."}],
    "hsk3_251": [{"chinese": "他每天练毛笔字。", "pinyin": "Tā měitiān liàn máobǐ zì.", "meaningVi": "Anh ấy mỗi ngày luyện viết chữ bằng bút lông."}],
    "hsk3_253": [{"chinese": "树下很凉快。", "pinyin": "Shù xià hěn liángkuai.", "meaningVi": "Dưới gốc cây rất mát mẻ."}],
    "hsk3_254": [{"chinese": "停车场里停了很多辆车。", "pinyin": "Tíngchēchǎng lǐ tíngle hěn duō liàng chē.", "meaningVi": "Trong bãi đỗ xe có rất nhiều xe."}],
    "hsk3_255": [{"chinese": "我们聊了很长时间。", "pinyin": "Wǒmen liáole hěn cháng shíjiān.", "meaningVi": "Chúng tôi đã trò chuyện rất lâu."}],
    "hsk3_256": [{"chinese": "我喜欢和朋友聊天儿。", "pinyin": "Wǒ xǐhuan hé péngyou liáotiānr.", "meaningVi": "Tôi thích trò chuyện cùng bạn bè."}],
    "hsk3_257": [{"chinese": "我想多了解一下这个国家的文化。", "pinyin": "Wǒ xiǎng duō liǎojiě yíxià zhège guójiā de wénhuà.", "meaningVi": "Tôi muốn tìm hiểu thêm về văn hóa của đất nước này."}],
    "hsk3_258": [{"chinese": "我们的邻居很友好。", "pinyin": "Wǒmen de línjū hěn yǒuhǎo.", "meaningVi": "Hàng xóm của chúng tôi rất thân thiện."}],
    "hsk3_259": [{"chinese": "他打算去英国留学。", "pinyin": "Tā dǎsuàn qù Yīngguó liúxué.", "meaningVi": "Anh ấy định đi Anh du học."}],
    "hsk3_260": [{"chinese": "我们学校有很多留学生。", "pinyin": "Wǒmen xuéxiào yǒu hěn duō liúxuéshēng.", "meaningVi": "Trường chúng tôi có rất nhiều du học sinh."}],
    "hsk3_261": [{"chinese": "请走楼梯，不要坐电梯。", "pinyin": "Qǐng zǒu lóutī, búyào zuò diàntī.", "meaningVi": "Xin đi cầu thang, đừng đi thang máy."}],
    "hsk3_262": [{"chinese": "路边有很多小吃摊。", "pinyin": "Lùbiān yǒu hěn duō xiǎochī tān.", "meaningVi": "Ven đường có rất nhiều quầy ăn vặt."}],
    "hsk3_263": [{"chinese": "请在下一个路口右转。", "pinyin": "Qǐng zài xià yí gè lùkǒu yòu zhuǎn.", "meaningVi": "Xin rẽ phải ở ngã đường tiếp theo."}],
    "hsk3_264": [{"chinese": "他会骑马。", "pinyin": "Tā huì qí mǎ.", "meaningVi": "Anh ấy biết cưỡi ngựa."}],
    "hsk3_265": [{"chinese": "过马路要小心。", "pinyin": "Guò mǎlù yào xiǎoxīn.", "meaningVi": "Qua đường phải cẩn thận."}],
    "hsk3_266": [{"chinese": "我马上就来。", "pinyin": "Wǒ mǎshàng jiù lái.", "meaningVi": "Tôi đến ngay đây."}],
    "hsk3_267": [{"chinese": "老板对这次的结果很满意。", "pinyin": "Lǎobǎn duì zhè cì de jiéguǒ hěn mǎnyì.", "meaningVi": "Sếp rất hài lòng với kết quả lần này."}],
    "hsk3_270": [{"chinese": "困难面前，他从不放弃。", "pinyin": "Kùnnan miànqián, tā cóng bú fàngqì.", "meaningVi": "Trước khó khăn, anh ấy không bao giờ từ bỏ."}],
    "hsk3_272": [{"chinese": "请把名单交给我。", "pinyin": "Qǐng bǎ míngdān jiāo gěi wǒ.", "meaningVi": "Xin đưa danh sách cho tôi."}],
    "hsk3_273": [{"chinese": "他是一位名人。", "pinyin": "Tā shì yí wèi míngrén.", "meaningVi": "Anh ấy là một người nổi tiếng."}],
    "hsk3_274": [{"chinese": "学校在城市的南边。", "pinyin": "Xuéxiào zài chéngshì de nánbiān.", "meaningVi": "Trường học ở phía nam thành phố."}],
    "hsk3_276": [{"chinese": "南方的夏天很潮湿。", "pinyin": "Nánfāng de xiàtiān hěn cháoshī.", "meaningVi": "Mùa hè ở phương Nam rất ẩm ướt."}],
    "hsk3_277": [{"chinese": "听到这个消息，我很难过。", "pinyin": "Tīngdào zhège xiāoxi, wǒ hěn nánguò.", "meaningVi": "Nghe tin này, tôi rất buồn."}],
    "hsk3_278": [{"chinese": "这件衣服的颜色很难看。", "pinyin": "Zhè jiàn yīfu de yánsè hěn nánkàn.", "meaningVi": "Màu của chiếc áo này rất xấu."}],
    "hsk3_279": [{"chinese": "那个男人是我爸爸。", "pinyin": "Nàge nánrén shì wǒ bàba.", "meaningVi": "Người đàn ông đó là bố tôi."}],
    "hsk3_280": [{"chinese": "班里的男生比女生多。", "pinyin": "Bān lǐ de nánshēng bǐ nǚshēng duō.", "meaningVi": "Con trai trong lớp nhiều hơn con gái."}],
    "hsk3_281": [{"chinese": "这是一个难题。", "pinyin": "Zhè shì yí gè nántí.", "meaningVi": "Đây là một vấn đề khó."}],
    "hsk3_282": [{"chinese": "他唱歌很难听。", "pinyin": "Tā chànggē hěn nántīng.", "meaningVi": "Anh ấy hát rất khó nghe."}],
    "hsk3_283": [{"chinese": "我女儿上三年级了。", "pinyin": "Wǒ nǚ'ér shàng sān niánjí le.", "meaningVi": "Con gái tôi học lớp ba rồi."}],
    "hsk3_284": [{"chinese": "他看起来很年轻。", "pinyin": "Tā kàn qǐlái hěn niánqīng.", "meaningVi": "Trông anh ấy rất trẻ."}],
    "hsk3_287": [{"chinese": "她是一个坚强的女人。", "pinyin": "Tā shì yí gè jiānqiáng de nǚrén.", "meaningVi": "Cô ấy là một người phụ nữ mạnh mẽ."}],
    "hsk3_288": [{"chinese": "这个女生很活泼。", "pinyin": "Zhège nǚshēng hěn huópō.", "meaningVi": "Nữ sinh này rất hoạt bát."}],
    "hsk3_289": [{"chinese": "我们周末去爬山。", "pinyin": "Wǒmen zhōumò qù páshān.", "meaningVi": "Cuối tuần chúng tôi đi leo núi."}],
    "hsk3_291": [{"chinese": "我们在这里拍照吧。", "pinyin": "Wǒmen zài zhèlǐ pāizhào ba.", "meaningVi": "Chúng ta chụp ảnh ở đây đi."}],
    "hsk3_292": [{"chinese": "请把菜放在盘子里。", "pinyin": "Qǐng bǎ cài fàng zài pánzi lǐ.", "meaningVi": "Xin để món ăn vào đĩa."}],
    "hsk3_293": [{"chinese": "他最近胖了不少。", "pinyin": "Tā zuìjìn pàngle bù shǎo.", "meaningVi": "Gần đây anh ấy béo lên khá nhiều."}],
    "hsk3_294": [{"chinese": "天热的时候，人们喜欢喝啤酒。", "pinyin": "Tiān rè de shíhou, rénmen xǐhuan hē píjiǔ.", "meaningVi": "Khi trời nóng, mọi người thích uống bia."}],
    "hsk3_295": [{"chinese": "我平时七点起床。", "pinyin": "Wǒ píngshí qī diǎn qǐchuáng.", "meaningVi": "Ngày thường tôi thức dậy lúc bảy giờ."}],
    "hsk3_296": [{"chinese": "这个瓶子是空的。", "pinyin": "Zhège píngzi shì kōng de.", "meaningVi": "Cái chai này rỗng."}],
    "hsk3_297": [{"chinese": "他骑自行车上班。", "pinyin": "Tā qí zìxíngchē shàngbān.", "meaningVi": "Anh ấy đi xe đạp đi làm."}],
    "hsk3_298": [{"chinese": "这件事很奇怪。", "pinyin": "Zhè jiàn shì hěn qíguài.", "meaningVi": "Chuyện này rất kỳ lạ."}],
    "hsk3_299": [{"chinese": "其实我不太喜欢这个电影。", "pinyin": "Qíshí wǒ bú tài xǐhuan zhège diànyǐng.", "meaningVi": "Thực ra tôi không thích bộ phim này lắm."}],
    "hsk3_300": [{"chinese": "你还有其他问题吗？", "pinyin": "Nǐ hái yǒu qítā wèntí ma?", "meaningVi": "Bạn còn câu hỏi nào khác không?"}],
    "hsk3_302": [{"chinese": "飞机马上就要起飞了。", "pinyin": "Fēijī mǎshàng jiù yào qǐfēi le.", "meaningVi": "Máy bay sắp cất cánh rồi."}],
    "hsk3_303": [{"chinese": "他新买了一辆汽车。", "pinyin": "Tā xīn mǎile yí liàng qìchē.", "meaningVi": "Anh ấy vừa mua một chiếc ô tô mới."}],
    "hsk3_304": [{"chinese": "请用铅笔写。", "pinyin": "Qǐng yòng qiānbǐ xiě.", "meaningVi": "Xin viết bằng bút chì."}],
    "hsk3_305": [{"chinese": "前年我去过日本。", "pinyin": "Qiánnián wǒ qùguò Rìběn.", "meaningVi": "Năm kia tôi đã đi Nhật Bản."}],
    "hsk3_306": [{"chinese": "前天我很忙。", "pinyin": "Qiántiān wǒ hěn máng.", "meaningVi": "Hôm kia tôi rất bận."}],
    "hsk3_308": [{"chinese": "他今天请假没来上班。", "pinyin": "Tā jīntiān qǐngjià méi lái shàngbān.", "meaningVi": "Hôm nay anh ấy xin nghỉ không đi làm."}],
    "hsk3_309": [{"chinese": "今天我请客。", "pinyin": "Jīntiān wǒ qǐngkè.", "meaningVi": "Hôm nay tôi mời."}],
    "hsk3_310": [{"chinese": "秋天的树叶很漂亮。", "pinyin": "Qiūtiān de shùyè hěn piàoliang.", "meaningVi": "Lá cây mùa thu rất đẹp."}],
    "hsk3_311": [{"chinese": "他们在球场上打篮球。", "pinyin": "Tāmen zài qiúchǎng shàng dǎ lánqiú.", "meaningVi": "Họ đang chơi bóng rổ trên sân bóng."}],
    "hsk3_312": [{"chinese": "这条裙子很适合你。", "pinyin": "Zhè tiáo qúnzi hěn shìhé nǐ.", "meaningVi": "Chiếc váy này rất hợp với bạn."}],
    "hsk3_313": [{"chinese": "我们先吃饭，然后去看电影。", "pinyin": "Wǒmen xiān chīfàn, ránhòu qù kàn diànyǐng.", "meaningVi": "Chúng ta ăn cơm trước, sau đó đi xem phim."}],
    "hsk3_314": [{"chinese": "服务员对我们很热情。", "pinyin": "Fúwùyuán duì wǒmen hěn rèqíng.", "meaningVi": "Nhân viên phục vụ rất nhiệt tình với chúng tôi."}],
    "hsk3_315": [{"chinese": "我认得这个字。", "pinyin": "Wǒ rènde zhège zì.", "meaningVi": "Tôi nhận biết được chữ này."}],
    "hsk3_316": [{"chinese": "我认为这是个好主意。", "pinyin": "Wǒ rènwéi zhè shì gè hǎo zhǔyi.", "meaningVi": "Tôi cho rằng đây là một ý tưởng hay."}],
    "hsk3_317": [{"chinese": "他学习很认真。", "pinyin": "Tā xuéxí hěn rènzhēn.", "meaningVi": "Anh ấy học rất nghiêm túc."}],
    "hsk3_318": [{"chinese": "这个问题不容易回答。", "pinyin": "Zhège wèntí bù róngyì huídá.", "meaningVi": "Câu hỏi này không dễ trả lời."}],
    "hsk3_319": [{"chinese": "如果你有时间，请来找我。", "pinyin": "Rúguǒ nǐ yǒu shíjiān, qǐng lái zhǎo wǒ.", "meaningVi": "Nếu bạn có thời gian, xin đến tìm tôi."}],
    "hsk3_320": [{"chinese": "外面下雨了，带上伞吧。", "pinyin": "Wàimiàn xiàyǔ le, dàishàng sǎn ba.", "meaningVi": "Bên ngoài đang mưa, mang theo ô đi."}],
    "hsk3_321": [{"chinese": "请把地扫一下。", "pinyin": "Qǐng bǎ dì sǎo yíxià.", "meaningVi": "Xin quét sàn nhà một chút."}],
    "hsk3_322": [{"chinese": "他坐在沙发上看电视。", "pinyin": "Tā zuò zài shāfā shàng kàn diànshì.", "meaningVi": "Anh ấy ngồi trên ghế sofa xem tivi."}],
    "hsk3_323": [{"chinese": "这座山很高。", "pinyin": "Zhè zuò shān hěn gāo.", "meaningVi": "Ngọn núi này rất cao."}],
    "hsk3_324": [{"chinese": "他穿了一件黑色的上衣。", "pinyin": "Tā chuānle yí jiàn hēisè de shàngyī.", "meaningVi": "Anh ấy mặc một chiếc áo màu đen."}],
    "hsk3_325": [{"chinese": "请给我一个勺子。", "pinyin": "Qǐng gěi wǒ yí gè sháozi.", "meaningVi": "Xin cho tôi một cái thìa."}],
    "hsk3_326": [{"chinese": "她一直在我身边。", "pinyin": "Tā yìzhí zài wǒ shēnbiān.", "meaningVi": "Cô ấy luôn ở bên cạnh tôi."}],
    "hsk3_327": [{"chinese": "他的身高是一米八。", "pinyin": "Tā de shēngāo shì yì mǐ bā.", "meaningVi": "Chiều cao của anh ấy là một mét tám."}],
    "hsk3_330": [{"chinese": "别生气了。", "pinyin": "Bié shēngqì le.", "meaningVi": "Đừng tức giận nữa."}],
    "hsk3_331": [{"chinese": "她的声音很好听。", "pinyin": "Tā de shēngyīn hěn hǎotīng.", "meaningVi": "Giọng nói của cô ấy rất hay."}],
    "hsk3_332": [{"chinese": "这是本市最大的商场。", "pinyin": "Zhè shì běn shì zuì dà de shāngchǎng.", "meaningVi": "Đây là trung tâm thương mại lớn nhất thành phố này."}],
    "hsk3_333": [{"chinese": "你先试一下，看看合不合适。", "pinyin": "Nǐ xiān shì yíxià, kànkan hé bu héshì.", "meaningVi": "Bạn thử trước xem có vừa không."}],
    "hsk3_334": [{"chinese": "请在室内休息。", "pinyin": "Qǐng zài shìnèi xiūxi.", "meaningVi": "Xin nghỉ ngơi trong nhà."}],
    "hsk3_335": [{"chinese": "这是世界上最大的城市之一。", "pinyin": "Zhè shì shìjiè shàng zuì dà de chéngshì zhīyī.", "meaningVi": "Đây là một trong những thành phố lớn nhất thế giới."}],
    "hsk3_336": [{"chinese": "邮递员每天来收信。", "pinyin": "Yóudìyuán měitiān lái shōu xìn.", "meaningVi": "Người đưa thư mỗi ngày đến thu thư."}],
    "hsk3_337": [{"chinese": "我收到了你的邮件。", "pinyin": "Wǒ shōudàole nǐ de yóujiàn.", "meaningVi": "Tôi đã nhận được email của bạn."}],
    "hsk3_338": [{"chinese": "他在比赛中受了伤。", "pinyin": "Tā zài bǐsài zhōng shòule shāng.", "meaningVi": "Anh ấy đã bị thương trong trận đấu."}],
    "hsk3_339": [{"chinese": "她最近瘦了很多。", "pinyin": "Tā zuìjìn shòule hěn duō.", "meaningVi": "Gần đây cô ấy gầy đi nhiều."}],
    "hsk3_340": [{"chinese": "这部电影受到了观众的喜爱。", "pinyin": "Zhè bù diànyǐng shòudàole guānzhòng de xǐ'ài.", "meaningVi": "Bộ phim này được khán giả yêu thích."}],
    "hsk3_341": [{"chinese": "我叔叔在北京工作。", "pinyin": "Wǒ shūshu zài Běijīng gōngzuò.", "meaningVi": "Chú tôi làm việc ở Bắc Kinh."}],
    "hsk3_342": [{"chinese": "院子里有一棵大树。", "pinyin": "Yuànzi lǐ yǒu yì kē dà shù.", "meaningVi": "Trong sân có một cây to."}],
    "hsk3_343": [{"chinese": "他数学考得很好。", "pinyin": "Tā shùxué kǎo de hěn hǎo.", "meaningVi": "Anh ấy thi toán rất tốt."}],
    "hsk3_344": [{"chinese": "我每天早晚刷牙。", "pinyin": "Wǒ měitiān zǎowǎn shuāyá.", "meaningVi": "Tôi đánh răng mỗi sáng tối."}],
    "hsk3_345": [{"chinese": "我买了一双新鞋。", "pinyin": "Wǒ mǎile yì shuāng xīn xié.", "meaningVi": "Tôi đã mua một đôi giày mới."}],
    "hsk3_346": [{"chinese": "他的汉语水平很高。", "pinyin": "Tā de Hànyǔ shuǐpíng hěn gāo.", "meaningVi": "Trình độ tiếng Trung của anh ấy rất cao."}],
    "hsk3_347": [{"chinese": "出租车司机很热情。", "pinyin": "Chūzūchē sījī hěn rèqíng.", "meaningVi": "Tài xế taxi rất nhiệt tình."}],
    "hsk3_348": [{"chinese": "这里四季如春。", "pinyin": "Zhèlǐ sìjì rú chūn.", "meaningVi": "Nơi đây bốn mùa như mùa xuân."}],
    "hsk3_349": [{"chinese": "今天太阳很大。", "pinyin": "Jīntiān tàiyáng hěn dà.", "meaningVi": "Hôm nay nắng rất to."}],
    "hsk3_350": [{"chinese": "孩子们都喜欢吃糖。", "pinyin": "Háizimen dōu xǐhuan chī táng.", "meaningVi": "Bọn trẻ đều thích ăn kẹo."}],
    "hsk3_352": [{"chinese": "他想提高自己的英语水平。", "pinyin": "Tā xiǎng tígāo zìjǐ de Yīngyǔ shuǐpíng.", "meaningVi": "Anh ấy muốn nâng cao trình độ tiếng Anh của mình."}],
    "hsk3_353": [{"chinese": "他很喜欢体育运动。", "pinyin": "Tā hěn xǐhuan tǐyù yùndòng.", "meaningVi": "Anh ấy rất thích các môn thể thao."}],
    "hsk3_354": [{"chinese": "比赛在体育馆举行。", "pinyin": "Bǐsài zài tǐyùguǎn jǔxíng.", "meaningVi": "Trận đấu được tổ chức tại nhà thi đấu."}],
    "hsk3_355": [{"chinese": "这个水果很甜。", "pinyin": "Zhège shuǐguǒ hěn tián.", "meaningVi": "Loại trái cây này rất ngọt."}],
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
