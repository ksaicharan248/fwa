

emoji_dict = {
    "1": "<:1_:1248255567307214858>",
    "2": "<:2_:1248255772312473722>",
    "3": "<:3_:1248255764364132362>",
    "4": "<:4_:1248255757514838098>",
    "5": "<:5_:1248255752083345418>",
    "6": "<:6_:1248255716603461755>",
    "7": "<:7_:1248255745393430571>",
    "8": "<:8_:1248255741471752255>",
    "9": "<:9_:1248255734462943275>",
    "10": "<:10:1248255726611337266>",
    "11": "<:11:1248255652166504488>",
    "12": "<:12:1248255708311584940>",
    "13": "<:13:1248255700426293298>",
    "14": "<:14:1248255692993990797>",
    "15": "<:15:1248255686811320361>",
    "16": "<:16:1248255671078748231>",
    "17": "<:17:1248255648039178290>",
    "18": "<:18:1248255642360348752>",
    "19": "<:19:1248255679123292232>",
    "20": "<:20:1248255662589345812>",
    "21": "<:21:1248255852159434753>",
    "22": "<:22:1248255846413238372>",
    "23": "<:23:1248255838259511336>",
    "24": "<:24:1248255829975498842>",
    "25": "<:25:1248255824120516711>",
    "26": "<:26:1248255818499887186>",
    "27": "<:27:1248255804373733450>",
    "28": "<:28:1248255796702351430>",
    "29": "<:29:1248255789982941344>",
    "30": "<:30:1248255782705827893>",
    "31": "<:31:1248255938041872385>",
    "32": "<:32:1248255930387140648>",
    "33": "<:33:1248255860665221242>",
    "34": "<:34:1248255911483674634>",
    "35": "<:35:1248255946367701094>",
    "36": "<:36:1248255920455159958>",
    "37": "<:37:1248255868945039440>",
    "38": "<:38:1248255901555757180>",
    "39": "<:39:1248255891879493682>",
    "40": "<:40:1248255878105399336>",
    "41": "<:41:1248255965632008244>",
    "42": "<:42:1248255973399855217>",
    "43": "<:43:1248255982463615068>",
    "44": "<:44:1248255958904475762>",
    "45": "<:45:1248255988088180746>",
    "46": "<:46:1248255994912313345>",
    "47": "<:47:1248255953372188803>",
    "48": "<:48:1248256003296985119>",
    "49": "<:49:1248256010813182004>",
    "50": "<:50:1248256018694275173>"
}


def find_emoji(value) :
    return emoji_dict.get(str(value) , "<:1_:1247868845662928936>")