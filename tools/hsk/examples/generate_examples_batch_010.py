"""P5.10.3 (continued) -- Batch 010 (continues immediately after
examples_batch_009.json; entirely within HSK4).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch:
  - 订 (dìng, "to book/order") vs 定 (dìng, "to fix/determine"): same
    pinyin, different characters -- kept in separate natural sentences
    (订机票 vs 定计划) so neither could be confused with the other.
  - 赶 (gǎn, "to hurry/catch up") vs 敢 (gǎn, "to dare") vs 感 (gǎn,
    bound "feeling" suffix): THREE different characters sharing one
    pinyin syllable. Each kept in its own unambiguous natural
    construction/compound (赶时间 / 不敢 / 安全感) -- no sentence could
    be mistaken for demonstrating a different one of the three.
  - 赶紧 (gǎnjǐn) vs 赶快 (gǎnkuài), both "hurry up": genuine near-
    synonyms, each with its own natural sentence, not forced into an
    artificial contrast.
  - 改 (gǎi, "to correct/change") vs 改变 (gǎibiàn, "to change/
    transform"): kept structurally distinct (small correction vs.
    broader transformation sense).
  - 父女/父子 (fùnǚ/fùzǐ, "father-daughter"/"father-son" kinship
    pairs) and 父亲 (fùqīn, "father"): each demonstrates its own
    distinct relational sense rather than reusing one template.

Usage:
    python generate_examples_batch_010.py --dry-run
    python generate_examples_batch_010.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 10
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_010.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_119": [{"chinese": "请帮我打印这份文件。", "pinyin": "Qǐng bāng wǒ dǎyìn zhè fèn wénjiàn.", "meaningVi": "Xin giúp tôi in tài liệu này."}],
    "hsk4_120": [{"chinese": "打印机没有纸了。", "pinyin": "Dǎyìnjī méiyǒu zhǐ le.", "meaningVi": "Máy in hết giấy rồi."}],
    "hsk4_121": [{"chinese": "这些衣服在打折。", "pinyin": "Zhèxiē yīfu zài dǎzhé.", "meaningVi": "Những bộ quần áo này đang giảm giá."}],
    "hsk4_122": [{"chinese": "孩子怕打针。", "pinyin": "Háizi pà dǎzhēn.", "meaningVi": "Đứa trẻ sợ tiêm."}],
    "hsk4_123": [{"chinese": "我们坐大巴去旅游。", "pinyin": "Wǒmen zuò dàbā qù lǚyóu.", "meaningVi": "Chúng tôi đi xe khách đi du lịch."}],
    "hsk4_124": [{"chinese": "新方法大大提高了效率。", "pinyin": "Xīn fāngfǎ dàdà tígāole xiàolǜ.", "meaningVi": "Phương pháp mới đã nâng cao hiệu suất đáng kể."}],
    "hsk4_125": [{"chinese": "大夫，我最近总是头疼。", "pinyin": "Dàifu, wǒ zuìjìn zǒngshì tóuténg.", "meaningVi": "Bác sĩ ơi, gần đây tôi luôn bị đau đầu."}],
    "hsk4_126": [{"chinese": "工厂排放了大量废气。", "pinyin": "Gōngchǎng páifàngle dàliàng fèiqì.", "meaningVi": "Nhà máy thải ra lượng lớn khí thải."}],
    "hsk4_127": [{"chinese": "他获得了这次大赛的冠军。", "pinyin": "Tā huòdéle zhè cì dàsài de guànjūn.", "meaningVi": "Anh ấy đã giành chức vô địch trong cuộc thi lớn này."}],
    "hsk4_128": [{"chinese": "我们在酒店大厅见面吧。", "pinyin": "Wǒmen zài jiǔdiàn dàtīng jiànmiàn ba.", "meaningVi": "Chúng ta gặp nhau ở sảnh khách sạn nhé."}],
    "hsk4_129": [{"chinese": "现在大约六点。", "pinyin": "Xiànzài dàyuē liù diǎn.", "meaningVi": "Bây giờ khoảng sáu giờ."}],
    "hsk4_130": [{"chinese": "我们应该保护大自然。", "pinyin": "Wǒmen yīnggāi bǎohù dàzìrán.", "meaningVi": "Chúng ta nên bảo vệ thiên nhiên."}],
    "hsk4_132": [{"chinese": "他戴着一副眼镜。", "pinyin": "Tā dàizhe yí fù yǎnjìng.", "meaningVi": "Anh ấy đeo một cặp kính."}],
    "hsk4_133": [{"chinese": "请把苹果放进袋子里。", "pinyin": "Qǐng bǎ píngguǒ fàngjìn dàizi lǐ.", "meaningVi": "Xin cho táo vào túi."}],
    "hsk4_134": [{"chinese": "他在政府单位工作。", "pinyin": "Tā zài zhèngfǔ dānwèi gōngzuò.", "meaningVi": "Anh ấy làm việc ở cơ quan nhà nước."}],
    "hsk4_136": [{"chinese": "当时我还不认识他。", "pinyin": "Dāngshí wǒ hái bú rènshi tā.", "meaningVi": "Lúc đó tôi vẫn chưa quen biết anh ấy."}],
    "hsk4_137": [{"chinese": "小心，这把刀很快。", "pinyin": "Xiǎoxīn, zhè bǎ dāo hěn kuài.", "meaningVi": "Cẩn thận, con dao này rất sắc."}],
    "hsk4_141": [{"chinese": "你到底想说什么？", "pinyin": "Nǐ dàodǐ xiǎng shuō shénme?", "meaningVi": "Rốt cuộc bạn muốn nói gì?"}],
    "hsk4_142": [{"chinese": "我们期待春天的到来。", "pinyin": "Wǒmen qīdài chūntiān de dàolái.", "meaningVi": "Chúng tôi mong chờ mùa xuân đến."}],
    "hsk4_143": [{"chinese": "这条道路正在维修。", "pinyin": "Zhè tiáo dàolù zhèngzài wéixiū.", "meaningVi": "Con đường này đang được sửa chữa."}],
    "hsk4_144": [{"chinese": "他向我道歉了。", "pinyin": "Tā xiàng wǒ dàoqiàn le.", "meaningVi": "Anh ấy đã xin lỗi tôi."}],
    "hsk4_145": [{"chinese": "他考了满分，非常得意。", "pinyin": "Tā kǎole mǎnfēn, fēicháng déyì.", "meaningVi": "Anh ấy thi được điểm tuyệt đối, rất đắc ý."}],
    "hsk4_146": [{"chinese": "请到三号口登机。", "pinyin": "Qǐng dào sān hào kǒu dēngjī.", "meaningVi": "Xin lên máy bay tại cửa số ba."}],
    "hsk4_148": [{"chinese": "等到放假，我们就去旅行。", "pinyin": "Děngdào fàngjià, wǒmen jiù qù lǚxíng.", "meaningVi": "Đợi đến khi nghỉ lễ, chúng ta sẽ đi du lịch."}],
    "hsk4_150": [{"chinese": "这家店以低价出售商品。", "pinyin": "Zhè jiā diàn yǐ dījià chūshòu shāngpǐn.", "meaningVi": "Cửa hàng này bán hàng với giá thấp."}],
    "hsk4_151": [{"chinese": "食物需要在低温下保存。", "pinyin": "Shíwù xūyào zài dīwēn xià bǎocún.", "meaningVi": "Thực phẩm cần được bảo quản ở nhiệt độ thấp."}],
    "hsk4_152": [{"chinese": "今天的气温低于零度。", "pinyin": "Jīntiān de qìwēn dīyú líng dù.", "meaningVi": "Nhiệt độ hôm nay thấp hơn không độ."}],
    "hsk4_153": [{"chinese": "这是杯子的底。", "pinyin": "Zhè shì bēizi de dǐ.", "meaningVi": "Đây là đáy cốc."}],
    "hsk4_154": [{"chinese": "猫躲在床底下。", "pinyin": "Māo duǒ zài chuáng dǐxia.", "meaningVi": "Con mèo trốn dưới gầm giường."}],
    "hsk4_155": [{"chinese": "地球是我们共同的家园。", "pinyin": "Dìqiú shì wǒmen gòngtóng de jiāyuán.", "meaningVi": "Trái đất là ngôi nhà chung của chúng ta."}],
    "hsk4_156": [{"chinese": "请告诉我你的地址。", "pinyin": "Qǐng gàosu wǒ nǐ de dìzhǐ.", "meaningVi": "Xin cho tôi biết địa chỉ của bạn."}],
    "hsk4_157": [{"chinese": "老师正在点名。", "pinyin": "Lǎoshī zhèngzài diǎnmíng.", "meaningVi": "Giáo viên đang điểm danh."}],
    "hsk4_158": [{"chinese": "他点头表示明白了。", "pinyin": "Tā diǎntóu biǎoshì míngbai le.", "meaningVi": "Anh ấy gật đầu biểu thị đã hiểu."}],
    "hsk4_159": [{"chinese": "他骑电动车上班。", "pinyin": "Tā qí diàndòngchē shàngbān.", "meaningVi": "Anh ấy đi xe điện đi làm."}],
    "hsk4_160": [{"chinese": "这部电视剧很受欢迎。", "pinyin": "Zhè bù diànshìjù hěn shòu huānyíng.", "meaningVi": "Bộ phim truyền hình này rất được yêu thích."}],
    "hsk4_161": [{"chinese": "他的手机掉进了水里。", "pinyin": "Tā de shǒujī diàojìnle shuǐ lǐ.", "meaningVi": "Điện thoại của anh ấy rơi xuống nước."}],
    "hsk4_162": [{"chinese": "警方正在调查这起事故。", "pinyin": "Jǐngfāng zhèngzài diàochá zhè qǐ shìgù.", "meaningVi": "Cảnh sát đang điều tra vụ tai nạn này."}],
    "hsk4_163": [{"chinese": "我订了一张明天的机票。", "pinyin": "Wǒ dìngle yì zhāng míngtiān de jīpiào.", "meaningVi": "Tôi đã đặt một vé máy bay cho ngày mai."}],
    "hsk4_164": [{"chinese": "我们已经定好了计划。", "pinyin": "Wǒmen yǐjīng dìnghǎole jìhuà.", "meaningVi": "Chúng tôi đã xác định xong kế hoạch."}],
    "hsk4_165": [{"chinese": "他住在城市的东部。", "pinyin": "Tā zhù zài chéngshì de dōngbù.", "meaningVi": "Anh ấy sống ở phía đông thành phố."}],
    "hsk4_166": [{"chinese": "我们坐动车回家。", "pinyin": "Wǒmen zuò dòngchē huí jiā.", "meaningVi": "Chúng tôi đi tàu cao tốc về nhà."}],
    "hsk4_167": [{"chinese": "请注意他的动作。", "pinyin": "Qǐng zhùyì tā de dòngzuò.", "meaningVi": "Xin chú ý động tác của anh ấy."}],
    "hsk4_168": [{"chinese": "这本书受到读者的喜欢。", "pinyin": "Zhè běn shū shòudào dúzhě de xǐhuan.", "meaningVi": "Cuốn sách này được độc giả yêu thích."}],
    "hsk4_169": [{"chinese": "上班路上堵车很严重。", "pinyin": "Shàngbān lùshang dǔchē hěn yánzhòng.", "meaningVi": "Trên đường đi làm bị kẹt xe rất nghiêm trọng."}],
    "hsk4_170": [{"chinese": "我们去海边度假。", "pinyin": "Wǒmen qù hǎibiān dùjià.", "meaningVi": "Chúng tôi đi biển nghỉ dưỡng."}],
    "hsk4_171": [{"chinese": "我肚子有点儿疼。", "pinyin": "Wǒ dùzi yǒudiǎnr téng.", "meaningVi": "Bụng tôi hơi đau."}],
    "hsk4_172": [{"chinese": "他给我发了一条短信。", "pinyin": "Tā gěi wǒ fāle yì tiáo duǎnxìn.", "meaningVi": "Anh ấy đã gửi cho tôi một tin nhắn."}],
    "hsk4_174": [{"chinese": "请先了解对方的想法。", "pinyin": "Qǐng xiān liǎojiě duìfāng de xiǎngfǎ.", "meaningVi": "Xin tìm hiểu suy nghĩ của đối phương trước."}],
    "hsk4_175": [{"chinese": "银行就在马路对面。", "pinyin": "Yínháng jiù zài mǎlù duìmiàn.", "meaningVi": "Ngân hàng ở ngay phía đối diện đường."}],
    "hsk4_176": [{"chinese": "对于这个问题，大家有不同的看法。", "pinyin": "Duìyú zhège wèntí, dàjiā yǒu bùtóng de kànfǎ.", "meaningVi": "Đối với vấn đề này, mọi người có những quan điểm khác nhau."}],
    "hsk4_177": [{"chinese": "每个队员都很努力。", "pinyin": "Měi gè duìyuán dōu hěn nǔlì.", "meaningVi": "Mỗi thành viên trong đội đều rất nỗ lực."}],
    "hsk4_178": [{"chinese": "他被选为队长。", "pinyin": "Tā bèi xuǎn wéi duìzhǎng.", "meaningVi": "Anh ấy được bầu làm đội trưởng."}],
    "hsk4_180": [{"chinese": "这里的风景多么美丽啊！", "pinyin": "Zhèlǐ de fēngjǐng duōme měilì a!", "meaningVi": "Phong cảnh ở đây đẹp biết bao!"}],
    "hsk4_181": [{"chinese": "多数人同意这个方案。", "pinyin": "Duōshù rén tóngyì zhège fāng'àn.", "meaningVi": "Đa số mọi người đồng ý với phương án này."}],
    "hsk4_182": [{"chinese": "这里的商品种类多样。", "pinyin": "Zhèlǐ de shāngpǐn zhǒnglèi duōyàng.", "meaningVi": "Hàng hóa ở đây rất đa dạng chủng loại."}],
    "hsk4_183": [{"chinese": "学习不是为了考试，而是为了成长。", "pinyin": "Xuéxí bú shì wèile kǎoshì, ér shì wèile chéngzhǎng.", "meaningVi": "Học tập không phải vì thi cử, mà là vì sự trưởng thành."}],
    "hsk4_184": [{"chinese": "这是一部儿童电影。", "pinyin": "Zhè shì yí bù értóng diànyǐng.", "meaningVi": "Đây là một bộ phim thiếu nhi."}],
    "hsk4_185": [{"chinese": "手机发出了提示音。", "pinyin": "Shǒujī fāchūle tíshì yīn.", "meaningVi": "Điện thoại phát ra tiếng thông báo."}],
    "hsk4_186": [{"chinese": "请把文件发送给我。", "pinyin": "Qǐng bǎ wénjiàn fāsòng gěi wǒ.", "meaningVi": "Xin gửi tài liệu cho tôi."}],
    "hsk4_187": [{"chinese": "我们要依法办事。", "pinyin": "Wǒmen yào yī fǎ bànshì.", "meaningVi": "Chúng ta phải làm việc theo pháp luật."}],
    "hsk4_188": [{"chinese": "每个人都应该遵守法律。", "pinyin": "Měi gè rén dōu yīnggāi zūnshǒu fǎlǜ.", "meaningVi": "Mỗi người đều nên tuân thủ pháp luật."}],
    "hsk4_191": [{"chinese": "别为这点小事烦恼。", "pinyin": "Bié wèi zhè diǎn xiǎoshì fánnǎo.", "meaningVi": "Đừng phiền não vì chuyện nhỏ này."}],
    "hsk4_192": [{"chinese": "很多人反对这个计划。", "pinyin": "Hěn duō rén fǎnduì zhège jìhuà.", "meaningVi": "Rất nhiều người phản đối kế hoạch này."}],
    "hsk4_193": [{"chinese": "他在很多方面都很优秀。", "pinyin": "Tā zài hěn duō fāngmiàn dōu hěn yōuxiù.", "meaningVi": "Anh ấy xuất sắc ở nhiều phương diện."}],
    "hsk4_194": [{"chinese": "每个人的学习方式都不一样。", "pinyin": "Měi gè rén de xuéxí fāngshì dōu bù yíyàng.", "meaningVi": "Cách học của mỗi người đều khác nhau."}],
    "hsk4_195": [{"chinese": "我的房东人很好。", "pinyin": "Wǒ de fángdōng rén hěn hǎo.", "meaningVi": "Chủ nhà của tôi rất tốt bụng."}],
    "hsk4_196": [{"chinese": "这个月的房租还没交。", "pinyin": "Zhège yuè de fángzū hái méi jiāo.", "meaningVi": "Tiền thuê nhà tháng này vẫn chưa nộp."}],
    "hsk4_197": [{"chinese": "无论多难，都不要放弃。", "pinyin": "Wúlùn duō nán, dōu búyào fàngqì.", "meaningVi": "Dù khó khăn đến đâu, cũng đừng bỏ cuộc."}],
    "hsk4_198": [{"chinese": "周末我喜欢在家放松。", "pinyin": "Zhōumò wǒ xǐhuan zài jiā fàngsōng.", "meaningVi": "Cuối tuần tôi thích ở nhà thư giãn."}],
    "hsk4_200": [{"chinese": "这次旅行的费用不低。", "pinyin": "Zhè cì lǚxíng de fèiyong bù dī.", "meaningVi": "Chi phí của chuyến du lịch lần này không thấp."}],
    "hsk4_201": [{"chinese": "他这次考试的分数很高。", "pinyin": "Tā zhè cì kǎoshì de fēnshù hěn gāo.", "meaningVi": "Điểm thi lần này của anh ấy rất cao."}],
    "hsk4_202": [{"chinese": "这门课分为三个部分。", "pinyin": "Zhè mén kè fēnwéi sān gè bùfen.", "meaningVi": "Môn học này được chia thành ba phần."}],
    "hsk4_203": [{"chinese": "请给我一份报纸。", "pinyin": "Qǐng gěi wǒ yí fèn bàozhǐ.", "meaningVi": "Xin cho tôi một tờ báo."}],
    "hsk4_204": [{"chinese": "他的经验很丰富。", "pinyin": "Tā de jīngyàn hěn fēngfù.", "meaningVi": "Kinh nghiệm của anh ấy rất phong phú."}],
    "hsk4_205": [{"chinese": "这里的风景真美。", "pinyin": "Zhèlǐ de fēngjǐng zhēn měi.", "meaningVi": "Phong cảnh ở đây thật đẹp."}],
    "hsk4_206": [{"chinese": "快点走，否则要迟到了。", "pinyin": "Kuài diǎn zǒu, fǒuzé yào chídào le.", "meaningVi": "Đi nhanh lên, nếu không sẽ muộn."}],
    "hsk4_207": [{"chinese": "墙上挂着一幅画。", "pinyin": "Qiáng shàng guàzhe yì fú huà.", "meaningVi": "Trên tường treo một bức tranh."}],
    "hsk4_208": [{"chinese": "这个答案符合要求。", "pinyin": "Zhège dá'àn fúhé yāoqiú.", "meaningVi": "Đáp án này phù hợp với yêu cầu."}],
    "hsk4_209": [{"chinese": "谁来付钱？", "pinyin": "Shéi lái fù qián?", "meaningVi": "Ai trả tiền đây?"}],
    "hsk4_210": [{"chinese": "我的父母都很爱我。", "pinyin": "Wǒ de fùmǔ dōu hěn ài wǒ.", "meaningVi": "Cha mẹ tôi đều rất yêu tôi."}],
    "hsk4_211": [{"chinese": "他们是一对父女。", "pinyin": "Tāmen shì yí duì fùnǚ.", "meaningVi": "Họ là một cặp cha con (cha và con gái)."}],
    "hsk4_212": [{"chinese": "我父亲是一名工程师。", "pinyin": "Wǒ fùqīn shì yì míng gōngchéngshī.", "meaningVi": "Cha tôi là một kỹ sư."}],
    "hsk4_213": [{"chinese": "请帮我复印这份材料。", "pinyin": "Qǐng bāng wǒ fùyìn zhè fèn cáiliào.", "meaningVi": "Xin giúp tôi photo tài liệu này."}],
    "hsk4_214": [{"chinese": "这个问题很复杂。", "pinyin": "Zhège wèntí hěn fùzá.", "meaningVi": "Vấn đề này rất phức tạp."}],
    "hsk4_216": [{"chinese": "他是这个项目的负责人。", "pinyin": "Tā shì zhège xiàngmù de fùzérén.", "meaningVi": "Anh ấy là người phụ trách dự án này."}],
    "hsk4_217": [{"chinese": "他们父子俩关系很好。", "pinyin": "Tāmen fùzǐ liǎ guānxi hěn hǎo.", "meaningVi": "Hai cha con họ quan hệ rất tốt."}],
    "hsk4_218": [{"chinese": "请把这句话改一下。", "pinyin": "Qǐng bǎ zhè jù huà gǎi yíxià.", "meaningVi": "Xin sửa câu này lại."}],
    "hsk4_219": [{"chinese": "他的想法改变了很多。", "pinyin": "Tā de xiǎngfǎ gǎibiànle hěn duō.", "meaningVi": "Suy nghĩ của anh ấy đã thay đổi rất nhiều."}],
    "hsk4_221": [{"chinese": "大家一起干杯吧！", "pinyin": "Dàjiā yìqǐ gānbēi ba!", "meaningVi": "Mọi người cùng cạn ly đi!"}],
    "hsk4_222": [{"chinese": "我们赶时间，快点走吧。", "pinyin": "Wǒmen gǎn shíjiān, kuài diǎn zǒu ba.", "meaningVi": "Chúng ta đang gấp thời gian, đi nhanh lên đi."}],
    "hsk4_223": [{"chinese": "他不敢一个人去。", "pinyin": "Tā bù gǎn yí gè rén qù.", "meaningVi": "Anh ấy không dám đi một mình."}],
    "hsk4_224": [{"chinese": "他对这份工作很有安全感。", "pinyin": "Tā duì zhè fèn gōngzuò hěn yǒu ānquángǎn.", "meaningVi": "Anh ấy cảm thấy rất an toàn với công việc này."}],
    "hsk4_226": [{"chinese": "天要黑了，我们赶紧回家吧。", "pinyin": "Tiān yào hēi le, wǒmen gǎnjǐn huí jiā ba.", "meaningVi": "Trời sắp tối rồi, chúng ta mau về nhà thôi."}],
    "hsk4_228": [{"chinese": "快迟到了，赶快出门吧。", "pinyin": "Kuài chídào le, gǎnkuài chūmén ba.", "meaningVi": "Sắp muộn rồi, mau ra khỏi nhà đi."}],
    "hsk4_229": [{"chinese": "他们的感情很深。", "pinyin": "Tāmen de gǎnqíng hěn shēn.", "meaningVi": "Tình cảm của họ rất sâu đậm."}],
    "hsk4_230": [{"chinese": "这是一个很感人的故事。", "pinyin": "Zhè shì yí gè hěn gǎnrén de gùshi.", "meaningVi": "Đây là một câu chuyện rất cảm động."}],
    "hsk4_231": [{"chinese": "我差点没赶上火车。", "pinyin": "Wǒ chàdiǎn méi gǎnshàng huǒchē.", "meaningVi": "Tôi suýt nữa không kịp chuyến tàu."}],
    "hsk4_233": [{"chinese": "非常感谢你的帮助。", "pinyin": "Fēicháng gǎnxiè nǐ de bāngzhù.", "meaningVi": "Rất cảm ơn sự giúp đỡ của bạn."}],
    "hsk4_234": [{"chinese": "农民们正在地里干活儿。", "pinyin": "Nóngmínmen zhèngzài dì lǐ gànhuór.", "meaningVi": "Những người nông dân đang làm việc ở ruộng."}],
    "hsk4_235": [{"chinese": "她从小学习弹钢琴。", "pinyin": "Tā cóngxiǎo xuéxí tán gāngqín.", "meaningVi": "Cô ấy học đàn piano từ nhỏ."}],
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
