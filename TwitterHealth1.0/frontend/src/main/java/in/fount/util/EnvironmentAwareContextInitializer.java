package in.fount.util;

import java.io.IOException;
import java.util.Properties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.ApplicationContextInitializer;
import org.springframework.core.env.MutablePropertySources;
import org.springframework.core.env.PropertiesPropertySource;
import org.springframework.core.env.PropertySource;
import org.springframework.core.io.support.ResourcePropertySource;
import org.springframework.web.context.ConfigurableWebApplicationContext;

/**
 * Initializes {@link PropertySource}s needed for spring placeholder resolution.
 * Based on the <code>environment</code> property supplied from build into
 * <code>twitterhealth.properties</code>, it registers either development (
 * <code>twitterhealth.development.properties</code>) or production (
 * <code>twitterhealth.production.properties</code>) property source.
 * <p>
 * {@link Environment} get initialized here.
 * 
 * @see Environment
 */
public class EnvironmentAwareContextInitializer implements
        ApplicationContextInitializer<ConfigurableWebApplicationContext> {

    private static Logger log = LoggerFactory
            .getLogger(EnvironmentAwareContextInitializer.class);

    @Override
    public void initialize(ConfigurableWebApplicationContext ctx) {
        try {
            // twitterhealth.properties
            Properties properties = new Properties();
            properties.load(getClass().getResourceAsStream(
                    "/fountin.properties"));
            String environment = properties.getProperty("environment");

            PropertiesPropertySource basicPropertySource = new PropertiesPropertySource(
                    "fountin.properties.propertySource", properties);

            log.info("Current environment is {}", environment);

            // initialize the environment
            Environment.setValue(environment);

            // twitterhealth.<environment>.properties
            ResourcePropertySource environmentPropertySource = resolveEnvironmentPropertySource(environment);

            // register property sources in current environment
            MutablePropertySources sources = ctx.getEnvironment()
                    .getPropertySources();
            sources.addFirst(basicPropertySource);
            sources.addFirst(environmentPropertySource);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private ResourcePropertySource resolveEnvironmentPropertySource(
            String environment) {
        try {
            String resourceName = "classpath:/fountin." + environment
                    + ".properties";

            log.info("using properties from {}", resourceName);

            return new ResourcePropertySource(
                    "fountin.environment.properties.propertySource",
                    resourceName, getClass().getClassLoader());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
