import java.util.*;
import java.net.*;

public class glass-teach-teacher {

    public static void main(String[] args) {

    }

    /**
     * Loops every couple of seconds, attempts to connect to a phone over usb
     * TODO: Make this more effecient by checking output of 'adb devices'
     */
    public static void connectToPhone() {
        Socket socket = new Socket("localhost", 38300);
        //try for a little bit, sleep for awhile if nothing pops up
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
        Scanner in = new Scanner(socket.getInputStream());
    }
}
