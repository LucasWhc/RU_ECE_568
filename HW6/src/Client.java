import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Base64;

public class Client {
    public static void main(String[] args) {
        if (args.length != 2) { // Test for correct num. of arguments
            System.err.println("ERROR: server host name and port number not given");
            System.exit(1);
        }
        int portNum = Integer.parseInt(args[1]);
        while (true) {
            try {
                Socket cSock = new Socket(args[0], portNum);
                BufferedReader in = new BufferedReader(new InputStreamReader(cSock.getInputStream()));
                PrintWriter out = new PrintWriter(new OutputStreamWriter(cSock.getOutputStream()), true);
                BufferedReader userEntry = new BufferedReader(new InputStreamReader(System.in));
                String cmd = "";
                while(!checkCmd(cmd)){
                    System.out.print("\nType in the command: ");
                    cmd = userEntry.readLine().trim();
                }
                out.println(cmd);
                String response = in.readLine();
                System.out.println(response);
                response = in.readLine();
                if (response.equals("See you!")) {
                    cSock.close();
                    System.out.println(response);
                    System.out.println("Disconnected from the server!");
                    System.exit(0);
                } else if(response.equals("    Invalid command.")) {
                    help();
                    cSock.close();
                    continue;
                } else if(response.equals("FILE")){
                    response = in.readLine(); //get the Base64 codes of file content
                    System.out.println("\n******File content starts******");
                    //decode and output
                    System.out.println(new String(Base64.getDecoder().decode(response.getBytes())));
                    System.out.println("******File  content  ends******");
                    response = in.readLine();
                }
                if (response != null) {
                    System.out.println(response);
                }
                cSock.close();
            } catch (IOException ex) {
                System.out.println("Server is not online. Press Ctrl+C to stop reconnect.");
            }
        }
    }

        private static boolean checkCmd (String cmd){
            boolean temp = true;
            String[] newCmd = cmd.split(" ");
            if (newCmd[0].equals("\n") || newCmd[0].equals("")) { //empty input
                temp = false;
            } else if (newCmd.length > 2) {
                System.out.println("    Wrong command: too much parameters.");
                help();
                temp = false;
            } else if (!newCmd[0].equals("GET") && !newCmd[0].equals("BOUNCE") && !newCmd[0].equals("EXIT")) {
                System.out.println("    Unknown command.\n");
                help();
                temp = false;
            } else if (newCmd[0].equals("GET") || newCmd[0].equals("BOUNCE")) {
                if (newCmd.length != 2) {
                    System.out.println("    Missing parameters.");
                    help();
                    temp = false;
                }
            }
            return temp;
        }

        private static void help () {
            System.out.println("GET <filename>:\n"
                    + "Return the content of filename from the server");
            System.out.println("BOUNCE <msg>:\n"
                    + "Send a message to the server");
            System.out.println("EXIT [code]:\n"
                    + "Disconnect from server, and send a code to server (optional)");
            System.out.println();
        }
    }
