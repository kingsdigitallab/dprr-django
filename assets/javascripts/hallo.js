(function() {
    (function($) {
        return $.widget('IKS.blockQuoteButton', {
            options: {
                uuid: '',
                editable: null
            },
            populateToolbar: function(toolbar) {
                var button, widget;

                widget = this;

                button = $('<span></span>');
                button.hallobutton({
                    uuid: this.options.uuid,
                    editable: this.options.editable,
                    label: 'Blockquote',
                    icon: 'fa fa-quote-left',
                    command: null
                });

                toolbar.append(button);

                button.on('click', function(event) {
                    return widget.options.editable.execute('formatBlock',
                                                           'blockquote');
                });
            }
        });
    })(jQuery);
}).call(this);

/*
    raw html edit button based on the original code by https://github.com/ejucovy
    https://gist.github.com/ejucovy/5c5370dc73b80b8896c8
*/

(function() {
    (function($) {
        return $.widget('IKS.editHtmlButton', {
            options: {
                uuid: '',
                editable: null
            },
            populateToolbar: function(toolbar) {
                var button, widget;

                var getEnclosing = function(tag) {
                    var node;

                    node = widget.options.editable.getSelection().commonAncestorContainer;
                    return $(node).parents(tag).get(0);
                };

                widget = this;

                button = $('<span></span>');
                button.hallobutton({
                    uuid: this.options.uuid,
                    editable: this.options.editable,
                    label: 'Edit HTML',
                    icon: 'fa fa-file-code-o',
                    command: null
                });

                toolbar.append(button);

                button.on('click', function(event) {
                    $('body > .modal').remove();
                    var container = $('<div class="modal fade editor" tabindex="-1" role="dialog" aria-hidden="true">\n    <div class="modal-dialog">\n        <div class="modal-content"\
>\n            <button type="button" class="close text-replace" data-dismiss="modal" aria-hidden="true"><i class="fa fa-times fa-lg"></i></button>\n            <div class="modal-body"><hea\
der class="nice-padding hasform"><div class="row"><div class="left"><div class="col"><h1><i class="fa fa-file-code-o"></i>&nbsp;Edit HTML Code</h1></div></header><div class="modal-bo\
dy-body"></div></div>\n        </div><!-- /.modal-content -->\n    </div><!-- /.modal-dialog -->\n</div>');

                    // add container to body and hide it, so content can be added to it before display
                    $('body').append(container);
                    container.modal('hide');
                    var modalBody = container.find('.modal-body-body');
                    modalBody.html('<textarea style="height: 400px; width: 92%; font: 14px/21px monospace; border: 1px solid #d8d8d8; background: #f4f4f4; margin: 2% 4%;" id="wagtail-edit-html-content">'+widget.options.editable.element.html()+'</textarea><button i\
d="wagtail-edit-html-save" type="button" style="margin: 0 4%; float: right;">Save</button>');
                    $("#wagtail-edit-html-save").on("click", function() {
                        widget.options.editable.setContents($("#wagtail-edit-html-content").val());
                        widget.options.editable.setModified();
                        container.modal('hide');
                    });
                    container.modal('show');
                });
            }
        });
    })(jQuery);
}).call(this);