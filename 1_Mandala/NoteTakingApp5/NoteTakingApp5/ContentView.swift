import SwiftUI

struct ContentView: View {
    @Binding var conversation: Conversation
    @State private var currentMessage: String = ""
    @State private var title: String = "Untitled"
    @State private var navigateToNewPage: Bool = false
    
    var body: some View {
        VStack(alignment: .leading) {
            TextField("Title", text: $conversation.title)
                .font(.title)
                .fontWeight(.bold)
                .padding(.vertical, 10)
                .padding(.horizontal, 30)
            ScrollView {
                ForEach(conversation.messages, id: \.self) { message in
                    MessageView(message: message)
                }
            }

            VStack {
                TextView(text: $currentMessage)
                    .frame(height: 200)
                    .cornerRadius(10)
                Button(action: sendMessage) {
                    Text("Send")
                        .foregroundColor(.white)
                        .padding(.horizontal, 50)
                        .padding(.vertical, 5)
                        .background(Color.purple)
                        .cornerRadius(10)
                }
                .foregroundColor(.purple) // Change button color to purple
                .frame(maxWidth: .infinity, alignment: .trailing) // Align button to the left
            }
            .padding()
        }
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {}) { // Placeholder action
                    Image(systemName: "bell")
                }
            }
            ToolbarItem(placement: .navigationBarLeading) {
                Button(action: {}) { // Placeholder action
                    Image(systemName: "paperplane")
                }
            }
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {}) { // Placeholder action
                    Image(systemName: "square.and.arrow.up")
                }
            }
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {}) { // Placeholder action
                    Image(systemName: "pencil")
                }
            }
        }
        .accentColor(.purple)
    }
    
    func sendMessage() {
        // Append the user's message to the conversation thread
        conversation.messages.append(Message(content: currentMessage, isUser: true))
        
        // Prepare the URL and request
        guard let url = URL(string: "http://localhost:5001/api/ask") else {
            print("Invalid URL")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let jsonData = try? JSONEncoder().encode(["text": currentMessage])
        request.httpBody = jsonData

        // Send the request
        URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    // Handle the error
                    print("Error: \(error)")
                } else if let data = data {
                    // Decode the JSON response and add the assistant's reply to the conversation thread
                    if let decodedResponse = try? JSONDecoder().decode([String: String].self, from: data),
                        let assistantReply = decodedResponse["assistant"] {
                        DispatchQueue.main.async {
                            conversation.messages.append(Message(content: assistantReply, isUser: false))
                            self.navigateToNewPage = true  // Set the navigation trigger
                        }
                    }
                }
            }.resume()

        // Clear the current message
        currentMessage = ""
    }
}
