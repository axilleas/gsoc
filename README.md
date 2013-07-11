These are some dummy scripts to find which gems that [GitLab][gitlab] is using, are missing from Fedora repositories.

On a Fedora machine, clone the repository, cd into it and run:

```  
sudo yum install python2 python-bugzilla python-pkgwat.api
chmod +x run.sh
./run.sh
```

Note that it could take some time because it queries both Fedora's repos and rubygems.org.

[gitlab]: https://github.com/gitlabhq/gitlabhq
