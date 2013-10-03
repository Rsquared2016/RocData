package in.fount.controller;

import in.fount.service.HealthRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class SocialController {

    private static final String TITLE = "TwitterHealth :: Social";

    @Autowired
    private HealthRepository healthRepo;

    // ------------------- Social Connection Page ---------------------
    @RequestMapping(value = { "/dev1", "/social" }, method = RequestMethod.GET)
    public ModelAndView viewSocial() {
        ModelAndView view = new ModelAndView("social");

        view.addObject("title", TITLE);
        view.addObject("page", healthRepo.getAll());

        return view;
    }
}
