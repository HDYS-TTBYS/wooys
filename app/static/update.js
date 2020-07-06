/**
テキストエディタの生成(中身有り)
引数１： 作成する場所のid
引数２： 表示させるJSONテキスト
戻り値： Quillエディタの生成情報
*/
function QuillUpdateEditorMake(make_id, json_text) {
    let toolbarOptions; // ツールバーの機能設定
    let quill; // エディタ情報
    const themes = set_themes(); // エディタのテーマ（snow , bubble）

    // ツールバー機能の設定
    toolbarOptions = [
        //見出し
        [{
            header: [1, 2, 3, 4, 5, 6, false],
        },],
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
        },
        {
            background: [],
        },
        ],
        // リスト
        [{
            list: "ordered",
        },
        {
            list: "bullet",
        },
        ],
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
        theme: themes, //'snow' or 'bubble'
    });

    //表示させる文章データを取得
    json_data = JSON.parse(json_text);

    //データを表示
    quill.setContents(json_data);


    /**
     * Step1. ローカル画像選択
     *
     */
    function selectLocalImage() {
        //フォーム作成
        const input = document.createElement("input");
        input.setAttribute("type", "file");
        input.click();

        // 変更を検知してサーバー転送関数を呼び出す
        input.onchange = () => {
            const file = input.files[0];

            // バリデート
            if (/^image\//.test(file.type)) {
                saveToServer(file);
            } else {
                console.warn("画像のみアップロードできます。");
            }
        };
    }

    /**
     * Step2. ajaxでサーバーへ転送
     *
     * @param {File} file
     */
    function saveToServer(file) {
        const fd = new FormData();
        fd.append("image", file);

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/uploadByFile/", true);
        // for Django
        // ------------------------------------------------
        let CSRF_KEY_NAME = "csrftoken=";
        let csrf = _.find(document.cookie.split(";"), (cookie) => {
            return cookie.trim().substr(0, CSRF_KEY_NAME.length) == CSRF_KEY_NAME;
        })
        if (csrf) xhr.setRequestHeader("X-CSRFToken", csrf.trim().substr(CSRF_KEY_NAME.length));
        // ------------------------------------------------
        xhr.onload = () => {
            if (xhr.status === 200) {
                // url response = {"data": download_url}
                const url = JSON.parse(xhr.responseText).data;
                insertToEditor(url);
            }
        };
        xhr.send(fd);
    }

    /**
     * Step3. rich editorに挿入
     *
     * @param {string} url
     */
    function insertToEditor(url) {
        const range = quill.getSelection();
        quill.insertEmbed(range.index, "image", `${url}`);
    }

    // クイルエディターへ画像ハンドラーの追加
    quill.getModule("toolbar").addHandler("image", () => {
        selectLocalImage();
    });

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
