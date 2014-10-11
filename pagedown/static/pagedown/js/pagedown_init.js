var DjangoPagedown = DjangoPagedown | {};


DjangoPagedown = (function() {

    var converter,
        editors,
        elements;

    var that = this;

    var isPagedownable = function(el) {
        if ( (' ' + el.className + ' ').indexOf(' wmd-input ') > -1 ) {
            return true;
        }
        return false;
    };

    var createEditor = function(el) {
        if ( isPagedownable(el) ) {
            if ( ! that.editors.hasOwnProperty(el.id) ) {
                var selectors = {
                    input : el.id,
                    button : el.id + "_wmd_button_bar",
                    preview : el.id + "_wmd_preview",
                };
                that.editors[el.id] = new Markdown.Editor(that.converter, "", selectors);

                var editor =  that.editors[el.id];

                var $dialog = $('#insertImageDialog').dialog({
                    autoOpen: false,
                    closeOnEscape: false,
                    open: function(event, ui) { $(".ui-dialog-titlebar-close").hide(); }
                });

                var $loader = $('span.loading-small', $dialog);
                var $url = $('input[type=text]', $dialog);
                var $file = $('input[type=file]', $dialog);

                editor.hooks.set('insertImageDialog', function(callback) {
                // dialog functions
                    var dialogInsertClick = function() {
                        callback($url.val().length > 0 ? $url.val() : null);
                        dialogClose();
                    };

                    var dialogCancelClick = function() {
                        dialogClose();
                        callback(null);
                    };

                    var dialogClose = function() {
                        // clean up inputs
                        $url.val('');
                        $file.val('');
                        $dialog.dialog('close');
                    };

                    // set up dialog button handlers
                    $dialog.dialog( 'option', 'buttons', {
                        'Insert': dialogInsertClick,
                        'Cancel': dialogCancelClick
                    });

                    var uploadStart = function() {
                        $loader.show();
                    };

                    var uploadComplete = function(response) {
                        $loader.hide();
                        var response_str = $(response).text(); //Hack to remove pretag embedded by ajaxuploader
                        response_obj = JSON.parse(response_str);
                        if (response_obj.success) {
                            callback(response_obj.image_path);
                            dialogClose();
                        } else {
                            alert(response_obj.message);
                            $file.val('');
                        }
                    };

                    // upload
                    $file.unbind('change').ajaxfileupload({
                        action: $file.attr('data-action'),
                        onStart: uploadStart,
                        onComplete: uploadComplete
                    });

                    // open the dialog
                    $dialog.dialog('open');

                    return true; // tell the editor that we'll take care of getting the image url
                });


                that.editors[el.id].run();
                return true;
            } else {
                console.log("Pagedown editor already attached to element: <#" + el.id + ">");
            }
        }
        return false;
    };

    var destroyEditor = function(el) {
        if ( that.editors.hasOwnProperty(el.id)) {
            delete that.editors[el.id];
            return true;
        }
        return false;
    };

    var init = function() {
        that.converter = Markdown.getSanitizingConverter();
        that.elements = document.getElementsByTagName("textarea");
        that.editors = {};
        for (var i = 0; i < that.elements.length; ++i){
            if ( isPagedownable(that.elements[i]) ) {
                createEditor(that.elements[i]);
            }
        }
    };

    return {
        init: function() {
            return init();
        },
        createEditor: function(el) {
            return createEditor(el);
        },
        destroyEditor: function(el) {
            return destroyEditor(el);
        },
    };
})();

window.onload = DjangoPagedown.init;
