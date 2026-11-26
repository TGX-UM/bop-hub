source "https://rubygems.org"

# Jekyll 4 directly, NOT the `github-pages` gem.
#
# `github-pages` exists to mirror the gem versions GitHub's own legacy,
# branch-based Pages builder runs. This site builds in its own Actions
# workflow (Settings -> Pages -> Source = GitHub Actions), so those pins buy
# nothing -- and they actively break: github-pages 222 pins liquid 4.0.3,
# whose taint_check calls Object#tainted?, removed in Ruby 3.2. The upstream
# Jiffy template only survived that by depending on liquid-c, a C extension
# that happens to bypass the call. Jekyll 4 fixed it properly.
gem "jekyll", "~> 4.4"

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
