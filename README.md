# zdropy

A bot for booking classes in sports clubs that support the 
[perfectgym](https://www.perfectgym.com/en) system using Selenium and Python.
Tested and pre-configured for Zdrofit (hence the name), but other clubs should
work just fine, including the famous Gold's Gym.

<!-- TOC -->
* [How it works](#how-it-works)
* [How to run](#how-to-run)
* [How to run tests](#how-to-run-tests)
* [Examples](#examples)
* [IMPORTANT SECURITY NOTE](#important-security-note)
* [TODO](#todo)
<!-- TOC -->

## How it works

Most of the sports clubs let you book a class no sooner than 48 hours before
the class starts. It's easy to miss it if you're busy and the class is popular,
and here comes zdropy – run the program in the background, and it will book the
class automatically! Selenium goes through the motions of your web browser as if
it was you, but faster. By default, the class will be checked first to make sure 
that it's available and there were no typos in the class info.
[See a demo on YouTube](https://youtu.be/nSgE0pPtX0A)


## How to run

1. Create a `.env` file in the project directory and input your login info:
``` 
# zdropy/.env
LOGIN=your.login.probably@an.email.address
PASSWORD=your_password
```
2. Make sure Python3 and Chrome (pre-configured by default) or Firefox is installed.
3. Install additional requirements from `requirements.txt`
4. Take a look at the `config.py` file and if needed, edit it to your preference.
Most notably, you specify whether to join the wait list if booking fails, 
or if the program should retry the booking process on a failed attempt
(i.e. due to server overload on perfectgym)   
5. Run the program with `python3 project.py {arguments}`,
specifying the required positional arguments:
```
name                  name of the class (case-sensitive)
time                  time of the class, formatted as %H:%M
date                  date of the class, formatted as %Y-%m-%d
```
You can additionally specify the club location with `-c`/`--club`
(the club you booked in previously should be preselected) or skip
class checking with `-s`/`--skip-check`.

## How to run tests

Make sure `.env` file is present and filled.
Copy the contents of `testdata_template.py` to `zdropy/testdata.py`.
Fill with your class info and run the tests.

## Examples

```
$ python3 project.py Stretching  09:30 2023-02-15
$ python3 project.py Tabata 18:15 2023-03-16 --club "Zdrofit Arkadia"
$ python3 porject.py "Trening Cross" 16:30 2023-04-13 --skip-check
```

## IMPORTANT SECURITY NOTE

I am by no means a security expert and I take no responsibility for your privacy.
Storing credentials in `.env` is relatively safe, albeit [not foolproof](https://stackoverflow.com/questions/60360298/is-it-secure-way-to-store-private-values-in-env-file).
You should probably make sure that the password you're using for the sports club
is not reused in other important services, i.e. your email address.

## TODO

* Scheduling weekly class booking (!)
* Optimization for headless mode
* Support for cron expressions
* Cancelling classes (mostly for tests)
* Support for auto execution on Linux, maybe Mac