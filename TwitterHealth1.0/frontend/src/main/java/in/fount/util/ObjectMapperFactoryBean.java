package in.fount.util;

import org.codehaus.jackson.map.DeserializationConfig;
import org.codehaus.jackson.map.ObjectMapper;
import org.springframework.beans.factory.FactoryBean;

/**
 * {@link FactoryBean} that creates configured instances of {@link ObjectMapper}
 * .
 */
public class ObjectMapperFactoryBean implements FactoryBean<ObjectMapper> {

    private boolean failOnUnknownProperties;

    @Override
    public ObjectMapper getObject() throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();

        configureMapper(objectMapper);

        return objectMapper;
    }

    @Override
    public Class<?> getObjectType() {
        return ObjectMapper.class;
    }

    @Override
    public boolean isSingleton() {
        return false;
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

    public void setFailOnUnknownProperties(boolean failOnUnknownProperties) {
        this.failOnUnknownProperties = failOnUnknownProperties;
    }

}
