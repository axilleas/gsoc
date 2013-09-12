## stringex

Problem: Fedora(2.0.8), gitlab-gollum-lib needs ~>1.5.1
Solution: Update to latest gollum-lib 1.0.6, send patch to GitLab

## gitlab-gollum-lib

Problem: Current version 1.0.1 has stringex ~> 1.5.1 and pygments.rb ~> 0.4.3. Need to change to 2.0.3 and 0.5.2 respectively.
Solution: patch gemspec (ideal update gollum-lib to 1.0.6)

## tinder
Problem: Current version has dependencies that need updating, see https://github.com/collectiveidea/tinder/issues/61
Solution: New release on rubygems.org, or temporarily disable this gem as it's not crucial for running GitLab.

## grape

Problem: GitLab uses 0.4.1, latest upstream 0.5.0. I used 0.5.0, let's see if it breaks something.
Solution: Will have to check api calls with updated grape
  
## gemoji

Problem0: with latest 1.4.0 requiring 'emoji/railtie' is deprecated.
Solution: downgrade to 1.2.1

Problem1: License is a hell. See http://words.steveklabnik.com/emoji-licensing
Solution: Use https://github.com/Genshin/PhantomOpenEmoji instead?

## rack-mount

Problem: /usr/share/gems/gems/backports-3.3.3/lib/backports/tools.rb:328:in 'require': cannot load such file -- regin (LoadError)

```
grape -> virtus -> backports
grape -> rack-mount -> regin bundled
```

Solution: Move vendor/ in /usr/share/gems/gems/rack-mount-0.8.3/lib/rack/mount/

## github-linguist
Problem: github-linguist-2.9.4/lib/linguist/language.rb:229:in 'initialize': Ceylon is missing lexer (ArgumentError)
Solution: Revert to 2.3.4 for now.

github-liguist -> escape_utils ~> 2.3.4 
