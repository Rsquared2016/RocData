package in.fount.util;

import javax.servlet.http.HttpServletRequest;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ServletUtil {

    private static Logger log = LoggerFactory.getLogger(ServletUtil.class);

    /**
     * @param request
     * @return base URL from a {@link HttpServletRequest} in the following form:
     *         <code>scheme://serverName:serverPort</code>
     */
    public static String getBaseUrlFromRequest(HttpServletRequest request) {
        String baseUrl = String.format("%s://%s:%d", request.getScheme(),
                request.getServerName(), request.getServerPort());

        log.debug(
                "base URL constructed from request: {}, original request({})",
                baseUrl, request.getRequestURL());

        return baseUrl;
    }

}
