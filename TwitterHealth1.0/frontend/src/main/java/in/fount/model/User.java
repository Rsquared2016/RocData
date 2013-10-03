package in.fount.model;

import java.util.ArrayList;

import org.codehaus.jackson.annotate.JsonIgnore;
import org.ektorp.support.CouchDbDocument;
import org.ektorp.support.TypeDiscriminator;
import org.jasypt.digest.StandardStringDigester;

public class User extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    /**
     * @TypeDiscriminator is used to mark properties that makes this class's
     *                    documents unique in the database.
     */
    @TypeDiscriminator
    private String name;
    private String fullname;
    private String type = "user";
    private String password;
    private String email;
    private ArrayList<String> roles = new ArrayList<String>();
    @JsonIgnore
    private String ok;
    @JsonIgnore
    private String userCtx;
    @JsonIgnore
    private String info;

    public ArrayList<String> getRoles() {
        return roles;
    }

    public String getName() {
        return name;
    }

    public void setName(String u) {
        roles.add("");
        this.setId("org.couchdb.user:" + u);
        name = u;
    }

    public String getFullname() {
        return this.fullname;
    }

    public void setFullname(String s) {
        fullname = s;
    }

    public String getPassword() {
        return this.password;
    }

    public void setPassword(String p) {
        password = p;
    }

    public void hashPassword(String s) {
        StandardStringDigester digester = new StandardStringDigester();
        digester.setAlgorithm("SHA-1");
        digester.setIterations(1);
        digester.setStringOutputType("hexadecimal");
        digester.setSaltSizeBytes(10);
        String digested = digester.digest(s).toLowerCase();
        password = digested;
    }

    public boolean validate(String s) {
        StandardStringDigester digester = new StandardStringDigester();
        digester.setAlgorithm("SHA-1");
        digester.setIterations(1);
        digester.setStringOutputType("hexadecimal");
        digester.setSaltSizeBytes(10);
        return digester.matches(s, getPassword());
    }

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String s) {
        email = s;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String s) {
        type = s;
    }

}