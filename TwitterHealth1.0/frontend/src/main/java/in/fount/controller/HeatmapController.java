package in.fount.controller;

import static in.fount.util.CalendarUtils.formatDateIso;
import static in.fount.util.CalendarUtils.isSameDay;
import in.fount.model.Tweet;
import in.fount.model.heatmap.DataPoint;
import in.fount.service.HealthRepository;
import in.fount.util.CalendarUtils;

import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.format.annotation.DateTimeFormat.ISO;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class HeatmapController {

    private static final String TITLE = "TwitterHealth :: Heatmap";

    @Autowired
    private HealthRepository healthRepo;

    @RequestMapping(value = "/heatmap", method = RequestMethod.GET)
    public String viewHeatmap() {
        List<Date> uniqueDays = healthRepo.getAvailableDays();

        if (uniqueDays.isEmpty())
            return "errors/nodata";

        return "redirect:/heatmap/"
                + formatDateIso(uniqueDays.get(uniqueDays.size() - 1));
    }

    @RequestMapping(value = "/heatmap/{day}", method = RequestMethod.GET)
    public ModelAndView viewHeatmapByDay(
            @PathVariable @DateTimeFormat(iso = ISO.DATE) Date day) {
        ModelAndView view = new ModelAndView("heatmap");
        view.addObject("title", TITLE);

        int index = -1;
        boolean dayFound = false;
        List<Date> availableDays = healthRepo.getAvailableDays();
        Iterator<Date> iterator = availableDays.iterator();
        while (!dayFound && iterator.hasNext()) {
            index++;
            Date d = iterator.next();
            if (isSameDay(day, d)) {
                dayFound = true;
                break;
            }
        }

        if (dayFound) {
            view.addObject("currentDay", formatDateIso(day));

            if (index > 0)
                view.addObject("previousDay", CalendarUtils
                        .formatDateIso(availableDays.get(index - 1)));

            if (index < availableDays.size() - 1)
                view.addObject("nextDay", CalendarUtils
                        .formatDateIso(availableDays.get(index + 1)));
        } else {
            view.setViewName("errors/nodata");
        }

        return view;
    }

    @RequestMapping(value = "/heatmap/{day}/data", method = RequestMethod.GET)
    public @ResponseBody
    List<DataPoint> getDataSetByDay(
            @PathVariable @DateTimeFormat(iso = ISO.DATE) Date day) {

        List<Tweet> list = healthRepo.getTweetsByDay(day);

        List<DataPoint> result = new ArrayList<DataPoint>();

        for (Tweet tweet : list) {
            DataPoint dataPoint = new DataPoint();
            dataPoint.setLat(tweet.getLat());
            dataPoint.setLng(tweet.getLon());
            dataPoint.setCreatedAt(CalendarUtils.parseTweetDate(tweet
                    .getCreated_at()));
            dataPoint.setCount(tweet.getHealth());
            result.add(dataPoint);
        }

        return result;
    }

}
