package in.fount;

import static junit.framework.Assert.assertEquals;
import static junit.framework.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mortbay.jetty.servlet.DefaultServlet;
import org.mortbay.jetty.testing.HttpTester;
import org.mortbay.jetty.testing.ServletTester;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

//@RunWith(SpringJUnit4ClassRunner.class)
//@ContextConfiguration(locations = { "classpath*:spring/application-context.xml" })
public class ServerTest {

    private ServletTester tester;
    private HttpTester request;
    private HttpTester response;

    @Before
    public void setUp() throws Exception {
        this.tester = new ServletTester();
        this.tester.setContextPath("/");
        tester.addServlet(DefaultServlet.class, "/");
        this.tester.start();

        this.request = new HttpTester();
        this.response = new HttpTester();
        this.request.setMethod("GET");
        this.request.setHeader("Host", "tester");
        this.request.setVersion("HTTP/1.0");
    }

//    @Test
    public void testHomepage() throws Exception {
        this.request.setURI("/");
        this.response.parse(tester.getResponses(request.generate()));
        assertTrue(this.response.getMethod() == null);
        assertEquals(200, this.response.getStatus());
        assertEquals("Hello World", this.response.getContent());
    }

}