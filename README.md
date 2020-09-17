#TODO
* setup.py, cythonize
* class annotations with examples
* README


## RoadRunner usage

worker class
use your own json encoder/decoder


## Run tests

```bash
docker-compose -f ./goridge/tests/docker-compose.yml up
docker-compose -f tests/rr_test_app/docker-compose.yml up --build
python3 -m unittest discover -s tests
```