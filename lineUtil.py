
import time
from blynkutil import (blynkGetPinValue, blynkGetPinHistoryValue)
import datetime
from modeldb import (dbListAllByUser, dbAddbyUser, dbCheckExist)
from stock import (getXrateById, getStockById,getXrateName, getXrateName)

RED='AA0000'
GREEN='00AA01'  
#                <4        6       8         10        12      14        16      18        20        22      24      26        28      30      32        34
TEMPCOLORGRID=['330066','000066','000099','0000CC','003366','004C99','0066CC','0080FF','3399FF','009999','006633','009900','FF8000','FF3333','990000','CC0000']
#                 20        40        60      80      100
HUMIDCOLORGRID=['FF8000','9933FF','66FF66','0066CC','004C99','006600']

def generateStockJSON(n0,n1,n2,par,startTime):
  t0="""
    {
      "type": "bubble",
      "styles": {
        "footer": {
          "separator": true
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "{0}",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "{1}",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "{2}",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": true
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "dollars",
                    "size": "sm",
                    "color": "#111111",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "buy",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "sell",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "CRITERIA",
                    "size": "xxs",
                    "color": "#111111",
                    "align": "end",
                    "flex": 2
                  }
                ]
              },
    """
  ct="""
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [


                {
                  "type": "text",
                  "text": "{XID}",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 1
                },
                {
                  "type": "text",
                  "text": "{XIDTXT}",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 1
                },
                {
                  "type": "text",
                  "text": "{XBUY}",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end",
                  "flex":1
                },
                {
                  "type": "text",
                  "text": "{XSELL}",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end",
                  "flex":1
                },
                {
                  "type": "text",
                  "text": "{XCRITERIA}",
                  "size": "xxs",
                  "color": "#111111",
                  "align": "end",
                  "flex":2
                }
              ]
            }
  """

  t1="""
            {
              "type": "separator",
              "margin": "xxl"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "margin": "xxl",
              "contents": [
                {
                  "type": "text",
                  "text": "股 票",
                  "size": "sm",
                  "color": "#555555",
                  "margin": "md"
                },
                {
                  "type": "text",
                  "text": "成交",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                },
                {
                  "type": "text",
                  "text": "漲跌",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                },
                {
                  "type": "text",
                  "text": "%",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                },
                {
                  "type": "text",
                  "text": "條件",
                  "size": "xxs",
                  "color": "#111111",
                  "align": "end"
                }
              ]
            },
  """
  st="""
            {
              "type": "box",
              "layout": "horizontal",
              "margin": "md",
              "contents": [
                {
                  "type": "text",
                  "text": "{st0}",
                  "size": "xs",
                  "color": "#555555",
                  "margin": "md"
                },
                {
                  "type": "text",
                  "text": "{st2}",
                  "size": "sm",
                  "color": "#{stc}",
                  "align": "end"
                },
                {
                  "type": "text",
                  "text": "{st3}",
                  "size": "sm",
                  "color": "#{stc}",
                  "align": "end"
                },
                {
                  "type": "text",
                  "text": "{st4}",
                  "size": "sm",
                  "color": "#{stc}",
                  "align": "end"
                },
                {
                  "type": "text",
                  "text": "{st5}",
                  "size": "xxs",
                  "color": "#111111",
                  "align": "end"
                }
              ]
            }
  """
        
  t2="""
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "data source  ",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "台灣銀行, 證交所",
                "color": "#aaaaaa",
                "size": "xxs",
                "align": "end"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "generated at ",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "{3}",
                "color": "#aaaaaa",
                "size": "xxs",
                "align": "end"
              }
            ]
          }
        ]
      }
     }
  """
  target=t0.replace('{0}',n0)
  target=target.replace('{1}',n1)
  target=target.replace('{2}',n2)
  #  tmpCur=['USD','美金','buy','sell','criteria']
  #  tmpStk=['中美晶','5483','成交','漲跌','漲跌百分比','criteria','color']

  for curc in par[0]:
    stemp=ct.replace('{XID}',curc[0])
    stemp=stemp.replace('{XIDTXT}',curc[1])
    stemp=stemp.replace('{XBUY}',curc[2])
    stemp=stemp.replace('{XSELL}',curc[3])   # text
    stemp=stemp.replace('{XCRITERIA}',curc[4])    # criteria
    target +=stemp+',\n'
  #if not len(par[0]) :
  #  target +=',\n'
  target += t1
  commaC=0

  for curs in par[1]:
    stemp=st.replace('{st0}',curs[0])     #股票名稱
  #    stemp=stemp.replace('{st1}',curs[1])  #代碼
    stemp=stemp.replace('{st2}',curs[2])  #成交
    stemp=stemp.replace('{st3}',curs[3])  #漲跌
    stemp=stemp.replace('{st4}',curs[4])  #漲跌幅
    stemp=stemp.replace('{st5}',curs[5])  #條件
    stemp=stemp.replace('{stc}',curs[6])  #顏色
    commaC+=1
    target += stemp
    if (commaC < len(par[1])) : 
      target += ',\n'
    else:
      target +='\n' 
  #if not len(par[1]) :
  #  target +=',\n'

  pDate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  periodTime=round(time.time()-startTime,1)

  target+=t2.replace('{3}', pDate+' ('+str(periodTime)+'s)')


  #  print (target)

  return target


