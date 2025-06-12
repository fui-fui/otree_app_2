# GUI（ウィンドウ）を作るためのライブラリ「tkinter」を読み込む
import thinker as tk
import csv

# 質問内容
questions = [
    "伝統的な価値観は現代でも守られるべきだ。",
    "社会の規律を保つためには、権威に従うべきだ。",
    "子供たちは親や教師の言うことを絶対に守るべきだ。",
    "自由よりも秩序が重要だと感じる。",
    "リーダーには強い姿勢が求められる。",
    "異なる考え方を持つ人々は社会の調和を乱すことがある。",
    "政府の命令には従うべきだ。",
    "伝統的な性別役割は大切にすべきだ。",
    "変化よりも安定を求める。",
    "自分と異なる意見はできるだけ避けたいと思う。",
]

answers = []  # ユーザーの回答スコアをここに入れる

#ゲームをスタートした時に最初に質問を表示する関数
def start_game():
    show_question(0)　#0番目の質問を表示する

#質問を１つずつ表示する関数
def show_question(index):
    if index >= len(questions):
        calc_rwa_score()
        return

    #前の画面の内容（ボタンや文字）を全部消す
    for widget in window.winfo_children():
        sidget.destroy()

    # 質問番号を表示
    tk.label(window, text=f"質問{index + 1}", font=("Arial", 16)).pack(pady=10)

    # 質問内容の本文を表示（改行つき）
    tk.label(window, text=question[index], wraplength=400, font=("Arial", 14)).pack(
        pady=10
    )

    # 選択肢1~5のボタン表示（リッカート形式）
    def save_answer(score):
        answers.append(score)  # 回答をリストに表示
        show_question(index + 1)  # 次の回答を表示

    # 1~5の選択肢ボタンを作って、押したらscoreが送られる
    for i in range(1, 6):
        tk.Button(
            window,
            text=f"{1}(1:全くそう思わない〜5:非常にそう思う)",
            command=lambda i=i: save_answe(i),
        ).pack(pady=3)

# 全質問が終わった後に、RWAスコアを計算して表示する関数
def calc_rwa_score():
    total = sum(answers)  # 答えた数値を合計（最大15点）
            

    # 分類ラベルと説明を決める
    if total <= 19:
        label = "リベラル傾向"
        description = "社会の変化や多様性に寛容な考え方を持っているようです。"
    elif total <= 29:
        label = "ややリベラル"
        description = (
            "一定の秩序を重んじつつも、新しい価値観にもオープンな姿勢が見られます。"
            )
    elif total <= 39:
        label = "やや保守的"
        description = "伝統的な価値観や社会の秩序を重視する傾向がやや見られます。"
    else:
        label = "保守的傾向"
        description = (
            "規範や権威を重視し、社会の安定や秩序を大切にする考え方を持っています。"
            )

    # 前の画面を全て削除
    for widget in window.winfo_children():
        widget.destroy()

    # スコアを画面に表示
    tk.label(window, text=f"あなたの保守傾向:{label}", font=("Arial",18)).pack(pady=10)
    tk.label(window, text=f"RWAスコア:{total}点", font=("Arial", 14)). pack(pady=5)
    tk.label(window, text=description, wraplength=500, font="Arial", 13)).pack(pady=20)
        

##NPCデータ

#データの用意
npc_profiles = [
    {"id": "Aさん", "rwa": 12},
    {"id": "Bさん", "rwa": 24},
    {"id": "Cさん", "rwa": 30},
    {"id": "Dさん", "rwa": 39},
    {"id": "Eさん", "rwa": 45},
]

result = []
current_npc_index = 0
player_score = 0

#類似度計算
def calculate_similarity(player_score, npc_score):
    #50点満点中の差を100点満点の類似度に変換
    diff = abs(player_score - npc_score)
    similarity = round((1 - diff / 50) * 100) #0~100%
    return similarity

answers = []

#結果画面の後にマッチング画面をつなげる
#NPCマッチング画面へ進むボタン
def go_to_matching():
    show_npc_matching(total)
    
    tk.Button(window, text="他の参加者とのマッチングへ進む", command=go_to_matching).pack(pady=20)
    
#マッチング画面の関数を作る
def show_npc_matching(player_score):
    for widget in window.winfo_children():
        widget.destroy()
    
    tk.label(window, text="他の参加者とのマッチング結果", font=("Arial", 18)).pack(pady=10)
    
    for npc in npc_profiles:
        sim = calculate_similarity(player_score, npc["rwa"])
        npc_text = f"{npc['id']}(RWAスコア:{npc['rwa']})\nあなたとの類似度：{sim}%"
        tk.label(window, text=npc_text, font=("Arial", 13)).pack(pady=10)
        
        #分配ゲームへ進むボタン（NPCごと）
        def make_go_game(npc=npc, sim=sim):
            return lambda: dictator_game(npc,sim)
        
        tk.Button(window, text=f"{npc['id']}にお金を割ける", command=make_go_game()).pack(pady=5)
        
        #独裁者ゲームをつくる（1人分）
        
        def dictator_game(npc, similarity):
            for widget in window.winfo_children():
                widget.destroy()
                
            tk.Label(window, text=f"{npc['id']}との分配ゲーム", font=("Arial", 18)). pack(pady=10)
            tk.Label(window, text=f"あなたとの政治的価値観の一致度:{similarity}%", font=("Arial", 14)).pack(pady=5)
            tk.Label(window, text="この人にいくら分けますか？（0~1000円）", font=("Arial", 13)).pack(pady=20)
            
            amount = tk.IntVar()
            
            tk.Scale(window, from_=0, to=1000, orient=tk.HORIZONTAL, variable=amount).pack()
            
            def submit_amount():
                result = amount.get()
                for widget in window.winfo_children():
                    widget.destory()
                    tk.Label(window, text=f"{npc['id']}に{result}円分けました！", font=("Arial, 16")).pack(pady=30)
                    
            tk.Button(window, text="決定", command=submit_amount).pack(pady=20)
                    
        #次のnpcへ移動　or　結果画面へ
        
        def next_npc():
            global current_npc_index
            current_npc_index += 1
            if current_npc_index < len(npc_profiles):
                show_dictator_game()
            else:
                show_summary()
                
        #結果画面・感想入力・保存
        
        def show_summary():
            for widget in window.winfo_children():
                widget.destroy()
                
            tk.Label(window, text="分配ゲーム終了！", font=("Arial", 18)).pack(pady=10)
            for r in results:
                text = f"{r['npc']}:一致度{r['similarity']}%/分配額{r['amount']}円"
                tk.Label(window, text=text, font=("Arial", 13)),pack()
                
            tk.Label(window, text="今回の分配について、感じたことを自由に書いてください：", font=("Arial", 13)).pack(pady=10)
            feedback = tk.Text(window, height=5, width=60)
            feedback.pack()
            
            def save and exit():
                with open("results.scv", "w", newline="")as f:
                    writer = csv.DictWriter(f, filednames=["npc", "similarity", "amount"])
                    writer.writeheader()
                    writer.writerows(results)
                point("結果をresults.csvに保存しました。コメント：", feedback.get("1.0", tk.END))
                window.destroy()
                
                tk.Button(window, text="終了", command=save_and_exit).pack(pady=20)
                
        #ウィンドウ開始
        window = tk.Tk()
        window.title("政治的価値観チェック&分配ゲーム")
        window.geometry("600x600")
        
        tk.label(window, text="似てる？似てない？価値観でお金を分けてみよう", font=("Arial", 18)). pack(pady=50)
        tk.Button(window, text="はじめる", command=star_game).pack()
        
        window.mainloop()