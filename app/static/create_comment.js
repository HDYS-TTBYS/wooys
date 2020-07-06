const deleteUpdate = (pk) => {
    document.getElementById('delete-update').addEventListener("click", () => {
        const title_key = "comment_id_title"
        sessionStorage.removeItem(title_key)

        const content_key = "comment_id_content"
        sessionStorage.removeItem(content_key)
    });
}

const sessionTitle = () => {
    document.getElementById("id_title").addEventListener("change", () => {
        sessionStorage.setItem('comment_id_title', document.create_comment_form.title.value);
    })
};

const setTitle = () => {
    if (sessionStorage.getItem('comment_id_title')) {
        document.create_comment_form.title.value = sessionStorage.getItem('comment_id_title')
    }
};


const setSearchTag = () => {
    if (sessionStorage.getItem('create_id_search_tag')) {
        document.create_comment_form.search_tag.value = sessionStorage.getItem('create_id_search_tag')
    }
};
