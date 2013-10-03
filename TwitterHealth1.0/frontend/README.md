# Run

Deploy the server on your machine by navigating to the frontend directory and running:

## Production environment:

    $ ./prod_run_webapp.sh
    
## Development environment:

    $ ./dev_run_webapp.sh

# Testing

Testing frameworks are currently in place for the Java and Javascript portions of our frontend. All tests live in the
subdirectories of frontend/src/test.

## Java

(No information yet... :( )

## Javascript

Javascript unit tests and integration tests live in the js/unit and js/spec directories, respectively. 

To perform tests manually, navigate to frontend/src, then:

    $ java -jar test/tools/jsTestDriver/JsTestDriver-1.3.4.b.jar --port 4223 &

This will run an instance of the JsTestDriver server. (You can set the port to whatever your heart desires, just make
sure you update the server value in the JsTestDriver.conf file accordingly)

Next, in the browser you're testing, navigate to the capture page of the machine the server is running on. On your local
machine, this will simply be http://localhost:4223/capture. On our development server, it's
http://dev.fount.in:4223/capture.

Finally, to actually run all tests, do:

    $ java -jar test/tools/jsTestDriver/JsTestDriver-1.3.4.b.jar --tests all --reset

### Adding Testable Units

In frontend/src/JsTestDriver.conf, under load, specify the locations of any modules you wish to pull into the test space
on server load. You can see some existing examples in  the file already. Happily, JsTestDriver supports globbing.

### Adding Tests

All tests in js/unit and js/spec are automatically loaded into the test suite. Our JS test framework of choice is Jasmine
which you can read more about here: http://pivotal.github.com/jasmine/
