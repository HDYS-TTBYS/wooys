const deleteUpdate = (pk) => {
    document.getElementById('delete-update').addEventListener("click", () => {
        const title_key = "update_id_title_" + pk
        sessionStorage.removeItem(title_key)

        const search_key = "update_id_search_tag_" + pk
        sessionStorage.removeItem(search_key)

        const content_key = "update_id_content_" + pk
        sessionStorage.removeItem(content_key)
    });
}

const sessionTitle = (pk) => {
    document.getElementById("id_title").addEventListener("change", () => {
        sessionStorage.setItem('update_id_title_' + pk, document.update_form.title.value);
    })
};

const setTitle = (pk) => {
    if (sessionStorage.getItem('update_id_title_' + pk)) {
        document.update_form.title.value = sessionStorage.getItem('update_id_title_' + pk)
    }
};

const sessionSearchTag = (pk) => {
    document.getElementById("id_search_tag").addEventListener("change", () => {
        sessionStorage.setItem('update_id_search_tag_' + pk, document.update_form.search_tag.value);
    })
};

const setSearchTag = (pk) => {
    if (sessionStorage.getItem('update_id_search_tag_' + pk)) {
        document.update_form.search_tag.value = sessionStorage.getItem('update_id_search_tag_' + pk)
    }
};
