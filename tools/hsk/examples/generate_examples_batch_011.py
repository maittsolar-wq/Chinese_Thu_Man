"""P5.10.3 (continued) -- Batch 011 (continues immediately after
examples_batch_010.json; entirely within HSK4).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch:
  - 假 (jiǎ, "fake/false" -- this specific record) vs the unrelated jià
    "vacation" reading that appears only inside separate compound words
    elsewhere in the universe (放假/寒假/假期/假日, none of which are
    the bare character "假" as their own record, so no tier3/4 conflict
    was flagged -- but the example was still deliberately written to
    use an unambiguous jiǎ "fake" sense, e.g. 假新闻 "fake news", never
    touching the vacation sense).
  - 共 (gòng, bound "total/together") vs 共同 (gòngtóng, "shared/
    common"): kept structurally distinct.
  - 购买 (gòumǎi, formal "to purchase") vs 购物 (gòuwù, "to shop/go
    shopping"): distinct register and construction.
  - 获得/获奖/获取 (huòdé/huòjiǎng/huòqǔ, "to obtain"/"to win an
    award"/"to acquire"): three genuine near-synonyms, each given its
    own natural, non-interchangeable sentence.
  - 减/减轻/减少 (jiǎn/jiǎnqīng/jiǎnshǎo, "subtract"/"lighten"/
    "reduce"): kept in three distinct natural constructions (arithmetic
    / pressure-relief / waste-reduction) so none reads as a template
    variant of another.

Usage:
    python generate_examples_batch_011.py --dry-run
    python generate_examples_batch_011.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 11
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_011.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_236": [{"chinese": "他以高价卖掉了房子。", "pinyin": "Tā yǐ gāojià màidiàole fángzi.", "meaningVi": "Anh ấy đã bán căn nhà với giá cao."}],
    "hsk4_237": [{"chinese": "高考对中国学生很重要。", "pinyin": "Gāokǎo duì Zhōngguó xuésheng hěn zhòngyào.", "meaningVi": "Kỳ thi đại học rất quan trọng đối với học sinh Trung Quốc."}],
    "hsk4_238": [{"chinese": "我们走高速公路吧。", "pinyin": "Wǒmen zǒu gāosù gōnglù ba.", "meaningVi": "Chúng ta đi đường cao tốc đi."}],
    "hsk4_239": [{"chinese": "这几天一直是高温天气。", "pinyin": "Zhè jǐ tiān yìzhí shì gāowēn tiānqì.", "meaningVi": "Mấy ngày nay thời tiết luôn nóng bức."}],
    "hsk4_240": [{"chinese": "今年的销量高于去年。", "pinyin": "Jīnnián de xiāoliàng gāoyú qùnián.", "meaningVi": "Doanh số năm nay cao hơn năm ngoái."}],
    "hsk4_241": [{"chinese": "他的胳膊受伤了。", "pinyin": "Tā de gēbo shòushāng le.", "meaningVi": "Cánh tay của anh ấy bị thương."}],
    "hsk4_242": [{"chinese": "远处传来悠扬的歌声。", "pinyin": "Yuǎnchù chuánlái yōuyáng de gēshēng.", "meaningVi": "Từ xa vọng lại tiếng hát du dương."}],
    "hsk4_243": [{"chinese": "她是一位有名的歌手。", "pinyin": "Tā shì yí wèi yǒumíng de gēshǒu.", "meaningVi": "Cô ấy là một ca sĩ nổi tiếng."}],
    "hsk4_245": [{"chinese": "来自各地的游客都来这里旅游。", "pinyin": "Láizì gèdì de yóukè dōu lái zhèlǐ lǚyóu.", "meaningVi": "Du khách từ khắp nơi đều đến đây du lịch."}],
    "hsk4_247": [{"chinese": "各位好，欢迎参加今天的会议。", "pinyin": "Gèwèi hǎo, huānyíng cānjiā jīntiān de huìyì.", "meaningVi": "Xin chào mọi người, hoan nghênh tham dự cuộc họp hôm nay."}],
    "hsk4_248": [{"chinese": "商店里有各种商品。", "pinyin": "Shāngdiàn lǐ yǒu gèzhǒng shāngpǐn.", "meaningVi": "Trong cửa hàng có đủ các loại hàng hóa."}],
    "hsk4_249": [{"chinese": "经过努力，他变得更加自信。", "pinyin": "Jīngguò nǔlì, tā biàn de gèngjiā zìxìn.", "meaningVi": "Qua nỗ lực, anh ấy trở nên tự tin hơn."}],
    "hsk4_250": [{"chinese": "这家工厂生产电器。", "pinyin": "Zhè jiā gōngchǎng shēngchǎn diànqì.", "meaningVi": "Nhà máy này sản xuất đồ điện."}],
    "hsk4_251": [{"chinese": "他会打中国功夫。", "pinyin": "Tā huì dǎ Zhōngguó gōngfu.", "meaningVi": "Anh ấy biết đánh võ công phu Trung Quốc."}],
    "hsk4_252": [{"chinese": "请爱护公共设施。", "pinyin": "Qǐng àihù gōnggòng shèshī.", "meaningVi": "Xin bảo vệ cơ sở vật chất công cộng."}],
    "hsk4_253": [{"chinese": "他每天认真做功课。", "pinyin": "Tā měitiān rènzhēn zuò gōngkè.", "meaningVi": "Anh ấy mỗi ngày làm bài tập một cách nghiêm túc."}],
    "hsk4_254": [{"chinese": "这里离机场大约十公里。", "pinyin": "Zhèlǐ lí jīchǎng dàyuē shí gōnglǐ.", "meaningVi": "Từ đây đến sân bay khoảng mười ki-lô-mét."}],
    "hsk4_255": [{"chinese": "这条公路正在扩建。", "pinyin": "Zhè tiáo gōnglù zhèngzài kuòjiàn.", "meaningVi": "Con đường này đang được mở rộng."}],
    "hsk4_256": [{"chinese": "工厂里有很多工人。", "pinyin": "Gōngchǎng lǐ yǒu hěn duō gōngrén.", "meaningVi": "Trong nhà máy có rất nhiều công nhân."}],
    "hsk4_257": [{"chinese": "他这个月的工资涨了。", "pinyin": "Tā zhège yuè de gōngzī zhǎng le.", "meaningVi": "Lương tháng này của anh ấy đã tăng."}],
    "hsk4_258": [{"chinese": "这次活动共有一百人参加。", "pinyin": "Zhè cì huódòng gòng yǒu yìbǎi rén cānjiā.", "meaningVi": "Hoạt động lần này có tổng cộng một trăm người tham gia."}],
    "hsk4_259": [{"chinese": "这是我们共同的目标。", "pinyin": "Zhè shì wǒmen gòngtóng de mùbiāo.", "meaningVi": "Đây là mục tiêu chung của chúng ta."}],
    "hsk4_261": [{"chinese": "顾客可以在网上购买商品。", "pinyin": "Gùkè kěyǐ zài wǎngshàng gòumǎi shāngpǐn.", "meaningVi": "Khách hàng có thể mua sản phẩm trên mạng."}],
    "hsk4_262": [{"chinese": "周末我喜欢去商场购物。", "pinyin": "Zhōumò wǒ xǐhuan qù shāngchǎng gòuwù.", "meaningVi": "Cuối tuần tôi thích đi trung tâm thương mại mua sắm."}],
    "hsk4_263": [{"chinese": "我估计他今天不会来了。", "pinyin": "Wǒ gūjì tā jīntiān bú huì lái le.", "meaningVi": "Tôi đoán hôm nay anh ấy sẽ không đến."}],
    "hsk4_264": [{"chinese": "那个姑娘很漂亮。", "pinyin": "Nàge gūniang hěn piàoliang.", "meaningVi": "Cô gái đó rất xinh đẹp."}],
    "hsk4_265": [{"chinese": "老师鼓励我们多提问。", "pinyin": "Lǎoshī gǔlì wǒmen duō tíwèn.", "meaningVi": "Giáo viên khuyến khích chúng tôi hỏi nhiều hơn."}],
    "hsk4_266": [{"chinese": "这家店的顾客很多。", "pinyin": "Zhè jiā diàn de gùkè hěn duō.", "meaningVi": "Cửa hàng này có rất nhiều khách hàng."}],
    "hsk4_267": [{"chinese": "他不是故意的。", "pinyin": "Tā bú shì gùyì de.", "meaningVi": "Anh ấy không phải cố ý."}],
    "hsk4_268": [{"chinese": "墙上挂着一张地图。", "pinyin": "Qiáng shàng guàzhe yì zhāng dìtú.", "meaningVi": "Trên tường treo một tấm bản đồ."}],
    "hsk4_270": [{"chinese": "我们一起观看了比赛。", "pinyin": "Wǒmen yìqǐ guānkànle bǐsài.", "meaningVi": "Chúng tôi cùng nhau xem trận đấu."}],
    "hsk4_271": [{"chinese": "现场观众非常热情。", "pinyin": "Xiànchǎng guānzhòng fēicháng rèqíng.", "meaningVi": "Khán giả tại hiện trường rất nhiệt tình."}],
    "hsk4_273": [{"chinese": "他负责管理这个团队。", "pinyin": "Tā fùzé guǎnlǐ zhège tuánduì.", "meaningVi": "Anh ấy phụ trách quản lý đội nhóm này."}],
    "hsk4_276": [{"chinese": "电视上有很多广告。", "pinyin": "Diànshì shàng yǒu hěn duō guǎnggào.", "meaningVi": "Trên tivi có rất nhiều quảng cáo."}],
    "hsk4_277": [{"chinese": "我们去逛街吧。", "pinyin": "Wǒmen qù guàngjiē ba.", "meaningVi": "Chúng ta đi dạo phố đi."}],
    "hsk4_279": [{"chinese": "他是什么国籍？", "pinyin": "Tā shì shénme guójí?", "meaningVi": "Anh ấy quốc tịch gì?"}],
    "hsk4_281": [{"chinese": "我想喝一杯果汁。", "pinyin": "Wǒ xiǎng hē yì bēi guǒzhī.", "meaningVi": "Tôi muốn uống một cốc nước trái cây."}],
    "hsk4_282": [{"chinese": "学习是一个漫长的过程。", "pinyin": "Xuéxí shì yí gè màncháng de guòchéng.", "meaningVi": "Học tập là một quá trình dài."}],
    "hsk4_283": [{"chinese": "海洋里有各种各样的生物。", "pinyin": "Hǎiyáng lǐ yǒu gèzhǒnggèyàng de shēngwù.", "meaningVi": "Trong đại dương có đủ loại sinh vật."}],
    "hsk4_284": [{"chinese": "她一见到陌生人就害羞。", "pinyin": "Tā yí jiàndào mòshēng rén jiù hàixiū.", "meaningVi": "Cô ấy hễ gặp người lạ là ngại ngùng."}],
    "hsk4_285": [{"chinese": "寒假我打算回老家。", "pinyin": "Hánjià wǒ dǎsuàn huí lǎojiā.", "meaningVi": "Kỳ nghỉ đông tôi định về quê."}],
    "hsk4_286": [{"chinese": "北方的冬天十分寒冷。", "pinyin": "Běifāng de dōngtiān shífēn hánlěng.", "meaningVi": "Mùa đông ở phương Bắc vô cùng lạnh giá."}],
    "hsk4_287": [{"chinese": "他大声喊了我的名字。", "pinyin": "Tā dàshēng hǎnle wǒ de míngzi.", "meaningVi": "Anh ấy hét to tên tôi."}],
    "hsk4_288": [{"chinese": "他跑步跑得满头是汗。", "pinyin": "Tā pǎobù pǎo de mǎntóu shì hàn.", "meaningVi": "Anh ấy chạy bộ đến mức đầu đầy mồ hôi."}],
    "hsk4_289": [{"chinese": "我们的航班几点起飞？", "pinyin": "Wǒmen de hángbān jǐ diǎn qǐfēi?", "meaningVi": "Chuyến bay của chúng ta mấy giờ cất cánh?"}],
    "hsk4_290": [{"chinese": "运动对身体有很多好处。", "pinyin": "Yùndòng duì shēntǐ yǒu hěn duō hǎochù.", "meaningVi": "Vận động có rất nhiều lợi ích cho sức khỏe."}],
    "hsk4_292": [{"chinese": "这个笑话很好笑。", "pinyin": "Zhège xiàohua hěn hǎoxiào.", "meaningVi": "Câu chuyện cười này rất buồn cười."}],
    "hsk4_293": [{"chinese": "这批产品都是合格的。", "pinyin": "Zhè pī chǎnpǐn dōu shì hégé de.", "meaningVi": "Lô sản phẩm này đều đạt chuẩn."}],
    "hsk4_294": [{"chinese": "这个盒子里装着礼物。", "pinyin": "Zhège hézi lǐ zhuāngzhe lǐwù.", "meaningVi": "Trong hộp này đựng quà."}],
    "hsk4_295": [{"chinese": "春节的时候，长辈会给孩子红包。", "pinyin": "Chūnjié de shíhou, zhǎngbèi huì gěi háizi hóngbāo.", "meaningVi": "Vào dịp Tết, người lớn sẽ cho trẻ em bao lì xì."}],
    "hsk4_296": [{"chinese": "这本书很厚。", "pinyin": "Zhè běn shū hěn hòu.", "meaningVi": "Cuốn sách này rất dày."}],
    "hsk4_297": [{"chinese": "他后悔没有努力学习。", "pinyin": "Tā hòuhuǐ méiyǒu nǔlì xuéxí.", "meaningVi": "Anh ấy hối hận vì đã không chăm chỉ học tập."}],
    "hsk4_298": [{"chinese": "天忽然黑了下来。", "pinyin": "Tiān hūrán hēile xiàlái.", "meaningVi": "Trời bỗng nhiên tối sầm lại."}],
    "hsk4_299": [{"chinese": "互联网改变了我们的生活。", "pinyin": "Hùliánwǎng gǎibiànle wǒmen de shēnghuó.", "meaningVi": "Internet đã thay đổi cuộc sống của chúng ta."}],
    "hsk4_300": [{"chinese": "她是一名护士。", "pinyin": "Tā shì yì míng hùshi.", "meaningVi": "Cô ấy là một y tá."}],
    "hsk4_301": [{"chinese": "我们应该互相帮助。", "pinyin": "Wǒmen yīnggāi hùxiāng bāngzhù.", "meaningVi": "Chúng ta nên giúp đỡ lẫn nhau."}],
    "hsk4_302": [{"chinese": "我们去看了一场话剧。", "pinyin": "Wǒmen qù kànle yì chǎng huàjù.", "meaningVi": "Chúng tôi đã đi xem một vở kịch nói."}],
    "hsk4_303": [{"chinese": "我怀疑他说的是假话。", "pinyin": "Wǒ huáiyí tā shuō de shì jiǎhuà.", "meaningVi": "Tôi nghi ngờ những gì anh ấy nói là giả."}],
    "hsk4_304": [{"chinese": "吸烟对身体有很多坏处。", "pinyin": "Xīyān duì shēntǐ yǒu hěn duō huàichù.", "meaningVi": "Hút thuốc có rất nhiều tác hại đối với sức khỏe."}],
    "hsk4_306": [{"chinese": "请在下一站换乘地铁二号线。", "pinyin": "Qǐng zài xià yí zhàn huànchéng dìtiě èr hào xiàn.", "meaningVi": "Xin đổi sang tuyến tàu điện ngầm số hai ở trạm tiếp theo."}],
    "hsk4_307": [{"chinese": "请尽快回复我的邮件。", "pinyin": "Qǐng jǐnkuài huífù wǒ de yóujiàn.", "meaningVi": "Xin hãy trả lời email của tôi sớm nhất có thể."}],
    "hsk4_309": [{"chinese": "他常常回忆起童年的生活。", "pinyin": "Tā chángcháng huíyì qǐ tóngnián de shēnghuó.", "meaningVi": "Anh ấy thường hồi tưởng lại cuộc sống thời thơ ấu."}],
    "hsk4_310": [{"chinese": "他是这家健身房的会员。", "pinyin": "Tā shì zhè jiā jiànshēnfáng de huìyuán.", "meaningVi": "Anh ấy là hội viên của phòng gym này."}],
    "hsk4_313": [{"chinese": "这个孩子很活泼。", "pinyin": "Zhège háizi hěn huópō.", "meaningVi": "Đứa trẻ này rất hoạt bát."}],
    "hsk4_315": [{"chinese": "这批货明天就能到。", "pinyin": "Zhè pī huò míngtiān jiù néng dào.", "meaningVi": "Lô hàng này ngày mai là có thể đến."}],
    "hsk4_316": [{"chinese": "他获得了第一名。", "pinyin": "Tā huòdéle dì-yī míng.", "meaningVi": "Anh ấy đã giành được vị trí thứ nhất."}],
    "hsk4_317": [{"chinese": "这部电影获奖了。", "pinyin": "Zhè bù diànyǐng huòjiǎng le.", "meaningVi": "Bộ phim này đã đoạt giải."}],
    "hsk4_318": [{"chinese": "我们可以通过阅读获取知识。", "pinyin": "Wǒmen kěyǐ tōngguò yuèdú huòqǔ zhīshi.", "meaningVi": "Chúng ta có thể thu được kiến thức thông qua việc đọc sách."}],
    "hsk4_320": [{"chinese": "这个问题基本上解决了。", "pinyin": "Zhège wèntí jīběnshàng jiějué le.", "meaningVi": "Vấn đề này về cơ bản đã được giải quyết."}],
    "hsk4_321": [{"chinese": "打好基础很重要。", "pinyin": "Dǎhǎo jīchǔ hěn zhòngyào.", "meaningVi": "Xây dựng nền tảng vững chắc rất quan trọng."}],
    "hsk4_323": [{"chinese": "他工作态度很积极。", "pinyin": "Tā gōngzuò tàidu hěn jījí.", "meaningVi": "Thái độ làm việc của anh ấy rất tích cực."}],
    "hsk4_324": [{"chinese": "学习需要长期积累。", "pinyin": "Xuéxí xūyào chángqī jīlěi.", "meaningVi": "Học tập cần tích lũy lâu dài."}],
    "hsk4_326": [{"chinese": "即使下雨，我们也要出发。", "pinyin": "Jíshǐ xiàyǔ, wǒmen yě yào chūfā.", "meaningVi": "Ngay cả khi trời mưa, chúng tôi cũng phải xuất phát."}],
    "hsk4_328": [{"chinese": "我给妈妈寄了一封信。", "pinyin": "Wǒ gěi māma jìle yì fēng xìn.", "meaningVi": "Tôi đã gửi một lá thư cho mẹ."}],
    "hsk4_330": [{"chinese": "既然你不同意，那就算了。", "pinyin": "Jìrán nǐ bù tóngyì, nà jiù suàn le.", "meaningVi": "Đã vậy bạn không đồng ý, thì thôi vậy."}],
    "hsk4_331": [{"chinese": "这项技术很先进。", "pinyin": "Zhè xiàng jìshù hěn xiānjìn.", "meaningVi": "Công nghệ này rất tiên tiến."}],
    "hsk4_332": [{"chinese": "我们继续开会吧。", "pinyin": "Wǒmen jìxù kāihuì ba.", "meaningVi": "Chúng ta tiếp tục họp đi."}],
    "hsk4_333": [{"chinese": "她是一名记者。", "pinyin": "Tā shì yì míng jìzhě.", "meaningVi": "Cô ấy là một nhà báo."}],
    "hsk4_334": [{"chinese": "他昨晚加班到很晚。", "pinyin": "Tā zuówǎn jiābān dào hěn wǎn.", "meaningVi": "Tối qua anh ấy làm thêm giờ đến rất muộn."}],
    "hsk4_335": [{"chinese": "这些家具是新买的。", "pinyin": "Zhèxiē jiājù shì xīn mǎi de.", "meaningVi": "Những đồ nội thất này mới mua."}],
    "hsk4_336": [{"chinese": "我们要加快工作进度。", "pinyin": "Wǒmen yào jiākuài gōngzuò jìndù.", "meaningVi": "Chúng ta phải đẩy nhanh tiến độ công việc."}],
    "hsk4_337": [{"chinese": "学校加强了安全管理。", "pinyin": "Xuéxiào jiāqiángle ānquán guǎnlǐ.", "meaningVi": "Nhà trường đã tăng cường quản lý an toàn."}],
    "hsk4_338": [{"chinese": "他决定加入我们的团队。", "pinyin": "Tā juédìng jiārù wǒmen de tuánduì.", "meaningVi": "Anh ấy quyết định gia nhập đội của chúng tôi."}],
    "hsk4_339": [{"chinese": "加上运费，一共一百元。", "pinyin": "Jiāshàng yùnfèi, yígòng yìbǎi yuán.", "meaningVi": "Cộng thêm phí vận chuyển, tổng cộng một trăm đồng."}],
    "hsk4_340": [{"chinese": "他出生在一个幸福的家庭。", "pinyin": "Tā chūshēng zài yí gè xìngfú de jiātíng.", "meaningVi": "Anh ấy sinh ra trong một gia đình hạnh phúc."}],
    "hsk4_341": [{"chinese": "我很想念我的家乡。", "pinyin": "Wǒ hěn xiǎngniàn wǒ de jiāxiāng.", "meaningVi": "Tôi rất nhớ quê hương của mình."}],
    "hsk4_342": [{"chinese": "大家一起为他加油！", "pinyin": "Dàjiā yìqǐ wèi tā jiāyóu!", "meaningVi": "Mọi người cùng cổ vũ cho anh ấy!"}],
    "hsk4_343": [{"chinese": "前面有一个加油站。", "pinyin": "Qiánmiàn yǒu yí gè jiāyóuzhàn.", "meaningVi": "Phía trước có một trạm xăng."}],
    "hsk4_344": [{"chinese": "家长会明天下午举行。", "pinyin": "Jiāzhǎnghuì míngtiān xiàwǔ jǔxíng.", "meaningVi": "Cuộc họp phụ huynh sẽ diễn ra vào chiều mai."}],
    "hsk4_345": [{"chinese": "这是一条假新闻。", "pinyin": "Zhè shì yì tiáo jiǎ xīnwén.", "meaningVi": "Đây là một tin giả."}],
    "hsk4_346": [{"chinese": "这里的价格比较便宜。", "pinyin": "Zhèlǐ de jiàgé bǐjiào piányi.", "meaningVi": "Giá cả ở đây khá rẻ."}],
    "hsk4_347": [{"chinese": "你们商量一下价钱吧。", "pinyin": "Nǐmen shāngliang yíxià jiàqián ba.", "meaningVi": "Các bạn thương lượng giá tiền một chút đi."}],
    "hsk4_348": [{"chinese": "假日期间，商场里人很多。", "pinyin": "Jiàrì qījiān, shāngchǎng lǐ rén hěn duō.", "meaningVi": "Trong dịp nghỉ lễ, trung tâm thương mại có rất nhiều người."}],
    "hsk4_349": [{"chinese": "十减五等于五。", "pinyin": "Shí jiǎn wǔ děngyú wǔ.", "meaningVi": "Mười trừ năm bằng năm."}],
    "hsk4_350": [{"chinese": "运动可以减轻压力。", "pinyin": "Yùndòng kěyǐ jiǎnqīng yālì.", "meaningVi": "Vận động có thể giảm nhẹ áp lực."}],
    "hsk4_351": [{"chinese": "我们应该减少浪费。", "pinyin": "Wǒmen yīnggāi jiǎnshǎo làngfèi.", "meaningVi": "Chúng ta nên giảm bớt lãng phí."}],
    "hsk4_352": [{"chinese": "他每天下班后去健身。", "pinyin": "Tā měitiān xiàbān hòu qù jiànshēn.", "meaningVi": "Anh ấy mỗi ngày sau khi tan làm đều đi tập gym."}],
    "hsk4_353": [{"chinese": "小区里新开了一家健身房。", "pinyin": "Xiǎoqū lǐ xīn kāile yì jiā jiànshēnfáng.", "meaningVi": "Trong khu dân cư mới mở một phòng gym."}],
    "hsk4_355": [{"chinese": "长江是中国最长的河流。", "pinyin": "Chángjiāng shì Zhōngguó zuì cháng de héliú.", "meaningVi": "Trường Giang là con sông dài nhất Trung Quốc."}],
    "hsk4_357": [{"chinese": "他对将来充满信心。", "pinyin": "Tā duì jiānglái chōngmǎn xìnxīn.", "meaningVi": "Anh ấy tràn đầy tự tin vào tương lai."}],
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
