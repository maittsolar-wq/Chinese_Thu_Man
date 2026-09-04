"""P5.10.3 (continued) -- Batch 003 (records 201-300 of the 5300 remaining
after the P5.10.2 pilot; continues immediately after examples_batch_002.json).

Same honesty note as generate_hsk_examples_p102.py / generate_examples_batch_002.py:
record SELECTION (via queue_lib_p103.get_next_batch_ids) is deterministic;
example CONTENT below was authored directly by this assistant (LLM).

Usage:
    python generate_examples_batch_003.py --dry-run
    python generate_examples_batch_003.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 3
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_003.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk1_124": [
        {"chinese": "同学们，早上好！", "pinyin": "Tóngxuémen, zǎoshang hǎo!", "meaningVi": "Các bạn học sinh, chào buổi sáng!"},
        {"chinese": "朋友们都来参加我的生日会。", "pinyin": "Péngyoumen dōu lái cānjiā wǒ de shēngrì huì.", "meaningVi": "Các bạn bè đều đến tham dự sinh nhật của tôi."},
    ],
    "hsk1_125": [{"chinese": "我每天都吃米饭。", "pinyin": "Wǒ měitiān dōu chī mǐfàn.", "meaningVi": "Tôi ăn cơm mỗi ngày."}],
    "hsk1_126": [{"chinese": "早上我喜欢吃面包。", "pinyin": "Zǎoshang wǒ xǐhuan chī miànbāo.", "meaningVi": "Buổi sáng tôi thích ăn bánh mì."}],
    "hsk1_127": [{"chinese": "妈妈做的面条儿很好吃。", "pinyin": "Māma zuò de miàntiáor hěn hǎochī.", "meaningVi": "Mì mẹ làm rất ngon."}],
    "hsk1_128": [{"chinese": "明年我要去中国留学。", "pinyin": "Míngnián wǒ yào qù Zhōngguó liúxué.", "meaningVi": "Năm sau tôi sẽ đi du học ở Trung Quốc."}],
    "hsk1_129": [{"chinese": "明天是星期六。", "pinyin": "Míngtiān shì xīngqīliù.", "meaningVi": "Ngày mai là thứ Bảy."}],
    "hsk1_130": [
        {"chinese": "你叫什么名字？", "pinyin": "Nǐ jiào shénme míngzi?", "meaningVi": "Bạn tên là gì?"},
        {"chinese": "请在这里写上你的名字。", "pinyin": "Qǐng zài zhèlǐ xiěshàng nǐ de míngzi.", "meaningVi": "Xin viết tên của bạn vào đây."},
    ],
    "hsk1_131": [{"chinese": "哪种颜色比较好看？", "pinyin": "Nǎ zhǒng yánsè bǐjiào hǎokàn?", "meaningVi": "Màu nào đẹp hơn?"}],
    "hsk1_132": [{"chinese": "你要哪个？", "pinyin": "Nǐ yào nǎge?", "meaningVi": "Bạn muốn cái nào?"}],
    "hsk1_133": [{"chinese": "你家在哪里？", "pinyin": "Nǐ jiā zài nǎlǐ?", "meaningVi": "Nhà bạn ở đâu?"}],
    "hsk1_134": [{"chinese": "你要去哪儿？", "pinyin": "Nǐ yào qù nǎr?", "meaningVi": "Bạn muốn đi đâu?"}],
    "hsk1_135": [{"chinese": "你喜欢哪些运动？", "pinyin": "Nǐ xǐhuan nǎxiē yùndòng?", "meaningVi": "Bạn thích những môn thể thao nào?"}],
    "hsk1_136": [{"chinese": "那是我的书包。", "pinyin": "Nà shì wǒ de shūbāo.", "meaningVi": "Đó là cặp sách của tôi."}],
    "hsk1_137": [{"chinese": "洗手间在那边。", "pinyin": "Xǐshǒujiān zài nàbiān.", "meaningVi": "Nhà vệ sinh ở bên kia."}],
    "hsk1_138": [{"chinese": "那个人是谁？", "pinyin": "Nàge rén shì shéi?", "meaningVi": "Người đó là ai?"}],
    "hsk1_139": [{"chinese": "我们在那里等你。", "pinyin": "Wǒmen zài nàlǐ děng nǐ.", "meaningVi": "Chúng tôi đợi bạn ở đó."}],
    "hsk1_140": [{"chinese": "请把书放在那儿。", "pinyin": "Qǐng bǎ shū fàng zài nàr.", "meaningVi": "Xin đặt sách ở đó."}],
    "hsk1_141": [{"chinese": "那些苹果是新鲜的。", "pinyin": "Nàxiē píngguǒ shì xīnxiān de.", "meaningVi": "Những quả táo đó là tươi."}],
    "hsk1_142": [{"chinese": "这个班男学生比较多。", "pinyin": "Zhège bān nán xuéshēng bǐjiào duō.", "meaningVi": "Lớp này có nhiều học sinh nam hơn."}],
    "hsk1_143": [{"chinese": "她的男朋友是医生。", "pinyin": "Tā de nánpéngyou shì yīshēng.", "meaningVi": "Bạn trai của cô ấy là bác sĩ."}],
    "hsk1_144": [{"chinese": "我很好，你呢？", "pinyin": "Wǒ hěn hǎo, nǐ ne?", "meaningVi": "Tôi khỏe, còn bạn thì sao?"}],
    "hsk1_145": [{"chinese": "你能帮我一下吗？", "pinyin": "Nǐ néng bāng wǒ yíxià ma?", "meaningVi": "Bạn có thể giúp tôi một chút không?"}],
    "hsk1_146": [{"chinese": "你今天忙吗？", "pinyin": "Nǐ jīntiān máng ma?", "meaningVi": "Hôm nay bạn có bận không?"}],
    "hsk1_147": [{"chinese": "你好，很高兴认识你。", "pinyin": "Nǐ hǎo, hěn gāoxìng rènshi nǐ.", "meaningVi": "Xin chào, rất vui được quen biết bạn."}],
    "hsk1_148": [{"chinese": "你们好，欢迎来到我们学校。", "pinyin": "Nǐmen hǎo, huānyíng lái dào wǒmen xuéxiào.", "meaningVi": "Xin chào các bạn, chào mừng đến trường chúng tôi."}],
    "hsk1_150": [{"chinese": "您好，请问您贵姓？", "pinyin": "Nín hǎo, qǐngwèn nín guìxìng?", "meaningVi": "Xin chào, xin hỏi quý danh của ngài là gì?"}],
    "hsk1_151": [{"chinese": "我早上喝一杯牛奶。", "pinyin": "Wǒ zǎoshang hē yì bēi niúnǎi.", "meaningVi": "Buổi sáng tôi uống một cốc sữa."}],
    "hsk1_152": [{"chinese": "这个班女学生比较多。", "pinyin": "Zhège bān nǚ xuéshēng bǐjiào duō.", "meaningVi": "Lớp này có nhiều học sinh nữ hơn."}],
    "hsk1_153": [{"chinese": "他们的女儿很聪明。", "pinyin": "Tāmen de nǚ'ér hěn cōngming.", "meaningVi": "Con gái của họ rất thông minh."}],
    "hsk1_154": [{"chinese": "他的女朋友是老师。", "pinyin": "Tā de nǚpéngyou shì lǎoshī.", "meaningVi": "Bạn gái của anh ấy là giáo viên."}],
    "hsk1_155": [{"chinese": "这位女士是我们的新同事。", "pinyin": "Zhè wèi nǚshì shì wǒmen de xīn tóngshì.", "meaningVi": "Vị quý bà này là đồng nghiệp mới của chúng tôi."}],
    "hsk1_156": [{"chinese": "他是我最好的朋友。", "pinyin": "Tā shì wǒ zuì hǎo de péngyou.", "meaningVi": "Anh ấy là người bạn tốt nhất của tôi."}],
    "hsk1_157": [{"chinese": "这里的水果很便宜。", "pinyin": "Zhèlǐ de shuǐguǒ hěn piányi.", "meaningVi": "Hoa quả ở đây rất rẻ."}],
    "hsk1_158": [{"chinese": "她今天穿得很漂亮。", "pinyin": "Tā jīntiān chuān de hěn piàoliang.", "meaningVi": "Hôm nay cô ấy mặc rất đẹp."}],
    "hsk1_159": [{"chinese": "我想吃一个苹果。", "pinyin": "Wǒ xiǎng chī yí gè píngguǒ.", "meaningVi": "Tôi muốn ăn một quả táo."}],
    "hsk1_160": [{"chinese": "一个星期有七天。", "pinyin": "Yí gè xīngqī yǒu qī tiān.", "meaningVi": "Một tuần có bảy ngày."}],
    "hsk1_161": [{"chinese": "我每天七点起床。", "pinyin": "Wǒ měitiān qī diǎn qǐchuáng.", "meaningVi": "Mỗi ngày tôi thức dậy lúc bảy giờ."}],
    "hsk1_162": [{"chinese": "这台电脑要五千块钱。", "pinyin": "Zhè tái diànnǎo yào wǔqiān kuài qián.", "meaningVi": "Chiếc máy tính này giá năm nghìn tệ."}],
    "hsk1_163": [{"chinese": "三年前我住在上海。", "pinyin": "Sān nián qián wǒ zhù zài Shànghǎi.", "meaningVi": "Ba năm trước tôi sống ở Thượng Hải."}],
    "hsk1_164": [{"chinese": "你有多少钱？", "pinyin": "Nǐ yǒu duōshao qián?", "meaningVi": "Bạn có bao nhiêu tiền?"}],
    "hsk1_165": [{"chinese": "请坐。", "pinyin": "Qǐng zuò.", "meaningVi": "Mời ngồi."}],
    "hsk1_166": [{"chinese": "请问，洗手间在哪里？", "pinyin": "Qǐngwèn, xǐshǒujiān zài nǎlǐ?", "meaningVi": "Xin hỏi, nhà vệ sinh ở đâu?"}],
    "hsk1_167": [{"chinese": "我们去公园吧。", "pinyin": "Wǒmen qù gōngyuán ba.", "meaningVi": "Chúng ta đi công viên đi."}],
    "hsk1_168": [{"chinese": "去年我去了日本。", "pinyin": "Qùnián wǒ qùle Rìběn.", "meaningVi": "Năm ngoái tôi đã đi Nhật Bản."}],
    "hsk1_169": [{"chinese": "夏天的天气很热。", "pinyin": "Xiàtiān de tiānqì hěn rè.", "meaningVi": "Thời tiết mùa hè rất nóng."}],
    "hsk1_170": [{"chinese": "这个房间里有很多人。", "pinyin": "Zhège fángjiān lǐ yǒu hěn duō rén.", "meaningVi": "Trong phòng này có rất nhiều người."}],
    "hsk1_171": [{"chinese": "我不认识他。", "pinyin": "Wǒ bú rènshi tā.", "meaningVi": "Tôi không quen anh ấy."}],
    "hsk1_172": [{"chinese": "今天是五月一日。", "pinyin": "Jīntiān shì wǔ yuè yī rì.", "meaningVi": "Hôm nay là ngày một tháng năm."}],
    "hsk1_173": [{"chinese": "我家有三口人。", "pinyin": "Wǒ jiā yǒu sān kǒu rén.", "meaningVi": "Nhà tôi có ba người."}],
    "hsk1_174": [{"chinese": "这家商店九点开门。", "pinyin": "Zhè jiā shāngdiàn jiǔ diǎn kāimén.", "meaningVi": "Cửa hàng này mở cửa lúc chín giờ."}],
    "hsk1_176": [{"chinese": "我每天九点上班。", "pinyin": "Wǒ měitiān jiǔ diǎn shàngbān.", "meaningVi": "Mỗi ngày tôi đi làm lúc chín giờ."}],
    "hsk1_177": [{"chinese": "我们八点上课。", "pinyin": "Wǒmen bā diǎn shàngkè.", "meaningVi": "Chúng tôi vào lớp lúc tám giờ."}],
    "hsk1_178": [{"chinese": "我上午有一节课。", "pinyin": "Wǒ shàngwǔ yǒu yì jié kè.", "meaningVi": "Buổi sáng tôi có một tiết học."}],
    "hsk1_179": [{"chinese": "我弟弟明年上学。", "pinyin": "Wǒ dìdi míngnián shàngxué.", "meaningVi": "Em trai tôi sang năm đi học."}],
    "hsk1_181": [{"chinese": "这是谁的手机？", "pinyin": "Zhè shì shéi de shǒujī?", "meaningVi": "Đây là điện thoại của ai?"}],
    "hsk1_182": [{"chinese": "你想吃什么？", "pinyin": "Nǐ xiǎng chī shénme?", "meaningVi": "Bạn muốn ăn gì?"}],
    "hsk1_183": [{"chinese": "他生病了，没来上课。", "pinyin": "Tā shēngbìng le, méi lái shàngkè.", "meaningVi": "Anh ấy bị ốm, không đến lớp."}],
    "hsk1_184": [{"chinese": "我们班有十个学生。", "pinyin": "Wǒmen bān yǒu shí gè xuéshēng.", "meaningVi": "Lớp chúng tôi có mười học sinh."}],
    "hsk1_185": [{"chinese": "你什么时候回来？", "pinyin": "Nǐ shénme shíhou huílái?", "meaningVi": "Khi nào bạn về?"}],
    "hsk1_186": [{"chinese": "我没有时间。", "pinyin": "Wǒ méiyǒu shíjiān.", "meaningVi": "Tôi không có thời gian."}],
    "hsk1_187": [{"chinese": "他有点事要办。", "pinyin": "Tā yǒudiǎn shì yào bàn.", "meaningVi": "Anh ấy có việc cần giải quyết."}],
    "hsk1_188": [{"chinese": "我是越南人。", "pinyin": "Wǒ shì Yuènán rén.", "meaningVi": "Tôi là người Việt Nam."}],
    "hsk1_189": [{"chinese": "我的手机没电了。", "pinyin": "Wǒ de shǒujī méi diàn le.", "meaningVi": "Điện thoại của tôi hết pin rồi."}],
    "hsk1_190": [{"chinese": "图书馆里有很多书。", "pinyin": "Túshūguǎn lǐ yǒu hěn duō shū.", "meaningVi": "Trong thư viện có rất nhiều sách."}],
    "hsk1_191": [{"chinese": "我在书店买了两本书。", "pinyin": "Wǒ zài shūdiàn mǎile liǎng běn shū.", "meaningVi": "Tôi đã mua hai cuốn sách ở hiệu sách."}],
    "hsk1_192": [{"chinese": "请给我一杯水。", "pinyin": "Qǐng gěi wǒ yì bēi shuǐ.", "meaningVi": "Xin cho tôi một cốc nước."}],
    "hsk1_193": [{"chinese": "我每天都吃水果。", "pinyin": "Wǒ měitiān dōu chī shuǐguǒ.", "meaningVi": "Tôi ăn trái cây mỗi ngày."}],
    "hsk1_194": [{"chinese": "我昨晚睡得很晚。", "pinyin": "Wǒ zuówǎn shuì de hěn wǎn.", "meaningVi": "Tối qua tôi ngủ rất muộn."}],
    "hsk1_195": [{"chinese": "我十一点睡觉。", "pinyin": "Wǒ shíyī diǎn shuìjiào.", "meaningVi": "Tôi đi ngủ lúc mười một giờ."}],
    "hsk1_196": [{"chinese": "请再说一遍。", "pinyin": "Qǐng zài shuō yí biàn.", "meaningVi": "Xin nói lại một lần nữa."}],
    "hsk1_197": [{"chinese": "上课的时候不要说话。", "pinyin": "Shàngkè de shíhou búyào shuōhuà.", "meaningVi": "Khi học không được nói chuyện."}],
    "hsk1_198": [{"chinese": "现在是四月。", "pinyin": "Xiànzài shì sì yuè.", "meaningVi": "Bây giờ là tháng Tư."}],
    "hsk1_199": [{"chinese": "我女儿三岁了。", "pinyin": "Wǒ nǚ'ér sān suì le.", "meaningVi": "Con gái tôi ba tuổi rồi."}],
    "hsk1_200": [{"chinese": "他是我的同学。", "pinyin": "Tā shì wǒ de tóngxué.", "meaningVi": "Anh ấy là bạn học của tôi."}],
    "hsk1_201": [{"chinese": "这只猫，它很可爱。", "pinyin": "Zhè zhī māo, tā hěn kě'ài.", "meaningVi": "Con mèo này, nó rất đáng yêu."}],
    "hsk1_202": [{"chinese": "她是我姐姐。", "pinyin": "Tā shì wǒ jiějie.", "meaningVi": "Cô ấy là chị gái tôi."}],
    "hsk1_203": [{"chinese": "他们是我的朋友。", "pinyin": "Tāmen shì wǒ de péngyou.", "meaningVi": "Họ là bạn của tôi."}],
    "hsk1_204": [{"chinese": "这些书，它们都是我的。", "pinyin": "Zhèxiē shū, tāmen dōu shì wǒ de.", "meaningVi": "Những cuốn sách này, chúng đều là của tôi."}],
    "hsk1_205": [{"chinese": "她们都是护士。", "pinyin": "Tāmen dōu shì hùshi.", "meaningVi": "Họ đều là y tá."}],
    "hsk1_206": [{"chinese": "今天太热了。", "pinyin": "Jīntiān tài rè le.", "meaningVi": "Hôm nay nóng quá."}],
    "hsk1_208": [{"chinese": "今天天气怎么样？", "pinyin": "Jīntiān tiānqì zěnmeyàng?", "meaningVi": "Hôm nay thời tiết thế nào?"}],
    "hsk1_209": [{"chinese": "我喜欢听音乐。", "pinyin": "Wǒ xǐhuan tīng yīnyuè.", "meaningVi": "Tôi thích nghe nhạc."}],
    "hsk1_210": [{"chinese": "你听见了吗？", "pinyin": "Nǐ tīngjiàn le ma?", "meaningVi": "Bạn nghe thấy chưa?"}],
    "hsk1_211": [{"chinese": "他是我的大学同学。", "pinyin": "Tā shì wǒ de dàxué tóngxué.", "meaningVi": "Anh ấy là bạn học đại học của tôi."}],
    "hsk1_212": [{"chinese": "教室外有很多学生。", "pinyin": "Jiàoshì wài yǒu hěn duō xuéshēng.", "meaningVi": "Bên ngoài lớp học có rất nhiều học sinh."}],
    "hsk1_213": [{"chinese": "外边在下雨。", "pinyin": "Wàibian zài xià yǔ.", "meaningVi": "Bên ngoài đang mưa."}],
    "hsk1_214": [{"chinese": "孩子们在外边玩。", "pinyin": "Háizimen zài wàibian wán.", "meaningVi": "Bọn trẻ đang chơi bên ngoài."}],
    "hsk1_215": [{"chinese": "现在已经很晚了。", "pinyin": "Xiànzài yǐjīng hěn wǎn le.", "meaningVi": "Bây giờ đã rất muộn rồi."}],
    "hsk1_216": [{"chinese": "我们六点吃晚饭。", "pinyin": "Wǒmen liù diǎn chī wǎnfàn.", "meaningVi": "Chúng tôi ăn tối lúc sáu giờ."}],
    "hsk1_217": [{"chinese": "晚上我常常看书。", "pinyin": "Wǎnshang wǒ chángcháng kàn shū.", "meaningVi": "Buổi tối tôi thường đọc sách."}],
    "hsk1_218": [{"chinese": "喂，请问是王先生吗？", "pinyin": "Wèi, qǐngwèn shì Wáng xiānsheng ma?", "meaningVi": "Alo, xin hỏi có phải anh Vương không?"}],
    "hsk1_219": [{"chinese": "我想问你一个问题。", "pinyin": "Wǒ xiǎng wèn nǐ yí gè wèntí.", "meaningVi": "Tôi muốn hỏi bạn một câu hỏi."}],
    "hsk1_220": [{"chinese": "这个问题很难。", "pinyin": "Zhège wèntí hěn nán.", "meaningVi": "Câu hỏi này rất khó."}],
    "hsk1_221": [{"chinese": "我是老师。", "pinyin": "Wǒ shì lǎoshī.", "meaningVi": "Tôi là giáo viên."}],
    "hsk1_222": [{"chinese": "我们明天见。", "pinyin": "Wǒmen míngtiān jiàn.", "meaningVi": "Chúng ta gặp nhau ngày mai."}],
    "hsk1_223": [{"chinese": "我们五个人一起去。", "pinyin": "Wǒmen wǔ gè rén yìqǐ qù.", "meaningVi": "Năm người chúng tôi cùng đi."}],
    "hsk1_224": [{"chinese": "我们十二点吃午饭。", "pinyin": "Wǒmen shí'èr diǎn chī wǔfàn.", "meaningVi": "Chúng tôi ăn trưa lúc mười hai giờ."}],
    "hsk1_225": [{"chinese": "我很喜欢这本书。", "pinyin": "Wǒ hěn xǐhuan zhè běn shū.", "meaningVi": "Tôi rất thích cuốn sách này."}],
    "hsk1_227": [{"chinese": "今天下雨了。", "pinyin": "Jīntiān xià yǔ le.", "meaningVi": "Hôm nay trời mưa rồi."}],
    "hsk1_228": [{"chinese": "我六点下班。", "pinyin": "Wǒ liù diǎn xiàbān.", "meaningVi": "Tôi tan làm lúc sáu giờ."}],
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
