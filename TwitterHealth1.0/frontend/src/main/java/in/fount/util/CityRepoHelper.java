package in.fount.util;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

public class CityRepoHelper {

    private static final Set<String> VALID_CITIES;

    static {
        String[] cityNames = new String[] { "nyc", "dc", "boston" };
        Set<String> set = new HashSet<String>(Arrays.asList(cityNames));
        VALID_CITIES = Collections.unmodifiableSet(set);
    }

    // This is used for the /pollutions page
    public static boolean isValidCity(String s) {
        return VALID_CITIES.contains(s);
    }

}
