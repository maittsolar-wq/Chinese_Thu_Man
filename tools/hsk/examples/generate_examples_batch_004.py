"""P5.10.3 (continued) -- Batch 004 (continues immediately after
examples_batch_003.json; spans the tail of HSK1's eligible pool into
the start of HSK2's).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Usage:
    python generate_examples_batch_004.py --dry-run
    python generate_examples_batch_004.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 4
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_004.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk1_229": [{"chinese": "我们十二点下课。", "pinyin": "Wǒmen shí'èr diǎn xiàkè.", "meaningVi": "Chúng tôi tan học lúc mười hai giờ."}],
    "hsk1_230": [{"chinese": "下午我要去图书馆。", "pinyin": "Xiàwǔ wǒ yào qù túshūguǎn.", "meaningVi": "Buổi chiều tôi sẽ đi thư viện."}],
    "hsk1_231": [{"chinese": "这位是王先生。", "pinyin": "Zhè wèi shì Wáng xiānsheng.", "meaningVi": "Đây là ông Vương."}],
    "hsk1_232": [{"chinese": "现在我很忙。", "pinyin": "Xiànzài wǒ hěn máng.", "meaningVi": "Bây giờ tôi rất bận."}],
    "hsk1_233": [
        {"chinese": "我想去中国旅游。", "pinyin": "Wǒ xiǎng qù Zhōngguó lǚyóu.", "meaningVi": "Tôi muốn đi Trung Quốc du lịch."},
        {"chinese": "我很想家。", "pinyin": "Wǒ hěn xiǎng jiā.", "meaningVi": "Tôi rất nhớ nhà."},
    ],
    "hsk1_235": [{"chinese": "公园里有很多小朋友在玩。", "pinyin": "Gōngyuán lǐ yǒu hěn duō xiǎopéngyǒu zài wán.", "meaningVi": "Trong công viên có rất nhiều trẻ em đang chơi."}],
    "hsk1_236": [{"chinese": "从这儿到机场要一个小时。", "pinyin": "Cóng zhèr dào jīchǎng yào yí gè xiǎoshí.", "meaningVi": "Từ đây đến sân bay mất một tiếng."}],
    "hsk1_237": [{"chinese": "这所小学很有名。", "pinyin": "Zhè suǒ xiǎoxué hěn yǒumíng.", "meaningVi": "Trường tiểu học này rất nổi tiếng."}],
    "hsk1_238": [{"chinese": "小学生们放学了。", "pinyin": "Xiǎoxuéshēngmen fàngxué le.", "meaningVi": "Các học sinh tiểu học đã tan học."}],
    "hsk1_239": [{"chinese": "我买了一些水果。", "pinyin": "Wǒ mǎile yìxiē shuǐguǒ.", "meaningVi": "Tôi đã mua một ít trái cây."}],
    "hsk1_240": [{"chinese": "请写下你的名字。", "pinyin": "Qǐng xiěxià nǐ de míngzi.", "meaningVi": "Xin viết tên của bạn xuống."}],
    "hsk1_241": [{"chinese": "谢谢你的帮助。", "pinyin": "Xièxie nǐ de bāngzhù.", "meaningVi": "Cảm ơn sự giúp đỡ của bạn."}],
    "hsk1_242": [{"chinese": "我买了一部新手机。", "pinyin": "Wǒ mǎile yí bù xīn shǒujī.", "meaningVi": "Tôi đã mua một chiếc điện thoại mới."}],
    "hsk1_243": [{"chinese": "这个星期我很忙。", "pinyin": "Zhège xīngqī wǒ hěn máng.", "meaningVi": "Tuần này tôi rất bận."}],
    "hsk1_244": [{"chinese": "星期日我不用上班。", "pinyin": "Xīngqīrì wǒ búyòng shàngbān.", "meaningVi": "Chủ nhật tôi không cần đi làm."}],
    "hsk1_245": [{"chinese": "我们星期天去爬山吧。", "pinyin": "Wǒmen xīngqītiān qù páshān ba.", "meaningVi": "Chủ nhật chúng ta đi leo núi đi."}],
    "hsk1_246": [{"chinese": "你累了就休息一下吧。", "pinyin": "Nǐ lèi le jiù xiūxi yíxià ba.", "meaningVi": "Nếu bạn mệt thì nghỉ ngơi một chút đi."}],
    "hsk1_247": [{"chinese": "他在学开车。", "pinyin": "Tā zài xué kāichē.", "meaningVi": "Anh ấy đang học lái xe."}],
    "hsk1_248": [{"chinese": "她是一个好学生。", "pinyin": "Tā shì yí gè hǎo xuéshēng.", "meaningVi": "Cô ấy là một học sinh giỏi."}],
    "hsk1_249": [{"chinese": "他每天都努力学习。", "pinyin": "Tā měitiān dōu nǔlì xuéxí.", "meaningVi": "Anh ấy học tập chăm chỉ mỗi ngày."}],
    "hsk1_250": [{"chinese": "我们学校很大。", "pinyin": "Wǒmen xuéxiào hěn dà.", "meaningVi": "Trường chúng tôi rất rộng."}],
    "hsk1_251": [{"chinese": "冬天这里常常下雪。", "pinyin": "Dōngtiān zhèlǐ chángcháng xiàxuě.", "meaningVi": "Mùa đông ở đây thường có tuyết rơi."}],
    "hsk1_252": [{"chinese": "我要一杯咖啡。", "pinyin": "Wǒ yào yì bēi kāfēi.", "meaningVi": "Tôi muốn một cốc cà phê."}],
    "hsk1_253": [{"chinese": "我也喜欢喝茶。", "pinyin": "Wǒ yě xǐhuan hē chá.", "meaningVi": "Tôi cũng thích uống trà."}],
    "hsk1_254": [{"chinese": "桌子上有一本书。", "pinyin": "Zhuōzi shàng yǒu yì běn shū.", "meaningVi": "Trên bàn có một cuốn sách."}],
    "hsk1_255": [{"chinese": "这件衣服是新买的。", "pinyin": "Zhè jiàn yīfu shì xīn mǎi de.", "meaningVi": "Chiếc áo này mới mua."}],
    "hsk1_256": [{"chinese": "他想当医生。", "pinyin": "Tā xiǎng dāng yīshēng.", "meaningVi": "Anh ấy muốn trở thành bác sĩ."}],
    "hsk1_257": [{"chinese": "医院离这儿不远。", "pinyin": "Yīyuàn lí zhèr bù yuǎn.", "meaningVi": "Bệnh viện cách đây không xa."}],
    "hsk1_258": [{"chinese": "他把苹果分给我一半。", "pinyin": "Tā bǎ píngguǒ fēn gěi wǒ yíbàn.", "meaningVi": "Anh ấy chia cho tôi một nửa quả táo."}],
    "hsk1_259": [{"chinese": "请等一下。", "pinyin": "Qǐng děng yíxià.", "meaningVi": "Xin đợi một chút."}],
    "hsk1_260": [{"chinese": "这把椅子很舒服。", "pinyin": "Zhè bǎ yǐzi hěn shūfu.", "meaningVi": "Chiếc ghế này rất thoải mái."}],
    "hsk1_261": [{"chinese": "请再给我一点儿时间。", "pinyin": "Qǐng zài gěi wǒ yìdiǎnr shíjiān.", "meaningVi": "Xin cho tôi thêm một chút thời gian."}],
    "hsk1_262": [{"chinese": "我给你带了一些礼物。", "pinyin": "Wǒ gěi nǐ dàile yìxiē lǐwù.", "meaningVi": "Tôi mang cho bạn một ít quà."}],
    "hsk1_263": [{"chinese": "我有一个哥哥。", "pinyin": "Wǒ yǒu yí gè gēge.", "meaningVi": "Tôi có một anh trai."}],
    "hsk1_264": [{"chinese": "有的人喜欢咖啡，有的人喜欢茶。", "pinyin": "Yǒude rén xǐhuan kāfēi, yǒude rén xǐhuan chá.", "meaningVi": "Có người thích cà phê, có người thích trà."}],
    "hsk1_265": [{"chinese": "这件衣服有点儿贵。", "pinyin": "Zhè jiàn yīfu yǒudiǎnr guì.", "meaningVi": "Chiếc áo này hơi đắt."}],
    "hsk1_266": [{"chinese": "有些问题我还不明白。", "pinyin": "Yǒuxiē wèntí wǒ hái bù míngbai.", "meaningVi": "Có một số câu hỏi tôi vẫn chưa hiểu."}],
    "hsk1_267": [{"chinese": "外面的雨很大。", "pinyin": "Wàimiàn de yǔ hěn dà.", "meaningVi": "Mưa bên ngoài rất to."}],
    "hsk1_268": [{"chinese": "这本书二十元。", "pinyin": "Zhè běn shū èrshí yuán.", "meaningVi": "Cuốn sách này hai mươi đồng."}],
    "hsk1_269": [{"chinese": "我下个月要去北京。", "pinyin": "Wǒ xià gè yuè yào qù Běijīng.", "meaningVi": "Tháng sau tôi sẽ đi Bắc Kinh."}],
    "hsk1_270": [{"chinese": "你能再说一次吗？", "pinyin": "Nǐ néng zài shuō yí cì ma?", "meaningVi": "Bạn có thể nói lại một lần nữa không?"}],
    "hsk1_272": [{"chinese": "再见，明天见！", "pinyin": "Zàijiàn, míngtiān jiàn!", "meaningVi": "Tạm biệt, hẹn gặp lại ngày mai!"}],
    "hsk1_273": [{"chinese": "你今天来得很早。", "pinyin": "Nǐ jīntiān lái de hěn zǎo.", "meaningVi": "Hôm nay bạn đến sớm."}],
    "hsk1_274": [{"chinese": "我很少吃早饭。", "pinyin": "Wǒ hěn shǎo chī zǎofàn.", "meaningVi": "Tôi ít khi ăn sáng."}],
    "hsk1_275": [{"chinese": "早上的空气很新鲜。", "pinyin": "Zǎoshang de kōngqì hěn xīnxiān.", "meaningVi": "Không khí buổi sáng rất trong lành."}],
    "hsk1_276": [{"chinese": "这个字怎么读？", "pinyin": "Zhège zì zěnme dú?", "meaningVi": "Chữ này đọc thế nào?"}],
    "hsk1_277": [{"chinese": "我们明天去看电影，怎么样？", "pinyin": "Wǒmen míngtiān qù kàn diànyǐng, zěnmeyàng?", "meaningVi": "Ngày mai chúng ta đi xem phim, được không?"}],
    "hsk1_278": [{"chinese": "我在找我的钥匙。", "pinyin": "Wǒ zài zhǎo wǒ de yàoshi.", "meaningVi": "Tôi đang tìm chìa khóa của tôi."}],
    "hsk1_279": [{"chinese": "这是什么？", "pinyin": "Zhè shì shénme?", "meaningVi": "Đây là cái gì?"}],
    "hsk1_280": [{"chinese": "请走这边。", "pinyin": "Qǐng zǒu zhèbiān.", "meaningVi": "Xin đi bên này."}],
    "hsk1_281": [{"chinese": "这个比那个好。", "pinyin": "Zhège bǐ nàge hǎo.", "meaningVi": "Cái này tốt hơn cái kia."}],
    "hsk1_282": [{"chinese": "这里的风景很美。", "pinyin": "Zhèlǐ de fēngjǐng hěn měi.", "meaningVi": "Phong cảnh ở đây rất đẹp."}],
    "hsk1_283": [{"chinese": "请到这儿来。", "pinyin": "Qǐng dào zhèr lái.", "meaningVi": "Xin đến đây."}],
    "hsk1_284": [{"chinese": "这些照片都很好看。", "pinyin": "Zhèxiē zhàopiàn dōu hěn hǎokàn.", "meaningVi": "Những bức ảnh này đều rất đẹp."}],
    "hsk1_285": [{"chinese": "你真聪明。", "pinyin": "Nǐ zhēn cōngming.", "meaningVi": "Bạn thật thông minh."}],
    "hsk1_286": [{"chinese": "妈妈正在做饭。", "pinyin": "Māma zhèngzài zuò fàn.", "meaningVi": "Mẹ đang nấu cơm."}],
    "hsk1_288": [{"chinese": "我不知道他在哪里。", "pinyin": "Wǒ bù zhīdào tā zài nǎlǐ.", "meaningVi": "Tôi không biết anh ấy ở đâu."}],
    "hsk1_289": [{"chinese": "我来自中国。", "pinyin": "Wǒ láizì Zhōngguó.", "meaningVi": "Tôi đến từ Trung Quốc."}],
    "hsk1_290": [{"chinese": "他的中文说得很好。", "pinyin": "Tā de Zhōngwén shuō de hěn hǎo.", "meaningVi": "Tiếng Trung của anh ấy nói rất tốt."}],
    "hsk1_291": [{"chinese": "中午我们去哪儿吃饭？", "pinyin": "Zhōngwǔ wǒmen qù nǎr chīfàn?", "meaningVi": "Buổi trưa chúng ta đi đâu ăn cơm?"}],
    "hsk1_292": [{"chinese": "我在这所中学教书。", "pinyin": "Wǒ zài zhè suǒ zhōngxué jiāoshū.", "meaningVi": "Tôi dạy học ở trường trung học này."}],
    "hsk1_293": [{"chinese": "中学生的学习压力很大。", "pinyin": "Zhōngxuéshēng de xuéxí yālì hěn dà.", "meaningVi": "Áp lực học tập của học sinh trung học rất lớn."}],
    "hsk1_294": [{"chinese": "你住在哪儿？", "pinyin": "Nǐ zhù zài nǎr?", "meaningVi": "Bạn sống ở đâu?"}],
    "hsk1_295": [{"chinese": "桌子上放着一杯咖啡。", "pinyin": "Zhuōzi shàng fàngzhe yì bēi kāfēi.", "meaningVi": "Trên bàn đặt một cốc cà phê."}],
    "hsk1_296": [{"chinese": "他写的字很漂亮。", "pinyin": "Tā xiě de zì hěn piàoliang.", "meaningVi": "Chữ anh ấy viết rất đẹp."}],
    "hsk1_297": [{"chinese": "昨天我没去上班。", "pinyin": "Zuótiān wǒ méi qù shàngbān.", "meaningVi": "Hôm qua tôi không đi làm."}],
    "hsk1_298": [{"chinese": "请坐在这把椅子上。", "pinyin": "Qǐng zuò zài zhè bǎ yǐzi shàng.", "meaningVi": "Xin ngồi vào chiếc ghế này."}],
    "hsk1_299": [{"chinese": "你在做什么？", "pinyin": "Nǐ zài zuò shénme?", "meaningVi": "Bạn đang làm gì?"}],
    "hsk1_300": [{"chinese": "我妈妈很会做饭。", "pinyin": "Wǒ māma hěn huì zuò fàn.", "meaningVi": "Mẹ tôi rất giỏi nấu ăn."}],
    "hsk2_040": [{"chinese": "小鸟在天上飞。", "pinyin": "Xiǎo niǎo zài tiānshàng fēi.", "meaningVi": "Con chim nhỏ đang bay trên trời."}],
    "hsk2_046": [{"chinese": "我每天坐公交车上班。", "pinyin": "Wǒ měitiān zuò gōngjiāochē shàngbān.", "meaningVi": "Tôi đi xe buýt đi làm mỗi ngày."}],
    "hsk2_053": [{"chinese": "他喜欢穿黑色的衣服。", "pinyin": "Tā xǐhuan chuān hēisè de yīfu.", "meaningVi": "Anh ấy thích mặc quần áo màu đen."}],
    "hsk2_054": [{"chinese": "我早上喜欢喝红茶。", "pinyin": "Wǒ zǎoshang xǐhuan hē hóngchá.", "meaningVi": "Buổi sáng tôi thích uống trà đen."}],
    "hsk2_055": [{"chinese": "中国国旗是红色的。", "pinyin": "Zhōngguó guóqí shì hóngsè de.", "meaningVi": "Quốc kỳ Trung Quốc màu đỏ."}],
    "hsk2_063": [{"chinese": "我去机场接朋友。", "pinyin": "Wǒ qù jīchǎng jiē péngyou.", "meaningVi": "Tôi đi sân bay đón bạn."}],
    "hsk2_064": [{"chinese": "我在网上买了机票。", "pinyin": "Wǒ zài wǎngshàng mǎile jīpiào.", "meaningVi": "Tôi đã mua vé máy bay trên mạng."}],
    "hsk2_067": [{"chinese": "她教我们数学。", "pinyin": "Tā jiāo wǒmen shùxué.", "meaningVi": "Cô ấy dạy toán cho chúng tôi."}],
    "hsk2_069": [{"chinese": "请介绍一下你自己。", "pinyin": "Qǐng jièshào yíxià nǐ zìjǐ.", "meaningVi": "Xin giới thiệu bản thân một chút."}],
    "hsk2_071": [{"chinese": "学校离我家很近。", "pinyin": "Xuéxiào lí wǒ jiā hěn jìn.", "meaningVi": "Trường học cách nhà tôi rất gần."}],
    "hsk2_075": [{"chinese": "我们住在一家五星级酒店。", "pinyin": "Wǒmen zhù zài yì jiā wǔxīngjí jiǔdiàn.", "meaningVi": "Chúng tôi ở một khách sạn năm sao."}],
    "hsk2_077": [{"chinese": "这家店的咖啡很香。", "pinyin": "Zhè jiā diàn de kāfēi hěn xiāng.", "meaningVi": "Cà phê của cửa hàng này rất thơm."}],
    "hsk2_083": [{"chinese": "这条裤子有点儿长。", "pinyin": "Zhè tiáo kùzi yǒudiǎnr cháng.", "meaningVi": "Chiếc quần này hơi dài."}],
    "hsk2_087": [{"chinese": "他每周都打篮球。", "pinyin": "Tā měi zhōu dōu dǎ lánqiú.", "meaningVi": "Anh ấy chơi bóng rổ mỗi tuần."}],
    "hsk2_089": [{"chinese": "我家离公司不远。", "pinyin": "Wǒ jiā lí gōngsī bù yuǎn.", "meaningVi": "Nhà tôi cách công ty không xa."}],
    "hsk2_094": [{"chinese": "暑假我们去云南旅游。", "pinyin": "Shǔjià wǒmen qù Yúnnán lǚyóu.", "meaningVi": "Kỳ nghỉ hè chúng tôi đi Vân Nam du lịch."}],
    "hsk2_095": [{"chinese": "绿茶对身体很好。", "pinyin": "Lǜchá duì shēntǐ hěn hǎo.", "meaningVi": "Trà xanh rất tốt cho sức khỏe."}],
    "hsk2_108": [{"chinese": "年轻人都喜欢喝奶茶。", "pinyin": "Niánqīngrén dōu xǐhuan hē nǎichá.", "meaningVi": "Người trẻ đều thích uống trà sữa."}],
    "hsk2_109": [{"chinese": "我奶奶今年八十岁了。", "pinyin": "Wǒ nǎinai jīnnián bāshí suì le.", "meaningVi": "Bà nội tôi năm nay tám mươi tuổi rồi."}],
    "hsk2_111": [{"chinese": "树上有很多小鸟。", "pinyin": "Shù shàng yǒu hěn duō xiǎo niǎo.", "meaningVi": "Trên cây có rất nhiều chim nhỏ."}],
    "hsk2_114": [{"chinese": "他跑得很快。", "pinyin": "Tā pǎo de hěn kuài.", "meaningVi": "Anh ấy chạy rất nhanh."}],
    "hsk2_115": [{"chinese": "她喜欢在公园跑步。", "pinyin": "Tā xǐhuan zài gōngyuán pǎobù.", "meaningVi": "Cô ấy thích chạy bộ trong công viên."}],
    "hsk2_117": [{"chinese": "他妻子是老师。", "pinyin": "Tā qīzi shì lǎoshī.", "meaningVi": "Vợ anh ấy là giáo viên."}],
    "hsk2_123": [{"chinese": "我不太喜欢吃肉。", "pinyin": "Wǒ bú tài xǐhuan chī ròu.", "meaningVi": "Tôi không thích ăn thịt lắm."}],
    "hsk2_130": [{"chinese": "今天是我的生日。", "pinyin": "Jīntiān shì wǒ de shēngrì.", "meaningVi": "Hôm nay là sinh nhật của tôi."}],
    "hsk2_134": [{"chinese": "这块手表是爸爸送我的。", "pinyin": "Zhè kuài shǒubiǎo shì bàba sòng wǒ de.", "meaningVi": "Chiếc đồng hồ này là bố tặng tôi."}],
    "hsk2_152": [{"chinese": "我忘了带钥匙。", "pinyin": "Wǒ wàngle dài yàoshi.", "meaningVi": "Tôi quên mang chìa khóa."}],
    "hsk2_153": [{"chinese": "这位是我们的新老师。", "pinyin": "Zhè wèi shì wǒmen de xīn lǎoshī.", "meaningVi": "Vị này là giáo viên mới của chúng tôi."}],
    "hsk2_163": [{"chinese": "她笑得很开心。", "pinyin": "Tā xiào de hěn kāixīn.", "meaningVi": "Cô ấy cười rất vui vẻ."}],
    "hsk2_166": [{"chinese": "你最喜欢什么颜色？", "pinyin": "Nǐ zuì xǐhuan shénme yánsè?", "meaningVi": "Bạn thích màu gì nhất?"}],
    "hsk2_168": [{"chinese": "医生给我开了一些药。", "pinyin": "Yīshēng gěi wǒ kāile yìxiē yào.", "meaningVi": "Bác sĩ đã kê cho tôi một ít thuốc."}],
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
