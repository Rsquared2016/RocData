package in.fount.util;

import org.codehaus.jackson.map.DeserializationConfig;
import org.codehaus.jackson.map.ObjectMapper;
import org.ektorp.CouchDbConnector;
import org.ektorp.impl.ObjectMapperFactory;
import org.ektorp.impl.StdObjectMapperFactory;

/**
 * Wrapper around {@link StdObjectMapperFactory} adding custom configuration
 * capabilities. Subclasses may overwrite {@link #configureMapper(ObjectMapper)}
 * .
 */
public class StdObjectMapperFactoryWrapper implements ObjectMapperFactory {

    private ObjectMapperFactory factory;

    private boolean failOnUnknownProperties;

    @Override
    public ObjectMapper createObjectMapper() {
        ObjectMapper mapper = factory.createObjectMapper();

        configureMapper(mapper);

        return mapper;
    }

    @Override
    public ObjectMapper createObjectMapper(CouchDbConnector connector) {
        ObjectMapper mapper = factory.createObjectMapper(connector);

        configureMapper(mapper);

        return mapper;
    }

    /**
     * Custom configuration of <code>mapper</code> argument. Subclasses may
     * overwrite.
     * 
     * @param mapper
     */
    protected void configureMapper(ObjectMapper mapper) {
        mapper.configure(
                DeserializationConfig.Feature.FAIL_ON_UNKNOWN_PROPERTIES,
                failOnUnknownProperties);
    }

    public void setFactory(ObjectMapperFactory factory) {
        this.factory = factory;
    }

    public void setFailOnUnknownProperties(boolean failOnUnknownProperties) {
        this.failOnUnknownProperties = failOnUnknownProperties;
    }

}
