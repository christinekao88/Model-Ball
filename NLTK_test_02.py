"""
使用Python中的NLTK庫分析文字。使用NLTK的twitter_samples語料庫。
1.下載語料庫：
2.下載POS標記器。POS標記是對文字中的單詞進行標記的過程，使其與特定POS標記對應：名詞，動詞，形容詞，副詞等。
我們將使用NLTK的平均感知器標記器( averaged_perceptron_tagger)。平均感知器標記器使用感知器演算法來預測最可能給出該單詞的POS標籤。
"""
# import nltk
# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download()

from nltk.corpus import twitter_samples

"""
NLTK的twitter語料庫目前包含從Twitter Streaming API檢索的20,000條推文樣本。完整推文以行分隔的JSON形式儲存。
"""
# 用twitter_samples.fileids()來檢視語料庫中存在多少個JSON檔案
# print(twitter_samples.fileids())

# 可以返回推文字串
# print(twitter_samples.strings('tweets.20150430-223406.json'))

tweets = twitter_samples.strings('positive_tweets.json')
print(tweets)

"""
分詞:
Tokenization是將一系列字串分解為單詞、關鍵字、短語、符號和其他元素，我們稱之為分詞。
讓我們建立一個名為tweets_tokens的新變數，為其分配分詞的推文列表
"""
# 這個新變數tweets_tokens是一個列表，其中每個元素都是一個分詞列表。
tweets_tokens = twitter_samples.tokenized('positive_tweets.json') # list
print(tweets_tokens)

# 匯入NLTK的POS標記器
from nltk.tag import pos_tag_sents

"""
標記句子:
現在，我們可以標記每個token 。我們將建立一個新變數tweets_tagged，來儲存標記列表。
推文被表示為一個列表，對於每個token，我們都有關於其POS標籤的資訊。每個token/標記對都儲存為元組。
在NLTK中，形容詞(JJ)，單數名詞（NN），複數名詞（NNS）。
為簡化起見，我們只會通過跟蹤NN標記來計算單數名詞。
在下一步中，我們將計算在我們的語料庫中出現多少次JJ和NN。
"""
tweets_tagged = pos_tag_sents(tweets_tokens)
print(tweets_tagged)

"""
計算POS標籤:
我們將使用累加器（計數）變數跟蹤JJ並NN出現的次數，並在每次找到標記時不斷新增該變數。
"""
# 建立計數，我們將首先設定為零
JJ_count = 0
NN_count = 0
# 第一個迴圈將迭代列表中的每個推文。
# 第二個迴圈將通過每個推文中的每個token /標籤對進行迭代。
for tweet in tweets_tagged:
	for pair in tweet:
		tag = pair[1]  # 對於每對，我們將使用適當的元組索引查詢標記。
		if tag == 'JJ': # 使用條件語句檢查標籤是否匹配字串'JJ'或'NN'
			JJ_count += 1 # 如果標記匹配，我們將add（+=1）新增到適當的累加器
		elif tag == 'NN':
			NN_count += 1

# 檢視我們的指令碼找到多少個形容詞和名詞的話
print('Total number of adjectives = ', JJ_count)
print('Total number of nouns =', NN_count)