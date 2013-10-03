package in.fount.util;

/**
 * Provides information about current application environment, which can be
 * either development or production. Its value is set during spring application
 * context initialization via {@link EnvironmentAwareContextInitializer} and
 * can't be changed later. The value itself comes from build (e.g.
 * <code>-Denvironment=production</code>). Useful methods are:
 * <ul>
 * <li>{@link #isDevelopment()}</li>
 * <li>{@link #isProduction()}</li>
 * </ul>
 * <b>This class is designed to change <i>code flow</i>. If you want to change
 * static values used by the application, in other words change the
 * <i>configuration</i>, add properties into production/development
 * configuration files and use property placeholders in
 * <code>applicationContext.xml</code>.</b>
 */
public class Environment {

    private static EnvironmentType value;

    private Environment() {
    }

    public static boolean isDevelopment() {
        if (value == null)
            throw new IllegalStateException("environment has not been set yet");
        return value == EnvironmentType.DEVELOPMENT;
    }

    public static boolean isProduction() {
        if (value == null)
            throw new IllegalStateException("environment has not been set yet");
        return value == EnvironmentType.PRODUCTION;
    }

    public static void setValue(String value) {
        if (value == null)
            throw new IllegalArgumentException("value must not be null");

        if (Environment.value != null)
            throw new RuntimeException("environment has been already set");

        Environment.value = EnvironmentType.valueOf(value.toUpperCase());
    }

    private enum EnvironmentType {
        DEVELOPMENT, PRODUCTION
    }

}
