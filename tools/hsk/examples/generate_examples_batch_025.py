"""P5.10.3 (continued) -- Batch 025 (continues immediately after
examples_batch_024.json; entirely within HSK6, hsk6_0287-hsk6_0588).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Numeric-suffix homograph records (needs_review) ***
Two records in this batch carry the HSK6 numeric-suffix homograph-
disambiguation pattern first identified in batch 024 (乘2): 副2
(hsk6_0407) and 该2 (hsk6_0413). The literal strings "副2" and "该2"
can never appear in natural Chinese text, so no authored example
could honestly satisfy target_word_present. Per the established rule
("mark needs_review rather than fabricate", same treatment as batch
024's 乘2 and the P5.10.2 pilot's hsk6_0027), both are left with an
empty examples list and qaStatus "needs_review". The underlying
production records are untouched. Ten further such records remain
further along in HSK6's queue (局1/局2, 料1/料2, 露1, 升2, 所2, 则1,
支2) and will need identical treatment when their batches are reached.

*** Extremely dense homophone/polyphonic landscape (entirely HSK6) ***
This batch continues and extends the pipeline's largest recurring
clusters, none flagged by the mechanical tier system (it compares the
`word` string, and every pair below is a different word):
  - gāo (1st tone), now the single largest cluster in the whole
    pipeline: nine new members here (高层/高超/高等/高端/高峰/高尚/
    高手/高新技术/高原) added to the fourteen already published across
    batches 011 (高价/高考/高速/高温/高于) and 022 (高大/高档/高级/
    高科技/高效) -- twenty-three members total, all kept in genuinely
    distinct real-world contexts.
  - gōng (1st tone) across five characters (公/工/攻/供/功), now
    roughly thirty members combined with the already-published
    公布/工程/工程师/工具/功能/公平/公务员/工业/工艺/公寓 (batch 022)
    and 共/共同/共享 (batches 016/020/022).
  - fā (1st tone), ten new members (发病/发愁/发电/发动/发放/发光/
    发票/发行/发炎/发育) added to the already-published 发表/发布/
    发挥/发起 (batch 022).
  - fēn (1st tone), four new members (分工/分级/分期/分散) plus 氛围
    (same reading, different character) added to the already-
    published 分布/分类/分离/分配/分手/分享 (batch 022).
  - hǎo/hào: 好不/好感/好容易 (hǎo, "good") kept distinct from 好客/
    好学 (hào, the polyphonic "to be fond of" reading of the same
    character) -- both readings given correctly, and both kept
    distinct from the already-published 好处/好笑/好评/好运/好转/好奇
    (batch 022).
  - guān (1st tone) across three characters (官/关/观): eight new
    members here, distinct from the already-published 观看/观众
    (batch 011) and 观察/观点/观念 (batch 022).
  - guó/guò/hǎi/hé/hòu/huí clusters continuing from their respective
    already-published families (国画/国庆, 过程/过度/过分/过期/过于,
    海洋/海关/海外/海鲜, 合/合法/合理/合同/合作, 后果/后悔, 回忆/回复/
    回收/回顾-adjacent) -- each new member here anchored to a distinct
    referent.
  - Genuine same-pinyin-different-character pairs newly introduced:
    典/点 (diǎn); 订/定 continuing from batch 010's 订/定; 栋/动 (dòng);
    毒/独 (dú, distinct from batch 022's 独特/独自); 番/翻 (fān,
    distinct from batch 022's 翻/番茄); 房/防/妨 (fáng); 服/浮/福/幅/
    符 (fú, five characters); 肝/干 (gān, distinct from the already-
    published 干杯/干活儿); 姑/估/孤 (gū); 顾/固/故 (gù); 归/规 (guī);
    跪/贵/柜 (guì); 壶/湖/胡/蝴 (hú, four characters); 户/互/护 (hù);
    化/话/画/划 (huà, four characters); 患/换/幻 (huàn); 灰/挥 (huī);
    会/汇 (huì).
  - Polyphonic characters given their correct reading per sense: 调
    (调动 = diàodòng, the diào reading, distinct from the already-
    published tiáo-reading 调整/调皮/调研); 都 (都市 = dūshì, the dū
    reading, distinct from the everyday dōu "all/also"); 给 (给予 =
    jǐyǔ, the formal jǐ reading, distinct from everyday gěi "to
    give"); 还 (还原 = huányuán, the "to restore" reading, distinct
    from the adverb hái "still/also").

Self-caught near-duplicate/exact-duplicate revisions made during
drafting (before this batch was finalized):
  - 动听 (dòngtīng): first draft "她的歌声很动听。" was a near-
    template match against 动人's own draft in batch 024 (hsk5_291:
    "她的歌声十分动人。", same subject 歌声) -- rewritten to "这首曲子
    旋律动听。".
  - 反思 (fǎnsī): first draft "我们应该反思自己的行为。" risked
    thematic overlap with 深刻's own batch-024 draft ("他对这次失败
    进行了深刻的反思。", also about reflecting on failure) -- rewritten
    to "犯了错误就要认真反思。".
  - 肥沃 (féiwò): first draft "这片土地十分肥沃。" was a near-
    duplicate of 土地's own already-published example (batch 021,
    hsk5_1153: "这片土地很肥沃。", differing by only 十分/很) --
    rewritten to "这里的土壤非常肥沃，适合种植水果。".
  - 滑行 (huáxíng): first draft "飞机正在跑道上滑行。" would have been
    an EXACT duplicate of 跑道's own already-published example (batch
    023, hsk5_814: "飞机正在跑道上滑行。") -- rewritten to "滑板车在
    人行道上滑行。".
  - 汇 (huì): first draft "请把钱汇到我的账户。" was a near-template
    match against 账户's own already-published example (batch 021,
    hsk5_1476: "请把钱转到我的账户。", differing by only 汇/转) --
    rewritten to "这是一笔跨国汇款。".
  All re-verified against the full pilot+002-024 corpus with zero
  remaining exact duplicates and zero near-template flags (see
  validation report).

Validator-caught fix (found by validate_examples_batch_p103.py's
no_duplicate_sentences_across_pilot_and_batches check): 国宝
(guóbǎo)'s first draft "大熊猫是中国的国宝。" was an EXACT duplicate
of 大熊猫's own already-published example (batch 005, hsk3_076:
"大熊猫是中国的国宝。") -- rewritten to "这件青铜器被视为国宝。".

Automated near-template pass (character-bigram Jaccard similarity
against the full pilot+002-024 corpus) caught two further near-
duplicates fixed after the manual drafting pass:
  - 订婚 (dìnghūn): first draft "他们下个月订婚。" was a near-
    template match against the near-synonym 结婚's own already-
    published example (batch 004, hsk3_209: "他们下个月结婚。") --
    rewritten to "他向女朋友求婚并订婚了。".
  - 古典 (gǔdiǎn): first draft "她喜欢古典音乐。" was a near-template
    match against an existing HSK3-lineage example (hsk3_435: "她喜欢
    听古典音乐。") -- rewritten to "这栋建筑是古典风格的。".
  Both re-verified with zero remaining flags.

Usage:
    python generate_examples_batch_025.py --dry-run
    python generate_examples_batch_025.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 25
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_025.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# Records deliberately left with 0 examples (see module docstring):
# HSK6's numeric-suffix homograph pattern makes the literal target
# word unmatchable in natural Chinese text.
NEEDS_REVIEW_IDS = {"hsk6_0407", "hsk6_0413"}

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk6_0287": [{"chinese": "水龙头在滴水。", "pinyin": "Shuǐlóngtóu zài dī shuǐ.", "meaningVi": "Vòi nước đang nhỏ giọt."}],
    "hsk6_0288": [{"chinese": "我们提倡低碳生活。", "pinyin": "Wǒmen tíchàng dītàn shēnghuó.", "meaningVi": "Chúng tôi đề xướng cuộc sống ít carbon."}],
    "hsk6_0289": [{"chinese": "飞机准时抵达机场。", "pinyin": "Fēijī zhǔnshí dǐdá jīchǎng.", "meaningVi": "Máy bay đến sân bay đúng giờ."}],
    "hsk6_0290": [{"chinese": "身体需要抵抗疾病的能力。", "pinyin": "Shēntǐ xūyào dǐkàng jíbìng de nénglì.", "meaningVi": "Cơ thể cần có khả năng chống lại bệnh tật."}],
    "hsk6_0291": [{"chinese": "他的普通话说得很地道。", "pinyin": "Tā de pǔtōnghuà shuō de hěn dìdao.", "meaningVi": "Tiếng phổ thông của anh ấy nói rất chuẩn."}],
    "hsk6_0293": [{"chinese": "这里地形复杂。", "pinyin": "Zhèlǐ dìxíng fùzá.", "meaningVi": "Địa hình ở đây phức tạp."}],
    "hsk6_0294": [{"chinese": "不同地域有不同的风俗。", "pinyin": "Bùtóng dìyù yǒu bùtóng de fēngsú.", "meaningVi": "Vùng miền khác nhau có phong tục khác nhau."}],
    "hsk6_0295": [{"chinese": "他是研究地质的专家。", "pinyin": "Tā shì yánjiū dìzhì de zhuānjiā.", "meaningVi": "Anh ấy là chuyên gia nghiên cứu địa chất."}],
    "hsk6_0296": [{"chinese": "请点击这个链接。", "pinyin": "Qǐng diǎnjī zhège liànjiē.", "meaningVi": "Xin nhấp vào liên kết này."}],
    "hsk6_0297": [{"chinese": "毕业典礼明天举行。", "pinyin": "Bìyè diǎnlǐ míngtiān jǔxíng.", "meaningVi": "Lễ tốt nghiệp sẽ được tổ chức vào ngày mai."}],
    "hsk6_0298": [{"chinese": "他点燃了一支蜡烛。", "pinyin": "Tā diǎnránle yì zhī làzhú.", "meaningVi": "Anh ấy đã thắp một cây nến."}],
    "hsk6_0299": [{"chinese": "这是一个典型的例子。", "pinyin": "Zhè shì yí gè diǎnxíng de lìzi.", "meaningVi": "Đây là một ví dụ điển hình."}],
    "hsk6_0300": [{"chinese": "妈妈用电饭锅煮饭。", "pinyin": "Māma yòng diànfànguō zhǔ fàn.", "meaningVi": "Mẹ dùng nồi cơm điện để nấu cơm."}],
    "hsk6_0301": [{"chinese": "这个地区电力供应充足。", "pinyin": "Zhège dìqū diànlì gōngyìng chōngzú.", "meaningVi": "Nguồn cung cấp điện của khu vực này đầy đủ."}],
    "hsk6_0302": [{"chinese": "这条街上有很多店铺。", "pinyin": "Zhè tiáo jiē shàng yǒu hěn duō diànpù.", "meaningVi": "Trên con phố này có rất nhiều cửa hàng."}],
    "hsk6_0303": [{"chinese": "请关闭电源。", "pinyin": "Qǐng guānbì diànyuán.", "meaningVi": "Xin tắt nguồn điện."}],
    "hsk6_0304": [{"chinese": "灯从天花板上吊下来。", "pinyin": "Dēng cóng tiānhuābǎn shàng diào xiàlai.", "meaningVi": "Đèn được treo từ trên trần nhà xuống."}],
    "hsk6_0305": [{"chinese": "他被调动到了新部门。", "pinyin": "Tā bèi diàodòng dàole xīn bùmén.", "meaningVi": "Anh ấy đã được điều chuyển đến bộ phận mới."}],
    "hsk6_0306": [{"chinese": "周末我喜欢去钓鱼。", "pinyin": "Zhōumò wǒ xǐhuan qù diàoyú.", "meaningVi": "Cuối tuần tôi thích đi câu cá."}],
    "hsk6_0307": [{"chinese": "股票价格大跌。", "pinyin": "Gǔpiào jiàgé dà diē.", "meaningVi": "Giá cổ phiếu sụt giảm mạnh."}],
    "hsk6_0308": [{"chinese": "他爬到了山顶。", "pinyin": "Tā pádàole shāndǐng.", "meaningVi": "Anh ấy đã trèo lên đến đỉnh núi."}],
    "hsk6_0309": [{"chinese": "我们收到了一份新订单。", "pinyin": "Wǒmen shōudàole yí fèn xīn dìngdān.", "meaningVi": "Chúng tôi đã nhận được một đơn đặt hàng mới."}],
    "hsk6_0310": [{"chinese": "他向女朋友求婚并订婚了。", "pinyin": "Tā xiàng nǚpéngyou qiúhūn bìng dìnghūn le.", "meaningVi": "Anh ấy đã cầu hôn bạn gái và đính hôn."}],
    "hsk6_0311": [{"chinese": "这款产品的定价偏高。", "pinyin": "Zhè kuǎn chǎnpǐn de dìngjià piān gāo.", "meaningVi": "Giá niêm yết của sản phẩm này hơi cao."}],
    "hsk6_0312": [{"chinese": "请设置一个定时提醒。", "pinyin": "Qǐng shèzhì yí gè dìngshí tíxǐng.", "meaningVi": "Xin đặt một lời nhắc theo giờ cố định."}],
    "hsk6_0313": [{"chinese": "手机可以帮你定位。", "pinyin": "Shǒujī kěyǐ bāng nǐ dìngwèi.", "meaningVi": "Điện thoại có thể giúp bạn định vị."}],
    "hsk6_0314": [{"chinese": "请给出这个词的定义。", "pinyin": "Qǐng gěichū zhège cí de dìngyì.", "meaningVi": "Xin đưa ra định nghĩa của từ này."}],
    "hsk6_0315": [{"chinese": "这件衣服是定制的。", "pinyin": "Zhè jiàn yīfu shì dìngzhì de.", "meaningVi": "Chiếc áo này là được đặt may riêng."}],
    "hsk6_0316": [{"chinese": "那栋楼是新建的。", "pinyin": "Nà dòng lóu shì xīnjiàn de.", "meaningVi": "Tòa nhà đó là mới xây."}],
    "hsk6_0317": [{"chinese": "他的动机不太单纯。", "pinyin": "Tā de dòngjī bú tài dānchún.", "meaningVi": "Động cơ của anh ấy không đơn thuần lắm."}],
    "hsk6_0318": [{"chinese": "兴趣是学习的动力。", "pinyin": "Xìngqù shì xuéxí de dònglì.", "meaningVi": "Hứng thú là động lực của việc học."}],
    "hsk6_0319": [{"chinese": "他从小喜欢看动漫。", "pinyin": "Tā cóngxiǎo xǐhuan kàn dòngmàn.", "meaningVi": "Anh ấy thích xem hoạt hình từ nhỏ."}],
    "hsk6_0320": [{"chinese": "请随时关注最新动态。", "pinyin": "Qǐng suíshí guānzhù zuìxīn dòngtài.", "meaningVi": "Xin luôn theo dõi động thái mới nhất."}],
    "hsk6_0321": [{"chinese": "这首曲子旋律动听。", "pinyin": "Zhè shǒu qǔzi xuánlǜ dòngtīng.", "meaningVi": "Giai điệu của bản nhạc này rất du dương."}],
    "hsk6_0322": [{"chinese": "他喜欢逗小孩子玩。", "pinyin": "Tā xǐhuan dòu xiǎo háizi wán.", "meaningVi": "Anh ấy thích trêu đùa với trẻ con."}],
    "hsk6_0323": [{"chinese": "他们为自由而斗争。", "pinyin": "Tāmen wèi zìyóu ér dòuzhēng.", "meaningVi": "Họ đấu tranh vì tự do."}],
    "hsk6_0324": [{"chinese": "她向往大都市的生活。", "pinyin": "Tā xiàngwǎng dà dūshì de shēnghuó.", "meaningVi": "Cô ấy khao khát cuộc sống ở đô thị lớn."}],
    "hsk6_0325": [{"chinese": "这种蘑菇有毒。", "pinyin": "Zhè zhǒng mógu yǒu dú.", "meaningVi": "Loại nấm này có độc."}],
    "hsk6_0326": [{"chinese": "他们乘船渡过了这条河。", "pinyin": "Tāmen chéngchuán dùguòle zhè tiáo hé.", "meaningVi": "Họ đi thuyền vượt qua con sông này."}],
    "hsk6_0327": [{"chinese": "请把杯子端稳。", "pinyin": "Qǐng bǎ bēizi duān wěn.", "meaningVi": "Xin bưng cốc cho chắc."}],
    "hsk6_0328": [{"chinese": "目前市场上原材料短缺。", "pinyin": "Mùqián shìchǎng shàng yuáncáiliào duǎnquē.", "meaningVi": "Hiện tại nguyên liệu trên thị trường đang thiếu hụt."}],
    "hsk6_0329": [{"chinese": "这座建筑左右对称。", "pinyin": "Zhè zuò jiànzhù zuǒyòu duìchèn.", "meaningVi": "Kiến trúc này đối xứng trái phải."}],
    "hsk6_0330": [{"chinese": "两个部门需要对接工作。", "pinyin": "Liǎng gè bùmén xūyào duìjiē gōngzuò.", "meaningVi": "Hai bộ phận cần phối hợp công việc."}],
    "hsk6_0331": [{"chinese": "双方展开了激烈的对抗。", "pinyin": "Shuāngfāng zhǎnkāile jīliè de duìkàng.", "meaningVi": "Hai bên đã diễn ra cuộc đối đầu kịch liệt."}],
    "hsk6_0332": [{"chinese": "这两种观点是对立的。", "pinyin": "Zhè liǎng zhǒng guāndiǎn shì duìlì de.", "meaningVi": "Hai quan điểm này là đối lập nhau."}],
    "hsk6_0333": [{"chinese": "每个问题都有对应的答案。", "pinyin": "Měi gè wèntí dōu yǒu duìyìng de dá'àn.", "meaningVi": "Mỗi câu hỏi đều có câu trả lời tương ứng."}],
    "hsk6_0334": [{"chinese": "他蹲在地上系鞋带。", "pinyin": "Tā dūn zài dìshang jì xiédài.", "meaningVi": "Anh ấy ngồi xổm trên đất buộc dây giày."}],
    "hsk6_0335": [{"chinese": "听到这个消息，大家顿时安静下来。", "pinyin": "Tīngdào zhège xiāoxi, dàjiā dùnshí ānjìng xiàlai.", "meaningVi": "Nghe được tin này, mọi người lập tức im lặng."}],
    "hsk6_0336": [{"chinese": "她是一个多才多艺的女孩。", "pinyin": "Tā shì yí gè duōcái-duōyì de nǚhái.", "meaningVi": "Cô ấy là một cô gái đa tài đa nghệ."}],
    "hsk6_0337": [{"chinese": "多亏你的帮助，我们才顺利完成任务。", "pinyin": "Duōkuī nǐ de bāngzhù, wǒmen cái shùnlì wánchéng rènwu.", "meaningVi": "Nhờ có sự giúp đỡ của bạn, chúng tôi mới hoàn thành nhiệm vụ thuận lợi."}],
    "hsk6_0338": [{"chinese": "教室里安装了多媒体设备。", "pinyin": "Jiàoshì lǐ ānzhuāngle duōméitǐ shèbèi.", "meaningVi": "Trong lớp học đã lắp đặt thiết bị đa phương tiện."}],
    "hsk6_0339": [{"chinese": "这句话有点多余。", "pinyin": "Zhè jù huà yǒudiǎn duōyú.", "meaningVi": "Câu nói này hơi thừa."}],
    "hsk6_0340": [{"chinese": "现代社会文化多元。", "pinyin": "Xiàndài shèhuì wénhuà duōyuán.", "meaningVi": "Xã hội hiện đại có văn hóa đa nguyên."}],
    "hsk6_0341": [{"chinese": "他成功夺得了冠军。", "pinyin": "Tā chénggōng duódéle guànjūn.", "meaningVi": "Anh ấy đã thành công giành được chức vô địch."}],
    "hsk6_0342": [{"chinese": "敌军企图夺取这座城市。", "pinyin": "Díjūn qǐtú duóqǔ zhè zuò chéngshì.", "meaningVi": "Quân địch mưu toan chiếm đoạt thành phố này."}],
    "hsk6_0343": [{"chinese": "他躲避着人群，快步走开。", "pinyin": "Tā duǒbìzhe rénqún, kuàibù zǒukāi.", "meaningVi": "Anh ấy né tránh đám đông, rảo bước rời đi."}],
    "hsk6_0344": [{"chinese": "闻到这个味道我觉得恶心。", "pinyin": "Wéndào zhège wèidào wǒ juéde ěxin.", "meaningVi": "Ngửi thấy mùi này tôi cảm thấy buồn nôn."}],
    "hsk6_0345": [{"chinese": "今天天气条件十分恶劣。", "pinyin": "Jīntiān tiānqì tiáojiàn shífēn èliè.", "meaningVi": "Điều kiện thời tiết hôm nay vô cùng khắc nghiệt."}],
    "hsk6_0346": [{"chinese": "她带孩子去了儿科看病。", "pinyin": "Tā dài háizi qùle érkē kànbìng.", "meaningVi": "Cô ấy đưa con đến khoa nhi khám bệnh."}],
    "hsk6_0347": [{"chinese": "她戴着一对耳环。", "pinyin": "Tā dàizhe yí duì ěrhuán.", "meaningVi": "Cô ấy đeo một đôi khuyên tai."}],
    "hsk6_0348": [{"chinese": "植物吸收二氧化碳，释放氧气。", "pinyin": "Zhíwù xīshōu èryǎnghuàtàn, shìfàng yǎngqì.", "meaningVi": "Thực vật hấp thụ khí cacbonic, thải ra khí oxy."}],
    "hsk6_0349": [{"chinese": "这种病一般在冬天发病。", "pinyin": "Zhè zhǒng bìng yìbān zài dōngtiān fābìng.", "meaningVi": "Loại bệnh này thường phát bệnh vào mùa đông."}],
    "hsk6_0350": [{"chinese": "别为这点小事发愁。", "pinyin": "Bié wèi zhè diǎn xiǎoshì fāchóu.", "meaningVi": "Đừng lo lắng vì chuyện nhỏ này."}],
    "hsk6_0351": [{"chinese": "这座水坝用来发电。", "pinyin": "Zhè zuò shuǐbà yònglái fādiàn.", "meaningVi": "Con đập này được dùng để phát điện."}],
    "hsk6_0352": [{"chinese": "请先发动汽车。", "pinyin": "Qǐng xiān fādòng qìchē.", "meaningVi": "Xin khởi động xe hơi trước."}],
    "hsk6_0353": [{"chinese": "公司按时发放工资。", "pinyin": "Gōngsī ànshí fāfàng gōngzī.", "meaningVi": "Công ty phát lương đúng hạn."}],
    "hsk6_0354": [{"chinese": "这种材料能在黑暗中发光。", "pinyin": "Zhè zhǒng cáiliào néng zài hēi'àn zhōng fāguāng.", "meaningVi": "Loại vật liệu này có thể phát sáng trong bóng tối."}],
    "hsk6_0355": [{"chinese": "请给我开一张发票。", "pinyin": "Qǐng gěi wǒ kāi yì zhāng fāpiào.", "meaningVi": "Xin xuất cho tôi một hóa đơn."}],
    "hsk6_0356": [{"chinese": "这本书即将正式发行。", "pinyin": "Zhè běn shū jíjiāng zhèngshì fāxíng.", "meaningVi": "Cuốn sách này sắp được chính thức phát hành."}],
    "hsk6_0357": [{"chinese": "他的伤口有点发炎。", "pinyin": "Tā de shāngkǒu yǒudiǎn fāyán.", "meaningVi": "Vết thương của anh ấy hơi bị viêm."}],
    "hsk6_0358": [{"chinese": "孩子正处于发育阶段。", "pinyin": "Háizi zhèng chǔyú fāyù jiēduàn.", "meaningVi": "Đứa trẻ đang ở giai đoạn phát triển."}],
    "hsk6_0359": [{"chinese": "十八岁是法定成年年龄。", "pinyin": "Shíbā suì shì fǎdìng chéngnián niánlíng.", "meaningVi": "Mười tám tuổi là độ tuổi trưởng thành theo pháp định."}],
    "hsk6_0360": [{"chinese": "法官宣布了判决结果。", "pinyin": "Fǎguān xuānbùle pànjué jiéguǒ.", "meaningVi": "Thẩm phán đã tuyên bố kết quả phán quyết."}],
    "hsk6_0361": [{"chinese": "企业必须遵守相关法规。", "pinyin": "Qǐyè bìxū zūnshǒu xiāngguān fǎguī.", "meaningVi": "Doanh nghiệp phải tuân thủ các quy định pháp luật liên quan."}],
    "hsk6_0362": [{"chinese": "他经历了一番波折。", "pinyin": "Tā jīnglìle yì fān bōzhé.", "meaningVi": "Anh ấy đã trải qua một phen sóng gió."}],
    "hsk6_0363": [{"chinese": "他工作十分繁忙。", "pinyin": "Tā gōngzuò shífēn fánmáng.", "meaningVi": "Công việc của anh ấy vô cùng bận rộn."}],
    "hsk6_0364": [{"chinese": "凡是参加的人都能获得礼品。", "pinyin": "Fánshì cānjiā de rén dōu néng huòdé lǐpǐn.", "meaningVi": "Bất cứ ai tham gia đều có thể nhận được quà tặng."}],
    "hsk6_0365": [{"chinese": "这种鱼繁殖能力很强。", "pinyin": "Zhè zhǒng yú fánzhí nénglì hěn qiáng.", "meaningVi": "Loại cá này có khả năng sinh sản rất mạnh."}],
    "hsk6_0366": [{"chinese": "请给我们一些反馈意见。", "pinyin": "Qǐng gěi wǒmen yìxiē fǎnkuì yìjiàn.", "meaningVi": "Xin cho chúng tôi một số ý kiến phản hồi."}],
    "hsk6_0367": [{"chinese": "犯了错误就要认真反思。", "pinyin": "Fànle cuòwù jiù yào rènzhēn fǎnsī.", "meaningVi": "Phạm lỗi thì phải suy ngẫm nghiêm túc."}],
    "hsk6_0368": [{"chinese": "他犯了一个严重的错误。", "pinyin": "Tā fànle yí gè yánzhòng de cuòwù.", "meaningVi": "Anh ấy đã phạm phải một lỗi nghiêm trọng."}],
    "hsk6_0369": [{"chinese": "这个计划考虑到了方方面面。", "pinyin": "Zhège jìhuà kǎolǜdàole fāngfāngmiànmiàn.", "meaningVi": "Kế hoạch này đã xem xét đến mọi mặt."}],
    "hsk6_0370": [{"chinese": "请确认一下方位。", "pinyin": "Qǐng quèrèn yíxià fāngwèi.", "meaningVi": "Xin xác nhận phương hướng."}],
    "hsk6_0371": [{"chinese": "他能听懂几种方言。", "pinyin": "Tā néng tīngdǒng jǐ zhǒng fāngyán.", "meaningVi": "Anh ấy có thể nghe hiểu vài loại phương ngữ."}],
    "hsk6_0372": [{"chinese": "请不要妨碍别人工作。", "pinyin": "Qǐng búyào fáng'ài biéren gōngzuò.", "meaningVi": "Xin đừng cản trở người khác làm việc."}],
    "hsk6_0373": [{"chinese": "这个城市的房价很高。", "pinyin": "Zhège chéngshì de fángjià hěn gāo.", "meaningVi": "Giá nhà của thành phố này rất cao."}],
    "hsk6_0374": [{"chinese": "这项工作重点是防治污染。", "pinyin": "Zhè xiàng gōngzuò zhòngdiǎn shì fángzhì wūrǎn.", "meaningVi": "Trọng tâm của công việc này là phòng chống ô nhiễm."}],
    "hsk6_0375": [{"chinese": "这是一次深入的访谈。", "pinyin": "Zhè shì yí cì shēnrù de fǎngtán.", "meaningVi": "Đây là một cuộc phỏng vấn sâu sắc."}],
    "hsk6_0376": [{"chinese": "请把这张图片放大。", "pinyin": "Qǐng bǎ zhè zhāng túpiàn fàngdà.", "meaningVi": "Xin phóng to bức ảnh này."}],
    "hsk6_0377": [{"chinese": "孩子们放飞了气球。", "pinyin": "Háizimen fàngfēile qìqiú.", "meaningVi": "Bọn trẻ đã thả bay bóng bay."}],
    "hsk6_0378": [{"chinese": "科技正在飞速发展。", "pinyin": "Kējì zhèngzài fēisù fāzhǎn.", "meaningVi": "Khoa học công nghệ đang phát triển với tốc độ nhanh chóng."}],
    "hsk6_0379": [{"chinese": "这块地很肥。", "pinyin": "Zhè kuài dì hěn féi.", "meaningVi": "Mảnh đất này rất màu mỡ."}],
    "hsk6_0380": [{"chinese": "肥胖会带来很多健康问题。", "pinyin": "Féipàng huì dàilái hěn duō jiànkāng wèntí.", "meaningVi": "Béo phì sẽ mang lại nhiều vấn đề sức khỏe."}],
    "hsk6_0381": [{"chinese": "这里的土壤非常肥沃，适合种植水果。", "pinyin": "Zhèlǐ de tǔrǎng fēicháng féiwò, shìhé zhòngzhí shuǐguǒ.", "meaningVi": "Đất ở đây rất màu mỡ, thích hợp trồng trái cây."}],
    "hsk6_0382": [{"chinese": "吸烟会伤害肺部。", "pinyin": "Xīyān huì shānghài fèi bù.", "meaningVi": "Hút thuốc sẽ gây hại cho phổi."}],
    "hsk6_0383": [{"chinese": "他因肺炎住院了。", "pinyin": "Tā yīn fèiyán zhùyuàn le.", "meaningVi": "Anh ấy nhập viện vì viêm phổi."}],
    "hsk6_0384": [{"chinese": "团队成员分工明确。", "pinyin": "Tuánduì chéngyuán fēngōng míngquè.", "meaningVi": "Sự phân công của các thành viên trong nhóm rất rõ ràng."}],
    "hsk6_0385": [{"chinese": "这些产品按质量分级。", "pinyin": "Zhèxiē chǎnpǐn àn zhìliàng fēnjí.", "meaningVi": "Những sản phẩm này được phân cấp theo chất lượng."}],
    "hsk6_0386": [{"chinese": "他选择分期付款购买手机。", "pinyin": "Tā xuǎnzé fēnqī fùkuǎn gòumǎi shǒujī.", "meaningVi": "Anh ấy chọn trả góp để mua điện thoại."}],
    "hsk6_0387": [{"chinese": "请大家分散开来，保持距离。", "pinyin": "Qǐng dàjiā fēnsàn kāilái, bǎochí jùlí.", "meaningVi": "Xin mọi người tản ra, giữ khoảng cách."}],
    "hsk6_0388": [{"chinese": "教室里学习氛围很浓厚。", "pinyin": "Jiàoshì lǐ xuéxí fēnwéi hěn nónghòu.", "meaningVi": "Bầu không khí học tập trong lớp học rất sôi nổi."}],
    "hsk6_0389": [{"chinese": "她用粉底遮盖了雀斑。", "pinyin": "Tā yòng fěndǐ zhēgàile quèbān.", "meaningVi": "Cô ấy dùng phấn nền để che tàn nhang."}],
    "hsk6_0390": [{"chinese": "他难以掩饰内心的愤怒。", "pinyin": "Tā nányǐ yǎnshì nèixīn de fènnù.", "meaningVi": "Anh ấy khó có thể che giấu sự phẫn nộ trong lòng."}],
    "hsk6_0391": [{"chinese": "这条路暂时封闭。", "pinyin": "Zhè tiáo lù zànshí fēngbì.", "meaningVi": "Con đường này tạm thời bị đóng."}],
    "hsk6_0392": [{"chinese": "这里的风光十分秀丽。", "pinyin": "Zhèlǐ de fēngguāng shífēn xiùlì.", "meaningVi": "Phong cảnh ở đây vô cùng tươi đẹp."}],
    "hsk6_0393": [{"chinese": "今天风力较大。", "pinyin": "Jīntiān fēnglì jiào dà.", "meaningVi": "Hôm nay sức gió khá mạnh."}],
    "hsk6_0394": [{"chinese": "今年是个丰收年。", "pinyin": "Jīnnián shì gè fēngshōu nián.", "meaningVi": "Năm nay là một năm được mùa."}],
    "hsk6_0395": [{"chinese": "他们一起经历过很多风雨。", "pinyin": "Tāmen yìqǐ jīnglìguo hěn duō fēngyǔ.", "meaningVi": "Họ đã cùng nhau trải qua rất nhiều sóng gió."}],
    "hsk6_0396": [{"chinese": "老师为教育事业奉献了一生。", "pinyin": "Lǎoshī wèi jiàoyù shìyè fèngxiànle yìshēng.", "meaningVi": "Giáo viên đã cống hiến cả đời cho sự nghiệp giáo dục."}],
    "hsk6_0397": [{"chinese": "请代我向您夫人问好。", "pinyin": "Qǐng dài wǒ xiàng nín fūrén wènhǎo.", "meaningVi": "Xin thay tôi gửi lời hỏi thăm đến phu nhân của ngài."}],
    "hsk6_0398": [{"chinese": "他心服口服。", "pinyin": "Tā xīnfú-kǒufú.", "meaningVi": "Anh ấy tâm phục khẩu phục."}],
    "hsk6_0399": [{"chinese": "树叶漂浮在水面上。", "pinyin": "Shùyè piāofú zài shuǐmiàn shàng.", "meaningVi": "Lá cây trôi nổi trên mặt nước."}],
    "hsk6_0400": [{"chinese": "军人要服从命令。", "pinyin": "Jūnrén yào fúcóng mìnglìng.", "meaningVi": "Quân nhân phải phục tùng mệnh lệnh."}],
    "hsk6_0401": [{"chinese": "今年工资涨幅度不大。", "pinyin": "Jīnnián gōngzī zhǎng fúdù bú dà.", "meaningVi": "Mức tăng lương năm nay không lớn."}],
    "hsk6_0402": [{"chinese": "请注意标点符号的使用。", "pinyin": "Qǐng zhùyì biāodiǎn fúhào de shǐyòng.", "meaningVi": "Xin chú ý cách sử dụng dấu câu."}],
    "hsk6_0403": [{"chinese": "这家公司的福利待遇很好。", "pinyin": "Zhè jiā gōngsī de fúlì dàiyù hěn hǎo.", "meaningVi": "Phúc lợi đãi ngộ của công ty này rất tốt."}],
    "hsk6_0404": [{"chinese": "请按时服用药物。", "pinyin": "Qǐng ànshí fúyòng yàowù.", "meaningVi": "Xin uống thuốc đúng giờ."}],
    "hsk6_0405": [{"chinese": "老师课后给学生辅导功课。", "pinyin": "Lǎoshī kèhòu gěi xuésheng fǔdǎo gōngkè.", "meaningVi": "Giáo viên hướng dẫn bài tập cho học sinh sau giờ học."}],
    "hsk6_0406": [{"chinese": "这个软件可以辅助学习。", "pinyin": "Zhège ruǎnjiàn kěyǐ fǔzhù xuéxí.", "meaningVi": "Phần mềm này có thể hỗ trợ việc học."}],
    "hsk6_0407": [],
    "hsk6_0408": [{"chinese": "大雪覆盖了整座城市。", "pinyin": "Dàxuě fùgàile zhěng zuò chéngshì.", "meaningVi": "Tuyết lớn đã bao phủ cả thành phố."}],
    "hsk6_0409": [{"chinese": "请查收邮件附件。", "pinyin": "Qǐng cháshōu yóujiàn fùjiàn.", "meaningVi": "Xin nhận tệp đính kèm trong email."}],
    "hsk6_0410": [{"chinese": "这件事产生了负面影响。", "pinyin": "Zhè jiàn shì chǎnshēngle fùmiàn yǐngxiǎng.", "meaningVi": "Việc này đã gây ra ảnh hưởng tiêu cực."}],
    "hsk6_0411": [{"chinese": "这个村子越来越富裕了。", "pinyin": "Zhège cūnzi yuèláiyuè fùyù le.", "meaningVi": "Ngôi làng này ngày càng giàu có."}],
    "hsk6_0412": [{"chinese": "法律赋予公民选举的权利。", "pinyin": "Fǎlǜ fùyǔ gōngmín xuǎnjǔ de quánlì.", "meaningVi": "Pháp luật trao cho công dân quyền bầu cử."}],
    "hsk6_0413": [],
    "hsk6_0414": [{"chinese": "这部电影是根据小说改编的。", "pinyin": "Zhè bù diànyǐng shì gēnjù xiǎoshuō gǎibiān de.", "meaningVi": "Bộ phim này được chuyển thể từ tiểu thuyết."}],
    "hsk6_0415": [{"chinese": "这栋老房子经过改造焕然一新。", "pinyin": "Zhè dòng lǎo fángzi jīngguò gǎizào huànrán-yìxīn.", "meaningVi": "Ngôi nhà cũ này sau khi cải tạo đã hoàn toàn đổi mới."}],
    "hsk6_0416": [{"chinese": "中奖的概率很低。", "pinyin": "Zhòngjiǎng de gàilǜ hěn dī.", "meaningVi": "Xác suất trúng thưởng rất thấp."}],
    "hsk6_0417": [{"chinese": "他肝不太好，医生让他戒酒。", "pinyin": "Tā gān bú tài hǎo, yīshēng ràng tā jièjiǔ.", "meaningVi": "Gan của anh ấy không tốt lắm, bác sĩ bảo anh ấy cai rượu."}],
    "hsk6_0418": [{"chinese": "他干脆拒绝了这个提议。", "pinyin": "Tā gāncuì jùjuéle zhège tíyì.", "meaningVi": "Anh ấy đã dứt khoát từ chối đề nghị này."}],
    "hsk6_0419": [{"chinese": "那一刻的气氛非常尴尬。", "pinyin": "Nà yí kè de qìfēn fēicháng gāngà.", "meaningVi": "Bầu không khí lúc đó vô cùng ngượng ngùng."}],
    "hsk6_0420": [{"chinese": "这个地区常年干旱。", "pinyin": "Zhège dìqū chángnián gānhàn.", "meaningVi": "Khu vực này quanh năm hạn hán."}],
    "hsk6_0421": [{"chinese": "请不要干扰他工作。", "pinyin": "Qǐng búyào gānrǎo tā gōngzuò.", "meaningVi": "Xin đừng làm nhiễu công việc của anh ấy."}],
    "hsk6_0422": [{"chinese": "冬天空气比较干燥。", "pinyin": "Dōngtiān kōngqì bǐjiào gānzào.", "meaningVi": "Mùa đông không khí khá khô."}],
    "hsk6_0423": [{"chinese": "我非常感激你的帮助。", "pinyin": "Wǒ fēicháng gǎnjī nǐ de bāngzhù.", "meaningVi": "Tôi vô cùng biết ơn sự giúp đỡ của bạn."}],
    "hsk6_0424": [{"chinese": "听到敲门声，他赶忙起身开门。", "pinyin": "Tīngdào qiāomén shēng, tā gǎnmáng qǐshēn kāimén.", "meaningVi": "Nghe tiếng gõ cửa, anh ấy vội vàng đứng dậy mở cửa."}],
    "hsk6_0425": [{"chinese": "伤口有被感染的风险。", "pinyin": "Shāngkǒu yǒu bèi gǎnrǎn de fēngxiǎn.", "meaningVi": "Vết thương có nguy cơ bị nhiễm trùng."}],
    "hsk6_0426": [{"chinese": "谈谈你的感想吧。", "pinyin": "Tántan nǐ de gǎnxiǎng ba.", "meaningVi": "Hãy nói về cảm tưởng của bạn đi."}],
    "hsk6_0427": [{"chinese": "他喜欢用钢笔写字。", "pinyin": "Tā xǐhuan yòng gāngbǐ xiězì.", "meaningVi": "Anh ấy thích dùng bút máy để viết chữ."}],
    "hsk6_0428": [{"chinese": "这是一座繁忙的港口。", "pinyin": "Zhè shì yí zuò fánmáng de gǎngkǒu.", "meaningVi": "Đây là một cảng biển nhộn nhịp."}],
    "hsk6_0429": [{"chinese": "他坚守在自己的工作岗位上。", "pinyin": "Tā jiānshǒu zài zìjǐ de gōngzuò gǎngwèi shàng.", "meaningVi": "Anh ấy kiên trì bám trụ ở vị trí công việc của mình."}],
    "hsk6_0430": [{"chinese": "公司高层决定进行改革。", "pinyin": "Gōngsī gāocéng juédìng jìnxíng gǎigé.", "meaningVi": "Cấp cao của công ty quyết định tiến hành cải cách."}],
    "hsk6_0431": [{"chinese": "他的技艺十分高超。", "pinyin": "Tā de jìyì shífēn gāochāo.", "meaningVi": "Kỹ thuật của anh ấy vô cùng cao siêu."}],
    "hsk6_0432": [{"chinese": "他在一所高等学府任教。", "pinyin": "Tā zài yì suǒ gāoděng xuéfǔ rènjiào.", "meaningVi": "Anh ấy giảng dạy tại một trường đại học."}],
    "hsk6_0433": [{"chinese": "这是一款高端产品。", "pinyin": "Zhè shì yì kuǎn gāoduān chǎnpǐn.", "meaningVi": "Đây là một sản phẩm cao cấp."}],
    "hsk6_0434": [{"chinese": "早上是交通高峰时段。", "pinyin": "Zǎoshang shì jiāotōng gāofēng shíduàn.", "meaningVi": "Buổi sáng là giờ cao điểm giao thông."}],
    "hsk6_0435": [{"chinese": "他的品格十分高尚。", "pinyin": "Tā de pǐngé shífēn gāoshàng.", "meaningVi": "Phẩm cách của anh ấy vô cùng cao thượng."}],
    "hsk6_0436": [{"chinese": "他是打篮球的高手。", "pinyin": "Tā shì dǎ lánqiú de gāoshǒu.", "meaningVi": "Anh ấy là cao thủ chơi bóng rổ."}],
    "hsk6_0437": [{"chinese": "这家公司专注于高新技术研发。", "pinyin": "Zhè jiā gōngsī zhuānzhù yú gāoxīn-jìshù yánfā.", "meaningVi": "Công ty này chuyên nghiên cứu phát triển công nghệ cao mới."}],
    "hsk6_0438": [{"chinese": "青藏高原海拔很高。", "pinyin": "Qīngzàng Gāoyuán hǎibá hěn gāo.", "meaningVi": "Cao nguyên Thanh Tạng có độ cao rất lớn."}],
    "hsk6_0439": [{"chinese": "请把稿件发给编辑。", "pinyin": "Qǐng bǎ gǎojiàn fā gěi biānjí.", "meaningVi": "Xin gửi bản thảo cho biên tập viên."}],
    "hsk6_0440": [{"chinese": "他正在修改稿子。", "pinyin": "Tā zhèngzài xiūgǎi gǎozi.", "meaningVi": "Anh ấy đang chỉnh sửa bản thảo."}],
    "hsk6_0441": [{"chinese": "他不小心割破了手指。", "pinyin": "Tā bù xiǎoxīn gēpòle shǒuzhǐ.", "meaningVi": "Anh ấy vô ý cắt phải ngón tay."}],
    "hsk6_0442": [{"chinese": "孩子们在歌唱祖国。", "pinyin": "Háizimen zài gēchàng zǔguó.", "meaningVi": "Bọn trẻ đang hát ca ngợi tổ quốc."}],
    "hsk6_0443": [{"chinese": "隔壁住着一对老夫妇。", "pinyin": "Gébì zhùzhe yí duì lǎo fūfù.", "meaningVi": "Nhà bên cạnh sống một cặp vợ chồng già."}],
    "hsk6_0444": [{"chinese": "这是一场伟大的革命。", "pinyin": "Zhè shì yì chǎng wěidà de gémìng.", "meaningVi": "Đây là một cuộc cách mạng vĩ đại."}],
    "hsk6_0445": [{"chinese": "每个个体都是独特的。", "pinyin": "Měi gè gètǐ dōu shì dútè de.", "meaningVi": "Mỗi cá thể đều là độc đáo."}],
    "hsk6_0446": [{"chinese": "政府给予受灾群众物资援助。", "pinyin": "Zhèngfǔ jǐyǔ shòuzāi qúnzhòng wùzī yuánzhù.", "meaningVi": "Chính phủ trao cho người dân vùng bị thiên tai sự viện trợ vật chất."}],
    "hsk6_0447": [{"chinese": "孩子站在妈妈跟前。", "pinyin": "Háizi zhàn zài māma gēnqián.", "meaningVi": "Đứa trẻ đứng trước mặt mẹ."}],
    "hsk6_0448": [{"chinese": "他一直跟随师傅学习。", "pinyin": "Tā yìzhí gēnsuí shīfu xuéxí.", "meaningVi": "Anh ấy luôn theo học người thầy."}],
    "hsk6_0449": [{"chinese": "警方一直在跟踪嫌疑人。", "pinyin": "Jǐngfāng yìzhí zài gēnzōng xiányírén.", "meaningVi": "Cảnh sát vẫn đang theo dõi nghi phạm."}],
    "hsk6_0450": [{"chinese": "这只猫是公的。", "pinyin": "Zhè zhī māo shì gōng de.", "meaningVi": "Con mèo này là con đực."}],
    "hsk6_0451": [{"chinese": "故宫是著名的旅游景点。", "pinyin": "Gùgōng shì zhùmíng de lǚyóu jǐngdiǎn.", "meaningVi": "Cố Cung là điểm du lịch nổi tiếng."}],
    "hsk6_0452": [{"chinese": "他是一名公安人员。", "pinyin": "Tā shì yì míng gōng'ān rényuán.", "meaningVi": "Anh ấy là một nhân viên công an."}],
    "hsk6_0453": [{"chinese": "工地上很多工人正在施工。", "pinyin": "Gōngdì shàng hěn duō gōngrén zhèngzài shīgōng.", "meaningVi": "Rất nhiều công nhân đang thi công tại công trường."}],
    "hsk6_0454": [{"chinese": "学好一门外语要花不少工夫。", "pinyin": "Xuéhǎo yì mén wàiyǔ yào huā bù shǎo gōngfu.", "meaningVi": "Học tốt một ngoại ngữ phải bỏ ra không ít công sức."}],
    "hsk6_0455": [{"chinese": "学校发布了一则公告。", "pinyin": "Xuéxiào fābùle yì zé gōnggào.", "meaningVi": "Nhà trường đã ban hành một thông báo."}],
    "hsk6_0456": [{"chinese": "市场供给充足。", "pinyin": "Shìchǎng gōngjǐ chōngzú.", "meaningVi": "Nguồn cung trên thị trường đầy đủ."}],
    "hsk6_0457": [{"chinese": "他遭到了网络攻击。", "pinyin": "Tā zāodàole wǎngluò gōngjī.", "meaningVi": "Anh ấy đã bị tấn công trên mạng."}],
    "hsk6_0458": [{"chinese": "这项调查结果将公开发布。", "pinyin": "Zhè xiàng diàochá jiéguǒ jiāng gōngkāi fābù.", "meaningVi": "Kết quả điều tra này sẽ được công bố công khai."}],
    "hsk6_0459": [{"chinese": "每个公民都要遵守法律。", "pinyin": "Měi gè gōngmín dōu yào zūnshǒu fǎlǜ.", "meaningVi": "Mỗi công dân đều phải tuân thủ pháp luật."}],
    "hsk6_0460": [{"chinese": "他是公认的技术专家。", "pinyin": "Tā shì gōngrèn de jìshù zhuānjiā.", "meaningVi": "Anh ấy là chuyên gia kỹ thuật được công nhận."}],
    "hsk6_0461": [{"chinese": "这种药有很好的功效。", "pinyin": "Zhè zhǒng yào yǒu hěn hǎo de gōngxiào.", "meaningVi": "Loại thuốc này có công hiệu rất tốt."}],
    "hsk6_0462": [{"chinese": "生产过程分为好几道工序。", "pinyin": "Shēngchǎn guòchéng fēnwéi hǎo jǐ dào gōngxù.", "meaningVi": "Quá trình sản xuất được chia thành nhiều công đoạn."}],
    "hsk6_0463": [{"chinese": "他热衷于公益事业。", "pinyin": "Tā rèzhōng yú gōngyì shìyè.", "meaningVi": "Anh ấy nhiệt tâm với sự nghiệp công ích."}],
    "hsk6_0464": [{"chinese": "商店保证蔬菜供应。", "pinyin": "Shāngdiàn bǎozhèng shūcài gōngyìng.", "meaningVi": "Cửa hàng đảm bảo nguồn cung cấp rau."}],
    "hsk6_0465": [{"chinese": "这座建筑建于公元前。", "pinyin": "Zhè zuò jiànzhù jiàn yú gōngyuán qián.", "meaningVi": "Công trình này được xây dựng trước Công nguyên."}],
    "hsk6_0466": [{"chinese": "法官必须公正判案。", "pinyin": "Fǎguān bìxū gōngzhèng pàn'àn.", "meaningVi": "Thẩm phán phải xét xử công chính."}],
    "hsk6_0467": [{"chinese": "这项决定受到了公众的关注。", "pinyin": "Zhè xiàng juédìng shòudàole gōngzhòng de guānzhù.", "meaningVi": "Quyết định này đã nhận được sự quan tâm của công chúng."}],
    "hsk6_0468": [{"chinese": "这是一个关于公主的童话故事。", "pinyin": "Zhè shì yí gè guānyú gōngzhǔ de tónghuà gùshi.", "meaningVi": "Đây là một câu chuyện cổ tích về công chúa."}],
    "hsk6_0469": [{"chinese": "我们要巩固已有的成果。", "pinyin": "Wǒmen yào gǒnggù yǐyǒu de chéngguǒ.", "meaningVi": "Chúng ta phải củng cố những thành quả đã có."}],
    "hsk6_0470": [{"chinese": "这次活动共计花费五万元。", "pinyin": "Zhè cì huódòng gòngjì huāfèi wǔwàn yuán.", "meaningVi": "Hoạt động lần này tổng cộng tiêu tốn năm mươi nghìn đồng."}],
    "hsk6_0471": [{"chinese": "田边有一条水沟。", "pinyin": "Tián biān yǒu yì tiáo shuǐgōu.", "meaningVi": "Bên cạnh ruộng có một con mương."}],
    "hsk6_0472": [{"chinese": "这台机器的构造很复杂。", "pinyin": "Zhè tái jīqì de gòuzào hěn fùzá.", "meaningVi": "Cấu tạo của cái máy này rất phức tạp."}],
    "hsk6_0473": [{"chinese": "他一个人生活，感到很孤独。", "pinyin": "Tā yí gè rén shēnghuó, gǎndào hěn gūdú.", "meaningVi": "Anh ấy sống một mình, cảm thấy rất cô đơn."}],
    "hsk6_0474": [{"chinese": "我姑姑住在国外。", "pinyin": "Wǒ gūgu zhù zài guówài.", "meaningVi": "Cô của tôi sống ở nước ngoài."}],
    "hsk6_0475": [{"chinese": "这栋建筑是古典风格的。", "pinyin": "Zhè dòng jiànzhù shì gǔdiǎn fēnggé de.", "meaningVi": "Tòa nhà này mang phong cách cổ điển."}],
    "hsk6_0476": [{"chinese": "这座城市有很多历史古迹。", "pinyin": "Zhè zuò chéngshì yǒu hěn duō lìshǐ gǔjì.", "meaningVi": "Thành phố này có rất nhiều di tích lịch sử."}],
    "hsk6_0477": [{"chinese": "他最近在研究股票。", "pinyin": "Tā zuìjìn zài yánjiū gǔpiào.", "meaningVi": "Gần đây anh ấy đang nghiên cứu cổ phiếu."}],
    "hsk6_0478": [{"chinese": "古人的智慧值得我们学习。", "pinyin": "Gǔrén de zhìhuì zhídé wǒmen xuéxí.", "meaningVi": "Trí tuệ của người xưa đáng để chúng ta học hỏi."}],
    "hsk6_0479": [{"chinese": "今天股市大涨。", "pinyin": "Jīntiān gǔshì dà zhǎng.", "meaningVi": "Hôm nay thị trường chứng khoán tăng mạnh."}],
    "hsk6_0480": [{"chinese": "小狗在啃骨头。", "pinyin": "Xiǎogǒu zài kěn gǔtou.", "meaningVi": "Chú chó con đang gặm xương."}],
    "hsk6_0481": [{"chinese": "他的话鼓舞了大家的士气。", "pinyin": "Tā de huà gǔwǔle dàjiā de shìqì.", "meaningVi": "Lời nói của anh ấy đã cổ vũ tinh thần của mọi người."}],
    "hsk6_0482": [{"chinese": "他只顾自己，不管别人。", "pinyin": "Tā zhǐ gù zìjǐ, bùguǎn biéren.", "meaningVi": "Anh ấy chỉ lo cho bản thân, không quan tâm đến người khác."}],
    "hsk6_0483": [{"chinese": "冰是水的固体状态。", "pinyin": "Bīng shì shuǐ de gùtǐ zhuàngtài.", "meaningVi": "Băng là trạng thái rắn của nước."}],
    "hsk6_0484": [{"chinese": "他是公司的法律顾问。", "pinyin": "Tā shì gōngsī de fǎlǜ gùwèn.", "meaningVi": "Anh ấy là cố vấn pháp lý của công ty."}],
    "hsk6_0485": [{"chinese": "电梯出现了故障。", "pinyin": "Diàntī chūxiànle gùzhàng.", "meaningVi": "Thang máy đã xảy ra sự cố."}],
    "hsk6_0486": [{"chinese": "前面路口往左拐。", "pinyin": "Qiánmiàn lùkǒu wǎng zuǒ guǎi.", "meaningVi": "Ngã tư phía trước rẽ trái."}],
    "hsk6_0487": [{"chinese": "开车拐弯时要减速。", "pinyin": "Kāichē guǎiwān shí yào jiǎnsù.", "meaningVi": "Khi lái xe rẽ cua phải giảm tốc độ."}],
    "hsk6_0488": [{"chinese": "他从小立志要当官。", "pinyin": "Tā cóngxiǎo lìzhì yào dāngguān.", "meaningVi": "Anh ấy từ nhỏ đã lập chí muốn làm quan."}],
    "hsk6_0489": [{"chinese": "社会应该多关爱老人。", "pinyin": "Shèhuì yīnggāi duō guān'ài lǎorén.", "meaningVi": "Xã hội nên quan tâm yêu thương người già nhiều hơn."}],
    "hsk6_0490": [{"chinese": "请以官方消息为准。", "pinyin": "Qǐng yǐ guānfāng xiāoxi wéizhǔn.", "meaningVi": "Xin lấy thông tin chính thức làm chuẩn."}],
    "hsk6_0491": [{"chinese": "很多游客来这里观光。", "pinyin": "Hěn duō yóukè lái zhèlǐ guānguāng.", "meaningVi": "Rất nhiều du khách đến đây tham quan."}],
    "hsk6_0492": [{"chinese": "公司很关怀员工的生活。", "pinyin": "Gōngsī hěn guānhuái yuángōng de shēnghuó.", "meaningVi": "Công ty rất quan tâm chăm sóc đến cuộc sống của nhân viên."}],
    "hsk6_0493": [{"chinese": "这两件事没有直接关联。", "pinyin": "Zhè liǎng jiàn shì méiyǒu zhíjiē guānlián.", "meaningVi": "Hai việc này không có liên quan trực tiếp."}],
    "hsk6_0494": [{"chinese": "大家一起观赏了这场表演。", "pinyin": "Dàjiā yìqǐ guānshǎngle zhè chǎng biǎoyǎn.", "meaningVi": "Mọi người cùng nhau thưởng thức buổi biểu diễn này."}],
    "hsk6_0495": [{"chinese": "一位政府官员出席了会议。", "pinyin": "Yí wèi zhèngfǔ guānyuán chūxíle huìyì.", "meaningVi": "Một quan chức chính phủ đã tham dự cuộc họp."}],
    "hsk6_0496": [{"chinese": "这根管道漏水了。", "pinyin": "Zhè gēn guǎndào lòushuǐ le.", "meaningVi": "Đường ống này bị rò rỉ nước."}],
    "hsk6_0497": [{"chinese": "桌上有一罐蜂蜜。", "pinyin": "Zhuō shàng yǒu yí guàn fēngmì.", "meaningVi": "Trên bàn có một lọ mật ong."}],
    "hsk6_0498": [{"chinese": "未来充满广阔的发展空间。", "pinyin": "Wèilái chōngmǎn guǎngkuò de fāzhǎn kōngjiān.", "meaningVi": "Tương lai tràn đầy không gian phát triển rộng lớn."}],
    "hsk6_0499": [{"chinese": "这件事最终应该归谁管？", "pinyin": "Zhè jiàn shì zuìzhōng yīnggāi guī shéi guǎn?", "meaningVi": "Việc này cuối cùng nên thuộc trách nhiệm của ai quản lý?"}],
    "hsk6_0500": [{"chinese": "请按照规范操作。", "pinyin": "Qǐng ànzhào guīfàn cāozuò.", "meaningVi": "Xin thao tác theo quy phạm."}],
    "hsk6_0501": [{"chinese": "政府正在规划新的交通线路。", "pinyin": "Zhèngfǔ zhèngzài guīhuà xīn de jiāotōng xiànlù.", "meaningVi": "Chính phủ đang quy hoạch tuyến giao thông mới."}],
    "hsk6_0502": [{"chinese": "请按时归还借的书。", "pinyin": "Qǐng ànshí guīhuán jiè de shū.", "meaningVi": "Xin trả lại sách đã mượn đúng hạn."}],
    "hsk6_0503": [{"chinese": "做事要守规矩。", "pinyin": "Zuòshì yào shǒu guīju.", "meaningVi": "Làm việc phải tuân thủ quy tắc."}],
    "hsk6_0504": [{"chinese": "火车沿着轨道行驶。", "pinyin": "Huǒchē yánzhe guǐdào xíngshǐ.", "meaningVi": "Tàu hỏa chạy dọc theo đường ray."}],
    "hsk6_0505": [{"chinese": "他跪在地上求她原谅。", "pinyin": "Tā guì zài dìshang qiú tā yuánliàng.", "meaningVi": "Anh ấy quỳ xuống đất cầu xin cô ấy tha thứ."}],
    "hsk6_0506": [{"chinese": "请把贵重物品存放好。", "pinyin": "Qǐng bǎ guìzhòng wùpǐn cúnfàng hǎo.", "meaningVi": "Xin cất giữ tốt vật phẩm quý giá."}],
    "hsk6_0507": [{"chinese": "他手里拿着一根木棍。", "pinyin": "Tā shǒu lǐ názhe yì gēn mùgùn.", "meaningVi": "Trong tay anh ấy cầm một cây gậy gỗ."}],
    "hsk6_0508": [{"chinese": "这件青铜器被视为国宝。", "pinyin": "Zhè jiàn qīngtóngqì bèi shìwéi guóbǎo.", "meaningVi": "Món đồ đồng này được coi là quốc bảo."}],
    "hsk6_0509": [{"chinese": "这是一款国产手机。", "pinyin": "Zhè shì yì kuǎn guóchǎn shǒujī.", "meaningVi": "Đây là một mẫu điện thoại sản xuất trong nước."}],
    "hsk6_0510": [{"chinese": "请全体起立，奏国歌。", "pinyin": "Qǐng quántǐ qǐlì, zòu guógē.", "meaningVi": "Xin tất cả đứng dậy, cử hành quốc ca."}],
    "hsk6_0511": [{"chinese": "每周一学校都会升国旗。", "pinyin": "Měi zhōuyī xuéxiào dōu huì shēng guóqí.", "meaningVi": "Mỗi thứ hai nhà trường đều làm lễ chào cờ."}],
    "hsk6_0512": [{"chinese": "政策制定要结合本国国情。", "pinyin": "Zhèngcè zhìdìng yào jiéhé běn guó guóqíng.", "meaningVi": "Xây dựng chính sách phải kết hợp với tình hình đất nước."}],
    "hsk6_0513": [{"chinese": "古代国王住在皇宫里。", "pinyin": "Gǔdài guówáng zhù zài huánggōng lǐ.", "meaningVi": "Vua thời cổ đại sống trong hoàng cung."}],
    "hsk6_0514": [{"chinese": "这是一个过渡阶段。", "pinyin": "Zhè shì yí gè guòdù jiēduàn.", "meaningVi": "Đây là một giai đoạn quá độ."}],
    "hsk6_0515": [{"chinese": "雨过后空气特别清新。", "pinyin": "Yǔ guòhòu kōngqì tèbié qīngxīn.", "meaningVi": "Sau cơn mưa không khí đặc biệt trong lành."}],
    "hsk6_0516": [{"chinese": "这种想法已经过时了。", "pinyin": "Zhè zhǒng xiǎngfǎ yǐjīng guòshí le.", "meaningVi": "Cách nghĩ này đã lỗi thời rồi."}],
    "hsk6_0517": [{"chinese": "这个品牌在海内外都很有名。", "pinyin": "Zhège páizi zài hǎi nèiwài dōu hěn yǒumíng.", "meaningVi": "Thương hiệu này nổi tiếng cả trong và ngoài nước."}],
    "hsk6_0518": [{"chinese": "他们沿着海岸散步。", "pinyin": "Tāmen yánzhe hǎi'àn sànbù.", "meaningVi": "Họ đi dạo dọc theo bờ biển."}],
    "hsk6_0519": [{"chinese": "这座山海拔三千米。", "pinyin": "Zhè zuò shān hǎibá sānqiān mǐ.", "meaningVi": "Ngọn núi này có độ cao ba nghìn mét so với mực nước biển."}],
    "hsk6_0520": [{"chinese": "海面上飘着几只船。", "pinyin": "Hǎimiàn shàng piāozhe jǐ zhī chuán.", "meaningVi": "Trên mặt biển có vài chiếc thuyền trôi."}],
    "hsk6_0521": [{"chinese": "这片海域盛产鱼类。", "pinyin": "Zhè piàn hǎiyù shèngchǎn yúlèi.", "meaningVi": "Vùng biển này sản xuất nhiều loại cá."}],
    "hsk6_0522": [{"chinese": "吸烟害人害己。", "pinyin": "Xīyān hài rén hài jǐ.", "meaningVi": "Hút thuốc hại người hại mình."}],
    "hsk6_0523": [{"chinese": "寒冬腊月，天气非常冷。", "pinyin": "Hándōng làyuè, tiānqì fēicháng lěng.", "meaningVi": "Mùa đông rét buốt, thời tiết rất lạnh."}],
    "hsk6_0524": [{"chinese": "这句话的含义很深。", "pinyin": "Zhè jù huà de hányì hěn shēn.", "meaningVi": "Hàm nghĩa của câu nói này rất sâu sắc."}],
    "hsk6_0525": [{"chinese": "这是一种罕见的疾病。", "pinyin": "Zhè shì yì zhǒng hǎnjiàn de jíbìng.", "meaningVi": "Đây là một loại bệnh hiếm gặp."}],
    "hsk6_0526": [{"chinese": "今年南方发生了严重旱灾。", "pinyin": "Jīnnián nánfāng fāshēngle yánzhòng hànzāi.", "meaningVi": "Năm nay miền Nam đã xảy ra hạn hán nghiêm trọng."}],
    "hsk6_0527": [{"chinese": "他在一家航空公司工作。", "pinyin": "Tā zài yì jiā hángkōng gōngsī gōngzuò.", "meaningVi": "Anh ấy làm việc tại một công ty hàng không."}],
    "hsk6_0528": [{"chinese": "他毫不犹豫地答应了。", "pinyin": "Tā háo bù yóuyù de dāying le.", "meaningVi": "Anh ấy đồng ý mà không hề do dự."}],
    "hsk6_0529": [{"chinese": "他毫无办法，只能等待。", "pinyin": "Tā háo wú bànfǎ, zhǐ néng děngdài.", "meaningVi": "Anh ấy hoàn toàn không có cách nào, chỉ có thể chờ đợi."}],
    "hsk6_0530": [{"chinese": "这根针的直径是两毫米。", "pinyin": "Zhè gēn zhēn de zhíjìng shì liǎng háomǐ.", "meaningVi": "Đường kính của cây kim này là hai milimét."}],
    "hsk6_0531": [{"chinese": "这瓶药水一次喝十毫升。", "pinyin": "Zhè píng yàoshuǐ yí cì hē shí háoshēng.", "meaningVi": "Chai thuốc nước này mỗi lần uống mười mililit."}],
    "hsk6_0532": [{"chinese": "这个消息让他好不高兴。", "pinyin": "Zhège xiāoxi ràng tā hǎobù gāoxìng.", "meaningVi": "Tin này khiến anh ấy vui biết bao."}],
    "hsk6_0533": [{"chinese": "她对他很有好感。", "pinyin": "Tā duì tā hěn yǒu hǎogǎn.", "meaningVi": "Cô ấy có thiện cảm với anh ấy."}],
    "hsk6_0534": [{"chinese": "好容易才买到这张票。", "pinyin": "Hǎoróngyì cái mǎidào zhè zhāng piào.", "meaningVi": "Khó khăn lắm mới mua được tấm vé này."}],
    "hsk6_0535": [{"chinese": "当地人非常好客。", "pinyin": "Dāngdì rén fēicháng hàokè.", "meaningVi": "Người dân địa phương rất hiếu khách."}],
    "hsk6_0536": [{"chinese": "这个孩子勤奋好学。", "pinyin": "Zhège háizi qínfèn hàoxué.", "meaningVi": "Đứa trẻ này chăm chỉ ham học."}],
    "hsk6_0537": [{"chinese": "政府号召大家节约用水。", "pinyin": "Zhèngfǔ hàozhào dàjiā jiéyuē yòngshuǐ.", "meaningVi": "Chính phủ kêu gọi mọi người tiết kiệm nước."}],
    "hsk6_0538": [{"chinese": "两家公司决定合并。", "pinyin": "Liǎng jiā gōngsī juédìng hébìng.", "meaningVi": "Hai công ty quyết định sáp nhập."}],
    "hsk6_0539": [{"chinese": "这种材料是人工合成的。", "pinyin": "Zhè zhǒng cáiliào shì réngōng héchéng de.", "meaningVi": "Loại vật liệu này được tổng hợp nhân tạo."}],
    "hsk6_0540": [{"chinese": "我们渴望世界和平。", "pinyin": "Wǒmen kěwàng shìjiè hépíng.", "meaningVi": "Chúng ta khao khát hòa bình thế giới."}],
    "hsk6_0541": [{"chinese": "邻里之间要和谐相处。", "pinyin": "Línlǐ zhījiān yào héxié xiāngchǔ.", "meaningVi": "Hàng xóm láng giềng phải sống hòa thuận với nhau."}],
    "hsk6_0542": [{"chinese": "这是问题的核心。", "pinyin": "Zhè shì wèntí de héxīn.", "meaningVi": "Đây là cốt lõi của vấn đề."}],
    "hsk6_0543": [{"chinese": "嘿，你在做什么呢？", "pinyin": "Hēi, nǐ zài zuò shénme ne?", "meaningVi": "Này, bạn đang làm gì vậy?"}],
    "hsk6_0544": [{"chinese": "房间里一片黑暗。", "pinyin": "Fángjiān lǐ yí piàn hēi'àn.", "meaningVi": "Trong phòng tối om."}],
    "hsk6_0545": [{"chinese": "墙上留下了岁月的痕迹。", "pinyin": "Qiáng shàng liúxiàle suìyuè de hénjì.", "meaningVi": "Trên tường để lại dấu vết của thời gian."}],
    "hsk6_0546": [{"chinese": "他下狠心离开了这里。", "pinyin": "Tā xià hěnxīn líkāile zhèlǐ.", "meaningVi": "Anh ấy đã nhẫn tâm rời khỏi nơi đây."}],
    "hsk6_0547": [{"chinese": "她恨透了这种虚伪的行为。", "pinyin": "Tā hèntòule zhè zhǒng xūwěi de xíngwéi.", "meaningVi": "Cô ấy vô cùng căm ghét hành vi giả dối này."}],
    "hsk6_0548": [{"chinese": "请把这根木头横放。", "pinyin": "Qǐng bǎ zhè gēn mùtou héng fàng.", "meaningVi": "Xin đặt cây gỗ này nằm ngang."}],
    "hsk6_0549": [{"chinese": "成绩不是衡量能力的唯一标准。", "pinyin": "Chéngjì bú shì héngliáng nénglì de wéiyī biāozhǔn.", "meaningVi": "Thành tích không phải là tiêu chuẩn duy nhất để đánh giá năng lực."}],
    "hsk6_0550": [{"chinese": "他有一个宏大的理想。", "pinyin": "Tā yǒu yí gè hóngdà de lǐxiǎng.", "meaningVi": "Anh ấy có một lý tưởng vĩ đại."}],
    "hsk6_0551": [{"chinese": "洪水冲毁了这座桥。", "pinyin": "Hóngshuǐ chōnghuǐle zhè zuò qiáo.", "meaningVi": "Lũ lụt đã cuốn trôi cây cầu này."}],
    "hsk6_0552": [{"chinese": "我们要为后代留下一个美好的环境。", "pinyin": "Wǒmen yào wèi hòudài liúxià yí gè měihǎo de huánjìng.", "meaningVi": "Chúng ta phải để lại một môi trường tốt đẹp cho thế hệ sau."}],
    "hsk6_0553": [{"chinese": "这部电影的后期制作花了很长时间。", "pinyin": "Zhè bù diànyǐng de hòuqī zhìzuò huāle hěn cháng shíjiān.", "meaningVi": "Công đoạn hậu kỳ của bộ phim này đã mất rất nhiều thời gian."}],
    "hsk6_0554": [{"chinese": "他的贡献被后人铭记。", "pinyin": "Tā de gòngxiàn bèi hòurén míngjì.", "meaningVi": "Cống hiến của ông ấy được người đời sau ghi nhớ."}],
    "hsk6_0555": [{"chinese": "遇到危险要及时后退。", "pinyin": "Yùdào wēixiǎn yào jíshí hòutuì.", "meaningVi": "Gặp nguy hiểm phải kịp thời lùi lại."}],
    "hsk6_0556": [{"chinese": "前者比后者更受欢迎。", "pinyin": "Qiánzhě bǐ hòuzhě gèng shòu huānyíng.", "meaningVi": "Cái trước được ưa chuộng hơn cái sau."}],
    "hsk6_0557": [{"chinese": "我们不能忽略这个细节。", "pinyin": "Wǒmen bù néng hūlüè zhège xìjié.", "meaningVi": "Chúng ta không thể bỏ qua chi tiết này."}],
    "hsk6_0558": [{"chinese": "请把水壶烧开。", "pinyin": "Qǐng bǎ shuǐhú shāokāi.", "meaningVi": "Xin đun sôi ấm nước."}],
    "hsk6_0559": [{"chinese": "他留着一把胡子。", "pinyin": "Tā liúzhe yì bǎ húzi.", "meaningVi": "Anh ấy để một bộ râu."}],
    "hsk6_0560": [{"chinese": "这个小区一共有五百户人家。", "pinyin": "Zhège xiǎoqū yígòng yǒu wǔbǎi hù rénjiā.", "meaningVi": "Khu dân cư này tổng cộng có năm trăm hộ gia đình."}],
    "hsk6_0561": [{"chinese": "邻居之间应该互助。", "pinyin": "Línjū zhījiān yīnggāi hùzhù.", "meaningVi": "Hàng xóm nên giúp đỡ lẫn nhau."}],
    "hsk6_0562": [{"chinese": "花园里开满了花朵。", "pinyin": "Huāyuán lǐ kāimǎnle huāduǒ.", "meaningVi": "Trong vườn hoa nở đầy hoa."}],
    "hsk6_0563": [{"chinese": "他喜欢吃花生。", "pinyin": "Tā xǐhuan chī huāshēng.", "meaningVi": "Anh ấy thích ăn đậu phộng."}],
    "hsk6_0564": [{"chinese": "冬天他喜欢滑冰。", "pinyin": "Dōngtiān tā xǐhuan huábīng.", "meaningVi": "Mùa đông anh ấy thích trượt băng."}],
    "hsk6_0565": [{"chinese": "滑板车在人行道上滑行。", "pinyin": "Huábǎnchē zài rénxíngdào shàng huáxíng.", "meaningVi": "Xe trượt scooter lướt đi trên vỉa hè."}],
    "hsk6_0566": [{"chinese": "他们去滑雪场滑雪。", "pinyin": "Tāmen qù huáxuěchǎng huáxuě.", "meaningVi": "Họ đi đến khu trượt tuyết để trượt tuyết."}],
    "hsk6_0568": [{"chinese": "请把班级划分成几个小组。", "pinyin": "Qǐng bǎ bānjí huàfēn chéng jǐ gè xiǎozǔ.", "meaningVi": "Xin chia lớp học thành mấy nhóm nhỏ."}],
    "hsk6_0569": [{"chinese": "科学家发现了一块恐龙化石。", "pinyin": "Kēxuéjiā fāxiànle yí kuài kǒnglóng huàshí.", "meaningVi": "Nhà khoa học đã phát hiện một mảnh hóa thạch khủng long."}],
    "hsk6_0570": [{"chinese": "请对着话筒讲话。", "pinyin": "Qǐng duìzhe huàtǒng jiǎnghuà.", "meaningVi": "Xin nói vào micro."}],
    "hsk6_0571": [{"chinese": "她每天都要化妆。", "pinyin": "Tā měitiān dōu yào huàzhuāng.", "meaningVi": "Cô ấy mỗi ngày đều phải trang điểm."}],
    "hsk6_0572": [{"chinese": "她怀里抱着一个孩子。", "pinyin": "Tā huái lǐ bàozhe yí gè háizi.", "meaningVi": "Trong lòng cô ấy bế một đứa trẻ."}],
    "hsk6_0573": [{"chinese": "他常常怀念童年的时光。", "pinyin": "Tā chángcháng huáiniàn tóngnián de shíguāng.", "meaningVi": "Anh ấy thường nhớ nhung thời thơ ấu."}],
    "hsk6_0574": [{"chinese": "她怀孕五个月了。", "pinyin": "Tā huáiyùn wǔ gè yuè le.", "meaningVi": "Cô ấy mang thai được năm tháng rồi."}],
    "hsk6_0575": [{"chinese": "节日里到处充满欢乐的气氛。", "pinyin": "Jiérì lǐ dàochù chōngmǎn huānlè de qìfēn.", "meaningVi": "Trong ngày lễ khắp nơi tràn đầy bầu không khí vui vẻ."}],
    "hsk6_0576": [{"chinese": "这是一枚金属环。", "pinyin": "Zhè shì yì méi jīnshǔ huán.", "meaningVi": "Đây là một chiếc vòng kim loại."}],
    "hsk6_0577": [{"chinese": "请把现场还原一下。", "pinyin": "Qǐng bǎ xiànchǎng huányuán yíxià.", "meaningVi": "Xin khôi phục lại hiện trường."}],
    "hsk6_0578": [{"chinese": "他患有严重的心脏病。", "pinyin": "Tā huànyǒu yánzhòng de xīnzàngbìng.", "meaningVi": "Anh ấy mắc bệnh tim nghiêm trọng."}],
    "hsk6_0579": [{"chinese": "别整天沉浸在幻想中。", "pinyin": "Bié zhěngtiān chénjìn zài huànxiǎng zhōng.", "meaningVi": "Đừng suốt ngày đắm chìm trong ảo tưởng."}],
    "hsk6_0580": [{"chinese": "医院里住着很多患者。", "pinyin": "Yīyuàn lǐ zhùzhe hěn duō huànzhě.", "meaningVi": "Trong bệnh viện có rất nhiều bệnh nhân đang nằm điều trị."}],
    "hsk6_0581": [{"chinese": "树叶变黄了。", "pinyin": "Shùyè biàn huáng le.", "meaningVi": "Lá cây đã chuyển sang màu vàng."}],
    "hsk6_0582": [{"chinese": "秦始皇是中国第一位皇帝。", "pinyin": "Qínshǐhuáng shì Zhōngguó dì-yī wèi huángdì.", "meaningVi": "Tần Thủy Hoàng là vị hoàng đế đầu tiên của Trung Quốc."}],
    "hsk6_0583": [{"chinese": "桌子上有一层灰尘。", "pinyin": "Zhuōzi shàng yǒu yì céng huīchén.", "meaningVi": "Trên bàn có một lớp bụi."}],
    "hsk6_0584": [{"chinese": "一次失败不要灰心。", "pinyin": "Yí cì shībài búyào huīxīn.", "meaningVi": "Một lần thất bại đừng nản lòng."}],
    "hsk6_0585": [{"chinese": "他希望自己的付出能得到回报。", "pinyin": "Tā xīwàng zìjǐ de fùchū néng dédào huíbào.", "meaningVi": "Anh ấy hy vọng sự cống hiến của mình sẽ nhận được đền đáp."}],
    "hsk6_0586": [{"chinese": "让我们回顾一下过去这一年。", "pinyin": "Ràng wǒmen huígù yíxià guòqù zhè yì nián.", "meaningVi": "Hãy cùng chúng ta nhìn lại năm qua."}],
    "hsk6_0587": [{"chinese": "他回头看了一眼。", "pinyin": "Tā huítóu kànle yì yǎn.", "meaningVi": "Anh ấy quay đầu nhìn lại một cái."}],
    "hsk6_0588": [{"chinese": "这是一笔跨国汇款。", "pinyin": "Zhè shì yì bǐ kuàguó huìkuǎn.", "meaningVi": "Đây là một khoản chuyển tiền quốc tế."}],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ids, universe, tiers = get_next_batch_ids(BATCH_SIZE)

    if len(ids) != BATCH_SIZE:
        print(f"FAIL: queue produced {len(ids)} records, expected {BATCH_SIZE}", file=sys.stderr)
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
            "qaStatus": "needs_review" if rid in NEEDS_REVIEW_IDS else "pending",
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
