"""P5.10.3 (continued) -- Batch 020 (continues immediately after
examples_batch_019.json; entirely within HSK5).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Dense homophone landscape in this batch ***
This batch contains the largest xíng-cluster seen so far in the
pipeline, split across two unrelated characters that share the exact
same pinyin and tone, none flagged by the mechanical tier system (it
compares the `word` string, and all ten are different words):
  - 行 (xíng, "to go/conduct"): 行程/行人/行驶/行为/行走 (5 members)
  - 形 (xíng, "shape/form"): 形成/形式/形势/形容/形状 (5 members)
  Two pairs within this cluster are FULL homophones of each other
  (identical pinyin AND tone, different character):
    - 行程 (xíngchéng, "itinerary") vs 形成 (xíngchéng, "to form")
    - 形式 (xíngshì, "format/mode") vs 形势 (xíngshì, "situation")
  Each of the ten was anchored to a distinct, concrete real-world
  referent (a trip itinerary / habit formation / a pedestrian / a
  vehicle on the highway / misconduct / an elderly person walking /
  an indescribable feeling / an online event format / international
  affairs / a rock's shape) so no two could be confused even without
  surrounding context.
Additional same-pinyin-different-character clusters:
  - 成 / 程 / 承 (chéng, 2nd tone): 成本/成分 (成) vs 程度 (程) vs
    承担 (承) -- three characters, one syllable+tone.
  - 称 (chēng, 1st tone, distinct tone from the chéng cluster above):
    称为/称赞.
  - 迎 (yíng, "to welcome") vs 赢 (yíng, already published, batch 016,
    "to win") vs 营 (yíng, "to operate/manage", in 营养/营业):
    three-way homophone; 迎/迎接 and 营养/营业 both appear as new
    records in this batch, kept fully distinct from each other and
    from the already-published 赢/赢得.
  - 应 (a polyphonic character): 应当 (yīng, 1st tone, "ought to") vs
    应对 (yìng, 4th tone, "to respond to") -- same character, two
    different readings and meanings, each demonstrated in its
    standard reading/sense.

Self-caught near-template revisions made during drafting (before this
batch was finalized):
  - 信任 (xìnrèn): first draft "他赢得了大家的信任。" was a near-
    template match against 赢得's own already-published example
    (batch 016, hsk4_875: "他赢得了大家的尊重。", differing by only
    信任/尊重) -- rewritten to "我们之间需要更多的信任。".
  - 夜间 (yèjiān): first draft "夜间请尽量保持安静。" was a thematic/
    structural near-match against 夜晚's own already-published example
    (batch 016, hsk4_863: "夜晚的城市很安静。", both centered on
    nighttime quietness) -- rewritten to "夜间行车要格外小心。".
  All re-verified against the full pilot+002-019 corpus with zero
  remaining exact duplicates and zero near-template flags.

Other productive-root families kept structurally distinct (no shared
template): 信封/信任/信用 (xìn+X); 修改/修建 (xiū+X, distinct from
the already-published 修/修理); 需/需求 (xū, root+derivative);
宣布/宣传 (xuān+X); 学分/学科/学历/学年/学术/学者 (xué+X, six
members); 研发/研制 (yán+X, distinct from the already-published
研究/研究生); 药品/药物 (yào+X near-synonyms); 夜间/夜市 (yè+X,
distinct from the already-published 夜晚); 医疗/医学 (yī+X); 移/移动
(yí, root+derivative); 用法/用户/用力/用品 (yòng+X, distinct from the
already-published 用来/用于); 影片/影视 (yǐng+X); 拥抱/拥有 (yōng+X).

Near-synonym pairs kept in genuinely distinct constructions: 要不/
要不是 (yàobù/yàobúshì); 因而 (yīn'ér) kept distinct from the
already-published 因此 (batch 016); 依然 (yīrán) kept distinct from
the already-published 仍然 (batch 017).

Usage:
    python generate_examples_batch_020.py --dry-run
    python generate_examples_batch_020.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 20
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_020.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk5_1278": [{"chinese": "新娘穿着一身白色婚纱。", "pinyin": "Xīnniáng chuānzhe yì shēn báisè hūnshā.", "meaningVi": "Cô dâu mặc một bộ váy cưới màu trắng."}],
    "hsk5_1279": [{"chinese": "公司来了几位新人。", "pinyin": "Gōngsī láile jǐ wèi xīnrén.", "meaningVi": "Công ty đã có vài người mới đến."}],
    "hsk5_1281": [{"chinese": "保持乐观的心态很重要。", "pinyin": "Bǎochí lèguān de xīntài hěn zhòngyào.", "meaningVi": "Giữ tâm thái lạc quan rất quan trọng."}],
    "hsk5_1282": [{"chinese": "这是一种新型材料。", "pinyin": "Zhè shì yì zhǒng xīnxíng cáiliào.", "meaningVi": "Đây là một loại vật liệu kiểu mới."}],
    "hsk5_1283": [{"chinese": "请把信放进信封里。", "pinyin": "Qǐng bǎ xìn fàng jìn xìnfēng lǐ.", "meaningVi": "Xin cho thư vào phong bì."}],
    "hsk5_1284": [{"chinese": "我们之间需要更多的信任。", "pinyin": "Wǒmen zhījiān xūyào gèng duō de xìnrèn.", "meaningVi": "Giữa chúng ta cần có thêm sự tin tưởng."}],
    "hsk5_1285": [{"chinese": "他很讲信用。", "pinyin": "Tā hěn jiǎng xìnyòng.", "meaningVi": "Anh ấy rất coi trọng chữ tín."}],
    "hsk5_1286": [{"chinese": "这次旅行的行程排得很满。", "pinyin": "Zhè cì lǚxíng de xíngchéng pái de hěn mǎn.", "meaningVi": "Lịch trình của chuyến du lịch lần này được sắp xếp rất kín."}],
    "hsk5_1287": [{"chinese": "长期的努力形成了良好的习惯。", "pinyin": "Chángqī de nǔlì xíngchéngle liánghǎo de xíguàn.", "meaningVi": "Sự nỗ lực lâu dài đã hình thành nên thói quen tốt."}],
    "hsk5_1289": [{"chinese": "请注意避让行人。", "pinyin": "Qǐng zhùyì bìràng xíngrén.", "meaningVi": "Xin chú ý nhường đường cho người đi bộ."}],
    "hsk5_129": [{"chinese": "这个问题需要彻底解决。", "pinyin": "Zhège wèntí xūyào chèdǐ jiějué.", "meaningVi": "Vấn đề này cần được giải quyết triệt để."}],
    "hsk5_1290": [{"chinese": "我简直无法形容当时的心情。", "pinyin": "Wǒ jiǎnzhí wúfǎ xíngróng dāngshí de xīnqíng.", "meaningVi": "Tôi thực sự không thể miêu tả tâm trạng lúc đó."}],
    "hsk5_1291": [{"chinese": "这次活动采取线上形式进行。", "pinyin": "Zhè cì huódòng cǎiqǔ xiànshàng xíngshì jìnxíng.", "meaningVi": "Hoạt động lần này được tiến hành theo hình thức trực tuyến."}],
    "hsk5_1292": [{"chinese": "目前的国际形势比较复杂。", "pinyin": "Mùqián de guójì xíngshì bǐjiào fùzá.", "meaningVi": "Tình hình quốc tế hiện nay khá phức tạp."}],
    "hsk5_1293": [{"chinese": "车辆正在高速公路上行驶。", "pinyin": "Chēliàng zhèngzài gāosù gōnglù shàng xíngshǐ.", "meaningVi": "Xe cộ đang chạy trên đường cao tốc."}],
    "hsk5_1294": [{"chinese": "这种行为是不对的。", "pinyin": "Zhè zhǒng xíngwéi shì bú duì de.", "meaningVi": "Hành vi này là không đúng."}],
    "hsk5_1296": [{"chinese": "这块石头的形状很特别。", "pinyin": "Zhè kuài shítou de xíngzhuàng hěn tèbié.", "meaningVi": "Hình dạng của tảng đá này rất đặc biệt."}],
    "hsk5_1297": [{"chinese": "老人在公园里慢慢行走。", "pinyin": "Lǎorén zài gōngyuán lǐ mànmàn xíngzǒu.", "meaningVi": "Người già đi bộ chậm rãi trong công viên."}],
    "hsk5_1299": [{"chinese": "这两件事的性质不同。", "pinyin": "Zhè liǎng jiàn shì de xìngzhì bùtóng.", "meaningVi": "Tính chất của hai việc này khác nhau."}],
    "hsk5_1300": [{"chinese": "请帮我修改一下这篇文章。", "pinyin": "Qǐng bāng wǒ xiūgǎi yíxià zhè piān wénzhāng.", "meaningVi": "Xin giúp tôi sửa lại bài viết này."}],
    "hsk5_1301": [{"chinese": "这座桥是去年修建的。", "pinyin": "Zhè zuò qiáo shì qùnián xiūjiàn de.", "meaningVi": "Cây cầu này được xây dựng vào năm ngoái."}],
    "hsk5_1302": [{"chinese": "周末是休闲放松的好时机。", "pinyin": "Zhōumò shì xiūxián fàngsōng de hǎo shíjī.", "meaningVi": "Cuối tuần là thời điểm tốt để giải trí thư giãn."}],
    "hsk5_1303": [{"chinese": "此事尚需进一步调查。", "pinyin": "Cǐ shì shàng xū jìnyíbù diàochá.", "meaningVi": "Việc này vẫn cần được điều tra thêm."}],
    "hsk5_1304": [{"chinese": "市场对这种产品的需求很大。", "pinyin": "Shìchǎng duì zhè zhǒng chǎnpǐn de xūqiú hěn dà.", "meaningVi": "Nhu cầu thị trường đối với sản phẩm này rất lớn."}],
    "hsk5_1306": [{"chinese": "公司宣布了新的政策。", "pinyin": "Gōngsī xuānbùle xīn de zhèngcè.", "meaningVi": "Công ty đã tuyên bố chính sách mới."}],
    "hsk5_1307": [{"chinese": "这部电影做了大量的宣传。", "pinyin": "Zhè bù diànyǐng zuòle dàliàng de xuānchuán.", "meaningVi": "Bộ phim này đã được quảng bá rất nhiều."}],
    "hsk5_1308": [{"chinese": "这位选手表现得非常出色。", "pinyin": "Zhè wèi xuǎnshǒu biǎoxiàn de fēicháng chūsè.", "meaningVi": "Vận động viên này thể hiện vô cùng xuất sắc."}],
    "hsk5_1309": [{"chinese": "这门课有三个学分。", "pinyin": "Zhè mén kè yǒu sān gè xuéfēn.", "meaningVi": "Môn học này có ba tín chỉ."}],
    "hsk5_131": [{"chinese": "听到这个消息，他沉默了很久。", "pinyin": "Tīngdào zhège xiāoxi, tā chénmòle hěn jiǔ.", "meaningVi": "Nghe được tin này, anh ấy im lặng rất lâu."}],
    "hsk5_1310": [{"chinese": "数学是一门重要的学科。", "pinyin": "Shùxué shì yì mén zhòngyào de xuékē.", "meaningVi": "Toán học là một môn học quan trọng."}],
    "hsk5_1311": [{"chinese": "这份工作对学历有要求。", "pinyin": "Zhè fèn gōngzuò duì xuélì yǒu yāoqiú.", "meaningVi": "Công việc này có yêu cầu về trình độ học vấn."}],
    "hsk5_1312": [{"chinese": "新学年就要开始了。", "pinyin": "Xīn xuénián jiù yào kāishǐ le.", "meaningVi": "Năm học mới sắp bắt đầu rồi."}],
    "hsk5_1313": [{"chinese": "他在学术方面很有成就。", "pinyin": "Tā zài xuéshù fāngmiàn hěn yǒu chéngjiù.", "meaningVi": "Anh ấy có nhiều thành tựu về mặt học thuật."}],
    "hsk5_1314": [{"chinese": "他是一位受人尊敬的学者。", "pinyin": "Tā shì yí wèi shòu rén zūnjìng de xuézhě.", "meaningVi": "Ông ấy là một học giả được mọi người kính trọng."}],
    "hsk5_1315": [{"chinese": "夏天他喜欢吃雪糕。", "pinyin": "Xiàtiān tā xǐhuan chī xuěgāo.", "meaningVi": "Mùa hè anh ấy thích ăn kem que."}],
    "hsk5_1317": [{"chinese": "他一直在寻找合适的工作。", "pinyin": "Tā yìzhí zài xúnzhǎo héshì de gōngzuò.", "meaningVi": "Anh ấy luôn tìm kiếm công việc phù hợp."}],
    "hsk5_1318": [{"chinese": "运动员每天都要训练。", "pinyin": "Yùndòngyuán měitiān dōu yào xùnliàn.", "meaningVi": "Vận động viên mỗi ngày đều phải luyện tập."}],
    "hsk5_1319": [{"chinese": "情况变化得很迅速。", "pinyin": "Qíngkuàng biànhuà de hěn xùnsù.", "meaningVi": "Tình hình thay đổi rất nhanh chóng."}],
    "hsk5_1320": [{"chinese": "呀，下雨了！", "pinyin": "Yā, xiàyǔ le!", "meaningVi": "Ôi, trời mưa rồi!"}],
    "hsk5_1322": [{"chinese": "过年时孩子们最期待压岁钱。", "pinyin": "Guònián shí háizimen zuì qídài yāsuìqián.", "meaningVi": "Vào dịp Tết trẻ con mong đợi nhất là tiền mừng tuổi."}],
    "hsk5_1323": [{"chinese": "湖里有几只鸭子。", "pinyin": "Hú lǐ yǒu jǐ zhī yāzi.", "meaningVi": "Trong hồ có vài con vịt."}],
    "hsk5_1324": [{"chinese": "饭后要刷牙齿。", "pinyin": "Fàn hòu yào shuā yáchǐ.", "meaningVi": "Sau bữa ăn phải đánh răng."}],
    "hsk5_1326": [{"chinese": "会议时间延长了半个小时。", "pinyin": "Huìyì shíjiān yánchángle bàn gè xiǎoshí.", "meaningVi": "Thời gian cuộc họp đã kéo dài thêm nửa tiếng."}],
    "hsk5_1327": [{"chinese": "公司投入大量资金研发新产品。", "pinyin": "Gōngsī tóurù dàliàng zījīn yánfā xīn chǎnpǐn.", "meaningVi": "Công ty đầu tư rất nhiều vốn để nghiên cứu phát triển sản phẩm mới."}],
    "hsk5_1329": [{"chinese": "科学家们正在研制新型疫苗。", "pinyin": "Kēxuéjiāmen zhèngzài yánzhì xīnxíng yìmiáo.", "meaningVi": "Các nhà khoa học đang nghiên cứu chế tạo loại vắc-xin mới."}],
    "hsk5_1331": [{"chinese": "他在台上发表演讲。", "pinyin": "Tā zài tái shàng fābiǎo yǎnjiǎng.", "meaningVi": "Anh ấy phát biểu diễn thuyết trên sân khấu."}],
    "hsk5_1332": [{"chinese": "她感动得流下了眼泪。", "pinyin": "Tā gǎndòng de liúxiàle yǎnlèi.", "meaningVi": "Cô ấy cảm động đến mức rơi nước mắt."}],
    "hsk5_1333": [{"chinese": "阳台上种了很多花。", "pinyin": "Yángtái shàng zhòngle hěn duō huā.", "meaningVi": "Trên ban công trồng rất nhiều hoa."}],
    "hsk5_1334": [{"chinese": "这件衣服的样式很流行。", "pinyin": "Zhè jiàn yīfu de yàngshì hěn liúxíng.", "meaningVi": "Kiểu dáng của chiếc áo này rất thịnh hành."}],
    "hsk5_1335": [{"chinese": "他弯腰捡起了地上的东西。", "pinyin": "Tā wānyāo jiǎnqǐle dìshang de dōngxi.", "meaningVi": "Anh ấy cúi lưng nhặt đồ vật trên đất lên."}],
    "hsk5_1336": [{"chinese": "他摇了摇头。", "pinyin": "Tā yáole yáo tóu.", "meaningVi": "Anh ấy lắc đầu."}],
    "hsk5_1338": [{"chinese": "快点走，要不就迟到了。", "pinyin": "Kuài diǎn zǒu, yàobù jiù chídào le.", "meaningVi": "Đi nhanh lên, nếu không thì sẽ đến muộn."}],
    "hsk5_1339": [{"chinese": "要不是你提醒，我都忘了。", "pinyin": "Yàobúshì nǐ tíxǐng, wǒ dōu wàng le.", "meaningVi": "Nếu không phải bạn nhắc thì tôi đã quên mất rồi."}],
    "hsk5_134": [{"chinese": "长江被称为中国的母亲河。", "pinyin": "Chángjiāng bèi chēngwéi Zhōngguó de mǔqīnhé.", "meaningVi": "Trường Giang được gọi là sông mẹ của Trung Quốc."}],
    "hsk5_1340": [{"chinese": "请把药品放在儿童接触不到的地方。", "pinyin": "Qǐng bǎ yàopǐn fàng zài értóng jiēchù bú dào de dìfang.", "meaningVi": "Xin để dược phẩm ở nơi trẻ em không với tới được."}],
    "hsk5_1341": [{"chinese": "医生给他开了一些药物。", "pinyin": "Yīshēng gěi tā kāile yìxiē yàowù.", "meaningVi": "Bác sĩ đã kê cho anh ấy một số loại thuốc."}],
    "hsk5_1342": [{"chinese": "夜间行车要格外小心。", "pinyin": "Yèjiān xíngchē yào géwài xiǎoxīn.", "meaningVi": "Lái xe vào ban đêm phải đặc biệt cẩn thận."}],
    "hsk5_1343": [{"chinese": "我们去夜市吃小吃吧。", "pinyin": "Wǒmen qù yèshì chī xiǎochī ba.", "meaningVi": "Chúng ta đi chợ đêm ăn đồ ăn vặt đi."}],
    "hsk5_1345": [{"chinese": "他是一位业余摄影爱好者。", "pinyin": "Tā shì yí wèi yèyú shèyǐng àihàozhě.", "meaningVi": "Anh ấy là một người yêu thích nhiếp ảnh nghiệp dư."}],
    "hsk5_1348": [{"chinese": "这里的医疗条件很好。", "pinyin": "Zhèlǐ de yīliáo tiáojiàn hěn hǎo.", "meaningVi": "Điều kiện y tế ở đây rất tốt."}],
    "hsk5_1349": [{"chinese": "多年过去了，他依然记得那件事。", "pinyin": "Duō nián guòqù le, tā yīrán jìde nà jiàn shì.", "meaningVi": "Nhiều năm đã trôi qua, anh ấy vẫn nhớ chuyện đó."}],
    "hsk5_135": [{"chinese": "老师称赞了他的进步。", "pinyin": "Lǎoshī chēngzànle tā de jìnbù.", "meaningVi": "Giáo viên đã khen ngợi sự tiến bộ của anh ấy."}],
    "hsk5_1350": [{"chinese": "他大学学的是医学。", "pinyin": "Tā dàxué xué de shì yīxué.", "meaningVi": "Anh ấy học ngành y học ở đại học."}],
    "hsk5_1351": [{"chinese": "请把桌子往左移一点。", "pinyin": "Qǐng bǎ zhuōzi wǎng zuǒ yí yìdiǎn.", "meaningVi": "Xin dịch cái bàn sang trái một chút."}],
    "hsk5_1352": [{"chinese": "请尽量减少使用一次性用品。", "pinyin": "Qǐng jǐnliàng jiǎnshǎo shǐyòng yícìxìng yòngpǐn.", "meaningVi": "Xin hãy cố gắng giảm sử dụng đồ dùng một lần."}],
    "hsk5_1353": [{"chinese": "年轻的一代想法很不一样。", "pinyin": "Niánqīng de yídài xiǎngfǎ hěn bù yíyàng.", "meaningVi": "Thế hệ trẻ có suy nghĩ rất khác."}],
    "hsk5_1354": [{"chinese": "一旦决定了就不要轻易改变。", "pinyin": "Yídàn juédìngle jiù búyào qīngyì gǎibiàn.", "meaningVi": "Một khi đã quyết định thì đừng dễ dàng thay đổi."}],
    "hsk5_1355": [{"chinese": "请不要随意移动这些物品。", "pinyin": "Qǐng búyào suíyì yídòng zhèxiē wùpǐn.", "meaningVi": "Xin đừng tùy tiện di chuyển những đồ vật này."}],
    "hsk5_1358": [{"chinese": "祝你一路顺风。", "pinyin": "Zhù nǐ yílù shùnfēng.", "meaningVi": "Chúc bạn thượng lộ bình an."}],
    "hsk5_1359": [{"chinese": "关于这一点，我还有疑问。", "pinyin": "Guānyú zhè yì diǎn, wǒ hái yǒu yíwèn.", "meaningVi": "Về điểm này, tôi vẫn còn nghi vấn."}],
    "hsk5_136": [{"chinese": "这种做法可以降低成本。", "pinyin": "Zhè zhǒng zuòfǎ kěyǐ jiàngdī chéngběn.", "meaningVi": "Cách làm này có thể giảm chi phí."}],
    "hsk5_1363": [{"chinese": "会议邀请了老师、学生以及家长参加。", "pinyin": "Huìyì yāoqǐngle lǎoshī, xuésheng yǐjí jiāzhǎng cānjiā.", "meaningVi": "Cuộc họp mời giáo viên, học sinh cùng với phụ huynh tham gia."}],
    "hsk5_1364": [{"chinese": "自从上个月以来，他每天都在学中文。", "pinyin": "Zìcóng shàng gè yuè yǐlái, tā měitiān dōu zài xué Zhōngwén.", "meaningVi": "Kể từ tháng trước đến nay, mỗi ngày anh ấy đều học tiếng Trung."}],
    "hsk5_1365": [{"chinese": "这个国家的人口超过十亿。", "pinyin": "Zhège guójiā de rénkǒu chāoguò shí yì.", "meaningVi": "Dân số của quốc gia này vượt quá một tỷ."}],
    "hsk5_1368": [{"chinese": "这意味着我们的努力没有白费。", "pinyin": "Zhè yìwèizhe wǒmen de nǔlì méiyǒu báifèi.", "meaningVi": "Điều này có nghĩa là nỗ lực của chúng ta không uổng phí."}],
    "hsk5_137": [{"chinese": "他愿意承担这次失败的后果。", "pinyin": "Tā yuànyì chéngdān zhè cì shībài de hòuguǒ.", "meaningVi": "Anh ấy sẵn sàng chịu trách nhiệm về hậu quả của thất bại lần này."}],
    "hsk5_1370": [{"chinese": "这件事对他意义重大。", "pinyin": "Zhè jiàn shì duì tā yìyì zhòngdà.", "meaningVi": "Việc này có ý nghĩa to lớn đối với anh ấy."}],
    "hsk5_1371": [{"chinese": "他准备充分，因而考试很顺利。", "pinyin": "Tā zhǔnbèi chōngfèn, yīn'ér kǎoshì hěn shùnlì.", "meaningVi": "Anh ấy chuẩn bị đầy đủ, do đó kỳ thi rất suôn sẻ."}],
    "hsk5_1372": [{"chinese": "请把电视的音量调小一点。", "pinyin": "Qǐng bǎ diànshì de yīnliàng tiáo xiǎo yìdiǎn.", "meaningVi": "Xin vặn nhỏ âm lượng tivi lại một chút."}],
    "hsk5_1373": [{"chinese": "天气是影响出行的重要因素。", "pinyin": "Tiānqì shì yǐngxiǎng chūxíng de zhòngyào yīnsù.", "meaningVi": "Thời tiết là nhân tố quan trọng ảnh hưởng đến việc đi lại."}],
    "hsk5_1374": [{"chinese": "这家公司引进了先进的设备。", "pinyin": "Zhè jiā gōngsī yǐnjìnle xiānjìn de shèbèi.", "meaningVi": "Công ty này đã đưa vào thiết bị tiên tiến."}],
    "hsk5_1375": [{"chinese": "健康的饮食习惯很重要。", "pinyin": "Jiànkāng de yǐnshí xíguàn hěn zhòngyào.", "meaningVi": "Thói quen ăn uống lành mạnh rất quan trọng."}],
    "hsk5_1376": [{"chinese": "这本书是在国外印刷的。", "pinyin": "Zhè běn shū shì zài guówài yìnshuā de.", "meaningVi": "Cuốn sách này được in ở nước ngoài."}],
    "hsk5_1377": [{"chinese": "我们应当遵守交通规则。", "pinyin": "Wǒmen yīngdāng zūnshǒu jiāotōng guīzé.", "meaningVi": "Chúng ta nên tuân thủ luật giao thông."}],
    "hsk5_1378": [{"chinese": "大家出门迎客。", "pinyin": "Dàjiā chūmén yíng kè.", "meaningVi": "Mọi người ra cửa đón khách."}],
    "hsk5_1379": [{"chinese": "我们去机场迎接远方的客人。", "pinyin": "Wǒmen qù jīchǎng yíngjiē yuǎnfāng de kèrén.", "meaningVi": "Chúng tôi đến sân bay đón khách từ xa."}],
    "hsk5_138": [{"chinese": "他的中文已经达到了很高的程度。", "pinyin": "Tā de Zhōngwén yǐjīng dádàole hěn gāo de chéngdù.", "meaningVi": "Tiếng Trung của anh ấy đã đạt đến trình độ rất cao."}],
    "hsk5_1380": [{"chinese": "这道菜营养很丰富。", "pinyin": "Zhè dào cài yíngyǎng hěn fēngfù.", "meaningVi": "Món ăn này rất giàu dinh dưỡng."}],
    "hsk5_1381": [{"chinese": "这家商店二十四小时营业。", "pinyin": "Zhè jiā shāngdiàn èrshísì xiǎoshí yíngyè.", "meaningVi": "Cửa hàng này kinh doanh hai mươi bốn giờ."}],
    "hsk5_1382": [{"chinese": "这部影片获得了很高的评价。", "pinyin": "Zhè bù yǐngpiàn huòdéle hěn gāo de píngjià.", "meaningVi": "Bộ phim này đã nhận được đánh giá rất cao."}],
    "hsk5_1383": [{"chinese": "他从事影视行业多年。", "pinyin": "Tā cóngshì yǐngshì hángyè duō nián.", "meaningVi": "Anh ấy làm việc trong ngành điện ảnh truyền hình đã nhiều năm."}],
    "hsk5_1385": [{"chinese": "我们要学会应对各种突发情况。", "pinyin": "Wǒmen yào xuéhuì yìngduì gèzhǒng tūfā qíngkuàng.", "meaningVi": "Chúng ta phải học cách ứng phó với các tình huống bất ngờ."}],
    "hsk5_1388": [{"chinese": "他们紧紧地拥抱在一起。", "pinyin": "Tāmen jǐnjǐn de yōngbào zài yìqǐ.", "meaningVi": "Họ ôm chặt lấy nhau."}],
    "hsk5_1389": [{"chinese": "他拥有一辆漂亮的跑车。", "pinyin": "Tā yōngyǒu yí liàng piàoliang de pǎochē.", "meaningVi": "Anh ấy sở hữu một chiếc xe thể thao đẹp."}],
    "hsk5_139": [{"chinese": "请查看产品的成分说明。", "pinyin": "Qǐng chákàn chǎnpǐn de chéngfèn shuōmíng.", "meaningVi": "Xin xem phần giải thích thành phần của sản phẩm."}],
    "hsk5_1390": [{"chinese": "他鼓起勇气向她表白。", "pinyin": "Tā gǔqǐ yǒngqì xiàng tā biǎobái.", "meaningVi": "Anh ấy lấy hết dũng khí để tỏ tình với cô ấy."}],
    "hsk5_1391": [{"chinese": "请看清楚这个词的用法。", "pinyin": "Qǐng kàn qīngchu zhège cí de yòngfǎ.", "meaningVi": "Xin xem kỹ cách dùng của từ này."}],
    "hsk5_1392": [{"chinese": "这款软件有上千万用户。", "pinyin": "Zhè kuǎn ruǎnjiàn yǒu shàng qiānwàn yònghù.", "meaningVi": "Phần mềm này có hàng chục triệu người dùng."}],
    "hsk5_1393": [{"chinese": "请用力推门。", "pinyin": "Qǐng yònglì tuī mén.", "meaningVi": "Xin dùng sức đẩy cửa."}],
    "hsk5_1394": [{"chinese": "这里出售各种日常用品。", "pinyin": "Zhèlǐ chūshòu gèzhǒng rìcháng yòngpǐn.", "meaningVi": "Ở đây bán các loại đồ dùng hàng ngày."}],
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
