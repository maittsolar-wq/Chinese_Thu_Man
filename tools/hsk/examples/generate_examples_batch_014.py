"""P5.10.3 (continued) -- Batch 014 (continues immediately after
examples_batch_013.json; entirely within HSK4).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch:
  - 弹 (tán, "to play [an instrument]/to flick") vs 谈 (tán, "to talk/
    discuss"): identical pinyin, different characters, not caught by
    the mechanical tier system (different `word` strings) -- given
    clearly distinct sentences (他会弹吉他。 vs 我们谈了很久。), and
    the instrument in 弹's example (吉他, guitar) was deliberately
    chosen to differ from the unrelated record 琴 (qín, batch 013,
    hsk4_585, "她会弹琴。") so no two sentences read as templated
    variants of each other.
  - 熟 (shú/shóu, dual reading "ripe/cooked" or "familiar/well-done")
    demonstrated with the unambiguous shú "ripe" sense (苹果...熟了)
    distinct from the separate 熟悉 (shúxi, "familiar") record.
  - 少见/少量/少数 (shǎo, 3rd tone) vs 少年 (shào, 4th tone): distinct
    tones and meanings, each given its own natural sentence so the
    tone contrast is unambiguous in context.
  - Productive-root families kept structurally distinct (no shared
    template): 仍/仍然 (réng, near-synonyms); 日常/日记/日期/日子
    (rì+X); 入/入口/入学/入住 (rù+X); 稍/稍微 (shāo, near-synonyms);
    食品/食堂/食物 (shí+X); 使/使馆/使用 (shǐ+X); 收费/收拾/收听
    (shōu+X); 首/首都 (shǒu+X); 顺便/顺利/顺序 (shùn+X); 孙女/孙子
    (sūn+X); 抬/抬头 (tái+X).

Usage:
    python generate_examples_batch_014.py --dry-run
    python generate_examples_batch_014.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 14
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_014.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_606": [{"chinese": "他很努力，却没有成功。", "pinyin": "Tā hěn nǔlì, què méiyǒu chénggōng.", "meaningVi": "Anh ấy rất nỗ lực, nhưng lại không thành công."}],
    "hsk4_607": [{"chinese": "这个方法确实有效。", "pinyin": "Zhège fāngfǎ quèshí yǒuxiào.", "meaningVi": "Phương pháp này quả thật có hiệu quả."}],
    "hsk4_608": [{"chinese": "他很想去，然而没有时间。", "pinyin": "Tā hěn xiǎng qù, rán'ér méiyǒu shíjiān.", "meaningVi": "Anh ấy rất muốn đi, tuy nhiên không có thời gian."}],
    "hsk4_610": [{"chinese": "人生充满了各种可能。", "pinyin": "Rénshēng chōngmǎnle gèzhǒng kěnéng.", "meaningVi": "Cuộc đời tràn đầy những khả năng khác nhau."}],
    "hsk4_611": [{"chinese": "今天参加会议的人数不多。", "pinyin": "Jīntiān cānjiā huìyì de rénshù bù duō.", "meaningVi": "Số người tham gia cuộc họp hôm nay không nhiều."}],
    "hsk4_612": [{"chinese": "工作人员正在准备材料。", "pinyin": "Gōngzuò rényuán zhèngzài zhǔnbèi cáiliào.", "meaningVi": "Nhân viên đang chuẩn bị tài liệu."}],
    "hsk4_613": [{"chinese": "任何人都可以参加。", "pinyin": "Rènhé rén dōu kěyǐ cānjiā.", "meaningVi": "Bất kỳ ai cũng có thể tham gia."}],
    "hsk4_614": [{"chinese": "这项任务由我负责。", "pinyin": "Zhè xiàng rènwu yóu wǒ fùzé.", "meaningVi": "Nhiệm vụ này do tôi phụ trách."}],
    "hsk4_615": [{"chinese": "别把垃圾扔在地上。", "pinyin": "Bié bǎ lājī rēng zài dìshang.", "meaningVi": "Đừng vứt rác xuống đất."}],
    "hsk4_616": [{"chinese": "他仍住在老家。", "pinyin": "Tā réng zhù zài lǎojiā.", "meaningVi": "Anh ấy vẫn sống ở quê nhà."}],
    "hsk4_617": [{"chinese": "虽然下雨，他仍然去跑步了。", "pinyin": "Suīrán xiàyǔ, tā réngrán qù pǎobù le.", "meaningVi": "Mặc dù trời mưa, anh ấy vẫn đi chạy bộ."}],
    "hsk4_618": [{"chinese": "这是我们的日常工作。", "pinyin": "Zhè shì wǒmen de rìcháng gōngzuò.", "meaningVi": "Đây là công việc hàng ngày của chúng tôi."}],
    "hsk4_619": [{"chinese": "她每天都写日记。", "pinyin": "Tā měitiān dōu xiě rìjì.", "meaningVi": "Cô ấy mỗi ngày đều viết nhật ký."}],
    "hsk4_620": [{"chinese": "请确认一下出发日期。", "pinyin": "Qǐng quèrèn yíxià chūfā rìqī.", "meaningVi": "Xin hãy xác nhận ngày xuất phát."}],
    "hsk4_621": [{"chinese": "我们的日子越过越好。", "pinyin": "Wǒmen de rìzi yuè guò yuè hǎo.", "meaningVi": "Cuộc sống của chúng tôi càng ngày càng tốt hơn."}],
    "hsk4_622": [{"chinese": "请按顺序入场。", "pinyin": "Qǐng àn shùnxù rùchǎng.", "meaningVi": "Xin hãy vào sảnh theo thứ tự."}],
    "hsk4_623": [{"chinese": "入口在大楼的左边。", "pinyin": "Rùkǒu zài dàlóu de zuǒbiān.", "meaningVi": "Lối vào ở phía bên trái tòa nhà."}],
    "hsk4_624": [{"chinese": "他今年九月入学。", "pinyin": "Tā jīnnián jiǔ yuè rùxué.", "meaningVi": "Năm nay anh ấy nhập học vào tháng chín."}],
    "hsk4_625": [{"chinese": "我们下午三点入住酒店。", "pinyin": "Wǒmen xiàwǔ sān diǎn rùzhù jiǔdiàn.", "meaningVi": "Chúng tôi nhận phòng khách sạn lúc ba giờ chiều."}],
    "hsk4_626": [{"chinese": "晚饭后我们去公园散步。", "pinyin": "Wǎnfàn hòu wǒmen qù gōngyuán sànbù.", "meaningVi": "Sau bữa tối chúng tôi đi dạo ở công viên."}],
    "hsk4_627": [{"chinese": "请扫码付款。", "pinyin": "Qǐng sǎomǎ fùkuǎn.", "meaningVi": "Xin quét mã để thanh toán."}],
    "hsk4_628": [{"chinese": "这片森林很大。", "pinyin": "Zhè piàn sēnlín hěn dà.", "meaningVi": "Khu rừng này rất rộng lớn."}],
    "hsk4_629": [{"chinese": "我们商量一下这件事吧。", "pinyin": "Wǒmen shāngliang yíxià zhè jiàn shì ba.", "meaningVi": "Chúng ta bàn bạc một chút về việc này đi."}],
    "hsk4_630": [{"chinese": "这家店的商品种类很多。", "pinyin": "Zhè jiā diàn de shāngpǐn zhǒnglèi hěn duō.", "meaningVi": "Loại hàng hóa của cửa hàng này rất nhiều."}],
    "hsk4_631": [{"chinese": "听到这个消息她很伤心。", "pinyin": "Tīngdào zhège xiāoxi tā hěn shāngxīn.", "meaningVi": "Nghe được tin này cô ấy rất buồn."}],
    "hsk4_632": [{"chinese": "师傅会上门维修。", "pinyin": "Shīfu huì shàngmén wéixiū.", "meaningVi": "Thợ sẽ đến tận nhà sửa chữa."}],
    "hsk4_633": [{"chinese": "请稍等。", "pinyin": "Qǐng shāo děng.", "meaningVi": "Xin đợi một chút."}],
    "hsk4_634": [{"chinese": "声音稍微大一点。", "pinyin": "Shēngyīn shāowēi dà yìdiǎn.", "meaningVi": "Âm thanh to hơn một chút."}],
    "hsk4_635": [{"chinese": "这种情况很少见。", "pinyin": "Zhè zhǒng qíngkuàng hěn shǎojiàn.", "meaningVi": "Tình huống này rất hiếm thấy."}],
    "hsk4_636": [{"chinese": "只需要少量的材料。", "pinyin": "Zhǐ xūyào shǎoliàng de cáiliào.", "meaningVi": "Chỉ cần một lượng ít nguyên liệu."}],
    "hsk4_637": [{"chinese": "只有少数人同意这个方案。", "pinyin": "Zhǐyǒu shǎoshù rén tóngyì zhège fāng'àn.", "meaningVi": "Chỉ có số ít người đồng ý với phương án này."}],
    "hsk4_638": [{"chinese": "他还是个少年。", "pinyin": "Tā háishi ge shàonián.", "meaningVi": "Cậu ấy vẫn còn là một thiếu niên."}],
    "hsk4_639": [{"chinese": "我们生活在一个多元的社会。", "pinyin": "Wǒmen shēnghuó zài yí gè duōyuán de shèhuì.", "meaningVi": "Chúng ta sống trong một xã hội đa dạng."}],
    "hsk4_640": [{"chinese": "今天气温是三十摄氏度。", "pinyin": "Jīntiān qìwēn shì sānshí shèshìdù.", "meaningVi": "Nhiệt độ hôm nay là ba mươi độ C."}],
    "hsk4_643": [{"chinese": "请出示您的身份证。", "pinyin": "Qǐng chūshì nín de shēnfènzhèng.", "meaningVi": "Xin xuất trình chứng minh thư của bạn."}],
    "hsk4_644": [{"chinese": "他申请了这份工作。", "pinyin": "Tā shēnqǐngle zhè fèn gōngzuò.", "meaningVi": "Anh ấy đã nộp đơn xin công việc này."}],
    "hsk4_645": [{"chinese": "他忙得甚至没时间吃饭。", "pinyin": "Tā máng de shènzhì méi shíjiān chīfàn.", "meaningVi": "Anh ấy bận đến mức thậm chí không có thời gian ăn cơm."}],
    "hsk4_648": [{"chinese": "我们要珍惜生命。", "pinyin": "Wǒmen yào zhēnxī shēngmìng.", "meaningVi": "Chúng ta phải trân trọng sự sống."}],
    "hsk4_649": [{"chinese": "他的生意越做越大。", "pinyin": "Tā de shēngyi yuè zuò yuè dà.", "meaningVi": "Việc kinh doanh của anh ấy càng làm càng lớn."}],
    "hsk4_650": [{"chinese": "他来自广东省。", "pinyin": "Tā láizì Guǎngdōng Shěng.", "meaningVi": "Anh ấy đến từ tỉnh Quảng Đông."}],
    "hsk4_651": [{"chinese": "饭还剩一点儿。", "pinyin": "Fàn hái shèng yìdiǎnr.", "meaningVi": "Cơm vẫn còn thừa một chút."}],
    "hsk4_653": [{"chinese": "这位师傅的手艺很好。", "pinyin": "Zhè wèi shīfu de shǒuyì hěn hǎo.", "meaningVi": "Tay nghề của người thợ này rất giỏi."}],
    "hsk4_654": [{"chinese": "他不想失去这次机会。", "pinyin": "Tā bù xiǎng shīqù zhè cì jīhuì.", "meaningVi": "Anh ấy không muốn mất đi cơ hội lần này."}],
    "hsk4_655": [{"chinese": "他们师生关系很好。", "pinyin": "Tāmen shīshēng guānxi hěn hǎo.", "meaningVi": "Quan hệ thầy trò của họ rất tốt."}],
    "hsk4_657": [{"chinese": "他对结果十分满意。", "pinyin": "Tā duì jiéguǒ shífēn mǎnyì.", "meaningVi": "Anh ấy rất hài lòng với kết quả."}],
    "hsk4_659": [{"chinese": "请按照时间表行动。", "pinyin": "Qǐng ànzhào shíjiānbiǎo xíngdòng.", "meaningVi": "Xin hãy hành động theo lịch trình."}],
    "hsk4_660": [{"chinese": "实际上事情没有那么简单。", "pinyin": "Shíjìshàng shìqing méiyǒu nàme jiǎndān.", "meaningVi": "Thực ra sự việc không đơn giản như vậy."}],
    "hsk4_661": [{"chinese": "这些食品都很新鲜。", "pinyin": "Zhèxiē shípǐn dōu hěn xīnxiān.", "meaningVi": "Những thực phẩm này đều rất tươi."}],
    "hsk4_662": [{"chinese": "我们在食堂吃午饭。", "pinyin": "Wǒmen zài shítáng chī wǔfàn.", "meaningVi": "Chúng tôi ăn trưa ở căng tin."}],
    "hsk4_663": [{"chinese": "冰箱里有很多食物。", "pinyin": "Bīngxiāng lǐ yǒu hěn duō shíwù.", "meaningVi": "Trong tủ lạnh có rất nhiều thức ăn."}],
    "hsk4_665": [{"chinese": "前面就是十字路口。", "pinyin": "Qiánmiàn jiù shì shízì lùkǒu.", "meaningVi": "Phía trước chính là ngã tư."}],
    "hsk4_666": [{"chinese": "这个消息使他很开心。", "pinyin": "Zhège xiāoxi shǐ tā hěn kāixīn.", "meaningVi": "Tin này khiến anh ấy rất vui."}],
    "hsk4_667": [{"chinese": "他去使馆办签证。", "pinyin": "Tā qù shǐguǎn bàn qiānzhèng.", "meaningVi": "Anh ấy đến đại sứ quán làm visa."}],
    "hsk4_668": [{"chinese": "请正确使用这个工具。", "pinyin": "Qǐng zhèngquè shǐyòng zhège gōngjù.", "meaningVi": "Xin hãy sử dụng công cụ này đúng cách."}],
    "hsk4_669": [{"chinese": "妈妈去市场买菜了。", "pinyin": "Māma qù shìchǎng mǎi cài le.", "meaningVi": "Mẹ đã đi chợ mua rau."}],
    "hsk4_670": [{"chinese": "我不知道他是否会来。", "pinyin": "Wǒ bù zhīdào tā shìfǒu huì lái.", "meaningVi": "Tôi không biết anh ấy có đến hay không."}],
    "hsk4_671": [{"chinese": "这份工作很适合你。", "pinyin": "Zhè fèn gōngzuò hěn shìhé nǐ.", "meaningVi": "Công việc này rất phù hợp với bạn."}],
    "hsk4_672": [{"chinese": "我们生活在二十一世纪。", "pinyin": "Wǒmen shēnghuó zài èrshíyī shìjì.", "meaningVi": "Chúng ta đang sống trong thế kỷ hai mươi mốt."}],
    "hsk4_673": [{"chinese": "他发了一个视频给我。", "pinyin": "Tā fāle yí gè shìpín gěi wǒ.", "meaningVi": "Anh ấy đã gửi cho tôi một video."}],
    "hsk4_674": [{"chinese": "我们家离市区不远。", "pinyin": "Wǒmen jiā lí shìqū bù yuǎn.", "meaningVi": "Nhà chúng tôi cách khu trung tâm thành phố không xa."}],
    "hsk4_675": [{"chinese": "这次的试题比较难。", "pinyin": "Zhè cì de shìtí bǐjiào nán.", "meaningVi": "Đề thi lần này khá khó."}],
    "hsk4_676": [{"chinese": "他已经适应了新环境。", "pinyin": "Tā yǐjīng shìyìngle xīn huánjìng.", "meaningVi": "Anh ấy đã thích nghi với môi trường mới."}],
    "hsk4_677": [{"chinese": "这个停车场不收费。", "pinyin": "Zhège tíngchēchǎng bù shōufèi.", "meaningVi": "Bãi đỗ xe này không thu phí."}],
    "hsk4_679": [{"chinese": "我在收拾房间。", "pinyin": "Wǒ zài shōushi fángjiān.", "meaningVi": "Tôi đang dọn dẹp phòng."}],
    "hsk4_680": [{"chinese": "很多人喜欢收听这个节目。", "pinyin": "Hěn duō rén xǐhuan shōutīng zhège jiémù.", "meaningVi": "Rất nhiều người thích nghe chương trình này."}],
    "hsk4_681": [{"chinese": "我会唱这首歌。", "pinyin": "Wǒ huì chàng zhè shǒu gē.", "meaningVi": "Tôi biết hát bài hát này."}],
    "hsk4_682": [{"chinese": "北京是中国的首都。", "pinyin": "Běijīng shì Zhōngguó de shǒudū.", "meaningVi": "Bắc Kinh là thủ đô của Trung Quốc."}],
    "hsk4_684": [{"chinese": "我实在受不了这种天气。", "pinyin": "Wǒ shízài shòubuliǎo zhè zhǒng tiānqì.", "meaningVi": "Tôi thực sự không chịu nổi kiểu thời tiết này."}],
    "hsk4_685": [{"chinese": "售票员帮我找到了座位。", "pinyin": "Shòupiàoyuán bāng wǒ zhǎodàole zuòwèi.", "meaningVi": "Nhân viên bán vé đã giúp tôi tìm được chỗ ngồi."}],
    "hsk4_686": [{"chinese": "他在比赛中受伤了。", "pinyin": "Tā zài bǐsài zhōng shòushāng le.", "meaningVi": "Anh ấy đã bị thương trong trận đấu."}],
    "hsk4_687": [{"chinese": "我们这次比赛输了。", "pinyin": "Wǒmen zhè cì bǐsài shū le.", "meaningVi": "Lần thi đấu này chúng tôi đã thua."}],
    "hsk4_688": [{"chinese": "苹果已经熟了。", "pinyin": "Píngguǒ yǐjīng shú le.", "meaningVi": "Táo đã chín rồi."}],
    "hsk4_689": [{"chinese": "我对这个地方很熟悉。", "pinyin": "Wǒ duì zhège dìfang hěn shúxi.", "meaningVi": "Tôi rất quen thuộc với nơi này."}],
    "hsk4_690": [{"chinese": "暑假我想去旅行。", "pinyin": "Shǔjià wǒ xiǎng qù lǚxíng.", "meaningVi": "Kỳ nghỉ hè tôi muốn đi du lịch."}],
    "hsk4_692": [{"chinese": "参加的人数量比预想的多。", "pinyin": "Cānjiā de rén shùliàng bǐ yùxiǎng de duō.", "meaningVi": "Số lượng người tham gia nhiều hơn dự kiến."}],
    "hsk4_693": [{"chinese": "孩子们在树林里玩耍。", "pinyin": "Háizimen zài shùlín lǐ wánshuǎ.", "meaningVi": "Bọn trẻ đang chơi đùa trong rừng cây."}],
    "hsk4_694": [{"chinese": "请把这些数字加起来。", "pinyin": "Qǐng bǎ zhèxiē shùzì jiā qǐlai.", "meaningVi": "Xin hãy cộng những con số này lại."}],
    "hsk4_695": [{"chinese": "他长得很帅。", "pinyin": "Tā zhǎng de hěn shuài.", "meaningVi": "Anh ấy trông rất đẹp trai."}],
    "hsk4_696": [{"chinese": "我去超市，顺便帮你买点东西。", "pinyin": "Wǒ qù chāoshì, shùnbiàn bāng nǐ mǎi diǎn dōngxi.", "meaningVi": "Tôi đi siêu thị, tiện thể mua giúp bạn ít đồ."}],
    "hsk4_697": [{"chinese": "祝你考试顺利。", "pinyin": "Zhù nǐ kǎoshì shùnlì.", "meaningVi": "Chúc bạn thi cử suôn sẻ."}],
    "hsk4_698": [{"chinese": "请按照顺序排队。", "pinyin": "Qǐng ànzhào shùnxù páiduì.", "meaningVi": "Xin hãy xếp hàng theo thứ tự."}],
    "hsk4_699": [{"chinese": "关于这件事有不同的说法。", "pinyin": "Guānyú zhè jiàn shì yǒu bùtóng de shuōfǎ.", "meaningVi": "Về việc này có nhiều cách nói khác nhau."}],
    "hsk4_701": [{"chinese": "使用前请先看说明书。", "pinyin": "Shǐyòng qián qǐng xiān kàn shuōmíngshū.", "meaningVi": "Trước khi sử dụng xin hãy đọc hướng dẫn sử dụng trước."}],
    "hsk4_702": [{"chinese": "她正在读硕士。", "pinyin": "Tā zhèngzài dú shuòshì.", "meaningVi": "Cô ấy đang học thạc sĩ."}],
    "hsk4_704": [{"chinese": "请注意行车速度。", "pinyin": "Qǐng zhùyì xíngchē sùdù.", "meaningVi": "Xin hãy chú ý tốc độ lái xe."}],
    "hsk4_705": [{"chinese": "这个杯子是塑料做的。", "pinyin": "Zhège bēizi shì sùliào zuò de.", "meaningVi": "Cái cốc này được làm bằng nhựa."}],
    "hsk4_706": [{"chinese": "这个橙子有点酸。", "pinyin": "Zhège chéngzi yǒudiǎn suān.", "meaningVi": "Quả cam này hơi chua."}],
    "hsk4_707": [{"chinese": "我每天早上喝一杯酸奶。", "pinyin": "Wǒ měitiān zǎoshang hē yì bēi suānnǎi.", "meaningVi": "Mỗi sáng tôi uống một cốc sữa chua."}],
    "hsk4_710": [{"chinese": "随着年龄的增长，他变得更成熟了。", "pinyin": "Suízhe niánlíng de zēngzhǎng, tā biàn de gèng chéngshú le.", "meaningVi": "Cùng với tuổi tác tăng lên, anh ấy trở nên chín chắn hơn."}],
    "hsk4_711": [{"chinese": "奶奶很疼爱她的孙女。", "pinyin": "Nǎinai hěn téng'ài tā de sūnnǚ.", "meaningVi": "Bà nội rất yêu thương cháu gái của mình."}],
    "hsk4_712": [{"chinese": "爷爷带着孙子去公园玩。", "pinyin": "Yéye dàizhe sūnzi qù gōngyuán wán.", "meaningVi": "Ông nội đưa cháu trai đi công viên chơi."}],
    "hsk4_715": [{"chinese": "大家一起把桌子抬起来。", "pinyin": "Dàjiā yìqǐ bǎ zhuōzi tái qǐlai.", "meaningVi": "Mọi người cùng nhau nhấc cái bàn lên."}],
    "hsk4_716": [{"chinese": "他抬头看了看天空。", "pinyin": "Tā táitóu kànle kàn tiānkōng.", "meaningVi": "Anh ấy ngẩng đầu nhìn bầu trời."}],
    "hsk4_717": [{"chinese": "他工作的态度很认真。", "pinyin": "Tā gōngzuò de tàidù hěn rènzhēn.", "meaningVi": "Thái độ làm việc của anh ấy rất nghiêm túc."}],
    "hsk4_718": [{"chinese": "他会弹吉他。", "pinyin": "Tā huì tán jítā.", "meaningVi": "Anh ấy biết chơi ghi-ta."}],
    "hsk4_719": [{"chinese": "我们谈了很久。", "pinyin": "Wǒmen tánle hěn jiǔ.", "meaningVi": "Chúng tôi đã nói chuyện rất lâu."}],
    "hsk4_720": [{"chinese": "妈妈煮了一锅汤。", "pinyin": "Māma zhǔle yì guō tāng.", "meaningVi": "Mẹ đã nấu một nồi canh."}],
    "hsk4_721": [{"chinese": "他躺在床上休息。", "pinyin": "Tā tǎng zài chuáng shàng xiūxi.", "meaningVi": "Anh ấy nằm trên giường nghỉ ngơi."}],
    "hsk4_722": [{"chinese": "我去了一趟超市。", "pinyin": "Wǒ qùle yí tàng chāoshì.", "meaningVi": "Tôi đã đi một chuyến đến siêu thị."}],
    "hsk4_723": [{"chinese": "我们讨论了这个问题。", "pinyin": "Wǒmen tǎolùnle zhège wèntí.", "meaningVi": "Chúng tôi đã thảo luận về vấn đề này."}],
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
