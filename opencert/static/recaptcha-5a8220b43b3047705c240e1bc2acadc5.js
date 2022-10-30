function onSubmit(token) {
    var formID = $(this).closest("form").attr("id");
    document.getElementById(formID).submit();
}