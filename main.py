import tkinter as tk
import random
from PIL import Image,ImageTk,ImageDraw,ImageFont
root=tk.Tk()
sw=800
sh=600
scene=0
can=True
turn=None
phase=None
P = None
root.geometry(f"{sw}x{sh}")
root.title("pygameから逃げるな godotから逃げるな tkinterに甘えるな")
class Draw():
    # mainから毎フレーム呼ばれる
    def __init__(self):
        self.canvas=tk.Canvas(root,bg="white", width=sw, height=sh)
    def draw(self,data):
        # 毎フレームキャンバスを置いて、中身を消してから描画
        self.canvas.pack()
        self.canvas.delete("all")
        if scene == 0:
            duel_button=self.canvas.create_rectangle(0,500,200,700,fill="red",tag="duel")
            self.canvas.tag_bind("duel", "<Button-1>", duelstart)
        if scene == 1:
            hand=data['hand']
            field=data['field']
            hp=data['hp'][0]
            ehp=data['hp'][1]
            self.canvas.photos=[]

            font = ("MS Gothic", 16, "bold")
            self.canvas.create_text(sw-80,sh-80,text=hp,fill="black",font=font)
            self.canvas.create_text(sw-80,80,text=ehp,fill="black",font=font)
            for i in range(len(hand)):#はんどのかーど　
                id=hand[i]
                photo=cardmake(id)
                self.canvas.create_image(10+i*90,sh-130,image=photo,anchor=tk.NW,tag=f"hand_{str(i)}")# val番目のカードはid
                self.canvas.photos.append(photo)
                self.canvas.tag_bind(f"hand_{str(i)}", "<Button-1>", lambda e,val=i,id=id:cardplay(id,val))
            for i in range(len(field)):
                id=field[i]
                photo=cardmake(id)
                self.canvas.create_image(10+i*90,sh-300,image=photo,anchor=tk.NW,tag=f"field_{str(i)}")# val番目のカードはid
                self.canvas.photos.append(photo)
                self.canvas.tag_bind(f"field_{str(i)}", "<Button-1>", lambda e,val=i,id=id:print("フィールドのカード",id,val))

            phase_button=self.canvas.create_rectangle(sw-100,sh/2,sw,sh/2+100,fill="red",tag="phase")
            self.canvas.tag_bind("phase", "<Button-1>", lambda phase=phase:phasechange(btn=True))
        if scene == 2:
            result=data['result']
            font = ("MS Gothic", 16, "bold")
            self.canvas.create_text(sw-80,sh-80,text=result,fill="black",font=font)
            ret_button=self.canvas.create_rectangle(0,sh/2,100,sh/2+100,fill="red",tag="ret")
            self.canvas.tag_bind("ret", "<Button-1>", lambda font=font:sc(0))
def sc(a):
    global scene
    scene=a

def phasechange(btn=None):
    global phase,turn
    if btn:
        if phase == "main" and turn == "player":
            pass
        else:
            print("押すタイミングじゃねぇよタコ")
            return
    if phase == "draw":
        phase = "main"
    elif phase == "main":
        phase = "end"
    else:
        if turn == "player":
            turn == "enemy"
        else:
            turn == "player"
        phase = "draw"


class Player():
    def __init__(self):
        self.hand=[]
        self.deck=[]
        self.field=[]
        self.hp=20
D=Draw()

class Game():
    def __init__(self):
        pass
    def load(self):
        self.card={
            "test":{"name":"おお","type":"unit","damage":2,"atk":3,"hp":2,"text":"おお"},
            "test2":{"name":"おお？","type":"spell","text":"お\nお"}
        }
G=Game()
G.load()


def main():#mainaminanisfniamiamiaminaminamianimnaimanmianmianmianminaimnamnaina
    
    #毎フレーム実行したいものだけ書く
    if scene == 0:# scene 0はホーム画面
        D.draw({"none":None}) # drawは、辞書に入ったものを中で変数として取り出すので、送りつけるときは辞書にパッケージングする
    if scene == 1:
        D.draw({"hand":P.hand,"field":P.field,"hp":[P.hp,E.hp]})
        if phase == "draw" and turn == "player":
            P.hand.append("test")
            phasechange()
        if phase == "end":
            damage=0
            for i in P.field:
                d=G.card[i]["damage"]
                damage+=d
            E.hp -= damage
            phasechange()
        if P.hp < 1:
            result_check("lose")
        elif E.hp < 1:
            result_check("win")
    if scene == 2:
        D.draw({"result":result})

            
        
        
    root.after(16,lambda: main())

def result_check(a):
    global scene,result
    sc(2)
    result = a

def duelstart(event):#デュエルスタートする時用のシーン変更
    global scene,P,E,turn,phase
    P=Player()
    E=Player()
    turn = "player"
    phase = "main"
    P.hand=["test","test2"]
    sc(1)

def cardplay(id,val):#カードをプレイするときに
    print(id,val)
    if tche(id) == "unit":
        if len(P.field) < 5:
            print("プレイした！")
            c=P.hand.pop(val)
            P.field.append(c)
        else:
            print("盤面　is いっぱい")

def tche(id):
    #type_check
    a=G.card[id]["type"]
    print(a)
    return a

def cardmake(id):#カード画像を作る。バインドとかは、呼び出し元で設定する。
    card_w = 70
    card_h = 120
    font = ImageFont.truetype("meiryo.ttc", 10)
    img=Image.new("RGB",(card_w,card_h),(255,0,255))
    draw = ImageDraw.Draw(img)
    t=G.card[id]["text"]
    draw.text((5,card_h/2),t,fill=(0,0,0),font=font)
    n=G.card[id]["name"]
    draw.text((5,5),n,fill=(0,0,0),font=font)
    photo = ImageTk.PhotoImage(img)
    return photo



main()
root.mainloop()

# ゲームルール:カードをプレイして、盤面をつくる。
# エンドフェイズ時に、自分の盤面の打点を相手hpに与える。
# メインフェイズ中に1回、ユニット同士で戦闘もできる。