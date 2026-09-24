"""Label-preserving representation adaptation. No new messages or pseudo-labels."""
import copy,hashlib,json,random
ZH_NAMES='查询闹钟 删除闹钟 设置闹钟 调低音量 静音 其他音量操作 调高音量 查询日程 删除日程 创建日程 烹饪咨询 查询菜谱 时区时间换算 查询日期时间 添加邮件联系人 查询邮件 查询邮件联系人 发送邮件 打招呼 讲笑话 随意闲聊 清扫操作 冲泡咖啡 改变灯光颜色 调暗灯光 关闭灯光 开启灯光 调亮灯光 关闭智能插座 开启智能插座 创建或添加清单 查询清单 删除清单 表达不喜欢音乐 表达喜欢音乐 查询音乐信息 音乐设置 查询新闻 播放有声书 玩游戏 播放音乐 播放播客 播放电台 货币汇率查询 词义定义查询 事实问答 数学问题 股票行情查询 推荐活动 推荐地点 推荐电影 发布社交动态 查询社交动态 下单外卖 查询外卖信息 出行路线查询 叫出租车 购买交通票 查询交通路况 查询天气'.split()
assert len(ZH_NAMES)==60

def transform(rows,intents):
 names=dict(zip(intents,ZH_NAMES));out=[]
 massive=[r for r in rows if r['source']=='massive']
 for row in rows:
  r=copy.deepcopy(row);seed=int(hashlib.sha256((r['source']+r['source_id']).encode()).hexdigest()[:16],16);rng=random.Random(seed);zh=r['language'].startswith('zh')
  structured=seed%4!=0
  if r['source']=='massive':
   if zh:r['q']['crit']={k:names[k] for k in r['q']['crit']}
   if seed%2==0:
    gold=r['original_label'];candidate=gold if rng.randrange(2)==0 else rng.choice([k for k in r['q']['crit'] if k!=gold]);target=int(candidate==gold);label=names[candidate] if zh else candidate.replace('_',' ')
    r['source']='massive_binary';r['q']={'t':'noul','ins':f'这条请求的意图是否是“{label}”？' if zh else f'Does this request express the intent "{label}"?','crit':{'false':'不符合该意图' if zh else 'The intent does not match','true':'符合该意图' if zh else 'The intent matches'}};r['target']=target
   if structured:
    others=[massive[rng.randrange(len(massive))]['state'] for _ in range(1)]
    pos=rng.randrange(2);messages=[{'id':f'm{i}','text':others[0]} for i in range(2)];messages[pos]['text']=r['state'];r['state']=json.dumps({'target_message_id':f'm{pos}','messages':messages},ensure_ascii=False)
    r['q']['ins']=('只判断target_message_id指定的消息，其他消息不影响答案。' if zh else 'Evaluate only the message selected by target_message_id. Other messages do not change the answer. ')+r['q']['ins']
  elif structured and r['source']=='crosswoz':
   turns=r['state'].split('\n');messages=[{'id':f'm{i}','text':t} for i,t in enumerate(turns)];r['state']=json.dumps({'target_message_id':messages[-1]['id'],'messages':messages},ensure_ascii=False);r['q']['ins']='只判断target_message_id指定的消息，结合前面的对话上下文。'+r['q']['ins'].replace('最后一句','目标消息')
  elif structured and r['source']=='t2':
   query,sep,doc=r['state'].partition('\n文本：')
   if sep:r['state']=json.dumps({'query':query.removeprefix('查询：'),'document':doc},ensure_ascii=False);r['q']['ins']='判断document对query的相关性，按原始四级相关性标注。'
  r['mapping_rule']=r['mapping_rule']+'+structure_intent_binary_v2';out.append(r)
 return out
