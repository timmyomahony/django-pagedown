(function ($) {
    $(document).ready(function(){
        /* Admin inline support */
        $('.add-row, .grp-add-handler').click(function(){
            $(".inline-related fieldset .form-row textarea.wmd-input").each(function(idx, el){
                DjangoPagedown.createEditor(el);
            });
        });
    });
})(django.jQuery);