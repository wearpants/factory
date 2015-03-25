Factory is an object-oriented approach to partial function application, also known as currying. The Factory module is a more powerful implementation of this pattern. Some improvements include:

  * safer, as invalid arguments are detected immediately, instead of at call time
  * intelligent support for classes, instance methods & all other callables
  * bound arguments can be inspected and modified as attributes
  * several convenient methods for (re)binding arguments
  * no "Russian dolls" of nested lambdas

Using Factories can:

  * simplify writing callbacks
  * reduce bugs in concurrent applications
  * provide easy lazy evaluation

For downloads and more information, please see the [Cheeseshop](http://pypi.python.org/pypi/Factory/)
