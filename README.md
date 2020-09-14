#TODO
* setup.py, cythonize
* tests + worker tests
* class annotations with examples
* python f-expressions are evaluated??
* проверить утечки памяти (memory view release)
* проверить rpc и worker.error
* README


## RoadRunner usage

worker class


## Run tests

```bash
docker-compose -f ./goridge/tests/docker-compose.yml up
python3 -m unittest discover -s tests
```