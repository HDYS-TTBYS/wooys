const deleteUpdate = (pk) => {
    document.getElementById('delete-update').addEventListener("click", () => {
        const title_key = "create_id_title"
        sessionStorage.removeItem(title_key)

        const search_key = "create_id_search_tag"
        sessionStorage.removeItem(search_key)

        const content_key = "create_id_content"
        sessionStorage.removeItem(content_key)
    });
}

const sessionTitle = () => {
    document.getElementById("id_title").addEventListener("change", () => {
        sessionStorage.setItem('create_id_title', document.create_form.title.value);
    })
};

const setTitle = () => {
    if (sessionStorage.getItem('create_id_title')) {
        document.create_form.title.value = sessionStorage.getItem('create_id_title')
    }
};

const sessionSearchTag = () => {
    document.getElementById("id_search_tag").addEventListener("change", () => {
        sessionStorage.setItem('create_id_search_tag', document.create_form.search_tag.value);
    })
};

const setSearchTag = () => {
    if (sessionStorage.getItem('create_id_search_tag')) {
        document.create_form.search_tag.value = sessionStorage.getItem('create_id_search_tag')
    }
};
