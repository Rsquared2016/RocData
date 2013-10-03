package in.fount.util;

import java.util.HashSet;
import java.util.Set;

public class CollectionUtils {

    public static <T> Set<T> arrayToSet(T[] array) {
        Set<T> set = new HashSet<T>();

        for (T t : array)
            set.add(t);

        return set;
    }

}
