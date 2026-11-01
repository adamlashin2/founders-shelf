import pickle,base64,io,sys
from PIL import Image
pkl,step,out=sys.argv[1],sys.argv[2],sys.argv[3]; occ=int(sys.argv[4]) if len(sys.argv)>4 else 0
d=pickle.load(open(pkl,'rb')); fr=d['frames']; i0=[i for n,i in d['marks'] if n==step][occ]; t0=fr[i0][0]
pick=[i0-1]+[i for i in range(i0,min(i0+60,len(fr))) if int((fr[i][0]-t0)*1000)//50!=int((fr[i-1][0]-t0)*1000)//50][:9]
ims=[Image.open(io.BytesIO(base64.b64decode(fr[i][1]))) for i in pick]
row=Image.new('RGB',(sum(m.width+4 for m in ims),ims[0].height),(255,0,255)); x=0
for m in ims: row.paste(m,(x,0)); x+=m.width+4
row.save(out,quality=80); print([round((fr[i][0]-t0)*1000) for i in pick])
