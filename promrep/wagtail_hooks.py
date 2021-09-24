from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.core import hooks
from wagtail.core.whitelist import allow_without_attributes


def whitelister_element_rules():
    return {
        "blockquote": allow_without_attributes,
    }


hooks.register("construct_whitelister_element_rules", whitelister_element_rules)


def editor_css():
    return format_html(
        """
                       <link href="{0}{1}" rel="stylesheet"
                       type="text/x-scss" />
                       """,
        settings.STATIC_URL,
        "vendor/font-awesome/scss/font-awesome.scss",
    )


hooks.register("insert_editor_css", editor_css)


def editor_js():
    js_files = [
        "javascripts/hallo.js",
    ]

    js_includes = format_html_join(
        "\n",
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files),
    )

    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('blockQuoteButton');
            registerHalloPlugin('editHtmlButton');
        </script>
        """
    )


hooks.register("insert_editor_js", editor_js)
