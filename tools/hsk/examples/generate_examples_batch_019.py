"""P5.10.3 (continued) -- Batch 019 (continues immediately after
examples_batch_018.json; entirely within HSK5).

Same honesty note as prior batch scripts: record SELECTION (via
queue_lib_p103.get_next_batch_ids) is deterministic; example CONTENT
below was authored directly by this assistant (LLM).

Resume context: this batch was rebuilt from scratch on a different
machine than an earlier, uncommitted Batch 019 draft (never merged,
never recovered). The queue-computed ID set below was independently
re-derived from tools/hsk/examples/queue_lib_p103.py against the
current repository state (checkpoint 870f791, batches 002-018) rather
than assumed from that earlier draft.

Cross-checked risk words carried over from that earlier draft's notes
(verified against the actual repository before use, not assumed):
  - xiaofeizhe (hsk5_1263, 消费者): batch 016's suffix-demonstration
    record for zhe3 (hsk4_926, 者) used "他是一位消费者。" verbatim as
    its own example, because 消费者 did not yet have its own
    vocabulary record. Now that it does, its example here is written
    completely differently: "这家公司很重视消费者的意见。".
  - xiangnian4 (hsk5_1253, 想念): hsk4_341 (家乡, batch 011) already
    used "我很想念我的家乡。" -- written with a different subject and
    object here: "出国以后，他常常想念父母。".
  - xianxiang4 (hsk5_1243, 现象): hsk4_932 (正常, batch 016) already
    used "这是正常现象。" -- written with an unrelated structure here:
    "科学家正在研究这种奇怪的自然现象。".
  - cheliang4 (hsk5_126, 车辆): hsk5_1140 (通行, batch 018) already
    used "这条路禁止车辆通行。" -- written with an unrelated structure
    here: "停车场里停满了各种车辆。".
  - chaoji2 (hsk5_119, 超级): hsk4_592 (球迷, batch 013) already used
    "他是一个球迷。"; "超级球迷" ("super fan") is a natural collocation
    that would have echoed it -- avoided entirely in favor of the
    unrelated "超级市场" (supermarket) collocation instead.
  - chekus4 (hsk5_125, 车库) / hsk4_740 (停车, batch 015, "这里不能
    停车。"): different word, different structure, no real collision
    risk, kept distinct regardless ("他把自行车放在车库里。").
  - wushu4 (hsk5_1212, 武术) / hsk5_1073 (睡眠, batch 018): no shared
    vocabulary or theme; the earlier draft's pairing was not a real
    collision (verified, not assumed).
  - "猪名" and "念念" from the earlier draft's notes do not correspond
    to any real HSK1-6 vocabulary record and were disregarded.

New homophone/near-homophone clusters found within this batch's own
100 words (via a pinyin-clustering pass over the queue output, same
discipline as batch 018) and kept structurally distinct:
  - chao1 (超, "exceed") vs chao3 (炒, "stir-fry"): unrelated topics,
    no shared vocabulary.
  - wei2 (围, "surround") vs wei4 (喂, "hello/feed"): unrelated topics.
  - wu2shu4 (无数, "countless") vs wu3shu4 (武术, "martial arts"):
    tone-only difference on the first syllable, unrelated topics.
  - xian2 (闲, "idle/vacant") vs xian4 (县, "county"): unrelated
    topics.

Productive-root families kept structurally distinct within this batch
(no shared sentence template despite the shared character): chao1/
chaochu1/chaoji2/chaosu4 (chao1+X, four members, four different
contexts: temperature, expectation, supermarket, speeding); wai4bu4/
wai4gong1/wai4guan1/wai4po2/wai4xing2 (wai4+X, five members); wei2/
wei2jin1/wei2rao4 (wei2+X); wei2chi2/wei2xiu1 (wei2+X, different wei2
character from the above); wei2fa3/wei2fan3 (wei2+X); wu2guan1/
wu2shu4/wu2xian4/wu2xiao4 (wu2+X); wu3dao3/wu3tai2 (wu3+X --
wu3dao3's sentence deliberately avoids the "cong2xiao3 jiu4 ..."
opener already used for wu3shu4 in this same batch, to avoid an
internal near-template); wu4jia4/wu4li3/wu4pin3/wu4ye4 (wu4+X);
xian3de/xian3ran2/xian3shi4 (xian3+X); xian4chang3/xian4dai4hua4/
xian4xiang4/xian4zhuang4 (xian4+X, four members, four different
contexts: accident scene, city modernizing, natural phenomenon,
company situation); xiang1chu3/xiang1guan1/xiang1si4/xiang1ce4
(xiang1+X); xiang1/xiang1cun1 (xiang1+X); xiang3nian4/xiang3xiang4
(xiang3+X); che1huo4/che1ku4/che1liang4/che1xiang1 (che1+X, four
members, four different contexts); xiao1fei4/xiao1fei4zhe3/xiao1hua4/
xiao1shi1 (xiao1+X, xiao1fei4zhe3 specifically NOT the banned "他是一
位消费者。" string); xiao1liang4/xiao1shou4 (xiao1+X, different
character from the xiao1fei4 family); xiao3jie3/xiao3xing2/xiao3yu2
(xiao3+X); tui4/tui4chu1/tui4huan2/tui4xiu1 (tui4+X, four members).

Usage:
    python generate_examples_batch_019.py --dry-run
    python generate_examples_batch_019.py
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import get_next_batch_ids, load_json_text, REPO_ROOT  # noqa: E402

BATCH_NUMBER = 19
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "examples_batch_019.json"
GENERATION_METHOD = "llm-authored (Claude, this assistant) -- see module docstring"

EXAMPLES_CONTENT: dict[str, list[dict]] = {
    "hsk5_1161": [{"chinese": "这项改革正在稳步推进。", "pinyin": "Zhè xiàng gǎigé zhèngzài wěnbù tuījìn.", "meaningVi": "Cuộc cải cách này đang được thúc đẩy một cách vững chắc."}],
    "hsk5_1162": [{"chinese": "他向后退了一步。", "pinyin": "Tā xiàng hòutuì le yí bù.", "meaningVi": "Anh ấy lùi lại một bước."}],
    "hsk5_1163": [{"chinese": "他决定退出这场比赛。", "pinyin": "Tā juédìng tuìchū zhè chǎng bǐsài.", "meaningVi": "Anh ấy quyết định rút khỏi cuộc thi này."}],
    "hsk5_1164": [{"chinese": "商店把多收的钱退还给了顾客。", "pinyin": "Shāngdiàn bǎ duō shōu de qián tuìhuán gěi le gùkè.", "meaningVi": "Cửa hàng đã hoàn trả lại số tiền thu thừa cho khách hàng."}],
    "hsk5_1165": [{"chinese": "我爷爷去年退休了。", "pinyin": "Wǒ yéye qùnián tuìxiū le.", "meaningVi": "Ông tôi đã nghỉ hưu vào năm ngoái."}],
    "hsk5_1166": [{"chinese": "进门请换上拖鞋。", "pinyin": "Jìnmén qǐng huàn shàng tuōxié.", "meaningVi": "Vào nhà xin hãy đổi sang dép lê."}],
    "hsk5_1167": [{"chinese": "这个问题是外部原因造成的。", "pinyin": "Zhège wèntí shì wàibù yuányīn zàochéng de.", "meaningVi": "Vấn đề này là do nguyên nhân bên ngoài gây ra."}],
    "hsk5_1168": [{"chinese": "我外公以前是一名医生。", "pinyin": "Wǒ wàigōng yǐqián shì yì míng yīshēng.", "meaningVi": "Ông ngoại tôi trước đây từng là bác sĩ."}],
    "hsk5_1169": [{"chinese": "这款手机的外观很时尚。", "pinyin": "Zhè kuǎn shǒujī de wàiguān hěn shíshàng.", "meaningVi": "Ngoại hình của chiếc điện thoại này rất thời trang."}],
    "hsk5_117": [{"chinese": "今天的气温超过了三十度。", "pinyin": "Jīntiān de qìwēn chāoguò le sānshí dù.", "meaningVi": "Nhiệt độ hôm nay đã vượt quá ba mươi độ."}],
    "hsk5_1170": [{"chinese": "外婆每天早上都去公园散步。", "pinyin": "Wàipó měitiān zǎoshang dōu qù gōngyuán sànbù.", "meaningVi": "Bà ngoại sáng nào cũng đi dạo công viên."}],
    "hsk5_1171": [{"chinese": "这辆车的外形很酷。", "pinyin": "Zhè liàng chē de wàixíng hěn kù.", "meaningVi": "Hình dáng bên ngoài của chiếc xe này rất ngầu."}],
    "hsk5_1173": [{"chinese": "这是我小时候最喜欢的玩具。", "pinyin": "Zhè shì wǒ xiǎoshíhou zuì xǐhuan de wánjù.", "meaningVi": "Đây là món đồ chơi mà tôi thích nhất hồi nhỏ."}],
    "hsk5_1174": [{"chinese": "这次演出非常完美。", "pinyin": "Zhè cì yǎnchū fēicháng wánměi.", "meaningVi": "Buổi biểu diễn lần này vô cùng hoàn hảo."}],
    "hsk5_1176": [{"chinese": "这是一份完整的报告。", "pinyin": "Zhè shì yí fèn wánzhěng de bàogào.", "meaningVi": "Đây là một bản báo cáo hoàn chỉnh."}],
    "hsk5_1178": [{"chinese": "这趟航班往返于北京和上海之间。", "pinyin": "Zhè tàng hángbān wǎngfǎn yú Běijīng hé Shànghǎi zhījiān.", "meaningVi": "Chuyến bay này khứ hồi giữa Bắc Kinh và Thượng Hải."}],
    "hsk5_1179": [{"chinese": "现在的网络速度越来越快。", "pinyin": "Xiànzài de wǎngluò sùdù yuèláiyuèkuài.", "meaningVi": "Tốc độ mạng bây giờ ngày càng nhanh."}],
    "hsk5_118": [{"chinese": "这个结果超出了我们的预期。", "pinyin": "Zhège jiéguǒ chāochū le wǒmen de yùqī.", "meaningVi": "Kết quả này đã vượt quá dự kiến của chúng tôi."}],
    "hsk5_1180": [{"chinese": "长期熬夜会危害健康。", "pinyin": "Chángqī áoyè huì wēihài jiànkāng.", "meaningVi": "Thức khuya lâu dài sẽ gây hại cho sức khỏe."}],
    "hsk5_1182": [{"chinese": "全球变暖威胁着许多动物的生存。", "pinyin": "Quánqiú biànnuǎn wēixiézhe xǔduō dòngwù de shēngcún.", "meaningVi": "Sự nóng lên toàn cầu đang đe dọa sự sinh tồn của nhiều loài động vật."}],
    "hsk5_1183": [{"chinese": "村子四周围着一圈高墙。", "pinyin": "Cūnzi sìzhōu wéizhe yì quān gāoqiáng.", "meaningVi": "Xung quanh làng được bao quanh bởi một vòng tường cao."}],
    "hsk5_1185": [{"chinese": "他靠打工维持生活。", "pinyin": "Tā kào dǎgōng wéichí shēnghuó.", "meaningVi": "Anh ấy dựa vào làm thêm để duy trì cuộc sống."}],
    "hsk5_1186": [{"chinese": "酒后开车是违法行为。", "pinyin": "Jiǔhòu kāichē shì wéifǎ xíngwéi.", "meaningVi": "Lái xe sau khi uống rượu là hành vi vi phạm pháp luật."}],
    "hsk5_1187": [{"chinese": "他违反了公司的规定。", "pinyin": "Tā wéifǎn le gōngsī de guīdìng.", "meaningVi": "Anh ấy đã vi phạm quy định của công ty."}],
    "hsk5_1188": [{"chinese": "冬天她总是戴着一条红色的围巾。", "pinyin": "Dōngtiān tā zǒngshì dàizhe yì tiáo hóngsè de wéijīn.", "meaningVi": "Mùa đông cô ấy luôn quàng một chiếc khăn màu đỏ."}],
    "hsk5_1189": [{"chinese": "这次会议围绕环保问题展开讨论。", "pinyin": "Zhè cì huìyì wéirào huánbǎo wèntí zhǎnkāi tǎolùn.", "meaningVi": "Cuộc họp lần này tập trung thảo luận về vấn đề bảo vệ môi trường."}],
    "hsk5_119": [{"chinese": "楼下新开了一家超级市场。", "pinyin": "Lóuxià xīn kāi le yì jiā chāojí shìchǎng.", "meaningVi": "Tầng dưới vừa mở một siêu thị mới."}],
    "hsk5_1190": [{"chinese": "这台电梯正在维修。", "pinyin": "Zhè tái diàntī zhèngzài wéixiū.", "meaningVi": "Chiếc thang máy này đang được sửa chữa."}],
    "hsk5_1191": [{"chinese": "这是我唯一的机会。", "pinyin": "Zhè shì wǒ wéiyī de jīhuì.", "meaningVi": "Đây là cơ hội duy nhất của tôi."}],
    "hsk5_1192": [{"chinese": "小狗摇着尾巴跑了过来。", "pinyin": "Xiǎogǒu yáozhe wěiba pǎo le guòlái.", "meaningVi": "Chú chó con vẫy đuôi chạy lại."}],
    "hsk5_1193": [{"chinese": "母爱是世界上最伟大的爱。", "pinyin": "Mǔ'ài shì shìjiè shàng zuì wěidà de ài.", "meaningVi": "Tình mẫu tử là tình yêu vĩ đại nhất trên thế giới."}],
    "hsk5_1195": [{"chinese": "喂，请问是谁？", "pinyin": "Wèi, qǐngwèn shì shéi?", "meaningVi": "Alo, xin hỏi là ai vậy?"}],
    "hsk5_1197": [{"chinese": "这座城市位于中国南方。", "pinyin": "Zhè zuò chéngshì wèiyú Zhōngguó nánfāng.", "meaningVi": "Thành phố này nằm ở miền Nam Trung Quốc."}],
    "hsk5_1198": [{"chinese": "请把书放回原来的位置。", "pinyin": "Qǐng bǎ shū fàng huí yuánlái de wèizhì.", "meaningVi": "Xin hãy đặt sách trở lại vị trí ban đầu."}],
    "hsk5_120": [{"chinese": "他因为超速被警察拦下了。", "pinyin": "Tā yīnwèi chāosù bèi jǐngchá lán xià le.", "meaningVi": "Anh ấy bị cảnh sát chặn lại vì chạy quá tốc độ."}],
    "hsk5_1200": [{"chinese": "她大学时学的是中国文学。", "pinyin": "Tā dàxué shí xué de shì Zhōngguó wénxué.", "meaningVi": "Thời đại học cô ấy học ngành văn học Trung Quốc."}],
    "hsk5_1202": [{"chinese": "请大家认真填写这份问卷。", "pinyin": "Qǐng dàjiā rènzhēn tiánxiě zhè fèn wènjuàn.", "meaningVi": "Xin mọi người điền phiếu khảo sát này một cách nghiêm túc."}],
    "hsk5_1203": [{"chinese": "他紧紧地握着方向盘。", "pinyin": "Tā jǐnjǐn de wòzhe fāngxiàngpán.", "meaningVi": "Anh ấy nắm chặt vô lăng."}],
    "hsk5_1204": [{"chinese": "这套房子有两间卧室。", "pinyin": "Zhè tào fángzi yǒu liǎng jiān wòshì.", "meaningVi": "Căn nhà này có hai phòng ngủ."}],
    "hsk5_1205": [{"chinese": "两位领导人友好地握手。", "pinyin": "Liǎng wèi lǐngdǎorén yǒuhǎo de wòshǒu.", "meaningVi": "Hai vị lãnh đạo bắt tay nhau một cách thân thiện."}],
    "hsk5_1206": [{"chinese": "这件事跟你无关。", "pinyin": "Zhè jiàn shì gēn nǐ wúguān.", "meaningVi": "Chuyện này không liên quan đến bạn."}],
    "hsk5_1208": [{"chinese": "天上有无数颗星星。", "pinyin": "Tiānshàng yǒu wúshù kē xīngxing.", "meaningVi": "Trên trời có vô số ngôi sao."}],
    "hsk5_1209": [{"chinese": "他对未来充满了无限的希望。", "pinyin": "Tā duì wèilái chōngmǎn le wúxiàn de xīwàng.", "meaningVi": "Anh ấy tràn đầy hy vọng vô hạn về tương lai."}],
    "hsk5_1210": [{"chinese": "这张优惠券已经无效了。", "pinyin": "Zhè zhāng yōuhuìquàn yǐjīng wúxiào le.", "meaningVi": "Phiếu giảm giá này đã hết hiệu lực rồi."}],
    "hsk5_1211": [{"chinese": "她每天晚上都要练习舞蹈。", "pinyin": "Tā měitiān wǎnshang dōu yào liànxí wǔdǎo.", "meaningVi": "Tối nào cô ấy cũng phải luyện tập múa."}],
    "hsk5_1212": [{"chinese": "他从小就喜欢练习武术。", "pinyin": "Tā cóngxiǎo jiù xǐhuan liànxí wǔshù.", "meaningVi": "Anh ấy từ nhỏ đã thích luyện tập võ thuật."}],
    "hsk5_1213": [{"chinese": "这个舞台可以容纳上千名观众。", "pinyin": "Zhège wǔtái kěyǐ róngnà shàng qiān míng guānzhòng.", "meaningVi": "Sân khấu này có thể chứa hàng nghìn khán giả."}],
    "hsk5_1214": [{"chinese": "花园里开满了五颜六色的花。", "pinyin": "Huāyuán lǐ kāi mǎn le wǔyánliùsè de huā.", "meaningVi": "Trong vườn hoa nở đầy đủ màu sắc."}],
    "hsk5_1215": [{"chinese": "今天早上雾很大。", "pinyin": "Jīntiān zǎoshang wù hěn dà.", "meaningVi": "Sáng nay sương mù rất dày."}],
    "hsk5_1216": [{"chinese": "最近几年物价上涨得很快。", "pinyin": "Zuìjìn jǐ nián wùjià shàngzhǎng de hěn kuài.", "meaningVi": "Mấy năm gần đây giá cả hàng hóa tăng rất nhanh."}],
    "hsk5_1217": [{"chinese": "他物理考试考了满分。", "pinyin": "Tā wùlǐ kǎoshì kǎo le mǎnfēn.", "meaningVi": "Anh ấy thi vật lý được điểm tuyệt đối."}],
    "hsk5_1218": [{"chinese": "请不要把贵重物品留在车里。", "pinyin": "Qǐng búyào bǎ guìzhòng wùpǐn liú zài chē lǐ.", "meaningVi": "Xin đừng để đồ vật quý giá lại trong xe."}],
    "hsk5_1219": [{"chinese": "这个小区的物业管理得很好。", "pinyin": "Zhège xiǎoqū de wùyè guǎnlǐ de hěn hǎo.", "meaningVi": "Khu chung cư này được quản lý bất động sản rất tốt."}],
    "hsk5_1221": [{"chinese": "他们今晚打算吃西餐。", "pinyin": "Tāmen jīnwǎn dǎsuàn chī xīcān.", "meaningVi": "Tối nay họ định ăn món Tây."}],
    "hsk5_1222": [{"chinese": "现在很多商店不再提供塑料吸管。", "pinyin": "Xiànzài hěn duō shāngdiàn bú zài tígōng sùliào xīguǎn.", "meaningVi": "Hiện nay nhiều cửa hàng không còn cung cấp ống hút nhựa nữa."}],
    "hsk5_1223": [{"chinese": "植物通过根部吸收水分。", "pinyin": "Zhíwù tōngguò gēnbù xīshōu shuǐfèn.", "meaningVi": "Thực vật hấp thụ nước qua rễ."}],
    "hsk5_1224": [{"chinese": "他穿着一身黑色西装。", "pinyin": "Tā chuānzhe yì shēn hēisè xīzhuāng.", "meaningVi": "Anh ấy mặc một bộ đồ tây màu đen."}],
    "hsk5_1225": [{"chinese": "这出戏非常感人。", "pinyin": "Zhè chū xì fēicháng gǎnrén.", "meaningVi": "Vở kịch này vô cùng cảm động."}],
    "hsk5_1227": [{"chinese": "这份合同的细节需要再确认一下。", "pinyin": "Zhè fèn hétong de xìjié xūyào zài quèrèn yíxià.", "meaningVi": "Chi tiết của bản hợp đồng này cần xác nhận lại."}],
    "hsk5_123": [{"chinese": "妈妈正在厨房里炒菜。", "pinyin": "Māma zhèngzài chúfáng lǐ chǎocài.", "meaningVi": "Mẹ đang xào rau trong bếp."}],
    "hsk5_1230": [{"chinese": "请先下载这个应用程序。", "pinyin": "Qǐng xiān xiàzài zhège yìngyòng chéngxù.", "meaningVi": "Xin hãy tải xuống ứng dụng này trước."}],
    "hsk5_1233": [{"chinese": "这个房间一直闲着，没人住。", "pinyin": "Zhège fángjiān yìzhí xiánzhe, méi rén zhù.", "meaningVi": "Căn phòng này cứ bỏ trống mãi, không ai ở."}],
    "hsk5_1234": [{"chinese": "他今天显得特别高兴。", "pinyin": "Tā jīntiān xiǎnde tèbié gāoxìng.", "meaningVi": "Hôm nay anh ấy tỏ ra đặc biệt vui vẻ."}],
    "hsk5_1235": [{"chinese": "显然，他并不同意这个方案。", "pinyin": "Xiǎnrán, tā bìng bù tóngyì zhège fāng'àn.", "meaningVi": "Rõ ràng là anh ấy không đồng ý với phương án này."}],
    "hsk5_1236": [{"chinese": "屏幕上显示着一行字。", "pinyin": "Píngmù shàng xiǎnshìzhe yì háng zì.", "meaningVi": "Trên màn hình hiển thị một dòng chữ."}],
    "hsk5_1237": [{"chinese": "这个县有很多历史古迹。", "pinyin": "Zhège xiàn yǒu hěn duō lìshǐ gǔjì.", "meaningVi": "Huyện này có rất nhiều di tích lịch sử."}],
    "hsk5_1238": [{"chinese": "警察很快赶到了事故现场。", "pinyin": "Jǐngchá hěn kuài gǎndào le shìgù xiànchǎng.", "meaningVi": "Cảnh sát nhanh chóng đến hiện trường vụ tai nạn."}],
    "hsk5_124": [{"chinese": "他昨天出了一场车祸。", "pinyin": "Tā zuótiān chū le yì chǎng chēhuò.", "meaningVi": "Hôm qua anh ấy bị một vụ tai nạn giao thông."}],
    "hsk5_1240": [{"chinese": "这座城市正在快速现代化。", "pinyin": "Zhè zuò chéngshì zhèngzài kuàisù xiàndàihuà.", "meaningVi": "Thành phố này đang hiện đại hóa nhanh chóng."}],
    "hsk5_1241": [{"chinese": "这条公交线路经过我家附近。", "pinyin": "Zhè tiáo gōngjiāo xiànlù jīngguò wǒ jiā fùjìn.", "meaningVi": "Tuyến xe buýt này đi qua gần nhà tôi."}],
    "hsk5_1243": [{"chinese": "科学家正在研究这种奇怪的自然现象。", "pinyin": "Kēxuéjiā zhèngzài yánjiū zhè zhǒng qíguài de zìrán xiànxiàng.", "meaningVi": "Các nhà khoa học đang nghiên cứu hiện tượng tự nhiên kỳ lạ này."}],
    "hsk5_1245": [{"chinese": "他对公司的现状不太满意。", "pinyin": "Tā duì gōngsī de xiànzhuàng bú tài mǎnyì.", "meaningVi": "Anh ấy không hài lòng lắm với hiện trạng của công ty."}],
    "hsk5_1246": [{"chinese": "这个乡的人口不多。", "pinyin": "Zhège xiāng de rénkǒu bù duō.", "meaningVi": "Xã này dân số không đông."}],
    "hsk5_1247": [{"chinese": "他们俩相处得很好。", "pinyin": "Tāmen liǎ xiāngchǔ de hěn hǎo.", "meaningVi": "Hai người họ sống với nhau rất hòa hợp."}],
    "hsk5_1248": [{"chinese": "他喜欢乡村的宁静生活。", "pinyin": "Tā xǐhuan xiāngcūn de níngjìng shēnghuó.", "meaningVi": "Anh ấy thích cuộc sống yên tĩnh ở nông thôn."}],
    "hsk5_125": [{"chinese": "他把自行车放在车库里。", "pinyin": "Tā bǎ zìxíngchē fàng zài chēkù lǐ.", "meaningVi": "Anh ấy để xe đạp trong nhà để xe."}],
    "hsk5_1251": [{"chinese": "这个问题和天气相关。", "pinyin": "Zhège wèntí hé tiānqì xiāngguān.", "meaningVi": "Vấn đề này có liên quan đến thời tiết."}],
    "hsk5_1252": [{"chinese": "这两件衣服的颜色很相似。", "pinyin": "Zhè liǎng jiàn yīfu de yánsè hěn xiāngsì.", "meaningVi": "Màu sắc của hai chiếc áo này rất giống nhau."}],
    "hsk5_1253": [{"chinese": "出国以后，他常常想念父母。", "pinyin": "Chūguó yǐhòu, tā chángcháng xiǎngniàn fùmǔ.", "meaningVi": "Sau khi ra nước ngoài, anh ấy thường xuyên nhớ nhung bố mẹ."}],
    "hsk5_1254": [{"chinese": "楼上传来一阵响声。", "pinyin": "Lóushàng chuánlái yí zhèn xiǎngshēng.", "meaningVi": "Từ tầng trên vọng lại một tiếng động."}],
    "hsk5_1256": [{"chinese": "你很难想象他当时有多害怕。", "pinyin": "Nǐ hěn nán xiǎngxiàng tā dāngshí yǒu duō hàipà.", "meaningVi": "Bạn khó mà tưởng tượng được lúc đó anh ấy sợ đến mức nào."}],
    "hsk5_1257": [{"chinese": "她把照片都放进了相册里。", "pinyin": "Tā bǎ zhàopiàn dōu fàngjìn le xiàngcè lǐ.", "meaningVi": "Cô ấy đã cho hết ảnh vào album."}],
    "hsk5_1258": [{"chinese": "这个项目下个月就要完成了。", "pinyin": "Zhège xiàngmù xià gè yuè jiù yào wánchéng le.", "meaningVi": "Hạng mục này tháng sau sẽ hoàn thành."}],
    "hsk5_1259": [{"chinese": "我忘了带橡皮，能借我用一下吗？", "pinyin": "Wǒ wàng le dài xiàngpí, néng jiè wǒ yòng yíxià ma?", "meaningVi": "Tôi quên mang tẩy, cậu cho mình mượn dùng một chút được không?"}],
    "hsk5_126": [{"chinese": "停车场里停满了各种车辆。", "pinyin": "Tíngchēchǎng lǐ tíngmǎn le gèzhǒng chēliàng.", "meaningVi": "Bãi đỗ xe đầy các loại phương tiện."}],
    "hsk5_1260": [{"chinese": "他一直保持积极向上的态度。", "pinyin": "Tā yìzhí bǎochí jījí xiàngshàng de tàidù.", "meaningVi": "Anh ấy luôn giữ thái độ tích cực, hướng lên."}],
    "hsk5_1262": [{"chinese": "年轻人的消费观念正在改变。", "pinyin": "Niánqīngrén de xiāofèi guānniàn zhèngzài gǎibiàn.", "meaningVi": "Quan niệm tiêu dùng của giới trẻ đang thay đổi."}],
    "hsk5_1263": [{"chinese": "这家公司很重视消费者的意见。", "pinyin": "Zhè jiā gōngsī hěn zhòngshì xiāofèizhě de yìjiàn.", "meaningVi": "Công ty này rất coi trọng ý kiến của người tiêu dùng."}],
    "hsk5_1264": [{"chinese": "饭后散步有助于消化。", "pinyin": "Fàn hòu sànbù yǒuzhùyú xiāohuà.", "meaningVi": "Đi dạo sau bữa ăn có ích cho tiêu hóa."}],
    "hsk5_1266": [{"chinese": "这双鞋子的销量一直很好。", "pinyin": "Zhè shuāng xiézi de xiāoliàng yìzhí hěn hǎo.", "meaningVi": "Doanh số của đôi giày này luôn rất tốt."}],
    "hsk5_1267": [{"chinese": "他的身影很快消失在人群中。", "pinyin": "Tā de shēnyǐng hěn kuài xiāoshī zài rénqún zhōng.", "meaningVi": "Bóng dáng anh ấy nhanh chóng biến mất trong đám đông."}],
    "hsk5_1268": [{"chinese": "这家公司主要负责产品销售。", "pinyin": "Zhè jiā gōngsī zhǔyào fùzé chǎnpǐn xiāoshòu.", "meaningVi": "Công ty này chủ yếu phụ trách bán sản phẩm."}],
    "hsk5_1269": [{"chinese": "这位小姐，请问您需要帮忙吗？", "pinyin": "Zhè wèi xiǎojiě, qǐngwèn nín xūyào bāngmáng ma?", "meaningVi": "Cô ơi, xin hỏi cô có cần giúp đỡ không?"}],
    "hsk5_127": [{"chinese": "这节车厢里人不多。", "pinyin": "Zhè jié chēxiāng lǐ rén bù duō.", "meaningVi": "Trong toa xe này không có nhiều người."}],
    "hsk5_1270": [{"chinese": "我们公司买了一台小型打印机。", "pinyin": "Wǒmen gōngsī mǎi le yì tái xiǎoxíng dǎyìnjī.", "meaningVi": "Công ty chúng tôi đã mua một chiếc máy in loại nhỏ."}],
    "hsk5_1271": [{"chinese": "这个数字小于一百。", "pinyin": "Zhège shùzì xiǎoyú yìbǎi.", "meaningVi": "Con số này nhỏ hơn một trăm."}],
    "hsk5_1272": [{"chinese": "这样做可以提高工作效率。", "pinyin": "Zhèyàng zuò kěyǐ tígāo gōngzuò xiàolǜ.", "meaningVi": "Làm như vậy có thể nâng cao hiệu suất công việc."}],
    "hsk5_1275": [{"chinese": "老师建议他多练习写作。", "pinyin": "Lǎoshī jiànyì tā duō liànxí xiězuò.", "meaningVi": "Giáo viên khuyên anh ấy nên luyện tập viết văn nhiều hơn."}],
    "hsk5_1276": [{"chinese": "新郎在婚礼上向大家敬酒。", "pinyin": "Xīnláng zài hūnlǐ shàng xiàng dàjiā jìngjiǔ.", "meaningVi": "Chú rể mời rượu mọi người trong lễ cưới."}],
    "hsk5_1277": [{"chinese": "这段经历对他的心理产生了很大影响。", "pinyin": "Zhè duàn jīnglì duì tā de xīnlǐ chǎnshēng le hěn dà yǐngxiǎng.", "meaningVi": "Trải nghiệm này đã gây ảnh hưởng lớn đến tâm lý của anh ấy."}],
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
