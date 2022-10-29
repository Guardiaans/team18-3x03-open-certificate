function onSubmit(token) {
    let btn = document.getElementById("btn");
    let id = btn.form.id;
    document.getElementById(id).submit();
}