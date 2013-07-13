(function () {
    var converter = Markdown.getSanitizingConverter(),
        elements = document.querySelectorAll('[data-widget="PagedownWidget"]');

    for (var i = 0; i < elements.length, el = elements[i]; ++i)
    {
        selectors = {
            input : el.id,
            button : el.id + "_wmd_button_bar",
            preview : el.id + "_wmd_preview",
        }

        var editor = new Markdown.Editor(converter, "", selectors);

        editor.run();
    }
})();
