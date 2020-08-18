"""
Kakaotalk Analyzer

2017103758 Cho Moon Gi (KHU Software Convergence)

Last Update Date: 2017-12-09

"""


import codecs
import numpy as np
import webbrowser
import tkinter as tk

from tkinter import filedialog
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc
from collections import Counter
from konlpy.tag import Twitter
from wordcloud import WordCloud

#Basic Settings
root = Tk()
twitter = Twitter()
member=Counter()
chattime=Counter()
chat=[]
sentences_tag=[]
noun_adj_list = []
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
extra_except_list_file= open('extra_except_list.txt', 'r')
extra_except_list = extra_except_list_file.read().splitlines()

#Open KakaoTalk Chat Log File
root.filename = filedialog.askopenfilename(initialdir = "C:/Images",title = "choose your file",filetypes = [("text files","*.txt")])
f = codecs.open(root.filename, 'r', 'utf-8')
f.readline()
f.readline()
f.readline()
f.readline()
sentences = f.readlines()     
f.close()

#Garbled Korean Fix Code
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

#Chat Log Parsing Code
for stc in sentences :
     if stc.startswith('-'):
          None
     else:
          if stc.startswith('['):
               firstname=stc.find('[')
               secondname=stc.find(']')
               firsttime=stc.find('[', firstname + 1)
               secondtime=stc.find(':', firsttime + 1)
               member[stc[firstname+1:secondname]] += 1
               chattime[stc[firsttime+1:secondtime]] += 1
               chat.append(stc[secondtime+5:])

#Emoji Delete Code
for i in range(len(chat)):
     chat[i] = chat[i].translate(non_bmp_map)

#Word Analysis Code     
for sentence in chat:
     sentences_tag.append(twitter.pos(sentence))     
for sentence in sentences_tag:
     for word, tag in sentence:
          if tag in ['Noun']:
               if len(word)>1:
                    if word not in extra_except_list:
                         noun_adj_list.append(word)

#Dictionary Code
words = Counter(noun_adj_list)
common_words=dict(words.most_common(20))
common_members=dict(member.most_common(20))
common_chattimes=dict(chattime.most_common(24))
wclist = dict(words.most_common(40))

#Tkinter Button Code
def member_button():
     y_pos = np.arange(len(common_members))
     plt.barh(y_pos, list(common_members.values()), align='center', alpha=0.5)
     plt.yticks(y_pos, common_members)
     plt.xlabel('Frequency of Conversations Per Member')
     plt.title('KakaoTalk Analyzer')
     plt.show()
def word_button():
     y_pos = np.arange(len(common_words))
     plt.barh(y_pos, list(common_words.values()), align='center', alpha=0.5)
     plt.yticks(y_pos, common_words)
     plt.xlabel('Frequency of Words Used In The Conversation')
     plt.title("KakaoTalk Analyzer")
     plt.show()
def chattime_button():
     y_pos = np.arange(len(common_chattimes))
     plt.barh(y_pos, list(common_chattimes.values()), align='center', alpha=0.5)
     plt.yticks(y_pos, common_chattimes)
     plt.xlabel('Time When The Members Talked')
     plt.title("KakaoTalk Analyzer")
     plt.show()
def wordcloud_button():
     wordcloud=WordCloud(font_path="c:\Windows\Fonts\malgun.ttf", relative_scaling = 0.2, background_color="white",).generate_from_frequencies(wclist)
     plt.figure(figsize=(16,8))
     plt.imshow(wordcloud)
     plt.axis("off")
     plt.show()

def select():
     sf = "value is %s" % var.get()
     color = var.get()
     
def websearch_button():
     sf = "value is %s" % var.get()
     query = var.get()                                  
     url = 'https://www.google.co.kr/search?q='+query
     webbrowser.open(url)

#Tkinter UI Code     
root.title("KakaoTalk Analyzer")
root.geometry('500x100+500+100')
var = tk.StringVar(root)

var.set('Select Word')
choices = common_words.keys()

optionbutton = tk.OptionMenu(root, var, *choices)
optionbutton.pack(side='bottom', padx=10, pady=10)

memberbutton = Button(root, text="Members", width=10, command=member_button)
memberbutton.pack(side='left', padx=10, pady=10)

wordbutton = Button(root, text="Words", width=10, command=word_button)
wordbutton.pack(side='left', padx=10, pady=10)

chattimebutton = Button(root, text="Time", width=10, command=chattime_button)
chattimebutton.pack(side='right', padx=10, pady=10)

wordcloudbutton = Button(root, text="Wordcloud", width=10, command=wordcloud_button)
wordcloudbutton.pack(side='right', padx=10, pady=10)

websearchbutton = Button(root, text="Search!", width=10, command=websearch_button)
websearchbutton.pack(side='bottom', padx=10, pady=10)

root.mainloop()


