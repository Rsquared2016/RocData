import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.WindowConstants;

public class newDatabase extends JFrame{
	JPanel panel;
	JPanel pnlDisplay;
	JPanel pnlSettings;
	public newDatabase(){
		panel = new JPanel();
		panel.setLayout(null);	
		final JTextField txt1 = new JTextField();
		txt1.setSize(200,20);
		txt1.setLocation(170,50);
		panel.add(txt1);
		this.setResizable(false);
		
		
		
		JButton findFile = new JButton("Browse");
		findFile.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				JFileChooser getDataFile = new JFileChooser();
				getDataFile.setMultiSelectionEnabled(false);
				int option = getDataFile.showOpenDialog(newDatabase.this);
				if(option ==JFileChooser.APPROVE_OPTION){
					File dataFile = getDataFile.getSelectedFile();
					txt1.setText(dataFile.getPath());
				}
				else
				{
					
				}
			}
		});
		findFile.setSize(80,20);
		findFile.setLocation(400,50);
		panel.add(findFile);
		
		
		final JTextField txt2 = new JTextField();
		txt2.setSize(200,20);
		txt2.setLocation(170,90);
		panel.add(txt2);
		
		JButton findFile2 = new JButton("Browse");
		findFile2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				JFileChooser getDataFile = new JFileChooser();
				getDataFile.setMultiSelectionEnabled(false);
				int option = getDataFile.showOpenDialog(newDatabase.this);
				if(option ==JFileChooser.APPROVE_OPTION){
					File dataFile = getDataFile.getSelectedFile();
					txt2.setText(dataFile.getPath());
				}
				else
				{
					
				}
			}
		});
		findFile2.setSize(80,20);
		findFile2.setLocation(400,90);
		panel.add(findFile2);
		
		final JTextField txt3 = new JTextField();
		txt3.setSize(200,20);
		txt3.setLocation(170,130);
		panel.add(txt3);
		
		JButton findFile3 = new JButton("Browse");
		findFile3.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				JFileChooser getDataFile = new JFileChooser();
				getDataFile.setMultiSelectionEnabled(false);
				int option = getDataFile.showOpenDialog(newDatabase.this);
				if(option ==JFileChooser.APPROVE_OPTION){
					File dataFile = getDataFile.getSelectedFile();
					txt3.setText(dataFile.getPath());
				}
				else
				{
					
				}
			}
		});
		findFile3.setSize(80,20);
		findFile3.setLocation(400,130);
		panel.add(findFile3);
		
		final JTextField txt4 = new JTextField();
		txt4.setSize(200,20);
		txt4.setLocation(170,170);		
		panel.add(txt4);
		
		JButton findFile4 = new JButton("Browse");
		findFile4.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				JFileChooser getDataFile = new JFileChooser();
				getDataFile.setMultiSelectionEnabled(false);
				int option = getDataFile.showOpenDialog(newDatabase.this);
				if(option ==JFileChooser.APPROVE_OPTION){
					File dataFile = getDataFile.getSelectedFile();
					txt4.setText(dataFile.getPath());
				}
				else
				{
					
				}
			}
		});
		findFile4.setSize(80,20);
		findFile4.setLocation(400,170);
		panel.add(findFile4);
		
		JLabel File1 = new JLabel("First Database File:");
		File1.setSize(130,20);
		File1.setLocation(52,50);
		File1.setVisible(true);
		panel.add(File1);
		
		JLabel File2 = new JLabel("Second Database File:");
		File2.setSize(130,20);
		File2.setLocation(34,90);
		File2.setVisible(true);
		panel.add(File2);
		
		JLabel File3 = new JLabel("Third Database File:");
		File3.setSize(130,20);
		File3.setLocation(48,130);
		File3.setVisible(true);
		panel.add(File3);
		
		JLabel File4 = new JLabel("Fourth Database File:");
		File4.setSize(130,20);
		File4.setLocation(42,170);
		File4.setVisible(true);
		panel.add(File4);
		
		JLabel Heading = new JLabel("Browse for Database Files:");
		Heading.setSize(160,20);
		Heading.setLocation(190,20);
		Heading.setVisible(true);
		panel.add(Heading);
		
		

		JButton AddDatabases = new JButton("Add Databases");
		AddDatabases.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				
			}
		});
		AddDatabases.setSize(130,20);
		AddDatabases.setLocation(100,210);
		panel.add(AddDatabases);
		

		JButton btnCancel = new JButton("Cancel");
		btnCancel.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				newDatabase.this.setVisible(false);
			}
		});
		btnCancel.setSize(130,20);
		btnCancel.setLocation(320,210);
		panel.add(btnCancel);
		
		this.add(panel);
		
	}

}
