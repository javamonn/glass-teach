import java.util.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.*;

public class teacher {
	
		public static String SHARED_FILE_PATH = "";

	    public static void main(String[] args) {
	    	connectToPhone();
	    }

	    /**
	     * Loops every couple of seconds, attempts to connect to a phone over usb
	     * TODO: Make this more effecient by checking output of 'adb devices'
	     */
	    public static void connectToPhone() {
	        Socket socket;
			try {
				socket = new Socket("localhost", 38300);
				//try for a little bit, sleep for awhile if nothing pops up
				System.out.println("opened socket");
		        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
		        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		        System.out.println("opened streams");
		        String line;
		        while ((line = in.readLine()) != null) {
		        	if (line.equals("break")) {
		        		break;
		        	}
		        	if (line.equals("ping")) {
		        		System.out.println("ping");
		        		continue;
		        	}
		        	if (line.equals("monitor off") || line.equals("monitor on")) {
		        		//write to shared file to turn off monitors
		        		File tempFile = File.createTempFile("temp", ".txt");
		        			
		        		FileWriter writer = new FileWriter(tempFile);
		        		writer.write("monitor=");
		        		writer.write(line.equals("monitor off") ? "off" : "on");
		        		writer.write("\n");
		        		writer.flush();
		        		writer.close();
		        		tempFile.renameTo(new File(SHARED_FILE_PATH));
		        		System.out.println("monitor off");
		        	}
		        	//not sure if I have to sleep here?
		        }
		        System.out.println("loop over");
		        
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	        
	    }

}
