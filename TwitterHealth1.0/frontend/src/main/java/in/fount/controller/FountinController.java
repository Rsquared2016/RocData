package in.fount.controller;

import static in.fount.controller.ControllerHelper.buildPage;
import in.fount.tools.EmailAccess;

import javax.servlet.http.HttpSession;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class FountinController {

    // ------------------- Common Resources ---------------------------
    @RequestMapping(value = "/favicon", method = RequestMethod.GET)
    public ModelAndView getFavicon() {
        return new ModelAndView();
    }

    @RequestMapping(value = "/debug", method = RequestMethod.GET)
    public ModelAndView getDebug() {
        return new ModelAndView();
    }

    @RequestMapping(value = { "/labs" }, method = RequestMethod.GET)
    public ModelAndView goToLabs() {
        return buildPage("TwitterHealth", "pollution.jsp").addObject("api",
                "pollution").addObject("defaultCity", "nyc");
    }

    // ------------------- Home Page ----------------------------------
    @RequestMapping(value = { "/" }, method = RequestMethod.GET)
    public ModelAndView fountinHome(@RequestHeader("Host") String host) {
        if (host.contains("m.fount.in")) {
            return new ModelAndView("forward:/mobile");
        } else {
            return buildPage("Fount.in :: Health insights in realtime",
                    "../static/index.jsp");
        }
    }

    // --------------------- About -----------------------------------
    @RequestMapping(value = { "/about" }, method = RequestMethod.GET)
    public ModelAndView aboutFountin(@RequestHeader("Host") String host) {
        return buildPage("About Fount.in", "../static/about.jsp");
    }

    // -------------------- Contact -----------------------------
    @RequestMapping(value = "/contact", method = RequestMethod.POST)
    public ModelAndView sendContact(
            @RequestParam(value = "name", required = true) String name,
            @RequestParam(value = "email", required = true) String email,
            @RequestParam(value = "phone", required = true) String phone,
            @RequestParam(value = "message", required = true) String message,
            @RequestParam(value = "leaveblank", required = true) String leaveblank,
            HttpSession session) {

        EmailAccess.sendContact(name, email, phone, "", message);
        return buildPage(name + "'s Contact", "static/contact.jsp").addObject(
                "message", "Ok, we got it. You'll hear back from us soon!");
    }

    @RequestMapping(value = { "/contact" }, method = RequestMethod.GET)
    public ModelAndView contactUs(@RequestHeader("Host") String host) {
        return buildPage("Contact us at Fount.in", "../static/contact.jsp");
    }

    // --------------------- Research -------------------------------
    @RequestMapping(value = { "/research" }, method = RequestMethod.GET)
    public ModelAndView researchFountin(@RequestHeader("Host") String host) {
        return buildPage("Fount.in's Research", "../static/research.jsp");
    }

}
