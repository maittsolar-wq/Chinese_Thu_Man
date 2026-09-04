"""P5.10.3 (continued) -- Batch 013 (continues immediately after
examples_batch_012.json; entirely within HSK4).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Extra care applied in this batch -- three same-pinyin-different-
character pairs, none flagged by the mechanical tier system (which
compares the `word` string, and these are different words):
  - 难 (nán, "difficult") in 难道/难受/难忘 vs 男 (nán, "male") in
    男士/男性: identical pinyin, unrelated characters/meanings, each
    demonstrated in its own unambiguous natural compound.
  - 皮 (pí, "skin/leather") in 皮肤/皮鞋 vs 脾 (pí, "temperament", as
    in 脾气) : identical pinyin, unrelated characters.
  - 气 (qì, "air/gas") in 气候/气温 vs 汽 (qì, "steam/vapor", as in
    汽水/汽车) : identical pinyin, unrelated characters.

Other productive-root families kept structurally distinct (no shared
template): 美/美好/美景/美丽/美食 (měi+X); 母女/母亲/母子 (mǔ+X);
目标/目的/目的地/目前 (mù+X); 内/内容/内心 (nèi+X); 能否/能够/能力
(néng+X); 排队/排球/牌/牌子 (pái+X); 普遍/普通/普通话 (pǔ+X);
期/期末/期中 (qī+X); 前方/前后 (qián+X); 全部/全都/全球/全身
(quán+X); 缺/缺点/缺少 (quē+X); 取/取得/取消 (qǔ+X).

Cross-batch collision found and fixed during authoring: the first
draft of hsk4_500 (美) reused "这里的风景真美。" verbatim from
examples_batch_010.json's hsk4_205 (风景). Rewritten to "这幅画真美。"
before this batch was finalized; re-verified against the full
pilot+002-012 corpus with zero remaining collisions.

Usage:
    python generate_examples_batch_013.py --dry-run
    python generate_examples_batch_013.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 13
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_013.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_487": [{"chinese": "我路过这里的时候看到了你。", "pinyin": "Wǒ lùguò zhèlǐ de shíhou kàndàole nǐ.", "meaningVi": "Khi tôi đi ngang qua đây thì nhìn thấy bạn."}],
    "hsk4_488": [{"chinese": "我们住在一家小旅馆。", "pinyin": "Wǒmen zhù zài yì jiā xiǎo lǚguǎn.", "meaningVi": "Chúng tôi ở tại một khách sạn nhỏ."}],
    "hsk4_489": [{"chinese": "旅客们正在排队登机。", "pinyin": "Lǚkèmen zhèngzài páiduì dēngjī.", "meaningVi": "Các hành khách đang xếp hàng lên máy bay."}],
    "hsk4_490": [{"chinese": "我打算暑假去旅行。", "pinyin": "Wǒ dǎsuàn shǔjià qù lǚxíng.", "meaningVi": "Tôi định đi du lịch vào kỳ nghỉ hè."}],
    "hsk4_491": [{"chinese": "他是一名律师。", "pinyin": "Tā shì yì míng lǜshī.", "meaningVi": "Anh ấy là một luật sư."}],
    "hsk4_495": [{"chinese": "早饭我吃了一个馒头。", "pinyin": "Zǎofàn wǒ chīle yí gè mántou.", "meaningVi": "Bữa sáng tôi ăn một cái bánh bao hấp."}],
    "hsk4_497": [{"chinese": "请把毛巾递给我。", "pinyin": "Qǐng bǎ máojīn dì gěi wǒ.", "meaningVi": "Xin đưa khăn mặt cho tôi."}],
    "hsk4_498": [{"chinese": "天冷了，穿上毛衣吧。", "pinyin": "Tiān lěng le, chuān shàng máoyī ba.", "meaningVi": "Trời lạnh rồi, mặc áo len vào đi."}],
    "hsk4_499": [{"chinese": "他戴着一顶帽子。", "pinyin": "Tā dàizhe yì dǐng màozi.", "meaningVi": "Anh ấy đội một cái mũ."}],
    "hsk4_500": [{"chinese": "这幅画真美。", "pinyin": "Zhè fú huà zhēn měi.", "meaningVi": "Bức tranh này thật đẹp."}],
    "hsk4_501": [{"chinese": "祝你有一个美好的未来。", "pinyin": "Zhù nǐ yǒu yí gè měihǎo de wèilái.", "meaningVi": "Chúc bạn có một tương lai tốt đẹp."}],
    "hsk4_502": [{"chinese": "大家都被这美景吸引住了。", "pinyin": "Dàjiā dōu bèi zhè měijǐng xīyǐn zhù le.", "meaningVi": "Mọi người đều bị cảnh đẹp này thu hút."}],
    "hsk4_503": [{"chinese": "她穿着一条美丽的裙子。", "pinyin": "Tā chuānzhe yì tiáo měilì de qúnzi.", "meaningVi": "Cô ấy mặc một chiếc váy xinh đẹp."}],
    "hsk4_504": [{"chinese": "这座城市有很多美食。", "pinyin": "Zhè zuò chéngshì yǒu hěn duō měishí.", "meaningVi": "Thành phố này có rất nhiều món ngon."}],
    "hsk4_507": [{"chinese": "我忘记密码了。", "pinyin": "Wǒ wàngjì mìmǎ le.", "meaningVi": "Tôi quên mật khẩu rồi."}],
    "hsk4_508": [{"chinese": "这里的停车是免费的。", "pinyin": "Zhèlǐ de tíngchē shì miǎnfèi de.", "meaningVi": "Đỗ xe ở đây là miễn phí."}],
    "hsk4_509": [{"chinese": "我们要勇敢面对困难。", "pinyin": "Wǒmen yào yǒnggǎn miànduì kùnnan.", "meaningVi": "Chúng ta phải dũng cảm đối mặt với khó khăn."}],
    "hsk4_510": [{"chinese": "明天我有一场面试。", "pinyin": "Míngtiān wǒ yǒu yì chǎng miànshì.", "meaningVi": "Ngày mai tôi có một buổi phỏng vấn."}],
    "hsk4_511": [{"chinese": "请等我三十秒。", "pinyin": "Qǐng děng wǒ sānshí miǎo.", "meaningVi": "Xin đợi tôi ba mươi giây."}],
    "hsk4_512": [{"chinese": "中国有五十六个民族。", "pinyin": "Zhōngguó yǒu wǔshíliù gè mínzú.", "meaningVi": "Trung Quốc có năm mươi sáu dân tộc."}],
    "hsk4_513": [{"chinese": "他打算月末去旅行。", "pinyin": "Tā dǎsuàn yuèmò qù lǚxíng.", "meaningVi": "Anh ấy định đi du lịch vào cuối tháng."}],
    "hsk4_514": [{"chinese": "她们是一对母女。", "pinyin": "Tāmen shì yí duì mǔnǚ.", "meaningVi": "Họ là một cặp mẹ con gái."}],
    "hsk4_515": [{"chinese": "母亲节快到了。", "pinyin": "Mǔqīnjié kuài dào le.", "meaningVi": "Ngày của Mẹ sắp đến rồi."}],
    "hsk4_516": [{"chinese": "这对母子感情很好。", "pinyin": "Zhè duì mǔzǐ gǎnqíng hěn hǎo.", "meaningVi": "Cặp mẹ con trai này tình cảm rất tốt."}],
    "hsk4_517": [{"chinese": "他为自己定了一个目标。", "pinyin": "Tā wèi zìjǐ dìngle yí gè mùbiāo.", "meaningVi": "Anh ấy đã đặt ra một mục tiêu cho bản thân."}],
    "hsk4_518": [{"chinese": "你学习中文的目的是什么？", "pinyin": "Nǐ xuéxí Zhōngwén de mùdì shì shénme?", "meaningVi": "Mục đích học tiếng Trung của bạn là gì?"}],
    "hsk4_519": [{"chinese": "我们终于到达了目的地。", "pinyin": "Wǒmen zhōngyú dàodále mùdìdì.", "meaningVi": "Chúng tôi cuối cùng đã đến được điểm đến."}],
    "hsk4_520": [{"chinese": "目前情况还比较稳定。", "pinyin": "Mùqián qíngkuàng hái bǐjiào wěndìng.", "meaningVi": "Hiện tại tình hình vẫn khá ổn định."}],
    "hsk4_522": [{"chinese": "他来自中国南部。", "pinyin": "Tā láizì Zhōngguó nánbù.", "meaningVi": "Anh ấy đến từ miền Nam Trung Quốc."}],
    "hsk4_523": [{"chinese": "难道你忘了吗？", "pinyin": "Nándào nǐ wàng le ma?", "meaningVi": "Chẳng lẽ bạn quên rồi sao?"}],
    "hsk4_524": [{"chinese": "这是男士专用的洗手间。", "pinyin": "Zhè shì nánshì zhuānyòng de xǐshǒujiān.", "meaningVi": "Đây là nhà vệ sinh dành riêng cho nam giới."}],
    "hsk4_525": [{"chinese": "我今天肚子有点难受。", "pinyin": "Wǒ jīntiān dùzi yǒudiǎn nánshòu.", "meaningVi": "Hôm nay bụng tôi hơi khó chịu."}],
    "hsk4_526": [{"chinese": "那是一次难忘的旅行。", "pinyin": "Nà shì yí cì nánwàng de lǚxíng.", "meaningVi": "Đó là một chuyến du lịch khó quên."}],
    "hsk4_527": [{"chinese": "这份工作男性女性都可以做。", "pinyin": "Zhè fèn gōngzuò nánxìng nǚxìng dōu kěyǐ zuò.", "meaningVi": "Công việc này cả nam giới lẫn nữ giới đều có thể làm."}],
    "hsk4_528": [{"chinese": "请在三天内回复。", "pinyin": "Qǐng zài sān tiān nèi huífù.", "meaningVi": "Xin phản hồi trong vòng ba ngày."}],
    "hsk4_529": [{"chinese": "这本书的内容很丰富。", "pinyin": "Zhè běn shū de nèiróng hěn fēngfù.", "meaningVi": "Nội dung của cuốn sách này rất phong phú."}],
    "hsk4_530": [{"chinese": "她内心很坚强。", "pinyin": "Tā nèixīn hěn jiānqiáng.", "meaningVi": "Nội tâm cô ấy rất mạnh mẽ."}],
    "hsk4_531": [{"chinese": "能否请你帮个忙？", "pinyin": "Néng fǒu qǐng nǐ bāng ge máng?", "meaningVi": "Liệu bạn có thể giúp tôi một việc được không?"}],
    "hsk4_532": [{"chinese": "我相信你能够做到。", "pinyin": "Wǒ xiāngxìn nǐ nénggòu zuòdào.", "meaningVi": "Tôi tin rằng bạn có thể làm được."}],
    "hsk4_533": [{"chinese": "他的工作能力很强。", "pinyin": "Tā de gōngzuò nénglì hěn qiáng.", "meaningVi": "Khả năng làm việc của anh ấy rất mạnh."}],
    "hsk4_534": [{"chinese": "嗯，我知道了。", "pinyin": "Ǹg, wǒ zhīdào le.", "meaningVi": "Ừ, tôi biết rồi."}],
    "hsk4_535": [{"chinese": "我们年底再见面吧。", "pinyin": "Wǒmen niándǐ zài jiànmiàn ba.", "meaningVi": "Chúng ta gặp lại nhau vào cuối năm nhé."}],
    "hsk4_536": [{"chinese": "请问您的年龄是多少？", "pinyin": "Qǐngwèn nín de niánlíng shì duōshao?", "meaningVi": "Xin hỏi tuổi của ông/bà là bao nhiêu?"}],
    "hsk4_537": [{"chinese": "他小时候住在农村。", "pinyin": "Tā xiǎoshíhou zhù zài nóngcūn.", "meaningVi": "Lúc nhỏ anh ấy sống ở nông thôn."}],
    "hsk4_538": [{"chinese": "别把衣服弄脏了。", "pinyin": "Bié bǎ yīfu nòngzāng le.", "meaningVi": "Đừng làm bẩn quần áo."}],
    "hsk4_539": [{"chinese": "越来越多的女性开始创业。", "pinyin": "Yuèláiyuè duō de nǚxìng kāishǐ chuàngyè.", "meaningVi": "Ngày càng nhiều phụ nữ bắt đầu khởi nghiệp."}],
    "hsk4_544": [{"chinese": "他喜欢打牌。", "pinyin": "Tā xǐhuan dǎpái.", "meaningVi": "Anh ấy thích chơi bài."}],
    "hsk4_545": [{"chinese": "大家都在排队买票。", "pinyin": "Dàjiā dōu zài páiduì mǎi piào.", "meaningVi": "Mọi người đều đang xếp hàng mua vé."}],
    "hsk4_546": [{"chinese": "他每周都打排球。", "pinyin": "Tā měi zhōu dōu dǎ páiqiú.", "meaningVi": "Anh ấy mỗi tuần đều chơi bóng chuyền."}],
    "hsk4_547": [{"chinese": "这个牌子的手机很受欢迎。", "pinyin": "Zhège páizi de shǒujī hěn shòu huānyíng.", "meaningVi": "Điện thoại của nhãn hiệu này rất được ưa chuộng."}],
    "hsk4_548": [{"chinese": "我们要根据事实来判断。", "pinyin": "Wǒmen yào gēnjù shìshí lái pànduàn.", "meaningVi": "Chúng ta phải căn cứ vào sự thật để phán đoán."}],
    "hsk4_549": [{"chinese": "我今天陪妈妈去医院。", "pinyin": "Wǒ jīntiān péi māma qù yīyuàn.", "meaningVi": "Hôm nay tôi đi cùng mẹ đến bệnh viện."}],
    "hsk4_550": [{"chinese": "老师批评了他。", "pinyin": "Lǎoshī pīpíngle tā.", "meaningVi": "Giáo viên đã phê bình anh ấy."}],
    "hsk4_551": [{"chinese": "她的皮肤很白。", "pinyin": "Tā de pífū hěn bái.", "meaningVi": "Da của cô ấy rất trắng."}],
    "hsk4_552": [{"chinese": "他的脾气很好。", "pinyin": "Tā de píqi hěn hǎo.", "meaningVi": "Tính tình của anh ấy rất tốt."}],
    "hsk4_553": [{"chinese": "他买了一双新皮鞋。", "pinyin": "Tā mǎile yì shuāng xīn píxié.", "meaningVi": "Anh ấy đã mua một đôi giày da mới."}],
    "hsk4_556": [{"chinese": "我们下午打乒乓球吧。", "pinyin": "Wǒmen xiàwǔ dǎ pīngpāngqiú ba.", "meaningVi": "Chiều nay chúng ta chơi bóng bàn đi."}],
    "hsk4_559": [{"chinese": "这些葡萄很甜。", "pinyin": "Zhèxiē pútao hěn tián.", "meaningVi": "Những quả nho này rất ngọt."}],
    "hsk4_560": [{"chinese": "他喜欢喝红葡萄酒。", "pinyin": "Tā xǐhuan hē hóng pútaojiǔ.", "meaningVi": "Anh ấy thích uống rượu vang đỏ."}],
    "hsk4_561": [{"chinese": "这是一个普遍现象。", "pinyin": "Zhè shì yí gè pǔbiàn xiànxiàng.", "meaningVi": "Đây là một hiện tượng phổ biến."}],
    "hsk4_562": [{"chinese": "我只是一个普通人。", "pinyin": "Wǒ zhǐshì yí gè pǔtōng rén.", "meaningVi": "Tôi chỉ là một người bình thường."}],
    "hsk4_563": [{"chinese": "他的普通话说得很标准。", "pinyin": "Tā de pǔtōnghuà shuō de hěn biāozhǔn.", "meaningVi": "Tiếng phổ thông của anh ấy nói rất chuẩn."}],
    "hsk4_564": [{"chinese": "这份杂志每周出一期。", "pinyin": "Zhè fèn zázhì měi zhōu chū yì qī.", "meaningVi": "Tạp chí này mỗi tuần ra một kỳ."}],
    "hsk4_565": [{"chinese": "期末考试快到了。", "pinyin": "Qīmò kǎoshì kuài dào le.", "meaningVi": "Kỳ thi cuối kỳ sắp đến rồi."}],
    "hsk4_566": [{"chinese": "期中考试结束了。", "pinyin": "Qīzhōng kǎoshì jiéshù le.", "meaningVi": "Kỳ thi giữa kỳ đã kết thúc."}],
    "hsk4_567": [{"chinese": "首先要准备材料，其次要填表格。", "pinyin": "Shǒuxiān yào zhǔnbèi cáiliào, qícì yào tián biǎogé.", "meaningVi": "Trước tiên phải chuẩn bị tài liệu, tiếp theo phải điền vào biểu mẫu."}],
    "hsk4_568": [{"chinese": "我有三个爱好，其中一个是画画。", "pinyin": "Wǒ yǒu sān gè àihào, qízhōng yí gè shì huàhuà.", "meaningVi": "Tôi có ba sở thích, trong đó một cái là vẽ tranh."}],
    "hsk4_569": [{"chinese": "这个方法起到了很好的效果。", "pinyin": "Zhège fāngfǎ qǐdàole hěn hǎo de xiàoguǒ.", "meaningVi": "Phương pháp này đã phát huy hiệu quả rất tốt."}],
    "hsk4_571": [{"chinese": "这里的气候四季分明。", "pinyin": "Zhèlǐ de qìhòu sìjì fēnmíng.", "meaningVi": "Khí hậu ở đây bốn mùa rõ rệt."}],
    "hsk4_572": [{"chinese": "他喜欢喝汽水。", "pinyin": "Tā xǐhuan hē qìshuǐ.", "meaningVi": "Anh ấy thích uống nước ngọt có ga."}],
    "hsk4_573": [{"chinese": "今天的气温很高。", "pinyin": "Jīntiān de qìwēn hěn gāo.", "meaningVi": "Nhiệt độ hôm nay rất cao."}],
    "hsk4_574": [{"chinese": "这个箱子重十千克。", "pinyin": "Zhège xiāngzi zhòng shí qiānkè.", "meaningVi": "Cái hộp này nặng mười ki-lô-gam."}],
    "hsk4_575": [{"chinese": "你千万别迟到。", "pinyin": "Nǐ qiānwàn bié chídào.", "meaningVi": "Bạn nhất định đừng đến muộn."}],
    "hsk4_577": [{"chinese": "前方是一片森林。", "pinyin": "Qiánfāng shì yí piàn sēnlín.", "meaningVi": "Phía trước là một khu rừng."}],
    "hsk4_578": [{"chinese": "春节前后天气会变冷。", "pinyin": "Chūnjié qiánhòu tiānqì huì biàn lěng.", "meaningVi": "Trước sau Tết thời tiết sẽ trở lạnh."}],
    "hsk4_579": [{"chinese": "他的责任心很强。", "pinyin": "Tā de zérènxīn hěn qiáng.", "meaningVi": "Trách nhiệm của anh ấy rất mạnh mẽ."}],
    "hsk4_580": [{"chinese": "有人在敲门。", "pinyin": "Yǒu rén zài qiāo mén.", "meaningVi": "Có người đang gõ cửa."}],
    "hsk4_581": [{"chinese": "这座桥很长。", "pinyin": "Zhè zuò qiáo hěn cháng.", "meaningVi": "Cây cầu này rất dài."}],
    "hsk4_582": [{"chinese": "真巧，我也要去那里。", "pinyin": "Zhēn qiǎo, wǒ yě yào qù nàlǐ.", "meaningVi": "Thật trùng hợp, tôi cũng định đến đó."}],
    "hsk4_583": [{"chinese": "她很喜欢吃巧克力。", "pinyin": "Tā hěn xǐhuan chī qiǎokèlì.", "meaningVi": "Cô ấy rất thích ăn sô cô la."}],
    "hsk4_584": [{"chinese": "过年的时候我们去看亲戚。", "pinyin": "Guònián de shíhou wǒmen qù kàn qīnqi.", "meaningVi": "Vào dịp Tết chúng tôi đi thăm họ hàng."}],
    "hsk4_585": [{"chinese": "她会弹琴。", "pinyin": "Tā huì tán qín.", "meaningVi": "Cô ấy biết chơi đàn."}],
    "hsk4_586": [{"chinese": "这个包很轻。", "pinyin": "Zhège bāo hěn qīng.", "meaningVi": "Cái túi này rất nhẹ."}],
    "hsk4_587": [{"chinese": "他是一名优秀的青年。", "pinyin": "Tā shì yì míng yōuxiù de qīngnián.", "meaningVi": "Anh ấy là một thanh niên ưu tú."}],
    "hsk4_588": [{"chinese": "周末让人感到轻松。", "pinyin": "Zhōumò ràng rén gǎndào qīngsōng.", "meaningVi": "Cuối tuần khiến người ta cảm thấy thư giãn."}],
    "hsk4_589": [{"chinese": "请介绍一下目前的情况。", "pinyin": "Qǐng jièshào yíxià mùqián de qíngkuàng.", "meaningVi": "Xin hãy giới thiệu một chút về tình hình hiện tại."}],
    "hsk4_590": [{"chinese": "我们一起庆祝生日吧。", "pinyin": "Wǒmen yìqǐ qìngzhù shēngrì ba.", "meaningVi": "Chúng ta cùng nhau ăn mừng sinh nhật đi."}],
    "hsk4_591": [{"chinese": "他是这支球队的队长。", "pinyin": "Tā shì zhè zhī qiúduì de duìzhǎng.", "meaningVi": "Anh ấy là đội trưởng của đội bóng này."}],
    "hsk4_592": [{"chinese": "他是一个球迷。", "pinyin": "Tā shì yí gè qiúmí.", "meaningVi": "Anh ấy là một người hâm mộ bóng đá."}],
    "hsk4_593": [{"chinese": "这个区的房价很高。", "pinyin": "Zhège qū de fángjià hěn gāo.", "meaningVi": "Giá nhà ở khu vực này rất cao."}],
    "hsk4_595": [{"chinese": "我去银行取点钱。", "pinyin": "Wǒ qù yínháng qǔ diǎn qián.", "meaningVi": "Tôi đi ngân hàng lấy ít tiền."}],
    "hsk4_596": [{"chinese": "他在比赛中取得了好成绩。", "pinyin": "Tā zài bǐsài zhōng qǔdéle hǎo chéngjì.", "meaningVi": "Anh ấy đã đạt được thành tích tốt trong cuộc thi."}],
    "hsk4_597": [{"chinese": "航班因为天气被取消了。", "pinyin": "Hángbān yīnwèi tiānqì bèi qǔxiāo le.", "meaningVi": "Chuyến bay bị hủy vì thời tiết."}],
    "hsk4_599": [{"chinese": "这些东西全部都是我的。", "pinyin": "Zhèxiē dōngxi quánbù dōu shì wǒ de.", "meaningVi": "Những thứ này toàn bộ đều là của tôi."}],
    "hsk4_600": [{"chinese": "大家全都同意这个计划。", "pinyin": "Dàjiā quándōu tóngyì zhège jìhuà.", "meaningVi": "Mọi người tất cả đều đồng ý với kế hoạch này."}],
    "hsk4_601": [{"chinese": "这是一个全球性的问题。", "pinyin": "Zhè shì yí gè quánqiúxìng de wèntí.", "meaningVi": "Đây là một vấn đề mang tính toàn cầu."}],
    "hsk4_602": [{"chinese": "运动后他全身都是汗。", "pinyin": "Yùndòng hòu tā quánshēn dōu shì hàn.", "meaningVi": "Sau khi vận động toàn thân anh ấy đều là mồ hôi."}],
    "hsk4_603": [{"chinese": "这里还缺一个人。", "pinyin": "Zhèlǐ hái quē yí gè rén.", "meaningVi": "Ở đây vẫn còn thiếu một người."}],
    "hsk4_604": [{"chinese": "每个人都有优点和缺点。", "pinyin": "Měi gè rén dōu yǒu yōudiǎn hé quēdiǎn.", "meaningVi": "Mỗi người đều có ưu điểm và nhược điểm."}],
    "hsk4_605": [{"chinese": "这个地区缺少水资源。", "pinyin": "Zhège dìqū quēshǎo shuǐ zīyuán.", "meaningVi": "Khu vực này thiếu tài nguyên nước."}],
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
