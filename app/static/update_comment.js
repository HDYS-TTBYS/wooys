const deleteUpdate = (pk) => {
    document.getElementById('delete-update').addEventListener("click", () => {
        const title_key = "update_comment_id_title_" + pk
        sessionStorage.removeItem(title_key)

        const content_key = "update_comment_id_content_" + pk
        sessionStorage.removeItem(content_key)
    });
}

const sessionTitle = (pk) => {
    document.getElementById("id_title").addEventListener("change", () => {
        sessionStorage.setItem('update_comment_id_title_' + pk, document.update_comment_form.title.value);
    })
};

const setTitle = (pk) => {
    if (sessionStorage.getItem('update_comment_id_title_' + pk)) {
        document.update_comment_form.title.value = sessionStorage.getItem('update_comment_id_title_' + pk)
    }
};
