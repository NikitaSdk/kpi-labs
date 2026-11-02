package OperationwithDB;

import com.mongodb.client.*;
import com.mongodb.client.model.Filters;
import com.mongodb.client.result.UpdateResult;
import org.bson.Document;
import org.bson.types.ObjectId;

import java.util.Scanner;


public class WorkWithMongoDB {
    public static void main(String[] args) {
        try (MongoClient mongoClient = MongoClients.create("mongodb://localhost:27017")) {
            MongoDatabase database = mongoClient.getDatabase("faculties");
            MongoCollection<Document> collection = database.getCollection("facultyCollection");

            // Example: Read all documents from the collection
            readAllDocuments(collection);

            // Check if the user wants to update Places and/or decrease People
            Scanner scanner = new Scanner(System.in);
            System.out.print("Enter 1 to increase number of people, 2 to decrease People: ");
            int userInput = scanner.nextInt();

            if (userInput == 1) {
                // Get the _id from the user
                System.out.print("Enter the _id to update number of people: ");
                scanner.nextLine(); // Consume the newline character
                String documentId = scanner.nextLine();

                // Update the "People" field for the specified document
                updateFields(collection, documentId, 1);
                System.out.println("Updated People for document with _id " + documentId + ".");
            } else if (userInput == 2) {
                // Get the _id from the user
                System.out.print("Enter the _id to decrease number of people: ");
                scanner.nextLine(); // Consume the newline character
                String documentId = scanner.nextLine();

                // Decrease the "People" field for the specified document
                updateFields(collection, documentId, -1);
                System.out.println("Decreased People for document with _id " + documentId + ".");
            }

            // Read all documents again to verify the update or decrease
            readAllDocuments(collection);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    private static void readAllDocuments(MongoCollection<Document> collection) {
        MongoCursor<Document> cursor = collection.find().iterator();
        while (cursor.hasNext()) {
            Document document = cursor.next();
            System.out.println(document.toJson());
        }
    }
    private static void updateFields(MongoCollection<Document> collection, String documentId, int deltaPeople) {
        try {
            // You can modify this method to update or decrease the "People" field based on your requirements
            Document filter = new Document("_id", documentId);
            Document update = new Document("$inc", new Document("People", deltaPeople));

            UpdateResult result = collection.updateOne(filter, update);

            // Check if the update or decrease was successful
            if (result.getModifiedCount() == 0) {
                System.out.println("No document found with _id " + documentId + ". Update or decrease failed.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
