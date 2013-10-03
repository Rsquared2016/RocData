package in.fount.tools;

import javax.mail.Message;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import javax.mail.PasswordAuthentication;
import java.util.Properties;

public class EmailAccess{
	//helper functions
	@SuppressWarnings("unused")
    private static String getValidationCode(int n){
		StringBuffer sb = new StringBuffer(n);  
		int c = 'A';  
		for (int i = 0; i < n; i++) {  
			switch ((int) (Math.random() * 3)) {  
				case 0:  c = '0' + (int) (Math.random() * 10);break;  
				case 1:  c = 'a' + (int) (Math.random() * 26);break;  
				case 2:  c = 'A' + (int) (Math.random() * 26);break;  
			}
		sb.append( (char) c );
		}
		return sb.toString();
	}

	// --- contact form
	public static void sendContact(String name, String email, String phone, String website, String message){
		InternetAddress from=new InternetAddress();
		try{from = new InternetAddress("team@fount.in");
		from.setPersonal("Fount.in");}
		catch(Exception e){}
		StringBuilder emailContent= new StringBuilder();
		emailContent.append("Hey "+name+" wants to hear back from us\n\n");
		emailContent.append(name+"\n");
		emailContent.append(email+"\n");
		emailContent.append(phone+"\n");
		emailContent.append(website+"\n");
		emailContent.append("--------------------------------------------------\n");
		emailContent.append(message+"\n");
		send("team@fount.in",from,"Contact Request from : "+name, emailContent.toString());
	}

	// --- email factory
	private static void send(String to, InternetAddress from, String subject,  String content) {
		Properties props = new Properties();
		props.put("mail.smtp.auth", "true");
		props.put("mail.smtp.port", "465");
		props.put("mail.smtp.socketFactory.port", "465");
		props.put("mail.smtp.host", "smtp.gmail.com");
		props.put("mail.smtp.socketFactory.class","javax.net.ssl.SSLSocketFactory");
		Session mailSession = Session.getInstance(props,
			new javax.mail.Authenticator() {
				protected PasswordAuthentication getPasswordAuthentication() {
					return new PasswordAuthentication("team@fount.in","fountinspews");
		}});	 
		try{
			Message msg = new MimeMessage(mailSession);				
			msg.setFrom(from);
			msg.addRecipient(Message.RecipientType.TO, new InternetAddress(to));
			msg.setSubject(subject);
			msg.setText(content);
			Transport.send(msg);
		}catch (Exception e) {//TODO: log errors
		}
	}
	
}