/**
テキストページ生成
エディタで作ったデータを表示させる側（編集不可）の設定
引数： 作成する場所のid
引数２： 表示させるJSONテキスト
戻り値： Quillエディタの生成情報
*/
function QuillPageMake(make_id, json_text) {
    let toolbarOptions; // ツールバーの機能設定
    let quill; // エディタ情報
    let json_data; //エディタに表示させるデータ（json形式）
    const themes = set_themes(); // エディタのテーマ（snow , bubble）

    // ツールバー機能の設定
    toolbarOptions = [
        //見出し
        [{
            header: [1, 2, 3, 4, 5, 6, false]
        }],
        //フォント種類
        [{
            font: []
        }],
        //文字寄せ
        [{
            align: []
        }],
        //太字、斜め、アンダーバー
        ["bold", "italic", "underline"],
        //文字色 //文字背景色
        [{
            color: []
        }, {
            background: []
        }],
        // リスト
        [{
            list: "ordered"
        }, {
            list: "bullet"
        }],
        //インデント
        [{
            indent: "-1"
        }, {
            indent: "+1"
        }],
        //画像挿入
        ["image"],
        //動画
        ["video"],
        //数式
        ["formula"],
        //URLリンク
        ["link"],

        ["code-block"],
    ];

    //渡ってきたID名に「#」をくっつける
    make_id = `#${make_id}`;

    //エディタの情報を生成
    quill = new Quill(make_id, {
        modules: {
            //ツールバーの設定
            syntax: true,
            toolbar: toolbarOptions,
        },
        placeholder: "入力してください",
        //ツールバーのあるデザイン
        theme: "bubble", //'snow' or 'bubble'
    });

    //エディタを入力不可にする
    quill.disable();

    //表示させる文章データを取得
    json_data = JSON.parse(json_text);

    //データを表示
    quill.setContents(json_data);

    return quill;
}


// テーマ設定（PCとスマホで切り替える画面幅で判定）
function set_themes() {
    let themes;
    if (window.parent.screen.width > 800) {
        themes = "snow";
    } else {
        themes = "bubble";
    }
    return themes;
}
