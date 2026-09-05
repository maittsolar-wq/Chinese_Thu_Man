"""P5.10.3 (continued) -- Batch 028 (continues immediately after
examples_batch_027.json; entirely within HSK6, hsk6_1197-hsk6_1498).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Numeric-suffix homograph records (needs_review) ***
One record in this batch carries the HSK6 numeric-suffix homograph
pattern (see batch 024's 乘2, batch 025's 副2/该2, batch 026's
局1/局2/料1/料2/露1, and batch 027's 升2 for the full explanation):
所2 (hsk6_1254). The literal string "所2" can never appear in natural
Chinese text, so it is left with an empty examples list and qaStatus
"needs_review", per the established rule. Production record
untouched. Two further such records remain later in HSK6 (则1, 支2)
and will need identical treatment when reached.

*** Continuing extremely dense homophone/polyphonic clusters ***
None of the pairs below are flagged by the mechanical tier system (it
compares the `word` string, and every pair is a different word), but
all required deliberate disambiguation:
  - shì (4th tone): 适度/示范/释放/事后/视觉/试图/事务/事项/适宜 --
    nine members, plus 势力 and 视力, which are BOTH shìlì (identical
    pinyin+tone, different characters: 势力 "influence/power" vs 视力
    "eyesight") -- given deliberately distinct natural contexts.
  - 率 polyphonic: 率领/率先 read SHUÀI (4th tone, "to lead/be first")
    here, NOT the lǜ reading used elsewhere in the pipeline for 频率/
    概率 ("rate/frequency") -- genuinely different tone for the same
    character, kept distinct.
  - tè (4th tone): 特/特长/特地/特定/特性/特意 -- six members, same
    character 特 in different compounds.
  - tiān (1st tone): 添/天才/添加/天然/天然气/天文/天下/天真 --
    eight members, two different characters (添/天).
  - tōng (1st tone): 通道/通风/通话/通用 plus the near-synonym pair
    通信/通讯 (both "communication/telecommunications") -- given
    deliberately distinct natural contexts (卫星通信技术 "satellite
    communication technology" vs 现场通讯 "on-site news dispatch") to
    keep them semantically distinguishable despite their overlap.
  - tuō (1st tone) polyphonic pair: 拖 ("to drag/pull") and 托 (in
    托运, "to check in luggage") share the SAME pinyin+tone but are
    different characters -- kept distinct.
  - wéi/wèi polyphonic 为: 为难/为期/为止 all read WÉI (2nd tone, "to
    do/act/serve as") while 为此/为何 read WÈI (4th tone, "for/
    because of") -- genuinely different tones for the same character,
    all five given distinct natural contexts to keep both readings
    and all three wéi-compounds unambiguous.
  - wén (2nd tone): 文档/文具/文科/文物/文献/文艺 -- six members,
    plus 文明 and 闻名, which are BOTH wénmíng (identical pinyin+
    tone, different characters: 文明 "civilization" vs 闻名 "to be
    famous/well-known") -- given deliberately distinct natural
    contexts.
  - xiàn (4th tone): 现存/现货/陷入/线索 plus 限度 and 限于, both of
    which use the same character 限 in different compounds -- kept to
    distinct natural contexts.
  - xiāng/xiàng polyphonic 相: 相差/相传/相等/相连/相应 read XIĀNG
    (1st tone) while 相声 reads XIÀNG (4th tone, "comic dialogue") --
    genuinely different tone for the same character, kept distinct.
  - xīn (1st tone): the largest cluster in this batch -- 心爱/心底/
    新款/心灵/新媒体/心目/新能源/薪水/心疼/新兴/新颖/心愿/心脏 --
    thirteen members across three different characters (心/新/薪).

Fix applied after the first validator pass (caught by
validate_examples_batch_p103.py's no_duplicate_sentences_across_
pilot_and_batches check): 团结 (tuánjié)'s first draft "团结就是
力量。" was an EXACT duplicate of an already-published sentence
elsewhere in the corpus (a common idiom). Rewritten to "全班同学都很
团结。".

Near-template fixes (character-bigram Jaccard >= 0.55 against the
full pilot+002-027 corpus, caught by the independent script-level
check, not the validator): six flags, all fixed by diverging sentence
structure while preserving natural, correct usage:
  - 收藏 vs hsk5_1044's "他喜欢收集邮票。" (near-synonym 收藏/收集 in
    an otherwise identical clause) -> "这位老人收藏了上千枚邮票。".
  - 铜牌 vs batch 026's hsk6_0623 "他获得了这次比赛的季军。" (both
    used the "他获得了这次比赛的...。" template) -> "这枚铜牌是他
    多年努力的见证。".
  - 为此 vs batch 027's hsk6_1174 "他为升学付出了很多努力。" (both
    used the "他为...付出了很多努力。" template) -> "为此，公司调整
    了整体战略。".
  - 文档 vs hsk3_445's "请把文件发到我的邮箱。" (near-synonym 文档/
    文件 in an otherwise identical clause) -> "这份文档还需要进一步
    修改。".
  - 文艺 vs hsk3_371's "学校举办了一场晚会。" (both used the "学校
    举办了一场...晚会。" template) -> "这场文艺演出深受观众喜爱。".
  - 心愿 vs hsk5_1020's "他终于实现了自己的梦想。" (both used the
    "他终于实现了自己的...。" template) -> "这个心愿藏在她心里很多
    年了。".
Re-verified after these fixes: zero cross-corpus flags, zero
within-batch flags (see validation report).

All re-verified against the full pilot+002-027 corpus with zero
remaining exact duplicates and zero near-template flags (see
validation report).

Usage:
    python generate_examples_batch_028.py --dry-run
    python generate_examples_batch_028.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 28
BATCH_SIZE = 300
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_028.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

# Records deliberately left with 0 examples (see module docstring):
# HSK6's numeric-suffix homograph pattern makes the literal target
# word unmatchable in natural Chinese text.
NEEDS_REVIEW_IDS = {"hsk6_1254"}

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk6_1197": [{"chinese": "运动要适度，不要过量。", "pinyin": "Yùndòng yào shìdù, búyào guòliàng.", "meaningVi": "Vận động phải vừa phải, đừng quá mức."}],
    "hsk6_1198": [{"chinese": "老师给学生做了示范。", "pinyin": "Lǎoshī gěi xuésheng zuòle shìfàn.", "meaningVi": "Giáo viên đã làm mẫu cho học sinh."}],
    "hsk6_1199": [{"chinese": "运动可以释放压力。", "pinyin": "Yùndòng kěyǐ shìfàng yālì.", "meaningVi": "Vận động có thể giải tỏa áp lực."}],
    "hsk6_1200": [{"chinese": "他事后才意识到自己的错误。", "pinyin": "Tā shìhòu cái yìshí dào zìjǐ de cuòwù.", "meaningVi": "Sau đó anh ấy mới nhận ra lỗi lầm của mình."}],
    "hsk6_1201": [{"chinese": "这部电影带来了强烈的视觉冲击。", "pinyin": "Zhè bù diànyǐng dàiláile qiángliè de shìjué chōngjī.", "meaningVi": "Bộ phim này mang lại hiệu ứng thị giác mạnh mẽ."}],
    "hsk6_1202": [{"chinese": "这个组织的势力越来越大。", "pinyin": "Zhège zǔzhī de shìlì yuè lái yuè dà.", "meaningVi": "Thế lực của tổ chức này ngày càng lớn."}],
    "hsk6_1203": [{"chinese": "他的视力下降了。", "pinyin": "Tā de shìlì xiàjiàng le.", "meaningVi": "Thị lực của anh ấy đã giảm sút."}],
    "hsk6_1204": [{"chinese": "他试图说服大家。", "pinyin": "Tā shìtú shuōfú dàjiā.", "meaningVi": "Anh ấy cố gắng thuyết phục mọi người."}],
    "hsk6_1205": [{"chinese": "他每天要处理很多事务。", "pinyin": "Tā měitiān yào chǔlǐ hěn duō shìwù.", "meaningVi": "Mỗi ngày anh ấy phải xử lý rất nhiều công việc."}],
    "hsk6_1206": [{"chinese": "请注意以下几点注意事项。", "pinyin": "Qǐng zhùyì yǐxià jǐ diǎn zhùyì shìxiàng.", "meaningVi": "Xin chú ý mấy điểm lưu ý sau đây."}],
    "hsk6_1207": [{"chinese": "这里的气候十分适宜居住。", "pinyin": "Zhèlǐ de qìhòu shífēn shìyí jūzhù.", "meaningVi": "Khí hậu nơi đây vô cùng thích hợp để sinh sống."}],
    "hsk6_1208": [{"chinese": "这位老人收藏了上千枚邮票。", "pinyin": "Zhè wèi lǎorén shōucángle shàng qiān méi yóupiào.", "meaningVi": "Cụ già này đã sưu tầm hàng nghìn con tem."}],
    "hsk6_1209": [{"chinese": "这家公司被另一家企业收购了。", "pinyin": "Zhè jiā gōngsī bèi lìng yì jiā qǐyè shōugòu le.", "meaningVi": "Công ty này đã bị một doanh nghiệp khác mua lại."}],
    "hsk6_1210": [{"chinese": "银行收取一定的手续费。", "pinyin": "Yínháng shōuqǔ yídìng de shǒuxùfèi.", "meaningVi": "Ngân hàng thu một khoản phí thủ tục nhất định."}],
    "hsk6_1211": [{"chinese": "这项投资带来了不错的收益。", "pinyin": "Zhè xiàng tóuzī dàiláile búcuò de shōuyì.", "meaningVi": "Khoản đầu tư này đã mang lại lợi nhuận khá tốt."}],
    "hsk6_1212": [{"chinese": "她的手臂受伤了。", "pinyin": "Tā de shǒubì shòushāng le.", "meaningVi": "Cánh tay của cô ấy bị thương."}],
    "hsk6_1213": [{"chinese": "这幅画运用了独特的绘画手法。", "pinyin": "Zhè fú huà yùnyòngle dútè de huìhuà shǒufǎ.", "meaningVi": "Bức tranh này sử dụng thủ pháp hội họa độc đáo."}],
    "hsk6_1214": [{"chinese": "他用手势示意大家安静。", "pinyin": "Tā yòng shǒushì shìyì dàjiā ānjìng.", "meaningVi": "Anh ấy ra hiệu bằng cử chỉ tay cho mọi người im lặng."}],
    "hsk6_1215": [{"chinese": "安全是首要问题。", "pinyin": "Ānquán shì shǒuyào wèntí.", "meaningVi": "An toàn là vấn đề hàng đầu."}],
    "hsk6_1216": [{"chinese": "这种电池的寿命比较长。", "pinyin": "Zhè zhǒng diànchí de shòumìng bǐjiào cháng.", "meaningVi": "Tuổi thọ của loại pin này khá dài."}],
    "hsk6_1217": [{"chinese": "这个村子受灾严重。", "pinyin": "Zhège cūnzi shòuzāi yánzhòng.", "meaningVi": "Ngôi làng này chịu thiên tai nghiêm trọng."}],
    "hsk6_1218": [{"chinese": "这台机器每小时输出一百件产品。", "pinyin": "Zhè tái jīqì měi xiǎoshí shūchū yìbǎi jiàn chǎnpǐn.", "meaningVi": "Cỗ máy này mỗi giờ xuất ra một trăm sản phẩm."}],
    "hsk6_1219": [{"chinese": "他喜欢收藏名家书画。", "pinyin": "Tā xǐhuan shōucáng míngjiā shūhuà.", "meaningVi": "Anh ấy thích sưu tầm thư họa của các danh gia."}],
    "hsk6_1220": [{"chinese": "图书馆里有各种各样的书籍。", "pinyin": "Túshūguǎn lǐ yǒu gèzhǒng-gèyàng de shūjí.", "meaningVi": "Trong thư viện có đủ loại sách."}],
    "hsk6_1221": [{"chinese": "请提交一份书面申请。", "pinyin": "Qǐng tíjiāo yí fèn shūmiàn shēnqǐng.", "meaningVi": "Xin nộp một bản đơn xin bằng văn bản."}],
    "hsk6_1222": [{"chinese": "管道负责输送石油。", "pinyin": "Guǎndào fùzé shūsòng shíyóu.", "meaningVi": "Đường ống chịu trách nhiệm vận chuyển dầu mỏ."}],
    "hsk6_1223": [{"chinese": "他用毛笔书写了这幅字。", "pinyin": "Tā yòng máobǐ shūxiěle zhè fú zì.", "meaningVi": "Anh ấy đã dùng bút lông viết bức thư pháp này."}],
    "hsk6_1224": [{"chinese": "我属虎。", "pinyin": "Wǒ shǔ hǔ.", "meaningVi": "Tôi tuổi Hổ."}],
    "hsk6_1225": [{"chinese": "他一边看电视一边吃薯片。", "pinyin": "Tā yìbiān kàn diànshì yìbiān chī shǔpiàn.", "meaningVi": "Anh ấy vừa xem tivi vừa ăn khoai tây chiên."}],
    "hsk6_1226": [{"chinese": "请把这块木板竖起来。", "pinyin": "Qǐng bǎ zhè kuài mùbǎn shù qǐlai.", "meaningVi": "Xin dựng đứng tấm ván này lên."}],
    "hsk6_1227": [{"chinese": "他为大家树立了榜样。", "pinyin": "Tā wèi dàjiā shùlìle bǎngyàng.", "meaningVi": "Anh ấy đã làm gương cho mọi người."}],
    "hsk6_1228": [{"chinese": "参加比赛的人数目不小。", "pinyin": "Cānjiā bǐsài de rén shùmù bù xiǎo.", "meaningVi": "Số lượng người tham gia cuộc thi không nhỏ."}],
    "hsk6_1229": [{"chinese": "公司正在推进数字化转型。", "pinyin": "Gōngsī zhèngzài tuījìn shùzìhuà zhuǎnxíng.", "meaningVi": "Công ty đang thúc đẩy chuyển đổi số."}],
    "hsk6_1230": [{"chinese": "他明显比同龄人衰老得快。", "pinyin": "Tā míngxiǎn bǐ tónglíngrén shuāilǎo de kuài.", "meaningVi": "Anh ấy rõ ràng già đi nhanh hơn người cùng tuổi."}],
    "hsk6_1231": [{"chinese": "队长率领大家完成了任务。", "pinyin": "Duìzhǎng shuàilǐng dàjiā wánchéngle rènwu.", "meaningVi": "Đội trưởng đã dẫn dắt mọi người hoàn thành nhiệm vụ."}],
    "hsk6_1232": [{"chinese": "他率先举手发言。", "pinyin": "Tā shuàixiān jǔshǒu fāyán.", "meaningVi": "Anh ấy giơ tay phát biểu đầu tiên."}],
    "hsk6_1233": [{"chinese": "农民正在收割水稻。", "pinyin": "Nóngmín zhèngzài shōugē shuǐdào.", "meaningVi": "Nông dân đang gặt lúa nước."}],
    "hsk6_1234": [{"chinese": "这座水库为周边地区提供用水。", "pinyin": "Zhè zuò shuǐkù wèi zhōubiān dìqū tígōng yòngshuǐ.", "meaningVi": "Hồ chứa nước này cung cấp nước cho các khu vực lân cận."}],
    "hsk6_1235": [{"chinese": "这里的水流十分湍急。", "pinyin": "Zhèlǐ de shuǐliú shífēn tuānjí.", "meaningVi": "Dòng nước ở đây chảy xiết vô cùng."}],
    "hsk6_1236": [{"chinese": "一只小船漂在水面上。", "pinyin": "Yì zhī xiǎochuán piāo zài shuǐmiàn shàng.", "meaningVi": "Một chiếc thuyền nhỏ trôi trên mặt nước."}],
    "hsk6_1237": [{"chinese": "工人正在搅拌水泥。", "pinyin": "Gōngrén zhèngzài jiǎobàn shuǐní.", "meaningVi": "Công nhân đang trộn xi măng."}],
    "hsk6_1238": [{"chinese": "那一瞬间，他终于明白了。", "pinyin": "Nà yí shùnjiān, tā zhōngyú míngbai le.", "meaningVi": "Khoảnh khắc đó, cuối cùng anh ấy cũng hiểu ra."}],
    "hsk6_1239": [{"chinese": "他的思路很清晰。", "pinyin": "Tā de sīlù hěn qīngxī.", "meaningVi": "Tư duy của anh ấy rất rõ ràng."}],
    "hsk6_1240": [{"chinese": "她十分思念故乡。", "pinyin": "Tā shífēn sīniàn gùxiāng.", "meaningVi": "Cô ấy vô cùng nhớ nhung quê hương."}],
    "hsk6_1241": [{"chinese": "这种疾病的死亡率很低。", "pinyin": "Zhè zhǒng jíbìng de sǐwánglǜ hěn dī.", "meaningVi": "Tỷ lệ tử vong của căn bệnh này rất thấp."}],
    "hsk6_1242": [{"chinese": "请把绳子松一松。", "pinyin": "Qǐng bǎ shéngzi sōng yi sōng.", "meaningVi": "Xin nới lỏng sợi dây một chút."}],
    "hsk6_1243": [{"chinese": "港口停靠着几艘轮船。", "pinyin": "Gǎngkǒu tíngkàozhe jǐ sōu lúnchuán.", "meaningVi": "Tại cảng đang neo đậu vài chiếc tàu thủy."}],
    "hsk6_1244": [{"chinese": "他正在搜集相关资料。", "pinyin": "Tā zhèngzài sōují xiāngguān zīliào.", "meaningVi": "Anh ấy đang thu thập tài liệu liên quan."}],
    "hsk6_1245": [{"chinese": "这部小说塑造了一个鲜明的人物形象。", "pinyin": "Zhè bù xiǎoshuō sùzàole yí gè xiānmíng de rénwù xíngxiàng.", "meaningVi": "Cuốn tiểu thuyết này đã xây dựng nên một hình tượng nhân vật nổi bật."}],
    "hsk6_1246": [{"chinese": "提高国民素质十分重要。", "pinyin": "Tígāo guómín sùzhì shífēn zhòngyào.", "meaningVi": "Nâng cao tố chất của người dân vô cùng quan trọng."}],
    "hsk6_1247": [{"chinese": "算了，别再提这件事了。", "pinyin": "Suànle, bié zài tí zhè jiàn shì le.", "meaningVi": "Thôi bỏ đi, đừng nhắc lại chuyện này nữa."}],
    "hsk6_1248": [{"chinese": "这次表现总算是不错了。", "pinyin": "Zhè cì biǎoxiàn zǒngsuàn shì búcuò le.", "meaningVi": "Lần này thể hiện coi như là khá tốt rồi."}],
    "hsk6_1249": [{"chinese": "他虽年轻，却很有经验。", "pinyin": "Tā suī niánqīng, què hěn yǒu jīngyàn.", "meaningVi": "Anh ấy tuy còn trẻ, nhưng lại rất có kinh nghiệm."}],
    "hsk6_1250": [{"chinese": "您今年多大岁数了？", "pinyin": "Nín jīnnián duō dà suìshu le?", "meaningVi": "Năm nay bác bao nhiêu tuổi rồi?"}],
    "hsk6_1251": [{"chinese": "岁月不饶人。", "pinyin": "Suìyuè bù ráo rén.", "meaningVi": "Năm tháng không tha cho ai."}],
    "hsk6_1252": [{"chinese": "这台电脑已经损坏了。", "pinyin": "Zhè tái diànnǎo yǐjīng sǔnhuài le.", "meaningVi": "Cái máy tính này đã bị hỏng."}],
    "hsk6_1253": [{"chinese": "长期熬夜会损伤身体。", "pinyin": "Chángqī áoyè huì sǔnshāng shēntǐ.", "meaningVi": "Thức khuya lâu dài sẽ tổn hại cơ thể."}],
    "hsk6_1254": [],
    "hsk6_1255": [{"chinese": "他工作起来很踏实。", "pinyin": "Tā gōngzuò qǐlai hěn tāshi.", "meaningVi": "Anh ấy làm việc rất chắc chắn ổn định."}],
    "hsk6_1256": [{"chinese": "远处有一座古塔。", "pinyin": "Yuǎnchù yǒu yí zuò gǔtǎ.", "meaningVi": "Ở đằng xa có một ngôi tháp cổ."}],
    "hsk6_1257": [{"chinese": "台风即将登陆。", "pinyin": "Táifēng jíjiāng dēnglù.", "meaningVi": "Bão sắp đổ bộ."}],
    "hsk6_1258": [{"chinese": "他晚上常去打台球。", "pinyin": "Tā wǎnshang cháng qù dǎ táiqiú.", "meaningVi": "Buổi tối anh ấy thường đi chơi bi-a."}],
    "hsk6_1259": [{"chinese": "宇航员在太空中生活了半年。", "pinyin": "Yǔhángyuán zài tàikōng zhōng shēnghuóle bànnián.", "meaningVi": "Phi hành gia đã sống nửa năm trong vũ trụ."}],
    "hsk6_1260": [{"chinese": "这栋房子安装了太阳能板。", "pinyin": "Zhè dòng fángzi ānzhuāngle tàiyángnéng bǎn.", "meaningVi": "Ngôi nhà này đã lắp đặt tấm pin năng lượng mặt trời."}],
    "hsk6_1261": [{"chinese": "大家都在谈论这条新闻。", "pinyin": "Dàjiā dōu zài tánlùn zhè tiáo xīnwén.", "meaningVi": "Mọi người đều đang bàn luận về tin tức này."}],
    "hsk6_1262": [{"chinese": "双方正在进行谈判。", "pinyin": "Shuāngfāng zhèngzài jìnxíng tánpàn.", "meaningVi": "Hai bên đang tiến hành đàm phán."}],
    "hsk6_1263": [{"chinese": "这种材料很有弹性。", "pinyin": "Zhè zhǒng cáiliào hěn yǒu tánxìng.", "meaningVi": "Loại vật liệu này rất có tính đàn hồi."}],
    "hsk6_1264": [{"chinese": "人类一直在探索宇宙的奥秘。", "pinyin": "Rénlèi yìzhí zài tànsuǒ yǔzhòu de àomì.", "meaningVi": "Loài người luôn khám phá những bí ẩn của vũ trụ."}],
    "hsk6_1265": [{"chinese": "我们需要进一步探讨这个问题。", "pinyin": "Wǒmen xūyào jìnyíbù tàntǎo zhège wèntí.", "meaningVi": "Chúng ta cần thảo luận sâu hơn về vấn đề này."}],
    "hsk6_1266": [{"chinese": "元宵节大家都要吃汤圆。", "pinyin": "Yuánxiāojié dàjiā dōu yào chī tāngyuán.", "meaningVi": "Tết Nguyên Tiêu mọi người đều phải ăn bánh trôi."}],
    "hsk6_1267": [{"chinese": "孩子们喜欢吃糖果。", "pinyin": "Háizimen xǐhuan chī tángguǒ.", "meaningVi": "Bọn trẻ thích ăn kẹo."}],
    "hsk6_1268": [{"chinese": "小心，汤很烫。", "pinyin": "Xiǎoxīn, tāng hěn tàng.", "meaningVi": "Cẩn thận, canh nóng lắm."}],
    "hsk6_1269": [{"chinese": "他从口袋里掏出了钥匙。", "pinyin": "Tā cóng kǒudai lǐ tāochūle yàoshi.", "meaningVi": "Anh ấy lấy chìa khóa ra từ trong túi."}],
    "hsk6_1270": [{"chinese": "犯人已经逃走了。", "pinyin": "Fànrén yǐjīng táozǒu le.", "meaningVi": "Tên tội phạm đã bỏ trốn rồi."}],
    "hsk6_1271": [{"chinese": "小偷见状立刻逃跑了。", "pinyin": "Xiǎotōu jiàn zhuàng lìkè táopǎo le.", "meaningVi": "Tên trộm thấy vậy lập tức bỏ chạy."}],
    "hsk6_1272": [{"chinese": "这个孩子非常淘气。", "pinyin": "Zhège háizi fēicháng táoqì.", "meaningVi": "Đứa trẻ này vô cùng nghịch ngợm."}],
    "hsk6_1273": [{"chinese": "落后的技术终将被淘汰。", "pinyin": "Luòhòu de jìshù zhōng jiāng bèi táotài.", "meaningVi": "Công nghệ lạc hậu cuối cùng sẽ bị đào thải."}],
    "hsk6_1274": [{"chinese": "我点了一份午餐套餐。", "pinyin": "Wǒ diǎnle yí fèn wǔcān tàocān.", "meaningVi": "Tôi đã gọi một suất combo bữa trưa."}],
    "hsk6_1275": [{"chinese": "这份工作特累。", "pinyin": "Zhè fèn gōngzuò tè lèi.", "meaningVi": "Công việc này đặc biệt mệt."}],
    "hsk6_1276": [{"chinese": "音乐是他的特长。", "pinyin": "Yīnyuè shì tā de tècháng.", "meaningVi": "Âm nhạc là sở trường của anh ấy."}],
    "hsk6_1277": [{"chinese": "她特地为我准备了礼物。", "pinyin": "Tā tèdì wèi wǒ zhǔnbèile lǐwù.", "meaningVi": "Cô ấy đặc biệt chuẩn bị quà cho tôi."}],
    "hsk6_1278": [{"chinese": "这项政策只适用于特定人群。", "pinyin": "Zhè xiàng zhèngcè zhǐ shìyòng yú tèdìng rénqún.", "meaningVi": "Chính sách này chỉ áp dụng cho nhóm người cụ thể."}],
    "hsk6_1279": [{"chinese": "每种材料都有自己的特性。", "pinyin": "Měi zhǒng cáiliào dōu yǒu zìjǐ de tèxìng.", "meaningVi": "Mỗi loại vật liệu đều có đặc tính riêng."}],
    "hsk6_1280": [{"chinese": "他特意赶来参加婚礼。", "pinyin": "Tā tèyì gǎnlái cānjiā hūnlǐ.", "meaningVi": "Anh ấy đặc biệt vội đến tham dự đám cưới."}],
    "hsk6_1281": [{"chinese": "这部电影的题材十分新颖。", "pinyin": "Zhè bù diànyǐng de tícái shífēn xīnyǐng.", "meaningVi": "Đề tài của bộ phim này vô cùng mới lạ."}],
    "hsk6_1282": [{"chinese": "请到柜台提取现金。", "pinyin": "Qǐng dào guìtái tíqǔ xiànjīn.", "meaningVi": "Xin đến quầy để rút tiền mặt."}],
    "hsk6_1283": [{"chinese": "系统弹出了一个提示。", "pinyin": "Xìtǒng tánchūle yí gè tíshì.", "meaningVi": "Hệ thống đã hiện ra một gợi ý."}],
    "hsk6_1284": [{"chinese": "她从小练习体操。", "pinyin": "Tā cóngxiǎo liànxí tǐcāo.", "meaningVi": "Cô ấy từ nhỏ đã luyện tập thể dục dụng cụ."}],
    "hsk6_1285": [{"chinese": "这个箱子的体积很大。", "pinyin": "Zhège xiāngzi de tǐjī hěn dà.", "meaningVi": "Thể tích của cái hộp này rất lớn."}],
    "hsk6_1286": [{"chinese": "公司建立了完善的管理体系。", "pinyin": "Gōngsī jiànlìle wánshàn de guǎnlǐ tǐxì.", "meaningVi": "Công ty đã xây dựng hệ thống quản lý hoàn thiện."}],
    "hsk6_1287": [{"chinese": "请给我添点儿茶。", "pinyin": "Qǐng gěi wǒ tiān diǎnr chá.", "meaningVi": "Xin rót thêm cho tôi chút trà."}],
    "hsk6_1288": [{"chinese": "大家都说他是个天才。", "pinyin": "Dàjiā dōu shuō tā shì gè tiāncái.", "meaningVi": "Mọi người đều nói anh ấy là một thiên tài."}],
    "hsk6_1289": [{"chinese": "这款饮料没有添加任何色素。", "pinyin": "Zhè kuǎn yǐnliào méiyǒu tiānjiā rènhé sèsù.", "meaningVi": "Loại đồ uống này không thêm bất kỳ phẩm màu nào."}],
    "hsk6_1290": [{"chinese": "这种材料是天然形成的。", "pinyin": "Zhè zhǒng cáiliào shì tiānrán xíngchéng de.", "meaningVi": "Loại vật liệu này được hình thành tự nhiên."}],
    "hsk6_1291": [{"chinese": "家里改用天然气做饭了。", "pinyin": "Jiālǐ gǎiyòng tiānránqì zuòfàn le.", "meaningVi": "Nhà đã chuyển sang dùng khí tự nhiên để nấu ăn."}],
    "hsk6_1292": [{"chinese": "他从小就对天文感兴趣。", "pinyin": "Tā cóngxiǎo jiù duì tiānwén gǎn xìngqù.", "meaningVi": "Anh ấy từ nhỏ đã có hứng thú với thiên văn."}],
    "hsk6_1293": [{"chinese": "这道菜堪称天下第一。", "pinyin": "Zhè dào cài kānchēng tiānxià dì-yī.", "meaningVi": "Món ăn này xứng đáng là số một thiên hạ."}],
    "hsk6_1294": [{"chinese": "孩子的想法总是那么天真。", "pinyin": "Háizi de xiǎngfǎ zǒngshì nàme tiānzhēn.", "meaningVi": "Suy nghĩ của trẻ con luôn ngây thơ như vậy."}],
    "hsk6_1295": [{"chinese": "农民在田里种庄稼。", "pinyin": "Nóngmín zài tián lǐ zhòng zhuāngjia.", "meaningVi": "Nông dân trồng hoa màu trên ruộng."}],
    "hsk6_1296": [{"chinese": "他是一名田径运动员。", "pinyin": "Tā shì yì míng tiánjìng yùndòngyuán.", "meaningVi": "Anh ấy là một vận động viên điền kinh."}],
    "hsk6_1297": [{"chinese": "空调可以调节室内温度。", "pinyin": "Kōngtiáo kěyǐ tiáojié shìnèi wēndù.", "meaningVi": "Điều hòa có thể điều chỉnh nhiệt độ trong phòng."}],
    "hsk6_1298": [{"chinese": "她是一名跳水运动员。", "pinyin": "Tā shì yì míng tiàoshuǐ yùndòngyuán.", "meaningVi": "Cô ấy là một vận động viên nhảy cầu."}],
    "hsk6_1299": [{"chinese": "这些故事贴近百姓的生活。", "pinyin": "Zhèxiē gùshi tiējìn bǎixìng de shēnghuó.", "meaningVi": "Những câu chuyện này gần gũi với cuộc sống của người dân."}],
    "hsk6_1300": [{"chinese": "这个孩子从小就很听话。", "pinyin": "Zhège háizi cóngxiǎo jiù hěn tīnghuà.", "meaningVi": "Đứa trẻ này từ nhỏ đã rất ngoan."}],
    "hsk6_1301": [{"chinese": "老年人的听觉逐渐减退。", "pinyin": "Lǎoniánrén de tīngjué zhújiàn jiǎntuì.", "meaningVi": "Thính giác của người già dần suy giảm."}],
    "hsk6_1302": [{"chinese": "领导认真听取了大家的意见。", "pinyin": "Lǐngdǎo rènzhēn tīngqǔle dàjiā de yìjiàn.", "meaningVi": "Lãnh đạo đã nghiêm túc lắng nghe ý kiến của mọi người."}],
    "hsk6_1303": [{"chinese": "请走这条安全通道。", "pinyin": "Qǐng zǒu zhè tiáo ānquán tōngdào.", "meaningVi": "Xin đi theo lối thoát hiểm này."}],
    "hsk6_1304": [{"chinese": "请打开窗户让房间通风。", "pinyin": "Qǐng dǎkāi chuānghu ràng fángjiān tōngfēng.", "meaningVi": "Xin mở cửa sổ cho phòng thông gió."}],
    "hsk6_1305": [{"chinese": "他正在和客户通话。", "pinyin": "Tā zhèngzài hé kèhù tōnghuà.", "meaningVi": "Anh ấy đang gọi điện với khách hàng."}],
    "hsk6_1306": [{"chinese": "卫星通信技术不断发展。", "pinyin": "Wèixīng tōngxìn jìshù búduàn fāzhǎn.", "meaningVi": "Công nghệ thông tin liên lạc vệ tinh không ngừng phát triển."}],
    "hsk6_1307": [{"chinese": "记者发回了一篇现场通讯。", "pinyin": "Jìzhě fāhuíle yì piān xiànchǎng tōngxùn.", "meaningVi": "Phóng viên đã gửi về một bài tường thuật tại hiện trường."}],
    "hsk6_1308": [{"chinese": "这个零件在多个型号中通用。", "pinyin": "Zhège língjiàn zài duō gè xínghào zhōng tōngyòng.", "meaningVi": "Linh kiện này dùng chung được cho nhiều mẫu mã."}],
    "hsk6_1309": [{"chinese": "这枚硬币是用铜做的。", "pinyin": "Zhè méi yìngbì shì yòng tóng zuò de.", "meaningVi": "Đồng xu này được làm bằng đồng."}],
    "hsk6_1310": [{"chinese": "他和同伴一起完成了任务。", "pinyin": "Tā hé tóngbàn yìqǐ wánchéngle rènwu.", "meaningVi": "Anh ấy đã cùng bạn đồng hành hoàn thành nhiệm vụ."}],
    "hsk6_1311": [{"chinese": "他和几位同行交流了经验。", "pinyin": "Tā hé jǐ wèi tóngháng jiāoliúle jīngyàn.", "meaningVi": "Anh ấy đã trao đổi kinh nghiệm với vài đồng nghiệp."}],
    "hsk6_1312": [{"chinese": "妈妈每晚都给孩子讲童话。", "pinyin": "Māma měi wǎn dōu gěi háizi jiǎng tónghuà.", "meaningVi": "Mỗi tối mẹ đều kể chuyện cổ tích cho con nghe."}],
    "hsk6_1313": [{"chinese": "这两种产品属于同类商品。", "pinyin": "Zhè liǎng zhǒng chǎnpǐn shǔyú tónglèi shāngpǐn.", "meaningVi": "Hai loại sản phẩm này thuộc cùng một loại hàng hóa."}],
    "hsk6_1314": [{"chinese": "这枚铜牌是他多年努力的见证。", "pinyin": "Zhè méi tóngpái shì tā duō nián nǔlì de jiànzhèng.", "meaningVi": "Tấm huy chương đồng này là minh chứng cho nỗ lực nhiều năm của anh ấy."}],
    "hsk6_1315": [{"chinese": "大家玩得很痛快。", "pinyin": "Dàjiā wán de hěn tòngkuài.", "meaningVi": "Mọi người chơi rất thỏa thích."}],
    "hsk6_1316": [{"chinese": "有人偷了他的钱包。", "pinyin": "Yǒu rén tōule tā de qiánbāo.", "meaningVi": "Có người đã lấy trộm ví tiền của anh ấy."}],
    "hsk6_1317": [{"chinese": "他偷偷地溜出了教室。", "pinyin": "Tā tōutōu de liūchūle jiàoshì.", "meaningVi": "Anh ấy lén lút trốn ra khỏi lớp học."}],
    "hsk6_1318": [{"chinese": "他头脑很灵活。", "pinyin": "Tā tóunǎo hěn línghuó.", "meaningVi": "Đầu óc anh ấy rất linh hoạt."}],
    "hsk6_1319": [{"chinese": "大家举手投票表决。", "pinyin": "Dàjiā jǔshǒu tóupiào biǎojué.", "meaningVi": "Mọi người giơ tay biểu quyết."}],
    "hsk6_1320": [{"chinese": "顾客对服务态度提出了投诉。", "pinyin": "Gùkè duì fúwù tàidù tíchūle tóusù.", "meaningVi": "Khách hàng đã khiếu nại về thái độ phục vụ."}],
    "hsk6_1321": [{"chinese": "他把积蓄都用来投资了。", "pinyin": "Tā bǎ jīxù dōu yònglái tóuzī le.", "meaningVi": "Anh ấy đã dùng hết tiền tiết kiệm để đầu tư."}],
    "hsk6_1322": [{"chinese": "这张纸太薄，光能透过去。", "pinyin": "Zhè zhāng zhǐ tài báo, guāng néng tòu guòqu.", "meaningVi": "Tờ giấy này quá mỏng, ánh sáng có thể xuyên qua."}],
    "hsk6_1323": [{"chinese": "透过窗户可以看到花园。", "pinyin": "Tòuguò chuānghu kěyǐ kàndào huāyuán.", "meaningVi": "Qua cửa sổ có thể nhìn thấy khu vườn."}],
    "hsk6_1324": [{"chinese": "他向记者透露了一些细节。", "pinyin": "Tā xiàng jìzhě tòulùle yìxiē xìjié.", "meaningVi": "Anh ấy đã tiết lộ một số chi tiết với phóng viên."}],
    "hsk6_1325": [{"chinese": "这个玻璃杯是透明的。", "pinyin": "Zhège bōlibēi shì tòumíng de.", "meaningVi": "Chiếc cốc thủy tinh này trong suốt."}],
    "hsk6_1326": [{"chinese": "昨晚发生了一起突发事件。", "pinyin": "Zuówǎn fāshēngle yì qǐ tūfā shìjiàn.", "meaningVi": "Tối qua đã xảy ra một sự kiện đột phát."}],
    "hsk6_1327": [{"chinese": "科学家在这个领域取得了重大突破。", "pinyin": "Kēxuéjiā zài zhège lǐngyù qǔdéle zhòngdà tūpò.", "meaningVi": "Các nhà khoa học đã đạt được đột phá lớn trong lĩnh vực này."}],
    "hsk6_1328": [{"chinese": "这块布上印着精美的图案。", "pinyin": "Zhè kuài bù shàng yìnzhe jīngměi de tú'àn.", "meaningVi": "Trên tấm vải này in hoa văn tinh xảo."}],
    "hsk6_1329": [{"chinese": "报告中附有详细的图表。", "pinyin": "Bàogào zhōng fùyǒu xiángxì de túbiǎo.", "meaningVi": "Trong báo cáo có kèm theo biểu đồ chi tiết."}],
    "hsk6_1330": [{"chinese": "师傅正在教徒弟手艺。", "pinyin": "Shīfu zhèngzài jiāo túdì shǒuyì.", "meaningVi": "Sư phụ đang dạy nghề cho học trò."}],
    "hsk6_1331": [{"chinese": "我们需要寻找新的合作途径。", "pinyin": "Wǒmen xūyào xúnzhǎo xīn de hézuò tújìng.", "meaningVi": "Chúng ta cần tìm con đường hợp tác mới."}],
    "hsk6_1332": [{"chinese": "这张图像非常模糊。", "pinyin": "Zhè zhāng túxiàng fēicháng móhu.", "meaningVi": "Bức ảnh này vô cùng mờ."}],
    "hsk6_1334": [{"chinese": "这里的土壤十分肥沃。", "pinyin": "Zhèlǐ de tǔrǎng shífēn féiwò.", "meaningVi": "Đất ở đây vô cùng màu mỡ."}],
    "hsk6_1336": [{"chinese": "全班同学都很团结。", "pinyin": "Quán bān tóngxué dōu hěn tuánjié.", "meaningVi": "Cả lớp học sinh đều rất đoàn kết."}],
    "hsk6_1337": [{"chinese": "他们是一个非常优秀的团体。", "pinyin": "Tāmen shì yí gè fēicháng yōuxiù de tuántǐ.", "meaningVi": "Họ là một tập thể vô cùng xuất sắc."}],
    "hsk6_1338": [{"chinese": "春节是家人团圆的日子。", "pinyin": "Chūnjié shì jiārén tuányuán de rìzi.", "meaningVi": "Tết Nguyên Đán là ngày gia đình đoàn tụ."}],
    "hsk6_1339": [{"chinese": "专家推测这与气候变化有关。", "pinyin": "Zhuānjiā tuīcè zhè yǔ qìhòu biànhuà yǒuguān.", "meaningVi": "Chuyên gia suy đoán điều này có liên quan đến biến đổi khí hậu."}],
    "hsk6_1340": [{"chinese": "他挨家挨户推销产品。", "pinyin": "Tā āijiā-āihù tuīxiāo chǎnpǐn.", "meaningVi": "Anh ấy đi từng nhà chào bán sản phẩm."}],
    "hsk6_1341": [{"chinese": "政府正在推行新的环保政策。", "pinyin": "Zhèngfǔ zhèngzài tuīxíng xīn de huánbǎo zhèngcè.", "meaningVi": "Chính phủ đang triển khai chính sách bảo vệ môi trường mới."}],
    "hsk6_1342": [{"chinese": "游客离境时可以办理退税。", "pinyin": "Yóukè líjìng shí kěyǐ bànlǐ tuìshuì.", "meaningVi": "Du khách khi rời đi có thể làm thủ tục hoàn thuế."}],
    "hsk6_1343": [{"chinese": "他把药一口吞了下去。", "pinyin": "Tā bǎ yào yìkǒu tūnle xiàqù.", "meaningVi": "Anh ấy nuốt thuốc một hơi."}],
    "hsk6_1344": [{"chinese": "他把箱子拖到了门口。", "pinyin": "Tā bǎ xiāngzi tuō dàole ménkǒu.", "meaningVi": "Anh ấy kéo cái hộp đến cửa."}],
    "hsk6_1345": [{"chinese": "请不要再拖延时间了。", "pinyin": "Qǐng búyào zài tuōyán shíjiān le.", "meaningVi": "Xin đừng trì hoãn thời gian nữa."}],
    "hsk6_1346": [{"chinese": "这件行李需要托运。", "pinyin": "Zhè jiàn xíngli xūyào tuōyùn.", "meaningVi": "Kiện hành lý này cần ký gửi."}],
    "hsk6_1347": [{"chinese": "工人在挖一条水沟。", "pinyin": "Gōngrén zài wā yì tiáo shuǐgōu.", "meaningVi": "Công nhân đang đào một con mương."}],
    "hsk6_1348": [{"chinese": "哇，这个蛋糕真好看！", "pinyin": "Wā, zhège dàngāo zhēn hǎokàn!", "meaningVi": "Ôi, chiếc bánh này đẹp quá!"}],
    "hsk6_1349": [{"chinese": "女孩抱着她的洋娃娃。", "pinyin": "Nǚhái bàozhe tā de yángwáwa.", "meaningVi": "Cô bé ôm con búp bê của mình."}],
    "hsk6_1350": [{"chinese": "这幅画挂歪了。", "pinyin": "Zhè fú huà guà wāi le.", "meaningVi": "Bức tranh này treo bị lệch rồi."}],
    "hsk6_1351": [{"chinese": "不要只看一个人的外表。", "pinyin": "Búyào zhǐ kàn yí gè rén de wàibiǎo.", "meaningVi": "Đừng chỉ nhìn vẻ bề ngoài của một người."}],
    "hsk6_1352": [{"chinese": "他从事外交工作多年。", "pinyin": "Tā cóngshì wàijiāo gōngzuò duō nián.", "meaningVi": "Anh ấy đã làm công tác ngoại giao nhiều năm."}],
    "hsk6_1353": [{"chinese": "他很少受到外界的干扰。", "pinyin": "Tā hěn shǎo shòudào wàijiè de gānrǎo.", "meaningVi": "Anh ấy rất ít khi bị bên ngoài quấy nhiễu."}],
    "hsk6_1354": [{"chinese": "他是一名外科医生。", "pinyin": "Tā shì yì míng wàikē yīshēng.", "meaningVi": "Anh ấy là một bác sĩ ngoại khoa."}],
    "hsk6_1355": [{"chinese": "这种植物是外来物种。", "pinyin": "Zhè zhǒng zhíwù shì wàilái wùzhǒng.", "meaningVi": "Loại thực vật này là loài ngoại lai."}],
    "hsk6_1356": [{"chinese": "我的外甥今年上小学了。", "pinyin": "Wǒ de wàisheng jīnnián shàng xiǎoxué le.", "meaningVi": "Cháu trai của tôi năm nay đã vào tiểu học."}],
    "hsk6_1357": [{"chinese": "这条河道十分弯曲。", "pinyin": "Zhè tiáo hédào shífēn wānqū.", "meaningVi": "Dòng sông này vô cùng ngoằn ngoèo."}],
    "hsk6_1358": [{"chinese": "他以顽强的毅力战胜了病魔。", "pinyin": "Tā yǐ wánqiáng de yìlì zhànshèngle bìngmó.", "meaningVi": "Anh ấy đã dùng nghị lực ngoan cường chiến thắng bệnh tật."}],
    "hsk6_1359": [{"chinese": "春天万物复苏。", "pinyin": "Chūntiān wànwù fùsū.", "meaningVi": "Mùa xuân muôn vật hồi sinh."}],
    "hsk6_1360": [{"chinese": "故事里的王子娶了公主。", "pinyin": "Gùshi lǐ de wángzǐ qǔle gōngzhǔ.", "meaningVi": "Hoàng tử trong câu chuyện đã cưới công chúa."}],
    "hsk6_1361": [{"chinese": "渔民撒下了渔网。", "pinyin": "Yúmín sāxiàle yúwǎng.", "meaningVi": "Ngư dân đã thả lưới đánh cá."}],
    "hsk6_1362": [{"chinese": "往后的日子会越来越好。", "pinyin": "Wǎnghòu de rìzi huì yuè lái yuè hǎo.", "meaningVi": "Những ngày về sau sẽ ngày càng tốt hơn."}],
    "hsk6_1363": [{"chinese": "两国之间的贸易往来十分频繁。", "pinyin": "Liǎng guó zhījiān de màoyì wǎnglái shífēn pínfán.", "meaningVi": "Giao thương qua lại giữa hai nước vô cùng thường xuyên."}],
    "hsk6_1364": [{"chinese": "今年的雨水比往年多。", "pinyin": "Jīnnián de yǔshuǐ bǐ wǎngnián duō.", "meaningVi": "Lượng mưa năm nay nhiều hơn những năm trước."}],
    "hsk6_1365": [{"chinese": "他站在山顶远望大海。", "pinyin": "Tā zhàn zài shāndǐng yuǎnwàng dàhǎi.", "meaningVi": "Anh ấy đứng trên đỉnh núi nhìn xa ra biển."}],
    "hsk6_1366": [{"chinese": "公司正面临一场严重的危机。", "pinyin": "Gōngsī zhèng miànlín yì chǎng yánzhòng de wēijī.", "meaningVi": "Công ty đang đối mặt với một cuộc khủng hoảng nghiêm trọng."}],
    "hsk6_1367": [{"chinese": "这些微小的变化很容易被忽略。", "pinyin": "Zhèxiē wēixiǎo de biànhuà hěn róngyì bèi hūlüè.", "meaningVi": "Những thay đổi nhỏ bé này rất dễ bị bỏ qua."}],
    "hsk6_1368": [{"chinese": "他因为违规操作被处罚了。", "pinyin": "Tā yīnwèi wéiguī cāozuò bèi chǔfá le.", "meaningVi": "Anh ấy bị xử phạt vì thao tác vi phạm quy định."}],
    "hsk6_1369": [{"chinese": "我们应该维护公共秩序。", "pinyin": "Wǒmen yīnggāi wéihù gōnggòng zhìxù.", "meaningVi": "Chúng ta nên duy trì trật tự công cộng."}],
    "hsk6_1370": [{"chinese": "这个问题真让人为难。", "pinyin": "Zhège wèntí zhēn ràng rén wéinán.", "meaningVi": "Vấn đề này thật khiến người ta khó xử."}],
    "hsk6_1371": [{"chinese": "他从小就喜欢下围棋。", "pinyin": "Tā cóngxiǎo jiù xǐhuan xià wéiqí.", "meaningVi": "Anh ấy từ nhỏ đã thích chơi cờ vây."}],
    "hsk6_1372": [{"chinese": "这次培训为期三个月。", "pinyin": "Zhè cì péixùn wéiqī sān gè yuè.", "meaningVi": "Đợt đào tạo lần này kéo dài ba tháng."}],
    "hsk6_1373": [{"chinese": "水果里含有丰富的维生素。", "pinyin": "Shuǐguǒ lǐ hányǒu fēngfù de wéishēngsù.", "meaningVi": "Trong trái cây chứa nhiều vitamin."}],
    "hsk6_1374": [{"chinese": "到目前为止一切顺利。", "pinyin": "Dào mùqián wéizhǐ yíqiè shùnlì.", "meaningVi": "Cho đến hiện tại mọi thứ đều thuận lợi."}],
    "hsk6_1375": [{"chinese": "她觉得很委屈，忍不住哭了。", "pinyin": "Tā juéde hěn wěiqu, rěnbuzhù kū le.", "meaningVi": "Cô ấy cảm thấy rất tủi thân, không kìm được mà khóc."}],
    "hsk6_1376": [{"chinese": "他委托律师处理这件事。", "pinyin": "Tā wěituō lǜshī chǔlǐ zhè jiàn shì.", "meaningVi": "Anh ấy ủy thác cho luật sư xử lý việc này."}],
    "hsk6_1377": [{"chinese": "此事尚未确定。", "pinyin": "Cǐ shì shàng wèi quèdìng.", "meaningVi": "Việc này vẫn chưa được xác định."}],
    "hsk6_1378": [{"chinese": "便宜的东西未必质量差。", "pinyin": "Piányi de dōngxi wèibì zhìliàng chà.", "meaningVi": "Đồ rẻ chưa chắc đã kém chất lượng."}],
    "hsk6_1379": [{"chinese": "未成年人禁止饮酒。", "pinyin": "Wèichéngniánrén jìnzhǐ yǐnjiǔ.", "meaningVi": "Người chưa thành niên bị cấm uống rượu."}],
    "hsk6_1380": [{"chinese": "为此，公司调整了整体战略。", "pinyin": "Wèicǐ, gōngsī tiáozhěngle zhěngtǐ zhànlüè.", "meaningVi": "Vì điều này, công ty đã điều chỉnh chiến lược tổng thể."}],
    "hsk6_1381": [{"chinese": "他至今不明白为何会这样。", "pinyin": "Tā zhìjīn bù míngbai wèihé huì zhèyàng.", "meaningVi": "Cho đến nay anh ấy vẫn không hiểu tại sao lại như vậy."}],
    "hsk6_1382": [{"chinese": "感冒会影响味觉。", "pinyin": "Gǎnmào huì yǐngxiǎng wèijué.", "meaningVi": "Cảm cúm sẽ ảnh hưởng đến vị giác."}],
    "hsk6_1383": [{"chinese": "他今天胃口不太好。", "pinyin": "Tā jīntiān wèikǒu bú tài hǎo.", "meaningVi": "Hôm nay khẩu vị của anh ấy không tốt lắm."}],
    "hsk6_1384": [{"chinese": "他性格温和，从不发脾气。", "pinyin": "Tā xìnggé wēnhé, cóng bù fā píqi.", "meaningVi": "Tính cách anh ấy ôn hòa, không bao giờ nổi giận."}],
    "hsk6_1385": [{"chinese": "她说话的语气十分温柔。", "pinyin": "Tā shuōhuà de yǔqì shífēn wēnróu.", "meaningVi": "Giọng điệu nói chuyện của cô ấy vô cùng dịu dàng."}],
    "hsk6_1386": [{"chinese": "这份文档还需要进一步修改。", "pinyin": "Zhè fèn wéndàng hái xūyào jìnyíbù xiūgǎi.", "meaningVi": "Tài liệu này vẫn cần chỉnh sửa thêm."}],
    "hsk6_1387": [{"chinese": "他去商店买了一些文具。", "pinyin": "Tā qù shāngdiàn mǎile yìxiē wénjù.", "meaningVi": "Anh ấy đã đến cửa hàng mua một ít văn phòng phẩm."}],
    "hsk6_1388": [{"chinese": "她高中选择了文科。", "pinyin": "Tā gāozhōng xuǎnzéle wénkē.", "meaningVi": "Cô ấy đã chọn ban khoa học xã hội ở trung học."}],
    "hsk6_1389": [{"chinese": "古埃及是一个伟大的文明。", "pinyin": "Gǔ Āijí shì yí gè wěidà de wénmíng.", "meaningVi": "Ai Cập cổ đại là một nền văn minh vĩ đại."}],
    "hsk6_1390": [{"chinese": "这座城市以美食闻名。", "pinyin": "Zhè zuò chéngshì yǐ měishí wénmíng.", "meaningVi": "Thành phố này nổi tiếng với ẩm thực."}],
    "hsk6_1391": [{"chinese": "博物馆里收藏着许多珍贵文物。", "pinyin": "Bówùguǎn lǐ shōucángzhe xǔduō zhēnguì wénwù.", "meaningVi": "Trong bảo tàng lưu giữ rất nhiều di vật văn hóa quý giá."}],
    "hsk6_1392": [{"chinese": "他查阅了大量历史文献。", "pinyin": "Tā cháyuèle dàliàng lìshǐ wénxiàn.", "meaningVi": "Anh ấy đã tra cứu rất nhiều tài liệu lịch sử."}],
    "hsk6_1393": [{"chinese": "这场文艺演出深受观众喜爱。", "pinyin": "Zhè chǎng wényì yǎnchū shēn shòu guānzhòng xǐ'ài.", "meaningVi": "Buổi biểu diễn văn nghệ này rất được khán giả yêu thích."}],
    "hsk6_1394": [{"chinese": "池塘里有一只乌龟。", "pinyin": "Chítáng lǐ yǒu yì zhī wūguī.", "meaningVi": "Trong ao có một con rùa."}],
    "hsk6_1395": [{"chinese": "工厂的污水必须经过处理。", "pinyin": "Gōngchǎng de wūshuǐ bìxū jīngguò chǔlǐ.", "meaningVi": "Nước thải của nhà máy phải qua xử lý."}],
    "hsk6_1396": [{"chinese": "去哪儿吃饭我都无所谓。", "pinyin": "Qù nǎr chīfàn wǒ dōu wúsuǒwèi.", "meaningVi": "Đi đâu ăn cơm tôi cũng không quan trọng."}],
    "hsk6_1397": [{"chinese": "他无疑是这个团队最优秀的人。", "pinyin": "Tā wúyí shì zhège tuánduì zuì yōuxiù de rén.", "meaningVi": "Không nghi ngờ gì anh ấy là người xuất sắc nhất đội."}],
    "hsk6_1398": [{"chinese": "这个国家正在研发新型武器。", "pinyin": "Zhège guójiā zhèngzài yánfā xīnxíng wǔqì.", "meaningVi": "Quốc gia này đang nghiên cứu phát triển vũ khí kiểu mới."}],
    "hsk6_1399": [{"chinese": "他误以为我不在家。", "pinyin": "Tā wù yǐwéi wǒ bú zài jiā.", "meaningVi": "Anh ấy hiểu lầm rằng tôi không có nhà."}],
    "hsk6_1400": [{"chinese": "请不要误解我的意思。", "pinyin": "Qǐng búyào wùjiě wǒ de yìsi.", "meaningVi": "Xin đừng hiểu lầm ý của tôi."}],
    "hsk6_1401": [{"chinese": "这是一个圆形的物体。", "pinyin": "Zhè shì yí gè yuánxíng de wùtǐ.", "meaningVi": "Đây là một vật thể hình tròn."}],
    "hsk6_1402": [{"chinese": "我们应该从失败中吸取教训。", "pinyin": "Wǒmen yīnggāi cóng shībài zhōng xīqǔ jiàoxùn.", "meaningVi": "Chúng ta nên rút ra bài học từ thất bại."}],
    "hsk6_1403": [{"chinese": "她是一个孝顺的媳妇。", "pinyin": "Tā shì yí gè xiàoshùn de xífu.", "meaningVi": "Cô ấy là một nàng dâu hiếu thảo."}],
    "hsk6_1404": [{"chinese": "每个地方都有自己的习俗。", "pinyin": "Měi gè dìfang dōu yǒu zìjǐ de xísú.", "meaningVi": "Mỗi nơi đều có phong tục riêng của mình."}],
    "hsk6_1405": [{"chinese": "她喜欢看喜剧电影。", "pinyin": "Tā xǐhuan kàn xǐjù diànyǐng.", "meaningVi": "Cô ấy thích xem phim hài kịch."}],
    "hsk6_1406": [{"chinese": "家里最近有喜事。", "pinyin": "Jiālǐ zuìjìn yǒu xǐshì.", "meaningVi": "Gần đây nhà có chuyện vui."}],
    "hsk6_1407": [{"chinese": "他起床后先去洗漱。", "pinyin": "Tā qǐchuáng hòu xiān qù xǐshù.", "meaningVi": "Sau khi thức dậy anh ấy đi rửa mặt đánh răng trước."}],
    "hsk6_1408": [{"chinese": "人体由无数细胞组成。", "pinyin": "Réntǐ yóu wúshù xìbāo zǔchéng.", "meaningVi": "Cơ thể con người được cấu tạo từ vô số tế bào."}],
    "hsk6_1409": [{"chinese": "请勤洗手，避免细菌感染。", "pinyin": "Qǐng qín xǐshǒu, bìmiǎn xìjūn gǎnrǎn.", "meaningVi": "Xin rửa tay thường xuyên để tránh nhiễm khuẩn."}],
    "hsk6_1410": [{"chinese": "这是一系列的活动。", "pinyin": "Zhè shì yí xìliè de huódòng.", "meaningVi": "Đây là một loạt các hoạt động."}],
    "hsk6_1411": [{"chinese": "他对传统戏曲很感兴趣。", "pinyin": "Tā duì chuántǒng xìqǔ hěn gǎn xìngqù.", "meaningVi": "Anh ấy rất có hứng thú với hí kịch truyền thống."}],
    "hsk6_1412": [{"chinese": "他做事十分细致。", "pinyin": "Tā zuòshì shífēn xìzhì.", "meaningVi": "Anh ấy làm việc vô cùng tỉ mỉ."}],
    "hsk6_1413": [{"chinese": "你别吓我。", "pinyin": "Nǐ bié xià wǒ.", "meaningVi": "Bạn đừng dọa tôi."}],
    "hsk6_1414": [{"chinese": "学好一门语言需要下功夫。", "pinyin": "Xuéhǎo yì mén yǔyán xūyào xià gōngfu.", "meaningVi": "Học tốt một ngoại ngữ cần phải bỏ công sức."}],
    "hsk6_1415": [{"chinese": "顾客已经在网上下单了。", "pinyin": "Gùkè yǐjīng zài wǎngshàng xiàdān le.", "meaningVi": "Khách hàng đã đặt đơn hàng trên mạng."}],
    "hsk6_1416": [{"chinese": "孩子暑假参加了一个夏令营。", "pinyin": "Háizi shǔjià cānjiāle yí gè xiàlìngyíng.", "meaningVi": "Kỳ nghỉ hè con tham gia một trại hè."}],
    "hsk6_1417": [{"chinese": "第一辆新车已经下线。", "pinyin": "Dì-yī liàng xīnchē yǐjīng xiàxiàn.", "meaningVi": "Chiếc xe mới đầu tiên đã xuất xưởng."}],
    "hsk6_1418": [{"chinese": "会议安排在本月下旬。", "pinyin": "Huìyì ānpái zài běn yuè xiàxún.", "meaningVi": "Cuộc họp được sắp xếp vào hạ tuần tháng này."}],
    "hsk6_1419": [{"chinese": "这幅画的色彩十分鲜明。", "pinyin": "Zhè fú huà de sècǎi shífēn xiānmíng.", "meaningVi": "Màu sắc của bức tranh này vô cùng rõ nét."}],
    "hsk6_1420": [{"chinese": "情况比先前好多了。", "pinyin": "Qíngkuàng bǐ xiānqián hǎo duō le.", "meaningVi": "Tình hình đã tốt hơn nhiều so với trước đây."}],
    "hsk6_1421": [{"chinese": "这些花朵色彩鲜艳。", "pinyin": "Zhèxiē huāduǒ sècǎi xiānyàn.", "meaningVi": "Những bông hoa này màu sắc tươi sáng rực rỡ."}],
    "hsk6_1422": [{"chinese": "她嫌这件衣服太贵。", "pinyin": "Tā xián zhè jiàn yīfu tài guì.", "meaningVi": "Cô ấy chê chiếc áo này quá đắt."}],
    "hsk6_1423": [{"chinese": "这个颜色显得她更年轻。", "pinyin": "Zhège yánsè xiǎnde tā gèng niánqīng.", "meaningVi": "Màu này khiến cô ấy trông trẻ hơn."}],
    "hsk6_1424": [{"chinese": "他刚才真是好险。", "pinyin": "Tā gāngcái zhēnshi hǎo xiǎn.", "meaningVi": "Vừa nãy anh ấy thật là nguy hiểm quá."}],
    "hsk6_1425": [{"chinese": "这项措施取得了显著效果。", "pinyin": "Zhè xiàng cuòshī qǔdéle xiǎnzhù xiàoguǒ.", "meaningVi": "Biện pháp này đã đạt được hiệu quả rõ rệt."}],
    "hsk6_1426": [{"chinese": "每人限购两件。", "pinyin": "Měi rén xiàn gòu liǎng jiàn.", "meaningVi": "Mỗi người giới hạn mua hai món."}],
    "hsk6_1427": [{"chinese": "她用针线缝补衣服。", "pinyin": "Tā yòng zhēnxiàn féngbǔ yīfu.", "meaningVi": "Cô ấy dùng kim chỉ vá quần áo."}],
    "hsk6_1428": [{"chinese": "这是现存最古老的建筑之一。", "pinyin": "Zhè shì xiàncún zuì gǔlǎo de jiànzhù zhī yī.", "meaningVi": "Đây là một trong những công trình cổ nhất còn tồn tại."}],
    "hsk6_1429": [{"chinese": "忍耐是有限度的。", "pinyin": "Rěnnài shì yǒu xiàndù de.", "meaningVi": "Sự nhẫn nại là có giới hạn."}],
    "hsk6_1430": [{"chinese": "这款商品目前有现货。", "pinyin": "Zhè kuǎn shāngpǐn mùqián yǒu xiànhuò.", "meaningVi": "Sản phẩm này hiện tại có hàng sẵn."}],
    "hsk6_1431": [{"chinese": "他陷入了深深的沉思。", "pinyin": "Tā xiànrùle shēnshēn de chénsī.", "meaningVi": "Anh ấy chìm vào suy tư sâu sắc."}],
    "hsk6_1432": [{"chinese": "警方发现了一条重要线索。", "pinyin": "Jǐngfāng fāxiànle yì tiáo zhòngyào xiànsuǒ.", "meaningVi": "Cảnh sát đã phát hiện một manh mối quan trọng."}],
    "hsk6_1433": [{"chinese": "这项优惠限于新用户。", "pinyin": "Zhè xiàng yōuhuì xiànyú xīn yònghù.", "meaningVi": "Ưu đãi này chỉ giới hạn cho người dùng mới."}],
    "hsk6_1434": [{"chinese": "两人的年龄相差不大。", "pinyin": "Liǎng rén de niánlíng xiāngchà bú dà.", "meaningVi": "Tuổi tác của hai người chênh lệch không nhiều."}],
    "hsk6_1435": [{"chinese": "早餐吃了两根香肠。", "pinyin": "Zǎocān chīle liǎng gēn xiāngcháng.", "meaningVi": "Bữa sáng đã ăn hai chiếc xúc xích."}],
    "hsk6_1436": [{"chinese": "相传这座桥有上千年历史。", "pinyin": "Xiāngchuán zhè zuò qiáo yǒu shàng qiān nián lìshǐ.", "meaningVi": "Tương truyền cây cầu này có lịch sử hàng nghìn năm."}],
    "hsk6_1437": [{"chinese": "这两条线段的长度相等。", "pinyin": "Zhè liǎng tiáo xiànduàn de chángdù xiāngděng.", "meaningVi": "Độ dài của hai đoạn thẳng này bằng nhau."}],
    "hsk6_1438": [{"chinese": "这两座岛屿由一座桥相连。", "pinyin": "Zhè liǎng zuò dǎoyǔ yóu yí zuò qiáo xiānglián.", "meaningVi": "Hai hòn đảo này được kết nối bởi một cây cầu."}],
    "hsk6_1439": [{"chinese": "她喷了一点香水。", "pinyin": "Tā pēnle yìdiǎn xiāngshuǐ.", "meaningVi": "Cô ấy xịt một chút nước hoa."}],
    "hsk6_1440": [{"chinese": "请采取相应的措施。", "pinyin": "Qǐng cǎiqǔ xiāngyìng de cuòshī.", "meaningVi": "Xin áp dụng biện pháp tương ứng."}],
    "hsk6_1441": [{"chinese": "她戴着一条珍珠项链。", "pinyin": "Tā dàizhe yì tiáo zhēnzhū xiàngliàn.", "meaningVi": "Cô ấy đeo một chiếc vòng cổ trân châu."}],
    "hsk6_1442": [{"chinese": "爷爷喜欢下象棋。", "pinyin": "Yéye xǐhuan xià xiàngqí.", "meaningVi": "Ông thích chơi cờ tướng."}],
    "hsk6_1443": [{"chinese": "他很喜欢听相声。", "pinyin": "Tā hěn xǐhuan tīng xiàngsheng.", "meaningVi": "Anh ấy rất thích nghe tương thanh."}],
    "hsk6_1444": [{"chinese": "她一直向往自由的生活。", "pinyin": "Tā yìzhí xiàngwǎng zìyóu de shēnghuó.", "meaningVi": "Cô ấy luôn khao khát cuộc sống tự do."}],
    "hsk6_1445": [{"chinese": "运动可以消除疲劳。", "pinyin": "Yùndòng kěyǐ xiāochú píláo.", "meaningVi": "Vận động có thể xóa bỏ mệt mỏi."}],
    "hsk6_1446": [{"chinese": "请对伤口进行消毒。", "pinyin": "Qǐng duì shāngkǒu jìnxíng xiāodú.", "meaningVi": "Xin khử trùng vết thương."}],
    "hsk6_1447": [{"chinese": "消防人员及时赶到了现场。", "pinyin": "Xiāofáng rényuán jíshí gǎndàole xiànchǎng.", "meaningVi": "Nhân viên phòng cháy chữa cháy đã kịp thời đến hiện trường."}],
    "hsk6_1448": [{"chinese": "这台设备消耗大量电力。", "pinyin": "Zhè tái shèbèi xiāohào dàliàng diànlì.", "meaningVi": "Thiết bị này tiêu tốn nhiều điện năng."}],
    "hsk6_1449": [{"chinese": "军队彻底消灭了敌人。", "pinyin": "Jūnduì chèdǐ xiāomièle dírén.", "meaningVi": "Quân đội đã tiêu diệt hoàn toàn kẻ địch."}],
    "hsk6_1450": [{"chinese": "这个地区盛产小麦。", "pinyin": "Zhège dìqū shèngchǎn xiǎomài.", "meaningVi": "Khu vực này sản xuất nhiều lúa mì."}],
    "hsk6_1451": [{"chinese": "他对钱很小气。", "pinyin": "Tā duì qián hěn xiǎoqi.", "meaningVi": "Anh ấy rất keo kiệt về tiền bạc."}],
    "hsk6_1452": [{"chinese": "小偷儿被警察抓住了。", "pinyin": "Xiǎotōur bèi jǐngchá zhuāzhù le.", "meaningVi": "Tên trộm đã bị cảnh sát bắt được."}],
    "hsk6_1453": [{"chinese": "她脸上露出了甜美的笑容。", "pinyin": "Tā liǎn shàng lòuchūle tiánměi de xiàoróng.", "meaningVi": "Trên mặt cô ấy nở một nụ cười ngọt ngào."}],
    "hsk6_1454": [{"chinese": "这项政策产生了积极的效应。", "pinyin": "Zhè xiàng zhèngcè chǎnshēngle jījí de xiàoyìng.", "meaningVi": "Chính sách này đã tạo ra hiệu ứng tích cực."}],
    "hsk6_1455": [{"chinese": "走累了就歇一会儿吧。", "pinyin": "Zǒulèi le jiù xiē yíhuìr ba.", "meaningVi": "Đi mệt rồi thì nghỉ một lát đi."}],
    "hsk6_1456": [{"chinese": "请随身携带证件。", "pinyin": "Qǐng suíshēn xiédài zhèngjiàn.", "meaningVi": "Xin mang theo giấy tờ tùy thân."}],
    "hsk6_1457": [{"chinese": "他加入了一个摄影协会。", "pinyin": "Tā jiārùle yí gè shèyǐng xiéhuì.", "meaningVi": "Anh ấy đã gia nhập một hiệp hội nhiếp ảnh."}],
    "hsk6_1458": [{"chinese": "各部门之间需要相互协调。", "pinyin": "Gè bùmén zhījiān xūyào xiānghù xiétiáo.", "meaningVi": "Các bộ phận cần phối hợp lẫn nhau."}],
    "hsk6_1459": [{"chinese": "警方请求群众协助调查。", "pinyin": "Jǐngfāng qǐngqiú qúnzhòng xiézhù diàochá.", "meaningVi": "Cảnh sát yêu cầu quần chúng hỗ trợ điều tra."}],
    "hsk6_1460": [{"chinese": "这是他最心爱的东西。", "pinyin": "Zhè shì tā zuì xīn'ài de dōngxi.", "meaningVi": "Đây là món đồ mà anh ấy yêu quý nhất."}],
    "hsk6_1461": [{"chinese": "她把这份感情藏在心底。", "pinyin": "Tā bǎ zhè fèn gǎnqíng cáng zài xīndǐ.", "meaningVi": "Cô ấy giấu tình cảm này trong đáy lòng."}],
    "hsk6_1462": [{"chinese": "这是今年最新款的手机。", "pinyin": "Zhè shì jīnnián zuì xīnkuǎn de shǒujī.", "meaningVi": "Đây là chiếc điện thoại mẫu mới nhất năm nay."}],
    "hsk6_1463": [{"chinese": "音乐能够抚慰人的心灵。", "pinyin": "Yīnyuè nénggòu fǔwèi rén de xīnlíng.", "meaningVi": "Âm nhạc có thể xoa dịu tâm hồn con người."}],
    "hsk6_1464": [{"chinese": "越来越多的人通过新媒体获取信息。", "pinyin": "Yuè lái yuè duō de rén tōngguò xīnméitǐ huòqǔ xìnxī.", "meaningVi": "Ngày càng nhiều người tiếp nhận thông tin qua truyền thông mới."}],
    "hsk6_1465": [{"chinese": "在她心目中，父亲是英雄。", "pinyin": "Zài tā xīnmù zhōng, fùqīn shì yīngxióng.", "meaningVi": "Trong lòng cô ấy, cha là anh hùng."}],
    "hsk6_1466": [{"chinese": "政府大力支持新能源汽车发展。", "pinyin": "Zhèngfǔ dàlì zhīchí xīnnéngyuán qìchē fāzhǎn.", "meaningVi": "Chính phủ tích cực hỗ trợ phát triển xe năng lượng mới."}],
    "hsk6_1467": [{"chinese": "他这个月的薪水涨了。", "pinyin": "Tā zhège yuè de xīnshui zhǎng le.", "meaningVi": "Lương tháng này của anh ấy đã tăng."}],
    "hsk6_1468": [{"chinese": "看到孩子受伤，妈妈非常心疼。", "pinyin": "Kàndào háizi shòushāng, māma fēicháng xīnténg.", "meaningVi": "Thấy con bị thương, mẹ vô cùng xót xa."}],
    "hsk6_1469": [{"chinese": "这是一个新兴的行业。", "pinyin": "Zhè shì yí gè xīnxīng de hángyè.", "meaningVi": "Đây là một ngành nghề mới nổi."}],
    "hsk6_1470": [{"chinese": "这个设计非常新颖。", "pinyin": "Zhège shèjì fēicháng xīnyǐng.", "meaningVi": "Thiết kế này vô cùng mới lạ."}],
    "hsk6_1471": [{"chinese": "这个心愿藏在她心里很多年了。", "pinyin": "Zhège xīnyuàn cáng zài tā xīnli hěn duō nián le.", "meaningVi": "Tâm nguyện này đã được cô ấy giấu trong lòng nhiều năm rồi."}],
    "hsk6_1472": [{"chinese": "他的心脏跳得很快。", "pinyin": "Tā de xīnzàng tiào de hěn kuài.", "meaningVi": "Tim anh ấy đập rất nhanh."}],
    "hsk6_1473": [{"chinese": "他是一个值得信赖的人。", "pinyin": "Tā shì yí gè zhídé xìnlài de rén.", "meaningVi": "Anh ấy là một người đáng tin cậy."}],
    "hsk6_1474": [{"chinese": "坚定的信念支撑着他走下去。", "pinyin": "Jiāndìng de xìnniàn zhīchēngzhe tā zǒu xiàqu.", "meaningVi": "Niềm tin kiên định nâng đỡ anh ấy tiếp tục bước đi."}],
    "hsk6_1475": [{"chinese": "近年来短视频行业迅速兴起。", "pinyin": "Jìnnián lái duǎnshìpín hángyè xùnsù xīngqǐ.", "meaningVi": "Những năm gần đây ngành video ngắn phát triển nhanh chóng."}],
    "hsk6_1476": [{"chinese": "这款手机有多种型号。", "pinyin": "Zhè kuǎn shǒujī yǒu duō zhǒng xínghào.", "meaningVi": "Chiếc điện thoại này có nhiều mẫu mã."}],
    "hsk6_1477": [{"chinese": "这种物质有多种形态。", "pinyin": "Zhè zhǒng wùzhì yǒu duō zhǒng xíngtài.", "meaningVi": "Chất này có nhiều hình thái."}],
    "hsk6_1478": [{"chinese": "这款产品性价比很高。", "pinyin": "Zhè kuǎn chǎnpǐn xìngjiàbǐ hěn gāo.", "meaningVi": "Sản phẩm này rất đáng tiền."}],
    "hsk6_1479": [{"chinese": "这台电脑的性能十分出色。", "pinyin": "Zhè tái diànnǎo de xìngnéng shífēn chūsè.", "meaningVi": "Hiệu năng của chiếc máy tính này vô cùng xuất sắc."}],
    "hsk6_1480": [{"chinese": "他挺起胸膛走了进来。", "pinyin": "Tā tǐngqǐ xiōngtáng zǒule jìnlái.", "meaningVi": "Anh ấy ưỡn ngực bước vào."}],
    "hsk6_1481": [{"chinese": "这本教材已经修订了三次。", "pinyin": "Zhè běn jiàocái yǐjīng xiūdìngle sān cì.", "meaningVi": "Cuốn giáo trình này đã được biên tập lại ba lần."}],
    "hsk6_1482": [{"chinese": "工人们正在修复这座古建筑。", "pinyin": "Gōngrénmen zhèngzài xiūfù zhè zuò gǔ jiànzhù.", "meaningVi": "Các công nhân đang tu sửa công trình cổ này."}],
    "hsk6_1483": [{"chinese": "他的袖子被划破了。", "pinyin": "Tā de xiùzi bèi huàpò le.", "meaningVi": "Tay áo của anh ấy bị rách."}],
    "hsk6_1484": [{"chinese": "未经许可不得入内。", "pinyin": "Wèijīng xǔkě bùdé rùnèi.", "meaningVi": "Chưa được cho phép không được vào."}],
    "hsk6_1485": [{"chinese": "他详细叙述了事情的经过。", "pinyin": "Tā xiángxì xùshùle shìqing de jīngguò.", "meaningVi": "Anh ấy đã trần thuật chi tiết diễn biến sự việc."}],
    "hsk6_1486": [{"chinese": "地球围绕太阳旋转。", "pinyin": "Dìqiú wéirào tàiyáng xuánzhuǎn.", "meaningVi": "Trái Đất quay quanh Mặt Trời."}],
    "hsk6_1487": [{"chinese": "学校正在选拔优秀学生代表参赛。", "pinyin": "Xuéxiào zhèngzài xuǎnbá yōuxiù xuésheng dàibiǎo cānsài.", "meaningVi": "Nhà trường đang tuyển chọn học sinh xuất sắc đại diện thi đấu."}],
    "hsk6_1488": [{"chinese": "他选修了一门心理学课程。", "pinyin": "Tā xuǎnxiūle yì mén xīnlǐxué kèchéng.", "meaningVi": "Anh ấy đã chọn học môn tâm lý học tự chọn."}],
    "hsk6_1489": [{"chinese": "他终于学会了游泳。", "pinyin": "Tā zhōngyú xuéhuìle yóuyǒng.", "meaningVi": "Cuối cùng anh ấy đã học được bơi lội."}],
    "hsk6_1490": [{"chinese": "她获得了硕士学位。", "pinyin": "Tā huòdéle shuòshì xuéwèi.", "meaningVi": "Cô ấy đã nhận được bằng thạc sĩ."}],
    "hsk6_1491": [{"chinese": "他是一个很有学问的人。", "pinyin": "Tā shì yí gè hěn yǒu xuéwen de rén.", "meaningVi": "Anh ấy là một người rất có học vấn."}],
    "hsk6_1492": [{"chinese": "这个培训班共有二十名学员。", "pinyin": "Zhège péixùnbān gòng yǒu èrshí míng xuéyuán.", "meaningVi": "Lớp đào tạo này có tổng cộng hai mươi học viên."}],
    "hsk6_1493": [{"chinese": "这条血管出现了堵塞。", "pinyin": "Zhè tiáo xuèguǎn chūxiànle dǔsè.", "meaningVi": "Mạch máu này xuất hiện tắc nghẽn."}],
    "hsk6_1494": [{"chinese": "他的血型是O型。", "pinyin": "Tā de xuèxíng shì O xíng.", "meaningVi": "Nhóm máu của anh ấy là nhóm O."}],
    "hsk6_1495": [{"chinese": "他最近血压有点高。", "pinyin": "Tā zuìjìn xuèyā yǒudiǎn gāo.", "meaningVi": "Gần đây huyết áp của anh ấy hơi cao."}],
    "hsk6_1496": [{"chinese": "血液在全身循环流动。", "pinyin": "Xuèyè zài quánshēn xúnhuán liúdòng.", "meaningVi": "Máu tuần hoàn khắp cơ thể."}],
    "hsk6_1497": [{"chinese": "这台空调可以循环利用空气。", "pinyin": "Zhè tái kōngtiáo kěyǐ xúnhuán lìyòng kōngqì.", "meaningVi": "Chiếc điều hòa này có thể tuần hoàn tái sử dụng không khí."}],
    "hsk6_1498": [{"chinese": "遇到困难要主动寻求帮助。", "pinyin": "Yùdào kùnnan yào zhǔdòng xúnqiú bāngzhù.", "meaningVi": "Gặp khó khăn phải chủ động tìm kiếm sự giúp đỡ."}],
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
