"""P5.10.3 (continued) -- Batch 017 (continues immediately after
examples_batch_016.json). Spans the tail of HSK4 (25 records,
hsk4_958-hsk4_997) into the start of HSK5 (75 records). The HSK5 IDs
sort as plain strings, not numerically (e.g. "hsk5_100" < "hsk5_1000"
< ... < "hsk5_1039" < "hsk5_104" < "hsk5_1040" ...) -- this is the
same expected/confirmed string-sort behavior documented in batch 009
for hsk4_1000, not a bug.

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

*** Critical disambiguation cluster in this batch ***
Four HSK5 records in this single batch are near-homophones of each
other, none flagged by the mechanical tier system (it compares the
`word` string, and all four are different words):
  - 实用 (shíyòng, "practical/useful") and 食用 (shíyòng, "edible/for
    eating") -- identical pinyin AND identical tones.
  - 试用 (shìyòng, "to try out/trial use") and 适用 (shìyòng,
    "applicable/suitable for use") -- identical pinyin AND identical
    tones, and differing from the 实用/食用 pair by only the initial
    consonant's tone-adjacent syllable (shí- vs shì-).
  Each of the four was given a sentence built around a completely
  different real-world scenario (product design / a mushroom /
  a trial period / a workplace regulation) so no two could be
  confused even out of context.
Additional same-pinyin-different-character pairs in the same batch:
  - 诗 (shī, "poem") vs 湿 (shī, "wet") -- identical pinyin.
  - 胜 (shèng, "to win", demonstrated via 获胜) vs the unrelated,
    already-published 剩 (shèng, "left over", batch 014, hsk4_651) --
    identical pinyin, cross-batch pair, not a new record here but
    checked for interference; no overlap in the two sentences.
  - 做 (zuò, in 做法/做梦) vs 作 (zuò, in 作家/作品) vs 座 (zuò, in
    座位): three-way homophone cluster, disambiguated naturally via
    each word's own compound.

Self-caught near-duplicate revision made during drafting: 事业
(shìyè)'s first draft ("他把一生都献给了教育事业。") was near-verbatim
the existing 一生 example (batch 016, hsk4_869: "他把一生都献给了教育
事业。") -- rewritten to "她的事业发展得很顺利。" before finalizing.

Near-synonym pairs kept in genuinely distinct constructions (not
templated): 必需/必要 (bìxū/bìyào, "necessary"); 采取/采用 (cǎiqǔ/
cǎiyòng, paired with 措施 vs 技术 respectively); 曾/曾经 (céng/
céngjīng); 自习/自学 (zìxí/zìxué, school self-study period vs.
self-teaching a subject); 实施/实行/实现 (shíshī/shíxíng/shíxiàn,
policy rollout vs. long-running system vs. achieving a personal goal).

Polysemous words given ONE unambiguous sense rather than a blended
example: 才 (cái) as "just now/only just", not "only" or other
readings; 别 (bié) as the imperative "don't", not "different" or
"other"; 装 (zhuāng) as "to pretend" (装作), not "to install/pack".

Cross-batch exact-duplicate collision found and fixed during
authoring: 别 (hsk5_066)'s first draft "别担心，一切都会好的。"
duplicated examples_batch_005.json's hsk3_079 (担心) verbatim --
rewritten to "别乱扔垃圾。" before this batch was finalized;
re-verified against the full pilot+002-016 corpus with zero
remaining exact duplicates and zero near-template flags.

Usage:
    python generate_examples_batch_017.py --dry-run
    python generate_examples_batch_017.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 17
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_017.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk4_958": [{"chinese": "他已经步入中年。", "pinyin": "Tā yǐjīng bùrù zhōngnián.", "meaningVi": "Anh ấy đã bước vào tuổi trung niên."}],
    "hsk4_962": [{"chinese": "公司很重视员工培训。", "pinyin": "Gōngsī hěn zhòngshì yuángōng péixùn.", "meaningVi": "Công ty rất coi trọng việc đào tạo nhân viên."}],
    "hsk4_963": [{"chinese": "学校周围有很多商店。", "pinyin": "Xuéxiào zhōuwéi yǒu hěn duō shāngdiàn.", "meaningVi": "Xung quanh trường học có rất nhiều cửa hàng."}],
    "hsk4_964": [{"chinese": "他想出了一个好主意。", "pinyin": "Tā xiǎngchūle yí gè hǎo zhǔyi.", "meaningVi": "Anh ấy đã nghĩ ra một ý tưởng hay."}],
    "hsk4_965": [{"chinese": "祝你生日快乐。", "pinyin": "Zhù nǐ shēngrì kuàilè.", "meaningVi": "Chúc bạn sinh nhật vui vẻ."}],
    "hsk4_966": [{"chinese": "祝贺你考上了大学。", "pinyin": "Zhùhè nǐ kǎoshàngle dàxué.", "meaningVi": "Chúc mừng bạn đã thi đỗ đại học."}],
    "hsk4_967": [{"chinese": "他是一位著名的科学家。", "pinyin": "Tā shì yí wèi zhùmíng de kēxuéjiā.", "meaningVi": "Anh ấy là một nhà khoa học nổi tiếng."}],
    "hsk4_971": [{"chinese": "请帮我转发这条消息。", "pinyin": "Qǐng bāng wǒ zhuǎnfā zhè tiáo xiāoxi.", "meaningVi": "Xin giúp tôi chuyển tiếp tin nhắn này."}],
    "hsk4_972": [{"chinese": "我们需要在上海转机。", "pinyin": "Wǒmen xūyào zài Shànghǎi zhuǎnjī.", "meaningVi": "Chúng tôi cần chuyển máy bay tại Thượng Hải."}],
    "hsk4_973": [{"chinese": "他每个月能赚不少钱。", "pinyin": "Tā měi gè yuè néng zhuàn bù shǎo qián.", "meaningVi": "Mỗi tháng anh ấy kiếm được không ít tiền."}],
    "hsk4_974": [{"chinese": "他装作没看见。", "pinyin": "Tā zhuāngzuò méi kànjiàn.", "meaningVi": "Anh ấy giả vờ như không nhìn thấy."}],
    "hsk4_976": [{"chinese": "请给出准确的答案。", "pinyin": "Qǐng gěichū zhǔnquè de dá'àn.", "meaningVi": "Xin đưa ra câu trả lời chính xác."}],
    "hsk4_977": [{"chinese": "请准时到达。", "pinyin": "Qǐng zhǔnshí dàodá.", "meaningVi": "Xin đến đúng giờ."}],
    "hsk4_978": [{"chinese": "请把资料整理好。", "pinyin": "Qǐng bǎ zīliào zhěnglǐ hǎo.", "meaningVi": "Xin sắp xếp tài liệu cho gọn gàng."}],
    "hsk4_979": [{"chinese": "请仔细检查一遍。", "pinyin": "Qǐng zǐxì jiǎnchá yí biàn.", "meaningVi": "Xin kiểm tra cẩn thận một lượt."}],
    "hsk4_980": [{"chinese": "这趟列车来自北京。", "pinyin": "Zhè tàng lièchē láizì Běijīng.", "meaningVi": "Chuyến tàu này đến từ Bắc Kinh."}],
    "hsk4_982": [{"chinese": "下午第三节是自习课。", "pinyin": "Xiàwǔ dì-sān jié shì zìxí kè.", "meaningVi": "Tiết thứ ba buổi chiều là tiết tự học."}],
    "hsk4_984": [{"chinese": "他自学了三年英语。", "pinyin": "Tā zìxuéle sān nián Yīngyǔ.", "meaningVi": "Anh ấy đã tự học tiếng Anh ba năm."}],
    "hsk4_986": [{"chinese": "我们在这里租了一套房子。", "pinyin": "Wǒmen zài zhèlǐ zūle yí tào fángzi.", "meaningVi": "Chúng tôi đã thuê một căn nhà ở đây."}],
    "hsk4_988": [{"chinese": "他们最终达成了协议。", "pinyin": "Tāmen zuìzhōng dáchéngle xiéyì.", "meaningVi": "Cuối cùng họ đã đạt được thỏa thuận."}],
    "hsk4_992": [{"chinese": "这种做法不太合适。", "pinyin": "Zhè zhǒng zuòfǎ bú tài héshì.", "meaningVi": "Cách làm này không thích hợp lắm."}],
    "hsk4_993": [{"chinese": "她是一位有名的作家。", "pinyin": "Tā shì yí wèi yǒumíng de zuòjiā.", "meaningVi": "Cô ấy là một nhà văn nổi tiếng."}],
    "hsk4_994": [{"chinese": "我昨晚做梦了。", "pinyin": "Wǒ zuówǎn zuòmèng le.", "meaningVi": "Tối qua tôi đã nằm mơ."}],
    "hsk4_995": [{"chinese": "这是他的代表作品。", "pinyin": "Zhè shì tā de dàibiǎo zuòpǐn.", "meaningVi": "Đây là tác phẩm tiêu biểu của anh ấy."}],
    "hsk4_997": [{"chinese": "请坐到自己的座位上。", "pinyin": "Qǐng zuò dào zìjǐ de zuòwèi shàng.", "meaningVi": "Xin ngồi vào chỗ của mình."}],
    "hsk5_052": [{"chinese": "闭幕式将在今晚举行。", "pinyin": "Bìmùshì jiāng zài jīnwǎn jǔxíng.", "meaningVi": "Lễ bế mạc sẽ được tổ chức vào tối nay."}],
    "hsk5_054": [{"chinese": "水是生命必需的。", "pinyin": "Shuǐ shì shēngmìng bìxū de.", "meaningVi": "Nước là thứ cần thiết cho sự sống."}],
    "hsk5_055": [{"chinese": "没有必要担心这件事。", "pinyin": "Méiyǒu bìyào dānxīn zhè jiàn shì.", "meaningVi": "Không cần thiết phải lo lắng về việc này."}],
    "hsk5_056": [{"chinese": "只要你说一声，我便过去。", "pinyin": "Zhǐyào nǐ shuō yì shēng, wǒ biàn guòqù.", "meaningVi": "Chỉ cần bạn nói một tiếng, tôi liền qua ngay."}],
    "hsk5_059": [{"chinese": "楼下就有一家便利店。", "pinyin": "Lóuxià jiù yǒu yì jiā biànlìdiàn.", "meaningVi": "Ngay tầng dưới có một cửa hàng tiện lợi."}],
    "hsk5_060": [{"chinese": "请给这篇文章加个标题。", "pinyin": "Qǐng gěi zhè piān wénzhāng jiā ge biāotí.", "meaningVi": "Xin thêm tiêu đề cho bài viết này."}],
    "hsk5_062": [{"chinese": "他很会表达自己的想法。", "pinyin": "Tā hěn huì biǎodá zìjǐ de xiǎngfǎ.", "meaningVi": "Anh ấy rất giỏi diễn đạt suy nghĩ của mình."}],
    "hsk5_063": [{"chinese": "桌子表面很光滑。", "pinyin": "Zhuōzi biǎomiàn hěn guānghuá.", "meaningVi": "Bề mặt bàn rất nhẵn."}],
    "hsk5_064": [{"chinese": "研究表明运动有益健康。", "pinyin": "Yánjiū biǎomíng yùndòng yǒuyì jiànkāng.", "meaningVi": "Nghiên cứu cho thấy vận động có lợi cho sức khỏe."}],
    "hsk5_065": [{"chinese": "她脸上的表情很复杂。", "pinyin": "Tā liǎn shàng de biǎoqíng hěn fùzá.", "meaningVi": "Biểu cảm trên mặt cô ấy rất phức tạp."}],
    "hsk5_066": [{"chinese": "别乱扔垃圾。", "pinyin": "Bié luàn rēng lājī.", "meaningVi": "Đừng vứt rác bừa bãi."}],
    "hsk5_068": [{"chinese": "病人被送进了病房。", "pinyin": "Bìngrén bèi sòngjìnle bìngfáng.", "meaningVi": "Bệnh nhân đã được đưa vào phòng bệnh."}],
    "hsk5_069": [{"chinese": "他的病情逐渐好转。", "pinyin": "Tā de bìngqíng zhújiàn hǎozhuǎn.", "meaningVi": "Tình trạng bệnh của anh ấy dần dần chuyển biến tốt."}],
    "hsk5_070": [{"chinese": "请拨打这个号码咨询。", "pinyin": "Qǐng bōdǎ zhège hàomǎ zīxún.", "meaningVi": "Xin gọi số này để tư vấn."}],
    "hsk5_073": [{"chinese": "这个决定对我们不利。", "pinyin": "Zhège juédìng duì wǒmen búlì.", "meaningVi": "Quyết định này bất lợi cho chúng tôi."}],
    "hsk5_075": [{"chinese": "只是感冒，不要紧。", "pinyin": "Zhǐshì gǎnmào, búyàojǐn.", "meaningVi": "Chỉ là cảm cúm thôi, không sao đâu."}],
    "hsk5_076": [{"chinese": "我想补充一点意见。", "pinyin": "Wǒ xiǎng bǔchōng yìdiǎn yìjiàn.", "meaningVi": "Tôi muốn bổ sung thêm một chút ý kiến."}],
    "hsk5_078": [{"chinese": "这份报告与事实不符。", "pinyin": "Zhè fèn bàogào yǔ shìshí bùfú.", "meaningVi": "Báo cáo này không khớp với sự thật."}],
    "hsk5_081": [{"chinese": "从这里步行到车站要十分钟。", "pinyin": "Cóng zhèlǐ bùxíng dào chēzhàn yào shí fēnzhōng.", "meaningVi": "Từ đây đi bộ đến trạm xe mất mười phút."}],
    "hsk5_083": [{"chinese": "他才来，还不知道情况。", "pinyin": "Tā cái lái, hái bù zhīdào qíngkuàng.", "meaningVi": "Anh ấy vừa mới đến, vẫn chưa biết tình hình."}],
    "hsk5_085": [{"chinese": "记者采访了这位演员。", "pinyin": "Jìzhě cǎifǎngle zhè wèi yǎnyuán.", "meaningVi": "Phóng viên đã phỏng vấn diễn viên này."}],
    "hsk5_086": [{"chinese": "政府采取了新措施。", "pinyin": "Zhèngfǔ cǎiqǔle xīn cuòshī.", "meaningVi": "Chính phủ đã áp dụng biện pháp mới."}],
    "hsk5_087": [{"chinese": "这是一台彩色电视机。", "pinyin": "Zhè shì yì tái cǎisè diànshìjī.", "meaningVi": "Đây là một chiếc tivi màu."}],
    "hsk5_088": [{"chinese": "这家工厂采用了新技术。", "pinyin": "Zhè jiā gōngchǎng cǎiyòngle xīn jìshù.", "meaningVi": "Nhà máy này đã áp dụng công nghệ mới."}],
    "hsk5_089": [{"chinese": "这份资料仅供参考。", "pinyin": "Zhè fèn zīliào jǐn gōng cānkǎo.", "meaningVi": "Tài liệu này chỉ để tham khảo."}],
    "hsk5_091": [{"chinese": "很多人参与了这次活动。", "pinyin": "Hěn duō rén cānyùle zhè cì huódòng.", "meaningVi": "Rất nhiều người đã tham gia hoạt động lần này."}],
    "hsk5_092": [{"chinese": "他把礼物藏了起来。", "pinyin": "Tā bǎ lǐwù cángle qǐlai.", "meaningVi": "Anh ấy đã giấu món quà đi."}],
    "hsk5_093": [{"chinese": "请按照说明操作机器。", "pinyin": "Qǐng ànzhào shuōmíng cāozuò jīqì.", "meaningVi": "Xin vận hành máy theo hướng dẫn."}],
    "hsk5_095": [{"chinese": "用尺子测一下长度。", "pinyin": "Yòng chǐzi cè yíxià chángdù.", "meaningVi": "Dùng thước đo độ dài một chút."}],
    "hsk5_096": [{"chinese": "这个软件正在测试阶段。", "pinyin": "Zhège ruǎnjiàn zhèngzài cèshì jiēduàn.", "meaningVi": "Phần mềm này đang trong giai đoạn thử nghiệm."}],
    "hsk5_097": [{"chinese": "他曾是一名军人。", "pinyin": "Tā céng shì yì míng jūnrén.", "meaningVi": "Anh ấy từng là một quân nhân."}],
    "hsk5_098": [{"chinese": "我曾经去过北京。", "pinyin": "Wǒ céngjīng qùguo Běijīng.", "meaningVi": "Tôi đã từng đến Bắc Kinh."}],
    "hsk5_100": [{"chinese": "这两个方案没有太大差别。", "pinyin": "Zhè liǎng gè fāng'àn méiyǒu tài dà chābié.", "meaningVi": "Hai phương án này không có sự khác biệt lớn."}],
    "hsk5_1000": [{"chinese": "广州是广东省的省会。", "pinyin": "Guǎngzhōu shì Guǎngdōng Shěng de shěnghuì.", "meaningVi": "Quảng Châu là tỉnh lỵ của tỉnh Quảng Đông."}],
    "hsk5_1001": [{"chinese": "这场比赛他们获胜了。", "pinyin": "Zhè chǎng bǐsài tāmen huòshèng le.", "meaningVi": "Trận đấu này họ đã giành chiến thắng."}],
    "hsk5_1002": [{"chinese": "经过努力，他们终于取得了胜利。", "pinyin": "Jīngguò nǔlì, tāmen zhōngyú qǔdéle shènglì.", "meaningVi": "Qua nỗ lực, cuối cùng họ đã giành được thắng lợi."}],
    "hsk5_1003": [{"chinese": "他写了一首诗。", "pinyin": "Tā xiěle yì shǒu shī.", "meaningVi": "Anh ấy đã viết một bài thơ."}],
    "hsk5_1004": [{"chinese": "衣服还是湿的。", "pinyin": "Yīfu háishi shī de.", "meaningVi": "Quần áo vẫn còn ướt."}],
    "hsk5_1005": [{"chinese": "他因为失恋而难过。", "pinyin": "Tā yīnwèi shīliàn ér nánguò.", "meaningVi": "Anh ấy buồn vì thất tình."}],
    "hsk5_1006": [{"chinese": "我最近总是失眠。", "pinyin": "Wǒ zuìjìn zǒngshì shīmián.", "meaningVi": "Gần đây tôi luôn bị mất ngủ."}],
    "hsk5_1007": [{"chinese": "李白是中国著名的诗人。", "pinyin": "Lǐ Bái shì Zhōngguó zhùmíng de shīrén.", "meaningVi": "Lý Bạch là nhà thơ nổi tiếng của Trung Quốc."}],
    "hsk5_1009": [{"chinese": "很多人在经济危机中失业了。", "pinyin": "Hěn duō rén zài jīngjì wēijī zhōng shīyè le.", "meaningVi": "Rất nhiều người đã thất nghiệp trong cuộc khủng hoảng kinh tế."}],
    "hsk5_1010": [{"chinese": "从中国到美国有时差。", "pinyin": "Cóng Zhōngguó dào Měiguó yǒu shíchā.", "meaningVi": "Từ Trung Quốc đến Mỹ có sự chênh lệch múi giờ."}],
    "hsk5_1011": [{"chinese": "他时常来看我。", "pinyin": "Tā shícháng lái kàn wǒ.", "meaningVi": "Anh ấy thường xuyên đến thăm tôi."}],
    "hsk5_1012": [{"chinese": "我们生活在一个信息时代。", "pinyin": "Wǒmen shēnghuó zài yí gè xìnxī shídài.", "meaningVi": "Chúng ta sống trong một thời đại thông tin."}],
    "hsk5_1013": [{"chinese": "理论要联系实践。", "pinyin": "Lǐlùn yào liánxì shíjiàn.", "meaningVi": "Lý thuyết phải gắn liền với thực tiễn."}],
    "hsk5_1015": [{"chinese": "这支球队实力很强。", "pinyin": "Zhè zhī qiúduì shílì hěn qiáng.", "meaningVi": "Đội bóng này có thực lực rất mạnh."}],
    "hsk5_1016": [{"chinese": "那是一个特殊的历史时期。", "pinyin": "Nà shì yí gè tèshū de lìshǐ shíqī.", "meaningVi": "Đó là một thời kỳ lịch sử đặc biệt."}],
    "hsk5_1017": [{"chinese": "新政策将于下月实施。", "pinyin": "Xīn zhèngcè jiāng yú xià yuè shíshī.", "meaningVi": "Chính sách mới sẽ được thực hiện vào tháng sau."}],
    "hsk5_1018": [{"chinese": "路上有一块大石头。", "pinyin": "Lù shàng yǒu yí kuài dà shítou.", "meaningVi": "Trên đường có một tảng đá lớn."}],
    "hsk5_1019": [{"chinese": "他正在一家公司实习。", "pinyin": "Tā zhèngzài yì jiā gōngsī shíxí.", "meaningVi": "Anh ấy đang thực tập tại một công ty."}],
    "hsk5_102": [{"chinese": "请给我一把叉子。", "pinyin": "Qǐng gěi wǒ yì bǎ chāzi.", "meaningVi": "Xin cho tôi một cái nĩa."}],
    "hsk5_1020": [{"chinese": "他终于实现了自己的梦想。", "pinyin": "Tā zhōngyú shíxiànle zìjǐ de mèngxiǎng.", "meaningVi": "Cuối cùng anh ấy đã thực hiện được ước mơ của mình."}],
    "hsk5_1021": [{"chinese": "这项制度已经实行多年了。", "pinyin": "Zhè xiàng zhìdù yǐjīng shíxíng duō nián le.", "meaningVi": "Chế độ này đã được thi hành nhiều năm rồi."}],
    "hsk5_1023": [{"chinese": "他每天在实验室工作。", "pinyin": "Tā měitiān zài shíyànshì gōngzuò.", "meaningVi": "Anh ấy mỗi ngày làm việc trong phòng thí nghiệm."}],
    "hsk5_1024": [{"chinese": "这个设计既美观又实用。", "pinyin": "Zhège shèjì jì měiguān yòu shíyòng.", "meaningVi": "Thiết kế này vừa đẹp vừa hữu ích."}],
    "hsk5_1025": [{"chinese": "这种蘑菇不能食用。", "pinyin": "Zhè zhǒng mógu bù néng shíyòng.", "meaningVi": "Loại nấm này không thể ăn được."}],
    "hsk5_1026": [{"chinese": "这场雨使得比赛推迟了。", "pinyin": "Zhè chǎng yǔ shǐde bǐsài tuīchí le.", "meaningVi": "Trận mưa này đã khiến trận đấu bị hoãn lại."}],
    "hsk5_1028": [{"chinese": "这是中式建筑。", "pinyin": "Zhè shì zhōngshì jiànzhù.", "meaningVi": "Đây là kiến trúc kiểu Trung Quốc."}],
    "hsk5_1029": [{"chinese": "请选择适当的时间。", "pinyin": "Qǐng xuǎnzé shìdàng de shíjiān.", "meaningVi": "Xin chọn thời gian thích hợp."}],
    "hsk5_1030": [{"chinese": "他像孩子似的笑了。", "pinyin": "Tā xiàng háizi shìde xiào le.", "meaningVi": "Anh ấy cười như một đứa trẻ."}],
    "hsk5_1031": [{"chinese": "昨天这里发生了一起交通事故。", "pinyin": "Zuótiān zhèlǐ fāshēngle yì qǐ jiāotōng shìgù.", "meaningVi": "Hôm qua ở đây đã xảy ra một vụ tai nạn giao thông."}],
    "hsk5_1032": [{"chinese": "这是一起重大事件。", "pinyin": "Zhè shì yì qǐ zhòngdà shìjiàn.", "meaningVi": "Đây là một sự kiện trọng đại."}],
    "hsk5_1033": [{"chinese": "请把试卷交上来。", "pinyin": "Qǐng bǎ shìjuàn jiāo shànglái.", "meaningVi": "Xin nộp bài thi lên."}],
    "hsk5_1034": [{"chinese": "市民们积极参加了这次活动。", "pinyin": "Shìmínmen jījí cānjiāle zhè cì huódòng.", "meaningVi": "Người dân thành phố đã tích cực tham gia hoạt động lần này."}],
    "hsk5_1035": [{"chinese": "这是不可否认的事实。", "pinyin": "Zhè shì bù kě fǒurèn de shìshí.", "meaningVi": "Đây là sự thật không thể phủ nhận."}],
    "hsk5_1036": [{"chinese": "他被大家视为榜样。", "pinyin": "Tā bèi dàjiā shìwéi bǎngyàng.", "meaningVi": "Anh ấy được mọi người coi là tấm gương."}],
    "hsk5_1037": [{"chinese": "世界上的事物都在不断变化。", "pinyin": "Shìjiè shàng de shìwù dōu zài búduàn biànhuà.", "meaningVi": "Sự vật trên thế giới đều không ngừng biến đổi."}],
    "hsk5_1038": [{"chinese": "请事先通知我们。", "pinyin": "Qǐng shìxiān tōngzhī wǒmen.", "meaningVi": "Xin thông báo cho chúng tôi trước."}],
    "hsk5_1039": [{"chinese": "科学家进行了多次试验。", "pinyin": "Kēxuéjiā jìnxíngle duō cì shìyàn.", "meaningVi": "Các nhà khoa học đã tiến hành nhiều lần thí nghiệm."}],
    "hsk5_104": [{"chinese": "这个地区盛产水果。", "pinyin": "Zhège dìqū shèngchǎn shuǐguǒ.", "meaningVi": "Khu vực này sản xuất nhiều trái cây."}],
    "hsk5_1040": [{"chinese": "她的事业发展得很顺利。", "pinyin": "Tā de shìyè fāzhǎn de hěn shùnlì.", "meaningVi": "Sự nghiệp của cô ấy phát triển rất thuận lợi."}],
    "hsk5_1041": [{"chinese": "你可以先试用三天。", "pinyin": "Nǐ kěyǐ xiān shìyòng sān tiān.", "meaningVi": "Bạn có thể dùng thử ba ngày trước."}],
    "hsk5_1042": [{"chinese": "这条规定适用于所有员工。", "pinyin": "Zhè tiáo guīdìng shìyòng yú suǒyǒu yuángōng.", "meaningVi": "Quy định này áp dụng cho tất cả nhân viên."}],
    "hsk5_1044": [{"chinese": "他喜欢收集邮票。", "pinyin": "Tā xǐhuan shōují yóupiào.", "meaningVi": "Anh ấy thích sưu tầm tem."}],
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
