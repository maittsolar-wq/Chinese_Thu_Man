"""P5.10.3 (continued) -- Batch 018 (continues immediately after
examples_batch_017.json; entirely within HSK5).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch:
  - A dense shū/shù/shǔ homophone cluster, none flagged by the
    mechanical tier system (different `word` strings): 蔬 (shū, in
    蔬菜) / 书 (shū, in 书法/书房/书架) / 输 (shū, in 输入) / 舒 (shū,
    in 舒适) all share the shū syllable; 数 (shù, in 数据) / 树 (shù,
    in 树木) / 束 (shù, the measure word) share shù; 属 (shǔ, in
    属于) is a third, distinct tone. All disambiguated via their own
    well-known compounds.
  - 税 (shuì, "tax") vs 睡 (shuì, "to sleep", in 睡眠): identical
    pinyin, different characters, distinct sentences.
  - 守 (shǒu, "to guard", demonstrated via 坚守) vs 首 (shǒu, already
    published, batch 014 hsk4_681, "song") vs 手 (shǒu, the root of
    手段/手工/手套/手指/随手 in this same batch): three-way homophone,
    each kept in its own natural compound.
  - 长 (cháng, "long/lengthy", in 长处/长度/长久/长途/长远) vs 常
    (cháng, in 常识): identical pinyin, different characters.
  - 似乎 (sìhū, "seems") kept distinct in both meaning and sentence
    structure from the already-published 似的 (batch 017, hsk5_1030).

Sense-alignment note: 提起 (tíqǐ)'s production meaningVi is
specifically the legal sense "khởi tố" (to file/bring a legal case),
not the more common general sense "to mention/bring up" -- the
example was written to match that specific legal sense ("他决定提起
诉讼。") rather than defaulting to the more familiar everyday meaning,
to keep sense alignment with the production data as given (marking
needs_review was considered but the legal sense is unambiguous and
safely authorable).

Self-caught near-template revisions made during drafting (before this
batch was finalized):
  - 长处 (chángchù): first draft "每个人都有自己的长处。" was a
    near-template match against the existing 特点 example (batch 015,
    hsk4_725: "每个人都有自己的特点。", differing by only one word) --
    rewritten to "你应该发挥自己的长处。".
  - 长度 (chángdù): first draft "请测量绳子的长度。" risked reusing
    the "测...长度" pairing already used verbatim in the existing 测
    example (batch 017, hsk5_095: "用尺子测一下长度。") -- rewritten
    to "这条河的长度超过一千公里。".
  - 束 (shù): first draft used a "一束花" flower context that would
    have echoed the existing 鲜花 example (batch 015, hsk4_795: "他送
    了她一束鲜花。") -- rewritten to "这束光很亮。".
  - 图画 (túhuà): first draft "墙上挂着一幅图画。" echoed the "墙上
    挂着..." opener already used for 挂 (batch 014, hsk4_268: "墙上
    挂着一张地图。") -- rewritten to "这幅图画色彩丰富。".

Cross-batch collisions found and fixed during authoring:
  - hsk5_1143 (同一): first draft "我们住在同一个小区。" duplicated
    examples_batch_008.json's hsk3_397 (小区) verbatim -- rewritten to
    "我们俩是同一天出生的。".
  - hsk5_1147 (投): first draft "请把垃圾投进垃圾桶。" was a near-
    template match against 垃圾's own already-published example
    (batch 014, hsk4_448: "请把垃圾扔进垃圾桶。", differing by only
    投/扔) -- rewritten to the "invest" sense instead: "他投了很多钱
    在这个项目上。".
  - hsk5_1124 (天空): first draft "今天的天空很蓝。" was a near-
    template match against the already-published 蓝 example (batch
    007, hsk3_244: "今天天空很蓝。") -- rewritten to "傍晚的天空变成了
    橙红色。".
  - hsk5_1152 (图书): first draft "图书馆里有很多图书。" was a near-
    template match against the already-published 图书馆 example
    (hsk1_190: "图书馆里有很多书。") -- rewritten to "这批图书是上个月
    新到的。". Re-verified against the full pilot+002-017 corpus with
    zero remaining exact duplicates and zero near-template flags.

Other productive-root families kept structurally distinct (no shared
template): 产量/产品/产业 (chǎn+X); 手段/手工/手套/手指 (shǒu+X);
熟练/熟人 (shú+X, distinct from the already-published 熟/熟悉);
随/随后/随时/随手/随意 (suí+X); 特产/特色/特殊/特有/特征 (tè+X);
提交/提起/提升/提问 (tí+X, distinct from the already-published
提/提出/提到/提供/提前/提醒); 体力/体现/体验 (tǐ+X, distinct from
the already-published 体检/体温/体重); 天空/天上 (tiān+X); 挑/挑选
(tiāo+X); 跳高/跳远 (tiào+X); 同情/同一 (tóng+X, distinct from the
already-published 同样); 图画/图书 (tú+X); 推动/推广/推荐 (tuī+X,
distinct from the already-published 推/推迟/推出); 疼痛 vs the
already-published 头痛 (batch 015) kept in separate contexts;
停留 kept distinct from the already-published 停/留.

Usage:
    python generate_examples_batch_018.py --dry-run
    python generate_examples_batch_018.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 18
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_018.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk5_1045": [{"chinese": "他每天收看新闻联播。", "pinyin": "Tā měitiān shōukàn xīnwén liánbō.", "meaningVi": "Anh ấy mỗi ngày đều xem chương trình thời sự."}],
    "hsk5_1046": [{"chinese": "他一直坚守自己的岗位。", "pinyin": "Tā yìzhí jiānshǒu zìjǐ de gǎngwèi.", "meaningVi": "Anh ấy luôn kiên trì giữ vững vị trí của mình."}],
    "hsk5_1047": [{"chinese": "这是他首次来中国。", "pinyin": "Zhè shì tā shǒucì lái Zhōngguó.", "meaningVi": "Đây là lần đầu tiên anh ấy đến Trung Quốc."}],
    "hsk5_1048": [{"chinese": "这是解决问题的有效手段。", "pinyin": "Zhè shì jiějué wèntí de yǒuxiào shǒuduàn.", "meaningVi": "Đây là biện pháp hiệu quả để giải quyết vấn đề."}],
    "hsk5_1049": [{"chinese": "这是纯手工制作的。", "pinyin": "Zhè shì chún shǒugōng zhìzuò de.", "meaningVi": "Đây là được làm thủ công hoàn toàn."}],
    "hsk5_105": [{"chinese": "今年的粮食产量增加了。", "pinyin": "Jīnnián de liángshi chǎnliàng zēngjiā le.", "meaningVi": "Sản lượng lương thực năm nay đã tăng."}],
    "hsk5_1051": [{"chinese": "冬天要戴手套。", "pinyin": "Dōngtiān yào dài shǒutào.", "meaningVi": "Mùa đông phải đeo găng tay."}],
    "hsk5_1052": [{"chinese": "办理手续需要一些时间。", "pinyin": "Bànlǐ shǒuxù xūyào yìxiē shíjiān.", "meaningVi": "Làm thủ tục cần một chút thời gian."}],
    "hsk5_1053": [{"chinese": "他的手指很长。", "pinyin": "Tā de shǒuzhǐ hěn cháng.", "meaningVi": "Ngón tay của anh ấy rất dài."}],
    "hsk5_1054": [{"chinese": "这件商品的售价是一百元。", "pinyin": "Zhè jiàn shāngpǐn de shòujià shì yìbǎi yuán.", "meaningVi": "Giá bán của mặt hàng này là một trăm đồng."}],
    "hsk5_1055": [{"chinese": "多吃蔬菜对身体好。", "pinyin": "Duō chī shūcài duì shēntǐ hǎo.", "meaningVi": "Ăn nhiều rau tốt cho sức khỏe."}],
    "hsk5_1056": [{"chinese": "他的书法写得很好。", "pinyin": "Tā de shūfǎ xiě de hěn hǎo.", "meaningVi": "Thư pháp của anh ấy viết rất đẹp."}],
    "hsk5_1057": [{"chinese": "爸爸在书房看书。", "pinyin": "Bàba zài shūfáng kànshū.", "meaningVi": "Bố đang đọc sách trong phòng đọc sách."}],
    "hsk5_1058": [{"chinese": "书架上摆满了书。", "pinyin": "Shūjià shàng bǎimǎnle shū.", "meaningVi": "Trên giá sách xếp đầy sách."}],
    "hsk5_1059": [{"chinese": "请输入您的密码。", "pinyin": "Qǐng shūrù nín de mìmǎ.", "meaningVi": "Xin nhập mật khẩu của bạn."}],
    "hsk5_106": [{"chinese": "这是我们公司的新产品。", "pinyin": "Zhè shì wǒmen gōngsī de xīn chǎnpǐn.", "meaningVi": "Đây là sản phẩm mới của công ty chúng tôi."}],
    "hsk5_1060": [{"chinese": "这张床很舒适。", "pinyin": "Zhè zhāng chuáng hěn shūshì.", "meaningVi": "Chiếc giường này rất thoải mái."}],
    "hsk5_1061": [{"chinese": "他操作得很熟练。", "pinyin": "Tā cāozuò de hěn shúliàn.", "meaningVi": "Anh ấy thao tác rất thành thạo."}],
    "hsk5_1062": [{"chinese": "在这里我一个熟人都没有。", "pinyin": "Zài zhèlǐ wǒ yí gè shúrén dōu méiyǒu.", "meaningVi": "Ở đây tôi không có người quen nào."}],
    "hsk5_1065": [{"chinese": "这本书属于图书馆。", "pinyin": "Zhè běn shū shǔyú túshūguǎn.", "meaningVi": "Cuốn sách này thuộc về thư viện."}],
    "hsk5_1066": [{"chinese": "这束光很亮。", "pinyin": "Zhè shù guāng hěn liàng.", "meaningVi": "Chùm ánh sáng này rất sáng."}],
    "hsk5_1067": [{"chinese": "请分析这些数据。", "pinyin": "Qǐng fēnxī zhèxiē shùjù.", "meaningVi": "Xin phân tích những số liệu này."}],
    "hsk5_1068": [{"chinese": "校园里种满了树木。", "pinyin": "Xiàoyuán lǐ zhòngmǎnle shùmù.", "meaningVi": "Trong khuôn viên trường trồng đầy cây cối."}],
    "hsk5_1069": [{"chinese": "他不小心摔倒了。", "pinyin": "Tā bù xiǎoxīn shuāidǎo le.", "meaningVi": "Anh ấy vô ý bị ngã."}],
    "hsk5_107": [{"chinese": "这个城市的旅游产业很发达。", "pinyin": "Zhège chéngshì de lǚyóu chǎnyè hěn fādá.", "meaningVi": "Ngành du lịch của thành phố này rất phát triển."}],
    "hsk5_1070": [{"chinese": "双方达成了协议。", "pinyin": "Shuāngfāng dáchéngle xiéyì.", "meaningVi": "Hai bên đã đạt được thỏa thuận."}],
    "hsk5_1071": [{"chinese": "这种水果水分很足。", "pinyin": "Zhè zhǒng shuǐguǒ shuǐfèn hěn zú.", "meaningVi": "Loại trái cây này rất nhiều nước."}],
    "hsk5_1072": [{"chinese": "这笔收入需要交税。", "pinyin": "Zhè bǐ shōurù xūyào jiāo shuì.", "meaningVi": "Khoản thu nhập này cần phải đóng thuế."}],
    "hsk5_1073": [{"chinese": "良好的睡眠很重要。", "pinyin": "Liánghǎo de shuìmián hěn zhòngyào.", "meaningVi": "Giấc ngủ tốt rất quan trọng."}],
    "hsk5_1076": [{"chinese": "我说服了他改变主意。", "pinyin": "Wǒ shuōfúle tā gǎibiàn zhǔyi.", "meaningVi": "Tôi đã thuyết phục anh ấy thay đổi ý định."}],
    "hsk5_1077": [{"chinese": "请给我一点时间思考。", "pinyin": "Qǐng gěi wǒ yìdiǎn shíjiān sīkǎo.", "meaningVi": "Xin cho tôi một chút thời gian để suy nghĩ."}],
    "hsk5_108": [{"chinese": "你应该发挥自己的长处。", "pinyin": "Nǐ yīnggāi fāhuī zìjǐ de chángchù.", "meaningVi": "Bạn nên phát huy sở trường của mình."}],
    "hsk5_1080": [{"chinese": "他的思想很开放。", "pinyin": "Tā de sīxiǎng hěn kāifàng.", "meaningVi": "Tư tưởng của anh ấy rất cởi mở."}],
    "hsk5_1081": [{"chinese": "他四处寻找工作。", "pinyin": "Tā sìchù xúnzhǎo gōngzuò.", "meaningVi": "Anh ấy tìm việc khắp nơi."}],
    "hsk5_1082": [{"chinese": "他似乎不太高兴。", "pinyin": "Tā sìhū bú tài gāoxìng.", "meaningVi": "Anh ấy dường như không vui lắm."}],
    "hsk5_1083": [{"chinese": "他环顾四周。", "pinyin": "Tā huángù sìzhōu.", "meaningVi": "Anh ấy nhìn quanh bốn phía."}],
    "hsk5_1084": [{"chinese": "我在网上搜了一下。", "pinyin": "Wǒ zài wǎngshàng sōule yíxià.", "meaningVi": "Tôi đã tìm kiếm trên mạng một chút."}],
    "hsk5_1085": [{"chinese": "请在搜索框里输入关键词。", "pinyin": "Qǐng zài sōusuǒ kuàng lǐ shūrù guānjiàncí.", "meaningVi": "Xin nhập từ khóa vào ô tìm kiếm."}],
    "hsk5_1087": [{"chinese": "生活就像酸甜苦辣。", "pinyin": "Shēnghuó jiù xiàng suāntiánkǔlà.", "meaningVi": "Cuộc sống giống như đủ mọi vị chua ngọt đắng cay."}],
    "hsk5_1088": [{"chinese": "我随他一起去了。", "pinyin": "Wǒ suí tā yìqǐ qù le.", "meaningVi": "Tôi đã đi cùng với anh ấy."}],
    "hsk5_1089": [{"chinese": "他先走了，我随后就到。", "pinyin": "Tā xiān zǒu le, wǒ suíhòu jiù dào.", "meaningVi": "Anh ấy đi trước, tôi sẽ đến ngay sau đó."}],
    "hsk5_109": [{"chinese": "这条河的长度超过一千公里。", "pinyin": "Zhè tiáo hé de chángdù chāoguò yìqiān gōnglǐ.", "meaningVi": "Chiều dài của con sông này vượt quá một nghìn ki-lô-mét."}],
    "hsk5_1090": [{"chinese": "有问题可以随时问我。", "pinyin": "Yǒu wèntí kěyǐ suíshí wèn wǒ.", "meaningVi": "Có vấn đề gì có thể hỏi tôi bất cứ lúc nào."}],
    "hsk5_1091": [{"chinese": "请随手关门。", "pinyin": "Qǐng suíshǒu guānmén.", "meaningVi": "Xin tiện tay đóng cửa."}],
    "hsk5_1092": [{"chinese": "请随意，不要客气。", "pinyin": "Qǐng suíyì, búyào kèqi.", "meaningVi": "Xin cứ tự nhiên, đừng khách sáo."}],
    "hsk5_1094": [{"chinese": "吸烟会损害健康。", "pinyin": "Xīyān huì sǔnhài jiànkāng.", "meaningVi": "Hút thuốc sẽ gây tổn hại cho sức khỏe."}],
    "hsk5_1096": [{"chinese": "这项技术缩短了生产时间。", "pinyin": "Zhè xiàng jìshù suōduǎnle shēngchǎn shíjiān.", "meaningVi": "Công nghệ này đã rút ngắn thời gian sản xuất."}],
    "hsk5_1097": [{"chinese": "请把这张图片缩小一点。", "pinyin": "Qǐng bǎ zhè zhāng túpiàn suōxiǎo yìdiǎn.", "meaningVi": "Xin thu nhỏ bức ảnh này lại một chút."}],
    "hsk5_110": [{"chinese": "他们的友谊很长久。", "pinyin": "Tāmen de yǒuyì hěn chángjiǔ.", "meaningVi": "Tình bạn của họ rất lâu bền."}],
    "hsk5_1100": [{"chinese": "不要随便评价他人。", "pinyin": "Búyào suíbiàn píngjià tārén.", "meaningVi": "Đừng tùy tiện đánh giá người khác."}],
    "hsk5_1101": [{"chinese": "桌上放着一盏台灯。", "pinyin": "Zhuō shàng fàngzhe yì zhǎn táidēng.", "meaningVi": "Trên bàn đặt một chiếc đèn bàn."}],
    "hsk5_1102": [{"chinese": "小心台阶，别摔倒。", "pinyin": "Xiǎoxīn táijiē, bié shuāidǎo.", "meaningVi": "Cẩn thận bậc thềm, đừng ngã."}],
    "hsk5_1103": [{"chinese": "这位是我太太。", "pinyin": "Zhè wèi shì wǒ tàitai.", "meaningVi": "Đây là vợ tôi."}],
    "hsk5_1104": [{"chinese": "校长找他谈话了。", "pinyin": "Xiàozhǎng zhǎo tā tánhuà le.", "meaningVi": "Hiệu trưởng đã tìm anh ấy để nói chuyện."}],
    "hsk5_1107": [{"chinese": "这是我们当地的特产。", "pinyin": "Zhè shì wǒmen dāngdì de tèchǎn.", "meaningVi": "Đây là đặc sản của địa phương chúng tôi."}],
    "hsk5_1108": [{"chinese": "这家餐厅很有特色。", "pinyin": "Zhè jiā cāntīng hěn yǒu tèsè.", "meaningVi": "Nhà hàng này rất có đặc sắc."}],
    "hsk5_1109": [{"chinese": "这是一个特殊情况。", "pinyin": "Zhè shì yí gè tèshū qíngkuàng.", "meaningVi": "Đây là một trường hợp đặc biệt."}],
    "hsk5_1110": [{"chinese": "这是熊猫特有的习性。", "pinyin": "Zhè shì xióngmāo tèyǒu de xíxìng.", "meaningVi": "Đây là tập tính đặc trưng riêng của gấu trúc."}],
    "hsk5_1111": [{"chinese": "这个地区的建筑有明显的特征。", "pinyin": "Zhège dìqū de jiànzhù yǒu míngxiǎn de tèzhēng.", "meaningVi": "Kiến trúc của khu vực này có đặc trưng rõ rệt."}],
    "hsk5_1112": [{"chinese": "他的伤口还在疼痛。", "pinyin": "Tā de shāngkǒu hái zài téngtòng.", "meaningVi": "Vết thương của anh ấy vẫn còn đau."}],
    "hsk5_1114": [{"chinese": "请在明天之前提交报告。", "pinyin": "Qǐng zài míngtiān zhīqián tíjiāo bàogào.", "meaningVi": "Xin nộp báo cáo trước ngày mai."}],
    "hsk5_1115": [{"chinese": "这道题目很难。", "pinyin": "Zhè dào tímù hěn nán.", "meaningVi": "Đề bài này rất khó."}],
    "hsk5_1116": [{"chinese": "他决定提起诉讼。", "pinyin": "Tā juédìng tíqǐ sùsòng.", "meaningVi": "Anh ấy quyết định khởi kiện."}],
    "hsk5_1117": [{"chinese": "他的工作能力得到了提升。", "pinyin": "Tā de gōngzuò nénglì dédàole tíshēng.", "meaningVi": "Khả năng làm việc của anh ấy đã được nâng cao."}],
    "hsk5_1118": [{"chinese": "老师请学生提问。", "pinyin": "Lǎoshī qǐng xuésheng tíwèn.", "meaningVi": "Giáo viên mời học sinh đặt câu hỏi."}],
    "hsk5_112": [{"chinese": "这是基本的生活常识。", "pinyin": "Zhè shì jīběn de shēnghuó chángshí.", "meaningVi": "Đây là kiến thức cơ bản trong cuộc sống."}],
    "hsk5_1120": [{"chinese": "这份工作需要很好的体力。", "pinyin": "Zhè fèn gōngzuò xūyào hěn hǎo de tǐlì.", "meaningVi": "Công việc này cần có thể lực tốt."}],
    "hsk5_1121": [{"chinese": "这件事体现了他的责任心。", "pinyin": "Zhè jiàn shì tǐxiànle tā de zérènxīn.", "meaningVi": "Việc này thể hiện trách nhiệm của anh ấy."}],
    "hsk5_1122": [{"chinese": "我想体验一下当地的生活。", "pinyin": "Wǒ xiǎng tǐyàn yíxià dāngdì de shēnghuó.", "meaningVi": "Tôi muốn trải nghiệm cuộc sống của người dân địa phương."}],
    "hsk5_1124": [{"chinese": "傍晚的天空变成了橙红色。", "pinyin": "Bàngwǎn de tiānkōng biànchéngle chénghóngsè.", "meaningVi": "Bầu trời lúc hoàng hôn chuyển sang màu cam đỏ."}],
    "hsk5_1125": [{"chinese": "天上有一架飞机。", "pinyin": "Tiānshàng yǒu yí jià fēijī.", "meaningVi": "Trên trời có một chiếc máy bay."}],
    "hsk5_1126": [{"chinese": "请把空格填上。", "pinyin": "Qǐng bǎ kònggé tián shàng.", "meaningVi": "Xin điền vào chỗ trống."}],
    "hsk5_1127": [{"chinese": "饭后她喜欢吃点甜品。", "pinyin": "Fàn hòu tā xǐhuan chī diǎn tiánpǐn.", "meaningVi": "Sau bữa ăn cô ấy thích ăn chút đồ ngọt."}],
    "hsk5_1128": [{"chinese": "他挑了一件红色的衣服。", "pinyin": "Tā tiāole yí jiàn hóngsè de yīfu.", "meaningVi": "Anh ấy đã chọn một chiếc áo màu đỏ."}],
    "hsk5_1129": [{"chinese": "她仔细挑选礼物。", "pinyin": "Tā zǐxì tiāoxuǎn lǐwù.", "meaningVi": "Cô ấy cẩn thận lựa chọn quà tặng."}],
    "hsk5_1131": [{"chinese": "这个孩子很调皮。", "pinyin": "Zhège háizi hěn tiáopí.", "meaningVi": "Đứa trẻ này rất nghịch ngợm."}],
    "hsk5_1132": [{"chinese": "请调整一下计划。", "pinyin": "Qǐng tiáozhěng yíxià jìhuà.", "meaningVi": "Xin điều chỉnh lại kế hoạch."}],
    "hsk5_1134": [{"chinese": "他擅长跳高。", "pinyin": "Tā shàncháng tiàogāo.", "meaningVi": "Anh ấy giỏi môn nhảy cao."}],
    "hsk5_1135": [{"chinese": "她参加了跳远比赛。", "pinyin": "Tā cānjiāle tiàoyuǎn bǐsài.", "meaningVi": "Cô ấy đã tham gia thi đấu nhảy xa."}],
    "hsk5_1136": [{"chinese": "请把海报贴在墙上。", "pinyin": "Qǐng bǎ hǎibào tiē zài qiáng shàng.", "meaningVi": "Xin dán tấm áp phích lên tường."}],
    "hsk5_1137": [{"chinese": "这条铁路连接两座城市。", "pinyin": "Zhè tiáo tiělù liánjiē liǎng zuò chéngshì.", "meaningVi": "Tuyến đường sắt này kết nối hai thành phố."}],
    "hsk5_1138": [{"chinese": "我们在这个城市停留了三天。", "pinyin": "Wǒmen zài zhège chéngshì tíngliúle sān tiān.", "meaningVi": "Chúng tôi đã ở lại thành phố này ba ngày."}],
    "hsk5_114": [{"chinese": "他打算坐长途汽车回家。", "pinyin": "Tā dǎsuàn zuò chángtú qìchē huí jiā.", "meaningVi": "Anh ấy định đi xe khách đường dài về nhà."}],
    "hsk5_1140": [{"chinese": "这条路禁止车辆通行。", "pinyin": "Zhè tiáo lù jìnzhǐ chēliàng tōngxíng.", "meaningVi": "Con đường này cấm xe cộ lưu thông."}],
    "hsk5_1142": [{"chinese": "我很同情他的遭遇。", "pinyin": "Wǒ hěn tóngqíng tā de zāoyù.", "meaningVi": "Tôi rất thông cảm với hoàn cảnh của anh ấy."}],
    "hsk5_1143": [{"chinese": "我们俩是同一天出生的。", "pinyin": "Wǒmen liǎ shì tóng yì tiān chūshēng de.", "meaningVi": "Hai chúng tôi sinh cùng một ngày."}],
    "hsk5_1144": [{"chinese": "请统计一下人数。", "pinyin": "Qǐng tǒngjì yíxià rénshù.", "meaningVi": "Xin thống kê số người."}],
    "hsk5_1146": [{"chinese": "失去亲人让他很痛苦。", "pinyin": "Shīqù qīnrén ràng tā hěn tòngkǔ.", "meaningVi": "Mất người thân khiến anh ấy rất đau khổ."}],
    "hsk5_1147": [{"chinese": "他投了很多钱在这个项目上。", "pinyin": "Tā tóule hěn duō qián zài zhège xiàngmù shàng.", "meaningVi": "Anh ấy đã đầu tư rất nhiều tiền vào dự án này."}],
    "hsk5_115": [{"chinese": "我们要有长远的计划。", "pinyin": "Wǒmen yào yǒu chángyuǎn de jìhuà.", "meaningVi": "Chúng ta cần có kế hoạch lâu dài."}],
    "hsk5_1151": [{"chinese": "这幅图画色彩丰富。", "pinyin": "Zhè fú túhuà sècǎi fēngfù.", "meaningVi": "Bức tranh này màu sắc phong phú."}],
    "hsk5_1152": [{"chinese": "这批图书是上个月新到的。", "pinyin": "Zhè pī túshū shì shàng gè yuè xīn dào de.", "meaningVi": "Lô sách này là mới về từ tháng trước."}],
    "hsk5_1153": [{"chinese": "这片土地很肥沃。", "pinyin": "Zhè piàn tǔdì hěn féiwò.", "meaningVi": "Mảnh đất này rất màu mỡ."}],
    "hsk5_1154": [{"chinese": "妈妈买了几个土豆。", "pinyin": "Māma mǎile jǐ gè tǔdòu.", "meaningVi": "Mẹ đã mua vài củ khoai tây."}],
    "hsk5_1155": [{"chinese": "他家养了一只兔子。", "pinyin": "Tā jiā yǎngle yì zhī tùzi.", "meaningVi": "Nhà anh ấy nuôi một con thỏ."}],
    "hsk5_1157": [{"chinese": "我们是一个团队。", "pinyin": "Wǒmen shì yí gè tuánduì.", "meaningVi": "Chúng tôi là một đội ngũ."}],
    "hsk5_1158": [{"chinese": "这项政策推动了经济发展。", "pinyin": "Zhè xiàng zhèngcè tuīdòngle jīngjì fāzhǎn.", "meaningVi": "Chính sách này đã thúc đẩy sự phát triển kinh tế."}],
    "hsk5_1159": [{"chinese": "这种方法值得推广。", "pinyin": "Zhè zhǒng fāngfǎ zhídé tuīguǎng.", "meaningVi": "Phương pháp này đáng để quảng bá rộng rãi."}],
    "hsk5_116": [{"chinese": "这是公共场所，请保持安静。", "pinyin": "Zhè shì gōnggòng chǎngsuǒ, qǐng bǎochí ānjìng.", "meaningVi": "Đây là nơi công cộng, xin giữ trật tự."}],
    "hsk5_1160": [{"chinese": "你能推荐一本好书吗？", "pinyin": "Nǐ néng tuījiàn yì běn hǎo shū ma?", "meaningVi": "Bạn có thể giới thiệu một cuốn sách hay không?"}],
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
