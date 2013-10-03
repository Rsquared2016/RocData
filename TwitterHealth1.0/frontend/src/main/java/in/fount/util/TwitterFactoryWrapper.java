package in.fount.util;

import org.springframework.beans.factory.FactoryBean;

import twitter4j.TwitterFactory;
import twitter4j.conf.ConfigurationBuilder;

/**
 * {@link FactoryBean} implementation that creates {@link TwitterFactory}
 * instance using {@link ConfigurationBuilder} .
 */
public class TwitterFactoryWrapper implements FactoryBean<TwitterFactory> {

    protected String oAuthConsumerKey;

    protected String oAuthConsumerSecret;

    @Override
    public TwitterFactory getObject() throws Exception {
        ConfigurationBuilder cb = createConfigurationBuilder();
        return new TwitterFactory(cb.build());
    }

    @Override
    public Class<?> getObjectType() {
        return TwitterFactory.class;
    }

    @Override
    public boolean isSingleton() {
        return true;
    }

    protected ConfigurationBuilder createConfigurationBuilder() {
        ConfigurationBuilder cb = new ConfigurationBuilder();

        cb.setOAuthConsumerKey(oAuthConsumerKey);
        cb.setOAuthConsumerSecret(oAuthConsumerSecret);

        return cb;
    }

    // getters & setters

    public void setoAuthConsumerKey(String oAuthConsumerKey) {
        this.oAuthConsumerKey = oAuthConsumerKey;
    }

    public void setoAuthConsumerSecret(String oAuthConsumerSecret) {
        this.oAuthConsumerSecret = oAuthConsumerSecret;
    }

}
