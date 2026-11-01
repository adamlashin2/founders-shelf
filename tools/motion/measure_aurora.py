from PIL import Image; import numpy as np, json
from scipy import ndimage
A=np.asarray(Image.open('ref/aurora.png').convert('RGB')).astype(int); G=A.mean(2)
S=517/402; RX,LX,Y0=620,63,187
def hexc(c): return '#%02x%02x%02x'%tuple(int(v) for v in c)
def bb(x0,y0,x1,y1,cond):
    m=cond(A[y0:y1,x0:x1]); ys,xs=np.nonzero(m)
    return None if not len(xs) else (x0+xs.min(),y0+ys.min(),x0+xs.max(),y0+ys.max())
def pt(b,ox): return dict(x=round((b[0]-ox)/S,1),y=round((b[1]-Y0)/S,1),w=round((b[2]-b[0]+1)/S,1),h=round((b[3]-b[1]+1)/S,1))
dark=lambda c:c.mean(2)<90
out={}
def M(name,ox,box,cond):
    b=bb(*box,cond); out[name]=pt(b,ox) if b else None; print(f'{name:22s}',out[name])
R,L=RX,LX
# ---- right phone ----
M('wordmark',R,(670,280,800,320),dark)
M('heart',R,(970,270,1030,320),dark)
M('badge',R,(995,265,1030,300),lambda c:(c[...,0]>200)&(c[...,1]<120))
M('centre avatar',R,(830,300,930,400),lambda c:np.abs(c-np.array([253,250,250])).sum(2)>40)
M('post avatar',R,(670,505,725,560),lambda c:np.abs(c-255).sum(2)>60)
M('username',R,(722,520,820,545),dark)
M('post image',R,(630,540,1125,850),lambda c:np.abs(c-255).sum(2)>60)
M('liked by',R,(640,850,700,872),lambda c:c.mean(2)<180)
M('liked names',R,(700,848,815,872),dark)
M('caption l1',R,(640,875,1115,898),dark)
M('caption l2',R,(640,898,1115,920),dark)
M('centre btn',R,(840,1220,920,1275),lambda c:c.mean(2)<40)
M('person icon',R,(715,1235,760,1275),lambda c:c.mean(2)<170)
M('search icon',R,(995,1235,1045,1275),lambda c:c.mean(2)<170)
# ---- left phone ----
M('close btn',L,(80,265,155,340),lambda c:(np.abs(c-A[260,120]).sum(2)>25))
M('title l1',L,(130,685,520,735),lambda c:c.mean(2)>225)
M('title l2',L,(230,735,420,780),lambda c:c.mean(2)>225)
M('meta l1',L,(200,792,450,816),lambda c:c.mean(2)>150)
M('seg selected',L,(85,880,260,960),lambda c:c.mean(2)>240)
M('Going label',L,(140,920,200,945),lambda c:(c[...,1]>c[...,0]+40))
M('Not Going lbl',L,(270,920,370,945),lambda c:c.mean(2)>200)
M('Maybe lbl',L,(440,920,510,945),lambda c:c.mean(2)>200)
M('hosted',L,(225,1048,420,1070),lambda c:(c[...,2]>c[...,1]+20)&(c[...,2]>170))
M('body l1',L,(190,1074,450,1095),lambda c:c.mean(2)>190)
M('body l4',L,(160,1143,480,1165),lambda c:c.mean(2)>190)
M('scroll text',L,(200,1250,415,1275),lambda c:c.mean(2)>200)
M('scroll pill',L,(185,1238,460,1285),lambda c:np.abs(c-A[1262,175]).sum(2)>14)
M('host avatar',L,(290,995,350,1048),lambda c:(c[...,0]>c[...,2]+40))
json.dump(out,open('ref/aurora_boxes.json','w'),indent=1)
# ---- colours ----
for n,(x,y) in {'R header tint':(700,330),'R header tint2':(1050,320),'R below header':(640,470),'R page':(640,1000),
  'badge':(1011,281),'L close fill':(116,320),'L bg near close':(165,300),'seg container':(330,900),'seg container2':(520,940),'seg selected':(110,905),
  'Going green':(167,909),'card fill':(120,1000),'card fill2':(520,1180),'bg left of card':(75,1100),'scroll pill fill':(200,1262),'bg near pill':(170,1262),
  'bottom bar':(660,1290),'bottom bar top':(880,1215),'notch area':(1050,825)}.items():
    print(f'colour {n:18s} {hexc(A[y,x])}')
# text colours: extreme pixels
def ext(box,fn):
    x0,y0,x1,y1=box; s=A[y0:y1,x0:x1].reshape(-1,3); return hexc(s[fn(s)])
print('liked-by grey', ext((640,850,700,872),lambda s:s.sum(1).argmin()))
print('names', ext((700,848,815,872),lambda s:s.sum(1).argmin()))
print('caption', ext((640,875,1115,898),lambda s:s.sum(1).argmin()))
print('meta brightest', ext((200,792,450,816),lambda s:s.sum(1).argmax()))
print('title brightest', ext((130,685,520,735),lambda s:s.sum(1).argmax()))
print('hosted', ext((225,1048,420,1070),lambda s:(s[:,2]-s[:,0]).argmax()), ext((225,1048,420,1070),lambda s:s.sum(1).argmax()))
print('body brightest', ext((190,1074,450,1095),lambda s:s.sum(1).argmax()))
print('notlabel brightest', ext((270,920,370,945),lambda s:s.sum(1).argmax()))
