# Code generator
A python template engine for generating code for programming language. The program is packed with template for : c++ class, c++ template (todo) and rust struct (todo).

It use the [Cheetah template engine](http://www.cheetahtemplate.org/index.html).

If there is a folder inc, the header will be inserted in this folder.
If there is a folder src, the source will be inserted in this folder.

## Installing on Mac OSX
First you have to download cheetah :
https://pypi.python.org/pypi/Cheetah/2.4.4

To install cheetah without the root rights, de-tar it, go inside the folder and run the following command :
```
python setup.py install --user
```

## Execution
Just use the python command on main.py. If your program is in the ~/progs folder, adding the following alias to your [.zshrc, bashrc] will do it :
```
alias class="python ~/progs/cpp_class_generator/main.py"
```

## Customisation
The templates are header.tmpl and implementation.tmpl. Change them as you want !

By modifying the init.py file, you can :
* change the extension of the file
* the target directory of the created files
* the header guard extension
* the default type
