package in.fount.util;

import org.ektorp.CouchDbInstance;
import org.ektorp.impl.ObjectMapperFactory;
import org.ektorp.impl.StdCouchDbConnector;
import org.springframework.beans.factory.FactoryBean;

public class StdCouchdbFactoryBean implements FactoryBean<StdCouchDbConnector> {

    private String databaseName;

    private CouchDbInstance couchDbInstance;

    private ObjectMapperFactory objectMapperFactory;

    @Override
    public StdCouchDbConnector getObject() throws Exception {
        return new StdCouchDbConnector(databaseName, couchDbInstance,
                objectMapperFactory);
    }

    @Override
    public Class<?> getObjectType() {
        return StdCouchDbConnector.class;
    }

    @Override
    public boolean isSingleton() {
        return true;
    }

    public void setDatabaseName(String databaseName) {
        this.databaseName = databaseName;
    }

    public void setCouchDbInstance(CouchDbInstance couchDbInstance) {
        this.couchDbInstance = couchDbInstance;
    }

    public void setObjectMapperFactory(ObjectMapperFactory objectMapperFactory) {
        this.objectMapperFactory = objectMapperFactory;
    }

}
