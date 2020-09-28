# 專題：Model Ball

## 目的
選擇前五局的大小分來做分析研究，利用機器學習讓模型判斷出在該比賽條件下，前五局最後的總分會是大於或小於基準。

## 事前規劃
![](https://i.imgur.com/Xi4v14X.png)

事前所須的準備資料，主要從兩大方向去進行，一方面是可以量化的數字型態資料，另一方面是無法量化的文字型態資料。

* 量化資料方面，除了主要的***歷史球賽紀錄***外，還收集了***天氣***資料，因為濕度會影響投手投出的球的運行軌跡和轉速；***大小分及賠率***當做比較基準，最後是***球場***資料，因為每個球場大小距離都不一樣，這也會影響到我們的判斷結果。

* 非量化資料方面，選擇了美國最普及的社群媒體 - twitter 來做分析。目的是想要從各大意見領袖的發文中，藉由情感分析去獲取大家對比賽的意見及看法，進而成為不同來源的參考依據。

## 架構示意圖
![](https://i.imgur.com/zDmegXd.jpg)
* 量化資料的部份，我們利用python從網路上的數據庫中爬取到原始資料後，先儲放在hadoop叢集上，清洗過後再送入模型中訓練，最後將結果存放至mysql。

* 非量化資料的部份，一樣是透過python的爬蟲套件從twitter上爬取相關帳號的文章，儲放至ES，當中也有利用到kafka做為溝通媒介分配工作，最後再將分析的結果透過kibana來做視覺化的呈現。

* 與使用者互動的部份，選擇了最方便普及的linebot，在我們的chatbot上使用者輸入了查詢之後，我們利用了kafka來確保使用者資料不丟失，也利用了redis來增加查詢效率，減少使用者等待的時間。以上除了hadoop我們是選擇在本地端架設之外，其餘的服務我們也都將其包進docker容器化並架設在GCP雲端平台上。

## [分工部分]-情感分析
![](https://i.imgur.com/1WOheXt.jpg)
情感分析流程首先為收集推特文章內容，使用到的套件有Tweepy與Twint接著，針對推文的部分做資料處理，處理完之後，利用TextBlob library做情感分析，最後將結果視覺化呈現，使用的是Elasticsearch的Kibana

![](https://i.imgur.com/n7PVLJC.jpg)

利用下關鍵字的方式去爬取推文，所下的關鍵字包含了MLB 與各球隊隊名，然後利用Tweepy跟Twint來爬取我們感興趣的推文內容

![](https://i.imgur.com/48v3oOZ.jpg)

以李奧納多的推文為範例，This is great progress．
我們可以設定This和is為stop word. 然後移除標點符號
剩下的great被判定為positive，progress 被判定為neutral
我們即可認爲這篇推文為一篇正向的推文

![](https://i.imgur.com/TkuMd9G.jpg)

在清理推文的部分，我們將對情感分析並無影響的部分移除，其中包含像是標點符號，Hashtags， Mentions，(網址) URLs
並且還原縮寫的部分，像是 I can't會還原成 I can not
另外表情符號在推文中是十分常出現的，所以我們也針對了表情符號的部分做文字的轉換

![](https://i.imgur.com/bxvF4hU.jpg)

以 "Hello MLB !! 😁  :-)  “為例 透過python還原成Hello MLB !! happy face Happy face smiley

![](https://i.imgur.com/KKk8DTY.jpg)
我們可以發現，原本的neutral推文約有33萬，經由把表情符號轉換成文字，我們可以多判定了5萬則推文為positive或是negative

![](https://i.imgur.com/g4ufKIo.jpg)
在判定推文情緒方面，仍然還是有很多因素造成推文會被判定為neutral，像是推文長度太短，或是推文含有縮寫

![](https://i.imgur.com/HHIvwED.jpg)
還有諷刺性的推文跟看不出明顯情緒的推文

![](https://i.imgur.com/iz8yGZ8.jpg)
最後視覺化呈現的部分我們呈現了不同語系國家的情感分析，我們可以發現英語在推特的使用還是佔了主要的部分，其次之為日文，然後才是西班牙文，另外也可以觀察到三種情緒分別在不同國家佔的比例

![](https://i.imgur.com/w0pnrHU.png)
我們也呈現了不同球隊聲量圖與情感分析關係圖，我們可以發現關於芝加哥小熊的推文數量最多，我們也能分別觀察每個球隊三種情緒推文的數量各佔多少
