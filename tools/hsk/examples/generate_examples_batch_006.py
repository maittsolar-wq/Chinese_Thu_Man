"""P5.10.3 (continued) -- Batch 006 (continues immediately after
examples_batch_005.json; entirely within HSK3).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch (per explicit instruction) to several
HSK3 words with real ambiguity risk despite being classified Tier 1 by
the mechanical tier system (which only catches cross-record homographs/
duplicates, not construction-level ambiguity within a single record):
  - 极 (jí, "extremely"): only natural in the fixed "Adj+极了" pattern
    in modern spoken Mandarin; a bare "极 + Adj" sentence would be
    unnatural/literary, so the example uses "...极了" explicitly.
  - 借 (jiè, "to borrow/to lend" -- genuinely bidirectional in isolation):
    the example uses the explicit "跟...借" (borrow FROM someone)
    construction so the intended direction is unambiguous.
  - 句 (jù, measure word for sentences) vs 句子 (jùzi, "a sentence" as a
    noun) are adjacent production records; examples are written to keep
    the measure-word-usage vs. bare-noun-usage distinction clear so
    neither one's example could be mistaken for demonstrating the other.
  - 记 (jì, "to remember/note") and 季 (jì, "season") share pinyin but
    are different characters/words; each example uses the correct
    distinct character, so no ambiguity for a written-sentence learner.

Usage:
    python generate_examples_batch_006.py --dry-run
    python generate_examples_batch_006.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 6
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_006.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk3_123": [{"chinese": "他们买了一套新房子。", "pinyin": "Tāmen mǎile yí tào xīn fángzi.", "meaningVi": "Họ đã mua một căn nhà mới."}],
    "hsk3_124": [{"chinese": "你把手机放哪儿了？", "pinyin": "Nǐ bǎ shǒujī fàng nǎr le?", "meaningVi": "Bạn để điện thoại ở đâu rồi?"}],
    "hsk3_125": [{"chinese": "我们下周放假。", "pinyin": "Wǒmen xià zhōu fàngjià.", "meaningVi": "Tuần sau chúng tôi được nghỉ."}],
    "hsk3_126": [{"chinese": "你放心，一切都很顺利。", "pinyin": "Nǐ fàngxīn, yíqiè dōu hěn shùnlì.", "meaningVi": "Bạn yên tâm đi, mọi thứ đều thuận lợi."}],
    "hsk3_127": [{"chinese": "弟弟放学后去踢足球。", "pinyin": "Dìdi fàngxué hòu qù tī zúqiú.", "meaningVi": "Em trai sau khi tan học thì đi đá bóng."}],
    "hsk3_128": [{"chinese": "他们决定分开一段时间。", "pinyin": "Tāmen juédìng fēnkāi yí duàn shíjiān.", "meaningVi": "Họ quyết định chia tay một thời gian."}],
    "hsk3_129": [{"chinese": "今天风很大。", "pinyin": "Jīntiān fēng hěn dà.", "meaningVi": "Hôm nay gió rất to."}],
    "hsk3_131": [{"chinese": "他们是一对幸福的夫妻。", "pinyin": "Tāmen shì yí duì xìngfú de fūqī.", "meaningVi": "Họ là một cặp vợ chồng hạnh phúc."}],
    "hsk3_132": [{"chinese": "这家饭店的服务很好。", "pinyin": "Zhè jiā fàndiàn de fúwù hěn hǎo.", "meaningVi": "Dịch vụ của nhà hàng này rất tốt."}],
    "hsk3_133": [{"chinese": "附近有一家超市。", "pinyin": "Fùjìn yǒu yì jiā chāoshì.", "meaningVi": "Gần đây có một siêu thị."}],
    "hsk3_134": [{"chinese": "考试前我要好好复习。", "pinyin": "Kǎoshì qián wǒ yào hǎohǎo fùxí.", "meaningVi": "Trước kỳ thi tôi phải ôn tập thật kỹ."}],
    "hsk3_135": [{"chinese": "我们该走了。", "pinyin": "Wǒmen gāi zǒu le.", "meaningVi": "Chúng ta nên đi rồi."}],
    "hsk3_136": [{"chinese": "房间收拾得很干净。", "pinyin": "Fángjiān shōushi de hěn gānjìng.", "meaningVi": "Phòng được dọn dẹp rất sạch sẽ."}],
    "hsk3_137": [{"chinese": "他对音乐很感兴趣。", "pinyin": "Tā duì yīnyuè hěn gǎn xìngqù.", "meaningVi": "Anh ấy rất có hứng thú với âm nhạc."}],
    "hsk3_138": [{"chinese": "听到这个消息，她感到很高兴。", "pinyin": "Tīngdào zhège xiāoxi, tā gǎndào hěn gāoxìng.", "meaningVi": "Nghe tin này, cô ấy cảm thấy rất vui."}],
    "hsk3_141": [{"chinese": "我刚到家。", "pinyin": "Wǒ gāng dào jiā.", "meaningVi": "Tôi vừa mới về đến nhà."}],
    "hsk3_142": [{"chinese": "刚才是谁给我打电话？", "pinyin": "Gāngcái shì shéi gěi wǒ dǎ diànhuà?", "meaningVi": "Vừa nãy ai gọi điện cho tôi vậy?"}],
    "hsk3_143": [{"chinese": "电影刚刚开始。", "pinyin": "Diànyǐng gānggāng kāishǐ.", "meaningVi": "Bộ phim vừa mới bắt đầu."}],
    "hsk3_144": [{"chinese": "我们坐高铁去上海。", "pinyin": "Wǒmen zuò gāotiě qù Shànghǎi.", "meaningVi": "Chúng tôi đi tàu cao tốc đến Thượng Hải."}],
    "hsk3_146": [{"chinese": "今天比昨天更冷。", "pinyin": "Jīntiān bǐ zuótiān gèng lěng.", "meaningVi": "Hôm nay lạnh hơn hôm qua."}],
    "hsk3_147": [{"chinese": "这个箱子重十公斤。", "pinyin": "Zhège xiāngzi zhòng shí gōngjīn.", "meaningVi": "Cái hộp này nặng mười ki-lô-gam."}],
    "hsk3_148": [{"chinese": "我们晚上去公园散步。", "pinyin": "Wǒmen wǎnshang qù gōngyuán sànbù.", "meaningVi": "Buổi tối chúng tôi đi dạo ở công viên."}],
    "hsk3_149": [{"chinese": "工作日我们都很忙。", "pinyin": "Gōngzuòrì wǒmen dōu hěn máng.", "meaningVi": "Vào ngày làm việc chúng tôi đều rất bận."}],
    "hsk3_150": [{"chinese": "妈妈给我讲了一个故事。", "pinyin": "Māma gěi wǒ jiǎngle yí gè gùshi.", "meaningVi": "Mẹ đã kể cho tôi một câu chuyện."}],
    "hsk3_151": [{"chinese": "外面在刮风。", "pinyin": "Wàimiàn zài guā fēng.", "meaningVi": "Bên ngoài đang có gió thổi."}],
    "hsk3_153": [{"chinese": "睡觉前请把手机关机。", "pinyin": "Shuìjiào qián qǐng bǎ shǒujī guānjī.", "meaningVi": "Trước khi ngủ xin hãy tắt điện thoại."}],
    "hsk3_155": [{"chinese": "父母很关心孩子的学习。", "pinyin": "Fùmǔ hěn guānxīn háizi de xuéxí.", "meaningVi": "Cha mẹ rất quan tâm đến việc học của con cái."}],
    "hsk3_156": [{"chinese": "这是一本关于历史的书。", "pinyin": "Zhè shì yì běn guānyú lìshǐ de shū.", "meaningVi": "Đây là một cuốn sách về lịch sử."}],
    "hsk3_157": [{"chinese": "很多人在关注这个新闻。", "pinyin": "Hěn duō rén zài guānzhù zhège xīnwén.", "meaningVi": "Rất nhiều người đang theo dõi tin tức này."}],
    "hsk3_158": [{"chinese": "越南是一个美丽的国家。", "pinyin": "Yuènán shì yí gè měilì de guójiā.", "meaningVi": "Việt Nam là một đất nước xinh đẹp."}],
    "hsk3_159": [{"chinese": "我们全家一起过节。", "pinyin": "Wǒmen quánjiā yìqǐ guòjié.", "meaningVi": "Cả gia đình tôi cùng nhau đón lễ."}],
    "hsk3_161": [{"chinese": "我们去海边玩吧。", "pinyin": "Wǒmen qù hǎibiān wán ba.", "meaningVi": "Chúng ta đi chơi biển đi."}],
    "hsk3_162": [{"chinese": "她很害怕黑暗。", "pinyin": "Tā hěn hàipà hēi'àn.", "meaningVi": "Cô ấy rất sợ bóng tối."}],
    "hsk3_163": [{"chinese": "公园里有好多人。", "pinyin": "Gōngyuán lǐ yǒu hǎoduō rén.", "meaningVi": "Trong công viên có rất nhiều người."}],
    "hsk3_164": [{"chinese": "好久不见，你还好吗？", "pinyin": "Hǎojiǔ bú jiàn, nǐ hái hǎo ma?", "meaningVi": "Lâu rồi không gặp, bạn vẫn khỏe chứ?"}],
    "hsk3_166": [{"chinese": "请告诉我你的电话号码。", "pinyin": "Qǐng gàosu wǒ nǐ de diànhuà hàomǎ.", "meaningVi": "Xin cho tôi biết số điện thoại của bạn."}],
    "hsk3_167": [{"chinese": "这条河很长。", "pinyin": "Zhè tiáo hé hěn cháng.", "meaningVi": "Con sông này rất dài."}],
    "hsk3_168": [{"chinese": "这双鞋很合适。", "pinyin": "Zhè shuāng xié hěn héshì.", "meaningVi": "Đôi giày này rất vừa vặn."}],
    "hsk3_169": [{"chinese": "老师在黑板上写字。", "pinyin": "Lǎoshī zài hēibǎn shàng xiě zì.", "meaningVi": "Giáo viên viết chữ trên bảng đen."}],
    "hsk3_170": [{"chinese": "请遵守红绿灯。", "pinyin": "Qǐng zūnshǒu hónglǜdēng.", "meaningVi": "Xin hãy tuân thủ đèn giao thông."}],
    "hsk3_171": [{"chinese": "后来他搬到了北京。", "pinyin": "Hòulái tā bāndàole Běijīng.", "meaningVi": "Sau đó anh ấy chuyển đến Bắc Kinh."}],
    "hsk3_172": [{"chinese": "我打算后年结婚。", "pinyin": "Wǒ dǎsuàn hòunián jiéhūn.", "meaningVi": "Tôi định kết hôn vào hai năm nữa."}],
    "hsk3_173": [{"chinese": "后天是我的生日。", "pinyin": "Hòutiān shì wǒ de shēngrì.", "meaningVi": "Ngày kia là sinh nhật của tôi."}],
    "hsk3_174": [{"chinese": "出国旅行需要护照。", "pinyin": "Chūguó lǚxíng xūyào hùzhào.", "meaningVi": "Đi du lịch nước ngoài cần hộ chiếu."}],
    "hsk3_175": [{"chinese": "他们家有一个漂亮的花园。", "pinyin": "Tāmen jiā yǒu yí gè piàoliang de huāyuán.", "meaningVi": "Nhà họ có một khu vườn hoa xinh đẹp."}],
    "hsk3_176": [{"chinese": "他是一位有名的画家。", "pinyin": "Tā shì yí wèi yǒumíng de huàjiā.", "meaningVi": "Anh ấy là một họa sĩ nổi tiếng."}],
    "hsk3_177": [{"chinese": "欢迎来我家玩。", "pinyin": "Huānyíng lái wǒ jiā wán.", "meaningVi": "Hoan nghênh đến nhà tôi chơi."}],
    "hsk3_179": [{"chinese": "这里的环境很安静。", "pinyin": "Zhèlǐ de huánjìng hěn ānjìng.", "meaningVi": "Môi trường ở đây rất yên tĩnh."}],
    "hsk3_180": [{"chinese": "我想换一件大一点的。", "pinyin": "Wǒ xiǎng huàn yí jiàn dà yìdiǎn de.", "meaningVi": "Tôi muốn đổi một cái to hơn một chút."}],
    "hsk3_181": [{"chinese": "秋天树叶变成了黄色。", "pinyin": "Qiūtiān shùyè biànchéngle huángsè.", "meaningVi": "Mùa thu lá cây chuyển sang màu vàng."}],
    "hsk3_182": [{"chinese": "请回答我的问题。", "pinyin": "Qǐng huídá wǒ de wèntí.", "meaningVi": "Xin hãy trả lời câu hỏi của tôi."}],
    "hsk3_184": [{"chinese": "明天上午有一个会议。", "pinyin": "Míngtiān shàngwǔ yǒu yí gè huìyì.", "meaningVi": "Sáng mai có một cuộc họp."}],
    "hsk3_186": [{"chinese": "你可以坐地铁或者坐公交车。", "pinyin": "Nǐ kěyǐ zuò dìtiě huòzhě zuò gōngjiāochē.", "meaningVi": "Bạn có thể đi tàu điện ngầm hoặc đi xe buýt."}],
    "hsk3_187": [{"chinese": "奶奶在院子里养了几只鸡。", "pinyin": "Nǎinai zài yuànzi lǐ yǎngle jǐ zhī jī.", "meaningVi": "Bà nội nuôi vài con gà trong sân."}],
    "hsk3_188": [{"chinese": "他几乎每天都加班。", "pinyin": "Tā jīhū měitiān dōu jiābān.", "meaningVi": "Anh ấy gần như ngày nào cũng làm thêm giờ."}],
    "hsk3_189": [{"chinese": "这是一个很好的机会。", "pinyin": "Zhè shì yí gè hěn hǎo de jīhuì.", "meaningVi": "Đây là một cơ hội rất tốt."}],
    "hsk3_190": [{"chinese": "这个消息好极了。", "pinyin": "Zhège xiāoxi hǎo jí le.", "meaningVi": "Tin này tốt quá đi mất."}],
    "hsk3_192": [{"chinese": "请把这件事记在心里。", "pinyin": "Qǐng bǎ zhè jiàn shì jì zài xīnlǐ.", "meaningVi": "Xin hãy ghi nhớ chuyện này trong lòng."}],
    "hsk3_193": [{"chinese": "现在是雨季。", "pinyin": "Xiànzài shì yǔjì.", "meaningVi": "Bây giờ là mùa mưa."}],
    "hsk3_194": [{"chinese": "春天是我最喜欢的季节。", "pinyin": "Chūntiān shì wǒ zuì xǐhuan de jìjié.", "meaningVi": "Mùa xuân là mùa tôi thích nhất."}],
    "hsk3_195": [{"chinese": "请再给我加点儿水。", "pinyin": "Qǐng zài gěi wǒ jiā diǎnr shuǐ.", "meaningVi": "Xin thêm cho tôi một chút nước."}],
    "hsk3_196": [{"chinese": "假期我打算去旅行。", "pinyin": "Jiàqī wǒ dǎsuàn qù lǚxíng.", "meaningVi": "Kỳ nghỉ tôi định đi du lịch."}],
    "hsk3_197": [{"chinese": "他一直坚持锻炼身体。", "pinyin": "Tā yìzhí jiānchí duànliàn shēntǐ.", "meaningVi": "Anh ấy luôn kiên trì rèn luyện thân thể."}],
    "hsk3_198": [{"chinese": "医生给他做了检查。", "pinyin": "Yīshēng gěi tā zuòle jiǎnchá.", "meaningVi": "Bác sĩ đã khám cho anh ấy."}],
    "hsk3_199": [{"chinese": "这个问题很简单。", "pinyin": "Zhège wèntí hěn jiǎndān.", "meaningVi": "Câu hỏi này rất đơn giản."}],
    "hsk3_200": [{"chinese": "请在这里检票。", "pinyin": "Qǐng zài zhèlǐ jiǎnpiào.", "meaningVi": "Xin kiểm vé tại đây."}],
    "hsk3_201": [{"chinese": "祝你身体健康。", "pinyin": "Zhù nǐ shēntǐ jiànkāng.", "meaningVi": "Chúc bạn sức khỏe dồi dào."}],
    "hsk3_202": [{"chinese": "我们好久没见面了。", "pinyin": "Wǒmen hǎojiǔ méi jiànmiàn le.", "meaningVi": "Chúng ta lâu rồi không gặp mặt."}],
    "hsk3_203": [{"chinese": "老师给我们讲了这个语法。", "pinyin": "Lǎoshī gěi wǒmen jiǎngle zhège yǔfǎ.", "meaningVi": "Giáo viên đã giảng cho chúng tôi ngữ pháp này."}],
    "hsk3_205": [{"chinese": "我的脚有点儿疼。", "pinyin": "Wǒ de jiǎo yǒudiǎnr téng.", "meaningVi": "Chân tôi hơi đau."}],
    "hsk3_206": [{"chinese": "我去机场接你。", "pinyin": "Wǒ qù jīchǎng jiē nǐ.", "meaningVi": "Tôi đi sân bay đón bạn."}],
    "hsk3_207": [{"chinese": "这条街很热闹。", "pinyin": "Zhè tiáo jiē hěn rènao.", "meaningVi": "Con phố này rất náo nhiệt."}],
    "hsk3_209": [{"chinese": "他们下个月结婚。", "pinyin": "Tāmen xià gè yuè jiéhūn.", "meaningVi": "Tháng sau họ kết hôn."}],
    "hsk3_210": [{"chinese": "这个电视节目很有意思。", "pinyin": "Zhège diànshì jiémù hěn yǒu yìsi.", "meaningVi": "Chương trình truyền hình này rất thú vị."}],
    "hsk3_211": [{"chinese": "春节是中国最重要的节日。", "pinyin": "Chūnjié shì Zhōngguó zuì zhòngyào de jiérì.", "meaningVi": "Tết Nguyên Đán là ngày lễ quan trọng nhất của Trung Quốc."}],
    "hsk3_212": [{"chinese": "会议已经结束了。", "pinyin": "Huìyì yǐjīng jiéshù le.", "meaningVi": "Cuộc họp đã kết thúc rồi."}],
    "hsk3_213": [{"chinese": "这个问题不难解决。", "pinyin": "Zhège wèntí bù nán jiějué.", "meaningVi": "Vấn đề này không khó giải quyết."}],
    "hsk3_214": [{"chinese": "她们是亲姐妹。", "pinyin": "Tāmen shì qīn jiěmèi.", "meaningVi": "Họ là chị em ruột."}],
    "hsk3_215": [{"chinese": "我想跟你借一本书。", "pinyin": "Wǒ xiǎng gēn nǐ jiè yì běn shū.", "meaningVi": "Tôi muốn mượn bạn một cuốn sách."}],
    "hsk3_216": [{"chinese": "我买了两斤苹果。", "pinyin": "Wǒ mǎile liǎng jīn píngguǒ.", "meaningVi": "Tôi đã mua hai cân táo."}],
    "hsk3_218": [{"chinese": "他是这家公司的经理。", "pinyin": "Tā shì zhè jiā gōngsī de jīnglǐ.", "meaningVi": "Anh ấy là giám đốc của công ty này."}],
    "hsk3_219": [{"chinese": "他等了很久。", "pinyin": "Tā děngle hěn jiǔ.", "meaningVi": "Anh ấy đã đợi rất lâu."}],
    "hsk3_220": [{"chinese": "他不太会喝酒。", "pinyin": "Tā bú tài huì hē jiǔ.", "meaningVi": "Anh ấy không uống rượu giỏi lắm."}],
    "hsk3_221": [{"chinese": "这件衣服太旧了。", "pinyin": "Zhè jiàn yīfu tài jiù le.", "meaningVi": "Chiếc áo này quá cũ rồi."}],
    "hsk3_222": [{"chinese": "他只说了一句话就走了。", "pinyin": "Tā zhǐ shuōle yí jù huà jiù zǒu le.", "meaningVi": "Anh ấy chỉ nói một câu rồi đi."}],
    "hsk3_223": [{"chinese": "这个句子的语法不对。", "pinyin": "Zhège jùzi de yǔfǎ bú duì.", "meaningVi": "Ngữ pháp của câu này không đúng."}],
    "hsk3_226": [{"chinese": "春天到了，树都开花了。", "pinyin": "Chūntiān dào le, shù dōu kāihuā le.", "meaningVi": "Mùa xuân đến rồi, cây đều nở hoa."}],
    "hsk3_227": [{"chinese": "老板正在开会。", "pinyin": "Lǎobǎn zhèngzài kāihuì.", "meaningVi": "Sếp đang họp."}],
    "hsk3_228": [{"chinese": "请先开机再操作。", "pinyin": "Qǐng xiān kāijī zài cāozuò.", "meaningVi": "Xin bật máy trước rồi mới thao tác."}],
    "hsk3_229": [{"chinese": "今天大家都很开心。", "pinyin": "Jīntiān dàjiā dōu hěn kāixīn.", "meaningVi": "Hôm nay mọi người đều rất vui vẻ."}],
    "hsk3_230": [{"chinese": "看来他不会来了。", "pinyin": "Kànlái tā bú huì lái le.", "meaningVi": "Xem ra anh ấy sẽ không đến nữa."}],
    "hsk3_232": [{"chinese": "我很渴，想喝水。", "pinyin": "Wǒ hěn kě, xiǎng hē shuǐ.", "meaningVi": "Tôi khát quá, muốn uống nước."}],
    "hsk3_233": [{"chinese": "这只小狗很可爱。", "pinyin": "Zhè zhī xiǎo gǒu hěn kě'ài.", "meaningVi": "Con chó con này rất đáng yêu."}],
    "hsk3_234": [{"chinese": "我很想去，可是没有时间。", "pinyin": "Wǒ hěn xiǎng qù, kěshì méiyǒu shíjiān.", "meaningVi": "Tôi rất muốn đi, nhưng không có thời gian."}],
    "hsk3_236": [{"chinese": "请把课本打开。", "pinyin": "Qǐng bǎ kèběn dǎkāi.", "meaningVi": "Xin mở sách giáo khoa ra."}],
    "hsk3_237": [{"chinese": "家里来了几位客人。", "pinyin": "Jiā lǐ láile jǐ wèi kèrén.", "meaningVi": "Nhà có mấy vị khách đến."}],
    "hsk3_238": [{"chinese": "请大家读一下这篇课文。", "pinyin": "Qǐng dàjiā dú yíxià zhè piān kèwén.", "meaningVi": "Mời mọi người đọc bài khóa này."}],
    "hsk3_239": [{"chinese": "房间里的空调坏了。", "pinyin": "Fángjiān lǐ de kōngtiáo huài le.", "meaningVi": "Điều hòa trong phòng bị hỏng rồi."}],
    "hsk3_240": [{"chinese": "孩子哭了起来。", "pinyin": "Háizi kūle qǐlái.", "meaningVi": "Đứa trẻ bắt đầu khóc."}],
    "hsk3_241": [{"chinese": "请给我一双筷子。", "pinyin": "Qǐng gěi wǒ yì shuāng kuàizi.", "meaningVi": "Xin cho tôi một đôi đũa."}],
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
