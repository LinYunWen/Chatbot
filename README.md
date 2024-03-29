# body feeling bot

## prerequirement
 - python3
 - telegram
 - network
 - ngrok (如果使用本機作為伺服器)

## setup
    pip3 install requirement.txt
    pip3 install python-vlc

## purpose
1. 因為考量到自己最近身體不是很好，不過常常去診所看醫生，卻只是被簡單問個一兩句就結束，有時候都不知道是不是醫生人比較多，所以比較隨便，還是真的只是小問題。而且因為台灣的健保使得看病很便宜，所以有時沒甚麼事的小病，也會去看醫生，非常浪費醫療資源。
2. 而當如果要吃藥或是網路上掛號後，常常會一忙就忘記這些事，如果這些小事寫上行事曆又會顯得很雜亂，所以才希望有個可以提醒的功能
3. 因為去年我有個好朋友跟他女朋友分手，他連續好幾天心情都很難過，想跟我聊天或是談心，可是我剛好那幾個禮拜很忙幾乎天天都在系館到3.4點，所以沒有辦法第一時間陪在他身邊，看他變成行屍走肉，我自己也妥是難過，所以才想要可以安慰別人的功能，雖然還是有差，但是我想多多少少可以為他分擔一些不愉快，甚至給他一些鼓勵，或許我朋友就不會像個殭屍一樣度過了半年。

## finite start machine
![](https://i.imgur.com/4ee9wUr.png)

## usage
主要有三個功能:
1. **設定提醒事件鬧鐘**
可以用留言設定需要被提醒的事件和提醒時間，當時間到時，*bot會傳送提醒的事件作為訊息*，來通知使用者時間到了要做甚麼。
2. **簡易診斷身體狀況**
將身體不舒服的狀況以訊息做輸入，並且跟著bot的回覆類似醫生問診做問答，最後會簡單告訴使用者，*身體出了甚麼狀況和應該要如何解決*。
3. **心情抒發**
可以將自己不好的心情以訊息方式傳送，bot會以相對應的來給予鼓勵或安慰

### 設定提醒事件鬧鐘
1. state: user
    - input: ```"[提醒]"```
        - response: 
            ```
            請問要設定甚麼提醒?
            先打出時間(24小時制)
            再打事項
            ex.13:24
            要記得吃藥
            ```
2. state: setNote
    - input: 
        ```
        13:30
        要記得吃藥
        ```
        - response:
        ```"已經完成設定"```
        - error:
            ```
            "抱歉~你的設定負數的時間哦~請重新設定" or
            "抱歉~你的設定過去的時間哦~請重新設定"

            (如果時間設定為過去的時間或是負數時間，並重回到user state)
            ```
3. result:
    ``` 
    "要記得吃藥"
    
    (當時間到所設定的時間，伴隨BeapBeap聲)
    ```


### 簡易診斷身體狀況
目前有三種資訊系學生較為常見症狀可以診斷
- 嘴破
- 腰痛
- 眼睛痠
1. state: user
    - input: ```"我不舒服"```
        - response: ```"你怎麼啦??"```
2. state: uncomfort
    - input: 
        ```
        "我嘴巴破掉了" or
        "我眼酸" or
        "我腰痛"
        ```
        - response:
            會根據輸入進入到不同的狀態並給予不同的回覆
            ```
            嘴破:
                "你是不是最近太常熬夜=3=?"
            腰痛:
                "多久了??"
            眼酸:
                "你一定是眼睛用太久了"
                "來跟我一起做動眼操"
            ```
#### 嘴破
3. state: mouthache
    - input:```"沒有" or "有"```
        - response:
            ```
            嘴破有很多原因
            以中醫來看，就是「火氣太大」
            以西醫來看，有可能是下來原因
            ●精神緊張、壓力過大
            ●營養不均衡
            ●睡眠不足
            ●過度勞累
            ●女性內分泌失調
            ●免疫能力減退
            ●家族遺傳
            通常10％的嘴破發生原因是缺乏維生素B、C，
            造成黏膜發炎並破裂；而臨床上80％的患者都
            是因為情緒緊張造成免疫功能失調、或因此造
            成肌肉緊繃，使黏膜的血液循環不良而造成嘴破
            ```
4. state: mouthacheReason
    - input:```"那怎麼辦?"```
        - response:
            ```
            1.多吃水果，尤其是奇異果、柳丁、蘋果等等
            2.吃點退火食物，如綠豆、薏仁、仙草
            3.早點休息
            4.多運動、多喝水

            *盡量不要吃荔枝等上火水果
            *用鹽水漱口是沒用的
            ```
#### 腰痛

5. state: backpain
    - input: ```有一段時間 or 蠻久 or 最近```
        - response:
            ```
            long:
                "你有運動撞到或是坐姿不正確常翹腳嗎?"
            short:
                "那先多運動，不要坐太久、要正確坐姿，而且可以用熱敷稍微舒緩"
            ```
            ![](https://i.imgur.com/h0pxc7A.png)

6. state: backpainLong
    - input:```運動撞到 or 坐比較久ㄅ```
        - response:
            ```
            運動撞到:
                "那建議你最好去醫院照個X光檢查一下有沒有傷到骨頭或神經"
            坐比較久:
                "因為長時間久坐壓迫或是翹腳導致骨盆有高低差，所以會痛，做一段時間要起來走走，並且維持正確坐姿"
            ```
        ![](https://i.imgur.com/WosCjjt.png)
        


#### 眼睛痠
7. state: eyehurt
    - input: ```<no input>```
        - response:
            (會伴隨google小姐的聲音，並且自動隔5秒傳送下一則訊息)
            ```
            "先閉上眼睛5秒"
            "然後眼睛往左看5秒"
            "換往右看5秒"
            "換往上看5秒"
            "換往下看5秒"
            "好了~有舒服點嗎?"
            ```
8. state: seeDoctor
    (在每個症狀的最後狀態都接到seeDoctor)
    - input:```<no input>```
        - response:
        ```
        "如果長時間沒有好或持續惡化，建議還是去看個醫生ㄅ"
        ```

### 心情抒發
1. state: user
    - input: ```"我心情不好"```
        - response: ```"你還好嗎?說來聽聽"```
2. state: badMoodBegin
    - input: ```<any input>```
        - response: ``` <none>```
3. state: badMood
    - input: ```<any input>```
        - response:
            (根據你所做的輸入去做簡單的運算，先判斷是難過、失落、生氣狀態，而有以下不同的回覆等等，可能有圖片有文字或是有聲音訊息)
            ```
            angry:
                "別生氣別生氣~"
                "這就是人生啊~很多事情沒辦法如自己所願的"
            bad:
                "換個角度想嘛!會比較舒服的"

            sad:
                "好啦~走~我們去喝一杯"
            ```
            ![](https://i.imgur.com/Oi8SVFv.png)
            ![](https://i.imgur.com/n6vJDSX.png)
            ![](https://i.imgur.com/xfyOuv2.png)
            ![](https://i.imgur.com/v0FKwun.png)

4. state: badMoodFinish
    - input:```"謝謝你"```
        - response:```"加油~我會一直在這聽你說的"```

     
## problem
1. 目前所給的詞語還不能隨意點，必須要非常明確
2. 再傳送圖片上，沒有close
3. 不能多個人同時使用此bot
4. 聲音目前只能出現在server端，無法直接傳送
## next objective
1. 將一些症狀資料可以動態從網路上爬取
2. 可以自動生成新的診斷狀態
3. 對話在更人性化
