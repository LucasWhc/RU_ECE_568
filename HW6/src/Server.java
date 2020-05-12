import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Base64;


public class Server {
    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.err.println("Error: server port number not given");
            System.exit(1);
        }
        int portNum = Integer.parseInt(args[0]);
        ServerSocket rvSock = null;
        try {
            rvSock = new ServerSocket(portNum);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        while (true) {
            System.out.println("Waiting for commands...");
            try {
                Socket sSock = rvSock.accept();
                System.out.println("Connected to one client!");
                BufferedReader in = new BufferedReader(new InputStreamReader(sSock.getInputStream()));
                PrintWriter out = new PrintWriter(new OutputStreamWriter(sSock.getOutputStream()), true);
                String cmd = in.readLine();
                out.println("Command received!");
                if (checkCmd(cmd, out)) {
                    execCmd(cmd, out);
                } else {
                    out.println("Wrong command!");
                }
                sSock.close();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }

    private static void execCmd(String cmd, PrintWriter out) {
        String[] newCmd = cmd.split(" ");
        switch (newCmd[0]) {
            case "Exit":
                if (newCmd.length == 2) {
                    System.out.println("Message from clients: " + newCmd[1]);
                }
                out.println("See you!");
                System.out.println("Disconnected from one client!");
                break;
            case "BOUNCE":
                System.out.println("Message from clients: " + newCmd[1]);
                out.println("\n");
                break;
            case "GET":
                InputStream in = null;
                byte[] data = null;
                try {
                    in = new FileInputStream(newCmd[1]);
                    data = new byte[in.available()];
                    in.read(data);
                    in.close();
                    out.println("FILE");
                    out.println(new String(Base64.getEncoder().encode(data)));
                    System.out.println("The client is triyng to get the content of " + newCmd[1]);
                } catch (IOException e) {
                    out.println("Error: no such file");
                    System.out.println("The client is trying to get a file that doesn't exist.");
                }
        }
    }

    private static boolean checkCmd(String cmd, PrintWriter out) {
        boolean temp = true;
        if (cmd == null){
            return false;
        }
        String[] newCmd = cmd.split(" ");
        if (newCmd[0].equals("\n") || newCmd[0].equals("")) {
            temp = false;
        } else if (newCmd.length > 2) {
            temp = false;
        } else if (!newCmd[0].equals("GET") && !newCmd[0].equals("BOUNCE") && !newCmd[0].equals("EXIT")) {
            temp = false;
        } else if (newCmd[0].equals("GET") || newCmd[0].equals("BOUNCE")) {
            if (newCmd.length != 2) {
                temp = false;
            }
        }
        return temp;
    }
}
