from transitions.extensions import GraphMachine
from threading import Thread
import time
import vlc
import random

last_times = 1

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    #is going to function
    def is_going_to_state1(self, update):
        text = update.message.text
        return text.lower() == 'go to state1'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def is_going_to_state3(self, update):
        text = update.message.text
        return text.lower() == '你好'

    def is_going_to_setNote(self, update):
        text = update.message.text
        return text.lower() == '[提醒]'

    def is_going_to_setNoteTimer(self, update):
        text = update.message.text
        return True



    def is_going_to_eyehurt(self, update):
        text = update.message.text
        return text.lower() == '我眼酸'

    
    def is_going_to_uncomfort(self, update):
        text = update.message.text
        return text.lower() == '我不舒服'

    def is_going_to_mouthache(self, update):
        text = update.message.text
        return text.lower() == '我嘴巴破掉了'

    def is_going_to_mouthacheReason(self, update):
        text = update.message.text
        return (text.lower() == '沒有' or text.lower() == '有')

    def is_going_to_mouthacheDoing(self, update):
        text = update.message.text
        return text.lower() == '那怎麼辦?'

    def is_going_to_seeDoctor(self, update):
        text = update.message.text
        return True

    def is_going_to_backpain(self, update):
        text = update.message.text
        return text.lower() == '我腰痛'
    
    def is_going_to_backpainLong(self, update):
        text = update.message.text
        return (text.lower() == '有一段時間' or text.lower() == '蠻久')

    def is_going_to_backpainShort(self, update):
        text = update.message.text
        return text.lower() == '最近'

    def is_going_to_backpainSport(self, update):
        text = update.message.text
        return text.lower() == '運動撞到'

    def is_going_to_backpainSit(self, update):
        text = update.message.text
        return text.lower() == '坐比較久ㄅ'



    def is_going_to_badMoodBegin(self, update):
        text = update.message.text
        return text.lower() == '我心情不好'

    def is_going_to_badMood(self, update):
        text = update.message.text
        return text.lower() != '謝謝你'

    def is_going_to_badMoodFinish(self, update):
        text = update.message.text
        return text.lower() == '謝謝你'




    #doing function
    def on_enter_state1(self, update):
        update.message.reply_text("I'm entering state1")
        update.message.reply_photo("https://www.python.org/static/community_logos/python-logo-master-v3-TM.png")
        update.message.reply_photo(open("img/show-fsm.png","rb"))
        self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("I'm entering state2")
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("早安")
        #update.message.reply_photo(photo=open("/img/show-fsm.png"),"rb")
        self.go_back(update)

    def on_exit_state3(self, update):
        print('Leaving state3')


    def on_enter_setNote(self, update):
        update.message.reply_text("請問要設定甚麼提醒?\n先打出時間(24小時制)\n在打事項\n\nex.13:24\n要記得吃藥")

    def on_exit_setNote(self, update):
        print('Leaving setNote')

    def on_enter_setNoteTimer(self, update):
        

        index = update.message.text.find("\n")
        inputTime = update.message.text[:index]
        thing = update.message.text[index+1:]
        hour = int(inputTime[:2])
        minute = int(inputTime[3:])
        
        if hour<0 or minute<0:
            update.message.reply_text("抱歉~你的設定負數的時間哦~請重新設定")
            self.go_back(update)
        elif hour<int(time.localtime()[3]):
            update.message.reply_text("抱歉~你的設定是過去的時間哦~請重新設定")
            self.go_back(update)
        elif hour==int(time.localtime()[3]) and minute<int(time.localtime()[4]):
            update.message.reply_text("抱歉~你的設定是過去的時間哦~請重新設定")
            self.go_back(update)
        else:
            #print("hour: ",hour)
            #print("mintue: ",minute)
            #print("thing: ",thing)

            #noteThread = Thread(target=myTimer, args=(hour,minute,update,thing))
            noteThread = Thread(target=alarm_clock, args=(hour,minute,update,thing))
            noteThread.start()

            update.message.reply_text("已經完成設定")
            self.go_back(update)

    def on_exit_setNoteTimer(self, update):
        print('Leaving setNoteTimer')


    def on_enter_eyehurt(self, update):
        update.message.reply_text("你一定是眼睛用太久了")
        update.message.reply_text("來跟我一起做動眼操")
        
        instance = vlc.Instance()

        update.message.reply_text("先閉上眼睛5秒")
        player = instance.media_player_new()
        media = instance.media_new("https://translate.google.com.tw/translate_tts?ie=UTF-8&q=%E5%85%88%E9%96%89%E4%B8%8A%E7%9C%BC%E7%9D%9B5%E7%A7%92&tl=zh-CN&total=1&idx=0&textlen=7&tk=554570.926010&client=t&prev=input")
        player.set_media(media)
        player.play()
        count_down(5)

        update.message.reply_text("然後眼睛往左看5秒")
        media = instance.media_new("https://translate.google.com.tw/translate_tts?ie=UTF-8&q=%E7%84%B6%E5%BE%8C%E7%9C%BC%E7%9D%9B%E5%BE%80%E5%B7%A6%E7%9C%8B5%E7%A7%92&tl=zh-CN&total=1&idx=0&textlen=9&tk=315330.170173&client=t&prev=input")
        player.set_media(media)
        player.play()
        count_down(5)

        update.message.reply_text("換往右看5秒")
        media = instance.media_new("https://translate.google.com.tw/translate_tts?ie=UTF-8&q=%E7%84%B6%E5%BE%8C%E7%9C%BC%E7%9D%9B%E5%BE%80%E5%8F%B3%E7%9C%8B5%E7%A7%92&tl=zh-CN&total=1&idx=0&textlen=9&tk=698228.847883&client=t&prev=input")
        player.set_media(media)
        player.play()
        count_down(5)

        update.message.reply_text("換往上看5秒")
        media = instance.media_new("https://translate.google.com.tw/translate_tts?ie=UTF-8&q=%E7%84%B6%E5%BE%8C%E7%9C%BC%E7%9D%9B%E5%BE%80%E4%B8%8A%E7%9C%8B5%E7%A7%92&tl=zh-CN&total=1&idx=0&textlen=9&tk=455154.42637&client=t&prev=input")
        player.set_media(media)
        player.play()
        count_down(5)

        update.message.reply_text("換往下看5秒")
        media = instance.media_new("https://translate.google.com.tw/translate_tts?ie=UTF-8&q=%E7%84%B6%E5%BE%8C%E7%9C%BC%E7%9D%9B%E5%BE%80%E4%B8%8B%E7%9C%8B5%E7%A7%92&tl=zh-CN&total=1&idx=0&textlen=9&tk=283534.132337&client=t&prev=input")
        player.set_media(media)
        player.play()
        count_down(5)

        update.message.reply_text("好了~有舒服點嗎?")
        self.go_back(update)

    def on_exit_eyehurt(self, update):
        print('Leaving eyehurt')


    def on_enter_badMoodBegin(self, update):
        update.message.reply_text("你還好嗎?說來聽聽")

    def on_exit_badMoodBegin(self, update):
        print('Leaving badMoodBegin')

    def on_enter_badMood(self, update):
        moodArray = find_mood(update.message.text)
        print("moodArray: ",moodArray)
        resolute = bad_mood_respond(moodArray[0],moodArray[1],moodArray[2])
        #resolute = bad_mood_respond(2,3,1,global_times)
        print("resolute: ",resolute)
        number = random.randint(1,3)
        print("number: ",number)

        if resolute == 1:
            if number == 1:
                update.message.reply_text("別生氣別生氣~")
            elif number == 2:
                update.message.reply_text("這就是人生啊~很多事情沒辦法如自己所願的")
            elif number == 3:
                update.message.reply_text("好扯哦~")
        elif resolute == 2:
            if number == 1:
                update.message.reply_text("換個角度想嘛!會比較舒服的")
            elif number == 2:
                #update.message.reply_text("好啦~走~我們去喝一杯")
                #update.message.reply_photo(open("img/show-fsm.png","rb"))
                update.message.reply_photo(open("img/1.png","rb"))
            elif number == 3:
                #update.message.reply_text("好啦~走~我們去喝一杯")
                #update.message.reply_photo(open("img/show-fsm.png","rb"))
                update.message.reply_photo(open("img/3.png","rb"))
        elif resolute == 3:
            if number == 1:
                update.message.reply_text("好啦~走~我們去喝一杯")
            elif number == 2:
                update.message.reply_text("好啦~不然我唱首歌給你聽")
                update.message.reply_text("http://17sing.tw/share_song/index.html?sid=32780942")
                #update.message.reply_photo(open("img/show-fsm.png","rb"))
                update.message.reply_photo(open("img/2.png","rb"))
            elif number == 3:
                #update.message.reply_text("好啦~走~我們去喝一杯")
                #update.message.reply_photo(open("img/show-fsm.png","rb"))
                update.message.reply_photo(open("img/4.png","rb"))
        

    def on_exit_badMood(self, update):
        #update.message.reply_voice("https://www.youtube.com/watch?v=2cCligRwFoI")
        print('Leaving badMood')

    def on_enter_badMoodFinish(self, update):
        update.message.reply_text("加油~我會一直在這聽你說的")
        self.go_back(update)

    def on_exit_badMoodFinish(self, update):
        print('Leaving badMoodFinish')



    def on_enter_uncomfort(self, update):
        update.message.reply_text("你怎麼啦??")

    def on_exit_uncomfort(self, update):
        print('Leaving uncomfort')

    def on_enter_mouthache(self, update):
        update.message.reply_text("你是不是最近太常熬夜=3=?")

    def on_exit_mouthache(self, update):
        print('Leaving mouthache')

    def on_enter_mouthacheReason(self, update):
        update.message.reply_text("嘴破有很多原因\n以中醫來看，就是「火氣太大」\n以西醫來看，有可能是下來原因\n●精神緊張、壓力過大\n●營養不均衡\n●睡眠不足\n●過度勞累\n●女性內分泌失調\n●免疫能力減退\n●家族遺傳\n通常10％的嘴破發生原因是缺乏維生素B、C，造成黏膜發炎並破裂；而臨床上80％的患者都是因為情緒緊張造成免疫功能失調、或因此造成肌肉緊繃，使黏膜的血液循環不良而造成嘴破\n")

    def on_exit_mouthacheReason(self, update):
        print('Leaving mouthacheReason')

    def on_enter_mouthacheDoing(self, update):
        update.message.reply_text("1.多吃水果，尤其是奇異果、柳丁、蘋果等等\n2.	吃點退火食物，如綠豆、薏仁、仙草\n3.	早點休息\n4.	多運動、多喝水\n\n*盡量不要吃荔枝等上火水果\n*用鹽水漱口是沒用的")

    def on_exit_mouthacheDoing(self, update):
        print('Leaving mouthacheDoing')

    def on_enter_seeDoctor(self, update):
        update.message.reply_text("如果長時間沒有好或持續惡化，建議還是去看個醫生ㄅ")
        self.go_back(update)

    def on_exit_seeDoing(self, update):
        print('Leaving seeDoctor')



    def on_enter_backpain(self, update):
        update.message.reply_text("多久了??")

    def on_exit_backpain(self, update):
        print('Leaving backpain')

    def on_enter_backpainLong(self, update):
        update.message.reply_text("你有運動撞到或是坐姿不正確常翹腳嗎?")

    def on_exit_backpainLong(self, update):
        print('Leaving backpainLong')

    def on_enter_backpainShort(self, update):
        update.message.reply_text("那先多運動，不要坐太久、要正確坐姿，而且可以用熱敷稍微舒緩")
        update.message.reply_photo("https://media.taaze.tw/showTakeLook/1002724010.jpg")

    def on_exit_backpainShort(self, update):
        print('Leaving backpainShort')

    def on_enter_backpainSport(self, update):
        update.message.reply_text("那建議你最好去醫院照個X光檢查一下有沒有傷到骨頭或神經")

    def on_exit_backpainSport(self, update):
        print('Leaving backpainSport')

    def on_enter_backpainSit(self, update):
        update.message.reply_text("因為長時間久坐壓迫或是翹腳導致骨盆有高低差，所以會痛\n做一段時間要起來走走，並且維持正確坐姿")
        update.message.reply_photo("http://www.citytalk.tw/bbs/data/attachment/forum/201105/20/1105201149084a54e9e6ad5928.jpg")

    def on_exit_backpainSit(self, update):
        print('Leaving backpainSit')

