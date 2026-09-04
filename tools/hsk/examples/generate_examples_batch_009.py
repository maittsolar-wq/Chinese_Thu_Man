"""P5.10.3 (continued) -- Batch 009 (continues immediately after
examples_batch_008.json; spans the tail of HSK3's eligible pool into
the start of HSK4's).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Note on ID ordering: hsk4_1000 sorts between hsk4_100 and hsk4_101 in
this batch because the deterministic queue sorts source IDs as plain
strings (not numerically) -- this is expected, reproducible behavior of
queue_lib_p103, not an error.

Extra care applied in this batch:
  - 厂 (chǎng, "factory") vs 场 (chǎng, "measure word for events"):
    same pinyin, different characters/words -- each kept in its own
    natural compound/construction (汽车厂 / 这场比赛) so neither
    example could be mistaken for the other.
  - 城 (chéng, "city") vs 乘 (chéng, "to ride/take a vehicle"): same
    pinyin, different characters -- kept structurally distinct.
  - 答 (dá, "to answer," bound) vs 答案 (dá'àn, "answer/the noun"):
    答 is used in a classic parallel "老师问，学生答" construction
    that is natural for the bound verb; 答案 is used as the standalone
    noun it actually is.
  - 此/此次/此外/从此 (all built on the formal register morpheme 此,
    "this"): kept in four genuinely distinct formal constructions so no
    two examples read as templated variants of each other.
  - 不论 (búlùn) vs 不管 (bùguǎn), both "regardless of": distinct
    genuine near-synonyms, each with its own natural sentence.
  - 粗 (cū, "thick/coarse," bound) vs 粗心 (cūxīn, "careless"): kept
    in separate senses (physical thickness vs personality trait) so
    the shared root cannot cause sense confusion.

Usage:
    python generate_examples_batch_009.py --dry-run
    python generate_examples_batch_009.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 9
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_009.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk3_477": [{"chinese": "现在下雨了，我们只能在家里待着。", "pinyin": "Xiànzài xiàyǔ le, wǒmen zhǐ néng zài jiā lǐ dāizhe.", "meaningVi": "Bây giờ trời mưa rồi, chúng ta chỉ có thể ở nhà thôi."}],
    "hsk3_479": [{"chinese": "只要努力，就一定能成功。", "pinyin": "Zhǐyào nǔlì, jiù yídìng néng chénggōng.", "meaningVi": "Chỉ cần nỗ lực, nhất định sẽ thành công."}],
    "hsk3_480": [{"chinese": "只有他知道这个秘密。", "pinyin": "Zhǐyǒu tā zhīdào zhège mìmì.", "meaningVi": "Chỉ có anh ấy biết bí mật này."}],
    "hsk3_482": [{"chinese": "他坐在我们中间。", "pinyin": "Tā zuò zài wǒmen zhōngjiān.", "meaningVi": "Anh ấy ngồi ở giữa chúng tôi."}],
    "hsk3_483": [{"chinese": "他终于成功了。", "pinyin": "Tā zhōngyú chénggōng le.", "meaningVi": "Cuối cùng anh ấy đã thành công."}],
    "hsk3_485": [{"chinese": "健康比什么都重要。", "pinyin": "Jiànkāng bǐ shénme dōu zhòngyào.", "meaningVi": "Sức khỏe quan trọng hơn bất cứ điều gì."}],
    "hsk3_486": [{"chinese": "周末你有什么计划？", "pinyin": "Zhōumò nǐ yǒu shénme jìhuà?", "meaningVi": "Cuối tuần bạn có kế hoạch gì không?"}],
    "hsk3_487": [{"chinese": "这次会议的主要内容是什么？", "pinyin": "Zhè cì huìyì de zhǔyào nèiróng shì shénme?", "meaningVi": "Nội dung chủ yếu của cuộc họp lần này là gì?"}],
    "hsk3_488": [{"chinese": "过马路要注意安全。", "pinyin": "Guò mǎlù yào zhùyì ānquán.", "meaningVi": "Qua đường phải chú ý an toàn."}],
    "hsk3_489": [{"chinese": "他生病住院了。", "pinyin": "Tā shēngbìng zhùyuàn le.", "meaningVi": "Anh ấy bị bệnh phải nhập viện."}],
    "hsk3_490": [{"chinese": "不懂的字可以查字典。", "pinyin": "Bù dǒng de zì kěyǐ chá zìdiǎn.", "meaningVi": "Chữ không hiểu thì có thể tra từ điển."}],
    "hsk3_491": [{"chinese": "我每天骑自行车上班。", "pinyin": "Wǒ měitiān qí zìxíngchē shàngbān.", "meaningVi": "Tôi đi xe đạp đi làm mỗi ngày."}],
    "hsk3_494": [{"chinese": "他总是迟到。", "pinyin": "Tā zǒngshì chídào.", "meaningVi": "Anh ấy luôn luôn đến muộn."}],
    "hsk3_495": [{"chinese": "请把嘴张开。", "pinyin": "Qǐng bǎ zuǐ zhāngkāi.", "meaningVi": "Xin há miệng ra."}],
    "hsk3_496": [{"chinese": "你最好早点儿休息。", "pinyin": "Nǐ zuìhǎo zǎo diǎnr xiūxi.", "meaningVi": "Bạn nên nghỉ ngơi sớm một chút."}],
    "hsk3_497": [{"chinese": "最后，祝大家身体健康。", "pinyin": "Zuìhòu, zhù dàjiā shēntǐ jiànkāng.", "meaningVi": "Cuối cùng, chúc mọi người sức khỏe dồi dào."}],
    "hsk3_498": [{"chinese": "你最近怎么样？", "pinyin": "Nǐ zuìjìn zěnmeyàng?", "meaningVi": "Gần đây bạn thế nào?"}],
    "hsk3_499": [{"chinese": "欢迎你来我家做客。", "pinyin": "Huānyíng nǐ lái wǒ jiā zuòkè.", "meaningVi": "Hoan nghênh bạn đến nhà tôi chơi."}],
    "hsk3_500": [{"chinese": "你做完作业了吗？", "pinyin": "Nǐ zuòwán zuòyè le ma?", "meaningVi": "Bạn làm xong bài tập chưa?"}],
    "hsk4_024": [{"chinese": "他正在读本科。", "pinyin": "Tā zhèngzài dú běnkē.", "meaningVi": "Anh ấy đang học đại học (hệ cử nhân)."}],
    "hsk4_026": [{"chinese": "我不是笨，只是没学过。", "pinyin": "Wǒ bú shì bèn, zhǐshì méi xuéguò.", "meaningVi": "Tôi không ngốc, chỉ là chưa học qua thôi."}],
    "hsk4_027": [{"chinese": "他的鼻子有点儿红。", "pinyin": "Tā de bízi yǒudiǎnr hóng.", "meaningVi": "Mũi của anh ấy hơi đỏ."}],
    "hsk4_028": [{"chinese": "明天有一场笔试。", "pinyin": "Míngtiān yǒu yì chǎng bǐshì.", "meaningVi": "Ngày mai có một kỳ thi viết."}],
    "hsk4_029": [{"chinese": "他今年大学毕业。", "pinyin": "Tā jīnnián dàxué bìyè.", "meaningVi": "Năm nay anh ấy tốt nghiệp đại học."}],
    "hsk4_030": [{"chinese": "很多毕业生在找工作。", "pinyin": "Hěn duō bìyèshēng zài zhǎo gōngzuò.", "meaningVi": "Rất nhiều sinh viên tốt nghiệp đang tìm việc làm."}],
    "hsk4_031": [{"chinese": "这样安排便于大家参加。", "pinyin": "Zhèyàng ānpái biànyú dàjiā cānjiā.", "meaningVi": "Sắp xếp như vậy tiện cho mọi người tham gia."}],
    "hsk4_034": [{"chinese": "请填写这张表格。", "pinyin": "Qǐng tiánxiě zhè zhāng biǎogé.", "meaningVi": "Xin điền vào biểu mẫu này."}],
    "hsk4_035": [{"chinese": "他点头表示同意。", "pinyin": "Tā diǎntóu biǎoshì tóngyì.", "meaningVi": "Anh ấy gật đầu biểu thị đồng ý."}],
    "hsk4_036": [{"chinese": "他在比赛中表现得很好。", "pinyin": "Tā zài bǐsài zhōng biǎoxiàn de hěn hǎo.", "meaningVi": "Anh ấy thể hiện rất tốt trong cuộc thi."}],
    "hsk4_037": [{"chinese": "老师表扬了他。", "pinyin": "Lǎoshī biǎoyángle tā.", "meaningVi": "Giáo viên đã khen ngợi anh ấy."}],
    "hsk4_038": [{"chinese": "孩子喜欢吃饼干。", "pinyin": "Háizi xǐhuan chī bǐnggān.", "meaningVi": "Trẻ con thích ăn bánh quy."}],
    "hsk4_040": [{"chinese": "她聪明并且努力。", "pinyin": "Tā cōngming bìngqiě nǔlì.", "meaningVi": "Cô ấy thông minh mà lại chăm chỉ."}],
    "hsk4_041": [{"chinese": "电视台正在播放新闻。", "pinyin": "Diànshìtái zhèngzài bōfàng xīnwén.", "meaningVi": "Đài truyền hình đang phát sóng bản tin."}],
    "hsk4_042": [{"chinese": "他是一名博士。", "pinyin": "Tā shì yì míng bóshì.", "meaningVi": "Anh ấy là một tiến sĩ."}],
    "hsk4_043": [{"chinese": "你不必担心。", "pinyin": "Nǐ búbì dānxīn.", "meaningVi": "Bạn không cần lo lắng."}],
    "hsk4_048": [{"chinese": "不论发生什么，我都会支持你。", "pinyin": "Búlùn fāshēng shénme, wǒ dōu huì zhīchí nǐ.", "meaningVi": "Dù có chuyện gì xảy ra, tôi cũng sẽ ủng hộ bạn."}],
    "hsk4_049": [{"chinese": "他往前走了几步。", "pinyin": "Tā wǎng qián zǒule jǐ bù.", "meaningVi": "Anh ấy bước về phía trước vài bước."}],
    "hsk4_051": [{"chinese": "因为下雨，我们不得不取消比赛。", "pinyin": "Yīnwèi xiàyǔ, wǒmen bùdébù qǔxiāo bǐsài.", "meaningVi": "Vì trời mưa, chúng tôi buộc phải hủy trận đấu."}],
    "hsk4_052": [{"chinese": "大部分学生都通过了考试。", "pinyin": "Dà bùfen xuéshēng dōu tōngguòle kǎoshì.", "meaningVi": "Phần lớn học sinh đều đã vượt qua kỳ thi."}],
    "hsk4_053": [{"chinese": "不管多忙，他都会锻炼身体。", "pinyin": "Bùguǎn duō máng, tā dōu huì duànliàn shēntǐ.", "meaningVi": "Dù bận đến đâu, anh ấy cũng sẽ tập thể dục."}],
    "hsk4_055": [{"chinese": "他不仅会说汉语，还会说法语。", "pinyin": "Tā bùjǐn huì shuō Hànyǔ, hái huì shuō Fǎyǔ.", "meaningVi": "Anh ấy không chỉ biết nói tiếng Trung, mà còn biết nói tiếng Pháp."}],
    "hsk4_056": [{"chinese": "他对这个结果很不满。", "pinyin": "Tā duì zhège jiéguǒ hěn bùmǎn.", "meaningVi": "Anh ấy rất không hài lòng với kết quả này."}],
    "hsk4_057": [{"chinese": "他在销售部门工作。", "pinyin": "Tā zài xiāoshòu bùmén gōngzuò.", "meaningVi": "Anh ấy làm việc ở bộ phận bán hàng."}],
    "hsk4_058": [{"chinese": "这个方法不如那个好。", "pinyin": "Zhège fāngfǎ bùrú nàge hǎo.", "meaningVi": "Cách này không tốt bằng cách kia."}],
    "hsk4_059": [{"chinese": "请把桌子擦干净。", "pinyin": "Qǐng bǎ zhuōzi cā gānjìng.", "meaningVi": "Xin lau bàn cho sạch."}],
    "hsk4_060": [{"chinese": "你猜猜这是什么？", "pinyin": "Nǐ cāicai zhè shì shénme?", "meaningVi": "Bạn đoán xem đây là cái gì?"}],
    "hsk4_061": [{"chinese": "请准备好需要的材料。", "pinyin": "Qǐng zhǔnbèi hǎo xūyào de cáiliào.", "meaningVi": "Xin chuẩn bị sẵn tài liệu cần thiết."}],
    "hsk4_062": [{"chinese": "我们下午去参观博物馆。", "pinyin": "Wǒmen xiàwǔ qù cānguān bówùguǎn.", "meaningVi": "Buổi chiều chúng tôi đi tham quan bảo tàng."}],
    "hsk4_063": [{"chinese": "他决定参赛。", "pinyin": "Tā juédìng cānsài.", "meaningVi": "Anh ấy quyết định tham gia thi đấu."}],
    "hsk4_064": [{"chinese": "我们在学校餐厅吃饭。", "pinyin": "Wǒmen zài xuéxiào cāntīng chīfàn.", "meaningVi": "Chúng tôi ăn cơm ở căng tin trường."}],
    "hsk4_065": [{"chinese": "学生们在操场上跑步。", "pinyin": "Xuéshengmen zài cāochǎng shàng pǎobù.", "meaningVi": "Học sinh chạy bộ trên sân trường."}],
    "hsk4_066": [{"chinese": "厕所在走廊尽头。", "pinyin": "Cèsuǒ zài zǒuláng jìntóu.", "meaningVi": "Nhà vệ sinh ở cuối hành lang."}],
    "hsk4_067": [{"chinese": "请查看一下这份文件。", "pinyin": "Qǐng chákàn yíxià zhè fèn wénjiàn.", "meaningVi": "Xin xem qua tài liệu này."}],
    "hsk4_068": [{"chinese": "这种茶叶很有名。", "pinyin": "Zhè zhǒng cháyè hěn yǒumíng.", "meaningVi": "Loại trà này rất nổi tiếng."}],
    "hsk4_069": [{"chinese": "我在网上查找相关资料。", "pinyin": "Wǒ zài wǎngshàng cházhǎo xiāngguān zīliào.", "meaningVi": "Tôi tìm kiếm tài liệu liên quan trên mạng."}],
    "hsk4_071": [{"chinese": "这件事产生了很大的影响。", "pinyin": "Zhè jiàn shì chǎnshēngle hěn dà de yǐngxiǎng.", "meaningVi": "Việc này đã tạo ra ảnh hưởng rất lớn."}],
    "hsk4_072": [{"chinese": "这是一家汽车厂。", "pinyin": "Zhè shì yì jiā qìchēchǎng.", "meaningVi": "Đây là một nhà máy sản xuất ô tô."}],
    "hsk4_073": [{"chinese": "这场比赛很精彩。", "pinyin": "Zhè chǎng bǐsài hěn jīngcǎi.", "meaningVi": "Trận đấu này rất hấp dẫn."}],
    "hsk4_074": [{"chinese": "参加人数超过了一百人。", "pinyin": "Cānjiā rénshù chāoguòle yìbǎi rén.", "meaningVi": "Số người tham gia vượt quá một trăm người."}],
    "hsk4_075": [{"chinese": "请注意控制车速。", "pinyin": "Qǐng zhùyì kòngzhì chēsù.", "meaningVi": "Xin chú ý kiểm soát tốc độ xe."}],
    "hsk4_076": [{"chinese": "这里没有空的车位了。", "pinyin": "Zhèlǐ méiyǒu kòng de chēwèi le.", "meaningVi": "Ở đây không còn chỗ đỗ xe trống nữa."}],
    "hsk4_077": [{"chinese": "这座古城有两千年的历史。", "pinyin": "Zhè zuò gǔchéng yǒu liǎngqiān nián de lìshǐ.", "meaningVi": "Thành cổ này có lịch sử hai nghìn năm."}],
    "hsk4_078": [{"chinese": "我们乘火车去北京。", "pinyin": "Wǒmen chéng huǒchē qù Běijīng.", "meaningVi": "Chúng tôi đi tàu hỏa đến Bắc Kinh."}],
    "hsk4_080": [{"chinese": "车上的乘客都下车了。", "pinyin": "Chē shàng de chéngkè dōu xiàchē le.", "meaningVi": "Hành khách trên xe đều đã xuống xe."}],
    "hsk4_081": [{"chinese": "做人要诚实。", "pinyin": "Zuòrén yào chéngshí.", "meaningVi": "Làm người phải trung thực."}],
    "hsk4_082": [{"chinese": "他长大后成为了一名医生。", "pinyin": "Tā zhǎngdà hòu chéngwéile yì míng yīshēng.", "meaningVi": "Sau khi lớn lên, anh ấy trở thành một bác sĩ."}],
    "hsk4_083": [{"chinese": "请乘坐电梯到三楼。", "pinyin": "Qǐng chéngzuò diàntī dào sān lóu.", "meaningVi": "Xin đi thang máy lên tầng ba."}],
    "hsk4_084": [{"chinese": "听到这个消息，大家都很吃惊。", "pinyin": "Tīngdào zhège xiāoxi, dàjiā dōu hěn chījīng.", "meaningVi": "Nghe tin này, mọi người đều rất ngạc nhiên."}],
    "hsk4_085": [{"chinese": "他来得比较迟。", "pinyin": "Tā lái de bǐjiào chí.", "meaningVi": "Anh ấy đến khá muộn."}],
    "hsk4_087": [{"chinese": "我们需要重新计划一下。", "pinyin": "Wǒmen xūyào chóngxīn jìhuà yíxià.", "meaningVi": "Chúng ta cần lên kế hoạch lại."}],
    "hsk4_088": [{"chinese": "他下周要去上海出差。", "pinyin": "Tā xià zhōu yào qù Shànghǎi chūchāi.", "meaningVi": "Tuần sau anh ấy phải đi công tác ở Thượng Hải."}],
    "hsk4_090": [{"chinese": "天空中出现了一道彩虹。", "pinyin": "Tiānkōng zhōng chūxiànle yí dào cǎihóng.", "meaningVi": "Trên bầu trời xuất hiện một cầu vồng."}],
    "hsk4_091": [{"chinese": "春节期间出行的人很多。", "pinyin": "Chūnjié qījiān chūxíng de rén hěn duō.", "meaningVi": "Trong dịp Tết, số người đi lại rất đông."}],
    "hsk4_092": [{"chinese": "这套房子出租。", "pinyin": "Zhè tào fángzi chūzū.", "meaningVi": "Căn nhà này cho thuê."}],
    "hsk4_093": [{"chinese": "妈妈在厨房做饭。", "pinyin": "Māma zài chúfáng zuòfàn.", "meaningVi": "Mẹ đang nấu cơm trong bếp."}],
    "hsk4_094": [{"chinese": "他是一位有名的厨师。", "pinyin": "Tā shì yí wèi yǒumíng de chúshī.", "meaningVi": "Anh ấy là một đầu bếp nổi tiếng."}],
    "hsk4_095": [{"chinese": "请把窗打开。", "pinyin": "Qǐng bǎ chuāng dǎkāi.", "meaningVi": "Xin mở cửa sổ ra."}],
    "hsk4_096": [{"chinese": "窗户外面是一片花园。", "pinyin": "Chuānghu wàimiàn shì yí piàn huāyuán.", "meaningVi": "Bên ngoài cửa sổ là một khu vườn hoa."}],
    "hsk4_097": [{"chinese": "外面在吹大风。", "pinyin": "Wàimiàn zài chuī dà fēng.", "meaningVi": "Bên ngoài đang có gió lớn thổi."}],
    "hsk4_098": [{"chinese": "这个词语是什么意思？", "pinyin": "Zhège cíyǔ shì shénme yìsi?", "meaningVi": "Từ ngữ này có nghĩa là gì?"}],
    "hsk4_099": [{"chinese": "此事非常重要。", "pinyin": "Cǐ shì fēicháng zhòngyào.", "meaningVi": "Việc này vô cùng quan trọng."}],
    "hsk4_100": [{"chinese": "此次比赛的冠军是他。", "pinyin": "Cǐ cì bǐsài de guànjūn shì tā.", "meaningVi": "Nhà vô địch của giải đấu lần này là anh ấy."}],
    "hsk4_1000": [{"chinese": "这本书的作者是谁？", "pinyin": "Zhè běn shū de zuòzhě shì shéi?", "meaningVi": "Tác giả của cuốn sách này là ai?"}],
    "hsk4_101": [{"chinese": "此外，我们还需要准备一些材料。", "pinyin": "Cǐwài, wǒmen hái xūyào zhǔnbèi yìxiē cáiliào.", "meaningVi": "Ngoài ra, chúng ta còn cần chuẩn bị một số tài liệu."}],
    "hsk4_102": [{"chinese": "从此以后，他再也没有回来过。", "pinyin": "Cóngcǐ yǐhòu, tā zài yě méiyǒu huílái guò.", "meaningVi": "Từ đó về sau, anh ấy không bao giờ quay lại nữa."}],
    "hsk4_103": [{"chinese": "他从来不迟到。", "pinyin": "Tā cónglái bù chídào.", "meaningVi": "Anh ấy chưa bao giờ đến muộn."}],
    "hsk4_104": [{"chinese": "我们可以从中学到很多东西。", "pinyin": "Wǒmen kěyǐ cóngzhōng xuédào hěn duō dōngxi.", "meaningVi": "Chúng ta có thể học được nhiều điều từ trong đó."}],
    "hsk4_105": [{"chinese": "这根绳子很粗。", "pinyin": "Zhè gēn shéngzi hěn cū.", "meaningVi": "Sợi dây thừng này rất to."}],
    "hsk4_106": [{"chinese": "他做作业太粗心了，总是出错。", "pinyin": "Tā zuò zuòyè tài cūxīn le, zǒngshì chūcuò.", "meaningVi": "Anh ấy làm bài tập quá cẩu thả, luôn mắc lỗi."}],
    "hsk4_107": [{"chinese": "他出生在一个小村子里。", "pinyin": "Tā chūshēng zài yí gè xiǎo cūnzi lǐ.", "meaningVi": "Anh ấy sinh ra ở một ngôi làng nhỏ."}],
    "hsk4_108": [{"chinese": "我把钱存在银行里。", "pinyin": "Wǒ bǎ qián cún zài yínháng lǐ.", "meaningVi": "Tôi gửi tiền vào ngân hàng."}],
    "hsk4_109": [{"chinese": "别错过这个好机会。", "pinyin": "Bié cuòguò zhège hǎo jīhuì.", "meaningVi": "Đừng bỏ lỡ cơ hội tốt này."}],
    "hsk4_111": [{"chinese": "他答应帮我。", "pinyin": "Tā dāying bāng wǒ.", "meaningVi": "Anh ấy đã hứa giúp tôi."}],
    "hsk4_112": [{"chinese": "老师问，学生答。", "pinyin": "Lǎoshī wèn, xuéshēng dá.", "meaningVi": "Giáo viên hỏi, học sinh trả lời."}],
    "hsk4_113": [{"chinese": "这道题的答案是什么？", "pinyin": "Zhè dào tí de dá'àn shì shénme?", "meaningVi": "Đáp án của câu hỏi này là gì?"}],
    "hsk4_114": [{"chinese": "他终于达到了自己的目标。", "pinyin": "Tā zhōngyú dádàole zìjǐ de mùbiāo.", "meaningVi": "Cuối cùng anh ấy đã đạt được mục tiêu của mình."}],
    "hsk4_115": [{"chinese": "见到老师要打招呼。", "pinyin": "Jiàndào lǎoshī yào dǎ zhāohu.", "meaningVi": "Gặp giáo viên phải chào hỏi."}],
    "hsk4_116": [{"chinese": "我们队打败了对手。", "pinyin": "Wǒmen duì dǎbàile duìshǒu.", "meaningVi": "Đội chúng tôi đã đánh bại đối thủ."}],
    "hsk4_117": [{"chinese": "他利用暑假打工赚钱。", "pinyin": "Tā lìyòng shǔjià dǎgōng zhuànqián.", "meaningVi": "Anh ấy tận dụng kỳ nghỉ hè đi làm thêm kiếm tiền."}],
    "hsk4_118": [{"chinese": "打扰一下，请问几点了？", "pinyin": "Dǎrǎo yíxià, qǐngwèn jǐ diǎn le?", "meaningVi": "Xin làm phiền một chút, xin hỏi mấy giờ rồi?"}],
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
