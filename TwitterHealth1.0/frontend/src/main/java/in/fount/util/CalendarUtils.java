package in.fount.util;

import in.fount.model.Tweet;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

import org.joda.time.DateTimeZone;
import org.joda.time.LocalDate;
import org.joda.time.ReadableInstant;
import org.joda.time.format.DateTimeFormatter;
import org.joda.time.format.ISODateTimeFormat;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CalendarUtils {

    private static final Logger log = LoggerFactory
            .getLogger(CalendarUtils.class);

    private static final String ISO_DATE_PATTERN = "yyyy-MM-dd";

    private static final String SLASH_DATE_PATTERN = "MM/dd/yyyy";

    private static final String TWEET_CREATED_AT_PATTERN = "EEE, dd MMM yyyy HH:mm:ss Z";

    public static final long DAY_IN_MILLIS = 1000 * 60 * 60 * 24;

    public static final long HOUR_IN_MILLIS = 1000 * 60 * 60;

    public static final DateTimeZone EDT_TIME_ZONE = DateTimeZone
            .forID("Etc/GMT+4");

    private static ThreadLocal<SimpleDateFormat> SDF_ISO_DATE = new ThreadLocal<SimpleDateFormat>() {
        protected SimpleDateFormat initialValue() {
            return new SimpleDateFormat(ISO_DATE_PATTERN);
        };
    };

    private static ThreadLocal<SimpleDateFormat> SDF_SLASH_DATE = new ThreadLocal<SimpleDateFormat>() {
        protected SimpleDateFormat initialValue() {
            return new SimpleDateFormat(SLASH_DATE_PATTERN);
        };
    };

    private static ThreadLocal<DateFormat> DATE_FORMATTER = new ThreadLocal<DateFormat>() {
        protected DateFormat initialValue() {
            return new SimpleDateFormat(TWEET_CREATED_AT_PATTERN,
                    Locale.ENGLISH);
        };
    };

    public static SimpleDateFormat getIsoDateFormat() {
        return SDF_ISO_DATE.get();
    }

    private static final DateTimeFormatter ISO_DATE_FORMATTER = ISODateTimeFormat
            .yearMonthDay();

    /**
     * @param year
     * @param month
     *            January starts from 0
     * @param day
     * @return
     */
    public static Date newDate(int year, int month, int day) {
        Calendar cal = Calendar.getInstance();

        cal.set(Calendar.YEAR, year);
        cal.set(Calendar.MONTH, month);
        cal.set(Calendar.DAY_OF_MONTH, day);

        return cal.getTime();
    }

    public static Date newDate(int year, int month, int day, int hour) {
        Calendar cal = Calendar.getInstance();

        cal.set(Calendar.YEAR, year);
        cal.set(Calendar.MONTH, month);
        cal.set(Calendar.DAY_OF_MONTH, day);
        cal.set(Calendar.HOUR_OF_DAY, hour);

        return cal.getTime();
    }

    public static Date newDate(long millis) {
        Calendar cal = Calendar.getInstance();
        cal.setTimeInMillis(millis);
        return cal.getTime();
    }

    /**
     * Formats a given <code>date</code> using yyyy-MM-dd mask.
     * 
     * @param date
     * @return
     * 
     * @see #ISO_DATE_PATTERN
     */
    public static String formatDateIso(Date date) {
        return SDF_ISO_DATE.get().format(date);
    }

    public static String formatDateTimeIso(ReadableInstant date) {
        return ISO_DATE_FORMATTER.print(date);
    }

    public static String formatLocalDateIso(LocalDate date) {
        return ISO_DATE_FORMATTER.print(date);
    }

    /**
     * Formats a given <code>date</code> using MM/dd/yyyy mask.
     * 
     * @param date
     * @return
     * 
     * @see #SLASH_DATE_PATTERN
     */
    public static String formatDateSlash(Date date) {
        return SDF_SLASH_DATE.get().format(date);
    }

    /**
     * Formats a given <code>date</code> using EEE, dd MMM yyyy HH:mm:ss Z mask.
     * 
     * @param date
     * @return
     */
    public static String formatDateTweetCreatedAt(Date date) {
        return DATE_FORMATTER.get().format(date);
    }

    public static int getYear(Date date) {
        return getFieldValue(date, Calendar.YEAR);
    }

    /**
     * January is represented by 0.
     * 
     * @param date
     * @return
     */
    public static int getMonth(Date date) {
        return getFieldValue(date, Calendar.MONTH);
    }

    public static int getDay(Date date) {
        return getFieldValue(date, Calendar.DAY_OF_MONTH);
    }

    public static int getHour(Date date) {
        return getFieldValue(date, Calendar.HOUR_OF_DAY);
    }

    private static int getFieldValue(Date date, int field) {
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        return cal.get(field);
    }

    public static boolean isSameDay(Date date1, Date date2) {

        boolean sameYear = getYear(date1) == getYear(date2);
        boolean sameMonth = getMonth(date1) == getMonth(date2);
        boolean sameDay = getDay(date1) == getDay(date2);

        return sameYear && sameMonth && sameDay;
    }

    public static boolean isSameDay(LocalDate date1, LocalDate date2) {
        return date1.compareTo(date2) == 0;
    }

    /**
     * Parses a {@link Date} object following format used by {@link Tweet}'s
     * <code>created_at</code> attribute.
     * 
     * @param dateString
     * @return parsed date
     */
    public static Date parseTweetDate(String dateString) {
        try {
            Date date = DATE_FORMATTER.get().parse(dateString);
            if (log.isTraceEnabled())
                log.trace("parsed Date {} from string {}", date, dateString);
            return date;
        } catch (ParseException e) {
            throw new RuntimeException("couldn't parse Date from string "
                    + dateString, e);
        }
    }

}
