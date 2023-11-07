import requests
from bs4 import BeautifulSoup

def data_get(login_id,password):

    # ユーザーエージェントの設定
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # ログイン情報
    login_payload = {
        'data[Staff][login_id]':login_id,
        'data[Staff][password]':password
    }

    # セッションの作成
    session = requests.session()

    # ログインリクエストを送信
    login_url = 'https://www.join-kk.jp/mobile/users/login'  # ログインページのURL
    login_response = session.post(login_url, data=login_payload, headers=headers)

    # ログイン成功の確認
    if login_response.status_code == 200 and login_response.url == "https://www.join-kk.jp/mobile/mypages/":
        # ログインが成功し、mypagesにリダイレクトされた場合
        events_get = session.get("https://www.join-kk.jp/mobile/events/search/1", headers=headers)
        
        #イベント一覧ページにアクセスできた場合
        if events_get.status_code == 200:
            #お仕事一覧のページのhtmlを読み込み
            soup = BeautifulSoup(events_get.content, 'html.parser')
            #イベントごとの詳細URLをリストに格納
            detail_urls = []
            for link in soup.find_all('a', href=True):
                if '/event_jobs/choice/' in link['href']:  # 詳細URLの部分URLを特定
                    detail_urls.append(link['href'])
            
            #各業務の情報を格納するリストを作成
            event_info_list = []
            #変数の初期設定
            artist = None
            place = None
            date = None
            work_time = None
            work_matter = None
            reserve_stats = None
            
            #URLリストからfor文で一つ一つ読み込む
            for detail_url in detail_urls:
                full_detail_url = "https://www.join-kk.jp" + detail_url
                detail_response = session.get(full_detail_url)
                
                #アクセスが成功した場合
                if detail_response.status_code == 200:
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser',)

                    #アーティスト名と会場名の読み取り
                    title_elements = detail_soup.find("span",style="color:#000000;").find_all(string=True)
                    br_count = 0
                    for char in title_elements:
                        if "\n" in char:
                            br_count += 1 
                        if br_count == 1:
                            continue
                        elif br_count == 2:
                            place = char.replace("\r\n","")
                        
                        elif br_count == 3:
                            artist = char.replace("\r\n","")
                            break
                    
                    #各業務の日付、時間、業務内容、予約状態の読み取り
                    form_elements = detail_soup.find(["form"])
                    if form_elements == None: # 仕事が一つもない場合はスキップ
                        continue
                    for element in form_elements.find_all(["div","table"]):
                        tag_name = element.name

                        #divの場合（日付の情報）
                        if tag_name == "div":
                            style_attribute = element.get("style")
                            if style_attribute and 'background:#CCCCCC;color:#000000;' in style_attribute: # スタイルが特定の値を持つ場合のみ処理
                                date = element.text[:8]
                                
                        #tableの場合（時間、業務内容、予約状態の情報）
                        if tag_name == "table":
                            td_elements = element.find_all("td")
                            #チェックボックスの状態
                            on_check_box = td_elements[0]
                            #業務内容と時間の要素
                            work_info = [char.replace(" ","").replace("\r","").replace("\n","") for char in td_elements[1].find_all(string=True)]
                            #htmlの要素数で判別
                            reserved_or_not = len(on_check_box)
                            cansel_or_not= len(work_info)

                            #チェックボックスの状態が文字だった場合
                            if reserved_or_not == 1:
                                text = on_check_box.find_all(string=True)[0]
                                #キャンセル待ちの場合
                                if text == '\r\n\t\t\t        \t\t\t        ｷｬﾝｾﾙ待ち中\u3000\r\n\t\t\t        \t\t\t        ':
                                    reserve_stats = "キャンセル待ち中"
                                    work_matter, work_time = work_info[3:5]
                                #予約中だった場合
                                elif text == '\r\n\t\t\t        \t\t\t        予約中\u3000\r\n\t\t\t        \t\t\t        ':
                                    reserve_stats = "予約中"
                                    work_matter, work_time = work_info[:2]
                                #例外処理
                                else:
                                    reserve_stats = "例外な状態です。"
                                    work_matter, work_time = ["不明","不明"]

                            #チェックボックスの状態がチェックボックスだった場合
                            #キャンセル待ちではない場合
                            elif cansel_or_not == 2:
                                reserve_stats = "予約可能"
                                work_matter, work_time = work_info
                            #キャンセル待ちの場合
                            elif cansel_or_not == 6:
                                reserve_stats = "キャンセル待ち"
                                work_matter, work_time = work_info[3:5]
                            #例外処理
                            else:
                                reserve_stats = "例外な状態です。"
                                work_matter, work_time = ["不明","不明"]
                    
                        #業務の詳細情報をリストに格納
                        event_info_list.append({
                            "アーティスト": artist,
                            "会場": place,
                            "日付": date,
                            "時間": work_time,
                            "業務内容": work_matter,
                            "予約状態": reserve_stats
                        })
                    
                else:
                    print("詳細リンクにアクセスできませんでした")
            
        else:
            print("予約受付中の仕事一覧の取得に失敗")
    else:
        print("ログイン失敗")

    # セッションをクローズ
    session.close()

    return event_info_list

if __name__ == "__main__":
    data = data_get("519976471","8wzmqy")
    for char in data:
        print(f'''==========
アーティスト名:{char["アーティスト"]}
会場:{char["会場"]}
日時:{char["日付"]}|{char["時間"]}
業務内容:{char["業務内容"]}
予約状態:{char["予約状態"]}         
''')