def find_mood(str):
    sadArray = ["難過","哭","分手"]
    badArray = ["無力","煩","糟","痛"]
    angryArray = ["生氣","幹","機巴","怒"]
    
    moodArray = [0,0,0]

    for element in sadArray:
        index = str.find(element)
        while index!=-1:
            moodArray[0]+=1
            index = str.find(element,index+1)

    for element in badArray:
        index = str.find(element)
        while index!=-1:
            moodArray[1]+=1
            index = str.find(element,index+1)

    for element in angryArray:
        index = str.find(element)
        while index!=-1:
            moodArray[2]+=1
            index = str.find(element,index+1)

    return moodArray


def bad_mood_respond(sad,bad,angry):
    global last_times
    sadCoeff = 0.45
    badCoeff = 0.4
    angryCoeff = 0.15

    anlysis = sadCoeff*sad + badCoeff*bad + angryCoeff*angry
    total = sad + bad + angry
    if total!=0:
        temp_anlysis = (anlysis/total)
    else:
        temp_anlysis = 0

    p = 0.7
    anlysis = temp_anlysis*p + (1-p)*last_times
    last_times = anlysis
    print("anlysis: ",anlysis)

    if anlysis <= 0.3:
        return 1
    elif anlysis>0.3 and anlysis<=0.8:
        return 2
    elif anlysis>0.8:
        return 3



def count_down(seconds):
    while seconds>0:
        time.sleep(1)
        seconds-=1
        print('{:02d}'.format(seconds), end='\r')
    
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new('sound/count_down.mp3')
    player.set_media(media)
    player.play()
    print("finish")


def alarm_clock(hour,minute,update,todo):    
    while True:
        now = time.localtime()
        time.sleep(5)
        print(now[5])
        if(hour==now[3] and minute==now[4]):
            #myFunction(todo)
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new('sound/count_down.mp3')
            player.set_media(media)
            player.play()
            update.message.reply_text(todo)
            break
    
    

#'''
# Function to be called when the timer expires
def myFunction(todo):
    print ('Did anyone call me? ',todo)

#'''
# Function with the timer
def myTimer(hour,seconds,update,todo):
    print(seconds)
    time.sleep(seconds)
    myFunction(todo)
    update.message.reply_text(todo)
#'''

'''
# Thread that will sleep in background and call your function
# when the timer expires.
myThread = Thread(target=myTimer, args=(4,))
myThread.start()
'''