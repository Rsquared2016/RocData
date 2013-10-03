package in.fount.controller;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

import in.fount.model.GPlace;
import in.fount.service.GooglePlacesRepository;

@Controller
public class ExperimentalController {

    private static Logger log = LoggerFactory
            .getLogger(ExperimentalController.class);

    @Autowired
    @Qualifier("parkRepository")
    private GooglePlacesRepository parkRepo;

    @Autowired
    @Qualifier("gymRepository")
    private GooglePlacesRepository gymRepo;

    @RequestMapping(value = "/experimental/distances", method = RequestMethod.GET)
    public ModelAndView viewExperimentalDistances() {
        ModelAndView mv = new ModelAndView();
        mv.setViewName("distances");
        return mv;
    }

    @RequestMapping(value = "/experimental/distances/{placeType}/data", method = RequestMethod.GET)
    public @ResponseBody
    List<GPlace> getExperimentalDistancesData(@PathVariable String placeType) {

        if (placeType == null || placeType.trim().equals("")) {
            return null;
        }

        List<GPlace> places = null;
        log.info("Querying database for google places of type {}", placeType);

        if (placeType.equals("park"))
            places = parkRepo.getAll();
        else if (placeType.equals("gym"))
            places = gymRepo.getAll();
        else {
            log.error("Unknown google place requested {}", placeType);
        }

        log.info("{} google places({}) returned from the database.",
                places.size(), placeType);

        return places;
    }

}
