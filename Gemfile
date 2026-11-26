source "https://rubygems.org"

# GitHub Pages pins Jekyll and its dependencies. Keep the local setup aligned
# with whatever GitHub runs: https://pages.github.com/versions/
#   bundle update github-pages
gem "github-pages", group: :jekyll_plugins

# The default Jekyll theme, inherited from the Jiffy template.
gem "minima", "~> 2.5"

group :jekyll_plugins do
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
  gem "jekyll-redirect-from"
  gem "jekyll-include-cache"
end

# Webrick is no longer bundled with Ruby >= 3.0
# https://github.com/jekyll/jekyll/issues/8523
gem "webrick"

# Windows and JRuby do not ship zoneinfo files.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
