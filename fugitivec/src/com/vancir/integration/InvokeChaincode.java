package com.vancir.integration;

import java.util.Map;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Scanner;
import static java.nio.charset.StandardCharsets.UTF_8;

import com.vancir.manager.CAManager;
import com.vancir.manager.ChannelManager;
import com.vancir.manager.FabricManager;
import com.vancir.user.AppUser;
import com.vancir.utilities.Config;
import com.vancir.utilities.Util;

import org.apache.log4j.Logger;
import org.hyperledger.fabric.sdk.ChaincodeID;
import org.hyperledger.fabric.sdk.Channel;
// import org.hyperledger.fabric.sdk.EventHub;
import org.hyperledger.fabric.sdk.Orderer;
import org.hyperledger.fabric.sdk.Peer;
import org.hyperledger.fabric.sdk.TransactionProposalRequest;
public class InvokeChaincode {
    
    private static Logger logger = Logger.getLogger(InvokeChaincode.class); 

    // private static final byte[] EXPECTED_EVENT_DATA = "!".getBytes(UTF_8);
    // private static final String EXPECTED_EVENT_NAME = "event";

    public static void main(String[] args) {
        try {
            AppUser org1Admin = Util.getOrgUser(Config.ADMIN, Config.ORG1_MSP);
            CAManager caManager = new CAManager(Config.CA_ORG1_URL, null);
            caManager.setAdminUser(org1Admin);
            org1Admin = caManager.enrollUser(org1Admin, Config.ADMINPW);

            FabricManager fabricManager = new FabricManager(org1Admin);
            ChannelManager channelManager = fabricManager.createChannelManager(Config.CHANNEL_NAME);
            Channel channel = channelManager.getChannel();
            Peer peer = fabricManager.getHfclient().newPeer(Config.PEER0_ORG1_NAME, Config.PEER0_ORG1_URL);
            // EventHub eventHub = fabricManager.getHfclient().newEventHub(Config.EVENTHUB_NAME, Config.EVENTHUB_URL);
            Orderer orderer = fabricManager.getHfclient().newOrderer(Config.ORDERER_NAME, Config.ORDERER_URL);

            channel.addPeer(peer);
            // channel.addEventHub(eventHub);
            channel.addOrderer(orderer);
            channel.initialize();

            TransactionProposalRequest request = fabricManager.getHfclient().newTransactionProposalRequest();
            ChaincodeID chaincodeID = ChaincodeID.newBuilder().setName(Config.CHAINCODE_NAME).build();
            
            request.setChaincodeID(chaincodeID);   
            request.setFcn("init");
            // init <string ID> <string name> <string sex> <int age> <bool isFleeing> <String description>
            String[] arguments = { "ID001", "Alice", "Female", "20", "true", "Alice is not fugitive" };
            request.setArgs(arguments);
            request.setProposalWaitTime(1000);

            Map<String, byte[]> transMap = new HashMap<>();
            transMap.put("HyperLedgerFabric", "TransactionProposalRequest:JavaSDK".getBytes(UTF_8));
            transMap.put("method", "TransactionProposalRequest".getBytes(UTF_8));
            transMap.put("result", ":)".getBytes(UTF_8));
            // transMap.put(EXPECTED_EVENT_NAME, EXPECTED_EVENT_DATA);
            request.setTransientMap(transMap);

            // String[] testInitArgs = { "ID001", "Alice", "Female", "20", "true", "Alice is not fugitive" };
            // channelManager.invokeChaincode(Config.CHAINCODE_NAME, "init", testInitArgs);
            
            String[] testAddArgs = { "ID002", "Peter", "Male", "19", "false", "Perter is a good boy" };
            channelManager.invokeChaincode(Config.CHAINCODE_NAME, "add", testAddArgs);
            
            logger.info("Please input your command.");
            // add ID003 Sam Female 22 true Sam_is_not_good
            // delete ID003
            // query ID002
            // update ID002 Alice_is_fugitive
            Scanner sc = new Scanner(System.in);
            while(sc.hasNextLine()) {
                String inputLine = sc.nextLine();
                // logger.info(inputLine);

                String[] inputArray = inputLine.split(" ");
                String opt = inputArray[0];
                String[] inputArgs = new String[inputArray.length-1];
                for (int i=1; i<inputArray.length; i++) {
                    inputArgs[i-1] = inputArray[i];
                }


                logger.info("Your opt is: " + opt + " and your args is: " + Arrays.toString(inputArgs));
                channelManager.invokeChaincode(Config.CHAINCODE_NAME, inputArray[0], inputArgs);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}