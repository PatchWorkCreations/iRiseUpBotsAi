import css_html_js_minify

# Minify style.css
with open('/Users/Julia/Downloads/braine-package/myapp/static/myapp/css/style.css', 'r') as css_file:
    css_content = css_file.read()

minified_css = css_html_js_minify.css_minify(css_content)

with open('/Users/Julia/Downloads/braine-package/myapp/static/myapp/css/style.min.css', 'w') as minified_file:
    minified_file.write(minified_css)

# Minify bootstrap.css
with open('/Users/Julia/Downloads/braine-package/myapp/static/myapp/css/bootstrap.css', 'r') as css_file:
    css_content = css_file.read()

minified_bootstrap_css = css_html_js_minify.css_minify(css_content)

with open('/Users/Julia/Downloads/braine-package/myapp/static/myapp/css/bootstrap.min.css', 'w') as minified_file:
    minified_file.write(minified_bootstrap_css)

with open('/Users/Julia/Downloads/braine-package/myapp/static/myapp/css/global.css', 'r') as css_file:
    css_content = css_file.read()

minified_bootstrap_css = css_html_js_minify.css_minify(css_content)

with open('/Users/Julia/Downloads/braine-package/myapp/static/myapp/css/global.min.css', 'w') as minified_file:
    minified_file.write(minified_bootstrap_css)
print("CSS files have been minified!")

#python minify_css.py

