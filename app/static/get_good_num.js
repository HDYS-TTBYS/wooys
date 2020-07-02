function getGoodNum(article_id, user_id) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/good/?&article_id=" + article_id + "&user_id=" + user_id, true);
    xhr.onload = () => {
        if (xhr.status === 200) {
            const good_num = JSON.parse(xhr.responseText).good_num;
            const good_num_div = "good_num_" + String(article_id);
            document.getElementById(good_num_div).innerHTML = String(good_num)
        }
    };
    xhr.send();
}

function getGoodNumButton(article_id, user_id) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/good/?&article_id=" + article_id + "&user_id=" + user_id, true);
    xhr.onload = () => {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const good_button = document.getElementById("good_button");
            const good_button_val = document.getElementById("good_button_val");
            const good_num = document.getElementById("good_num");
            if (response.user_id === "undefined") {
                //ログインしていない
                good_button.disabled = true
                good_button.className = "btn btn-primary"
                good_button_val.innerHTML = "いいね(未ログイン)"
                good_num.innerHTML = response.good_num
            } else if (response.is_good === 0) {
                //いいねしていない
                good_button.className = "btn btn-primary"
                good_button_val.innerHTML = "いいねする"
                good_num.innerHTML = response.good_num
            } else {
                //いいね済
                good_button.className = "btn btn-secondary"
                good_button_val.innerHTML = "いいねを外す"
                good_num.innerHTML = response.good_num
            }
        }
    };
    xhr.send();
}

function clickGoodButton(article_id, user_id) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/good/", true);
    // for Django
    // ------------------------------------------------
    let CSRF_KEY_NAME = "csrftoken=";
    let csrf = _.find(document.cookie.split(";"), (cookie) => {
        return cookie.trim().substr(0, CSRF_KEY_NAME.length) == CSRF_KEY_NAME;
    })
    if (csrf) xhr.setRequestHeader("X-CSRFToken", csrf.trim().substr(CSRF_KEY_NAME.length));
    // ------------------------------------------------
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = () => {
        if (xhr.status === 200) {
            getGoodNumButton(article_id, user_id)
        }
    };
    body = {
        user_id: user_id,
        article_id: article_id,
    }
    var jsonText = JSON.stringify(body);
    xhr.send(jsonText);
}
