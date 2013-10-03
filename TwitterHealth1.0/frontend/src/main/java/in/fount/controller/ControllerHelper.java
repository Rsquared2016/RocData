package in.fount.controller;

import org.springframework.web.servlet.ModelAndView;

public class ControllerHelper {

    public static ModelAndView buildPage(String title, String include) {
        ModelAndView temp = new ModelAndView("index");
        temp.addObject("title", title);
        temp.addObject("include", include);
        return temp;
    }

}
