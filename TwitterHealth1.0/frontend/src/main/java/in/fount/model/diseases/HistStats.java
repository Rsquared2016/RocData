package in.fount.model.diseases;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * <pre>
 * date: Thu, 17 May 2012 20:04:28 +0000
 * dstr: Thu, 17 May 2012 20
 * 
 * values = {
 *     rows: [
 *         {key: [disease1, term1, dstr1], value: sum1},
 *         {key: [disease2, term2, dstr2], value: sum2},
 *         ...
 *     ]
 * }
 * </pre>
 */
public class HistStats {

    private List<Map<String, Object>> rows = new ArrayList<Map<String, Object>>();

    public List<Map<String, Object>> getRows() {
        return rows;
    }

}
