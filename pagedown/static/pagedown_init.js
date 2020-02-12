var DjangoPagedown = DjangoPagedown | {};

DjangoPagedown = (function() {
  var converter = Markdown.getSanitizingConverter();
  var editors = {};
  var elements;

  Markdown.Extra.init(converter, {
    extensions: "all"
  });

  var setupEditor = function(element) {
    var input = element.getElementsByClassName("wmd-input")[0];
    var id = input.id.substr(9);
    if (!editors.hasOwnProperty(id)) {
      var editor = new Markdown.Editor(converter, id, {});

      // Handle image upload
      if (element.classList.contains("image-upload-enabled")) {
        var upload = element.getElementsByClassName("pagedown-image-upload")[0];
        var url = upload.getElementsByClassName("url-input")[0];
        var file = upload.getElementsByClassName("file-input")[0];
        var cancel = upload.getElementsByClassName("deletelink")[0];
        var submit = upload.getElementsByClassName("submit-input")[0];

        var close = function(value, callback) {
          upload.classList.remove("show");
          url.value = "";
          file.value = "";
          callback(value);
        };

        editor.hooks.set("insertImageDialog", function(callback) {
          upload.classList.add("show");

          cancel.addEventListener(
            "click",
            function(event) {
              close(null, callback);
              event.preventDefault();
            },
            { once: true }
          );

          submit.addEventListener(
            "click",
            function() {
              // Regular URL
              if (url.value.length > 0) {
                close(url.value, callback);
              }
              // File upload
              else if (file.files.length > 0) {
                var data = new FormData();
                var request = new XMLHttpRequest();
                data.append("file", file.files[0]);
                request.open("POST", "/pagedown/image-upload/", true);
                request.addEventListener(
                  "load",
                  function() {
                    var response = JSON.parse(request.response);
                    if (response.success) {
                      close(response.url, callback);
                    } else {
                      if (response.error) {
                        alert(response.error);
                      }
                      close(null, callback);
                    }
                  },
                  {
                    once: true
                  }
                );
                request.send(data);
              } else {
                // Nothing
                close(null, callback);
              }
              event.preventDefault();
            },
            { once: true }
          );

          return true;
        });
      }

      editor.run();
      editors[id] = editor;
    }
  };

  var init = function() {
    elements = document.getElementsByClassName("wmd-wrapper");
    for (var i = 0; i < elements.length; ++i) {
      setupEditor(elements[i]);
    }
  };

  return {
    init: function() {
      return init();
    }
  };
})();

window.onload = DjangoPagedown.init;
