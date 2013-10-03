package in.fount;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.webapp.WebAppContext;

public class Main {

    public static Server setupServer(Server server, String dir) {
        WebAppContext root = new WebAppContext();
        root.setContextPath("/");
        root.setResourceBase(dir);
        root.setDescriptor(dir + "/WEB-INF/web.xml");
        root.setParentLoaderPriority(true);
        server.setHandler(root);
        return server;
    }

    public static void main(String[] args) throws Exception {

        Server fountin = setupServer(new Server(8080), "src/main/webapp/");
        fountin.start();
        fountin.join();
    }

}
