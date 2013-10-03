package in.fount.model.diseases;

import java.util.ArrayList;
import java.util.List;

/**
 * raw counts format:
 * 
 * <pre>
 * values = [
 *     [term1/disease1, sum1],
 *     [term2/disease2, sum2],
 *     ...
 * ]
 * </pre>
 * 
 * format for histogram processing
 * 
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
public class Statistics {

    /**
     * <pre>
     * values = [
     *     [term1/disease1, sum1],
     *     [term2/disease2, sum2],
     *     ...
     * ]
     * </pre>
     */
    private List<List<?>> categoryCounts = new ArrayList<List<?>>();

    /**
     * <pre>
     * values = [
     *     [term1/disease1, sum1],
     *     [term2/disease2, sum2],
     *     ...
     * ]
     * </pre>
     */
    private List<List<?>> termCounts = new ArrayList<List<?>>();

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
    private HistStats histStats = new HistStats();

    private List<DiseaseTweetLightweight> tweetSample = new ArrayList<DiseaseTweetLightweight>();

    public List<List<?>> getCategoryCounts() {
        return categoryCounts;
    }

    public HistStats getHistStats() {
        return histStats;
    }

    public List<List<?>> getTermCounts() {
        return termCounts;
    }

    public List<DiseaseTweetLightweight> getTweetSample() {
        return tweetSample;
    }

}
