"""P5.10.3 (continued) -- Batch 022 (continues immediately after
examples_batch_021.json; entirely within HSK5). First 300-record
batch in this phase (batches 002-020 were 100 each, batch 021 was 200).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Dense productive-root families in this batch kept structurally
distinct (no shared template): 打扮/打包/打断/打破/打听 (dǎ+X, five
members); 大胆/大多/大会/大妈/大米/大脑/大批/大厦/大事/大象/大型/
大爷/大于/大众 (dà+X, fourteen members); 当地/当年/当中/当成/当作
(dāng/dàng -- 当 is polyphonic, dāng in the first three, dàng in the
last two); 导致/到达/道理/到期 (dǎo/dào); 电动/电器/电商/电视台/
电子版 (diàn+X, five members); 分布/分类/分离/分配/分手/分享 (fēn+X,
six members); 改进/改善/改天/改正 (gǎi+X, four members); 高大/高档/
高级/高科技/高效 (gāo+X, five members, distinct from the already-
published 高价/高考/高速/高温/高于, batch 011); 公布/工程/工程师/
工具/功能/公平/公务员/工业/工艺/公寓 (gōng+X, ten members across
three characters 工/公/功, all gōng); 过度/过分/过期/过于 (guò+X,
four members); 含/含量/含有 (hán, root+derivatives); 好评/好运/
好转/好奇 (hǎo+X, four members); 合/合法/合理/合同/合作 (hé, five
members, distinct from the same-pinyin 盒饭); 打散字族 此后/此前/
此时 (cǐ+X); 从不/从而/从前/从事 (cóng+X); 促进/促使/促销 (cù+X).

Same-pinyin-different-character pairs disambiguated via natural
compound (none flagged by the mechanical tier system): 窗台 (chuāng)
vs 床单 (chuáng); 独特/独自 (dú) vs 读音 (dú, same pinyin+tone);
对待/对手/对象 (duì) vs 队伍 (duì, same pinyin+tone); 合/合法/合理/
合同/合作 (hé) vs 盒饭 (hé, same pinyin+tone); 伙/伙伴 (huǒ) vs
火锅 (huǒ, same pinyin+tone); 话费/话题 (huà) vs 画面 (huà, same
pinyin+tone); 调研 (diào, "to survey") kept distinct from the
already-published 调整/调皮 (tiáo -- same character 调, different
reading of this polyphonic character); 行业 (háng, "industry") kept
distinct from the already-published xíng-cluster (行程/行人/行驶/
行为/行走, batch 020/021 -- same character 行, different reading).

A dense jí(2nd tone) cluster spans seven characters in this single
batch: 及 (及格 too) / 疾 (疾病) / 集 (集合/集体) / 即 (即将) / 急
(急忙/急需) / 极 (极其) -- each anchored to a distinct real-world
referent (a capability comparison, illness detection, a meeting
point, an upcoming semester, running out of a room, urgent relief
supplies, importance) to keep the cluster unambiguous.
A dense jì(4th tone) cluster: 季度/纪录/纪录片/技能/纪念日/计算/
计算机/记载 (eight members across four characters 季/纪/技/计/记).

Self-caught near-duplicate/near-template revisions made during
drafting (before this batch was finalized):
  - 达成 (dáchéng): first draft "双方最终达成了协议。" was a near-
    template match against 最终's own already-published example
    (batch 017, hsk4_988: "他们最终达成了协议。", differing by only
    the subject) -- rewritten to "经过多次谈判，双方达成了共识。".
  - 到达 (dàodá): first draft "我们终于到达了目的地。" would have
    been an EXACT duplicate of 目的地's own already-published example
    (batch 013, hsk4_519: "我们终于到达了目的地。") -- rewritten to
    "飞机延误了，我们很晚才到达。".
  - 短处 (duǎnchù): first draft "每个人都有自己的短处。" would have
    recreated the "每个人都有自己的X" template already flagged and
    avoided for 长处 (batch 021, which itself was rewritten away from
    this exact template used by 特点, batch 015) -- rewritten to
    "他很谦虚，从不掩饰自己的短处。".
  - 好转 (hǎozhuǎn): first draft "他的病情逐渐好转。" would have been
    an EXACT duplicate of 病情's own already-published example (batch
    017, hsk5_069: "他的病情逐渐好转。") -- rewritten to "最近经济
    形势有所好转。".
  All re-verified against the full pilot+002-021 corpus with zero
  remaining exact duplicates and zero near-template flags (see
  validation report).

Validator-caught fix (found by validate_examples_batch_p103.py's
no_duplicate_sentences_across_pilot_and_batches check): 红 (hóng)'s
first draft "她的脸红了。" was an EXACT duplicate of 脸's own already-
published example (batch 007, hsk3_250: "她的脸红了。") -- rewritten
to "这面墙被漆成了红色。".

Automated near-template pass (character-bigram Jaccard similarity
against the full pilot+002-021 corpus) caught seven further near-
synonym/near-duplicate matches, all fixed after the manual drafting
pass:
  - 措施 (cuòshī): "政府采取了新的措施。" duplicated 采取's own example
    (batch 017, hsk5_086: "政府采取了新措施。") almost verbatim --
    rewritten to "这些措施已经取得了明显效果。".
  - 担任 (dānrèn): "他担任这个项目的负责人。" duplicated 负责人's own
    example (batch 010, hsk4_216: "他是这个项目的负责人。") --
    rewritten to "她担任公司的财务总监。".
  - 动人 (dòngrén): "这是一个动人的故事。" duplicated the near-
    synonym 感人's own example (batch 016, hsk4_230: "这是一个很感人
    的故事。") -- rewritten to "她的歌声十分动人。".
  - 队伍 (duìwu): "队伍排得很长。" was a substring match of 安检's own
    example (batch 002, hsk4_004: "安检的队伍排得很长。") -- rewritten
    to "他带领队伍完成了这次任务。".
  - 恭喜 (gōngxǐ): "恭喜你考上了大学。" duplicated the near-synonym
    祝贺's own example (batch 017, hsk4_966: "祝贺你考上了大学。") --
    rewritten to "恭喜你们喜结良缘。".
  - 冠军 (guànjūn): "他获得了这次比赛的冠军。" duplicated 大赛's own
    example (batch 009, hsk4_127: "他获得了这次大赛的冠军。") --
    rewritten to "上届冠军今年再次夺冠。".
  - 贵姓 (guìxìng): "请问您贵姓？" was a substring match of an existing
    HSK1-lineage example ("您好，请问您贵姓？") -- rewritten to "初次
    见面不知贵姓大名？".
  - 从不 (cóngbù): "他从不迟到。" duplicated the near-synonym 从来's
    own example (batch 009, hsk4_103: "他从来不迟到。") -- rewritten
    to "他从不抱怨工作辛苦。".
  All re-verified with zero remaining exact duplicates and zero
  near-template flags.

Usage:
    python generate_examples_batch_022.py --dry-run
    python generate_examples_batch_022.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 22
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_022.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk5_162": [{"chinese": "请给手机充值。", "pinyin": "Qǐng gěi shǒujī chōngzhí.", "meaningVi": "Xin nạp tiền cho điện thoại."}],
    "hsk5_163": [{"chinese": "睡眠充足对身体好。", "pinyin": "Shuìmián chōngzú duì shēntǐ hǎo.", "meaningVi": "Ngủ đủ giấc tốt cho sức khỏe."}],
    "hsk5_164": [{"chinese": "请不要重复同样的错误。", "pinyin": "Qǐng búyào chóngfù tóngyàng de cuòwù.", "meaningVi": "Xin đừng lặp lại cùng một lỗi."}],
    "hsk5_165": [{"chinese": "树叶上有一只虫子。", "pinyin": "Shùyè shàng yǒu yì zhī chóngzi.", "meaningVi": "Trên lá cây có một con sâu."}],
    "hsk5_166": [{"chinese": "她养了一只宠物狗。", "pinyin": "Tā yǎngle yì zhī chǒngwù gǒu.", "meaningVi": "Cô ấy nuôi một con chó cưng."}],
    "hsk5_167": [{"chinese": "他从口袋里抽出一张纸。", "pinyin": "Tā cóng kǒudai lǐ chōuchū yì zhāng zhǐ.", "meaningVi": "Anh ấy rút một tờ giấy từ trong túi ra."}],
    "hsk5_172": [{"chinese": "这是初级汉语课程。", "pinyin": "Zhè shì chūjí Hànyǔ kèchéng.", "meaningVi": "Đây là khóa học tiếng Hán sơ cấp."}],
    "hsk5_173": [{"chinese": "项目初期遇到了不少困难。", "pinyin": "Xiàngmù chūqī yùdàole bù shǎo kùnnan.", "meaningVi": "Giai đoạn đầu của dự án gặp không ít khó khăn."}],
    "hsk5_174": [{"chinese": "他的表现非常出色。", "pinyin": "Tā de biǎoxiàn fēicháng chūsè.", "meaningVi": "Biểu hiện của anh ấy vô cùng xuất sắc."}],
    "hsk5_175": [{"chinese": "这套房子正在出售。", "pinyin": "Zhè tào fángzi zhèngzài chūshòu.", "meaningVi": "Căn nhà này đang được rao bán."}],
    "hsk5_176": [{"chinese": "他出席了今天的会议。", "pinyin": "Tā chūxíle jīntiān de huìyì.", "meaningVi": "Anh ấy đã tham dự cuộc họp hôm nay."}],
    "hsk5_177": [{"chinese": "这句话出自一位名人。", "pinyin": "Zhè jù huà chūzì yí wèi míngrén.", "meaningVi": "Câu nói này xuất phát từ một người nổi tiếng."}],
    "hsk5_178": [{"chinese": "除夕夜全家人一起吃团圆饭。", "pinyin": "Chúxī yè quánjiā rén yìqǐ chī tuányuánfàn.", "meaningVi": "Đêm giao thừa cả nhà cùng ăn bữa cơm đoàn viên."}],
    "hsk5_180": [{"chinese": "请尽快处理这件事。", "pinyin": "Qǐng jǐnkuài chǔlǐ zhè jiàn shì.", "meaningVi": "Xin xử lý việc này càng sớm càng tốt."}],
    "hsk5_181": [{"chinese": "公司目前处于发展阶段。", "pinyin": "Gōngsī mùqián chǔyú fāzhǎn jiēduàn.", "meaningVi": "Công ty hiện đang ở giai đoạn phát triển."}],
    "hsk5_183": [{"chinese": "这个消息很快就传开了。", "pinyin": "Zhège xiāoxi hěn kuài jiù chuánkāi le.", "meaningVi": "Tin này nhanh chóng được lan truyền."}],
    "hsk5_184": [{"chinese": "病毒通过空气传播。", "pinyin": "Bìngdú tōngguò kōngqì chuánbō.", "meaningVi": "Virus lây truyền qua không khí."}],
    "hsk5_185": [{"chinese": "老师把知识传递给学生。", "pinyin": "Lǎoshī bǎ zhīshi chuándì gěi xuésheng.", "meaningVi": "Giáo viên truyền đạt kiến thức cho học sinh."}],
    "hsk5_188": [{"chinese": "猫喜欢趴在窗台上晒太阳。", "pinyin": "Māo xǐhuan pā zài chuāngtái shàng shài tàiyáng.", "meaningVi": "Mèo thích nằm trên bệ cửa sổ để phơi nắng."}],
    "hsk5_189": [{"chinese": "请换一下床单。", "pinyin": "Qǐng huàn yíxià chuángdān.", "meaningVi": "Xin thay ga trải giường."}],
    "hsk5_191": [{"chinese": "他辞职去创业了。", "pinyin": "Tā cízhí qù chuàngyè le.", "meaningVi": "Anh ấy đã nghỉ việc đi khởi nghiệp."}],
    "hsk5_192": [{"chinese": "我们要勇于创造新事物。", "pinyin": "Wǒmen yào yǒngyú chuàngzào xīn shìwù.", "meaningVi": "Chúng ta phải dũng cảm sáng tạo ra những điều mới."}],
    "hsk5_194": [{"chinese": "他的词汇量很大。", "pinyin": "Tā de cíhuì liàng hěn dà.", "meaningVi": "Vốn từ vựng của anh ấy rất lớn."}],
    "hsk5_196": [{"chinese": "此后他再也没有回来过。", "pinyin": "Cǐhòu tā zài yě méiyǒu huílái guo.", "meaningVi": "Từ đó về sau anh ấy không bao giờ quay lại nữa."}],
    "hsk5_197": [{"chinese": "此前我们从未见过面。", "pinyin": "Cǐqián wǒmen cóng wèi jiànguo miàn.", "meaningVi": "Trước đó chúng tôi chưa từng gặp mặt."}],
    "hsk5_198": [{"chinese": "此时窗外正下着雨。", "pinyin": "Cǐshí chuāngwài zhèng xiàzhe yǔ.", "meaningVi": "Lúc này bên ngoài cửa sổ đang mưa."}],
    "hsk5_200": [{"chinese": "他从不抱怨工作辛苦。", "pinyin": "Tā cóngbù bàoyuàn gōngzuò xīnkǔ.", "meaningVi": "Anh ấy chưa bao giờ than phiền công việc vất vả."}],
    "hsk5_201": [{"chinese": "他努力学习，从而提高了成绩。", "pinyin": "Tā nǔlì xuéxí, cóng'ér tígāole chéngjì.", "meaningVi": "Anh ấy chăm chỉ học tập, nhờ đó mà nâng cao thành tích."}],
    "hsk5_202": [{"chinese": "从前这里是一片农田。", "pinyin": "Cóngqián zhèlǐ shì yí piàn nóngtián.", "meaningVi": "Trước đây nơi này là một cánh đồng."}],
    "hsk5_203": [{"chinese": "他从事教育工作多年。", "pinyin": "Tā cóngshì jiàoyù gōngzuò duō nián.", "meaningVi": "Anh ấy đã làm công tác giáo dục nhiều năm."}],
    "hsk5_204": [{"chinese": "运动促进血液循环。", "pinyin": "Yùndòng cùjìn xuèyè xúnhuán.", "meaningVi": "Vận động thúc đẩy tuần hoàn máu."}],
    "hsk5_205": [{"chinese": "失败促使他更加努力。", "pinyin": "Shībài cùshǐ tā gèngjiā nǔlì.", "meaningVi": "Thất bại thúc đẩy anh ấy nỗ lực hơn."}],
    "hsk5_206": [{"chinese": "商场正在搞促销活动。", "pinyin": "Shāngchǎng zhèngzài gǎo cùxiāo huódòng.", "meaningVi": "Trung tâm thương mại đang tổ chức hoạt động khuyến mãi."}],
    "hsk5_207": [{"chinese": "妈妈催我快点起床。", "pinyin": "Māma cuī wǒ kuài diǎn qǐchuáng.", "meaningVi": "Mẹ giục tôi mau dậy."}],
    "hsk5_208": [{"chinese": "贵重物品请存放在保险柜里。", "pinyin": "Guìzhòng wùpǐn qǐng cúnfàng zài bǎoxiǎnguì lǐ.", "meaningVi": "Vật có giá trị xin cất giữ trong két sắt."}],
    "hsk5_210": [{"chinese": "这个问题一直存在。", "pinyin": "Zhège wèntí yìzhí cúnzài.", "meaningVi": "Vấn đề này luôn tồn tại."}],
    "hsk5_211": [{"chinese": "这些措施已经取得了明显效果。", "pinyin": "Zhèxiē cuòshī yǐjīng qǔdéle míngxiǎn xiàoguǒ.", "meaningVi": "Những biện pháp này đã đạt được hiệu quả rõ rệt."}],
    "hsk5_212": [{"chinese": "经过多次谈判，双方达成了共识。", "pinyin": "Jīngguò duō cì tánpàn, shuāngfāng dáchéngle gòngshí.", "meaningVi": "Qua nhiều lần đàm phán, hai bên đã đạt được sự đồng thuận."}],
    "hsk5_213": [{"chinese": "她打扮得很漂亮。", "pinyin": "Tā dǎban de hěn piàoliang.", "meaningVi": "Cô ấy trang điểm rất đẹp."}],
    "hsk5_214": [{"chinese": "剩下的菜可以打包带走。", "pinyin": "Shèngxià de cài kěyǐ dǎbāo dàizǒu.", "meaningVi": "Món ăn còn thừa có thể gói mang về."}],
    "hsk5_215": [{"chinese": "请不要打断我说话。", "pinyin": "Qǐng búyào dǎduàn wǒ shuōhuà.", "meaningVi": "Xin đừng ngắt lời tôi."}],
    "hsk5_216": [{"chinese": "他打破了世界纪录。", "pinyin": "Tā dǎpòle shìjiè jìlù.", "meaningVi": "Anh ấy đã phá kỷ lục thế giới."}],
    "hsk5_217": [{"chinese": "我想打听一下情况。", "pinyin": "Wǒ xiǎng dǎting yíxià qíngkuàng.", "meaningVi": "Tôi muốn hỏi thăm về tình hình."}],
    "hsk5_218": [{"chinese": "他的想法很大胆。", "pinyin": "Tā de xiǎngfǎ hěn dàdǎn.", "meaningVi": "Ý tưởng của anh ấy rất táo bạo."}],
    "hsk5_219": [{"chinese": "参加的人大多是学生。", "pinyin": "Cānjiā de rén dàduō shì xuésheng.", "meaningVi": "Phần lớn người tham gia là học sinh."}],
    "hsk5_220": [{"chinese": "明天将召开员工大会。", "pinyin": "Míngtiān jiāng zhàokāi yuángōng dàhuì.", "meaningVi": "Ngày mai sẽ tổ chức đại hội nhân viên."}],
    "hsk5_222": [{"chinese": "楼下的大妈很热心。", "pinyin": "Lóuxià de dàmā hěn rèxīn.", "meaningVi": "Bác gái ở tầng dưới rất nhiệt tình."}],
    "hsk5_223": [{"chinese": "这里的大米很好吃。", "pinyin": "Zhèlǐ de dàmǐ hěn hǎochī.", "meaningVi": "Gạo ở đây rất ngon."}],
    "hsk5_224": [{"chinese": "阅读能锻炼大脑。", "pinyin": "Yuèdú néng duànliàn dànǎo.", "meaningVi": "Đọc sách có thể rèn luyện não bộ."}],
    "hsk5_225": [{"chinese": "大批游客涌入这座城市。", "pinyin": "Dàpī yóukè yǒngrù zhè zuò chéngshì.", "meaningVi": "Một lượng lớn du khách đổ về thành phố này."}],
    "hsk5_226": [{"chinese": "这座大厦有五十层。", "pinyin": "Zhè zuò dàshà yǒu wǔshí céng.", "meaningVi": "Tòa nhà này cao năm mươi tầng."}],
    "hsk5_227": [{"chinese": "结婚是人生大事。", "pinyin": "Jiéhūn shì rénshēng dàshì.", "meaningVi": "Kết hôn là việc trọng đại trong đời người."}],
    "hsk5_228": [{"chinese": "动物园里有几头大象。", "pinyin": "Dòngwùyuán lǐ yǒu jǐ tóu dàxiàng.", "meaningVi": "Trong sở thú có mấy con voi."}],
    "hsk5_229": [{"chinese": "这是一场大型演出。", "pinyin": "Zhè shì yì chǎng dàxíng yǎnchū.", "meaningVi": "Đây là một buổi biểu diễn quy mô lớn."}],
    "hsk5_230": [{"chinese": "那位大爷每天在公园散步。", "pinyin": "Nà wèi dàye měitiān zài gōngyuán sànbù.", "meaningVi": "Ông cụ đó mỗi ngày đều đi dạo trong công viên."}],
    "hsk5_231": [{"chinese": "五大于三。", "pinyin": "Wǔ dàyú sān.", "meaningVi": "Năm lớn hơn ba."}],
    "hsk5_232": [{"chinese": "这是大众都能接受的价格。", "pinyin": "Zhè shì dàzhòng dōu néng jiēshòu de jiàgé.", "meaningVi": "Đây là mức giá mà đại chúng đều có thể chấp nhận."}],
    "hsk5_235": [{"chinese": "旅游业带动了当地经济。", "pinyin": "Lǚyóuyè dàidòngle dāngdì jīngjì.", "meaningVi": "Ngành du lịch đã thúc đẩy kinh tế địa phương."}],
    "hsk5_236": [{"chinese": "没有人能代替他的位置。", "pinyin": "Méiyǒu rén néng dàitì tā de wèizhi.", "meaningVi": "Không ai có thể thay thế vị trí của anh ấy."}],
    "hsk5_237": [{"chinese": "这份工作的待遇不错。", "pinyin": "Zhè fèn gōngzuò de dàiyù búcuò.", "meaningVi": "Đãi ngộ của công việc này khá tốt."}],
    "hsk5_239": [{"chinese": "请单独跟我谈谈。", "pinyin": "Qǐng dāndú gēn wǒ tántan.", "meaningVi": "Xin nói chuyện riêng với tôi."}],
    "hsk5_240": [{"chinese": "她担任公司的财务总监。", "pinyin": "Tā dānrèn gōngsī de cáiwù zǒngjiān.", "meaningVi": "Cô ấy đảm nhiệm chức giám đốc tài chính của công ty."}],
    "hsk5_241": [{"chinese": "收入来源比较单一。", "pinyin": "Shōurù láiyuán bǐjiào dānyī.", "meaningVi": "Nguồn thu nhập khá đơn nhất."}],
    "hsk5_242": [{"chinese": "这本书分成十个单元。", "pinyin": "Zhè běn shū fēnchéng shí gè dānyuán.", "meaningVi": "Cuốn sách này chia thành mười đơn vị bài học."}],
    "hsk5_243": [{"chinese": "他从小就很胆小。", "pinyin": "Tā cóngxiǎo jiù hěn dǎnxiǎo.", "meaningVi": "Anh ấy từ nhỏ đã rất nhút nhát."}],
    "hsk5_244": [{"chinese": "这道菜味道有点淡。", "pinyin": "Zhè dào cài wèidào yǒudiǎn dàn.", "meaningVi": "Món ăn này vị hơi nhạt."}],
    "hsk5_245": [{"chinese": "我们尝了当地的特色小吃。", "pinyin": "Wǒmen chángle dāngdì de tèsè xiǎochī.", "meaningVi": "Chúng tôi đã nếm thử món ăn vặt đặc sắc của địa phương."}],
    "hsk5_246": [{"chinese": "他常常想起当年的往事。", "pinyin": "Tā chángcháng xiǎngqǐ dāngnián de wǎngshì.", "meaningVi": "Anh ấy thường nhớ lại những chuyện xưa năm đó."}],
    "hsk5_248": [{"chinese": "在这些学生当中，他最优秀。", "pinyin": "Zài zhèxiē xuésheng dāngzhōng, tā zuì yōuxiù.", "meaningVi": "Trong số những học sinh này, anh ấy xuất sắc nhất."}],
    "hsk5_251": [{"chinese": "他把这里当成自己的家。", "pinyin": "Tā bǎ zhèlǐ dàngchéng zìjǐ de jiā.", "meaningVi": "Anh ấy coi nơi đây như nhà của mình."}],
    "hsk5_252": [{"chinese": "请把我的话当作参考。", "pinyin": "Qǐng bǎ wǒ de huà dàngzuò cānkǎo.", "meaningVi": "Xin hãy coi lời tôi nói như một tham khảo."}],
    "hsk5_255": [{"chinese": "粗心导致了这次失误。", "pinyin": "Cūxīn dǎozhìle zhè cì shīwù.", "meaningVi": "Sự bất cẩn đã dẫn đến sai sót lần này."}],
    "hsk5_256": [{"chinese": "飞机延误了，我们很晚才到达。", "pinyin": "Fēijī yánwù le, wǒmen hěn wǎn cái dàodá.", "meaningVi": "Máy bay bị trễ, chúng tôi rất muộn mới đến nơi."}],
    "hsk5_257": [{"chinese": "他说的话很有道理。", "pinyin": "Tā shuō de huà hěn yǒu dàolǐ.", "meaningVi": "Lời anh ấy nói rất có lý."}],
    "hsk5_258": [{"chinese": "我的护照快到期了。", "pinyin": "Wǒ de hùzhào kuài dàoqī le.", "meaningVi": "Hộ chiếu của tôi sắp hết hạn rồi."}],
    "hsk5_259": [{"chinese": "他们登上了山顶。", "pinyin": "Tāmen dēngshàngle shāndǐng.", "meaningVi": "Họ đã trèo lên đến đỉnh núi."}],
    "hsk5_260": [{"chinese": "舞台上的灯光很漂亮。", "pinyin": "Wǔtái shàng de dēngguāng hěn piàoliang.", "meaningVi": "Ánh đèn trên sân khấu rất đẹp."}],
    "hsk5_261": [{"chinese": "请先在前台登记。", "pinyin": "Qǐng xiān zài qiántái dēngjì.", "meaningVi": "Xin hãy đăng ký ở quầy lễ tân trước."}],
    "hsk5_262": [{"chinese": "请登录您的账号。", "pinyin": "Qǐng dēnglù nín de zhànghào.", "meaningVi": "Xin đăng nhập tài khoản của bạn."}],
    "hsk5_263": [{"chinese": "大家都在耐心等待。", "pinyin": "Dàjiā dōu zài nàixīn děngdài.", "meaningVi": "Mọi người đều đang kiên nhẫn chờ đợi."}],
    "hsk5_264": [{"chinese": "请在门口等候。", "pinyin": "Qǐng zài ménkǒu děnghòu.", "meaningVi": "Xin đợi ở cửa."}],
    "hsk5_265": [{"chinese": "二加二等于四。", "pinyin": "Èr jiā èr děngyú sì.", "meaningVi": "Hai cộng hai bằng bốn."}],
    "hsk5_266": [{"chinese": "他低头看着手机。", "pinyin": "Tā dītóu kànzhe shǒujī.", "meaningVi": "Anh ấy cúi đầu nhìn điện thoại."}],
    "hsk5_267": [{"chinese": "这个方法的确有效。", "pinyin": "Zhège fāngfǎ díquè yǒuxiào.", "meaningVi": "Phương pháp này quả thực có hiệu quả."}],
    "hsk5_268": [{"chinese": "他们打败了敌人。", "pinyin": "Tāmen dǎbàile dírén.", "meaningVi": "Họ đã đánh bại kẻ địch."}],
    "hsk5_269": [{"chinese": "请把盐递给我。", "pinyin": "Qǐng bǎ yán dì gěi wǒ.", "meaningVi": "Xin đưa muối cho tôi."}],
    "hsk5_270": [{"chinese": "他对地理很感兴趣。", "pinyin": "Tā duì dìlǐ hěn gǎn xìngqù.", "meaningVi": "Anh ấy rất hứng thú với địa lý."}],
    "hsk5_271": [{"chinese": "地面上都是水。", "pinyin": "Dìmiàn shàng dōu shì shuǐ.", "meaningVi": "Trên mặt đất toàn là nước."}],
    "hsk5_272": [{"chinese": "这个地区经济发展很快。", "pinyin": "Zhège dìqū jīngjì fāzhǎn hěn kuài.", "meaningVi": "Kinh tế của khu vực này phát triển rất nhanh."}],
    "hsk5_273": [{"chinese": "她在公司的地位很重要。", "pinyin": "Tā zài gōngsī de dìwèi hěn zhòngyào.", "meaningVi": "Địa vị của cô ấy trong công ty rất quan trọng."}],
    "hsk5_276": [{"chinese": "下午茶时间可以吃点心。", "pinyin": "Xiàwǔchá shíjiān kěyǐ chī diǎnxin.", "meaningVi": "Giờ trà chiều có thể ăn điểm tâm."}],
    "hsk5_277": [{"chinese": "这条视频获得了很多点赞。", "pinyin": "Zhè tiáo shìpín huòdéle hěn duō diǎnzàn.", "meaningVi": "Video này nhận được rất nhiều lượt thích."}],
    "hsk5_279": [{"chinese": "他骑的是电动车。", "pinyin": "Tā qí de shì diàndòng chē.", "meaningVi": "Xe anh ấy đi là xe điện."}],
    "hsk5_280": [{"chinese": "这家店卖各种电器。", "pinyin": "Zhè jiā diàn mài gèzhǒng diànqì.", "meaningVi": "Cửa hàng này bán các loại đồ điện."}],
    "hsk5_281": [{"chinese": "电商行业发展迅速。", "pinyin": "Diànshāng hángyè fāzhǎn xùnsù.", "meaningVi": "Ngành thương mại điện tử phát triển nhanh chóng."}],
    "hsk5_282": [{"chinese": "他在电视台工作。", "pinyin": "Tā zài diànshìtái gōngzuò.", "meaningVi": "Anh ấy làm việc ở đài truyền hình."}],
    "hsk5_283": [{"chinese": "这本书有电子版。", "pinyin": "Zhè běn shū yǒu diànzǐbǎn.", "meaningVi": "Cuốn sách này có bản điện tử."}],
    "hsk5_285": [{"chinese": "公司派人去做市场调研。", "pinyin": "Gōngsī pài rén qù zuò shìchǎng diàoyán.", "meaningVi": "Công ty cử người đi khảo sát thị trường."}],
    "hsk5_287": [{"chinese": "他的钱包丢失了。", "pinyin": "Tā de qiánbāo diūshī le.", "meaningVi": "Ví của anh ấy đã bị mất."}],
    "hsk5_289": [{"chinese": "墙上有一个洞。", "pinyin": "Qiáng shàng yǒu yí gè dòng.", "meaningVi": "Trên tường có một cái lỗ."}],
    "hsk5_290": [{"chinese": "孩子们喜欢看动画片。", "pinyin": "Háizimen xǐhuan kàn dònghuàpiàn.", "meaningVi": "Trẻ con thích xem phim hoạt hình."}],
    "hsk5_291": [{"chinese": "她的歌声十分动人。", "pinyin": "Tā de gēshēng shífēn dòngrén.", "meaningVi": "Giọng hát của cô ấy vô cùng lay động lòng người."}],
    "hsk5_292": [{"chinese": "大家一起动手打扫吧。", "pinyin": "Dàjiā yìqǐ dòngshǒu dǎsǎo ba.", "meaningVi": "Mọi người cùng bắt tay vào dọn dẹp đi."}],
    "hsk5_293": [{"chinese": "妈妈做了一盘豆腐。", "pinyin": "Māma zuòle yì pán dòufu.", "meaningVi": "Mẹ đã làm một đĩa đậu phụ."}],
    "hsk5_294": [{"chinese": "早餐我喝了一杯豆浆。", "pinyin": "Zǎocān wǒ hēle yì bēi dòujiāng.", "meaningVi": "Bữa sáng tôi đã uống một cốc sữa đậu nành."}],
    "hsk5_296": [{"chinese": "这个设计很独特。", "pinyin": "Zhège shèjì hěn dútè.", "meaningVi": "Thiết kế này rất độc đáo."}],
    "hsk5_297": [{"chinese": "这个字的读音是什么？", "pinyin": "Zhège zì de dúyīn shì shénme?", "meaningVi": "Cách đọc của chữ này là gì?"}],
    "hsk5_298": [{"chinese": "她独自一人去了旅行。", "pinyin": "Tā dúzì yì rén qùle lǚxíng.", "meaningVi": "Cô ấy một mình đi du lịch."}],
    "hsk5_301": [{"chinese": "他很谦虚，从不掩饰自己的短处。", "pinyin": "Tā hěn qiānxū, cóng bù yǎnshì zìjǐ de duǎnchù.", "meaningVi": "Anh ấy rất khiêm tốn, không bao giờ che giấu điểm yếu của mình."}],
    "hsk5_303": [{"chinese": "绳子突然断了。", "pinyin": "Shéngzi tūrán duàn le.", "meaningVi": "Sợi dây đột nhiên đứt."}],
    "hsk5_306": [{"chinese": "他很认真地对待这份工作。", "pinyin": "Tā hěn rènzhēn de duìdài zhè fèn gōngzuò.", "meaningVi": "Anh ấy rất nghiêm túc đối với công việc này."}],
    "hsk5_307": [{"chinese": "他是我的强劲对手。", "pinyin": "Tā shì wǒ de qiángjìng duìshǒu.", "meaningVi": "Anh ấy là đối thủ mạnh của tôi."}],
    "hsk5_308": [{"chinese": "他带领队伍完成了这次任务。", "pinyin": "Tā dàilǐng duìwu wánchéngle zhè cì rènwu.", "meaningVi": "Anh ấy đã dẫn dắt đội ngũ hoàn thành nhiệm vụ lần này."}],
    "hsk5_309": [{"chinese": "他还没有交往对象。", "pinyin": "Tā hái méiyǒu jiāowǎng duìxiàng.", "meaningVi": "Anh ấy vẫn chưa có đối tượng yêu đương."}],
    "hsk5_312": [{"chinese": "他躲在门后面。", "pinyin": "Tā duǒ zài mén hòumiàn.", "meaningVi": "Anh ấy trốn sau cánh cửa."}],
    "hsk5_313": [{"chinese": "父母为儿女操心一辈子。", "pinyin": "Fùmǔ wèi érnǚ cāoxīn yíbèizi.", "meaningVi": "Cha mẹ lo lắng cho con cái cả đời."}],
    "hsk5_314": [{"chinese": "他买了一辆二手车。", "pinyin": "Tā mǎile yí liàng èrshǒu chē.", "meaningVi": "Anh ấy đã mua một chiếc xe cũ."}],
    "hsk5_315": [{"chinese": "请扫描这个二维码。", "pinyin": "Qǐng sǎomiáo zhège èrwéimǎ.", "meaningVi": "Xin quét mã QR này."}],
    "hsk5_316": [{"chinese": "他在杂志上发表了一篇文章。", "pinyin": "Tā zài zázhì shàng fābiǎole yì piān wénzhāng.", "meaningVi": "Anh ấy đã đăng một bài viết trên tạp chí."}],
    "hsk5_317": [{"chinese": "公司发布了新产品。", "pinyin": "Gōngsī fābùle xīn chǎnpǐn.", "meaningVi": "Công ty đã ra mắt sản phẩm mới."}],
    "hsk5_319": [{"chinese": "他在比赛中发挥得很好。", "pinyin": "Tā zài bǐsài zhōng fāhuī de hěn hǎo.", "meaningVi": "Anh ấy thể hiện rất tốt trong trận đấu."}],
    "hsk5_321": [{"chinese": "他发起了这项公益活动。", "pinyin": "Tā fāqǐle zhè xiàng gōngyì huódòng.", "meaningVi": "Anh ấy đã phát động hoạt động công ích này."}],
    "hsk5_324": [{"chinese": "违反规定会被罚款。", "pinyin": "Wéifǎn guīdìng huì bèi fákuǎn.", "meaningVi": "Vi phạm quy định sẽ bị phạt tiền."}],
    "hsk5_326": [{"chinese": "这件案子已经交给法院处理。", "pinyin": "Zhè jiàn ànzi yǐjīng jiāo gěi fǎyuàn chǔlǐ.", "meaningVi": "Vụ án này đã được giao cho tòa án xử lý."}],
    "hsk5_327": [{"chinese": "请把书翻到第十页。", "pinyin": "Qǐng bǎ shū fāndào dì-shí yè.", "meaningVi": "Xin lật sách đến trang mười."}],
    "hsk5_328": [{"chinese": "这个汤里有番茄。", "pinyin": "Zhège tāng lǐ yǒu fānqié.", "meaningVi": "Trong món canh này có cà chua."}],
    "hsk5_331": [{"chinese": "他不但没生气，反而笑了。", "pinyin": "Tā búdàn méi shēngqì, fǎn'ér xiào le.", "meaningVi": "Anh ấy chẳng những không tức giận, ngược lại còn cười."}],
    "hsk5_333": [{"chinese": "他明天返回北京。", "pinyin": "Tā míngtiān fǎnhuí Běijīng.", "meaningVi": "Ngày mai anh ấy quay về Bắc Kinh."}],
    "hsk5_335": [{"chinese": "这个数据反映了真实情况。", "pinyin": "Zhège shùjù fǎnyìngle zhēnshí qíngkuàng.", "meaningVi": "Số liệu này phản ánh tình hình thực tế."}],
    "hsk5_336": [{"chinese": "反正我不同意这个方案。", "pinyin": "Fǎnzhèng wǒ bù tóngyì zhège fāng'àn.", "meaningVi": "Dù sao thì tôi cũng không đồng ý với phương án này."}],
    "hsk5_337": [{"chinese": "这超出了我的工作范围。", "pinyin": "Zhè chāochūle wǒ de gōngzuò fànwéi.", "meaningVi": "Việc này vượt ra ngoài phạm vi công việc của tôi."}],
    "hsk5_339": [{"chinese": "我们讨论了几个方案。", "pinyin": "Wǒmen tǎolùnle jǐ gè fāng'àn.", "meaningVi": "Chúng tôi đã thảo luận vài phương án."}],
    "hsk5_340": [{"chinese": "出门要防晒。", "pinyin": "Chūmén yào fángshài.", "meaningVi": "Ra ngoài phải chống nắng."}],
    "hsk5_341": [{"chinese": "地震损坏了很多房屋。", "pinyin": "Dìzhèn sǔnhuàile hěn duō fángwū.", "meaningVi": "Động đất đã làm hư hại rất nhiều nhà cửa."}],
    "hsk5_342": [{"chinese": "我们要防止类似问题再次发生。", "pinyin": "Wǒmen yào fángzhǐ lèisì wèntí zàicì fāshēng.", "meaningVi": "Chúng ta phải ngăn ngừa vấn đề tương tự xảy ra lần nữa."}],
    "hsk5_343": [{"chinese": "她仿佛什么都没听见。", "pinyin": "Tā fǎngfú shénme dōu méi tīngjiàn.", "meaningVi": "Cô ấy dường như không nghe thấy gì cả."}],
    "hsk5_344": [{"chinese": "总统正式访问了这个国家。", "pinyin": "Zǒngtǒng zhèngshì fǎngwènle zhège guójiā.", "meaningVi": "Tổng thống đã chính thức thăm quốc gia này."}],
    "hsk5_345": [{"chinese": "飞机正在平稳飞行。", "pinyin": "Fēijī zhèngzài píngwěn fēixíng.", "meaningVi": "Máy bay đang bay ổn định."}],
    "hsk5_346": [{"chinese": "他的梦想是成为一名飞行员。", "pinyin": "Tā de mèngxiǎng shì chéngwéi yì míng fēixíngyuán.", "meaningVi": "Ước mơ của anh ấy là trở thành một phi công."}],
    "hsk5_347": [{"chinese": "非洲有很多野生动物。", "pinyin": "Fēizhōu yǒu hěn duō yěshēng dòngwù.", "meaningVi": "Châu Phi có rất nhiều động vật hoang dã."}],
    "hsk5_349": [{"chinese": "人口分布不均。", "pinyin": "Rénkǒu fēnbù bù jūn.", "meaningVi": "Dân số phân bố không đều."}],
    "hsk5_351": [{"chinese": "请把垃圾分类处理。", "pinyin": "Qǐng bǎ lājī fēnlèi chǔlǐ.", "meaningVi": "Xin phân loại rác trước khi xử lý."}],
    "hsk5_352": [{"chinese": "这两种物质很难分离。", "pinyin": "Zhè liǎng zhǒng wùzhì hěn nán fēnlí.", "meaningVi": "Hai chất này rất khó tách rời."}],
    "hsk5_353": [{"chinese": "任务已经分配给大家了。", "pinyin": "Rènwu yǐjīng fēnpèi gěi dàjiā le.", "meaningVi": "Nhiệm vụ đã được phân công cho mọi người."}],
    "hsk5_354": [{"chinese": "他们两个人分手了。", "pinyin": "Tāmen liǎng gè rén fēnshǒu le.", "meaningVi": "Hai người họ đã chia tay."}],
    "hsk5_356": [{"chinese": "她喜欢和朋友分享快乐。", "pinyin": "Tā xǐhuan hé péngyou fēnxiǎng kuàilè.", "meaningVi": "Cô ấy thích chia sẻ niềm vui với bạn bè."}],
    "hsk5_357": [{"chinese": "他为了梦想努力奋斗。", "pinyin": "Tā wèile mèngxiǎng nǔlì fèndòu.", "meaningVi": "Anh ấy nỗ lực phấn đấu vì ước mơ."}],
    "hsk5_358": [{"chinese": "学校的课外活动丰富多彩。", "pinyin": "Xuéxiào de kèwài huódòng fēngfù-duōcǎi.", "meaningVi": "Hoạt động ngoại khóa của trường phong phú đa dạng."}],
    "hsk5_359": [{"chinese": "他的写作风格很独特。", "pinyin": "Tā de xiězuò fēnggé hěn dútè.", "meaningVi": "Phong cách viết của anh ấy rất độc đáo."}],
    "hsk5_361": [{"chinese": "每个地方的风俗都不一样。", "pinyin": "Měi gè dìfang de fēngsú dōu bù yíyàng.", "meaningVi": "Phong tục của mỗi nơi đều không giống nhau."}],
    "hsk5_362": [{"chinese": "投资总是有风险的。", "pinyin": "Tóuzī zǒngshì yǒu fēngxiǎn de.", "meaningVi": "Đầu tư luôn có rủi ro."}],
    "hsk5_364": [{"chinese": "他否认了这个说法。", "pinyin": "Tā fǒurènle zhège shuōfǎ.", "meaningVi": "Anh ấy đã phủ nhận cách nói này."}],
    "hsk5_365": [{"chinese": "这对夫妇结婚三十年了。", "pinyin": "Zhè duì fūfù jiéhūn sānshí nián le.", "meaningVi": "Cặp vợ chồng này đã kết hôn ba mươi năm rồi."}],
    "hsk5_367": [{"chinese": "这是个有福气的孩子。", "pinyin": "Zhè shì gè yǒu fúqi de háizi.", "meaningVi": "Đây là một đứa trẻ có phúc."}],
    "hsk5_368": [{"chinese": "这家店卖女士服装。", "pinyin": "Zhè jiā diàn mài nǚshì fúzhuāng.", "meaningVi": "Cửa hàng này bán quần áo nữ."}],
    "hsk5_369": [{"chinese": "他递给我一副手套。", "pinyin": "Tā dì gěi wǒ yí fù shǒutào.", "meaningVi": "Anh ấy đưa cho tôi một đôi găng tay."}],
    "hsk5_370": [{"chinese": "他家很富有。", "pinyin": "Tā jiā hěn fùyǒu.", "meaningVi": "Nhà anh ấy rất giàu có."}],
    "hsk5_371": [{"chinese": "他为家庭付出了很多。", "pinyin": "Tā wèi jiātíng fùchūle hěn duō.", "meaningVi": "Anh ấy đã cống hiến rất nhiều cho gia đình."}],
    "hsk5_373": [{"chinese": "三月八日是妇女节。", "pinyin": "Sānyuè bā rì shì Fùnǚjié.", "meaningVi": "Ngày mùng tám tháng ba là ngày Quốc tế Phụ nữ."}],
    "hsk5_375": [{"chinese": "请复制这段文字。", "pinyin": "Qǐng fùzhì zhè duàn wénzì.", "meaningVi": "Xin sao chép đoạn văn bản này."}],
    "hsk5_377": [{"chinese": "我们需要改进工作方法。", "pinyin": "Wǒmen xūyào gǎijìn gōngzuò fāngfǎ.", "meaningVi": "Chúng ta cần cải tiến phương pháp làm việc."}],
    "hsk5_378": [{"chinese": "他的病情有所改善。", "pinyin": "Tā de bìngqíng yǒusuǒ gǎishàn.", "meaningVi": "Tình trạng bệnh của anh ấy đã có phần cải thiện."}],
    "hsk5_379": [{"chinese": "今天没空，改天再聊吧。", "pinyin": "Jīntiān méi kòng, gǎitiān zài liáo ba.", "meaningVi": "Hôm nay không rảnh, hôm khác nói chuyện tiếp nhé."}],
    "hsk5_380": [{"chinese": "他及时改正了错误。", "pinyin": "Tā jíshí gǎizhèngle cuòwù.", "meaningVi": "Anh ấy đã kịp thời sửa chữa lỗi lầm."}],
    "hsk5_383": [{"chinese": "这是一个新概念。", "pinyin": "Zhè shì yí gè xīn gàiniàn.", "meaningVi": "Đây là một khái niệm mới."}],
    "hsk5_384": [{"chinese": "我们要敢于面对挑战。", "pinyin": "Wǒmen yào gǎnyú miànduì tiǎozhàn.", "meaningVi": "Chúng ta phải dám đối mặt với thử thách."}],
    "hsk5_386": [{"chinese": "他长得又高大又帅气。", "pinyin": "Tā zhǎng de yòu gāodà yòu shuàiqì.", "meaningVi": "Anh ấy cao lớn lại đẹp trai."}],
    "hsk5_387": [{"chinese": "这是一家高档餐厅。", "pinyin": "Zhè shì yì jiā gāodàng cāntīng.", "meaningVi": "Đây là một nhà hàng cao cấp."}],
    "hsk5_389": [{"chinese": "他住在高级公寓里。", "pinyin": "Tā zhù zài gāojí gōngyù lǐ.", "meaningVi": "Anh ấy sống trong căn hộ cao cấp."}],
    "hsk5_390": [{"chinese": "这是一款高科技产品。", "pinyin": "Zhè shì yì kuǎn gāokējì chǎnpǐn.", "meaningVi": "Đây là một sản phẩm công nghệ cao."}],
    "hsk5_391": [{"chinese": "他工作起来非常高效。", "pinyin": "Tā gōngzuò qǐlai fēicháng gāoxiào.", "meaningVi": "Anh ấy làm việc rất hiệu quả."}],
    "hsk5_393": [{"chinese": "他向大家告别后离开了。", "pinyin": "Tā xiàng dàjiā gàobié hòu líkāi le.", "meaningVi": "Anh ấy từ biệt mọi người rồi rời đi."}],
    "hsk5_394": [{"chinese": "这首歌的歌词很感人。", "pinyin": "Zhè shǒu gē de gēcí hěn gǎnrén.", "meaningVi": "Lời của bài hát này rất cảm động."}],
    "hsk5_395": [{"chinese": "我喜欢这首歌曲。", "pinyin": "Wǒ xǐhuan zhè shǒu gēqǔ.", "meaningVi": "Tôi thích bài hát này."}],
    "hsk5_396": [{"chinese": "他们隔着一条河住。", "pinyin": "Tāmen gézhe yì tiáo hé zhù.", "meaningVi": "Họ sống cách nhau một con sông."}],
    "hsk5_397": [{"chinese": "今天格外热。", "pinyin": "Jīntiān géwài rè.", "meaningVi": "Hôm nay nóng khác thường."}],
    "hsk5_399": [{"chinese": "各行各业都需要人才。", "pinyin": "Gèháng-gèyè dōu xūyào réncái.", "meaningVi": "Mọi ngành nghề đều cần nhân tài."}],
    "hsk5_400": [{"chinese": "这只是我个人的看法。", "pinyin": "Zhè zhǐshì wǒ gèrén de kànfǎ.", "meaningVi": "Đây chỉ là quan điểm cá nhân của tôi."}],
    "hsk5_401": [{"chinese": "他的个性很开朗。", "pinyin": "Tā de gèxìng hěn kāilǎng.", "meaningVi": "Cá tính của anh ấy rất cởi mở."}],
    "hsk5_402": [{"chinese": "大家各自回家了。", "pinyin": "Dàjiā gèzì huí jiā le.", "meaningVi": "Mọi người mỗi người tự về nhà."}],
    "hsk5_405": [{"chinese": "请更换新的零件。", "pinyin": "Qǐng gēnghuàn xīn de língjiàn.", "meaningVi": "Xin thay linh kiện mới."}],
    "hsk5_406": [{"chinese": "请更新你的软件。", "pinyin": "Qǐng gēngxīn nǐ de ruǎnjiàn.", "meaningVi": "Xin cập nhật phần mềm của bạn."}],
    "hsk5_407": [{"chinese": "考试成绩已经公布了。", "pinyin": "Kǎoshì chéngjì yǐjīng gōngbù le.", "meaningVi": "Điểm thi đã được công bố."}],
    "hsk5_408": [{"chinese": "这项工程还没完工。", "pinyin": "Zhè xiàng gōngchéng hái méi wángōng.", "meaningVi": "Công trình này vẫn chưa hoàn thành."}],
    "hsk5_409": [{"chinese": "他是一名软件工程师。", "pinyin": "Tā shì yì míng ruǎnjiàn gōngchéngshī.", "meaningVi": "Anh ấy là một kỹ sư phần mềm."}],
    "hsk5_410": [{"chinese": "这是修车用的工具。", "pinyin": "Zhè shì xiūchē yòng de gōngjù.", "meaningVi": "Đây là công cụ dùng để sửa xe."}],
    "hsk5_411": [{"chinese": "这部手机功能很多。", "pinyin": "Zhè bù shǒujī gōngnéng hěn duō.", "meaningVi": "Điện thoại này có rất nhiều tính năng."}],
    "hsk5_412": [{"chinese": "比赛结果很公平。", "pinyin": "Bǐsài jiéguǒ hěn gōngpíng.", "meaningVi": "Kết quả trận đấu rất công bằng."}],
    "hsk5_413": [{"chinese": "他考上了公务员。", "pinyin": "Tā kǎoshàngle gōngwùyuán.", "meaningVi": "Anh ấy đã thi đỗ công chức."}],
    "hsk5_414": [{"chinese": "恭喜你们喜结良缘。", "pinyin": "Gōngxǐ nǐmen xǐjié-liángyuán.", "meaningVi": "Chúc mừng hai bạn nên duyên vợ chồng."}],
    "hsk5_415": [{"chinese": "这个城市以工业为主。", "pinyin": "Zhège chéngshì yǐ gōngyè wéi zhǔ.", "meaningVi": "Thành phố này chủ yếu phát triển công nghiệp."}],
    "hsk5_416": [{"chinese": "这件工艺品非常精美。", "pinyin": "Zhè jiàn gōngyìpǐn fēicháng jīngměi.", "meaningVi": "Sản phẩm thủ công mỹ nghệ này vô cùng tinh xảo."}],
    "hsk5_417": [{"chinese": "他租了一套公寓。", "pinyin": "Tā zūle yí tào gōngyù.", "meaningVi": "Anh ấy đã thuê một căn hộ."}],
    "hsk5_419": [{"chinese": "城市里有很多共享单车。", "pinyin": "Chéngshì lǐ yǒu hěn duō gòngxiǎng dānchē.", "meaningVi": "Trong thành phố có rất nhiều xe đạp dùng chung."}],
    "hsk5_420": [{"chinese": "有效沟通能解决很多问题。", "pinyin": "Yǒuxiào gōutōng néng jiějué hěn duō wèntí.", "meaningVi": "Giao tiếp hiệu quả có thể giải quyết nhiều vấn đề."}],
    "hsk5_422": [{"chinese": "这是一座古城。", "pinyin": "Zhè shì yí zuò gǔ chéng.", "meaningVi": "Đây là một thành cổ."}],
    "hsk5_424": [{"chinese": "古代人是怎么生活的？", "pinyin": "Gǔdài rén shì zěnme shēnghuó de?", "meaningVi": "Người cổ đại sống như thế nào?"}],
    "hsk5_425": [{"chinese": "这是一个古老的传说。", "pinyin": "Zhè shì yí gè gǔlǎo de chuánshuō.", "meaningVi": "Đây là một truyền thuyết cổ xưa."}],
    "hsk5_426": [{"chinese": "大家都为他鼓掌。", "pinyin": "Dàjiā dōu wèi tā gǔzhǎng.", "meaningVi": "Mọi người đều vỗ tay cho anh ấy."}],
    "hsk5_427": [{"chinese": "请把梯子固定好。", "pinyin": "Qǐng bǎ tīzi gùdìng hǎo.", "meaningVi": "Xin cố định thang cho chắc."}],
    "hsk5_428": [{"chinese": "他常年在外，很少回故乡。", "pinyin": "Tā chángnián zài wài, hěn shǎo huí gùxiāng.", "meaningVi": "Anh ấy quanh năm ở xa, ít khi về quê hương."}],
    "hsk5_429": [{"chinese": "看病前要先挂号。", "pinyin": "Kànbìng qián yào xiān guàhào.", "meaningVi": "Trước khi khám bệnh phải xếp số trước."}],
    "hsk5_431": [{"chinese": "请关闭窗户。", "pinyin": "Qǐng guānbì chuānghu.", "meaningVi": "Xin đóng cửa sổ lại."}],
    "hsk5_432": [{"chinese": "他仔细观察了这只昆虫。", "pinyin": "Tā zǐxì guānchále zhè zhī kūnchóng.", "meaningVi": "Anh ấy đã quan sát kỹ con côn trùng này."}],
    "hsk5_433": [{"chinese": "我不同意你的观点。", "pinyin": "Wǒ bù tóngyì nǐ de guāndiǎn.", "meaningVi": "Tôi không đồng ý với quan điểm của bạn."}],
    "hsk5_434": [{"chinese": "年轻人的消费观念在变化。", "pinyin": "Niánqīng rén de xiāofèi guānniàn zài biànhuà.", "meaningVi": "Quan niệm tiêu dùng của giới trẻ đang thay đổi."}],
    "hsk5_435": [{"chinese": "上届冠军今年再次夺冠。", "pinyin": "Shàng jiè guànjūn jīnnián zàicì duóguàn.", "meaningVi": "Nhà vô địch mùa trước năm nay lại giành chức vô địch."}],
    "hsk5_436": [{"chinese": "欢迎光临。", "pinyin": "Huānyíng guānglín.", "meaningVi": "Hoan nghênh quý khách."}],
    "hsk5_438": [{"chinese": "房间里的光线不太好。", "pinyin": "Fángjiān lǐ de guāngxiàn bú tài hǎo.", "meaningVi": "Ánh sáng trong phòng không tốt lắm."}],
    "hsk5_439": [{"chinese": "这个消息传得很广。", "pinyin": "Zhège xiāoxi chuán de hěn guǎng.", "meaningVi": "Tin này lan truyền rất rộng."}],
    "hsk5_440": [{"chinese": "晚上很多人在广场跳舞。", "pinyin": "Wǎnshang hěn duō rén zài guǎngchǎng tiàowǔ.", "meaningVi": "Buổi tối rất nhiều người nhảy múa ở quảng trường."}],
    "hsk5_441": [{"chinese": "这项政策受到广大群众的欢迎。", "pinyin": "Zhè xiàng zhèngcè shòudào guǎngdà qúnzhòng de huānyíng.", "meaningVi": "Chính sách này được đông đảo quần chúng hoan nghênh."}],
    "hsk5_444": [{"chinese": "这家公司规模不小。", "pinyin": "Zhè jiā gōngsī guīmó bù xiǎo.", "meaningVi": "Quy mô của công ty này không nhỏ."}],
    "hsk5_446": [{"chinese": "初次见面不知贵姓大名？", "pinyin": "Chūcì jiànmiàn bùzhī guìxìng dàmíng?", "meaningVi": "Lần đầu gặp mặt, không biết quý danh của ngài là gì?"}],
    "hsk5_447": [{"chinese": "衣服都放在柜子里。", "pinyin": "Yīfu dōu fàng zài guìzi lǐ.", "meaningVi": "Quần áo đều để trong tủ."}],
    "hsk5_450": [{"chinese": "她喜欢画国画。", "pinyin": "Tā xǐhuan huà guóhuà.", "meaningVi": "Cô ấy thích vẽ tranh quốc họa."}],
    "hsk5_451": [{"chinese": "国庆节我们放假七天。", "pinyin": "Guóqìngjié wǒmen fàngjià qī tiān.", "meaningVi": "Dịp Quốc khánh chúng tôi được nghỉ bảy ngày."}],
    "hsk5_452": [{"chinese": "他果然没有来。", "pinyin": "Tā guǒrán méiyǒu lái.", "meaningVi": "Quả nhiên anh ấy đã không đến."}],
    "hsk5_453": [{"chinese": "这是他努力的果实。", "pinyin": "Zhè shì tā nǔlì de guǒshí.", "meaningVi": "Đây là thành quả nỗ lực của anh ấy."}],
    "hsk5_454": [{"chinese": "过度劳累对身体不好。", "pinyin": "Guòdù láolèi duì shēntǐ bù hǎo.", "meaningVi": "Làm việc quá sức không tốt cho sức khỏe."}],
    "hsk5_455": [{"chinese": "他这样做有点过分了。", "pinyin": "Tā zhèyàng zuò yǒudiǎn guòfèn le.", "meaningVi": "Anh ấy làm như vậy hơi quá đáng rồi."}],
    "hsk5_457": [{"chinese": "这瓶牛奶已经过期了。", "pinyin": "Zhè píng niúnǎi yǐjīng guòqī le.", "meaningVi": "Chai sữa này đã hết hạn rồi."}],
    "hsk5_458": [{"chinese": "他做事过于小心。", "pinyin": "Tā zuòshì guòyú xiǎoxīn.", "meaningVi": "Anh ấy làm việc quá cẩn thận."}],
    "hsk5_460": [{"chinese": "过海关需要出示护照。", "pinyin": "Guò hǎiguān xūyào chūshì hùzhào.", "meaningVi": "Qua hải quan cần xuất trình hộ chiếu."}],
    "hsk5_461": [{"chinese": "他的孩子在海外留学。", "pinyin": "Tā de háizi zài hǎiwài liúxué.", "meaningVi": "Con của anh ấy đang du học ở nước ngoài."}],
    "hsk5_462": [{"chinese": "这家餐厅的海鲜很新鲜。", "pinyin": "Zhè jiā cāntīng de hǎixiān hěn xīnxiān.", "meaningVi": "Hải sản của nhà hàng này rất tươi."}],
    "hsk5_463": [{"chinese": "这种饮料含糖量很高。", "pinyin": "Zhè zhǒng yǐnliào hán táng liàng hěn gāo.", "meaningVi": "Loại đồ uống này chứa hàm lượng đường rất cao."}],
    "hsk5_464": [{"chinese": "这种水果的维生素含量很高。", "pinyin": "Zhè zhǒng shuǐguǒ de wéishēngsù hánliàng hěn gāo.", "meaningVi": "Hàm lượng vitamin trong loại trái cây này rất cao."}],
    "hsk5_465": [{"chinese": "这种蔬菜含有丰富的营养。", "pinyin": "Zhè zhǒng shūcài hányǒu fēngfù de yíngyǎng.", "meaningVi": "Loại rau này chứa nhiều dinh dưỡng."}],
    "hsk5_466": [{"chinese": "他的额头上满是汗水。", "pinyin": "Tā de étóu shàng mǎn shì hànshuǐ.", "meaningVi": "Trên trán anh ấy đầy mồ hôi."}],
    "hsk5_468": [{"chinese": "他从事金融行业。", "pinyin": "Tā cóngshì jīnróng hángyè.", "meaningVi": "Anh ấy làm trong ngành tài chính."}],
    "hsk5_469": [{"chinese": "这家餐厅获得了很多好评。", "pinyin": "Zhè jiā cāntīng huòdéle hěn duō hǎopíng.", "meaningVi": "Nhà hàng này nhận được rất nhiều đánh giá tốt."}],
    "hsk5_470": [{"chinese": "祝你好运。", "pinyin": "Zhù nǐ hǎoyùn.", "meaningVi": "Chúc bạn may mắn."}],
    "hsk5_471": [{"chinese": "最近经济形势有所好转。", "pinyin": "Zuìjìn jīngjì xíngshì yǒusuǒ hǎozhuǎn.", "meaningVi": "Gần đây tình hình kinh tế có phần chuyển biến tốt."}],
    "hsk5_473": [{"chinese": "孩子对什么都很好奇。", "pinyin": "Háizi duì shénme dōu hěn hàoqí.", "meaningVi": "Trẻ con tò mò với mọi thứ."}],
    "hsk5_474": [{"chinese": "这双鞋不合脚。", "pinyin": "Zhè shuāng xié bù hé jiǎo.", "meaningVi": "Đôi giày này không vừa chân."}],
    "hsk5_475": [{"chinese": "这样做是合法的。", "pinyin": "Zhèyàng zuò shì héfǎ de.", "meaningVi": "Làm như vậy là hợp pháp."}],
    "hsk5_476": [{"chinese": "中午我们叫了盒饭。", "pinyin": "Zhōngwǔ wǒmen jiàole héfàn.", "meaningVi": "Buổi trưa chúng tôi gọi cơm hộp."}],
    "hsk5_477": [{"chinese": "这个价格很合理。", "pinyin": "Zhège jiàgé hěn hélǐ.", "meaningVi": "Giá này khá hợp lý."}],
    "hsk5_478": [{"chinese": "这条河流经过好几个城市。", "pinyin": "Zhè tiáo héliú jīngguò hǎo jǐ gè chéngshì.", "meaningVi": "Con sông này chảy qua mấy thành phố."}],
    "hsk5_479": [{"chinese": "请签一下合同。", "pinyin": "Qǐng qiān yíxià hétóng.", "meaningVi": "Xin ký hợp đồng."}],
    "hsk5_481": [{"chinese": "我们希望能长期合作。", "pinyin": "Wǒmen xīwàng néng chángqī hézuò.", "meaningVi": "Chúng tôi hy vọng có thể hợp tác lâu dài."}],
    "hsk5_482": [{"chinese": "天已经黑了。", "pinyin": "Tiān yǐjīng hēi le.", "meaningVi": "Trời đã tối rồi."}],
    "hsk5_483": [{"chinese": "这面墙被漆成了红色。", "pinyin": "Zhè miàn qiáng bèi qī chéngle hóngsè.", "meaningVi": "Bức tường này được sơn thành màu đỏ."}],
    "hsk5_484": [{"chinese": "树上有一只猴子。", "pinyin": "Shù shàng yǒu yì zhī hóuzi.", "meaningVi": "Trên cây có một con khỉ."}],
    "hsk5_485": [{"chinese": "请测量一下纸张的厚度。", "pinyin": "Qǐng cèliáng yíxià zhǐzhāng de hòudù.", "meaningVi": "Xin đo độ dày của tờ giấy."}],
    "hsk5_486": [{"chinese": "这样做的后果很严重。", "pinyin": "Zhèyàng zuò de hòuguǒ hěn yánzhòng.", "meaningVi": "Hậu quả của việc làm như vậy rất nghiêm trọng."}],
    "hsk5_487": [{"chinese": "我们不能忽视这个问题。", "pinyin": "Wǒmen bù néng hūshì zhège wèntí.", "meaningVi": "Chúng ta không thể xem nhẹ vấn đề này."}],
    "hsk5_488": [{"chinese": "深呼吸可以帮助放松。", "pinyin": "Shēn hūxī kěyǐ bāngzhù fàngsōng.", "meaningVi": "Hít thở sâu có thể giúp thư giãn."}],
    "hsk5_489": [{"chinese": "这个湖很大。", "pinyin": "Zhège hú hěn dà.", "meaningVi": "Cái hồ này rất lớn."}],
    "hsk5_490": [{"chinese": "花园里飞着几只蝴蝶。", "pinyin": "Huāyuán lǐ fēizhe jǐ zhī húdié.", "meaningVi": "Trong vườn hoa có mấy con bướm đang bay."}],
    "hsk5_491": [{"chinese": "他住在一条老胡同里。", "pinyin": "Tā zhù zài yì tiáo lǎo hútòng lǐ.", "meaningVi": "Anh ấy sống trong một con hẻm cổ."}],
    "hsk5_492": [{"chinese": "主播和观众积极互动。", "pinyin": "Zhǔbō hé guānzhòng jījí hùdòng.", "meaningVi": "Người dẫn chương trình và khán giả tương tác tích cực."}],
    "hsk5_493": [{"chinese": "周末我们去户外运动吧。", "pinyin": "Zhōumò wǒmen qù hùwài yùndòng ba.", "meaningVi": "Cuối tuần chúng ta đi vận động ngoài trời đi."}],
    "hsk5_494": [{"chinese": "这次装修花费了不少钱。", "pinyin": "Zhè cì zhuāngxiū huāfèile bù shǎo qián.", "meaningVi": "Lần sửa nhà này đã tốn không ít tiền."}],
    "hsk5_498": [{"chinese": "我的话费用完了。", "pinyin": "Wǒ de huàfèi yòngwán le.", "meaningVi": "Cước điện thoại của tôi đã dùng hết."}],
    "hsk5_499": [{"chinese": "这部电影的画面很美。", "pinyin": "Zhè bù diànyǐng de huàmiàn hěn měi.", "meaningVi": "Hình ảnh của bộ phim này rất đẹp."}],
    "hsk5_500": [{"chinese": "这是大家都感兴趣的话题。", "pinyin": "Zhè shì dàjiā dōu gǎn xìngqù de huàtí.", "meaningVi": "Đây là chủ đề mà mọi người đều hứng thú."}],
    "hsk5_501": [{"chinese": "他化学考了满分。", "pinyin": "Tā huàxué kǎole mǎnfēn.", "meaningVi": "Anh ấy thi môn hóa học được điểm tuyệt đối."}],
    "hsk5_502": [{"chinese": "这是整个流程中最重要的环节。", "pinyin": "Zhè shì zhěnggè liúchéng zhōng zuì zhòngyào de huánjié.", "meaningVi": "Đây là khâu quan trọng nhất trong toàn bộ quy trình."}],
    "hsk5_503": [{"chinese": "运动可以缓解压力。", "pinyin": "Yùndòng kěyǐ huǎnjiě yālì.", "meaningVi": "Vận động có thể giảm nhẹ áp lực."}],
    "hsk5_504": [{"chinese": "老人走路的速度很缓慢。", "pinyin": "Lǎorén zǒulù de sùdù hěn huǎnmàn.", "meaningVi": "Tốc độ đi bộ của người già rất chậm."}],
    "hsk5_505": [{"chinese": "这盘凉拌黄瓜很好吃。", "pinyin": "Zhè pán liángbàn huángguā hěn hǎochī.", "meaningVi": "Đĩa dưa chuột trộn này rất ngon."}],
    "hsk5_506": [{"chinese": "金价上涨，很多人抢购黄金。", "pinyin": "Jīnjià shàngzhǎng, hěn duō rén qiǎnggòu huángjīn.", "meaningVi": "Giá vàng tăng, rất nhiều người đổ xô mua vàng."}],
    "hsk5_508": [{"chinese": "他向我们挥手告别。", "pinyin": "Tā xiàng wǒmen huīshǒu gàobié.", "meaningVi": "Anh ấy vẫy tay từ biệt chúng tôi."}],
    "hsk5_511": [{"chinese": "这些瓶子可以回收利用。", "pinyin": "Zhèxiē píngzi kěyǐ huíshōu lìyòng.", "meaningVi": "Những chai này có thể tái chế sử dụng."}],
    "hsk5_512": [{"chinese": "最近汇率变化很大。", "pinyin": "Zuìjìn huìlǜ biànhuà hěn dà.", "meaningVi": "Gần đây tỷ giá hối đoái biến động rất lớn."}],
    "hsk5_513": [{"chinese": "他们的婚礼办得很隆重。", "pinyin": "Tāmen de hūnlǐ bàn de hěn lóngzhòng.", "meaningVi": "Đám cưới của họ được tổ chức rất long trọng."}],
    "hsk5_514": [{"chinese": "他们一伙人去爬山了。", "pinyin": "Tāmen yì huǒ rén qù páshān le.", "meaningVi": "Cả bọn họ đã đi leo núi."}],
    "hsk5_515": [{"chinese": "他是我最好的合作伙伴。", "pinyin": "Tā shì wǒ zuì hǎo de hézuò huǒbàn.", "meaningVi": "Anh ấy là đối tác hợp tác tốt nhất của tôi."}],
    "hsk5_516": [{"chinese": "冬天吃火锅最舒服。", "pinyin": "Dōngtiān chī huǒguō zuì shūfu.", "meaningVi": "Mùa đông ăn lẩu là thoải mái nhất."}],
    "hsk5_518": [{"chinese": "仓库里堆满了货物。", "pinyin": "Cāngkù lǐ duīmǎnle huòwù.", "meaningVi": "Trong kho chất đầy hàng hóa."}],
    "hsk5_519": [{"chinese": "或许他明天会来。", "pinyin": "Huòxǔ tā míngtiān huì lái.", "meaningVi": "Có lẽ ngày mai anh ấy sẽ đến."}],
    "hsk5_520": [{"chinese": "这是一家教育机构。", "pinyin": "Zhè shì yì jiā jiàoyù jīgòu.", "meaningVi": "Đây là một tổ chức giáo dục."}],
    "hsk5_521": [{"chinese": "比赛非常激烈。", "pinyin": "Bǐsài fēicháng jīliè.", "meaningVi": "Trận đấu vô cùng kịch liệt."}],
    "hsk5_522": [{"chinese": "这台机器坏了。", "pinyin": "Zhè tái jīqì huài le.", "meaningVi": "Cái máy này bị hỏng rồi."}],
    "hsk5_523": [{"chinese": "这个机器人可以做家务。", "pinyin": "Zhège jīqìrén kěyǐ zuò jiāwù.", "meaningVi": "Con robot này có thể làm việc nhà."}],
    "hsk5_525": [{"chinese": "他的能力远远不及你。", "pinyin": "Tā de nénglì yuǎnyuǎn bùjí nǐ.", "meaningVi": "Năng lực của anh ấy còn kém xa bạn."}],
    "hsk5_528": [{"chinese": "早发现疾病有利于治疗。", "pinyin": "Zǎo fāxiàn jíbìng yǒulì yú zhìliáo.", "meaningVi": "Phát hiện bệnh sớm có lợi cho việc điều trị."}],
    "hsk5_529": [{"chinese": "他这次考试及格了。", "pinyin": "Tā zhè cì kǎoshì jígé le.", "meaningVi": "Lần thi này anh ấy đã đạt điểm qua."}],
    "hsk5_530": [{"chinese": "大家八点在门口集合。", "pinyin": "Dàjiā bā diǎn zài ménkǒu jíhé.", "meaningVi": "Mọi người tập hợp ở cửa lúc tám giờ."}],
    "hsk5_531": [{"chinese": "新学期即将开始。", "pinyin": "Xīn xuéqī jíjiāng kāishǐ.", "meaningVi": "Học kỳ mới sắp bắt đầu."}],
    "hsk5_532": [{"chinese": "他急忙跑出了教室。", "pinyin": "Tā jímáng pǎochūle jiàoshì.", "meaningVi": "Anh ấy vội vàng chạy ra khỏi lớp học."}],
    "hsk5_533": [{"chinese": "这件事极其重要。", "pinyin": "Zhè jiàn shì jíqí zhòngyào.", "meaningVi": "Việc này cực kỳ quan trọng."}],
    "hsk5_534": [{"chinese": "我们要有集体荣誉感。", "pinyin": "Wǒmen yào yǒu jítǐ róngyù gǎn.", "meaningVi": "Chúng ta phải có tinh thần danh dự tập thể."}],
    "hsk5_535": [{"chinese": "灾区急需救援物资。", "pinyin": "Zāiqū jíxū jiùyuán wùzī.", "meaningVi": "Vùng thiên tai đang cần gấp vật tư cứu trợ."}],
    "hsk5_540": [{"chinese": "这是第一季度的报告。", "pinyin": "Zhè shì dì-yī jìdù de bàogào.", "meaningVi": "Đây là báo cáo quý một."}],
    "hsk5_542": [{"chinese": "他打破了自己的纪录。", "pinyin": "Tā dǎpòle zìjǐ de jìlù.", "meaningVi": "Anh ấy đã phá kỷ lục của chính mình."}],
    "hsk5_543": [{"chinese": "我们看了一部关于海洋的纪录片。", "pinyin": "Wǒmen kànle yí bù guānyú hǎiyáng de jìlùpiàn.", "meaningVi": "Chúng tôi đã xem một bộ phim tài liệu về đại dương."}],
    "hsk5_544": [{"chinese": "他掌握了很多实用技能。", "pinyin": "Tā zhǎngwòle hěn duō shíyòng jìnéng.", "meaningVi": "Anh ấy đã nắm vững nhiều kỹ năng thực dụng."}],
    "hsk5_546": [{"chinese": "今天是我们的结婚纪念日。", "pinyin": "Jīntiān shì wǒmen de jiéhūn jìniànrì.", "meaningVi": "Hôm nay là ngày kỷ niệm kết hôn của chúng tôi."}],
    "hsk5_547": [{"chinese": "请帮我计算一下总数。", "pinyin": "Qǐng bāng wǒ jìsuàn yíxià zǒngshù.", "meaningVi": "Xin giúp tôi tính tổng số."}],
    "hsk5_548": [{"chinese": "他在学习计算机专业。", "pinyin": "Tā zài xuéxí jìsuànjī zhuānyè.", "meaningVi": "Anh ấy đang học chuyên ngành máy tính."}],
    "hsk5_550": [{"chinese": "历史书上记载了这件事。", "pinyin": "Lìshǐ shū shàng jìzǎile zhè jiàn shì.", "meaningVi": "Sách lịch sử đã ghi chép lại sự việc này."}],
    "hsk5_551": [{"chinese": "今晚的嘉宾是一位著名演员。", "pinyin": "Jīnwǎn de jiābīn shì yí wèi zhùmíng yǎnyuán.", "meaningVi": "Khách mời tối nay là một diễn viên nổi tiếng."}],
    "hsk5_552": [{"chinese": "这家店专卖家电。", "pinyin": "Zhè jiā diàn zhuānmài jiādiàn.", "meaningVi": "Cửa hàng này chuyên bán đồ điện gia dụng."}],
    "hsk5_553": [{"chinese": "这些原材料需要进一步加工。", "pinyin": "Zhèxiē yuáncáiliào xūyào jìnyíbù jiāgōng.", "meaningVi": "Những nguyên liệu này cần được gia công thêm."}],
    "hsk5_554": [{"chinese": "请把牛奶加热一下。", "pinyin": "Qǐng bǎ niúnǎi jiārè yíxià.", "meaningVi": "Xin hâm nóng sữa một chút."}],
    "hsk5_555": [{"chinese": "这次旅行加深了我们的友谊。", "pinyin": "Zhè cì lǚxíng jiāshēnle wǒmen de yǒuyì.", "meaningVi": "Chuyến du lịch lần này đã làm sâu thêm tình bạn của chúng tôi."}],
    "hsk5_556": [{"chinese": "汽车开始加速。", "pinyin": "Qìchē kāishǐ jiāsù.", "meaningVi": "Ô tô bắt đầu tăng tốc."}],
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
