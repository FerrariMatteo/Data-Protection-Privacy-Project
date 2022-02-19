# Data protection & privacy project

Implementation of the [GRAM](https://www.sciencedirect.com/science/article/abs/pii/S0957417420302785) algorithm for (*k*, *l*) graph anonymization.

## Testing
To run tests use the `python -m unittest -v` command from the root directory.
Graphs used for testing:
* [jazz musicians](http://konect.cc/networks/arenas-jazz/) (*n*=198, *m*=2742)
* [Zachary karate club](http://konect.cc/networks/ucidata-zachary/) (*n*=34, *m*=78)
* [U. Rovira i Virgili](http://konect.cc/networks/arenas-email/) (*n*=1133, *m*=5451)
* [US power grid](http://konect.cc/networks/opsahl-powergrid/) (*n*=4941, *m*=6594)
