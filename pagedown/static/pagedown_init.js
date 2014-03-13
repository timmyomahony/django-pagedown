function bindPagedown(){
    var $ = django.jQuery;
    var converter = Markdown.getSanitizingConverter(),
        elements = document.getElementsByTagName("textarea");

    for (var i = 0; i < elements.length; ++i){
        var el = elements[i];
        var $el = $(el);
        var isTemplate = !$el.is(":visible");
        var hasRun = $el.data('pagedowned');
        if(isTemplate || hasRun)continue;
        $el.data('pagedowned', true);
        if ( (' ' + el.className + ' ').indexOf(' wmd-input ') > -1 ) {
            selectors = {
                input : el.id,
                button : el.id + "_wmd_button_bar",
                preview : el.id + "_wmd_preview",
            };
            var editor = new Markdown.Editor(converter, "", selectors);
            editor.run();
        }
    }
}


function initPagedown() {
    var $ = django.jQuery;
    $('.add-row, .grp-add-handler').bind('click', bindPagedown);
    bindPagedown();

}
window.onload = initPagedown;