def getTempGrid(temp):
  if temp == '--.-':
    return 'A0A0A0'
  else:
    cidx = int((float(temp)-4)//2)
    return TEMPCOLORGRID[cidx]

def getHumidGrid(humid):
  if humid=='--.-':
    return 'A0A0A0'
  else:
    cidx = int((float(humid))//20 )
    return HUMIDCOLORGRID[cidx]


#def generateTempJSON(TITLE, it,ih,ot,oh,timestamp):
def generateTempJSON(param,startTime):
  template="""  
    {
    "type": "bubble",
    "hero": {
      "type": "image",
      "url": "https://i.imgur.com/HCtu129.jpg",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "uri": "http://google.com"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "{TITLE}",
          "weight": "bold",
          "size": "xl"
        },
        {
          "type": "box",
          "layout": "vertical",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "box",
              "layout": "horizontal",
              "spacing": "lg",
              "contents": [
                {
                  "type": "text",
                  "text": "\u5ba4\u5167",
                  "color": "#aaaaaa",
                  "size": "sm",
                  "flex": 1
                },
                {
                  "type": "text",
                  "text": "{IT}",
                  "wrap": true,
                  "color": "#{ITc}",
                  "size": "xxl",
                  "flex": 3,
                  "align": "end"
                },
                {
                  "type": "separator"
                },
                {
                  "type": "text",
                  "text": "{IH}%",
                  "wrap": true,
                  "color": "#{IHc}",
                  "size": "md",
                  "flex": 2,
                  "align": "end"
                }
              ]
            },
            {
              "type": "separator"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "spacing": "lg",
              "contents": [
                {
                  "type": "text",
                  "text": "\u5ba4\u5916",
                  "color": "#aaaaaa",
                  "size": "sm",
                  "flex": 1
                },
                {
                  "type": "text",
                  "text": "{OT}",
                  "wrap": true,
                  "color": "#{OTc}",
                  "size": "xxl",
                  "flex": 3,
                  "align": "end"
                },
                {
                  "type": "separator"
                },
                {
                  "type": "text",
                  "text": "{OH}%",
                  "wrap": true,
                  "color": "#{OHc}",
                  "size": "md",
                  "flex": 2,
                  "align": "end"
                }
              ]
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "spacing": "sm",
      "contents": [
        {
          "type": "text",
          "text": "data from lugia at",
          "size": "xxs",
          "color": "#aaaaaa",
          "flex": 0
        },
        {
          "type": "text",
          "text": "{timestamp}",
          "color": "#aaaaaa",
          "size": "xxs",
          "align": "end"
        }        
      ],
      "flex": 0
    }
  }

  """
  output=template
  #TITLE, it,itc,ih,ihc,ot,otc,oh,ohc,timestamp

  output=output.replace('{TITLE}',param[0])
  if not int(float(param[1])) in  range(2,40): param[1]='--.-'
  if not int(float(param[3])) in  range(2,40): param[3]='--.-'
  if not int(float(param[2])) in  range(2,99): param[2]='--.-'
  if not int(float(param[4])) in  range(2,99): param[4]='--.-'

  output=output.replace('{IT}',param[1])
  output=output.replace('{IH}',param[2])
  output=output.replace('{OT}',param[3])
  output=output.replace('{OH}',param[4])

  periodTime=round(time.time()-startTime,1)

  output=output.replace('{timestamp}',param[5]+ ' ('+str(round(time.time()- startTime,1))+'s)')
  
  output=output.replace('{ITc}',getTempGrid(param[1]))
  output=output.replace('{OTc}',getTempGrid(param[3]))

  output=output.replace('{IHc}',getHumidGrid(param[2]))
  output=output.replace('{OHc}',getHumidGrid(param[4]))
  return output

def getHomeTemps(blynkServer, blynkAuth,startTime):
  param=['Sweet HOME']
  param.append(str(round(float(blynkGetPinValue(blynkServer, blynkAuth,'V1')),1)))
  param.append(str(round(float(blynkGetPinValue(blynkServer, blynkAuth,'V2')),1)))
  param.append(str(round(float(blynkGetPinValue(blynkServer, blynkAuth,'V3')),1)))
  param.append(str(round(float(blynkGetPinValue(blynkServer, blynkAuth,'V6')),1)))
  param.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  print ('temperature : ',param)
  flexMsg=generateTempJSON(param,startTime)
  
  return flexMsg

def generateHomeJSON(VERSION):
  s="""
  {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "SWEET HOME",
        "size": "xl",
        "weight": "bold"
      }
    ]
  },
  "hero": {
    "type": "image",
    "url": "https://i.imgur.com/ULBHr3f.jpg",
    "size": "full",
    
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "message",
                  "label": "匯率 股票",
                  "Text": "Finance"
                }
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "message",
                    "label": "家裡溫濕度",
                    "Text": "Temp"
                }
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "message",
                  "label": "主目錄",
                  "Text": "Menu"
                }
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "---",
                  "displayText": "---",
                  "data": "TABLE"
                }
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
       {
        "type": "text",
        "text": "by cnwang 2018 ",
        "size": "xs",
        "color": "#aaaaaa",
        "flex": 3
        },
        {
        "type": "text",
        "text": "V{VERSION} ",
        "size": "xs",
        "align": "end",
        "color": "#aaaaaa",
        "flex": 1
        }

      ]
    }
  }
  """
  s=s.replace('{VERSION}',str(VERSION))
  return s


def generateStockByUser(uid, userName, startTime):
  h1="""
    {
      "type": "bubble",
      "styles": {
        "footer": {
          "separator": true
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "{HEAD}",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "{TITLE}",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "{ADDR}",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": true
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "幣 ",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": " 別",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "匯 率",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "條 件",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 2
                  }
                ]
              },

  """
  ct1="""
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "{SUBJECT}",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "{SUBJECTTXT}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "{PRICE}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "{CRITERIA}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 2
                  }
                ]
              },  
  """
  sep="""
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "股",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "票",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "參考市價",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "條 件",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 4
                  }
                ]
              },
  """
  st1="""
              
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "{SUBJECT}",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "{SUBJECTTXT}",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "{PRICE}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "{CRITERIA}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "flex": 4
                  }
                ]
              }


  """
  ft1="""
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "generated ",
                "size": "xxs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "{timestamp}",
                "color": "#aaaaaa",
                "size": "xxs",
                "align": "end"
              }
            ]
          }
        ]
      }
    }
  """

  output=""
  output +=h1.replace ('{HEAD}', 'Finance' )
  output=output.replace('{TITLE}', userName+u' 注意的')
  output=output.replace('{ADDR}', 'cnwang406@gmail.com')

  stockData=dbListAllByUser(uid, 'c')
  print ('Xrate ==',stockData)
  print ('len(stockData)=', len(stockData))
  #sqlStr="SELECT id, type, fid, fidtxt, criteria FROM stocks WHERE (userid = '{0}' AND type='{1}'".format(userId, stype)
  count=0
  for sd in stockData:
    output += ct1
    output=output.replace('{SUBJECT}', sd[2])
    output=output.replace('{PRICE}', getXrateById(sd[2]))
    output=output.replace('{SUBJECTTXT}', sd[3])
    output=output.replace('{CRITERIA}', sd[4])
    count+=1
    print ('round ',count)
    #if count <= len(stockData):
    #  print (' add ,')
    #output+=','

  output+=sep
  stockData=dbListAllByUser (uid, 's')

  #sqlStr="SELECT id, type, fid, fidtxt, criteria FROM stocks WHERE (userid = '{0}' AND type='{1}'".format(userId, stype)
  count=0
  for sd in stockData:
    output += st1
    output=output.replace('{SUBJECT}', sd[2])
    output=output.replace('{PRICE}', getStockById(sd[2]))
    output=output.replace('{SUBJECTTXT}', sd[3])
    output=output.replace('{CRITERIA}', sd[4])
    count+=1
    if count< len(stockData):
      output+=','

  output+=ft1 
  output=output.replace('{timestamp}',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' ('+str(round(time.time()- startTime,1))+'s)')
  print(output)
  return output


def generateHelpJSON(startTime):
  s="""
      {
      "type": "bubble",
      "styles": {
        "footer": {
          "separator": true
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "HELP",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "可用的指令",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "cnwang406@gmail.com",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": true
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "cmd",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "說明",
                    "size": "sm",
                    "color": "#111111",
                    "flex": 3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "LIST",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "show all monitor xrate / stocks",
                    "size": "sm",
                    "color": "#111111",
                    "wrap": true,
                    "flex": 3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "+nnnn",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "加 monitor 股票. - 刪除. 三位數 匯率, 後面為criteria>, <, * ",
                    "size": "sm",
                    "color": "#111111",
                    "wrap": true,
                    "flex": 3
                  }
                ]
              },
              {
                "type": "separator",
                "margin": "xxl"
              }
              
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "generated at ",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": " {timestamp} ",
                "color": "#aaaaaa",
                "size": "xxs",
                "align": "end"
              }
            ]
          }
        ]
      }
    }
    """

  output = s.replace('{timestamp}',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' ('+str(round(time.time()- startTime,1))+'s)')
  return output

def updateStock(param):
  pass
