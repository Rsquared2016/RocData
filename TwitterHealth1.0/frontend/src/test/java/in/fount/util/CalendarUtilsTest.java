package in.fount.util;

import static junit.framework.Assert.assertEquals;

import java.util.Calendar;
import java.util.Date;

import org.junit.Test;

public class CalendarUtilsTest {

    @Test
    public void testParseDate() {
        Date date = CalendarUtils.newDate(2012, 4, 27);

        Calendar cal = Calendar.getInstance();
        cal.setTime(date);

        assertEquals(2012, cal.get(Calendar.YEAR));
        assertEquals(4, cal.get(Calendar.MONTH));
        assertEquals(27, cal.get(Calendar.DAY_OF_MONTH));
    }

}
